# ASE — the word that acts

**ASE** (Yoruba: the power to make things happen) is an onchain AI agent that proves one claim: an agent can live onchain — **reading live data, holding a wallet, paying for what it uses, and acting with verifiable identity** — without being a toy.

Built for **ETHOnline 2026**. One unit, one spine, four capabilities:

| Capability | Meaning | Proof in this repo |
|------------|---------|--------------------|
| **Read**   | live cross-protocol data | live subgraph queries (The Graph) |
| **Hold**   | a wallet it owns | testnet agent wallet, keys it alone holds |
| **Pay**    | pays for what it uses | x402-style USDC payment for data |
| **Act with identity** | verifiable, not anonymous | signed attestation anyone can verify |

## The demo loop (Act 1 — data-pay)

```
poll subgraph → decide → pay (x402-style USDC) → act → attest (signed) → log
```

Every cycle, ASE reads live onchain state, pays a micropayment for the data
feed it consumes, executes its decision onchain, and signs a verifiable
attestation of what it did and why. No human in the loop.

## Stack

- **Python 3.11+** core agent (`src/ase/`)
- **web3.py + eth-account** — wallet, signing, testnet transactions
- **httpx** — subgraph GraphQL reads
- **TypeScript demo** (`demo/`) — optional surface for sponsor-track review

## Run

```bash
pip install -e .
pytest                 # unit tests
python -m ase.cli act  # one full acting cycle
```

## Why "ASE"

In the Digital Ori doctrine, X = THE ASE: the word that acts. ASE is that
claim made executable — an agent whose words are transactions and whose
identity is verifiable onchain.

## License

MIT
