"""The acting loop: read -> decide -> pay -> act -> attest -> log.

One cycle of ASE. No human in the loop; every act is signed and auditable.
The decision function is deliberately simple and legible - judges (and the
human) must be able to read exactly why ASE acted.
"""
import time
from dataclasses import dataclass, field

from .config import Config, load_config
from .identity import make_attestation, sign_attestation
from .journal import append as journal_append
from .read import read_chain_state, read_subgraph, subgraph_available
from .wallet import Wallet


@dataclass
class CycleResult:
    ts: int
    block: int
    reading: dict
    decision: str
    paid: bool = False
    payment: dict = field(default_factory=dict)
    attestation_json: str = ""
    errors: list = field(default_factory=list)


def decide(reading) -> tuple[str, str]:
    """The legible policy. Returns (action, rationale).

    Threshold policy on the agent's own USDC balance:
    - balance below floor  -> "accumulate" (note it; faucet tops us up on testnet)
    - balance above target -> "report_surplus"
    - otherwise            -> "hold_and_observe"
    """
    bal = reading.data.get("human", 0.0)
    if bal < 1.0:
        return "accumulate", (f"USDC balance {bal:.2f} below floor 1.00 - "
                              f"requesting replenishment, no spend")
    if bal > 5.0:
        return "report_surplus", (f"USDC balance {bal:.2f} above target 5.00 - "
                                  f"flagging surplus for the human's review")
    return "hold_and_observe", f"USDC balance {bal:.2f} within band [1.00, 5.00]"


def run_cycle(config: Config, wallet: Wallet, w3, pay_fn=None) -> CycleResult:
    """One full acting cycle. pay_fn injectable for dry-run/testing."""
    result = CycleResult(ts=int(time.time()), block=0, reading={},
                         decision="", paid=False)

    # READ (chain state, block-stamped)
    reading = read_chain_state(config.rpc_url, config.usdc_address,
                               wallet.address)
    result.block = reading.block
    result.reading = {"kind": reading.kind, "block": reading.block,
                      **reading.data}

    # optional subgraph data path (The Graph track): when a URL and a query
    # are configured, ASE pulls live indexed data into the block-stamped
    # reading, so The Graph is load-bearing where it is wired. Errors never
    # kill the cycle; they are recorded honestly in the attestation.
    if config.subgraph_url and subgraph_available(config.subgraph_url):
        result.reading["subgraph"] = "reachable"
        if config.subgraph_query:
            try:
                result.reading["subgraph_data"] = read_subgraph(
                    config.subgraph_url, config.subgraph_query)
            except Exception as e:
                result.errors.append(f"subgraph: {e}")

    # DECIDE
    action, rationale = decide(reading)
    result.decision = f"{action}: {rationale}"

    # PAY (only when the policy says the data/action is worth paying for;
    # in cycle v1 the payment lane is exercised when a payee is configured
    # and the policy action is report_surplus - a tip to the data provider)
    if pay_fn is not None and config.has_payee and action == "report_surplus":
        try:
            pay = pay_fn()
            result.paid = True
            result.payment = pay
        except Exception as e:
            result.errors.append(f"pay: {e}")

    # ATTEST (sign what happened)
    att = make_attestation(
        agent_address=wallet.address, act="data_pay_cycle",
        ts=result.ts, block=result.block, decision=result.decision,
        payload={"reading": result.reading, "paid": result.paid,
                 "payment": result.payment, "errors": result.errors})
    signed = sign_attestation(att, wallet)
    result.attestation_json = signed.to_json()

    # JOURNAL (durable memory - survive restarts, full life record)
    journal_append({
        "kind": "cycle",
        "act": "data_pay_cycle",
        "agent": wallet.address,
        "block": result.block,
        "decision": result.decision,
        "paid": result.paid,
        "reading": result.reading,
        "payment": result.payment,
        "errors": result.errors,
        "attestation": result.attestation_json,
    })
    return result
