import { useState, useEffect, useCallback, useRef } from 'react'
import type { AgentState } from '../types/agent'
import Header from '../components/Header'
import AgentCycle from '../components/AgentCycle'
import ActionCard from '../components/ActionCard'
import AttestationCard from '../components/AttestationCard'
import ActivityLog from '../components/ActivityLog'
import AseEmblem from '../components/AseEmblem'
import AseIdentity from '../components/AseIdentity'
import Receipts from '../components/Receipts'
import { initialDemoState, demoCycleSteps, demoPayment, demoAttestation } from '../data/demoData'
import { fetchAgentState, triggerCycle } from '../services/api'

const CYCLE_INTERVAL_MS = 2400
const POLL_INTERVAL_MS = 2000

export default function Dashboard() {
  const [state, setState] = useState<AgentState>(initialDemoState)
  const [demoStep, setDemoStep] = useState(0)
  const [isLive, setIsLive] = useState(false)
  const [cycleRunning, setCycleRunning] = useState(false)
  const pollRef = useRef<ReturnType<typeof setInterval> | null>(null)

  // Try live API, fall back to demo
  const tryLive = useCallback(async () => {
    const liveState = await fetchAgentState()
    if (liveState) {
      setState(liveState)
      setIsLive(true)
      return true
    }
    return false
  }, [])

  useEffect(() => {
    tryLive()
  }, [tryLive])

  // Poll live API when connected
  useEffect(() => {
    if (!isLive) return

    pollRef.current = setInterval(async () => {
      const liveState = await fetchAgentState()
      if (liveState) {
        setState(liveState)
        // check if cycle just finished
        const allComplete = liveState.cycle.stages.every(
          (s) => s.status === 'complete' || s.status === 'failed'
        )
        if (allComplete) setCycleRunning(false)
      } else {
        // lost connection
        setIsLive(false)
        if (pollRef.current) clearInterval(pollRef.current)
      }
    }, POLL_INTERVAL_MS)

    return () => {
      if (pollRef.current) clearInterval(pollRef.current)
    }
  }, [isLive])

  // Demo mode auto-cycling
  useEffect(() => {
    if (isLive) return

    const timer = setInterval(() => {
      setDemoStep((prev) => {
        const next = (prev + 1) % demoCycleSteps.length
        const step = demoCycleSteps[next]

        setState((s) => {
          const newStages = s.cycle.stages.map((st) => {
            const stepIdx = demoCycleSteps.findIndex((d) => d.stage === st.name)
            const currentIdx = next
            if (stepIdx < currentIdx) return { ...st, status: 'complete' as const }
            if (stepIdx === currentIdx) return { ...st, status: 'active' as const }
            return { ...st, status: 'pending' as const }
          })

          const now = new Date()
          const timestamp = now.toTimeString().slice(0, 8)

          const newAction = step.actionType === 'payment'
            ? { type: 'payment' as const, payment: demoPayment }
            : step.actionType === 'attestation'
            ? { type: 'attestation' as const, attestation: demoAttestation }
            : {
                type: 'live-read' as const,
                live: {
                  subgraph: 'The Graph',
                  balance: '18.75 USDC',
                  token: 'USDC',
                  blockNumber: 11668461,
                },
              }

          const newAttestation = step.stage === 'attest'
            ? demoAttestation
            : s.attestation

          const newEvent = {
            timestamp,
            stage: step.stage as AgentState['activity'][0]['stage'],
            message: step.logMessage,
          }

          return {
            ...s,
            cycle: {
              ...s.cycle,
              currentStage: step.stage as AgentState['cycle']['currentStage'],
              stages: newStages,
            },
            action: newAction,
            attestation: newAttestation,
            activity: [...s.activity, newEvent],
          }
        })

        return next
      })
    }, CYCLE_INTERVAL_MS)

    return () => clearInterval(timer)
  }, [isLive])

  const handleRunCycle = async () => {
    setCycleRunning(true)
    await triggerCycle()
  }

  return (
    <div className="min-h-screen flex flex-col bg-ase-black">
      <Header online={state.online} />

      {/* Identity / Canon */}
      <AseIdentity />

      {/* Agent Status Bar */}
      <div className="bg-ase-card border-b border-ase-border px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto flex items-center justify-between h-10">
          <div className="flex items-center gap-2">
            <AseEmblem size={18} />
            <span className="mono text-xs text-ase-text-dim">
              {isLive ? 'LIVE MODE' : 'DEMO MODE'}
            </span>
          </div>
          <div className="flex items-center gap-4">
            {isLive && (
              <button
                onClick={handleRunCycle}
                disabled={cycleRunning}
                className={`mono text-xs px-3 py-1 rounded border transition-colors ${
                  cycleRunning
                    ? 'border-ase-border text-ase-text-dim cursor-not-allowed'
                    : 'border-ase-emerald/40 text-ase-emerald hover:bg-ase-emerald/10 cursor-pointer'
                }`}
              >
                {cycleRunning ? 'CYCLING...' : 'RUN CYCLE'}
              </button>
            )}
            <span className="mono text-xs text-ase-text-dim hidden sm:inline">
              {isLive ? `CYCLE ${demoStep + 1}` : `STEP ${demoStep + 1}/${demoCycleSteps.length}`}
            </span>
            <span className="mono text-xs text-ase-deep">
              {state.cycle.currentStage.toUpperCase()}
            </span>
          </div>
        </div>
      </div>

      {/* Main Dashboard */}
      <main className="flex-1 px-4 sm:px-6 lg:px-8 py-6">
        <div className="max-w-7xl mx-auto">
          {/* Three-column layout on desktop */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-4 mb-4">
            {/* Agent Cycle - Left */}
            <div className="lg:col-span-3">
              <AgentCycle cycle={state.cycle} />
            </div>

            {/* Action Card - Center (focal point) */}
            <div className="lg:col-span-6">
              <ActionCard state={state.action} />
            </div>

            {/* Attestation - Right */}
            <div className="lg:col-span-3">
              <AttestationCard data={state.attestation} />
            </div>
          </div>

          {/* Activity Log - Full width */}
          <ActivityLog events={state.activity} />

          {/* Her on-chain record */}
          <Receipts />
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-ase-black border-t border-ase-border px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto flex items-center justify-between h-10">
          <div className="flex items-center gap-2">
            <AseEmblem size={14} />
            <span className="mono text-xs text-ase-text-dim">
              ASE by ZyphonOS
            </span>
          </div>
          <span className="mono text-xs text-ase-text-dim">
            ETHOnline 2026
          </span>
        </div>
      </footer>
    </div>
  )
}
