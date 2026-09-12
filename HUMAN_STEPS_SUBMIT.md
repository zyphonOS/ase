# ASE — HUMAN STEPS TO SUBMIT (Sep 9)

The machine did everything it can: 6 upload strategies proven dead against
ETHGlobal's picker (chooser interception, objectId file sets, drag events,
full network trace — the file never persists, React never fires onChange from
CDP on this build). So the picker, the crop-editors, and the final SUBMIT
belong to your hands. Everything else is done or staged below.

**Browser already open:** the `chrome-profile-team` window (port 9225) sits on
`https://ethglobal.com/events/ethonline2026/project` with the Images step
expanded. Project details + repo (`zyphonOS/ase`) are already saved server-side.

---

## STEP 1 — Images (the Final step literally lists these as missing)

Upload pack is ready in `D:\ZyphonOS\assets\uploads\`:

| Slot | File | Note |
|---|---|---|
| Logo * | `ase_logo_512.png` | official ZyphonOS icon, 512×512 |
| Cover * | `ase_cover_1920x1080.png` | 16:9 branded cover |
| Screenshot 1 | `ase_shot_25s.jpg` | real demo frame |
| Screenshot 2 | `ase_shot_55s.jpg` | real demo frame |
| Screenshot 3 | `ase_shot_95s.jpg` | real demo frame |
| Screenshot 4 (opt) | `ase_shot_115s.jpg` | pay-lane frame |

Click each dropzone → pick the file → use the built-in crop editor (Upload
button) to confirm. Min 3 screenshots required.

**Want better graphics?** ChatGPT prompts are at the bottom of this file.
Generate → save into `assets/uploads/` with the same filenames → upload.

## STEP 2 — Video step

Click "Video" in the step nav. It wants the demo **uploaded** (same picker).

- File: `hackathons/ethonline_2026/ase/demo/ASE_demo_final_loudnorm.mp4`
  (2:29, 1080p — inside the 4-min rule)
- Or paste the public URL field (if present) with:
  `https://github.com/zyphonOS/ase/raw/main/demo/ASE_demo_final_loudnorm.mp4`

## STEP 3 — Tech stack

Paste (from SUBMISSION_FINAL.md, ready to go):

```
Python, web3.py, eth-account, httpx, The Graph subgraphs, x402-style USDC payments (Sepolia), ENSv2 identity, signed attestations, GitHub Actions CI
```

## STEP 4 — Future

Paste:

```
Next: mainnet-ready read/pay lanes, agent-to-agent settlement on Celo (Agents at Work port), and folding ASE's attestations into ZyphonOS — our autonomous agent OS — so every house agent acts with verifiable on-chain identity.
```

## STEP 5 — Select prizes

Partner checkboxes were platform-disabled earlier. If they are live now:
The Graph (Best AI Use Case), Arc (Agentic Economy), Ledger (AI Agents x Ledger).
Our description already names all three as fallback.

## STEP 6 — Final step → SUBMIT

The Final step's own deficit list is your checklist — it should be empty
before the button unlocks. Verify each: Logo, Banner, 3+ screenshots, video,
tech stack. Then press **SUBMIT** (or Save & Continue through to it).

**Say the word after and I hard-verify server-side** (reload, read what
ETHGlobal actually stored) — same standard we used for the text fields.

---

## ChatGPT prompts (if you want judge-grade graphics)

**Logo (square, works at 512):**
> Flat vector logo icon for "ASE", a mythical seer character with glowing
> blockchain eyes, minimal geometric style, deep black background (#1A1A1A),
> sharp crimson red (#E8453C) accents, single centered emblem, no text,
> high contrast, crisp edges, app-icon composition, square 1:1

**Cover (16:9):**
> Wide 16:9 hackathon banner: dark near-black (#1A1A1A) background, subtle
> crimson circuit-network lines converging into a glowing red seer-eye emblem
> on the right, bold white headline text "ASE — the word that acts", small
> subtitle "Onchain AI agent: reads, holds, pays, acts with verifiable
> identity", clean Inter-style typography, professional crypto-brand aesthetic

**Screenshots (3, matching the demo story):**
> UI dashboard mockup, dark theme (#0d0d0d background, crimson #E8453C
> highlights): left panel "AGENT CYCLE" with terminal log lines
> (read → decide → pay → act → attest), center a glowing USDC payment
> confirmation card "tx 0xd472…7558 CONFIRMED", right panel an attestation
> signature card "valid: true", clean monospace typography, 16:9

(Repeat the last one with the center card varied: "SUBGRAPH LIVE READ
18.75 USDC", "ATTESTATION SIGNED block 11668461", "WALLET HOLDING 19.75 USDC"
— three distinct frames for the three screenshot slots.)
