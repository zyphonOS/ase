"""IDENTITY - verifiable agent identity.

ASE signs every significant act with its wallet key. Anyone can verify the
signature recovers to ASE's address - no registrar, no API, no trust needed.
This module builds the attestation format and the verify tool.
"""
import json
from dataclasses import dataclass, asdict

from .wallet import verify_signature


ATTESTATION_VERSION = "ase-attest-v1"


@dataclass
class Attestation:
    """A signed statement about an act ASE took."""
    version: str
    agent: str          # ASE wallet address
    act: str            # what it did, e.g. "data_pay_cycle"
    ts: int             # unix seconds
    block: int          # chain height at decision time
    decision: str       # human-readable rationale
    payload: dict       # act-specific data (readings, payments, tx hashes)

    def signing_message(self) -> str:
        """The exact byte string ASE signs. Deterministic."""
        canonical = json.dumps({
            "version": self.version, "agent": self.agent, "act": self.act,
            "ts": self.ts, "block": self.block, "decision": self.decision,
            "payload": self.payload,
        }, sort_keys=True, separators=(",", ":"))
        return f"{ATTESTATION_VERSION}\n{canonical}"

    def to_json(self) -> str:
        d = asdict(self)
        d["signature"] = self.signature
        return json.dumps(d, indent=2)

    signature: str = ""


def make_attestation(agent_address: str, act: str, ts: int, block: int,
                     decision: str, payload: dict) -> Attestation:
    return Attestation(version=ATTESTATION_VERSION, agent=agent_address,
                       act=act, ts=ts, block=block, decision=decision,
                       payload=payload)


def sign_attestation(att: Attestation, wallet) -> Attestation:
    att.signature = wallet.sign_message(att.signing_message())
    return att


def verify_attestation(att_json: str) -> dict:
    """Standalone verification: does the signature recover to the agent addr?
    Returns {valid: bool, agent: str, reason: str}."""
    d = json.loads(att_json)
    att = Attestation(**{k: v for k, v in d.items() if k != "signature"})
    att.signature = d.get("signature", "")
    ok = verify_signature(att.signing_message(), att.signature, att.agent)
    return {"valid": ok, "agent": att.agent,
            "act": att.act, "block": att.block,
            "reason": "" if ok else "signature does not recover to agent address"}
