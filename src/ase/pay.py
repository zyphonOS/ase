"""PAY - x402-style payment for what ASE uses.

x402 is the HTTP-native payment protocol (status 402 = Payment Required).
ASE's version: when a data resource demands payment, ASE pays USDC onchain
and retries with a payment proof header. Real token transfer, real 402 flow.
"""
import json
from dataclasses import dataclass

import httpx
from web3 import Web3

from .read import ERC20_ABI

# Sepolia USDC (Circle native)
SEPOLIA_USDC = "0x1c7D4B196Cb0C7B01d743Fbc6116a902379C7238"
USDC_DECIMALS = 6


@dataclass
class PaymentProof:
    """What ASE hands to a resource after paying. Verifiable by anyone."""
    tx_hash: str
    amount_raw: int
    token: str
    resource: str
    ts: int


@dataclass
class Quote:
    """The resource's payment demand."""
    resource: str
    accepts: list
    raw_headers: dict


def fetch_with_payment(url: str, wallet, w3: Web3, max_usdc: float = 0.01,
                       usdc_address: str = SEPOLIA_USDC,
                       payee_address: str = "") -> dict:
    """GET a URL; if it answers 402 with payment demands, pay USDC and retry.

    Real flow: GET -> 402 + demands -> onchain USDC transfer ->
    retry with X-PAYMENT proof header -> resource body.
    """
    with httpx.Client(timeout=15) as client:
        r = client.get(url)
        if r.status_code == 200:
            return {"paid": False, "status": 200, "body": r.text[:2000]}
        if r.status_code != 402:
            r.raise_for_status()

        quote = Quote(resource=url, accepts=_parse_accepts(r),
                      raw_headers=dict(r.headers))
        amount_raw = _demand_amount(quote, max_usdc)
        if amount_raw is None:
            raise ValueError("no acceptable payment demand within budget")

        # PAY: real USDC transfer from the agent wallet
        proof = _pay_usdc(w3, wallet, usdc_address, amount_raw,
                          payee_address or _demand_payee(quote), url)

        headers = {"X-PAYMENT": json.dumps({
            "scheme": "exact", "network": "sepolia",
            "tx_hash": proof.tx_hash, "amount": str(proof.amount_raw),
            "resource": url, "ts": proof.ts})}
        r2 = client.get(url, headers=headers)
        return {"paid": True, "status": r2.status_code,
                "proof": proof.__dict__, "body": r2.text[:2000]}


def _parse_accepts(r: httpx.Response) -> list:
    raw = r.headers.get("x-payment-required", "")
    if raw:
        try:
            return json.loads(raw).get("accepts", [])
        except Exception:
            pass
    try:
        return r.json().get("accepts", [])
    except Exception:
        return []


def _demand_amount(quote: Quote, max_usdc: float) -> int | None:
    """First demand whose amount fits the budget (raw units, 6 decimals)."""
    for a in quote.accepts:
        try:
            amt = int(a.get("maxAmountRequired", 0))
            if amt and amt <= max_usdc * 10 ** USDC_DECIMALS:
                return amt
        except (TypeError, ValueError):
            continue
    return None


def _demand_payee(quote: Quote) -> str:
    for a in quote.accepts:
        payee = a.get("payTo") or a.get("payee")
        if payee:
            return payee
    return ""


def _pay_usdc(w3: Web3, wallet, usdc_address: str, amount_raw: int,
              payee: str, resource: str) -> PaymentProof:
    if not payee:
        raise ValueError("payment demand has no payee address")
    token = w3.eth.contract(address=Web3.to_checksum_address(usdc_address),
                            abi=ERC20_ABI)
    # EIP-1559: maxFeePerGas must cover basefee + priority tip. Floor the tip
    # at 2 gwei but never let it exceed the max fee (RPC rejects otherwise).
    base_fee = w3.eth.get_block("latest").baseFeePerGas
    priority_tip = w3.to_wei(2, "gwei")
    max_fee = base_fee * 2 + priority_tip
    tx = token.functions.transfer(
        Web3.to_checksum_address(payee), amount_raw,
    ).build_transaction({
        "from": wallet.address,
        "nonce": w3.eth.get_transaction_count(wallet.address),
        "gas": 80_000,
        "maxFeePerGas": max_fee,
        "maxPriorityFeePerGas": priority_tip,
        "chainId": w3.eth.chain_id,
    })
    tx_hash = wallet.send_transaction(tx, w3)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
    if receipt.status != 1:
        raise RuntimeError(f"payment tx reverted: {tx_hash}")
    return PaymentProof(tx_hash=tx_hash, amount_raw=amount_raw,
                        token=usdc_address, resource=resource,
                        ts=int(w3.eth.get_block("latest").timestamp))
