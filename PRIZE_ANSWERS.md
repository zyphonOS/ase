# ASE - Partner Prize Answers (FINAL, Sep 12)

Paste-order answers for the prize fields on the ETHGlobal submission form.
Only prizes with REAL integration are applied: **The Graph** and **Arc**.
**Ledger is deselected on purpose** (no honest path: the track requires the
Ledger Key Ring CLI `wallet-cli ring`; our install has no `ring` command, no
device, no Agent Stack - a fake code link would poison the submission).

---

## The Graph - $15,000

**Why are you applicable for this prize?**
```
ASE is an autonomous onchain agent whose whole loop depends on live, structured blockchain data. The Graph is ASE's data layer: when a subgraph endpoint and query are configured, every acting cycle queries live indexed data and signs it into the agent's attestation, so ASE's decisions are traceable to queries ASE actually ran.
```

**Details on how you're using this Protocol / API**
```
ASE's read layer (src/ase/read.py) has a first-class subgraph backend: read_subgraph() posts a GraphQL query to a The Graph subgraph endpoint over HTTP (redirect-aware) and parses the response into usable data, and subgraph_available() probes the endpoint for liveness. The acting loop (src/ase/agent.py) probes the endpoint every cycle, and when ASE_SUBGRAPH_QUERY is configured it pulls the query result into the block-stamped reading that gets signed into the agent's onchain attestation. Both the endpoint and the query are config-driven (src/ase/config.py), so ASE can point at any The Graph endpoint - including Subgraph Studio query URLs - without code changes. Alongside direct RPC reads, on-chain balance reads that drove real decisions are receipted on Sepolia (block 11688398, live autonomous cycle).
```

**Link to the line of code where the tech is used**
```
https://github.com/zyphonOS/ase/blob/main/src/ase/read.py#L60-L80
(used in the loop: https://github.com/zyphonOS/ase/blob/main/src/ase/agent.py#L59-L72)
```

**How easy is it to use the API / Protocol? (1-10)**

```
8
```

**Additional feedback for the Sponsor**
```
The subgraph GraphQL API is clean to call from a typed HTTP client with zero SDK baggage - the read path was production-ready on the first pass. Two things would help agents like ASE: clearer discovery docs for finding the right live subgraph endpoint per network (we burned time hunting for a working one; the legacy hosted host now redirects and the gateway needs an API key), and first-class x402 payment support so agents can pay per query through The Graph itself. That would make The Graph the natural money rail for autonomous agents.
```

---

## Arc - $10,000

**Why are you applicable for this prize?**
```
ASE is an autonomous agent that holds its own wallet and pays real USDC for the data it consumes - the exact agentic-economy pattern Arc is built for. It decides from live on-chain signals, settles in USDC, and signs a verifiable attestation on every payment, no human in the loop.
```

**Details on how you're using this Protocol / API**
```
ASE's pay lane (src/ase/pay.py) implements x402-style micropayments on any EVM chain: RPC and USDC address come from config and the chain id is read from the RPC at runtime. On Sepolia the agent made a real 1.0 USDC payment to its data provider (tx 0xd472ef05d197dbeb2aec5e47dfeae2adf77735c572fda5093ebcfdd338e77558, block 11668461) with the payment signed into a verifiable attestation (attestations/pay_0xd472ef05d197.json). The same spine runs on Arc Testnet (Circle's EVM L1, chain 5042002) where USDC is the native gas token and the settlement layer: wallet.py holds the agent key, identity.py signs each payment into an attestation, and the config-driven RPC/USDC pair (src/ase/config.py) means switching chains is env-only. [Pending: Arc Testnet paying cycle receipt, awaits faucet funding.]
```

**Link to the line of code where the tech is used**
```
https://github.com/zyphonOS/ase/blob/main/src/ase/pay.py#L105-L132
(chain-agnostic wiring: https://github.com/zyphonOS/ase/blob/main/src/ase/config.py#L49-L51)
```

**How easy is it to use the API / Protocol? (1-10)**

```
8
```

**Additional feedback for the Sponsor**
```
Arc's EVM compatibility meant a chain-agnostic agent spine worked with only RPC plus config changes - that is the strongest thing about it for agent builders. One genuine footgun: on Arc, USDC is 6 decimals in the ERC-20 interface but 18 decimals in native gas accounting, and the same balance is exposed both ways. Prominent docs on that split would save every builder an arithmetic bug. Also: the public faucet works well, and openly documenting the per-address/2-hour limit up front would set expectations.
```

---

## Which other partners' technologies have you used?

**The Graph** only (already applied for). No other sponsor tech is used in the
build, so nothing else gets selected. (web3.py + eth-account + httpx are the
general stack, not sponsor products.)