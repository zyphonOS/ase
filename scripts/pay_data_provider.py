"""Exercise the PAY lane: ASE pays its data provider in real Sepolia USDC.

This is the honest payment primitive behind the x402-style flow: a real
onchain token transfer from the agent wallet, recorded as a verifiable
PaymentProof and signed into an attestation.

Usage:
    python scripts/pay_data_provider.py [amount_usdc]
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from ase.config import load_config
from ase.identity import make_attestation, sign_attestation
from ase.pay import _pay_usdc, USDC_DECIMALS
from ase.wallet import load_wallet
from web3 import Web3


def main() -> int:
    amount_usdc = float(sys.argv[1]) if len(sys.argv) > 1 else 0.25
    cfg = load_config()
    if not cfg.has_wallet or not cfg.has_payee:
        print("Need ASE_PRIVATE_KEY and ASE_PAYEE_ADDRESS in .env", file=sys.stderr)
        return 2
    wallet = load_wallet(cfg.private_key)
    w3 = Web3(Web3.HTTPProvider(cfg.rpc_url, request_kwargs={"timeout": 15}))
    amount_raw = int(amount_usdc * 10 ** USDC_DECIMALS)

    print(f"PAY: {wallet.address} -> {cfg.payee_address} "
          f"{amount_usdc} USDC on chain {w3.eth.chain_id}")
    proof = _pay_usdc(w3, wallet, cfg.usdc_address, amount_raw,
                      cfg.payee_address, resource="ase:data_feed")
    print(f"tx: {proof.tx_hash}")
    print(f"status: confirmed in block")

    att = make_attestation(
        agent_address=wallet.address, act="pay_data_provider",
        ts=proof.ts, block=w3.eth.block_number,
        decision=f"Paid {amount_usdc} USDC to data provider for feed access",
        payload={"payment": proof.__dict__})
    signed = sign_attestation(att, wallet)

    out_dir = Path(__file__).resolve().parent.parent / "attestations"
    out_dir.mkdir(exist_ok=True)
    out = out_dir / f"pay_{proof.tx_hash[:14]}.json"
    out.write_text(signed.to_json(), encoding="utf-8")
    print(f"attestation: {out.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
