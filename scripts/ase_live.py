#!/usr/bin/env python3
"""ASE live runner - the autonomous loop that keeps ASE alive.

Every interval (default 300s) ASE runs one full cycle against a live chain
(Sepolia by default, any EVM chain via env): read -> decide -> (pay when
--pay and the policy allows) -> attest -> journal. Durable memory lives in
state/ase_journal.jsonl (her full life) and state/ase_live.json (heartbeat).

Stop her with Ctrl+C or by placing a file at state/ase_live.stop.

  python scripts/ase_live.py                  live loop, no spending
  python scripts/ase_live.py --once           run a single cycle, no spending
  python scripts/ase_live.py --once --pay     single cycle + payment lane
  python scripts/ase_live.py --interval 120   faster rhythm
"""
import argparse
import json
import os
import signal
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ase.agent import run_cycle
from ase.config import load_config
from ase.wallet import load_wallet

STATE_DIR = ROOT / "state"
HEARTBEAT = STATE_DIR / "ase_live.json"
STOP_FLAG = STATE_DIR / "ase_live.stop"
ATT_DIR = ROOT / "attestations"
_PAY_FN_ARG = "--pay"


def _wallet_and_w3(config):
    from web3 import Web3
    if not config.has_wallet:
        print("No ASE_PRIVATE_KEY set. Run: python -m ase.cli wallet new",
              file=sys.stderr)
        sys.exit(2)
    wallet = load_wallet(config.private_key)
    w3 = Web3(Web3.HTTPProvider(config.rpc_url, request_kwargs={"timeout": 20}))
    return wallet, w3


def _pay_fn(config, wallet, w3):
    from ase.pay import fetch_with_payment

    def pay_fn():
        resource = (config.payee_address
                    if config.payee_address.startswith("http")
                    else "http://localhost:4021/data")
        return fetch_with_payment(
            resource, wallet, w3, usdc_address=config.usdc_address,
            payee_address=config.payee_address)

    return pay_fn


def _save_attestation(attestation_json, ts):
    ATT_DIR.mkdir(exist_ok=True)
    path = ATT_DIR / f"live_{ts}.json"
    path.write_text(attestation_json, encoding="utf-8")
    return path


def _heartbeat(payload):
    STATE_DIR.mkdir(exist_ok=True)
    HEARTBEAT.write_text(json.dumps(payload, indent=2, default=str),
                         encoding="utf-8")


def run_once(config, wallet, w3, pay, ts=None) -> dict:
    ts = ts or int(time.time())
    pay_fn = _pay_fn(config, wallet, w3) if pay else None
    result = run_cycle(config, wallet, w3, pay_fn=pay_fn)
    att_path = _save_attestation(result.attestation_json, result.ts or ts)
    summary = {
        "ts": result.ts, "block": result.block, "decision": result.decision,
        "paid": result.paid, "reading": result.reading,
        "attestation": str(att_path), "errors": result.errors,
    }
    _heartbeat({"alive": True, "pid": os.getpid(), "at": time.time(),
                "last_cycle": summary, "mode": "once" if ts else "loop"})
    return summary


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="ASE live runner")
    p.add_argument("--once", action="store_true", help="run one cycle then exit")
    p.add_argument("--pay", action="store_true", help="enable the payment lane")
    p.add_argument("--interval", type=int, default=300, help="seconds between cycles")
    p.add_argument("--max-cycles", type=int, default=0, help="0 = unlimited")
    args = p.parse_args(argv)

    config = load_config()
    wallet, w3 = _wallet_and_w3(config)

    if args.once:
        summary = run_once(config, wallet, w3, args.pay)
        print(json.dumps(summary, indent=2, default=str))
        return 0

    STATE_DIR.mkdir(exist_ok=True)
    if STOP_FLAG.exists():
        STOP_FLAG.unlink()
    print(f"ASE live loop started (pid={os.getpid()}), interval={args.interval}s, "
          f"pay={args.pay}. Stop: Ctrl+C or {STOP_FLAG}")
    _heartbeat({"alive": True, "pid": os.getpid(), "at": time.time(),
                "started_at": int(time.time()), "mode": "loop", "interval": args.interval})
    cycles = 0
    try:
        while True:
            if STOP_FLAG.exists():
                print("stop flag present - exiting")
                break
            summary = run_once(config, wallet, w3, args.pay)
            cycles += 1
            hb = json.loads(HEARTBEAT.read_text(encoding="utf-8"))
            hb["cycles"] = cycles
            _heartbeat(hb)
            print(f"[{cycles}] block={summary['block']} "
                  f"decision={summary['decision'][:70]} paid={summary['paid']}")
            if args.max_cycles and cycles >= args.max_cycles:
                print(f"max cycles reached ({args.max_cycles})")
                break
            for _ in range(args.interval):
                if STOP_FLAG.exists():
                    break
                time.sleep(1)
    except KeyboardInterrupt:
        print("\ninterrupted - ASE goes quiet, memory persists")
    finally:
        try:
            hb = json.loads(HEARTBEAT.read_text(encoding="utf-8"))
            hb["alive"] = False
            hb["ended_at"] = int(time.time())
            _heartbeat(hb)
        except Exception:
            pass
    return 0


if __name__ == "__main__":
    sys.exit(main())