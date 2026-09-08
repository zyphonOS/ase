"""HOLD - the agent wallet.

ASE holds its own key. Nobody signs for it. This module creates, loads,
signs, and verifies - the minimal honest wallet for an acting agent.

Testnet only by doctrine. Never commit the key. Never mainnet without the
human's explicit gate (the ZyphonOS human_signal gate exists for exactly this).
"""
from dataclasses import dataclass
from eth_account import Account
from eth_account.messages import encode_defunct


@dataclass
class Wallet:
    account: Account

    @property
    def address(self) -> str:
        return self.account.address

    def sign_message(self, message: str) -> str:
        """Sign an arbitrary message; returns the rlp-encoded signature."""
        signed = self.account.sign_message(encode_defunct(text=message))
        return signed.signature.to_0x_hex()

    def send_transaction(self, web3_tx: dict, w3) -> str:
        """Sign and send a transaction dict (already gas-priced). Returns tx hash."""
        signed = self.account.sign_transaction(web3_tx)
        tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
        return tx_hash.to_0x_hex()


def create_wallet() -> Wallet:
    """Generate a fresh agent wallet. The key is shown ONCE - the caller must
    persist it to .env immediately or it is gone."""
    acct = Account.create()
    return Wallet(account=acct)


def load_wallet(private_key: str) -> Wallet:
    if not private_key or not private_key.startswith("0x"):
        raise ValueError("ASE_PRIVATE_KEY missing or malformed (expect 0x-prefixed hex)")
    return Wallet(account=Account.from_key(private_key))


def verify_signature(message: str, signature: str, address: str) -> bool:
    """Anyone can verify ASE's words came from ASE's wallet. This is the
    verifiable-identity primitive the whole demo rests on."""
    try:
        recovered = Account.recover_message(encode_defunct(text=message),
                                            signature=signature)
        return recovered.lower() == address.lower()
    except Exception:
        return False
