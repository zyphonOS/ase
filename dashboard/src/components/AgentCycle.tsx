import type { AgentCycleState } from '../types/agent'
import { StageIndicator } from './StatusBadge'

const stageLabels: Record<string, string> = {
  read: 'READ',
  decide: 'DECIDE',
  pay: 'PAY',
  act: 'ACT',
  attest: 'ATTEST',
}

export default function AgentCycle({ cycle }: { cycle: AgentCycleState }) {
  return (
    <div className="bg-ase-card border border-ase-border rounded-lg p-5 flex flex-col">
      <h3 className="text-xs mono text-ase-text-dim tracking-widest uppercase mb-5">
        Agent Cycle
      </h3>
      <div className="flex flex-col gap-3 flex-1 justify-center">
        {cycle.stages.map((stage, i) => (
          <div key={stage.name} className="flex items-center gap-3">
            <StageIndicator
              status={stage.status}
              label={stageLabels[stage.name]}
            />
            {i < cycle.stages.length - 1 && (
              <div className="ml-8 text-ase-text-muted text-xs">↓</div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}
