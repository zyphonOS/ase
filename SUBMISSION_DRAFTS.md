# ASE submission drafts

These are pre-drafts for the ETHGlobal project form fields.

Do not paste blindly. The real submission should use real artifacts
(repo, demo, attestation, testnet proof) where they exist.

## Short description (max 100 characters)

ASE: an onchain AI agent that reads live chain data, holds a wallet,
pays for what it uses, and acts with verifiable identity.

Character count: 120 — too long. Trimmed version:

ASE: onchain AI agent that reads live chain data, holds a wallet,
pays for usage, and acts with verifiable identity.

Character count: 103 — still slightly over. Trimmed again:

Onchain AI agent that reads live chain data, holds a wallet,
pays for usage, and acts with verifiable identity.

Character count: 99 — good.

Final candidate:

Onchain AI agent that reads live chain data, holds a wallet,
pays for usage, and acts with verifiable identity.

## Description (min 280 characters)

ASE is an onchain AI agent built to prove one claim: an agent can
live onchain without being a toy. It reads live cross-protocol
blockchain data through The Graph, holds a wallet it alone controls,
pays for the data it consumes using x402-style USDC payments, and
acts with a verifiable on-chain identity through signed attestations.

Every cycle follows the same loop: poll live on-chain state, decide,
pay for the data feed it consumes, act on what it read, then sign a
verifiable attestation of what it did and why. The agent is not a
chat wrapper; it is a small spine with four capabilities — read,
hold, pay, act with identity — glued into one acting loop.

The project is built as a Python agent core with web3.py and
eth-account for wallet and signing, httpx for subgraph reads, and a
clear separation between reading, paying, and acting so the same loop
can be extended to more protocols and use cases later.

What makes ASE different from a generic agent demo is that it is not
only talking about agents. It is an agent that reads, pays, and signs
its own actions on chain, which makes its behavior verifiable instead
of promotional.

## How it's made (min 280 characters)

ASE is built as a single Python agent spine for ETHOnline 2026. The
core lives in `src/ase/` and is split into four modules that map
directly to the four capabilities: `read.py` for live on-chain data
access, `wallet.py` for the agent-held wallet and signing, `pay.py`
for x402-style USDC data payments, and `agent.py` for the acting loop
that ties them together. `config.py` holds network and key material
for testnet runs, and `identity.py` handles the signed attestation
output.

On the read side, ASE queries live subgraph data over HTTP with
httpx and parses the response into a usable view of on-chain state.
On the hold and pay side, the agent uses web3.py and eth-account to
own a testnet wallet, sign transactions, and pay for the data it
consumes rather than only observing it. On the identity side, every
acting cycle produces a signed attestation that anyone can verify
against the agent's on-chain key material.

The repo is intentionally small and explicit. The goal was the
smallest acting version that still proves the spine: read, hold, pay,
and act with identity, all in one loop, with a public repo and a
verifiable artifact behind it.

## Demo link candidates

- GitHub repo: the ASE repo itself, if public and committed
- X thread: the @ebvkaar ASE announcement thread as a live walkthrough
  surface if no video exists yet
- Substack: any posted write-up if available
- Demo video: preferred if ready, 2-4 min, >= 720p, clear audio

## Partner prize targets

1. The Graph — Best AI Use Case
2. Arc — Agentic Economy
3. Ledger — AI Agents x Ledger

## Open question

The submission should not be finalized until the repo is public and
the demo link is a real verifiable artifact, not a promise.
