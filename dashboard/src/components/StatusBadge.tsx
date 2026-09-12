import type { StageStatus } from '../types/agent'

export default function StatusBadge({ status }: { status: 'online' | 'offline' }) {
  const isOnline = status === 'online'
  return (
    <span className="flex items-center gap-2 text-sm mono">
      <span
        className={`inline-block w-2 h-2 rounded-full ${
          isOnline ? 'bg-ase-emerald pulse-emerald' : 'bg-red-500'
        }`}
      />
      <span className={isOnline ? 'text-ase-emerald' : 'text-red-400'}>
        {isOnline ? 'AGENT ONLINE' : 'AGENT OFFLINE'}
      </span>
    </span>
  )
}

export function StageIndicator({ status, label }: { status: StageStatus; label: string }) {
  const colorMap: Record<StageStatus, string> = {
    pending: 'text-ase-text-dim',
    active: 'text-ase-emerald pulse-emerald',
    complete: 'text-ase-emerald',
    failed: 'text-red-400',
  }

  const iconMap: Record<StageStatus, string> = {
    pending: '○',
    active: '●',
    complete: '✓',
    failed: '✗',
  }

  return (
    <div className={`flex items-center gap-3 mono text-sm ${colorMap[status]}`}>
      <span className="w-5 text-center check-mark">{iconMap[status]}</span>
      <span className={status === 'pending' ? 'opacity-40' : ''}>{label}</span>
    </div>
  )
}
