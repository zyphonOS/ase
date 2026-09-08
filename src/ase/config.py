"""Configuration - everything comes from the environment, nothing is hardcoded.

ASE never commits secrets. The agent wallet key lives in .env (gitignored).
"""
import os
from dataclasses import dataclass, field


def _env(key: str, default: str = "") -> str:
    return os.environ.get(key, default)


@dataclass
class Config:
    # Hold: the agent wallet
    private_key: str = field(default_factory=lambda: _env("ASE_PRIVATE_KEY"))
    # Read: live data source
    rpc_url: str = field(default_factory=lambda: _env(
        "ASE_RPC_URL", "https://ethereum-sepolia-rpc.publicnode.com"))
    subgraph_url: str = field(default_factory=lambda: _env("ASE_SUBGRAPH_URL"))
    # Pay: the payment layer (x402-style USDC)
    usdc_address: str = field(default_factory=lambda: _env(
        "ASE_USDC_ADDRESS", "0x1c7D4B196Cb0C7B01d743Fbc6116a902379C7238"))  # Sepolia USDC
    payee_address: str = field(default_factory=lambda: _env("ASE_PAYEE_ADDRESS"))
    price_per_read_gwei: int = field(default_factory=lambda: int(_env("ASE_PRICE_PER_READ_GWEI", "1000")))
    # Identity
    agent_name: str = field(default_factory=lambda: _env("ASE_AGENT_NAME", "ase.ethonline2026"))

    @property
    def has_wallet(self) -> bool:
        return bool(self.private_key)

    @property
    def has_payee(self) -> bool:
        return bool(self.payee_address)


def load_config() -> Config:
    return Config()
