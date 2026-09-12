# ASE - Partner Prize Answers (FINAL, Sep 12)

Paste-order answers for the prize fields on the ETHGlobal submission form.
Three partners covered with REAL integrations: **The Graph**, **Arc**,
**Chainlink**. Ledger is NOT selected (no honest path: the track requires the
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
ASE's pay lane (src/ase/pay.py) implements x402-style micropayments on any EVM chain: RPC and USDC address come from config and the chain id is read from the RPC at runtime. On Sepolia the agent made a real 1.0 USDC payment to its data provider (tx 0xd472ef05d197dbeb2aec5e47dfeae2adf77735c572fda5093ebcfdd338e77558, block 11668461) with the payment signed into a verifiable attestation (attestations/pay_0xd472ef05d197.json). The same spine runs on Arc Testnet (Circle's EVM L1, chain 5042002) where USDC is the native gas token and the settlement layer: wallet.py holds the agent key, identity.py signs each payment into an attestation, and the config-driven RPC/USDC pair (src/ase/config.py) means switching chains is env-only. A live Arc payment fired during the event: 1.0 USDC to the data provider on Arc Testnet, block 61750008, tx 0x96d7a87b97b8784aa9b8dbba00e2a43135c4d1f9f3d047026a948c7effd0a9c9 (receipt status 0x1), signed attestation valid:true (attestations/arc_pay_0x96d7a87b...json; https://testnet.arcscan.app/tx/0x96d7a87b97b8784aa9b8dbba00e2a43135c4d1f9f3d047026a948c7effd0a9c9).
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

## Chainlink - $3,000

**Why are you applicable for this prize?**
```
ASE reads a live Chainlink price feed in every acting cycle, giving the agent external market truth alongside its own on-chain state. The read is block-stamped and signed into ASE's attestation, so the market data behind every decision is verifiable by anyone.
```

**Details on how you're using this Protocol / API**
```
ASE's read layer (src/ase/read.py) includes a Chainlink data-feed reader: read_chainlink_feed() calls latestRoundData() on an AggregatorV3Interface proxy over a public RPC (no SDK needed), reads decimals and description, and returns a block-stamped reading. The acting loop (src/ase/agent.py) runs it every cycle when ASE_CHAINLINK_FEED is set and includes the feed data - description, raw answer, human price, round id, and updated timestamp - in the reading that gets signed into the attestation. A live read is receipted on Sepolia (block 11689470, ETH/USD $2541.18, feed 0x694AA1769357215DE4FAC081bf1f309aDC325306).
```

**Link to the line of code where the tech is used**
```
https://github.com/zyphonOS/ase/blob/main/src/ase/read.py#L99-L115
(wired in the loop: https://github.com/zyphonOS/ase/blob/main/src/ase/agent.py#L73-L77)
```

**How easy is it to use the API / Protocol? (1-10)**

```
9
```

**Additional feedback for the Sponsor**
```
Chainlink feeds are the cleanest external data integration we added: a standard AggregatorV3Interface, one eth_call, zero SDK dependency, and it worked first try on the public testnet feed. Suggestions: a maintained list of live testnet feed addresses with exact proxy contracts would save lookup time, and the roundId/updatedAt transparency is excellent for agent verifiability - we read those fields straight into our attestation.
```

---

## Which other partners' technologies have you used?

None extra. The Graph, Arc, and Chainlink are all applied for as partner
prizes above, and no other sponsor's tech is used in the build - so nothing
else gets selected. (web3.py + eth-account + httpx are the general stack, not
sponsor products.)