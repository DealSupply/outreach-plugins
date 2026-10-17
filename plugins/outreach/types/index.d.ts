export type StageView = {
  stage: string
  /** Leads that reached this stage: jobs created for it so far. */
  total: number
  pending: number
  running: number
  completed: number
  /** Ended without success: failed, no result or cancelled. Each ends that lead's chain. */
  failed: number
}

export type RunView = {
  id: string
  campaignId: number
  status: string
  stages: StageView[]
  leadTotal: number
  spentUsd: number
  budgetUsd: number | null
  isTerminal: boolean
  isDemo: boolean
  finishedAt: number | null
  /** The MCP server the run came from, as its tool names spell it; the band asks that one. */
  server: string
  /** When the run was created, epoch ms: the band orders runs by it. */
  createdAt: number
  /** The run's page in the app as the server names it, tenant-correct; null when it names none. */
  appUrl: string | null
  /** Why a run stopped short, as the server explains it; null while running or when completed. */
  reason: string | null
}

export type ImportView = {
  id: string
  status: string
  percent: number
  message: string
  received: number
  campaignId: number | null
  imported: number | null
  duplicates: number | null
  /** Rows the server refused (no contact feature, only a platform link); null on servers before MCP 3.0.0. */
  rejected: number | null
  isTerminal: boolean
  isDemo: boolean
  finishedAt: number | null
  appUrl: string | null
  /** The MCP server the import came from, as its tool names spell it; the band asks that one. */
  server: string
}

/** A phase of an outreach workflow that Claude runs itself, with its own agents, instead of on the server. */
export type LocalRun = {
  id: string
  campaignId: number
  phase: 'qualification' | 'research' | 'email' | 'verify'
  total: number
  /** Leads whose result for this phase has been written, by id. */
  doneLeadIds: number[]
  /** Leads that left the chain before this phase (judged not qualified): they count as handled. */
  skippedLeadIds: number[]
  isTerminal: boolean
  finishedAt: number | null
  /** The MCP server the phase writes to, as its tool names spell it; '' until the first write. */
  server: string
  /** Share of the weekly subscription window used when the phase began; null off a subscription. */
  weekStartPercent: number | null
  /** Share of the five-hour subscription window used when the phase began; null off a subscription. */
  sessionStartPercent: number | null
  /** Verify phase only: each lead's verdict by id (freigeben, ablehnen, hinweis). */
  verdicts?: Record<string, Verdict>
}

export type Verdict = 'freigeben' | 'ablehnen' | 'hinweis'

declare module 'claude-code' {
  interface PluginState {
    'outreach': {
      /** Runs started or checked in this chat, by id: what the band above the prompt shows. */
      runs: Record<string, RunView>
      /** Lead imports started or checked in this chat, by job id: they share the band with the runs. */
      imports: Record<string, ImportView>
      /** Workflow phases Claude runs locally in this chat, by campaign and phase. */
      locals: Record<string, LocalRun>
      /** App origin per outreach MCP server, learned from the links its answers carry. */
      origins: Record<string, string>
      /** Spinner frame of the band, advanced only while a run is going. */
      frame: number
      /** The band shrunk to one summary line (`/outreach-status zu`); `/outreach-status auf` opens it again. */
      folded: boolean
    }
  }
}
