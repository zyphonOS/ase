import type { ActionCardState } from '../types/agent'
import AseEmblem from './AseEmblem'

function PaymentState({ data }: { data: NonNullable<ActionCardState['payment']> }) {
  return (
    <div className="flex flex-col items-center gap-6 text-center">
      <div className="mono text-ase-text-dim text-xs tracking-wider">TX HASH</div>
      <div className="mono text-ase-text text-base sm:text-lg break-all max-w-full">
        {data.txHash.length > 20
          ? `${data.txHash.slice(0, 6)}...${data.txHash.slice(-4)}`
          : data.txHash}
      </div>
      <div className="bg-ase-emerald/10 border border-ase-emerald/30 rounded px-4 py-2 mono text-ase-emerald text-sm tracking-wider">
        CONFIRMED
      </div>
      <div className="text-ase-text-dim text-sm">USDC payment</div>
      <div className="grid grid-cols-2 gap-x-8 gap-y-2 text-left mono text-xs mt-2">
        <div className="text-ase-text-dim">BLOCK</div>
        <div className="text-ase-text">{data.block}</div>
      </div>
    </div>
  )
}

function LiveReadState({ data }: { data: NonNullable<ActionCardState['live']> }) {
  return (
    <div className="flex flex-col items-center gap-5 text-center">
      <div className="mono text-ase-emerald text-sm tracking-wider pulse-emerald">
        LIVE READ
      </div>
      <div className="text-ase-text text-lg">{data.subgraph}</div>
      <div className="text-ase-text-dim text-sm mono">
        {data.balance}
      </div>
      <div className="grid grid-cols-2 gap-x-8 gap-y-2 text-left mono text-xs mt-3">
        <div className="text-ase-text-dim">SUBGRAPH</div>
        <div className="text-ase-text">{data.subgraph}</div>
        <div className="text-ase-text-dim">BALANCE</div>
        <div className="text-ase-text">{data.balance}</div>
      </div>
    </div>
  )
}

function AttestationSignedState({ data }: { data: NonNullable<ActionCardState['attestation']> }) {
  return (
    <div className="flex flex-col items-center gap-5 text-center">
      <div className="mono text-ase-emerald text-sm tracking-wider">
        ATTESTATION SIGNED
      </div>
      <div className="text-ase-text-dim text-sm mono">
        block {data.block}
      </div>
      <div className="grid grid-cols-2 gap-x-8 gap-y-2 text-left mono text-xs mt-3">
        <div className="text-ase-text-dim">SUBGRAPH</div>
        <div className="text-ase-text">{data.subgraph}</div>
        <div className="text-ase-text-dim">BALANCE</div>
        <div className="text-ase-text">{data.balance}</div>
        <div className="text-ase-text-dim">STATUS</div>
        <div className="text-ase-emerald">ATTESTATION VERIFIED</div>
      </div>
    </div>
  )
}

export default function ActionCard({ state }: { state: ActionCardState }) {
  const isAttestation = state.type === 'attestation' && state.attestation?.valid

  return (
    <div
      className={`bg-ase-card border rounded-lg p-6 flex flex-col items-center justify-center min-h-[320px] ${
        isAttestation
          ? 'border-ase-emerald/40 glow-emerald-strong'
          : 'border-ase-border glow-emerald'
      }`}
    >
      <AseEmblem size={40} className="mb-6 opacity-70" />

      {state.type === 'payment' && state.payment && (
        <PaymentState data={state.payment} />
      )}
      {state.type === 'live-read' && state.live && (
        <LiveReadState data={state.live} />
      )}
      {state.type === 'attestation' && state.attestation && (
        <AttestationSignedState data={state.attestation} />
      )}
    </div>
  )
}
