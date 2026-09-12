import type { AgentState } from '../types/agent'

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export async function fetchAgentState(): Promise<AgentState | null> {
  try {
    const res = await fetch(`${API_BASE}/api/state`, {
      signal: AbortSignal.timeout(5000),
    })
    if (!res.ok) return null
    return await res.json()
  } catch {
    return null
  }
}

export async function fetchActivity(): Promise<AgentState['activity'] | null> {
  try {
    const res = await fetch(`${API_BASE}/api/activity`, {
      signal: AbortSignal.timeout(5000),
    })
    if (!res.ok) return null
    return await res.json()
  } catch {
    return null
  }
}

export async function fetchAttestation(): Promise<AgentState['attestation'] | null> {
  try {
    const res = await fetch(`${API_BASE}/api/attestation`, {
      signal: AbortSignal.timeout(5000),
    })
    if (!res.ok) return null
    return await res.json()
  } catch {
    return null
  }
}

export async function fetchStatus(): Promise<{ online: boolean } | null> {
  try {
    const res = await fetch(`${API_BASE}/api/status`, {
      signal: AbortSignal.timeout(5000),
    })
    if (!res.ok) return null
    return await res.json()
  } catch {
    return null
  }
}

export async function triggerCycle(): Promise<boolean> {
  try {
    const res = await fetch(`${API_BASE}/api/cycle`, {
      method: 'POST',
      signal: AbortSignal.timeout(5000),
    })
    return res.ok
  } catch {
    return false
  }
}
