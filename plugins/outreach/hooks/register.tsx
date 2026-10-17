import { atom, read, update } from 'claude-code'
import type { EngineInterface, Register } from 'claude-code'

import type { ImportView, LocalRun, RunView, StageView, Verdict } from '../types'
import {
  BRAND,
  FIT_LABEL,
  RUN_STATUS_LABEL,
  STAGE_LABEL,
  appLink,
  bar,
  importFrom,
  importOutcome,
  leadsThrough,
  leadsFrom,
  payloadOf,
  runFrom,
  type LeadList,
  type LeadRow,
} from './model'

/**
 * The outreach MCP tools' results drawn readable and clickable in the chat,
 * and the lead runs and imports of this chat as one band above the prompt. The
 * band asks the server itself only for those, every POLL_MS, until each has ended.
 */

const PREVIEW_ROWS = 6
const POLL_MS = 20_000
/** Rounds without a usable answer after which the band stops asking for a run. */
const MAX_MISSES = 3
/** How long a run that ended stays in the band. */
const LINGER_MS = 120_000

const runs = atom({ plugin: 'outreach', key: 'runs' } as const, {})
const imports = atom({ plugin: 'outreach', key: 'imports' } as const, {})
const locals = atom({ plugin: 'outreach', key: 'locals' } as const, {})
const origins = atom({ plugin: 'outreach', key: 'origins' } as const, {})
const frame = atom({ plugin: 'outreach', key: 'frame' } as const, 0)
const folded = atom({ plugin: 'outreach', key: 'folded' } as const, false)
let configuredServer = 'akquise'
let poller: { cancel: () => void } | null = null
const missedRounds = new Map<string, number>()
let spinner: { cancel: () => void } | null = null

let base = 'https://outreach.akquise.de'

/**
 * Which MCP servers speak the outreach tools. A server is recognised by
 * what it offers, not by its name: every customer names it as they like when
 * setting it up ("akquise", "listm8", "Outreach" ...), and one session may hold
 * several (a paid account and a local one). Cached per session; a server first
 * seen later (still connecting at start) is looked up when its first call comes.
 */
const SIGNATURE = ['list_leads', 'start_lead_run', 'get_lead_run_status'] as const
const OUR_TOOLS = new Set([
  'list_leads', 'search_leads', 'get_lead_data', 'start_lead_run', 'get_lead_run_status', 'cancel_lead_run',
  'list_lead_runs', 'import_leads', 'get_job_status', 'write_lead_details', 'save_lead_variables',
  'approve_lead_variables', 'reject_lead_variables',
])
let knownServers = new Map<string, boolean>()

type Recognized = { server: string; name: string }

const parseTool = (tool: string): Recognized | null => {
  const m = /^mcp__(.+)__([a-z_]+)$/.exec(tool)
  return m && m[1] !== undefined && m[2] !== undefined ? { server: m[1], name: m[2] } : null
}

/** Re-reads the tool list and notes, per MCP server, whether it offers the whole signature. */
const refreshServers = async ($: EngineInterface) => {
  const offered = new Map<string, Set<string>>()
  let tools: Awaited<ReturnType<EngineInterface['tool']['list']>> = []
  try {
    tools = await $.tool.list()
  } catch {
    return // No list now: keep what is known; the configured server still works.
  }
  for (const info of tools) {
    const parsed = info.mcp ? parseTool(info.name) : null
    if (parsed === null) continue
    const names = offered.get(parsed.server) ?? new Set<string>()
    names.add(parsed.name)
    offered.set(parsed.server, names)
  }
  for (const [srv, names] of offered) knownServers.set(srv, SIGNATURE.every(n => names.has(n)))
}

/** The outreach call behind a tool name, or null when the tool is not one of ours. */
const recognize = async ($: EngineInterface, tool: string): Promise<Recognized | null> => {
  const parsed = parseTool(tool)
  if (parsed === null || !OUR_TOOLS.has(parsed.name)) return null
  if (parsed.server === configuredServer) return parsed
  if (!knownServers.has(parsed.server)) await refreshServers($)
  return knownServers.get(parsed.server) === true ? parsed : null
}

/** Every server recognised now, the configured one included. */
const akquiseServers = async ($: EngineInterface): Promise<string[]> => {
  await refreshServers($)
  const found = [...knownServers].filter(([, ok]) => ok).map(([srv]) => srv)
  return found.includes(configuredServer) ? found : [...found, configuredServer]
}

type El = ReturnType<EngineInterface['ui']['resolve']>

/** A run's page: the link its server sent, else built from the configured app address. */
const runHref = (run: RunView) => run.appUrl ?? appLink(base, `/campaigns/${run.campaignId}/leads`)

const leadPreview = (el: El, list: LeadList) => {
  const { Box, Text, Link } = el
  const shown = list.leads.slice(0, PREVIEW_ROWS)
  const more = list.total - shown.length
  const cid = list.campaign?.id
  const leadHref = (lead: LeadRow) => lead.appUrl ?? appLink(base, cid ? `/campaigns/${cid}/leads/${lead.id}` : `/leads/${lead.id}`)

  return (
    <Box flexDirection="column" borderStyle="round" borderColor={BRAND.accent} paddingX={1}>
      <Box gap={1}>
        <Text bold>{`${list.total} ${list.total === 1 ? 'Lead' : 'Leads'}`}</Text>
        {list.campaign && <Text dimColor>{`in „${list.campaign.name}“`}</Text>}
      </Box>
      {shown.map(lead => {
        const fit = FIT_LABEL[lead.fit]
        return (
          <Box key={`lead-${lead.id}`} gap={1}>
            <Text color={fit?.color ?? 'gray'}>●</Text>
            <Box width={28}><Text wrap="truncate-end">{lead.company}</Text></Box>
            <Box width={12}><Text dimColor wrap="truncate-end">{lead.city || '–'}</Text></Box>
            <Box width={14}><Text color={fit?.color} dimColor={fit === undefined} wrap="truncate-end">{fit?.text ?? 'nicht bewertet'}</Text></Box>
            <Box width={4}><Text dimColor>{lead.score === null ? '' : String(lead.score)}</Text></Box>
            <Link href={leadHref(lead)} label="Öffnen ↗" />
          </Box>
        )
      })}
      <Box gap={1}>
        {more > 0 && <Text dimColor>{`… ${more} weitere`}</Text>}
        <Link href={list.campaign?.appUrl ?? appLink(base, cid ? `/campaigns/${cid}/leads` : '/leads')} label="Alle in der App ↗" />
      </Box>
    </Box>
  )
}

/** In the chat a started run is one line; its progress lives in the band. */
const startLine = (el: El, run: RunView) => {
  const { Box, Text, Link } = el
  const stages = run.stages.map(s => STAGE_LABEL[s.stage] ?? s.stage).join(' + ')
  const budget = run.budgetUsd === null ? '' : ` · Budget ${run.budgetUsd.toFixed(2)} $`

  return (
    <Box gap={1}>
      <Text color={BRAND.accent}>▶</Text>
      <Text>{`Lead-Run gestartet · ${run.leadTotal} Leads · ${stages}${budget}`}</Text>
      <Text dimColor>· Fortschritt über dem Prompt</Text>
      {(run.appUrl !== null || run.campaignId > 0) && <Link href={runHref(run)} label="Öffnen ↗" />}
    </Box>
  )
}

const RUN_COLOR = (run: RunView) =>
  !run.isTerminal ? BRAND.accent : run.status === 'completed' ? BRAND.done : run.status === 'cancelled' ? 'gray' : BRAND.warn

/** One run in the band: the stage it is in, done against the lead total, and why it stopped if it did. */
const STAGE_SHORT: Record<string, string> = { qualification: 'Qual.', research: 'Rech.', email: 'Mail' }

/** Cells of a two-part bar: finished, set aside, and what is left, over `width`. */
const barCells = (total: number, finished: number, setAside: number, width: number): [number, number, number] => {
  const cells = (n: number) => (total > 0 ? Math.round((Math.min(n, total) / total) * width) : 0)
  const done = cells(finished)
  const aside = Math.max(0, cells(finished + setAside) - done)
  return [done, aside, width - done - aside]
}

/**
 * One run as one row of the band, for when several share it. It never wraps:
 * the left part shrinks and cuts with an ellipsis, cost and link stay put on
 * the right. Of the stages it names only the one at work, so rows of runs with
 * different stages still line up.
 */
const bandRow = (el: El, run: RunView, step: number) => {
  const { Box, Text, Link } = el
  const color = RUN_COLOR(run)
  const isShort = run.isTerminal && run.status !== 'completed'
  const finished = run.stages[run.stages.length - 1]?.completed ?? 0
  const failed = run.stages.reduce((sum, s) => sum + s.failed, 0)
  const setAside = isShort ? 0 : Math.max(0, leadsThrough(run) - finished - failed)
  const [doneCells, asideCells, restCells] = barCells(run.leadTotal, finished, setAside, 10)
  const inFlight = (s: StageView) => (run.isTerminal ? 0 : (s.pending || 0) + (s.running || 0))
  // The stage at work: the furthest one with jobs in flight, else the last one begun.
  const working = [...run.stages].reverse().find(s => inFlight(s) > 0)
  const shown = working ?? [...run.stages].reverse().find(s => s.total > 0) ?? run.stages[0]
  const state = run.isTerminal
    ? (RUN_STATUS_LABEL[run.status] ?? run.status)
    : `${finished} fertig${setAside > 0 ? ` · ${setAside} raus` : ''}`
  const stage = shown === undefined || run.isTerminal ? '' : `${STAGE_SHORT[shown.stage] ?? shown.stage} ${shown.completed}/${shown.total}`

  return (
    <Box key={`run-${run.id}`} flexDirection="column">
      <Box>
        <Box flexGrow={1} flexShrink={1} gap={1}>
          <Text bold color={working !== undefined ? BRAND.accent : color}>
            {working !== undefined ? SPIN[step % SPIN.length] : run.isTerminal ? '■' : '▶'}
          </Text>
          <Box width={9} flexShrink={0}><Text>{`${run.leadTotal} Leads`}</Text></Box>
          <Box flexShrink={0}>
            <Text color={color}>{'█'.repeat(doneCells)}</Text>
            <Text dimColor>{'█'.repeat(asideCells)}</Text>
            <Text color={color} dimColor>{'░'.repeat(restCells)}</Text>
          </Box>
          <Text bold color={run.isTerminal ? color : undefined} wrap="truncate-end">{state}</Text>
          {stage !== '' && <Text dimColor wrap="truncate-end">{`· ${stage}`}</Text>}
          {failed > 0 && <Text color={BRAND.error} wrap="truncate-end">{`· ${failed} Fehler`}</Text>}
        </Box>
        <Box flexShrink={0} gap={2} marginLeft={1}>
          <Text dimColor>{`${run.spentUsd.toFixed(2)} $`}</Text>
          {(run.appUrl !== null || run.campaignId > 0) && <Link href={runHref(run)} label="Öffnen ↗" />}
        </Box>
      </Box>
      {run.reason !== null && <Text color={BRAND.warn} wrap="truncate-end">{`  ${run.reason}`}</Text>}
    </Box>
  )
}

/**
 * One run as a funnel, a row per stage: each stage against the leads that reached it,
 * so 10 qualified, 5 passed on, 5 in research reads as it happened. The stage at work
 * turns a spinner; one already done shows a tick.
 */
const funnelRun = (el: El, run: RunView, step: number) => {
  const { Box, Text, Link } = el
  const color = RUN_COLOR(run)
  const budget = run.budgetUsd === null ? '' : `/${run.budgetUsd.toFixed(2)}`
  const head = run.isTerminal ? (RUN_STATUS_LABEL[run.status] ?? run.status) : `${run.leadTotal} Leads`

  return (
    <Box key={`funnel-${run.id}`} flexDirection="column">
      <Box justifyContent="space-between">
        <Box gap={1}>
          <Text bold>Outreach · Lead-Run</Text>
          <Text color={color}>{`· ${head}`}</Text>
        </Box>
        <Box gap={2}>
          <Text dimColor>{`${run.spentUsd.toFixed(2)}${budget} $`}</Text>
          {(run.appUrl !== null || run.campaignId > 0) && <Link href={runHref(run)} label="Öffnen ↗" />}
        </Box>
      </Box>
      {run.stages.map((s, i) => {
        const prev = run.stages[i - 1]
        const next = run.stages[i + 1]
        // The first stage is reached by every lead once the run has prepared; later ones by those passed on.
        const reached = i === 0 && s.total === 0 && run.status === 'preparing' ? run.leadTotal : s.total
        // An ended run has nothing in flight, whatever its last counters still say.
        const inFlight = (x: StageView) => (run.isTerminal ? 0 : (x.pending || 0) + (x.running || 0))
        const live = inFlight(s)
        const earlierLive = run.stages.slice(0, i).some(p => inFlight(p) > 0)
        const isDone = reached > 0 && live === 0 && !earlierLive
        const isSkipped = reached === 0 && (run.isTerminal || (prev !== undefined && !earlierLive && run.status !== 'preparing'))
        const mark = live > 0 ? SPIN[step % SPIN.length] : isDone ? '✓' : isSkipped ? '–' : '·'
        const markColor = live > 0 ? BRAND.accent : isDone ? BRAND.done : undefined
        const out = next !== undefined && s.stage === 'qualification' && isDone ? Math.max(0, s.completed - next.total) : 0
        const notes = [
          out > 0 ? `${next !== undefined ? next.total : 0} passen · ${out} raus` : '',
          live > 0 && s.running > 0 ? `${s.running} laufen` : '',
          live > 0 && (s.pending || 0) > 0 ? `${s.pending} warten` : '',
          isSkipped ? 'übersprungen' : '',
          !isDone && !isSkipped && live === 0 ? 'wartet' : '',
        ].filter(n => n !== '')

        return (
          <Box key={`funnel-${run.id}-${s.stage}`} gap={1}>
            <Text color={markColor} dimColor={markColor === undefined}>{mark}</Text>
            <Box width={15}><Text dimColor={!isDone && live === 0}>{STAGE_LABEL[s.stage] ?? s.stage}</Text></Box>
            <Text color={isDone ? BRAND.done : BRAND.accent} dimColor={!isDone && live === 0}>{bar(s.completed, Math.max(1, reached), 10)}</Text>
            <Box width={7}><Text>{reached > 0 ? `${s.completed}/${reached}` : '–'}</Text></Box>
            <Text dimColor>{notes.join(' · ')}</Text>
            {s.failed > 0 && <Text color={BRAND.error}>{`· ${s.failed} Fehler`}</Text>}
          </Box>
        )
      })}
      {run.reason !== null && <Text color={BRAND.warn} wrap="wrap">{run.reason}</Text>}
    </Box>
  )
}

/** The subscription windows now, in percent used; null where off a subscription. */
type Usage = { session: number | null; week: number | null }

const usageNow = async ($: EngineInterface): Promise<Usage> => {
  try {
    const { rateLimits } = await $.session.usage()
    const of = (kind: string) => rateLimits.find(r => r.kind === kind)?.percentUsed ?? null
    return { session: of('five_hour'), week: of('seven_day') }
  } catch {
    return { session: null, week: null }
  }
}

/**
 * What the run has used of the subscription windows: how far each rose since the run began, not
 * where it stands. The engine reports whole percent, so a rise below one point reads as „< 1 %“.
 * The windows count the whole account, so other sessions running at the same time show here too.
 */
const usageText = (group: LocalRun[], now: Usage): string | null => {
  const part = (label: string, current: number | null, starts: (number | null)[]) => {
    const known = starts.filter((v): v is number => v !== null)
    if (current === null || known.length === 0) return null
    const rose = Math.max(0, current - Math.min(...known))
    return rose < 1 ? `${label} < 1 %` : `${label} ${Math.round(rose)} %`
  }
  const parts = [
    part('5 h', now.session, group.map(l => l.sessionStartPercent)),
    part('Woche', now.week, group.map(l => l.weekStartPercent)),
  ].filter((v): v is string => v !== null)
  return parts.length === 0 ? null : `verbraucht ${parts.join(' · ')}`
}

/** A local phase's campaign page: on the origin its server links to; null while that is unknown. */
const localHref = (local: LocalRun, known: Record<string, string>) => {
  const origin = local.server === '' ? undefined : known[local.server]
  return origin === undefined ? null : appLink(origin, `/campaigns/${local.campaignId}/leads`)
}

const PHASE_SHORT: Record<string, string> = { qualification: 'Qual', research: 'Rech', email: 'Mail', verify: 'Prüf' }

/** The phases of one campaign's run in the subscription, in the order they happen. */
const groupPhases = (phases: LocalRun[]): LocalRun[][] => {
  const byCampaign = new Map<number, LocalRun[]>()
  for (const local of phases) byCampaign.set(local.campaignId, [...(byCampaign.get(local.campaignId) ?? []), local])
  const order = (l: LocalRun) => PHASES.indexOf(l.phase as Phase)
  return [...byCampaign.values()].map(g => [...g].sort((a, b) => order(a) - order(b)))
}

/**
 * One run in the subscription as one row: its phases counted from the writes, so exact and without
 * polling. Leads judged not qualified leave the later phases and count as handled, so a run that
 * did all it could ends green, not as if work were missing.
 */
const localRow = (el: El, group: LocalRun[], href: string | null, usage: Usage) => {
  const { Box, Text, Link } = el
  const last = group[group.length - 1]
  if (last === undefined) return null
  const total = Math.max(...group.map(l => l.total))
  const done = last.doneLeadIds.length
  const skipped = last.skippedLeadIds.length
  const isTerminal = group.every(l => l.isTerminal)
  const complete = group.every(l => l.doneLeadIds.length + l.skippedLeadIds.length >= l.total)
  const color = isTerminal ? (complete ? BRAND.done : BRAND.warn) : BRAND.local
  const [doneCells, asideCells, restCells] = barCells(total, done, skipped, 14)
  const verdicts = Object.values(last.verdicts ?? {})
  const tally = (v: Verdict) => verdicts.filter(x => x === v).length
  const state =
    last.phase === 'verify'
      ? `${done} geprüft` +
        [['frei', tally('freigeben')], ['abgelehnt', tally('ablehnen')], ['Hinweis', tally('hinweis')]]
          .filter(([, n]) => Number(n) > 0)
          .map(([label, n]) => ` · ${n} ${label}`)
          .join('')
      : `${done} fertig${skipped > 0 ? ` · ${skipped} aussortiert` : ''}`
  const stages = group
    .map(l => `${PHASE_SHORT[l.phase] ?? l.phase} ${l.doneLeadIds.length}/${l.total - l.skippedLeadIds.length}`)
    .join(' · ')
  const used = usageText(group, usage)

  return (
    <Box key={`local-${last.campaignId}`}>
      <Box flexGrow={1} flexShrink={1} gap={1}>
        <Text bold color={color}>{isTerminal ? '■' : '▶'}</Text>
        <Box width={9} flexShrink={0}><Text>{`${total} Leads`}</Text></Box>
        <Box flexShrink={0}>
          <Text color={color}>{'█'.repeat(doneCells)}</Text>
          <Text dimColor>{'█'.repeat(asideCells)}</Text>
          <Text color={color} dimColor>{'░'.repeat(restCells)}</Text>
        </Box>
        <Text bold color={isTerminal ? color : undefined} wrap="truncate-end">{state}</Text>
        <Text dimColor wrap="truncate-end">{`· ${stages} · im Abo`}</Text>
      </Box>
      <Box flexShrink={0} gap={2} marginLeft={1}>
        {used !== null && <Text dimColor>{used}</Text>}
        {href !== null && <Link href={href} label="Öffnen ↗" />}
      </Box>
    </Box>
  )
}

/**
 * One import as one row, lined up with the run rows. No bar: a bulk import
 * reports no share while it works, only its state and in the end its result.
 */
const importRow = (el: El, job: ImportView, step: number) => {
  const { Box, Text, Link } = el
  const color = !job.isTerminal ? BRAND.accent : job.status === 'completed' ? BRAND.done : BRAND.error

  return (
    <Box key={`import-${job.id}`}>
      <Box flexGrow={1} flexShrink={1} gap={1}>
        <Text bold color={color}>{job.isTerminal ? '■' : SPIN[step % SPIN.length]}</Text>
        <Box width={9} flexShrink={0}><Text>{`${job.received} Leads`}</Text></Box>
        <Box width={10} flexShrink={0}><Text>Import</Text></Box>
        <Text bold={job.isTerminal} color={job.isTerminal ? color : undefined} wrap="truncate-end">{importOutcome(job)}</Text>
      </Box>
      <Box flexShrink={0} marginLeft={1}>
        <Link href={importHref(job)} label="Öffnen ↗" />
      </Box>
    </Box>
  )
}

/** The band folded to one line: how many runs, how many still going; `/outreach-status auf` opens it. */
const foldedBand = (el: El, shown: RunView[], jobs: ImportView[], phases: LocalRun[]) => {
  const { Box, Text } = el
  const groups = groupPhases(phases)
  const count = shown.length + jobs.length + groups.length
  const active =
    shown.filter(r => !r.isTerminal).length +
    jobs.filter(j => !j.isTerminal).length +
    groups.filter(g => g.some(l => !l.isTerminal)).length
  const color = active > 0 ? BRAND.accent : BRAND.done

  return (
    <Box borderStyle="round" borderColor={color} paddingX={1} justifyContent="space-between">
      <Text bold>{`Outreach · ${count} ${count === 1 ? 'Lauf' : 'Läufe'} · ${active === 0 ? 'alle beendet' : `${active} ${active === 1 ? 'läuft' : 'laufen'}`}`}</Text>
      <Text dimColor>eingeklappt · /outreach-status auf</Text>
    </Box>
  )
}

/** Server runs, imports and local phases in one frame. A single run alone shows as a funnel; else a row each. */
const band = (
  el: El,
  shown: RunView[],
  jobs: ImportView[],
  phases: LocalRun[],
  step: number,
  known: Record<string, string>,
  usage: Usage,
) => {
  const { Box, Text } = el
  const groups = groupPhases(phases)
  const count = shown.length + jobs.length + groups.length
  const active =
    shown.filter(r => !r.isTerminal).length +
    jobs.filter(j => !j.isTerminal).length +
    groups.filter(g => g.some(l => !l.isTerminal)).length
  const allGood =
    shown.every(r => r.status === 'completed') &&
    jobs.every(j => j.status === 'completed') &&
    phases.every(l => l.doneLeadIds.length + l.skippedLeadIds.length >= l.total)
  const color = active > 0 ? BRAND.accent : allGood ? BRAND.done : BRAND.warn
  const single = shown.length === 1 && jobs.length === 0 && groups.length === 0 ? shown[0] : undefined

  if (single !== undefined) {
    return (
      <Box flexDirection="column" borderStyle="round" borderColor={color} paddingX={1}>
        {funnelRun(el, single, step)}
      </Box>
    )
  }

  const summary = active === 0 ? 'alle beendet' : active === 1 ? '1 läuft' : `${active} laufen`
  const title = jobs.length === count ? (count === 1 ? 'Import' : `${count} Importe`) : `${count} Läufe`

  return (
    <Box flexDirection="column" borderStyle="round" borderColor={color} paddingX={1}>
      <Box justifyContent="space-between">
        <Text bold>{`Outreach · ${title}`}</Text>
        <Text color={color}>{summary}</Text>
      </Box>
      {shown.map(run => bandRow(el, run, step))}
      {jobs.map(job => importRow(el, job, step))}
      {groups.map(g => localRow(el, g, g.map(l => localHref(l, known)).find(h => h !== null) ?? null, usage))}
    </Box>
  )
}

/** How many runs that have ended stay in the band beside the ones still going. */
const ENDED_SHOWN = 2

/**
 * Every run still going, oldest first, then the few that ended last. No cap on
 * the active ones: a run started last still belongs in the band, with 0 % too.
 * (list_lead_runs answers newest first, so insertion order is no start order.)
 */
const bandRuns = (all: RunView[]): RunView[] => [
  ...all.filter(r => !r.isTerminal).sort((a, b) => (a.createdAt || 0) - (b.createdAt || 0)),
  ...all
    .filter(r => r.isTerminal)
    .sort((a, b) => (b.finishedAt ?? 0) - (a.finishedAt ?? 0))
    .slice(0, ENDED_SHOWN),
]

const bandImports = (all: ImportView[]): ImportView[] => [
  ...all.filter(j => !j.isTerminal),
  ...all
    .filter(j => j.isTerminal)
    .sort((a, b) => (b.finishedAt ?? 0) - (a.finishedAt ?? 0))
    .slice(0, ENDED_SHOWN),
]

/** A run in the subscription has up to three phases; those of the last two runs stay in view once ended. */
const ENDED_PHASES_SHOWN = 6

const bandPhases = (all: LocalRun[]): LocalRun[] => [
  ...all.filter(l => !l.isTerminal),
  ...all
    .filter(l => l.isTerminal)
    .sort((a, b) => (b.finishedAt ?? 0) - (a.finishedAt ?? 0))
    .slice(0, ENDED_PHASES_SHOWN),
]

// ── the runs of this chat ────────────────────────────────────────────────

const call = async ($: EngineInterface, server: string, tool: string, args: Record<string, unknown>) => {
  const res = await $.mcp.call(server, tool, args)
  return res.isError ? null : payloadOf(res.structuredContent ?? res.content)
}

/** Keeps a run's newest state; says so in a toast when it has just ended. */
const putRun = async ($: EngineInterface, payload: Record<string, unknown>, server: string) => {
  let ended: RunView | null = null
  await update($, runs, all => {
    const id = String(payload.id ?? payload.lead_run_id ?? '')
    const before = all[id]
    const next = runFrom(payload, before)
    if (next === null) return all
    next.server = server
    if (next.isTerminal && next.finishedAt === null) next.finishedAt = Date.now()
    if (next.isTerminal && before !== undefined && !before.isTerminal) ended = next
    return { ...all, [next.id]: next }
  })
  if (ended !== null) {
    const run: RunView = ended
    $.ui.toast(`Outreach: Lead-Run ${RUN_STATUS_LABEL[run.status] ?? run.status}`)
  }
}

/** Keeps an import's newest state; says what it came to in a toast when it has just ended. */
const putImport = async ($: EngineInterface, payload: Record<string, unknown>, server: string): Promise<boolean> => {
  let ended: ImportView | null = null
  let kept = false
  await update($, imports, all => {
    const before = all[String(payload.job_id ?? '')]
    const next = importFrom(payload, before)
    if (next === null) return all
    kept = true
    next.server = server
    if (next.isTerminal && next.finishedAt === null) next.finishedAt = Date.now()
    if (next.isTerminal && before !== undefined && !before.isTerminal) ended = next
    return { ...all, [next.id]: next }
  })
  if (ended !== null) {
    const job: ImportView = ended
    $.ui.toast(`Outreach: Import ${importOutcome(job)}`)
  }
  return kept
}

const isGoing = async ($: EngineInterface) =>
  Object.values(await read($, runs)).some(r => !r.isTerminal) || Object.values(await read($, imports)).some(j => !j.isTerminal)

/** Asks for each run and import still going; stops asking once none is. Ended ones leave the band after LINGER_MS. */
const tick = async ($: EngineInterface) => {
  for (const job of Object.values(await read($, imports))) {
    if (job.isTerminal) continue
    try {
      const server = job.server || configuredServer
      const status = await call($, server, 'get_job_status', { job_id: job.id })
      if (status) await putImport($, status, server)
    } catch {
      // Not connected right now: the next tick tries again.
    }
  }
  // One list_lead_runs per server answers for all its runs at once; only a run that list leaves
  // out (older than its newest 20) is asked for on its own. Fewer calls keep a busy server quiet.
  const going = Object.values(await read($, runs)).filter(r => !r.isTerminal)
  const byServer = new Map<string, RunView[]>()
  for (const run of going) {
    const server = run.server || configuredServer
    byServer.set(server, [...(byServer.get(server) ?? []), run])
  }
  for (const [server, serverRuns] of byServer) {
    const listed = new Set<string>()
    const answered = new Set<string>()
    try {
      const answer = await call($, server, 'list_lead_runs', {})
      for (const one of Array.isArray(answer?.runs) ? answer.runs : []) {
        if (typeof one !== 'object' || one === null) continue
        const row = one as Record<string, unknown>
        const id = String(row.id ?? '')
        if (!serverRuns.some(r => r.id === id)) continue
        listed.add(id)
        answered.add(id)
        await putRun($, row, server)
      }
    } catch {
      // Not connected right now: the next tick tries again.
    }
    for (const run of serverRuns) {
      if (listed.has(run.id)) continue
      try {
        const status = await call($, server, 'get_lead_run_status', { lead_run_id: run.id })
        if (status && String(status.id ?? status.lead_run_id ?? '') === run.id) {
          answered.add(run.id)
          await putRun($, status, server)
        }
      } catch {
        // Not connected right now: the next tick tries again.
      }
    }
    // A slow server answers through a background task the band never sees: without a check the band
    // would ask forever and never learn the run ended. After MAX_MISSES rounds it stops asking.
    for (const run of serverRuns) {
      const misses = answered.has(run.id) ? 0 : (missedRounds.get(run.id) ?? 0) + 1
      missedRounds.set(run.id, misses)
      if (misses < MAX_MISSES) continue
      await update($, runs, all => {
        const current = all[run.id]
        if (current === undefined || current.isTerminal) return all
        const stale: RunView = {
          ...current,
          status: 'stand_unbekannt',
          isTerminal: true,
          finishedAt: Date.now(),
          reason: 'Server antwortet nicht rechtzeitig – /outreach-status lädt den Stand neu.',
        }
        return { ...all, [run.id]: stale }
      })
    }
  }
  const now = Date.now()
  const stays = (finishedAt: number | null) => finishedAt === null || now - finishedAt < LINGER_MS
  await update($, runs, all => Object.fromEntries(Object.entries(all).filter(([, r]) => stays(r.finishedAt))))
  await update($, imports, all => Object.fromEntries(Object.entries(all).filter(([, j]) => stays(j.finishedAt))))
  const left = [...Object.values(await read($, runs)), ...Object.values(await read($, imports))]
  if (!left.some(r => !r.isTerminal)) {
    poller?.cancel()
    poller = null
    // One last pass once the ended ones are due to leave.
    if (left.length > 0) $.clock.after(LINGER_MS, () => void tick($))
  }
}

// ── workflow phases Claude runs itself ───────────────────────────────────

/** Keeps the app origin a server's links point to, so a local phase links to the right app. */
const learnOrigin = async ($: EngineInterface, server: string, payload: Record<string, unknown> | null) => {
  if (payload === null) return
  const campaign = payload.campaign
  const lead = Array.isArray(payload.leads) ? payload.leads[0] : payload.lead
  const link = [payload.appUrl, isRecord(campaign) ? campaign.appUrl : null, isRecord(lead) ? lead.appUrl : null]
    .find((v): v is string => typeof v === 'string' && /^https?:\/\//.test(v))
  if (link === undefined) return
  const origin = new URL(link).origin
  await update($, origins, all => (all[server] === origin ? all : { ...all, [server]: origin }))
}

const isRecord = (v: unknown): v is Record<string, unknown> => typeof v === 'object' && v !== null && !Array.isArray(v)


const PHASES = ['qualification', 'research', 'email', 'verify'] as const
type Phase = (typeof PHASES)[number]

const localKey = (campaignId: number, phase: Phase) => `${campaignId}:${phase}`

const RESEARCH_FIELDS = new Set(['research', 'status', 'bestEmail', 'decisionMaker', 'contactRecommendation'])

/** Which phase a successful write belongs to: email variables, a verdict, or research. */
const phaseOfWrite = (name: string | null, input: Record<string, unknown>): Phase | null => {
  if (name === 'save_lead_variables') return 'email'
  if (name === 'approve_lead_variables' || name === 'reject_lead_variables') return 'verify'
  if (name !== 'write_lead_details' || input.dry_run === true) return null
  const fields = typeof input.fields === 'object' && input.fields !== null ? Object.keys(input.fields) : []
  return fields.some(f => f.startsWith('qualification')) ? 'qualification' : 'research'
}

/** Done once every lead of the phase is written or has left the chain. */
const withLead = (local: LocalRun, leadId: number, how: 'done' | 'skipped'): LocalRun => {
  const doneLeadIds = how === 'done' ? [...local.doneLeadIds, leadId] : local.doneLeadIds
  const skippedLeadIds = how === 'skipped' ? [...local.skippedLeadIds, leadId] : local.skippedLeadIds
  const isTerminal = doneLeadIds.length + skippedLeadIds.length >= local.total
  return { ...local, doneLeadIds, skippedLeadIds, isTerminal, finishedAt: isTerminal ? Date.now() : null }
}

/** The lead a write answers with says the research found no address to send to (MCP 3.0.0 and later). */
const leftWithoutAddress = (answer: Record<string, unknown> | null): boolean => {
  const lead = answer !== null && typeof answer.lead === 'object' && answer.lead !== null
    ? (answer.lead as Record<string, unknown>)
    : answer
  return lead?.contactEmailState === 'not_found'
}

/**
 * Counts one lead as done for its phase. A lead judged not qualified also leaves the research and
 * email phases of its campaign still going: they will never write it, and must not wait for it. So
 * does a lead imported without an address whose research found none: it gets no mail.
 */
const countWrite = async (
  $: EngineInterface,
  phase: Phase,
  input: Record<string, unknown>,
  server: string,
  answer: Record<string, unknown> | null = null,
) => {
  const campaignId = Number(input.campaign_id)
  const leadId = Number(input.lead_id)
  if (!Number.isFinite(campaignId) || !Number.isFinite(leadId)) return
  const fields = typeof input.fields === 'object' && input.fields !== null ? (input.fields as Record<string, unknown>) : {}
  const leaves = phase === 'qualification' && fields.qualificationFitLevel === 'not_qualified'
  // A combined write (verdict plus research in one call) also completes the research phase.
  const carriesResearch = phase === 'research' || Object.keys(fields).some(f => RESEARCH_FIELDS.has(f))
  const noAddress = carriesResearch && leftWithoutAddress(answer)
  const ended: LocalRun[] = []
  await update($, locals, all => {
    const next = { ...all }
    const touch = (key: string, how: 'done' | 'skipped') => {
      const local = next[key]
      if (local === undefined || local.isTerminal) return
      if (local.doneLeadIds.includes(leadId) || local.skippedLeadIds.includes(leadId)) return
      const changed = withLead({ ...local, server: local.server || server }, leadId, how)
      if (changed.isTerminal) ended.push(changed)
      next[key] = changed
    }
    touch(localKey(campaignId, phase), 'done')
    if (phase === 'qualification' && carriesResearch && !leaves) touch(localKey(campaignId, 'research'), 'done')
    // Mail written without a research write: the lead's research already existed (it holds across campaigns).
    if (phase === 'email') touch(localKey(campaignId, 'research'), 'done')
    if (leaves) {
      touch(localKey(campaignId, 'research'), 'skipped')
      touch(localKey(campaignId, 'email'), 'skipped')
    }
    if (noAddress) touch(localKey(campaignId, 'email'), 'skipped')
    return next
  })
  for (const local of ended) await endLocal($, local)
}

const endLocal = async ($: EngineInterface, local: LocalRun) => {
  const skipped = local.skippedLeadIds.length
  $.ui.toast(
    `Outreach: ${STAGE_LABEL[local.phase] ?? local.phase} fertig · ${local.doneLeadIds.length}/${local.total} Leads` +
      (skipped > 0 ? `, ${skipped} aussortiert` : ''),
  )
  $.clock.after(LINGER_MS, () =>
    void update($, locals, all => {
      const now = Date.now()
      return Object.fromEntries(Object.entries(all).filter(([, l]) => l.finishedAt === null || now - l.finishedAt < LINGER_MS))
    }),
  )
}

type ProgressInput = {
  campaign_id?: unknown
  phase?: unknown
  total?: unknown
  action?: unknown
  lead_id?: unknown
  outcome?: unknown
}

const VERDICTS: readonly Verdict[] = ['freigeben', 'ablehnen', 'hinweis']

/** A verify agent's verdict for one lead: counts the lead as checked and keeps the outcome for the row. */
const recordVerdict = async ($: EngineInterface, input: ProgressInput): Promise<string> => {
  const campaignId = Number(input.campaign_id)
  const leadId = Number(input.lead_id)
  const outcome = VERDICTS.find(v => v === input.outcome)
  if (!Number.isFinite(campaignId) || !Number.isFinite(leadId) || outcome === undefined) {
    return 'campaign_id, lead_id und outcome (freigeben|ablehnen|hinweis) angeben.'
  }
  const key = localKey(campaignId, 'verify')
  let ended: LocalRun | null = null
  await update($, locals, all => {
    const local = all[key]
    if (local === undefined || local.isTerminal) return all
    const verdicts = { ...(local.verdicts ?? {}), [String(leadId)]: outcome }
    const counted = local.doneLeadIds.includes(leadId) ? { ...local, verdicts } : withLead({ ...local, verdicts }, leadId, 'done')
    if (counted.isTerminal) ended = counted
    return { ...all, [key]: counted }
  })
  if (ended !== null) await endLocal($, ended)
  return `Urteil gezählt: Lead ${leadId} ${outcome}.`
}

/** What the workflow skills call: a phase begins with its lead count, or ends. */
const reportProgress = async ($: EngineInterface, input: ProgressInput): Promise<string> => {
  if (input.action === 'verdict') return recordVerdict($, input)
  const campaignId = Number(input.campaign_id)
  const phase = PHASES.find(p => p === input.phase)
  if (!Number.isFinite(campaignId) || phase === undefined) return 'campaign_id und phase (qualification|research|email|verify) angeben.'
  const key = localKey(campaignId, phase)
  if (input.action === 'end') {
    const local = (await read($, locals))[key]
    if (local === undefined || local.isTerminal) return 'Keine laufende Phase dazu.'
    const ended = { ...local, isTerminal: true, finishedAt: Date.now() }
    // An end before every lead is through: what remains was neither done nor skipped.
    await update($, locals, all => ({ ...all, [key]: ended }))
    await endLocal($, ended)
    return `Phase beendet: ${ended.doneLeadIds.length}/${ended.total} Leads.`
  }
  // A phase already going keeps its count: a skill that starts it again for its next batch must not reset it.
  const going = (await read($, locals))[key]
  if (going !== undefined && !going.isTerminal) {
    return `Phase läuft bereits: ${STAGE_LABEL[phase]} · ${going.doneLeadIds.length}/${going.total} Leads.`
  }
  const total = Math.max(1, Math.floor(Number(input.total)) || 1)
  const local: LocalRun = {
    id: key,
    campaignId,
    phase,
    total,
    doneLeadIds: [],
    skippedLeadIds: [],
    isTerminal: false,
    finishedAt: null,
    server: '',
    ...(await usageNow($).then(u => ({ weekStartPercent: u.week, sessionStartPercent: u.session }))),
  }
  await update($, locals, all => ({ ...all, [key]: local }))
  spin($)
  return `Fortschritt läuft im Band: ${STAGE_LABEL[phase]} · 0/${total} Leads. Gezählt wird jeder erfolgreiche Schreibaufruf.`
}

/** The runs still going from a list_lead_runs answer join the band; ended ones are history and stay out. */
const putActiveRuns = async ($: EngineInterface, payload: Record<string, unknown>, server: string): Promise<number> => {
  const listed = Array.isArray(payload.runs) ? payload.runs : []
  let active = 0
  for (const run of listed) {
    if (typeof run !== 'object' || run === null) continue
    const one = run as Record<string, unknown>
    if (one.is_terminal === true) continue
    await putRun($, one, server)
    active += 1
  }
  if (active > 0) watch($)
  return active
}

const SPIN = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
const SPIN_MS = 250

/** Turns the band's spinner while anything runs, and stops itself once nothing does. */
const spin = ($: EngineInterface) => {
  if (spinner !== null) return
  spinner = $.clock.every(SPIN_MS, () =>
    void (async () => {
      const going = (await isGoing($)) || Object.values(await read($, locals)).some(l => !l.isTerminal)
      if (!going) {
        spinner?.cancel()
        spinner = null
        return
      }
      await update($, frame, n => (n + 1) % SPIN.length)
    })(),
  )
}

const watch = ($: EngineInterface) => {
  if (poller === null) poller = $.clock.every(POLL_MS, () => void tick($))
  spin($)
}

const importHref = (job: ImportView) =>
  job.appUrl ?? appLink(base, job.campaignId ? `/campaigns/${job.campaignId}/leads` : '/jobs')

/**
 * In the chat an import is one line, several started together one line between
 * them; how it goes lives in the band. A status check that finds it ended
 * says what it came to.
 */
const importLine = (el: El, jobs: ImportView[]) => {
  const { Box, Text, Link } = el
  const first = jobs[0]
  if (first === undefined) return null
  const leads = jobs.reduce((sum, j) => sum + j.received, 0)
  const sameCampaign = jobs.every(j => j.campaignId === first.campaignId)
  const href = sameCampaign ? importHref(first) : appLink(base, '/jobs')
  if (jobs.length === 1 && first.isTerminal) {
    const color = first.status === 'completed' ? BRAND.done : BRAND.error
    return (
      <Box gap={1}>
        <Text color={color}>■</Text>
        <Text>{`Import · ${importOutcome(first)}`}</Text>
        <Link href={href} label="In der App öffnen ↗" />
      </Box>
    )
  }
  const what = jobs.length === 1 ? 'Import' : `${jobs.length} Importe`
  const state = jobs.length === 1 && first.status === 'processing' ? 'läuft' : 'gestartet'

  return (
    <Box gap={1}>
      <Text color={BRAND.accent}>▶</Text>
      <Text>{`${what} ${state} · ${leads} Leads`}</Text>
      <Text dimColor>· Fortschritt über dem Prompt</Text>
      <Link href={href} label="In der App öffnen ↗" />
    </Box>
  )
}

/** The card for one outreach call, or null when it is not ours or carries nothing to draw. */
const cardFor = (el: El, name: string | null, output: unknown, key: string) => {
  if (name === null) return null
  const payload = payloadOf(output)
  if (payload === null) return null
  const { Box } = el
  let card = null
  if (name === 'list_leads' || name === 'search_leads' || name === 'get_lead_data') {
    const list = leadsFrom(payload)
    card = list && list.leads.length > 0 ? leadPreview(el, list) : null
  } else if (name === 'start_lead_run') {
    const run = runFrom(payload)
    card = run ? startLine(el, run) : null
  } else if (name === 'import_leads' || name === 'get_job_status') {
    const job = importFrom(payload)
    card = job ? importLine(el, [job]) : null
  }
  return card === null ? null : <Box key={`outreach-${key}`}>{card}</Box>
}

/** The progress tool skills call in manual mode; may fail where a server already carries this plugin's name. */
const registerProgressTool = async ($: EngineInterface) => {
  await $.tool.register({
    name: 'outreach_progress',
    description:
      'Zeigt den Fortschritt eines Abo-Laufs (Leads, die du selbst mit Subagents bearbeitest: outreach-abo-lauf, outreach-pipeline --abo, ' +
      'outreach-qualify, outreach-research, outreach-generate) als eine Zeile im Outreach-Band über dem Prompt. Zu Beginn jeder Phase ' +
      'einmal mit action=start, campaign_id, phase (qualification|research|email|verify) und total (Anzahl Leads der Phase) aufrufen. ' +
      'Gezählt wird danach automatisch: jeder erfolgreiche write_lead_details- bzw. save_lead_variables-Aufruf für einen ' +
      'Lead dieser Kampagne zählt als erledigt, in der Phase verify jedes approve/reject. Ein Prüf-Agent meldet sein Urteil ' +
      'mit action=verdict, campaign_id, lead_id und outcome (freigeben|ablehnen|hinweis), auch wenn er nichts schreibt. ' +
      'action=end schließt die Phase vorzeitig ab. Nicht für Server-Läufe (start_lead_run).',
    inputSchema: {
      type: 'object',
      properties: {
        action: { type: 'string', enum: ['start', 'end', 'verdict'] },
        campaign_id: { type: 'integer' },
        phase: { type: 'string', enum: ['qualification', 'research', 'email', 'verify'] },
        total: { type: 'integer', minimum: 1 },
        lead_id: { type: 'integer' },
        outcome: { type: 'string', enum: ['freigeben', 'ablehnen', 'hinweis'] },
      },
      required: ['campaign_id'],
    },
  })
}

/** /outreach-status (old name /outreach-runs): every run still going appears in the band; „zu“ folds it, „auf“ opens it. */
const statusCommand = async ($: EngineInterface, e: { args?: string }) => {
  const arg = (e.args ?? '').trim().toLowerCase()
  if (arg === 'zu' || arg === 'ein' || arg === 'einklappen') {
    await update($, folded, () => true)
    return { text: 'Outreach-Band eingeklappt – `/outreach-status auf` klappt es wieder auf.' }
  }
  await update($, folded, () => false)
  let active = 0
  let reached = 0
  for (const server of await akquiseServers($)) {
    try {
      const listed = await call($, server, 'list_lead_runs', { active_only: true })
      reached += 1
      if (listed !== null) active += await putActiveRuns($, listed, server)
    } catch {
      // Not connected: the others may still answer.
    }
  }
  if (reached === 0) return { text: 'Der Outreach-MCP ist nicht erreichbar – ist er verbunden?' }
  return { text: active === 0 ? 'Gerade läuft kein Lead-Run.' : `${active} laufende(r) Lead-Run(s) – Fortschritt über dem Prompt.` }
}

export const register: Register = (on, options) => {
  configuredServer = String(options.mcpServer ?? 'akquise').replace(/[^A-Za-z0-9_-]/g, '_')
  knownServers = new Map()
  poller = null
  spinner = null
  missedRounds.clear()
  base = String(options.appUrl ?? 'https://outreach.akquise.de')

  // A standalone tool row: our card in place of the engine's result block.
  on('ui.render', { component: 'ToolResult' }, async ($, e, next) => {
    if (e.props.isErrored) return next(e)
    const card = cardFor($.ui.resolve(e), (await recognize($, e.props.tool))?.name ?? null, e.props.output, e.props.tool_use_id)
    return card ?? next(e)
  })

  // Lookups like list_leads are folded into one group line ("Called akquise …"):
  // the engine's line stays, our cards follow beneath it.
  on('ui.render', { component: 'ToolGroup' }, async ($, e, next) => {
    const el = $.ui.resolve(e)
    const { Box } = el
    const cards = []
    // Imports started in one go become one line, after the other cards.
    const started: ImportView[] = []
    for (const [i, c] of e.props.calls.entries()) {
      if (c.isRunning || c.isErrored || c.isInterrupted) continue
      const name = (await recognize($, c.tool))?.name ?? null
      const payload = name === 'import_leads' ? payloadOf(c.output) : null
      const job = payload === null ? null : importFrom(payload)
      if (job !== null) {
        started.push(job)
        continue
      }
      const card = cardFor(el, name, c.output, c.tool_use_id ?? `call-${i}`)
      if (card !== null) cards.push(card)
    }
    const startedLine = started.length > 0 ? importLine(el, started) : null
    if (startedLine !== null) cards.push(<Box key="outreach-imports">{startedLine}</Box>)
    if (cards.length === 0) return next(e)
    const line = await next(e)

    return (
      <Box flexDirection="column">
        {line}
        {cards}
      </Box>
    )
  })

  // After a reload the timer is gone but the runs are kept: pick up the ones still going.
  // Each part stands alone: one that fails (an MCP server already named like
  // this plugin, an older engine) must not take the others down with it.
  on('session.start', async ($, e, next) => {
    try {
      await registerProgressTool($)
    } catch {
      // The band and /outreach-status work without the progress tool.
    }
    try {
      await $.command.register({
        name: 'outreach-status',
        description: 'Was gerade läuft (Server-Läufe, Abo-Läufe, Imports) über dem Prompt anzeigen; „zu“ klappt das Band auf eine Zeile ein, „auf“ wieder auf',
      })
      // The former name keeps working for habits and older notes.
      await $.command.register({ name: 'outreach-runs', description: 'Alter Name von /outreach-status' })
    } catch {
      // Without the command, runs still join the band when Claude checks them.
    }
    try {
      if (await isGoing($)) watch($)
    } catch {
      // Nothing to resume.
    }
    return next(e)
  })


  // One command, no wording needed: every run still going appears in the band.
  // „zu“ shrinks the band to one line, „auf“ (or the bare command) opens it again.
  on('command.run', { command: 'outreach-status' }, statusCommand)
  on('command.run', { command: 'outreach-runs' }, statusCommand)

  on('tool.call', { tool: 'mcp__outreach__outreach_progress' }, async ($, e) => ({
    result: await reportProgress($, e as unknown as ProgressInput),
  }))

  // A run Claude starts, checks or lists as running joins the band, and the band keeps it current.
  on('tool.call', async ($, e, next) => {
    const ran = await next(e)
    if (ran.deny !== undefined || ran.isError === true) return ran
    const recognized = await recognize($, e.tool)
    if (recognized === null) return ran
    const { name, server } = recognized
    await learnOrigin($, server, payloadOf(ran.result))
    const written = phaseOfWrite(name, e as unknown as Record<string, unknown>)
    if (written !== null) {
      await countWrite($, written, e as unknown as Record<string, unknown>, server, payloadOf(ran.result))
      return ran
    }
    if (name === 'import_leads' || name === 'get_job_status') {
      const payload = payloadOf(ran.result)
      if (payload !== null && (await putImport($, payload, server))) watch($)
      return ran
    }
    if (name === 'list_lead_runs') {
      const listed = payloadOf(ran.result)
      if (listed !== null) await putActiveRuns($, listed, server)
      return ran
    }
    const isRun = name === 'start_lead_run' || name === 'get_lead_run_status' || name === 'cancel_lead_run'
    if (!isRun) return ran
    const payload = payloadOf(ran.result)
    if (payload !== null) {
      await putRun($, payload, server)
      watch($)
    }
    return ran
  })

  on('ui.render', { component: 'AbovePrompt' }, async ($, e, next) => {
    const shown = bandRuns(Object.values(await read($, runs)))
    const jobs = bandImports(Object.values(await read($, imports)))
    const phases = bandPhases(Object.values(await read($, locals)))
    if (e.props.hasSurvey || shown.length + jobs.length + phases.length === 0) return next(e)
    if (await read($, folded)) return foldedBand($.ui.resolve(e), shown, jobs, phases)
    const usage = phases.length > 0 ? await usageNow($) : { session: null, week: null }
    return band($.ui.resolve(e), shown, jobs, phases, await read($, frame), await read($, origins), usage)
  })
}
