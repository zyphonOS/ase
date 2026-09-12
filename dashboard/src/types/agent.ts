export type CycleStage = 'read' | 'decide' | 'pay' | 'act' | 'attest'

export type StageStatus = 'pending' | 'active' | 'complete' | 'failed'

export type ActionType = 'payment' | 'live-read' | 'attestation'

export interface AgentCycleState {
  stages: {
    name: CycleStage
    status: StageStatus
  }[]
  currentStage: CycleStage
}

export interface PaymentData {
  txHash: string
  block: number
  amount: string
  token: string
  status: 'confirmed' | 'pending' | 'failed'
}

export interface LiveData {
  subgraph: string
  balance: string
  token: string
  blockNumber: number
}

export interface AttestationData {
  signature: string
  block: number
  valid: boolean
  subgraph: string
  balance: string
}

export interface ActionCardState {
  type: ActionType
  payment?: PaymentData
  live?: LiveData
  attestation?: AttestationData
}

export interface ActivityEvent {
  timestamp: string
  stage: CycleStage
  message: string
  txHash?: string
}

export interface AgentState {
  online: boolean
  cycle: AgentCycleState
  action: ActionCardState
  attestation: AttestationData
  activity: ActivityEvent[]
  mode: 'demo' | 'live'
}
