import AseEmblem from './AseEmblem'
import StatusBadge from './StatusBadge'

export default function Header({ online }: { online: boolean }) {
  return (
    <header className="bg-ase-black border-b border-ase-border px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto flex items-center justify-between h-14">
        <div className="flex items-center gap-3">
          <AseEmblem size={28} />
          <span className="text-ase-text font-semibold tracking-wide text-lg">ASE</span>
          <span className="text-ase-text-dim text-sm hidden sm:inline">|</span>
          <span className="text-ase-text-dim text-sm hidden sm:inline">ZyphonOS</span>
        </div>
        <div className="flex items-center gap-4">
          <span className="text-ase-text-dim text-xs mono hidden md:inline">
            SEPOLIA TESTNET
          </span>
          <StatusBadge status={online ? 'online' : 'offline'} />
        </div>
      </div>
      <div className="h-px bg-gradient-to-r from-transparent via-ase-deep/40 to-transparent" />
    </header>
  )
}
