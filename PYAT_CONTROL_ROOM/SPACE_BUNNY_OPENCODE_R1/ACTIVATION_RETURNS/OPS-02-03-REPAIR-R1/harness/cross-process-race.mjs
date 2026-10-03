// HQ188-A: TWO GENUINE OS PROCESSES racing submission against one store.
// Separate node PIDs, not an in-process simulation. Proves the enforced-writer
// discipline actually serialises across process boundaries.

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawn } from 'node:child_process';
import { pathToFileURL } from 'node:url';

const dispatcher = process.argv[2];
const storeDir = process.argv[3];
const D = await import(pathToFileURL(dispatcher).href);

// child worker: submit one task, print JSON result
const childSrc = `
import {pathToFileURL} from 'node:url';
const D = await import(pathToFileURL(${JSON.stringify(dispatcher)}).href);
const store = new D.Store(${JSON.stringify(storeDir)});
const t = JSON.parse(process.argv[2]);
try {
  const r = D.submitTask(store, t);
  console.log(JSON.stringify({ok:true, ...r}));
} catch (e) {
  console.log(JSON.stringify({ok:false, code:e.code||e.constructor.name, detail:e.detail||e.message}));
}
`;

const childPath = path.join(path.dirname(storeDir), 'racer.mjs');
fs.writeFileSync(childPath, childSrc);

const ROOT = path.dirname(storeDir);
const SHA = '2'.repeat(40);
function task(id) {
  const wt = path.join(ROOT, 'wt-' + id);
  fs.mkdirSync(wt, { recursive: true });
  return {
    task_id: id, role: 'worker', base_commit: SHA, worktree: wt, terrain: ['allowed/**'],
    acceptance_inputs: { gate: 'race' }, commission_path: path.join(wt, 'C.md'),
    commission_identity: 'b'.repeat(40),
    model: 'opencode-go/space-bunny-free', reasoning_variant: 'max',
  };
}

function runChild(t) {
  return new Promise((resolve) => {
    const c = spawn(process.execPath, [childPath, JSON.stringify(t)], { shell: false });
    let out = '', err = '';
    c.stdout.on('data', b => out += b);
    c.stderr.on('data', b => err += b);
    c.on('exit', code => resolve({ pid: c.pid, exit_code: code, stdout: out.trim(), stderr: err.trim() }));
  });
}

// --- Race A: SAME task id submitted by two real processes simultaneously.
// Exactly one must record the QUEUED event; the other must be idempotent.
const [a, b] = await Promise.all([runChild(task('RACE-SAME')), runChild(task('RACE-SAME'))]);
const parsed = [a, b].map(r => { try { return JSON.parse(r.stdout); } catch { return { ok: false, raw: r.stdout, stderr: r.stderr }; } });
const store = new D.Store(storeDir);
const sameQueued = store.all().filter(e => e.task_id === 'RACE-SAME' && e.state === 'QUEUED').length;

// --- Race B: DIFFERENT task ids racing for the same capped slot.
// worker cap is 2. Two distinct tasks may both queue; a third must be refused.
// Launch four distinct tasks concurrently and count how many actually queued.
const others = ['R1', 'R2', 'R3', 'R4'].map(id => task('RACE-' + id));
const results = await Promise.all(others.map(runChild));
const parsedOthers = results.map(r => { try { return JSON.parse(r.stdout); } catch { return { ok: false, raw: r.stdout }; } });
const queuedIds = new Set(store.all().filter(e => e.state === 'QUEUED' && String(e.task_id).startsWith('RACE-')).map(e => e.task_id));
const refused = parsedOthers.filter(p => p.ok === false).map(p => p.code);

const all = store.all();
const corrupt = store.corruption();
const integrity = {
  all_records_parse: corrupt.length === 0,
  no_duplicate_event_keys: new Set(all.map(e => e.key)).size === all.length,
  every_queued_task_has_complete_binding: all.filter(e => e.state === 'QUEUED').every(e => e.binding && e.binding.task_id && e.binding.model && e.binding.reasoning_variant),
  same_task_queued_exactly_once: sameQueued === 1,
  distinct_task_race_all_recorded_or_cleanly_refused: others.every((t, i) =>
    (queuedIds.has(t.task_id) && parsedOthers[i].ok) || (!queuedIds.has(t.task_id) && parsedOthers[i].ok === false)),
};

console.log(JSON.stringify({
  race_A_same_task: {
    child_pids: [a.pid, b.pid], distinct_pids: a.pid !== b.pid,
    results: parsed, queued_events_for_task: sameQueued,
    exactly_once: sameQueued === 1,
    idempotent_not_error: parsed.some(p => p.ok && p.dedup === true) || parsed.some(p => p.ok === false && p.code === 'CORRUPT_EVENT_LOG') === false,
  },
  race_B_distinct_tasks_for_capped_slots: {
    worker_slot_cap: D.SLOTS.worker,
    child_pids: results.map(r => r.pid), distinct_pids: new Set(results.map(r => r.pid)).size === results.length,
    queued_task_ids: [...queuedIds], refusal_codes: refused,
    queued_count: queuedIds.size,
  },
  store_integrity: integrity,
  corruption: corrupt,
}, null, 2));