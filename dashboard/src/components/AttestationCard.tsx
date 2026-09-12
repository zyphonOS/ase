import type { AttestationData } from '../types/agent'

export default function AttestationCard({ data }: { data: AttestationData }) {
  const hasSig = data.signature.length > 0

  return (
    <div className="bg-ase-card border border-ase-border rounded-lg p-5 flex flex-col">
      <h3 className="text-xs mono text-ase-text-dim tracking-widest uppercase mb-4">
        Attestation
      </h3>

      <div className="flex items-center gap-2 mb-4">
        {data.valid ? (
          <>
            <span className="text-ase-emerald text-lg check-mark">✓</span>
            <span className="text-ase-emerald mono text-sm">valid: true</span>
          </>
        ) : (
          <>
            <span className="text-ase-text-dim text-lg">○</span>
            <span className="text-ase-text-dim mono text-sm">
              {hasSig ? 'valid: false' : 'awaiting attestation'}
            </span>
          </>
        )}
      </div>

      {hasSig && (
        <div className="mt-auto">
          <div className="text-xs mono text-ase-text-dim tracking-wider mb-2">
            SIGNATURE
          </div>
          <div className="mono text-xs text-ase-text leading-relaxed break-all bg-ase-black/50 rounded p-3 border border-ase-border">
            {data.signature.length > 80
              ? `${data.signature.slice(0, 40)}\n${data.signature.slice(40, 80)}\n${data.signature.slice(80)}`
              : data.signature}
          </div>
        </div>
      )}

      {!hasSig && (
        <div className="mt-auto text-center text-ase-text-dim mono text-xs">
          Awaiting cycle completion
        </div>
      )}
    </div>
  )
}
