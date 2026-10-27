import type { ImportView, RunView, StageView } from '../types'

/** Die Farben des Bands (Akquise-Palette). */
export const BRAND = {
  /** primary 500, Grün: Rahmen, laufende Arbeit, Fortschritt. */
  accent: '#36ae66',
  /** primary 400: Erledigtes, damit es sich vom Laufenden abhebt. */
  done: '#6fc68e',
  /** primary 300: Phasen, die Claude lokal ausführt. */
  local: '#a8dfbd',
  warn: '#f59e0b',
  error: '#ef4444',
} as const

type Obj = Record<string, unknown>

const isObj = (v: unknown): v is Obj => typeof v === 'object' && v !== null && !Array.isArray(v)
const num = (v: unknown, fallback = 0): number => (typeof v === 'number' && Number.isFinite(v) ? v : fallback)
const str = (v: unknown, fallback = ''): string => (typeof v === 'string' ? v : fallback)

/**
 * Pulls the JSON object out of whatever an MCP tool result looks like by the
 * time it reaches us: structuredContent, content blocks, a JSON string or the
 * object itself.
 */
export function payloadOf(v: unknown): Obj | null {
  if (v === null || v === undefined) return null
  if (typeof v === 'string') {
    try {
      const parsed: unknown = JSON.parse(v)
      return isObj(parsed) ? parsed : null
    } catch {
      return null
    }
  }
  if (Array.isArray(v)) {
    for (const block of v) {
      if (isObj(block) && block.type === 'text') {
        const found = payloadOf(block.text)
        if (found) return found
      }
    }
    return null
  }
  if (!isObj(v)) return null
  if (isObj(v.structuredContent)) return v.structuredContent
  if ('content' in v && !('leads' in v)) return payloadOf(v.content)
  return v
}

export const TERMINAL_RUN = new Set([
  'completed',
  'completed_with_failures',
  'cancelled',
  'budget_exhausted',
  // The only end a run comes back from: resume_lead_run picks the same run up again after a top-up.
  'credits_exhausted',
  'limit_exhausted',
  'provider_exhausted',
  'failed',
])

export const RUN_STATUS_LABEL: Record<string, string> = {
  preparing: 'wird vorbereitet',
  running: 'läuft',
  completed: 'fertig',
  completed_with_failures: 'fertig, mit Fehlern',
  cancelled: 'abgebrochen',
  budget_exhausted: 'Lauf-Budget erreicht',
  credits_exhausted: 'Credits aufgebraucht',
  limit_exhausted: 'Planlimit erreicht',
  provider_exhausted: 'KI-Anbieter nicht verfügbar',
  failed: 'fehlgeschlagen',
  stand_unbekannt: 'Stand unbekannt',
}

export const STAGE_LABEL: Record<string, string> = {
  qualification: 'Qualifizierung',
  research: 'Recherche',
  email: 'E-Mail',
  verify: 'Prüfung',
}

export const FIT_LABEL: Record<string, { text: string; color: string }> = {
  highly_qualified: { text: 'sehr passend', color: BRAND.done },
  qualified: { text: 'passend', color: BRAND.done },
  mid_qualified: { text: 'bedingt', color: BRAND.warn },
  not_qualified: { text: 'passt nicht', color: BRAND.error },
}

/**
 * A credit amount as the server names it: the snake_case field (start_lead_run and the extras of
 * get_lead_run_status / list_lead_runs) before the camelCase one of the run resource. An explicit
 * null stays null (a byok run has no credits); a missing field keeps what was known before.
 */
const creditField = (p: Obj, snake: string, camel: string, fallback: number | null): number | null => {
  const v = snake in p ? p[snake] : camel in p ? p[camel] : undefined
  if (v === null) return null
  return typeof v === 'number' && Number.isFinite(v) ? v : fallback
}

/** Credits in German notation: up to three decimals, no trailing zeros, e.g. "12,25" or "1.250". */
export function formatCredits(n: number): string {
  const [int = '0', frac] = (Math.round(n * 1000) / 1000).toFixed(3).replace(/\.?0+$/, '').split('.')
  const grouped = int.replace(/\B(?=(\d{3})+(?!\d))/g, '.')
  return frac ? `${grouped},${frac}` : grouped
}

/** "12,25 Credits", "1 Credit". */
export const creditsLabel = (n: number): string => `${formatCredits(n)} ${n === 1 ? 'Credit' : 'Credits'}`

/**
 * A run from get_lead_run_status / list_lead_runs (camelCase resource plus snake_case extras),
 * start_lead_run (snake_case) or resume_lead_run (id, run_status and lead_total only: the rest
 * comes from the view before, the run is back from credits_exhausted).
 */
export function runFrom(p: Obj, previous?: RunView): RunView | null {
  const id = str(p.id) || str(p.lead_run_id)
  if (id === '') return null
  const status = str(p.status === 'success' ? p.run_status : p.status, previous?.status ?? 'preparing')
  const stageNames = Array.isArray(p.stages) ? p.stages.filter((s): s is string => typeof s === 'string') : []
  const progress = Array.isArray(p.stageProgress) ? p.stageProgress.filter(isObj) : []
  const stages: StageView[] = (stageNames.length > 0 ? stageNames : (previous?.stages.map(s => s.stage) ?? [])).map(stage => {
    const row = progress.find(r => r.stage === stage)
    const before = previous?.stages.find(s => s.stage === stage)
    return {
      stage,
      total: num(row?.total, before?.total ?? 0),
      pending: num(row?.pending, before?.pending ?? 0),
      running: num(row?.running, before?.running ?? 0),
      completed: num(row?.completed, before?.completed ?? 0),
      failed: row ? num(row.failed) + num(row.noResult) + num(row.cancelled) : (before?.failed ?? 0),
    }
  })
  const isTerminal = p.is_terminal === true || TERMINAL_RUN.has(status)
  const billingMode = p.billing_mode === 'credits' || p.billing_mode === 'byok' ? p.billing_mode : (previous?.billingMode ?? null)
  const byok = billingMode === 'byok'

  return {
    id,
    campaignId: num(p.campaignId ?? p.campaign_id, previous?.campaignId ?? 0),
    status,
    stages,
    leadTotal: num(p.leadTotal ?? p.lead_total, previous?.leadTotal ?? 0),
    spentCredits: byok ? null : creditField(p, 'spent_credits', 'spentCredits', previous?.spentCredits ?? null),
    budgetCredits: byok ? null : creditField(p, 'budget_credits', 'budgetCredits', previous?.budgetCredits ?? null),
    billingMode,
    isTerminal,
    isDemo: previous?.isDemo ?? false,
    // A resumed run is going again: it has not finished, whatever the view before said.
    finishedAt: isTerminal ? (previous?.finishedAt ?? null) : null,
    server: previous?.server ?? '',
    createdAt: previous?.createdAt ?? (Date.parse(str(p.createdAt)) || Date.now()),
    appUrl: urlOf(p.appUrl) ?? previous?.appUrl ?? null,
    reason: isTerminal && status !== 'completed' ? str(p.statusReason) || str(p.status_description) || null : null,
  }
}

export const IMPORT_STATUS_LABEL: Record<string, string> = {
  pending: 'wartet',
  processing: 'läuft',
  completed: 'fertig',
  failed: 'fehlgeschlagen',
  cancelled: 'abgebrochen',
}

/**
 * An import from import_leads (queued) or get_job_status (status, result).
 * get_job_status answers for every kind of job: one of another type is no
 * import, unless it is one already known.
 */
export function importFrom(p: Obj, previous?: ImportView): ImportView | null {
  const id = str(p.job_id)
  if (id === '') return null
  if (previous === undefined && typeof p.type === 'string' && p.type !== 'lead_bulk_import') return null
  const execution = isObj(p.execution) ? p.execution : null
  const result = isObj(p.result) ? p.result : null
  const status = p.status === 'success' && p.queued === true ? 'pending' : str(p.status, previous?.status ?? 'pending')
  const isTerminal = ['completed', 'failed', 'cancelled'].includes(status)
  const failure = status === 'failed' ? str(p.error) || str(result?.message) || str(execution?.failure_reason) : ''

  return {
    id,
    status,
    percent: status === 'completed' ? 100 : num(execution?.progress_percent, previous?.percent ?? 0),
    message: failure || str(execution?.progress_message, previous?.message ?? ''),
    received: num(p.received, previous?.received ?? num(result?.total)),
    campaignId: typeof p.campaign_id === 'number' ? p.campaign_id : (previous?.campaignId ?? null),
    imported: typeof result?.imported === 'number' ? result.imported : (previous?.imported ?? null),
    // The server lists the duplicate rows; older answers gave a count.
    duplicates: Array.isArray(result?.duplicates)
      ? result.duplicates.length
      : typeof result?.duplicates === 'number' ? result.duplicates : (previous?.duplicates ?? null),
    isTerminal,
    isDemo: previous?.isDemo ?? false,
    finishedAt: previous?.finishedAt ?? null,
    // import_leads links the campaign; get_job_status only the job list, so the first link stays.
    appUrl: previous !== undefined ? previous.appUrl : urlOf(p.appUrl),
    server: previous?.server ?? '',
  }
}

/** What an import came to, in a few words: imported and duplicates, or why it failed. */
export function importOutcome(job: ImportView): string {
  if (job.status === 'completed') {
    const dupes = job.duplicates ? ` · ${job.duplicates} Duplikate` : ''
    return `${job.imported ?? job.received} importiert${dupes}`
  }
  const label = IMPORT_STATUS_LABEL[job.status] ?? job.status
  if (job.isTerminal) return job.message ? `${label} · ${job.message}` : label
  // The server reports a share only where the job measures one; a bulk import does not.
  if (job.percent > 0) return `${label} · ${job.percent} %${job.message ? ` · ${job.message}` : ''}`
  return job.message ? `${label} · ${job.message}` : label
}

export type LeadRow = {
  id: number
  /** The lead's page in the app as the server names it; null when it names none. */
  appUrl: string | null
  company: string
  city: string
  email: string
  score: number | null
  fit: string
  contactStatus: string
}

export type LeadList = {
  campaign: { id: number; name: string; appUrl: string | null } | null
  leads: LeadRow[]
  total: number
}

/** list_leads, search_leads and get_lead_data all answer with leads; this reads the three alike. */
export function leadsFrom(p: Obj): LeadList | null {
  const campaign = isObj(p.campaign)
    ? { id: num(p.campaign.id), name: str(p.campaign.name), appUrl: urlOf(p.campaign.appUrl) }
    : null
  const raw = Array.isArray(p.leads) ? p.leads : isObj(p.lead) ? [p.lead] : null
  if (raw === null) return null
  const leads = raw.filter(isObj).map(l => {
    const q = isObj(l.qualification) ? l.qualification : null
    return {
      id: num(l.id),
      appUrl: urlOf(l.appUrl),
      company: str(l.company) || str(l.website) || str(l.email) || `Lead ${num(l.id)}`,
      city: str(l.city),
      email: str(l.sendingEmail) || str(l.email),
      score: typeof l.score === 'number' ? l.score : null,
      fit: str(q?.fitLevel),
      contactStatus: str(l.contactStatus),
    }
  })

  return { campaign, leads, total: num(p.total, leads.length) }
}

/**
 * Leads whose chain has ended: done with every stage, judged not qualified,
 * failed, or with nothing left to do. The server chains the stages per lead
 * and runs the leads side by side, so this is the total less every lead that
 * still has a job waiting or running. In the moment between one stage ending
 * and the next being queued a lead counts as through; the next poll corrects it.
 */
export function leadsThrough(run: RunView): number {
  if (run.isTerminal) return run.leadTotal
  // While the run prepares, or before its first status, no lead has a job yet: none is through.
  const hasWork = run.stages.some(s => (s.pending || 0) + (s.running || 0) + s.completed + s.failed > 0)
  if (run.status === 'preparing' || !hasWork) return 0
  // `|| 0`: a run kept from before `pending` was tracked reads it as absent until the next poll.
  const open = run.stages.reduce((sum, s) => sum + (s.pending || 0) + (s.running || 0), 0)
  return Math.max(0, Math.min(run.leadTotal, run.leadTotal - open))
}

/** A link the server sends, if it is one a Link may draw (https, or http://localhost). */
export function urlOf(v: unknown): string | null {
  if (typeof v !== 'string') return null
  return /^https:\/\/[^\s@]+$/.test(v) || /^http:\/\/localhost(?:[:/]|$)/.test(v) ? v : null
}

export function bar(done: number, total: number, width = 20): string {
  const ratio = total > 0 ? Math.min(1, Math.max(0, done / total)) : 0
  const full = Math.round(ratio * width)
  return '█'.repeat(full) + '░'.repeat(width - full)
}

export function appLink(base: string, path: string): string {
  return new URL(path, base.endsWith('/') ? base : `${base}/`).href
}
