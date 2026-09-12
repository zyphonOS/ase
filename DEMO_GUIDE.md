# ASE Demo Instructions

**How to run the ASE dashboard with a live on-chain agent cycle.**

---

## Prerequisites

You need:
- Python 3.11+ installed
- Node.js 18+ installed
- A Sepolia testnet wallet with:
  - A little ETH (for gas)
  - A little USDC (for payments)

---

## Step 1: Install Python Dependencies

Open a terminal in the ASE project root:

```bash
cd hackathons/ethonline_2026/ase
pip install -e .
```

This installs the agent and all its dependencies.

---

## Step 2: Get Your Wallet Key

If you already have a Sepolia wallet, skip to Step 3.

If you need a new wallet:

```bash
python -m ase.cli wallet new
```

This prints:
```
ADDRESS: 0xYourAddressHere
PRIVATE_KEY: 0xYourPrivateKeyHere
```

**Copy the PRIVATE_KEY.** You will need it in Step 3.

---

## Step 3: Create the .env File

In the ASE project root, create a file called `.env`:

```
ASE_PRIVATE_KEY=0xYourPrivateKeyHere
```

Replace `0xYourPrivateKeyHere` with your actual private key from Step 2.

If you have a data provider address for payments, also add:
```
ASE_PAYEE_ADDRESS=0xDataProviderAddress
```

If you do not have a payee, the agent will still run — it just will not make payments.

---

## Step 4: Build the Dashboard

```bash
cd dashboard
npm install
npm run build
cd ..
```

This builds the frontend. You should see "built in X.XXs" at the end.

---

## Step 5: Start the Server

```bash
python -m ase.server
```

You should see:
```
ASE server running on http://0.0.0.0:8000
Dashboard: serving from dashboard/dist/
```

---

## Step 6: Open the Dashboard

Open your browser and go to:

```
http://localhost:8000
```

You should see the ASE dashboard with:
- ASE emblem in the header
- "LIVE MODE" indicator
- "RUN CYCLE" button in the status bar
- Agent Cycle card (5 stages, all pending)
- Center Action Card (waiting for first read)
- Attestation card (awaiting attestation)

---

## Step 7: Run a Live Agent Cycle

Click the **RUN CYCLE** button in the status bar.

Watch the dashboard update in real time:

1. **READ** — Agent queries Sepolia chain state, reads your USDC balance
2. **DECIDE** — Agent evaluates its policy (balance thresholds)
3. **PAY** — If policy triggers payment, USDC is sent on-chain
4. **ACT** — Attestation is signed with the result
5. **ATTEST** — Verification shows `valid: true`

The Activity Log at the bottom shows every event with timestamps.

---

## Step 8: Verify On-Chain

After the cycle completes, you can verify the attestation:

```bash
# Save the attestation JSON from the activity log, then:
python -m ase.cli verify attestation.json
```

Or check the transaction on Sepolia Etherscan:
```
https://sepolia.etherscan.io/tx/<transaction_hash>
```

---

## Troubleshooting

**"No ASE_PRIVATE_KEY set"**
→ Your `.env` file is missing or the key is not set. Check Step 3.

**"Dashboard not built"**
→ Run `cd dashboard && npm run build` (Step 4).

**"Connection refused" on the dashboard**
→ Make sure the server is running (Step 5). Check terminal for errors.

**Payment fails with "insufficient balance"**
→ Your wallet needs USDC on Sepolia. Get testnet USDC from a faucet or transfer from another wallet.

**Dashboard shows "DEMO MODE" instead of "LIVE MODE"**
→ The server is not running, or the dashboard cannot reach `localhost:8000`. Start the server and refresh.

---

## Quick Start (All Commands)

```bash
cd hackathons/ethonline_2026/ase
pip install -e .
python -m ase.cli wallet new          # if you need a new wallet
# Create .env with ASE_PRIVATE_KEY=0x...
cd dashboard && npm install && npm run build && cd ..
python -m ase.server
# Open http://localhost:8000 and click RUN CYCLE
```

---

## What the Judges See

1. Dashboard loads with ASE branding
2. Click RUN CYCLE
3. Agent reads live Sepolia state
4. Agent decides based on legible policy
5. Agent pays USDC (if configured)
6. Agent produces cryptographic attestation
7. All visible in real time on the dashboard
8. Activity log shows full audit trail
9. Attestation can be verified independently

**This proves: ASE is an autonomous agent that reads, decides, pays, and proves — all on-chain, all without human intervention.**
