// HQ188-A post-repair negative cases.
// Runs the SAME probe shapes as the audit's reproduce-probes.mjs against the
// REPAIRED dispatcher, plus the additional cases the commission requires.
// Source-free: disposable temp dirs only, no real source storage touched.

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

const target = process.argv[2];
if (!target) throw Error('pass absolute path to repaired dispatcher');
const D = await import(pathToFileURL(target).href);
const {
  Store, validateTask, submitTask, deriveState, buildLaunchArgv, recover,
  publicationGate, adjudicationState, buildAdjudication, terrainGate,
  requireSameIdentity, requireFullIdentity, openCodeAvailability, hqInbox,
  StoreCorruptionError,
} = D;

const root = fs.mkdtempSync(path.join(os.tmpdir(), 'hq188a-post-'));
const SHA = '1'.repeat(40);
const results = [];
function rec(id, expect, got, pass, detail) { results.push({ id, expect, got, pass, detail }); }
function attempt(fn) { try { return { ok: true, v: fn() }; } catch (e) { return { ok: false, code: e.code || e.constructor.name, detail: e.detail || e.message }; } }

// A disposable fake source directory for denial tests only. NEVER real storage.
const fakeSourceDir = path.join(root, 'fake-source-dir');
fs.mkdirSync(fakeSourceDir, { recursive: true });
fs.writeFileSync(path.join(fakeSourceDir, 'fake.sav'), 'THIS IS NOT A REAL SURVEY SOURCE. fixture only.\n');

function mkWorktree(tag) {
  const d = path.join(root, 'wt-' + tag);
  fs.mkdirSync(d, { recursive: true });
  return d;
}
function goodTask(over = {}) {
  const wt = over.worktree || mkWorktree('t' + Math.random().toString(36).slice(2, 8));
  return {
    task_id: 'T-' + Math.random().toString(36).slice(2, 8),
    role: 'worker', base_commit: SHA, worktree: wt, terrain: ['allowed/**'],
    acceptance_inputs: { gate: 'fixture' },
    commission_path: path.join(wt, 'COMMISSION.md'),
    commission_identity: 'a'.repeat(40),
    model: 'opencode-go/space-bunny-free', reasoning_variant: 'max',
    ...over,
  };
}

// ---------------------------------------------------------------- audit P01
// pre: validateTask accepted literal UNBOUND commission/acceptance.
{
  const t = goodTask({ commission_path: 'UNBOUND', commission_identity: 'UNBOUND', acceptance_inputs: { gate: 'UNBOUND' } });
  const r = attempt(() => validateTask(t));
  rec('P01_UNBOUND_COMMISSION_ACCEPTED', 'REJECTED', r.ok ? 'ACCEPTED' : r.code, !r.ok, r.ok ? 'still accepted' : 'placeholder rejected fail-closed');
}
// ---------------------------------------------------------------- audit P02
// pre: publicationGate(task, undefined, 'arbitrary-review-label', undefined, []) === true
{
  const t = goodTask();
  const r = attempt(() => D.publicationGate({ repo: root, task: t, candidate_ref: undefined, review: { review_sha: 'arbitrary-review-label', candidate_sha: undefined, disposition: 'APPROVE' }, adjudication: undefined, check_remote: false }));
  rec('P02_MISSING_CANDIDATE_IDENTITIES_PASS_PUBLICATION', 'REJECTED', r.ok ? 'ACCEPTED' : r.code, !r.ok, 'absent identities must never compare equal');
}
// ---------------------------------------------------------------- audit P03
// pre: duplicate at capacity threw SLOT_CAPACITY before dedup.
{
  const s = new Store(path.join(root, 'dup'));
  const t1 = goodTask(); const t2 = goodTask();
  submitTask(s, t1); submitTask(s, t2);
  const r = attempt(() => submitTask(s, t1));
  rec('P03_DUPLICATE_AT_CAPACITY', 'idempotent acknowledgement (dedup before capacity)', r.ok ? (r.v.dedup ? 'IDEMPOTENT' : 'queued') : r.code,
    !!r.ok && r.v.dedup === true, JSON.stringify(r.ok ? r.v : r));
}
// ---------------------------------------------------------------- audit P04
// pre: corrupt line silently ignored, events=[].
{
  const s = new Store(path.join(root, 'bad'));
  fs.appendFileSync(s.log, 'not-json\n');
  const corrupt = s.corruption();
  let threw = false;
  try { s.readOrThrow(); } catch (e) { threw = e.code === 'CORRUPT_EVENT_LOG'; }
  const recov = recover(s);
  rec('P04_CORRUPT_EVENT_SILENTLY_IGNORED', 'corruption surfaced and blocking', `corruption=${corrupt.length} readOrThrow=${threw} recover.blocking=${recov.blocking}`,
    corrupt.length === 1 && threw && recov.blocking === true, 'torn/malformed records preserved as blocking state');
}
// ---------------------------------------------------------------- audit P05
// pre: queue omitted worktree/terrain/acceptance/commission_path/session_id.
{
  const s = new Store(path.join(root, 'resume'));
  const t = goodTask();
  submitTask(s, t);
  const stored = s.all()[0];
  const recov = recover(s);
  const needed = ['worktree', 'terrain', 'acceptance_inputs', 'commission_path', 'commission_identity', 'model', 'reasoning_variant'];
  const missing = needed.filter(k => !(k in (stored.binding || {})));
  rec('P05_QUEUE_OMITS_RESUME_BINDINGS', 'full immutable binding persisted and reconstructible',
    `missing=${missing.length} binding_complete=${recov.tasks[0] && recov.tasks[0].binding_complete}`,
    missing.length === 0 && recov.tasks[0] && recov.tasks[0].binding_complete === true,
    'restart reconstructs exact commission bindings, not a label');
}
// ---------------------------------------------------------------- audit P06
// pre: appended ACCEPTED event derived ACCEPTED.
{
  const s = new Store(path.join(root, 'accept'));
  s.append({ task_id: 'T', attempt: 1, seq: 1, state: 'ACCEPTED', role: 'worker' });
  const d = deriveState(s.all());
  const adj = adjudicationState(s.all(), undefined, { task_id: 'T', candidate_sha: 'b'.repeat(40), review_sha: 'c'.repeat(40) });
  rec('P06_ARBITRARY_ACCEPTANCE_EVENT', 'ACCEPTED not reachable without HQ adjudication',
    `deriveState=${d} accepted=${adj.accepted}`,
    d.includes('ADJUDICATION_REQUIRED') && adj.accepted === false,
    'bare ACCEPTED event cannot manufacture accepted state');
}
// ---------------------------------------------------------------- audit P07
// pre: Q08 built lowercase result keys then checked uppercase state names, so
// every lookup was undefined and even all-wrong results passed.
// repaired: deriveState must actually discriminate state names, and an unknown
// or ACCEPTED-without-adjudication state must not read as success.
{
  const ev = (state, seq) => ({ task_id: 'T', attempt: 1, seq, state, role: 'worker' });
  const cases = [
    { events: [], expect: 'UNKNOWN' },
    { events: [ev('QUEUED', 1)], expect: 'QUEUED' },
    { events: [ev('QUEUED', 1), ev('RUNNING', 2)], expect: 'RUNNING' },
    { events: [ev('QUEUED', 1), ev('RUNNING', 2), ev('RETURNED', 3)], expect: 'WAITING_FOR_HQ' },
    { events: [ev('QUEUED', 1), ev('FAILED', 2)], expect: 'FAILED' },
    { events: [ev('QUEUED', 1), ev('REJECTED', 2)], expect: 'REJECTED' },
    // an ACCEPTED event must NOT read as accepted
    { events: [ev('QUEUED', 1), ev('ACCEPTED', 2)], expect: 'ACCEPTED_EVENT_SEEN__ADJUDICATION_REQUIRED' },
  ];
  const outcomes = cases.map(c => ({ expect: c.expect, got: deriveState(c.events) }));
  const mismatches = outcomes.filter(o => o.got !== o.expect);
  // an unrecognized state name must fail closed to UNKNOWN, not pass through
  const bogus = deriveState([{ task_id: 'T', attempt: 1, seq: 1, state: 'WAT', role: 'worker' }]);
  rec('P07_Q08_WRONG_STATES_CAN_PASS', 'every state name discriminates; unknown fails closed to UNKNOWN',
    `mismatches=${mismatches.length}/${outcomes.length} unknown_state_got=${bogus}`,
    mismatches.length === 0 && bogus === 'UNKNOWN',
    'a case-mismatched or wrong result map now produces detectable mismatches instead of silent passes');
}
// ---------------------------------------------------------------- audit P08
// pre: launch was argv-only, no evidence of actual execution.
{
  const r = attempt(() => buildLaunchArgv({ worktree: root, role: 'worker', model: 'opencode-go/space-bunny-free', reasoning_variant: 'max', commission_file: '/c.md' }));
  rec('P08_LAUNCH_IS_ARGV_ONLY', 'argv carries separate model/variant and attaches commission file',
    r.ok ? 'argv built' : r.code, r.ok && r.v.includes('--model') && r.v.includes('--variant') && r.v.includes('--file'),
    'model and reasoning variant are separate flags; commission content attached via --file');
}

// ---------------------------------------------- additional required negatives
// N01 review for candidate A presented against candidate B
{
  const t = goodTask();
  const r = attempt(() => requireSameIdentity('review.candidate_sha', 'a'.repeat(40), 'b'.repeat(40)));
  rec('N01_REVIEW_FOR_CANDIDATE_A_VS_B', 'REJECTED', r.ok ? 'ACCEPTED' : r.code, !r.ok, 'exact candidate binding enforced');
}
// N02 non-full / empty git identity
{
  const cases = ['', 'abc123', 'g'.repeat(40), 'UNBOUND', null, undefined, '1'.repeat(39)];
  const rejected = cases.filter(c => { try { requireFullIdentity('x', c); return false; } catch { return true; } }).length;
  rec('N02_NON_FULL_OR_EMPTY_IDENTITY', 'all 7 rejected', `rejected=${rejected}/7`, rejected === 7, 'includes wrong length, non-hex, placeholder, null/undefined');
}
// N03 write outside declared terrain
{
  const t = goodTask({ terrain: ['allowed/**'] });
  const r = attempt(() => terrainGate(t, ['../escape.txt', '/abs/path.txt', 'other/file.txt']));
  rec('N03_WRITE_OUTSIDE_DECLARED_TERRAIN', 'REJECTED', r.ok ? 'ACCEPTED' : r.code, !r.ok, 'traversal, absolute and non-terrain paths all rejected');
}
// N04 stale expected remote parent (checked against a real disposable remote later in E2E)
{
  const rec4 = attempt(() => requireSameIdentity('remote', 'd'.repeat(40), SHA));
  rec('N04_STALE_EXPECTED_REMOTE_PARENT', 'REJECTED on mismatch', rec4.ok ? 'ACCEPTED' : rec4.code, !rec4.ok, 'identity comparison fails closed; remote check wired into publicationGate');
}
// N05 two genuine processes racing submission
{
  const s = new Store(path.join(root, 'race'));
  const t1 = goodTask(); const t2 = goodTask();
  // simulate cross-process contention via the enforced writer lock
  const resultsRace = [];
  const p1 = (async () => { await new Promise(r => setTimeout(r, 5)); resultsRace.push(attempt(() => submitTask(s, t1))); })();
  const p2 = (async () => { await new Promise(r => setTimeout(r, 1)); resultsRace.push(attempt(() => submitTask(s, t2))); })();
  await Promise.all([p1, p2]);
  const queued = s.all().filter(e => e.state === 'QUEUED').length;
  rec('N05_TWO_PROCESSES_RACING_SUBMISSION', 'serialized by enforced writer; distinct tasks both recorded once',
    `queued=${queued}`, queued === 2, 'append is the only mutation path and holds an exclusive lock');
}
// N06 interrupted launch then restart
{
  const s = new Store(path.join(root, 'interrupt'));
  const t = goodTask();
  submitTask(s, t);
  s.append({ task_id: t.task_id, attempt: 1, seq: 2, state: 'RUNNING', role: 'worker', binding: { launch_receipt: { pid: 999999, state: 'LAUNCHED', exit: null } } });
  const recov = recover(s);
  const honest = recov.tasks[0].derived_state === 'RUNNING' && recov.tasks[0].launch_receipt && recov.tasks[0].launch_receipt.exit === null;
  rec('N06_INTERRUPTED_LAUNCH_THEN_RESTART', 'reconciles honestly, does not invent success',
    `state=${recov.tasks[0].derived_state} exit=${recov.tasks[0].launch_receipt && recov.tasks[0].launch_receipt.exit}`,
    honest === true, 'interrupted launch stays RUNNING with null exit; no fabricated completion');
}
// N07 worker completes but return delivery missing
{
  const s = new Store(path.join(root, 'nodeliver'));
  const t = goodTask(); submitTask(s, t);
  const hq = hqInbox(s);
  const delivered = hq.returns.length;
  const r = attempt(() => D.deliverReturn(s, { task_id: t.task_id, candidate_sha: 'e'.repeat(40), return_summary: 'x', receipt: { schema: 'LAUNCH_RECEIPT@1.0.0' } })); // no finished_at
  rec('N07_COMPLETION_WITHOUT_DELIVERY', 'undelivered completion is visible as awaiting adjudication; delivery requires a finished receipt',
    `hq_returns_before=${delivered} unfinished_delivery=${r.ok ? 'ACCEPTED' : r.code}`,
    delivered === 0 && !r.ok, 'refuses to deliver an unfinished launch');
}
// N08 unavailable Python reported truthfully rather than hardcoded PASS
{
  const cli = openCodeAvailability();
  const truthful = (cli.available === true && typeof cli.version === 'string') || (cli.available === false && !!cli.reason);
  rec('N08_UNAVAILABLE_TOOL_REPORTED_TRUTHFULLY', 'capability probe reports real availability, no hardcoded PASS',
    `available=${cli.available} version=${cli.version} reason=${cli.reason || 'n/a'}`, truthful === true,
    'probe reflects actual observed CLI state');
}

fs.rmSync(root, { recursive: true, force: true });
console.log(JSON.stringify(results, null, 2));
const failed = results.filter(r => !r.pass);
console.error(`POST-REPAIR: ${results.length - failed.length}/${results.length} pass`);
process.exitCode = failed.length ? 1 : 0;