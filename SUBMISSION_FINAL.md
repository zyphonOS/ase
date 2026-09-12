# ASE - ETHGlobal Submission Pack (FINAL, Sep 9)

Every field verified by script. Paste in order. Form: ETHGlobal dashboard -> ASE project -> Submit.

## Demo video

File: `demo/ASE_demo_final_loudnorm.mp4` (2:29, 1920x1080, h264/aac, loudnorm)
Public URL (raw, from the pushed repo `ca3a963`):

```
https://github.com/zyphonOS/ase/raw/main/demo/ASE_demo_final_loudnorm.mp4
```

Backup: same path with `blob/main` for the browser player page.

## Short description (max 100) - VERIFIED 100

```
Onchain AI agent: reads live chain data, holds a wallet, pays for it, acts with verifiable identity.
```

## Description (min 280) - VERIFIED 972

```
ASE is an onchain AI agent built to prove one claim: an agent can live onchain without being a toy. It reads live cross-protocol blockchain data through The Graph, holds a wallet it alone controls, pays for the data it consumes using x402-style USDC payments, and acts with a verifiable on-chain identity through signed attestations.

Every cycle follows the same loop: poll live on-chain state, decide, pay for the data feed it consumes, act on what it read, then sign a verifiable attestation of what it did and why. The agent is not a chat wrapper; it is a small spine with four capabilities - read, hold, pay, act with identity - glued into one acting loop.

The pay lane has fired for real: a live Sepolia USDC transfer from the agent wallet to its data provider (tx 0xd472ef05d197dbeb2aec5e47dfeae2adf77735c572fda5093ebcfdd338e77558, confirmed in block 11668461), with the payment signed into a verifiable on-chain attestation anyone can check against the agent key.
```

## How it's made (min 280) - VERIFIED 1228

```
ASE is built as a single Python agent spine. The core lives in src/ase/ and is split into four modules that map directly to the four capabilities: read.py for live on-chain data access, wallet.py for the agent-held wallet and signing, pay.py for x402-style USDC data payments, and agent.py for the acting loop that ties them together. config.py holds network and key material for testnet runs, and identity.py handles the signed attestation output.

On the read side, ASE queries live subgraph data over HTTP with httpx and parses the response into a usable view of on-chain state. On the hold and pay side, the agent uses web3.py and eth-account to own a testnet wallet, sign transactions, and pay for the data it consumes - the payment lane has fired live, transferring real Sepolia USDC on-chain with the transfer signed into an attestation. On the identity side, every acting cycle produces a signed attestation that anyone can verify against the agent's on-chain key material.

The repo is intentionally small and explicit: the smallest acting version that still proves the spine - read, hold, pay, and act with identity, all in one loop, with a public repo, a 1080p demo video, and verifiable artifacts behind every claim.
```

## GitHub / repo link

```
https://github.com/zyphonOS/ase
```

## Verifiable proof (for judges, paste anywhere "links" are accepted)

- Payment tx (Sepolia USDC, agent -> data provider): `0xd472ef05d197dbeb2aec5e47dfeae2adf77735c572fda5093ebcfdd338e77558`
- Signed payment attestation (committed, verifies `valid: true`): `attestations/pay_0xd472ef05d197.json`
- First cycle attestation (read/decide/attest): `attestations/cycle_001.json`
- Verify locally: `python -m ase.cli verify attestations/pay_0xd472ef05d197.json`

## Partner prizes selected (max 3)

1. The Graph - Best AI Use Case (From Scratch) - $5,000
2. Arc - Agentic Economy - $1,667
3. Ledger - AI Agents x Ledger - $3,500

(If the checkboxes are platform-disabled, submit without them and note the
three picks in the description's last line: "Built for The Graph Best AI
Use Case, Arc Agentic Economy, and Ledger AI Agents tracks.")

## Remaining before SUBMIT

- [ ] EBVKA pastes the fields above into the ETHGlobal form (CDP session or manual)
- [ ] Demo video on YouTube (public/unlisted) if the form rejects raw GitHub raw links
- [ ] Partner prize checkboxes when ETHGlobal enables them
