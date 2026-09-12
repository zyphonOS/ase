import type { ActivityEvent } from '../types/agent'

const stageColor: Record<string, string> = {
  read: 'text-ase-emerald',
  decide: 'text-ase-text',
  pay: 'text-ase-emerald',
  act: 'text-ase-emerald',
  attest: 'text-ase-emerald',
}

export default function ActivityLog({ events }: { events: ActivityEvent[] }) {
  return (
    <div className="bg-ase-card border border-ase-border rounded-lg p-5">
      <h3 className="text-xs mono text-ase-text-dim tracking-widest uppercase mb-4">
        Activity
      </h3>
      <div className="mono text-xs max-h-48 overflow-y-auto">
        {events.length === 0 ? (
          <div className="text-ase-text-dim text-center py-4">No activity yet</div>
        ) : (
          <div className="flex flex-col gap-1">
            {[...events].reverse().map((e, i) => (
              <div key={i} className="flex gap-3 items-start slide-in">
                <span className="text-ase-text-dim shrink-0">{e.timestamp}</span>
                <span className={`shrink-0 w-16 uppercase ${stageColor[e.stage] || 'text-ase-text-dim'}`}>
                  {e.stage}
                </span>
                <span className="text-ase-text break-all">{e.message}</span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
