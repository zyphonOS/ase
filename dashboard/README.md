# ASE Dashboard

**ASE (the word that acts)** is an autonomous onchain agent built by [ZyphonOS](https://github.com/zyphonOS).

ASE reads live cross-protocol data, makes decisions, executes payments, and produces cryptographic attestations — all autonomously.

This dashboard is the real-time interface into ASE's execution cycle.

## How the Agent Cycle Works

```
READ → DECIDE → PAY → ACT → ATTEST
```

1. **READ** — ASE queries live on-chain data (The Graph subgraph, balances, state)
2. **DECIDE** — Based on the read, ASE determines whether action is needed
3. **PAY** — If action is warranted, ASE executes a USDC payment on Sepolia
4. **ACT** — The payment is confirmed on-chain (block number recorded)
5. **ATTEST** — ASE produces a cryptographic attestation proving the action occurred

## Architecture

```
src/
├── components/       # Reusable UI components
│   ├── AseEmblem     # The ASE brand mark (geometric eye/arrow)
│   ├── Header        # Application header with status
│   ├── AgentCycle    # The 5-stage execution pipeline
│   ├── ActionCard    # Center focal — changes based on current action
│   ├── AttestationCard  # Verification display
│   ├── ActivityLog   # Live event history
│   └── StatusBadge   # Online/offline indicators
├── pages/
│   └── Dashboard     # Main page layout
├── data/
│   └── demoData      # Demo mode simulation data
├── services/
│   └── api           # Backend API abstraction layer
└── types/
    └── agent         # TypeScript interfaces
```

## Local Setup

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Environment Variables

Create a `.env` file from `.env.example`:

```bash
cp .env.example .env
```

| Variable | Default | Description |
|----------|---------|-------------|
| `VITE_API_BASE_URL` | `http://localhost:8000` | ASE backend API URL |

## Demo Mode

The dashboard works without a backend. When no API is available, it automatically enters **demo mode** and cycles through the full agent execution sequence:

```
LIVE READ → DECISION RECORDED → USDC PAYMENT → CONFIRMED → ATTESTATION SIGNED
```

This lets hackathon judges see the complete flow immediately.

## API Integration

The frontend consumes structured state from these endpoints:

| Endpoint | Returns |
|----------|---------|
| `GET /api/state` | Full agent state (cycle, action, attestation, activity) |
| `GET /api/activity` | Activity event log |
| `GET /api/attestation` | Current attestation data |
| `GET /api/status` | Agent online status |

Components never reference hardcoded presentation strings. All data flows through typed interfaces in `src/types/agent.ts`.

## Deployment

```bash
# Build
npm run build

# The dist/ directory is static and deployable anywhere:
# - GitHub Pages
# - Vercel
# - Netlify
# - Any static host
```

Set `VITE_API_BASE_URL` in your hosting platform's environment variables to point to the live ASE backend.

## Brand System

| Color | Hex | Usage |
|-------|-----|-------|
| Emerald | `#34D399` | Primary, active states, verification |
| Deep Green | `#0D9568` | Borders, subtle accents |
| Pale Mint | `#C5F2E2` | Light text on dark |
| Near Black | `#0A0A0A` | Background |
| White | `#FFFFFF` | Headings, high contrast |

**Typography:** Inter (headings, labels), JetBrains Mono (hashes, logs, technical data)

## License

Built by ZyphonOS for ETHOnline 2026.
