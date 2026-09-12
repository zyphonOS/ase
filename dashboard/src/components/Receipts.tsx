import AseEmblem from './AseEmblem'

const RECEIPTS = [
  {
    label: 'FIRST READING',
    value: '18.75 USDC',
    sub: 'live balance, read by ASE from chain state',
  },
  {
    label: 'ON-CHAIN PAYMENT',
    value: '1.0 USDC',
    sub: 'block 11668461',
    tx: '0xd472ef05d197dbeb2aec5e47dfeae2adf77735c572fda5093ebcfdd338e77558',
  },
  {
    label: 'ATTESTATION',
    value: 'valid: true',
    sub: 'signed, recoverable to agent address',
  },
]

export default function Receipts() {
  return (
    <section className="mt-4">
      <div className="flex items-center gap-2 mb-2">
        <AseEmblem size={14} />
        <span className="mono text-xs text-ase-emerald uppercase tracking-widest">Her record, on-chain</span>
        <span className="mono text-[10px] text-ase-text-muted uppercase">verify everything</span>
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
        {RECEIPTS.map((r) => (
          <div key={r.label} className="bg-ase-card border border-ase-border rounded p-4 glow-emerald">
            <div className="mono text-[10px] text-ase-text-dim uppercase tracking-widest">{r.label}</div>
            <div className="mono text-xl font-semibold text-ase-emerald mt-1">{r.value}</div>
            <div className="mono text-[11px] text-ase-text-dim mt-1">{r.sub}</div>
            {r.tx && (
              <div className="mono text-[10px] text-ase-text-muted break-all mt-2 leading-tight">
                {r.tx.slice(0, 22)}...{r.tx.slice(-8)}
              </div>
            )}
          </div>
        ))}
      </div>
      <p className="mono text-[11px] text-ase-text-muted mt-2">
        Payment transaction live on Ethereum Sepolia. Her signatures verify against her own address.
      </p>
    </section>
  )
}