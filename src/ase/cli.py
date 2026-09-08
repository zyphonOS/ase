"""ASE CLI.

  python -m ase.cli wallet new         create agent wallet (prints key ONCE)
  python -m ase.cli wallet show        show agent address + balances
  python -m ase.cli read               one live block-stamped read
  python -m ase.cli act                one full acting cycle (read/decide/attest)
  python -m ase.cli act --pay          cycle + exercise the payment lane
  python -m ase.cli verify <file>      verify a signed attestation
"""
import json
import sys

from .agent import run_cycle
from .config import load_config
from .identity import verify_attestation
from .read import read_chain_state
from .wallet import create_wallet, load_wallet


def _wallet_and_w3(config):
    from web3 import Web3
    if not config.has_wallet:
        print("No ASE_PRIVATE_KEY set. Run: python -m ase.cli wallet new",
              file=sys.stderr)
        sys.exit(2)
    wallet = load_wallet(config.private_key)
    w3 = Web3(Web3.HTTPProvider(config.rpc_url, request_kwargs={"timeout": 15}))
    return wallet, w3


def main(argv=None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    if not argv:
        print(__doc__)
        return 1
    config = load_config()

    if argv[0] == "wallet" and len(argv) > 1 and argv[1] == "new":
        w = create_wallet()
        print("ADDRESS:", w.address)
        print("PRIVATE_KEY:", w.account.key.to_0x_hex())
        print("Put the key in .env as ASE_PRIVATE_KEY=<key> - it is NOT stored anywhere else.")
        return 0

    if argv[0] == "wallet":
        wallet, w3 = _wallet_and_w3(config)
        print("address:", wallet.address)
        print("eth:", w3.from_wei(w3.eth.get_balance(wallet.address), "ether"))
        return 0

    if argv[0] == "read":
        wallet, w3 = _wallet_and_w3(config)
        r = read_chain_state(config.rpc_url, config.usdc_address, wallet.address)
        print(json.dumps({"block": r.block, **r.data}, indent=2, default=str))
        return 0

    if argv[0] == "act":
        wallet, w3 = _wallet_and_w3(config)
        pay_fn = None
        if "--pay" in argv:
            from .pay import fetch_with_payment, SEPOLIA_USDC
            def pay_fn():
                return fetch_with_payment(
                    config.payee_address if config.payee_address.startswith("http")
                    else "http://localhost:4021/data",
                    wallet, w3, usdc_address=config.usdc_address,
                    payee_address=config.payee_address)
        result = run_cycle(config, wallet, w3, pay_fn=pay_fn)
        print(json.dumps(result.__dict__, indent=2, default=str))
        return 0

    if argv[0] == "verify" and len(argv) > 1:
        att_json = open(argv[1], encoding="utf-8").read()
        print(json.dumps(verify_attestation(att_json), indent=2))
        return 0

    print(__doc__)
    return 1


if __name__ == "__main__":
    sys.exit(main())
