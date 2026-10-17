import { describe, expect, mock, test } from 'claude-code/testing'
import type { Engine } from 'claude-code/testing'
import type { On, ToolGroupCall } from 'claude-code'

/** What the engine would draw itself: a marker the tests can tell apart from the mod's own tree. */
const engineDraws = (on: On) =>
  on('ui.render', () => ({ type: 'Text', props: {}, children: ['engine'] }))

const LIST_LEADS = {
  campaign: { id: 12, name: 'Zahnärzte München' },
  total: 3,
  offset: 0,
  remaining: 2,
  leads: [
    { id: 7, email: 'a@huber.de', company: 'Dr. Huber Zahnmedizin', city: 'München', score: 86, contactStatus: 'not_contacted', qualification: { fitLevel: 'qualified' } },
  ],
}

const RUN_STATUS = {
  id: 'run-1',
  campaignId: 12,
  status: 'running',
  stages: ['qualification', 'research'],
  leadTotal: 150,
  budgetUsd: 5,
  spentUsd: 0.12,
  stageProgress: [
    { stage: 'qualification', pending: 3, running: 2, completed: 40, failed: 1, noResult: 0, cancelled: 0, total: 46 },
  ],
  is_terminal: false,
}

const IMPORT_QUEUED = { status: 'success', job_id: 'job-1', received: 500, queued: true, campaign_id: 12, list_id: null }

const toolRow = (tool: string, payload: unknown) => ({
  plugin: 'outreach',
  component: 'ToolResult' as const,
  requestId: 'toolu_1',
  props: {
    tool_use_id: 'toolu_1',
    tool,
    isErrored: false,
    output: [{ type: 'text', text: JSON.stringify(payload) }],
  },
})

const SURFACES = ['terminal', 'desktop', 'vscode', 'mobile'] as const

describe('lead preview', () => {
  test('list_leads draws the leads with links into the campaign, on every surface', async $ => {
    for (const surface of SURFACES) {
      const ui = await $.ui.mount({ ...toolRow('mcp__akquise__list_leads', LIST_LEADS), surface })
      expect(await ui.find({ text: /Dr\. Huber Zahnmedizin/ })).toBeDefined()
      expect(await ui.find({ text: /3 Leads/ })).toBeDefined()
      const hrefs = (await ui.findAll({ type: 'Link' })).map(l => l.props.href)
      expect(hrefs).toContain('https://outreach.akquise.de/campaigns/12/leads/7')
      expect(hrefs).toContain('https://outreach.akquise.de/campaigns/12/leads')
      await ui.unmount()
    }
  })

  test('a lead without an address (MCP 3.0.0) draws with its website and the address research found', async $ => {
    const withoutEmail = {
      ...LIST_LEADS,
      leads: [
        { id: 8, email: null, contactEmailState: 'searching', company: '', website: 'https://zahnarzt-berg.de', city: 'München', score: null, contactStatus: 'not_contacted', qualification: null },
        { id: 9, email: 'praxis@mueller.de', contactEmailState: 'present', company: 'Praxis Müller', city: 'München', score: 70, contactStatus: 'not_contacted', qualification: null },
      ],
    }
    const ui = await $.ui.mount({ ...toolRow('mcp__akquise__list_leads', withoutEmail), surface: 'terminal' })
    expect(await ui.find({ text: /zahnarzt-berg\.de/ })).toBeDefined()
    expect(await ui.find({ text: /Praxis Müller/ })).toBeDefined()
    expect(await ui.find({ text: /null/ })).toBeUndefined()
    await ui.unmount()
  })

  test('a list-mode answer (MCP 2.1.0) draws like the queue', async $ => {
    const listMode = {
      ...LIST_LEADS,
      mode: 'list',
      matched_total: 40,
      lead_ids: [7, 8, 9],
      lead_ids_truncated: false,
      applied_filters: { run_stages: ['qualification', 'research', 'email'], sort_by: 'email', sort_direction: 'asc', take: 3 },
    }
    const ui = await $.ui.mount({ ...toolRow('mcp__akquise__list_leads', listMode), surface: 'terminal' })
    expect(await ui.find({ text: /Dr\. Huber Zahnmedizin/ })).toBeDefined()
    expect(await ui.find({ text: /3 Leads/ })).toBeDefined()
    await ui.unmount()
  })

  test('every fit level the server sends gets a German label', async $ => {
    const leads = ['highly_qualified', 'mid_qualified', 'not_qualified', null].map((fitLevel, i) => ({
      id: i + 1, company: `Firma ${i + 1}`, city: 'Freiburg', score: null, contactStatus: 'not_contacted', qualification: { fitLevel },
    }))
    const ui = await $.ui.mount({ ...toolRow('mcp__akquise__list_leads', { ...LIST_LEADS, total: 4, leads }), surface: 'terminal' })
    for (const label of ['sehr passend', 'bedingt', 'passt nicht', 'nicht bewertet']) {
      expect(await ui.find({ text: label })).toBeDefined()
    }
    expect(await ui.find({ text: 'not_contacted' })).toBeUndefined()
    await ui.unmount()
  })

  test('another server’s tools are left to the engine', async ($, on) => {
    engineDraws(on)
    const ui = await $.ui.mount({ ...toolRow('mcp__other__list_leads', LIST_LEADS), surface: 'terminal' })
    expect(await ui.find({ text: /Dr\. Huber/ })).toBeUndefined()
    await ui.unmount()
  })
})

const BAND = {
  plugin: 'outreach',
  component: 'AbovePrompt' as const,
  props: { hasSurvey: false, isWorking: false, maxRows: 12, bodyColumns: 100, scroll: { offset: 0, bodyRows: 12 }, view: {} },
}

/** Claude calls a ListM8 tool; the hook beneath answers it as the server would. */
const toolCall = ($: Engine, tool: string, input: Record<string, unknown>) =>
  $.tool.call({ tool, ...input } as unknown as Parameters<typeof $.tool.call>[0])

describe('which MCP server is ours', () => {
  const offers = (server: string, names: string[]) =>
    names.map(n => ({ name: `mcp__${server}__${n}`, description: '', mcp: true }))

  test('a server is recognised by what it offers, whatever its name', async ($, on) => {
    engineDraws(on)
    on('tool.list', () => ({
      value: [
        ...offers('Outreach_Akquise', ['list_leads', 'start_lead_run', 'get_lead_run_status', 'get_lead_data']),
        ...offers('crm', ['list_leads']),
      ],
    }))
    const ours = await $.ui.mount({ ...toolRow('mcp__Outreach_Akquise__list_leads', LIST_LEADS), surface: 'terminal' })
    expect(await ours.find({ text: /Dr\. Huber Zahnmedizin/ })).toBeDefined()
    await ours.unmount()

    const foreign = await $.ui.mount({ ...toolRow('mcp__crm__list_leads', LIST_LEADS), surface: 'terminal' })
    expect(await foreign.find({ text: /Dr\. Huber/ })).toBeUndefined()
    await foreign.unmount()
  })

  test('a link the server sends wins over the configured app address', async $ => {
    const withLinks = {
      ...LIST_LEADS,
      campaign: { ...LIST_LEADS.campaign, appUrl: 'https://kunde.example/campaigns/12/leads' },
      leads: [{ ...LIST_LEADS.leads[0], appUrl: 'https://kunde.example/campaigns/12/leads/7' }],
    }
    const ui = await $.ui.mount({ ...toolRow('mcp__akquise__list_leads', withLinks), surface: 'terminal' })
    const hrefs = (await ui.findAll({ type: 'Link' })).map(l => l.props.href)
    expect(hrefs).toContain('https://kunde.example/campaigns/12/leads/7')
    expect(hrefs).toContain('https://kunde.example/campaigns/12/leads')
    expect(hrefs.some(h => String(h).includes('outreach.akquise.de'))).toBe(false)
    await ui.unmount()
  })

  test('the band asks the server a run came from', async ($, on) => {
    engineDraws(on)
    const clock = mock.clock(on)
    const asked: string[] = []
    on('tool.list', () => ({ value: offers('akquise', ['list_leads', 'start_lead_run', 'get_lead_run_status']) }))
    on('tool.call', () => ({ result: RUN_STATUS }))
    on('mcp.call', ($, e) => {
      asked.push(String((e as { server: string }).server))
      const body = (e as { tool: string }).tool === 'list_lead_runs' ? { runs: [RUN_STATUS], count: 1 } : RUN_STATUS
      return { value: { content: [{ type: 'text', text: JSON.stringify(body) }], isError: false } }
    })
    await toolCall($, 'mcp__akquise__get_lead_run_status', { lead_run_id: 'run-1' })
    await clock.advance(20_000)
    expect(asked).toEqual(['akquise'])
  })
})

describe('run status', () => {
  test('a started run is one line in the chat', async $ => {
    const started = { status: 'success', lead_run_id: 'run-1', campaign_id: 12, run_status: 'preparing', stages: ['qualification'], lead_total: 10, budget_usd: 1, queued: true }
    const ui = await $.ui.mount({ ...toolRow('mcp__akquise__start_lead_run', started), surface: 'terminal' })
    expect(await ui.find({ text: /Lead-Run gestartet · 10 Leads · Qualifizierung · Budget 1.00 \$/ })).toBeDefined()
    await ui.unmount()
  })

  test('a run just started counts no lead as through, not all of them', async ($, on) => {
    engineDraws(on)
    mock.clock(on)
    const started = { status: 'success', lead_run_id: 'run-new', campaign_id: 12, run_status: 'preparing', stages: ['qualification', 'research', 'email'], lead_total: 10, budget_usd: 2, queued: true }
    on('tool.call', () => ({ result: started }))
    await toolCall($, 'mcp__akquise__start_lead_run', { campaign_id: 12, stages: ['qualification'] })
    const band = await $.ui.mount({ ...BAND, surface: 'terminal' })
    expect(await band.find({ text: '0/10' })).toBeDefined()
    expect(await band.find({ text: '10/10' })).toBeUndefined()
    await band.unmount()
  })

  test('a checked run shows in the band, not as a card in the chat', async ($, on) => {
    engineDraws(on)
    mock.clock(on)
    on('tool.call', () => ({ result: RUN_STATUS }))
    await toolCall($, 'mcp__akquise__get_lead_run_status', { lead_run_id: 'run-1' })

    const band = await $.ui.mount({ ...BAND, surface: 'terminal' })
    expect(await band.find({ text: 'Outreach · Lead-Run' })).toBeDefined()
    expect(await band.find({ text: '40/46' })).toBeDefined()
    expect(await band.find({ text: '2 laufen · 3 warten' })).toBeDefined()
    expect(await band.find({ text: '⠋' })).toBeDefined()
    expect(await band.find({ text: '· 1 Fehler' })).toBeDefined()
    await band.unmount()

    const row = await $.ui.mount({ ...toolRow('mcp__akquise__get_lead_run_status', RUN_STATUS), surface: 'terminal' })
    expect(await row.find({ text: 'engine' })).toBeDefined()
    await row.unmount()
  })

  test('the band asks every 20 s until the run has ended, and says why it stopped', async ($, on) => {
    engineDraws(on)
    const clock = mock.clock(on)
    const stopped = { ...RUN_STATUS, status: 'provider_exhausted', is_terminal: true, statusReason: 'OpenRouter rejected the API key' }
    let asked = 0
    on('tool.call', () => ({ result: RUN_STATUS }))
    on('mcp.call', (_$, e) => {
      asked += 1
      const body = (e as { tool: string }).tool === 'list_lead_runs' ? { runs: [stopped], count: 1 } : stopped
      return { value: { content: [{ type: 'text', text: JSON.stringify(body) }], isError: false } }
    })
    await toolCall($, 'mcp__akquise__get_lead_run_status', { lead_run_id: 'run-1' })

    await clock.advance(20_000)
    expect(asked).toBe(1)
    const band = await $.ui.mount({ ...BAND, surface: 'terminal' })
    expect(await band.find({ text: '· KI-Anbieter nicht verfügbar' })).toBeDefined()
    expect(await band.find({ text: /OpenRouter rejected the API key/ })).toBeDefined()

    await clock.advance(30_000)
    expect(asked).toBe(1)
    await band.unmount()
  })

  test('a server that never answers usably: after three rounds the band stops asking', async ($, on) => {
    engineDraws(on)
    const clock = mock.clock(on)
    let asked = 0
    on('tool.call', () => ({ result: RUN_STATUS }))
    on('mcp.call', () => {
      asked += 1
      return { value: { content: [{ type: 'text', text: 'Task started in the background.' }], isError: false } }
    })
    await toolCall($, 'mcp__akquise__get_lead_run_status', { lead_run_id: 'run-1' })
    for (let i = 0; i < 3; i++) await clock.advance(20_000)
    const after = asked
    await clock.advance(60_000)
    expect(asked).toBeLessThanOrEqual(after + 2)
    const band = await $.ui.mount({ ...BAND, surface: 'terminal' })
    expect(await band.find({ text: /Stand unbekannt/ })).toBeDefined()
    await band.unmount()
  })

  test('leads run their own chains: the band counts leads through, not a stage', async ($, on) => {
    engineDraws(on)
    mock.clock(on)
    // Lead 1 is writing its mail, lead 2 was judged not qualified, lead 3 is still being researched.
    const sideBySide = {
      ...RUN_STATUS,
      stages: ['qualification', 'research', 'email'],
      leadTotal: 3,
      stageProgress: [
        { stage: 'qualification', pending: 0, running: 0, completed: 3, failed: 0, noResult: 0, cancelled: 0, total: 3 },
        { stage: 'research', pending: 0, running: 1, completed: 1, failed: 0, noResult: 0, cancelled: 0, total: 2 },
        { stage: 'email', pending: 0, running: 1, completed: 0, failed: 0, noResult: 0, cancelled: 0, total: 1 },
      ],
    }
    on('tool.call', () => ({ result: sideBySide }))
    await toolCall($, 'mcp__akquise__get_lead_run_status', { lead_run_id: 'run-1' })
    const band = await $.ui.mount({ ...BAND, surface: 'terminal' })
    expect(await band.find({ text: '3/3' })).toBeDefined()
    expect(await band.find({ text: '2 passen · 1 raus' })).toBeDefined()
    expect(await band.find({ text: '1/2' })).toBeDefined()
    expect(await band.find({ text: '0/1' })).toBeDefined()
    expect(await band.find({ text: '✓' })).toBeDefined()
    await band.unmount()
  })

  test('several runs share one frame, a row each', async ($, on) => {
    engineDraws(on)
    mock.clock(on)
    let n = 0
    on('tool.call', () => {
      n += 1
      return { result: { ...RUN_STATUS, id: `run-${n}`, leadTotal: n === 1 ? 3 : 13 } }
    })
    await toolCall($, 'mcp__akquise__get_lead_run_status', { lead_run_id: 'run-1' })
    await toolCall($, 'mcp__akquise__get_lead_run_status', { lead_run_id: 'run-2' })
    const band = await $.ui.mount({ ...BAND, surface: 'terminal' })
    expect(await band.find({ text: 'Outreach · 2 Läufe' })).toBeDefined()
    expect(await band.find({ text: '2 laufen' })).toBeDefined()
    expect(await band.find({ text: '3 Leads' })).toBeDefined()
    expect(await band.find({ text: '13 Leads' })).toBeDefined()
    await band.unmount()
  })

  test('in a shared band each run names only its working stage, with a spinner', async ($, on) => {
    engineDraws(on)
    mock.clock(on)
    const researchOnly = {
      ...RUN_STATUS,
      id: 'run-vg',
      stages: ['research', 'email'],
      leadTotal: 1,
      stageProgress: [{ stage: 'research', pending: 0, running: 1, completed: 0, failed: 0, total: 1 }],
    }
    const full = {
      ...RUN_STATUS,
      id: 'run-ten',
      stages: ['qualification', 'research', 'email'],
      leadTotal: 10,
      stageProgress: [{ stage: 'qualification', pending: 3, running: 7, completed: 0, failed: 0, total: 10 }],
    }
    let n = 0
    on('tool.call', () => ({ result: (n += 1) === 1 ? researchOnly : full }))
    await toolCall($, 'mcp__akquise__get_lead_run_status', { lead_run_id: 'run-vg' })
    await toolCall($, 'mcp__akquise__get_lead_run_status', { lead_run_id: 'run-ten' })

    const band = await $.ui.mount({ ...BAND, surface: 'terminal' })
    expect(await band.find({ text: '· Rech. 0/1' })).toBeDefined()
    expect(await band.find({ text: '· Qual. 0/10' })).toBeDefined()
    expect(await band.find({ text: /Mail/ })).toBeUndefined()
    expect(await band.find({ text: '⠋' })).toBeDefined()
    await band.unmount()
  })

  test('/outreach-status puts every run still going into the band, and only those', async ($, on) => {
    engineDraws(on)
    mock.clock(on)
    const ended = { ...RUN_STATUS, id: 'run-old', status: 'completed', is_terminal: true }
    on('mcp.call', () => ({
      value: { content: [{ type: 'text', text: JSON.stringify({ runs: [RUN_STATUS, ended], count: 2 }) }], isError: false },
    }))
    const res = await $.command.run({ command: 'outreach-status' } as Parameters<typeof $.command.run>[0])
    expect(String((res as { text?: string }).text)).toContain('1 laufende')
    const band = await $.ui.mount({ ...BAND, surface: 'terminal' })
    expect(await band.find({ text: 'Outreach · Lead-Run' })).toBeDefined()
    expect(await band.find({ text: '40/46' })).toBeDefined()
    await band.unmount()
  })

  test('/outreach-status zu folds the band to one line, the old name /outreach-runs auf opens it again', async ($, on) => {
    engineDraws(on)
    mock.clock(on)
    on('mcp.call', () => ({
      value: { content: [{ type: 'text', text: JSON.stringify({ runs: [RUN_STATUS], count: 1 }) }], isError: false },
    }))
    const run = (args: string, command = 'outreach-status') => $.command.run({ command, args } as Parameters<typeof $.command.run>[0])
    await run('')
    const folded = await run('zu')
    expect(String((folded as { text?: string }).text)).toContain('eingeklappt')
    let band = await $.ui.mount({ ...BAND, surface: 'terminal' })
    expect(await band.find({ text: 'Outreach · 1 Lauf · 1 läuft' })).toBeDefined()
    expect(await band.find({ text: '40/46' })).toBeUndefined()
    await band.unmount()

    await run('auf', 'outreach-runs')
    band = await $.ui.mount({ ...BAND, surface: 'terminal' })
    expect(await band.find({ text: '40/46' })).toBeDefined()
    await band.unmount()
  })

  test('asking Claude for the runs fills the band too', async ($, on) => {
    engineDraws(on)
    mock.clock(on)
    on('tool.call', () => ({ result: { runs: [RUN_STATUS], count: 1 } }))
    await toolCall($, 'mcp__akquise__list_lead_runs', { active_only: true })
    const band = await $.ui.mount({ ...BAND, surface: 'terminal' })
    expect(await band.find({ text: '40/46' })).toBeDefined()
    await band.unmount()
  })

  test('the spinner turns while a stage works and stops once the run has ended', async ($, on) => {
    engineDraws(on)
    const clock = mock.clock(on)
    const ended = { ...RUN_STATUS, status: 'completed', is_terminal: true }
    on('tool.call', () => ({ result: RUN_STATUS }))
    on('mcp.call', () => ({ value: { content: [{ type: 'text', text: JSON.stringify(ended) }], isError: false } }))
    await toolCall($, 'mcp__akquise__get_lead_run_status', { lead_run_id: 'run-1' })

    const band = await $.ui.mount({ ...BAND, surface: 'terminal' })
    expect(await band.find({ text: '⠋' })).toBeDefined()
    await clock.advance(250)
    expect(await band.find({ text: '⠙' })).toBeDefined()

    await clock.advance(20_000)
    expect(await band.find({ text: /[⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏]/ })).toBeUndefined()
    await band.unmount()
  })

  test('every run still going is in the band, oldest first, however many', async ($, on) => {
    engineDraws(on)
    mock.clock(on)
    // list_lead_runs answers newest first; six runs started a second apart, none with work done yet.
    const listed = [2240, 2238, 2236, 2237, 2235, 2234].map((campaignId, i) => ({
      ...RUN_STATUS,
      id: `run-${campaignId}`,
      campaignId,
      leadTotal: campaignId,
      createdAt: `2026-10-03T16:39:${String(25 - i).padStart(2, '0')}+00:00`,
      stageProgress: [{ stage: 'qualification', pending: 10, running: 0, completed: 0, failed: 0, total: 10 }],
    }))
    on('tool.call', () => ({ result: { runs: listed, count: 6 } }))
    await toolCall($, 'mcp__akquise__list_lead_runs', { active_only: true })

    const band = await $.ui.mount({ ...BAND, surface: 'terminal' })
    expect(await band.find({ text: 'Outreach · 6 Läufe' })).toBeDefined()
    for (const total of [2234, 2235, 2236, 2237, 2238, 2240]) {
      expect(await band.find({ text: `${total} Leads` })).toBeDefined()
    }
    const order = (await band.findAll({ text: /^\d+ Leads$/ })).map(e => e.text)
    expect(order[0]).toBe('2234 Leads')
    expect(order[order.length - 1]).toBe('2240 Leads')
    await band.unmount()
  })

  test('without runs the band is the engine’s', async ($, on) => {
    engineDraws(on)
    const band = await $.ui.mount({ ...BAND, surface: 'terminal' })
    expect(await band.find({ text: 'engine' })).toBeDefined()
    await band.unmount()
  })
})

describe('local workflow phases', () => {
  const progress = ($: Engine, input: Record<string, unknown>) => toolCall($, 'mcp__outreach__outreach_progress', input)

  test('a phase Claude runs itself counts each lead written, once, and ends at its total', async ($, on) => {
    engineDraws(on)
    mock.clock(on)
    on('tool.call', () => ({ result: { status: 'success' } }))
    await progress($, { action: 'start', campaign_id: 2162, phase: 'research', total: 2 })

    const write = (leadId: number, fields: Record<string, unknown>) =>
      toolCall($, 'mcp__akquise__write_lead_details', { campaign_id: 2162, lead_id: leadId, fields })
    await write(1, { researchText: 'Bericht' })
    await write(1, { researchText: 'Bericht, nachgebessert' })
    await write(3, { qualificationFitLevel: 'qualified' })

    let band = await $.ui.mount({ ...BAND, surface: 'terminal' })
    expect(await band.find({ text: '1 fertig' })).toBeDefined()
    expect(await band.find({ text: '· Rech 1/2 · im Abo' })).toBeDefined()
    await band.unmount()

    await write(2, { researchText: 'Bericht' })
    band = await $.ui.mount({ ...BAND, surface: 'terminal' })
    expect(await band.find({ text: 'fertig' })).toBeDefined()
    expect(await band.find({ text: 'alle beendet' })).toBeDefined()
    await band.unmount()
  })

  test('a lead judged not qualified leaves research and email: they end green with it set aside', async ($, on) => {
    engineDraws(on)
    mock.clock(on)
    on('tool.call', () => ({ result: { status: 'success' } }))
    for (const phase of ['qualification', 'research', 'email']) await progress($, { action: 'start', campaign_id: 2274, phase, total: 2 })
    const write = (tool: string, leadId: number, fields: Record<string, unknown>) =>
      toolCall($, `mcp__akquise__${tool}`, { campaign_id: 2274, lead_id: leadId, fields, variables: '{}' })

    await write('write_lead_details', 1, { qualificationStatus: 'completed', qualificationFitLevel: 'qualified' })
    await write('write_lead_details', 2, { qualificationStatus: 'completed', qualificationFitLevel: 'not_qualified' })
    await write('write_lead_details', 1, { research: 'Bericht', status: 'researched' })
    await write('save_lead_variables', 1, {})

    const band = await $.ui.mount({ ...BAND, surface: 'terminal' })
    expect(await band.find({ text: '1 fertig · 1 aussortiert' })).toBeDefined()
    expect(await band.find({ text: /0 fertig/ })).toBeUndefined()
    expect(await band.find({ text: '· Qual 2/2 · Rech 1/1 · Mail 1/1 · im Abo' })).toBeDefined()
    expect(await band.find({ text: 'alle beendet' })).toBeDefined()
    await band.unmount()
  })

  test('a lead whose research found no address leaves the email phase (MCP 3.0.0)', async ($, on) => {
    engineDraws(on)
    mock.clock(on)
    on('tool.call', (_$, e) => {
      const leadId = (e as unknown as { lead_id: number }).lead_id
      const contactEmailState = leadId === 2 ? 'not_found' : 'present'
      return { result: { status: 'success', lead: { id: leadId, email: null, contactEmailState } } }
    })
    for (const phase of ['research', 'email']) await progress($, { action: 'start', campaign_id: 2280, phase, total: 2 })
    const write = (tool: string, leadId: number, fields: Record<string, unknown>) =>
      toolCall($, `mcp__akquise__${tool}`, { campaign_id: 2280, lead_id: leadId, fields, variables: '{}' })

    await write('write_lead_details', 1, { research: 'Bericht', status: 'researched' })
    await write('write_lead_details', 2, { research: 'Bericht\n\n## Kontakt\nkeine Adresse', status: 'researched' })
    await write('save_lead_variables', 1, {})

    const band = await $.ui.mount({ ...BAND, surface: 'terminal' })
    expect(await band.find({ text: '· Rech 2/2 · Mail 1/1 · im Abo' })).toBeDefined()
    expect(await band.find({ text: 'alle beendet' })).toBeDefined()
    await band.unmount()
  })

  test('a combined verdict and research write counts both phases and, without an address, leaves the email phase', async ($, on) => {
    engineDraws(on)
    mock.clock(on)
    on('tool.call', (_$, e) => {
      const leadId = (e as unknown as { lead_id: number }).lead_id
      const contactEmailState = leadId === 2 ? 'not_found' : 'present'
      return { result: { status: 'success', lead: { id: leadId, email: null, contactEmailState } } }
    })
    for (const phase of ['qualification', 'research', 'email']) await progress($, { action: 'start', campaign_id: 2281, phase, total: 2 })
    const write = (tool: string, leadId: number, fields: Record<string, unknown>) =>
      toolCall($, `mcp__akquise__${tool}`, { campaign_id: 2281, lead_id: leadId, fields, variables: '{}' })

    await write('write_lead_details', 1, { qualificationStatus: 'completed', qualificationFitLevel: 'qualified' })
    await write('write_lead_details', 1, { research: 'Bericht', status: 'researched' })
    await write('save_lead_variables', 1, {})
    await write('write_lead_details', 2, { qualificationStatus: 'completed', qualificationFitLevel: 'qualified', research: 'Bericht\n\n## Kontakt\nkeine Adresse', status: 'researched' })

    const band = await $.ui.mount({ ...BAND, surface: 'terminal' })
    expect(await band.find({ text: '· Qual 2/2 · Rech 2/2 · Mail 1/1 · im Abo' })).toBeDefined()
    expect(await band.find({ text: 'alle beendet' })).toBeDefined()
    await band.unmount()
  })

  test('a local phase links into the app only once its server has named its origin', async ($, on) => {
    engineDraws(on)
    mock.clock(on)
    const listed = { ...LIST_LEADS, campaign: { id: 2274, name: 'T', appUrl: 'https://listm8.test/campaigns/2274/leads' } }
    on('tool.call', (_$, e) => ({ result: String(e.tool).endsWith('list_leads') ? listed : { status: 'success' } }))
    await progress($, { action: 'start', campaign_id: 2274, phase: 'research', total: 3 })
    await toolCall($, 'mcp__akquise__write_lead_details', { campaign_id: 2274, lead_id: 1, fields: { research: 'x' } })
    let band = await $.ui.mount({ ...BAND, surface: 'terminal' })
    expect((await band.findAll({ type: 'Link' })).length).toBe(0)
    await band.unmount()

    await toolCall($, 'mcp__akquise__list_leads', { campaign_id: 2274 })
    band = await $.ui.mount({ ...BAND, surface: 'terminal' })
    const hrefs = (await band.findAll({ type: 'Link' })).map(l => l.props.href)
    expect(hrefs).toContain('https://listm8.test/campaigns/2274/leads')
    await band.unmount()
  })

  test('a lead whose research already existed counts as researched once its mail is written', async ($, on) => {
    engineDraws(on)
    mock.clock(on)
    on('tool.call', () => ({ result: { status: 'success' } }))
    for (const phase of ['qualification', 'research', 'email']) await progress($, { action: 'start', campaign_id: 2261, phase, total: 1 })
    await toolCall($, 'mcp__akquise__write_lead_details', { campaign_id: 2261, lead_id: 5, fields: { qualificationStatus: 'completed', qualificationFitLevel: 'qualified' } })
    await toolCall($, 'mcp__akquise__save_lead_variables', { campaign_id: 2261, lead_id: 5, variables: '{}' })
    const band = await $.ui.mount({ ...BAND, surface: 'terminal' })
    expect(await band.find({ text: '· Qual 1/1 · Rech 1/1 · Mail 1/1 · im Abo' })).toBeDefined()
    expect(await band.find({ text: 'alle beendet' })).toBeDefined()
    await band.unmount()
  })

  test('email variables count for the email phase; a dry run counts nothing', async ($, on) => {
    engineDraws(on)
    mock.clock(on)
    on('tool.call', () => ({ result: { status: 'success' } }))
    await progress($, { action: 'start', campaign_id: 7, phase: 'email', total: 3 })
    await toolCall($, 'mcp__akquise__save_lead_variables', { campaign_id: 7, lead_id: 1, variables: '{}' })
    await toolCall($, 'mcp__akquise__write_lead_details', { campaign_id: 7, lead_id: 2, fields: { researchText: 'x' }, dry_run: true })
    const band = await $.ui.mount({ ...BAND, surface: 'terminal' })
    expect(await band.find({ text: '1 fertig' })).toBeDefined()
    expect(await band.find({ text: '· Mail 1/3 · im Abo' })).toBeDefined()
    await band.unmount()
  })

  test('the tool answers what it shows, and end closes a phase early', async ($, on) => {
    engineDraws(on)
    mock.clock(on)
    const started = await progress($, { action: 'start', campaign_id: 7, phase: 'qualification', total: 20 })
    expect(String(started.result)).toContain('0/20')
    const again = await progress($, { action: 'start', campaign_id: 7, phase: 'qualification', total: 10 })
    expect(String(again.result)).toContain('läuft bereits')
    const ended = await progress($, { action: 'end', campaign_id: 7, phase: 'qualification' })
    expect(String(ended.result)).toContain('0/20')
    const band = await $.ui.mount({ ...BAND, surface: 'terminal' })
    expect(await band.find({ text: 'alle beendet' })).toBeDefined()
    await band.unmount()
  })

  test('a verify phase counts each verdict once and shows the outcomes, though nothing is written', async ($, on) => {
    engineDraws(on)
    mock.clock(on)
    await progress($, { action: 'start', campaign_id: 7, phase: 'verify', total: 3 })
    await progress($, { action: 'verdict', campaign_id: 7, lead_id: 1, outcome: 'freigeben' })
    await progress($, { action: 'verdict', campaign_id: 7, lead_id: 2, outcome: 'hinweis' })
    await progress($, { action: 'verdict', campaign_id: 7, lead_id: 2, outcome: 'hinweis' })
    let band = await $.ui.mount({ ...BAND, surface: 'terminal' })
    expect(await band.find({ text: /2 geprüft · 1 frei · 1 Hinweis/ })).toBeDefined()
    expect(await band.find({ text: /Prüf 2\/3/ })).toBeDefined()
    await band.unmount()
    await progress($, { action: 'verdict', campaign_id: 7, lead_id: 3, outcome: 'ablehnen' })
    band = await $.ui.mount({ ...BAND, surface: 'terminal' })
    expect(await band.find({ text: /3 geprüft · 1 frei · 1 abgelehnt · 1 Hinweis/ })).toBeDefined()
    await band.unmount()
  })
})

describe('imports', () => {
  const jobStatus = (status: string, result: unknown = null) => ({
    job_id: 'job-1',
    appUrl: 'https://outreach.akquise.de/jobs',
    type: 'lead_bulk_import',
    status,
    result,
    error: status === 'failed' ? 'CSV-Zeile 3 ist kaputt' : null,
    execution: { status, progress_percent: 0, progress_message: null },
  })
  const mcpAnswers = (on: On, answers: unknown[]) => {
    const asked: unknown[] = []
    on('mcp.call', (_$, e) => {
      asked.push(e)
      const answer = answers[Math.min(asked.length - 1, answers.length - 1)]
      return { value: { content: [{ type: 'text', text: JSON.stringify(answer) }], isError: false } }
    })
    return asked
  }

  test('a queued import is one line in the chat, without a bar, with the way into the app', async $ => {
    const ui = await $.ui.mount({ ...toolRow('mcp__akquise__import_leads', IMPORT_QUEUED), surface: 'terminal' })
    expect(await ui.find({ text: 'Import gestartet · 500 Leads' })).toBeDefined()
    expect(await ui.find({ text: /░/ })).toBeUndefined()
    expect(await ui.find({ text: /%/ })).toBeUndefined()
    const hrefs = (await ui.findAll({ type: 'Link' })).map(l => l.props.href)
    expect(hrefs).toContain('https://outreach.akquise.de/campaigns/12/leads')
    await ui.unmount()
  })

  test('a started import shows in the band and the band follows it to its result', async ($, on) => {
    engineDraws(on)
    const clock = mock.clock(on)
    const toasts: string[] = []
    on('ui.toast', (_$, e) => {
      toasts.push(e.text)
      return { value: undefined }
    })
    const asked = mcpAnswers(on, [
      jobStatus('processing'),
      jobStatus('completed', { status: 'success', imported: 480, total: 500, duplicates: Array.from({ length: 20 }, (_, i) => ({ row: i })) }),
    ])
    on('tool.call', () => ({ result: IMPORT_QUEUED }))
    await toolCall($, 'mcp__akquise__import_leads', { campaign_id: 12, leads: [] })

    const queued = await $.ui.mount({ ...BAND, surface: 'terminal' })
    expect(await queued.find({ text: 'Outreach · Import' })).toBeDefined()
    expect(await queued.find({ text: '500 Leads' })).toBeDefined()
    expect(await queued.find({ text: 'wartet' })).toBeDefined()
    await queued.unmount()

    await clock.advance(20_000)
    const working = await $.ui.mount({ ...BAND, surface: 'terminal' })
    expect(await working.find({ text: 'läuft' })).toBeDefined()
    await working.unmount()

    await clock.advance(20_000)
    expect(asked.length).toBe(2)
    const done = await $.ui.mount({ ...BAND, surface: 'terminal' })
    expect(await done.find({ text: '480 importiert · 20 Duplikate' })).toBeDefined()
    expect(await done.find({ text: 'alle beendet' })).toBeDefined()
    const hrefs = (await done.findAll({ type: 'Link' })).map(l => l.props.href)
    expect(hrefs).toContain('https://outreach.akquise.de/campaigns/12/leads')
    await done.unmount()
    expect(toasts.some(t => /Import 480 importiert/.test(t))).toBe(true)

    await clock.advance(30_000)
    expect(asked.length).toBe(2)
  })

  test('rows the server refused show next to the imported ones (MCP 3.0.0)', async ($, on) => {
    engineDraws(on)
    const clock = mock.clock(on)
    mcpAnswers(on, [jobStatus('completed', { status: 'success', imported: 470, total: 497, duplicates: [], rejected_count: 3 })])
    on('tool.call', () => ({ result: { ...IMPORT_QUEUED, received: 500, accepted: 497, rejected_total: 3 } }))
    await toolCall($, 'mcp__akquise__import_leads', { campaign_id: 12, leads: [] })
    await clock.advance(20_000)
    const done = await $.ui.mount({ ...BAND, surface: 'terminal' })
    expect(await done.find({ text: '470 importiert · 3 abgelehnt' })).toBeDefined()
    await done.unmount()
  })

  test('a failed import says why, in the band and when Claude checks it', async ($, on) => {
    engineDraws(on)
    const clock = mock.clock(on)
    mcpAnswers(on, [jobStatus('failed')])
    on('tool.call', () => ({ result: IMPORT_QUEUED }))
    await toolCall($, 'mcp__akquise__import_leads', { campaign_id: 12, leads: [] })
    await clock.advance(20_000)

    const band = await $.ui.mount({ ...BAND, surface: 'terminal' })
    expect(await band.find({ text: 'fehlgeschlagen · CSV-Zeile 3 ist kaputt' })).toBeDefined()
    await band.unmount()

    const row = await $.ui.mount({ ...toolRow('mcp__akquise__get_job_status', jobStatus('failed')), surface: 'terminal' })
    expect(await row.find({ text: 'Import · fehlgeschlagen · CSV-Zeile 3 ist kaputt' })).toBeDefined()
    await row.unmount()
  })

  test('get_job_status for a job of another kind is no import', async ($, on) => {
    engineDraws(on)
    const research = { ...jobStatus('processing'), type: 'lead_research' }
    on('tool.call', () => ({ result: research }))
    await toolCall($, 'mcp__akquise__get_job_status', { job_id: 'job-1' })
    const band = await $.ui.mount({ ...BAND, surface: 'terminal' })
    expect(await band.find({ text: 'engine' })).toBeDefined()
    await band.unmount()
    const row = await $.ui.mount({ ...toolRow('mcp__akquise__get_job_status', research), surface: 'terminal' })
    expect(await row.find({ text: 'engine' })).toBeDefined()
    await row.unmount()
  })

  test('imports started in one go are one line between them', async ($, on) => {
    engineDraws(on)
    const calls: ToolGroupCall[] = [10, 20, 30].map((received, i) => ({
      tool_use_id: `toolu_import_${i}`,
      tool: 'mcp__akquise__import_leads',
      input: {},
      isRunning: false,
      isErrored: false,
      isInterrupted: false,
      output: [{ type: 'text', text: JSON.stringify({ ...IMPORT_QUEUED, job_id: `job-${i}`, received }) }],
    }))
    const ui = await $.ui.mount({
      plugin: 'outreach',
      component: 'ToolGroup' as const,
      requestId: 'group-imports',
      props: { calls, isActive: false, isExpanded: false },
      surface: 'terminal',
    })
    expect(await ui.find({ text: 'engine' })).toBeDefined()
    expect(await ui.find({ text: '3 Importe gestartet · 60 Leads' })).toBeDefined()
    expect((await ui.findAll({ type: 'Link' })).length).toBe(1)
    await ui.unmount()
  })
})

describe('folded lookups', () => {
  const group = (calls: ToolGroupCall[]) => ({
    plugin: 'outreach',
    component: 'ToolGroup' as const,
    requestId: 'group-1',
    props: { calls, isActive: false, isExpanded: false },
  })
  const call = (tool: string, payload: unknown, isRunning = false): ToolGroupCall => ({
    tool_use_id: `toolu_${tool}`,
    tool,
    input: {},
    isRunning,
    isErrored: false,
    isInterrupted: false,
    output: isRunning ? undefined : [{ type: 'text', text: JSON.stringify(payload) }],
  })

  test('a group holding list_leads keeps its line and adds the preview beneath', async ($, on) => {
    engineDraws(on)
    for (const surface of SURFACES) {
      const ui = await $.ui.mount({ ...group([call('Read', {}), call('mcp__akquise__list_leads', LIST_LEADS)]), surface })
      expect(await ui.find({ text: 'engine' })).toBeDefined()
      expect(await ui.find({ text: /Dr\. Huber Zahnmedizin/ })).toBeDefined()
      await ui.unmount()
    }
  })

  test('a group still running, or without ListM8 calls, is the engine’s alone', async ($, on) => {
    engineDraws(on)
    const running = await $.ui.mount({ ...group([call('mcp__akquise__list_leads', LIST_LEADS, true)]), surface: 'terminal' })
    expect(await running.find({ text: /Dr\. Huber/ })).toBeUndefined()
    await running.unmount()
    const other = await $.ui.mount({ ...group([call('Read', {})]), surface: 'terminal' })
    expect(await other.find({ text: 'engine' })).toBeDefined()
    await other.unmount()
  })
})
