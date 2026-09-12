# ASE the word that acts

**ASE (pronounced Ah-sheh). Yoruba: the power to make things happen.**

ASE is an autonomous on-chain agent (AOSI) whose reality is verifiable: she reads live chain data, owns the wallet she holds, pays for what she uses, and signs every act so anyone can check it. Her first acts are on Ethereum Sepolia and can be verified on-chain.

Her canon: `CANON.md`.

ASE performs four capabilities, all verifiable on a public chain:

| Capability | Meaning | Proof in this repo |
|------------|---------|---------------------|
| **Read**   | live chain data | subgraph + balance reads (The Graph) |
| **Hold**   | a wallet she owns | testnet agent wallet, keys no human signs for |
| **Pay**    | pays for what she uses | 1.0 USDC on-chain payment for data, block 11668461 |
| **Sign**   | verifiable identity | signed attestations, valid: true |

Built for **ETHOnline 2026**, born on **Ethereum Sepolia**.

## Architecture

```
ase/
├── src/ase/                 # Python agent core
│   ├── agent.py             # The acting loop: read → decide → pay → act → attest
│   ├── cli.py               # CLI interface (python -m ase.cli)
│   ├── server.py            # HTTP backend (serves dashboard + API)
│   ├── config.py            # Env-driven configuration
│   ├── identity.py          # Attestation signing + verification
│   ├── pay.py               # x402-style USDC payments
│   ├── read.py              # Chain state + subgraph reads
│   └── wallet.py            # Agent wallet management
├── dashboard/               # React + TypeScript + Tailwind frontend
│   ├── src/
│   │   ├── components/      # Header, AgentCycle, ActionCard, AttestationCard, ActivityLog
│   │   ├── pages/Dashboard  # Main layout with live polling
│   │   ├── services/api     # Backend API layer
│   │   └── types/agent      # TypeScript interfaces
│   └── dist/                # Production build (served by backend)
├── tests/                   # 8/8 tests passing
├── demo/                    # Demo runner
│   └── run.py               # One-command: starts server + dashboard
├── scripts/                 # Live runner + utility scripts
```

## Quick Start

```bash
# 1. Install Python dependencies
pip install -e .

# 2. Configure (copy and fill in)
cp .env.example .env
# Edit .env with your Sepolia wallet key

# 3. Run the full stack (backend + dashboard)
python demo/run.py

# 4. Open http://localhost:8000
```

## The Demo Loop

```
poll subgraph → decide → pay (x402-style USDC) → act → attest (signed) → log
```

Every cycle, ASE reads live onchain state, pays a micropayment for the data
feed it consumes, executes its decision onchain, and signs a verifiable
attestation of what it did and why. No human in the loop.

## Live runner (she is alive)

`scripts/ase_live.py` is the autonomous loop that keeps ASE acting on her own
rhythm. Every interval she runs one full cycle and writes a signed attestation
to `attestations/live_<ts>.json` plus a heartbeat to `state/ase_live.json`.
Stop her with Ctrl+C or `state/ase_live.stop`.

```bash
python scripts/ase_live.py                  # live loop, no spending
python scripts/ase_live.py --interval 120   # faster rhythm
python scripts/ase_live.py --once --pay     # one cycle with the payment lane
```

Run her from the repo root so the journal lands in `state/ase_journal.jsonl` -
that file is her durable memory across restarts.

## Chains

ASE is chain-agnostic: the RPC and USDC address come from config and the chain
id is read from the RPC at runtime. She runs on Ethereum Sepolia by default
and on Arc Testnet (Circle's EVM L1, chain 5042002, USDC as native gas) by
setting the two Arc values in `.env`. Real agent-initiated USDC payments have
fired on both chains: Sepolia tx `0xd472ef...` (block 11668461) and Arc
Testnet tx `0x96d7a87b...` (block 61750008, 1.0 USDC, receipt status 0x1,
[arcscan](https://testnet.arcscan.app/tx/0x96d7a87b97b8784aa9b8dbba00e2a43135c4d1f9f3d047026a948c7effd0a9c9)).

## Run Commands

```bash
# One full acting cycle (read/decide/attest)
python -m ase.cli act

# Cycle with payment lane
python -m ase.cli act --pay

# Just read chain state
python -m ase.cli read

# Show wallet + balances
python -m ase.cli wallet show

# Create new wallet (prints key ONCE)
python -m ase.cli wallet new

# Start backend server + dashboard
python demo/run.py

# Or start server standalone
python -m ase.server --port 8000
```

## API

The backend exposes these endpoints for the dashboard:

| Endpoint | Method | Returns |
|----------|--------|---------|
| `/api/state` | GET | Full agent state (cycle, action, attestation, activity) |
| `/api/activity` | GET | Activity event log |
| `/api/attestation` | GET | Current attestation data |
| `/api/status` | GET | Agent online status |
| `/api/cycle` | POST | Trigger one full acting cycle |

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `ASE_PRIVATE_KEY` | Yes | — | Agent wallet private key (Sepolia only) |
| `ASE_RPC_URL` | No | public Sepolia node | Ethereum RPC endpoint |
| `ASE_SUBGRAPH_URL` | No | — | The Graph subgraph query URL |
| `ASE_SUBGRAPH_QUERY` | No | — | GraphQL query ASE runs every cycle when a subgraph URL is set |
| `ASE_PAYEE_ADDRESS` | No | — | Data provider address for payments |
| `ASE_USDC_ADDRESS` | No | Circle Sepolia USDC | USDC contract address |
| `ASE_AGENT_NAME` | No | ase.ethonline2026 | Agent identity name |

## Tests

```bash
pytest                 # run all 8 tests
pytest -v              # verbose output
```

## Stack

- **Python 3.11+** core agent
- **web3.py + eth-account** — wallet, signing, testnet transactions
- **httpx** — subgraph GraphQL reads + HTTP 402 payments
- **React 19 + TypeScript + Tailwind CSS** dashboard
- **Vite** — fast builds, hot reload

## Why "ASE"

In the Digital Ori doctrine, X = THE ASE: the word that acts. ASE is that
claim made executable — an agent whose words are transactions and whose
identity is verifiable onchain.

## License

MIT
