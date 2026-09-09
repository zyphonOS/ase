"""READ - live data.

Two backends, both real:
- rpc:      direct live onchain state via any public RPC (no key needed).
- subgraph: The Graph GraphQL endpoint (when ASE_SUBGRAPH_URL is set).

ASE must not decide on stale or fake data. Every read returns the block
it was read at, so every decision can be audited against the chain.
"""
from dataclasses import dataclass
from typing import Any

import httpx
from web3 import Web3

# Minimal ERC20 ABI: balanceOf + decimals + symbol + transfer
ERC20_ABI = [
    {"name": "balanceOf", "type": "function", "stateMutability": "view",
     "inputs": [{"name": "owner", "type": "address"}],
     "outputs": [{"name": "", "type": "uint256"}]},
    {"name": "decimals", "type": "function", "stateMutability": "view",
     "inputs": [], "outputs": [{"name": "", "type": "uint8"}]},
    {"name": "symbol", "type": "function", "stateMutability": "view",
     "inputs": [], "outputs": [{"name": "", "type": "string"}]},
    {"name": "transfer", "type": "function", "stateMutability": "nonpayable",
     "inputs": [{"name": "to", "type": "address"}, {"name": "amount", "type": "uint256"}],
     "outputs": [{"name": "", "type": "bool"}]},
]


@dataclass
class Reading:
    """A block-stamped fact. Decisions cite this."""
    block: int
    kind: str
    data: dict


def _w3(rpc_url: str) -> Web3:
    return Web3(Web3.HTTPProvider(rpc_url, request_kwargs={"timeout": 15}))


def read_chain_state(rpc_url: str, token_address: str, holder: str) -> Reading:
    """Live token balance of a holder, stamped with the block it was read at."""
    w3 = _w3(rpc_url)
    if not w3.is_connected():
        raise ConnectionError(f"RPC not reachable: {rpc_url}")
    block = w3.eth.block_number
    token = w3.eth.contract(address=Web3.to_checksum_address(token_address),
                            abi=ERC20_ABI)
    raw = token.functions.balanceOf(Web3.to_checksum_address(holder)).call()
    decimals = token.functions.decimals().call()
    symbol = token.functions.symbol().call()
    return Reading(block=block, kind="erc20_balance", data={
        "holder": holder, "token": token_address, "symbol": symbol,
        "raw": raw, "human": raw / (10 ** decimals),
    })


def read_subgraph(subgraph_url: str, query: str,
                  variables: dict | None = None) -> dict[str, Any]:
    """Query a The Graph subgraph endpoint. Returns raw GraphQL data."""
    resp = httpx.post(subgraph_url, json={"query": query,
                                          "variables": variables or {}},
                      timeout=15)
    resp.raise_for_status()
    payload = resp.json()
    if payload.get("errors"):
        raise RuntimeError(f"subgraph errors: {payload['errors']}")
    return payload.get("data", {})


def subgraph_available(subgraph_url: str) -> bool:
    if not subgraph_url:
        return False
    try:
        read_subgraph(subgraph_url, "{ __typename }")
        return True
    except Exception:
        return False
