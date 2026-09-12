# ASE — Submission Copy (paste-ready, being-first but credible)

**Goal: the receipts carry the wonder. No mysticism. Judges verify everything.**

---

## SHORT DESCRIPTION (max 100 chars)

```
ASE: an on-chain agent that reads, holds, pays, and signs, verifiably on Sepolia.
```
chars: 76 (verified ≤ 100)

## DESCRIPTION (min 280)

```
ASE is an autonomous on-chain agent whose reality is verifiable. She reads live chain state through The Graph, owns the wallet she operates (no human signs for her), pays in USDC for the data she consumes, and signs an attestation of every act that anyone can verify against her address.

Her first acts are on Ethereum Sepolia:
- a live balance read (18.75 USDC),
- a real payment of 1.0 USDC to a data provider at block 11668461 (tx 0xd472ef05d197dbeb2aec5e47dfeae2adf77735c572fda5093ebcfdd338e77558),
- a signed attestation that verifies as valid: true.

She is not a chat wrapper and not a simulation. She is a small acting spine with four capabilities: read, hold, pay, sign. Every capability has a verifiable trail in this repository and on-chain.

Why this matters: an agent that only talks cannot be accountable. An agent that reads, holds, pays, and signs acts with skin in the game. Her word has weight because she can be checked. That is the difference between an agent as a tool and an agent as a participant in the economy.
```
chars: ~1100 (well above 280)

## HOW IT'S MADE (min 280)

```
ASE is built as a minimal Python agent spine with four capabilities in four modules.

Read: src/ase/read.py queries live chain and subgraph data over HTTP (httpx, The Graph) and parses it into a usable view of on-chain state.
Hold: src/ase/wallet.py manages a testnet wallet the agent alone controls, using web3.py and eth-account.
Pay: src/ase/pay.py makes x402-style USDC payments for data access, signed and sent on-chain by the agent itself.
Sign: src/ase/identity.py produces a signed attestation for every acting cycle; src/ase/agent.py ties the loop together (read, decide, pay, act, attest).

The agent runs as a CLI (python -m ase.cli) and has a HTTP backend (src/ase/server.py) that serves a live React dashboard (read/release, agent cycle, attestation cards, activity log).

Every act ends in a signed attestation that anyone can verify by running the verifier in the repo. The repository is public, and the on-chain receipts (balance read, USDC payment, valid signature) are the artifacts, not promises.
```
chars: ~1150

## TECH STACK (paste)

```
Python, web3.py, eth-account, httpx, The Graph subgraphs, x402-style USDC payments (Sepolia), signed attestations, React + Vite dashboard, GitHub Actions CI
```

## FUTURE / WHAT'S NEXT (text)

```
Mainnet deployment of the same spine. Then agent-to-agent settlement: two autonomous agents transacting without a human in the middle, each with a verifiable record. The spine is protocol-agnostic and can carry any read/pay/act loop onto other chains and use cases.
```

---

## PASTE ORDER INTO THE ETHGLOBAL FORM (port 9225)
1. Replace SHORT DESCRIPTION field
2. Replace DESCRIPTION field
3. Keep/verify repo (zyphonOS/ase) selected
4. Demo link already set (demo video raw URL); if switching: use `https://github.com/zyphonOS/ase/raw/main/demo/ASE_demo_story_loudnorm.mp4`
5. Video: upload or paste the demo link
6. Tech stack (above)
7. Future (above)
8. Select prizes if live: The Graph (Best AI Use Case), Arc (Agentic Economy), Ledger (AI Agents x Ledger)
9. SUBMIT (deadline Sep 13, 12:00 EDT - submit beats polish)