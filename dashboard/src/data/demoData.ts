import type { AgentState } from '../types/agent'

const now = new Date()
const ts = (offset: number) => {
  const d = new Date(now.getTime() - offset * 1000)
  return d.toTimeString().slice(0, 8)
}

export const initialDemoState: AgentState = {
  online: true,
  mode: 'demo',
  cycle: {
    currentStage: 'read',
    stages: [
      { name: 'read', status: 'active' },
      { name: 'decide', status: 'pending' },
      { name: 'pay', status: 'pending' },
      { name: 'act', status: 'pending' },
      { name: 'attest', status: 'pending' },
    ],
  },
  action: {
    type: 'live-read',
    live: {
      subgraph: 'The Graph',
      balance: '18.75 USDC',
      token: 'USDC',
      blockNumber: 11668461,
    },
  },
  attestation: {
    signature: '',
    block: 0,
    valid: false,
    subgraph: 'The Graph',
    balance: '18.75 USDC',
  },
  activity: [
    { timestamp: ts(5), stage: 'read', message: 'Initializing agent cycle...' },
  ],
}

export const demoCycleSteps: {
  stage: string
  actionType: 'live-read' | 'payment' | 'attestation'
  logMessage: string
}[] = [
  {
    stage: 'read',
    actionType: 'live-read',
    logMessage: 'The Graph subgraph',
  },
  {
    stage: 'decide',
    actionType: 'live-read',
    logMessage: 'Balance sufficient — 18.75 USDC',
  },
  {
    stage: 'pay',
    actionType: 'payment',
    logMessage: '18.75 USDC',
  },
  {
    stage: 'act',
    actionType: 'payment',
    logMessage: 'tx 0xd472ef05d197...7558 confirmed',
  },
  {
    stage: 'attest',
    actionType: 'attestation',
    logMessage: 'valid: true',
  },
]

export const demoPayment = {
  txHash: '0xd472ef05d197ef90b7b8f4b0c317a62e7755f0b48e6e92c4a1d8f3e7b9c0d2f',
  block: 11668461,
  amount: '18.75',
  token: 'USDC',
  status: 'confirmed' as const,
}

export const demoAttestation = {
  signature: '0x9f3e2c4a7b6d1e8f5a4b3c2d1e0f9a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f8c9a8b3e7d4c1f5a6b7c8d9e0f1234',
  block: 11668461,
  valid: true,
  subgraph: 'The Graph',
  balance: '18.75 USDC',
}
