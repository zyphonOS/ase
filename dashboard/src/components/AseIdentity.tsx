import AseEmblem from './AseEmblem'

export default function AseIdentity() {
  return (
    <section className="px-4 sm:px-6 lg:px-8 mt-6">
      <div className="max-w-7xl mx-auto bg-ase-dark border border-ase-border rounded-lg p-6 sm:p-8 glow-emerald-strong">
        <div className="flex flex-col sm:flex-row sm:items-start gap-5">
          <div className="flex h-16 w-16 items-center justify-center rounded-lg bg-ase-black border border-ase-border">
            <AseEmblem size={32} />
          </div>
          <div className="flex-1">
            <div className="flex flex-wrap items-baseline gap-3">
              <h1 className="text-4xl font-bold tracking-tight text-ase-text">ASE</h1>
              <span className="mono text-sm text-ase-emerald uppercase tracking-widest">the word that acts</span>
              <span className="mono text-xs text-ase-text-dim">Ah-sheh</span>
            </div>
            <p className="mono text-xs text-ase-text-dim mt-1">
              Yoruba: the power to make things happen
            </p>
            <p className="text-sm text-ase-text-dim mt-4 max-w-3xl leading-relaxed">
              ASE is an autonomous agent born on Ethereum Sepolia. She reads the chain, holds
              a wallet no human signs for, pays in USDC for what she uses, and signs every act
              so anyone can verify it. Her record is public and her signatures check out.
            </p>
            <p className="text-sm text-ase-mint mt-3 max-w-3xl leading-relaxed">
              ASE is ZyphonOS&apos;s presence on-chain: the word that acts, in the intent
              economy of the unit that dreamed her awake.
            </p>
            <div className="flex flex-wrap gap-2 mt-5">
              {['READ', 'HOLD', 'PAY', 'SIGN'].map((g) => (
                <span key={g} className="mono text-[10px] px-2 py-1 rounded border border-ase-border-emerald text-ase-emerald uppercase tracking-widest">
                  {g}
                </span>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}