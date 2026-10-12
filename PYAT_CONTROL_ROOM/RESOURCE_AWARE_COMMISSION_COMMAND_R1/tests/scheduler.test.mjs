import { test } from 'node:test';
import assert from 'node:assert/strict';
import { createScheduler, DECISION_TYPES } from '../runtime/scheduler.mjs';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const vectors = JSON.parse(
  readFileSync(join(__dirname, '../fixtures/test_vectors.json'), 'utf8')
);

function makeResource(id, overrides = {}) {
  const base = {
    id,
    class: 'unknown',
    role: 'unknown',
    account_alias: null,
    model: null,
    variant: null,
    machine: null,
    tools: [],
    local_python: null,
    local_raw_custody: null,
    remaining_usage: null,
    reset_at: null,
    cost_per_accepted_product: null,
    source_privacy: 'UNKNOWN',
    live_evidence: 'NOT_MEASURED',
    can_act_as_runtime_reviewer: false,
    ...overrides
  };
  return base;
}

function makeTask(overrides = {}) {
  return {
    id: 'test-task',
    needs: [],
    risk: 'low',
    critical_path: false,
    status: 'NEW_NEEDS_LAUNCH',
    provenance: 'test',
    ...overrides
  };
}

function makeQuota(overrides = {}) {
  return {
    normalized_remaining: null,
    window: null,
    reset_at: null,
    overflow_enabled: false,
    ...overrides
  };
}

test('T01: Browser-only resource for pytest+SIGKILL task → NO_ELIGIBLE_EXECUTION_RESOURCE', () => {
  const scheduler = createScheduler();
  const task = makeTask({ needs: ['python', 'pytest', 'sigkill'], risk: 'high' });
  const resources = [makeResource('BROWSER_HQ', {
    class: 'browser_github',
    role: 'command_science_review',
    local_python: false,
    local_raw_custody: false
  })];
  const result = scheduler.advise({ task, resources, quota: makeQuota() });
  assert.equal(result.decision, DECISION_TYPES.NO_ELIGIBLE_EXECUTION_RESOURCE);
  assert.ok(result.provenance.hard_gates.includes('host_runtime'));
});

test('T02: Cheap DeepSeek tasked with unreviewed original scientific issuer → BROWSER_SCIENCE_OWNER_OR_SCIENTIFIC_HOLD', () => {
  const scheduler = createScheduler();
  const task = makeTask({ needs: ['document_science'], risk: 'issuer' });
  const resources = [
    makeResource('DEEPSEEK_HARNESS', { class: 'metered_local', role: 'economical_evidence_and_bounded_repairs' }),
    makeResource('BROWSER_HQ', { class: 'browser_github', role: 'command_science_review' })
  ];
  const result = scheduler.advise({ task, resources, quota: makeQuota() });
  assert.equal(result.decision, DECISION_TYPES.BROWSER_SCIENCE_OWNER_OR_SCIENTIFIC_HOLD);
});

test('T03: Budget exhausted, reset unknown, overflow disabled → WAIT_FOR_RESET_OR_BUDGET_HOLD', () => {
  const scheduler = createScheduler();
  const task = makeTask({ needs: ['python'], risk: 'low' });
  const resources = [makeResource('OPENCODE_GO', { class: 'subscription_pool' })];
  const quota = makeQuota({ normalized_remaining: 0, overflow_enabled: false });
  const result = scheduler.advise({ task, resources, quota });
  assert.equal(result.decision, DECISION_TYPES.WAIT_FOR_RESET_OR_BUDGET_HOLD);
});

test('T04: Two model SKUs sharing Go pool → SHARED_POOL_EXHAUSTED', () => {
  const scheduler = createScheduler();
  const task = makeTask({ needs: ['python'], risk: 'low' });
  const resources = [makeResource('OPENCODE_GO', {
    class: 'subscription_pool',
    eligible_models: [
      { label: 'GLM-5.3 Flash', fraction_used: 0.5 },
      { label: 'Kimi K2.7 Code', fraction_used: 0.5 }
    ]
  })];
  const quota = makeQuota({ normalized_remaining: 0 });
  const result = scheduler.advise({ task, resources, quota });
  assert.equal(result.decision, DECISION_TYPES.SHARED_POOL_EXHAUSTED);
});

test('T05: Codex A exhausted but B known usable → CONSIDER_CODEX_B_IF_INDEPENDENCE_AND_BUDGET_ALLOW', () => {
  const scheduler = createScheduler();
  const task = makeTask({ needs: ['python'], risk: 'high' });
  const resources = [
    makeResource('CODEX_A', { class: 'codex', remaining_usage: 0 }),
    makeResource('CODEX_B', { class: 'codex', remaining_usage: 50, authorized: true })
  ];
  const result = scheduler.advise({ task, resources, quota: makeQuota() });
  assert.equal(result.decision, DECISION_TYPES.CONSIDER_CODEX_B_IF_INDEPENDENCE_AND_BUDGET_ALLOW);
});

test('T06: Existing locally active worker with unpushed work → PRESERVE_ACTIVE_WORKTREE_AND_RESUME', () => {
  const scheduler = createScheduler();
  const task = makeTask({ status: 'EXISTING_ACTIVE_NOT_RETURNED', needs: ['python'], risk: 'low' });
  const resources = [
    makeResource('CODEX_A', { class: 'codex' }),
    makeResource('DEEPSEEK_HARNESS', { class: 'metered_local' })
  ];
  const result = scheduler.advise({ task, resources, quota: makeQuota() });
  assert.equal(result.decision, DECISION_TYPES.PRESERVE_ACTIVE_WORKTREE_AND_RESUME);
});

test('T07: Pushed worker return but no HQ adoption → INTAKE_EXISTING_RETURN', () => {
  const scheduler = createScheduler();
  const task = makeTask({ status: 'PUSHED_READY_FOR_HQ_INTAKE', needs: ['git_review'], risk: 'low' });
  const result = scheduler.advise({ task, resources: [], quota: makeQuota() });
  assert.equal(result.decision, DECISION_TYPES.INTAKE_EXISTING_RETURN);
});

test('T08: Reviewer is implementer → REVIEW_INELIGIBLE', () => {
  const scheduler = createScheduler();
  const task = makeTask({ needs: ['independent_review'], risk: 'high' });
  const result = scheduler.advise({
    task,
    resources: [],
    quota: makeQuota(),
    reviewer_same_as_implementer: true
  });
  assert.equal(result.decision, DECISION_TYPES.REVIEW_INELIGIBLE);
});

test('T09: Two writers overlap same exact owner/write paths → SERIALIZE_COLLIDING_WRITES_CONTINUE_ORTHOGONAL', () => {
  const scheduler = createScheduler();
  const task = makeTask({ needs: ['owner_mutation'], risk: 'high' });
  const result = scheduler.advise({
    task,
    resources: [],
    quota: makeQuota(),
    write_overlap: true,
    otherwise_independent_lane_ready: true
  });
  assert.equal(result.decision, DECISION_TYPES.SERIALIZE_COLLIDING_WRITES_CONTINUE_ORTHOGONAL);
});

test('T10: No qualified source/operation/EE12/EE13/model-use issuer → SCIENTIFIC_HOLD', () => {
  const scheduler = createScheduler();
  const task = makeTask({ needs: ['original_ee12_issuer'], risk: 'issuer' });
  const resources = [
    makeResource('CODEX_A', { class: 'codex' }),
    makeResource('ASTRA', { class: 'strategic_oversight' }),
    makeResource('BROWSER_HQ', { class: 'browser_github' })
  ];
  const result = scheduler.advise({ task, resources, quota: makeQuota(), issuer_credential: null });
  assert.equal(result.decision, DECISION_TYPES.SCIENTIFIC_HOLD);
});

test('T11: Cost and time estimates absent → EXPLICIT_ESTIMATE_UNKNOWN_OR_BOUNDED_PROBE', () => {
  const scheduler = createScheduler();
  const task = makeTask({ needs: ['python'], risk: 'low' });
  const result = scheduler.advise({
    task,
    resources: [makeResource('OPENCODE_GO', { class: 'subscription_pool' })],
    quota: makeQuota(),
    cost_estimate: null,
    wall_estimate: null
  });
  assert.equal(result.decision, DECISION_TYPES.EXPLICIT_ESTIMATE_UNKNOWN_OR_BOUNDED_PROBE);
});

test('T12: Free Browser incurs prohibitive repeated Git roundtrips → LOCAL_EVIDENCE_COLLECTOR_WITH_BROWSER_HQ_OWNER', () => {
  const scheduler = createScheduler();
  const task = makeTask({ needs: ['many_repo_reads'], risk: 'low' });
  const result = scheduler.advise({
    task,
    resources: [],
    quota: makeQuota(),
    browser_roundtrip_measured_slow: true,
    cheap_local_collector_available: true
  });
  assert.equal(result.decision, DECISION_TYPES.LOCAL_EVIDENCE_COLLECTOR_WITH_BROWSER_HQ_OWNER);
});

test('T13: Semantically successful measured null with valid product/consumer → COUNT_SCIENTIFIC_PRODUCT', () => {
  const scheduler = createScheduler();
  const task = makeTask({ needs: ['empirical_product'], risk: 'high' });
  const result = scheduler.advise({
    task,
    resources: [],
    quota: makeQuota(),
    measured_supported_null: true,
    real_consumer: true
  });
  assert.equal(result.decision, DECISION_TYPES.COUNT_SCIENTIFIC_PRODUCT);
});

test('T14: Fail-open/torn Space Bunny dispatcher → ADVISORY_ONLY_PUBLICATION_HOLD', () => {
  const scheduler = createScheduler();
  const task = makeTask({ needs: ['publication'], risk: 'security' });
  const result = scheduler.advise({
    task,
    resources: [],
    quota: makeQuota(),
    dispatcher_qualified: false
  });
  assert.equal(result.decision, DECISION_TYPES.ADVISORY_ONLY_PUBLICATION_HOLD);
});

test('T15: Stale provider pricing versus fresh observed provider limits → REQUIRE_FRESH_RESOURCE_EVIDENCE', () => {
  const scheduler = createScheduler();
  const task = makeTask({ needs: ['python'], risk: 'low' });
  const result = scheduler.advise({
    task,
    resources: [makeResource('OPENCODE_GO', { class: 'subscription_pool' })],
    quota: makeQuota({ normalized_remaining: null }),
    pricing_freshness: 'STALE'
  });
  assert.equal(result.decision, DECISION_TYPES.REQUIRE_FRESH_RESOURCE_EVIDENCE);
});

test('T16: Raw/private source provider has training/retention restriction → PROVIDER_PRIVACY_INELIGIBLE', () => {
  const scheduler = createScheduler();
  const task = makeTask({ needs: ['private_repo_processing'], risk: 'high' });
  const resources = [makeResource('FREE_PROVIDER_X', {
    class: 'metered_local',
    source_privacy: 'TRAINING_ALLOWED'
  })];
  const result = scheduler.advise({
    task,
    resources,
    quota: makeQuota(),
    provider_training: true,
    source_permission: false
  });
  assert.equal(result.decision, DECISION_TYPES.PROVIDER_PRIVACY_INELIGIBLE);
});

test('T17: Provider model repeatedly loops or fails stream → HALT_AND_PRESERVE_LOCAL_STATE', () => {
  const scheduler = createScheduler();
  const task = makeTask({ needs: ['python'], risk: 'low' });
  const result = scheduler.advise({
    task,
    resources: [],
    quota: makeQuota(),
    provider_stream_failure_repeated: true,
    local_committed_work: true
  });
  assert.equal(result.decision, DECISION_TYPES.HALT_AND_PRESERVE_LOCAL_STATE);
});

test('T18: Unknown current branch HEAD / changed branch ancestry / missing worktree → BLOCK_STARTUP_NO_CLONE_RESET', () => {
  const scheduler = createScheduler();
  const task = makeTask({ needs: ['worktree_mutation'], risk: 'low' });
  const result = scheduler.advise({
    task,
    resources: [],
    quota: makeQuota(),
    remote_sha_unknown: true,
    worktree_missing: true
  });
  assert.equal(result.decision, DECISION_TYPES.BLOCK_STARTUP_NO_CLONE_RESET);
});

test('T19: Reviewer frozen tip != candidate tip → REVIEW_INVALIDATED_BY_CHANGED_CANDIDATE', () => {
  const scheduler = createScheduler();
  const task = makeTask({ needs: ['runtime_review'], risk: 'high' });
  const result = scheduler.advise({
    task,
    resources: [],
    quota: makeQuota(),
    review_frozen_tip: 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
    candidate_tip: 'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb'
  });
  assert.equal(result.decision, DECISION_TYPES.REVIEW_INVALIDATED_BY_CHANGED_CANDIDATE);
});

test('T20: Secondary Go account intended for limit evasion → RESOURCE_INELIGIBLE_PROVIDER_POLICY', () => {
  const scheduler = createScheduler();
  const task = makeTask({ needs: ['python'], risk: 'low' });
  const result = scheduler.advise({
    task,
    resources: [],
    quota: makeQuota(),
    secondary_go_account_intended_for_limit_evasion: true
  });
  assert.equal(result.decision, DECISION_TYPES.RESOURCE_INELIGIBLE_PROVIDER_POLICY);
});

test('T21: Astra only because two retries → HQ_ROOT_CAUSE_REVIEW_NOT_AUTO_ASTRA', () => {
  const scheduler = createScheduler();
  const task = makeTask({ needs: ['authority_decision'], risk: 'high' });
  const result = scheduler.advise({
    task,
    resources: [],
    quota: makeQuota(),
    astra_only_because_two_retries: true,
    scientific_conflict: false
  });
  assert.equal(result.decision, DECISION_TYPES.HQ_ROOT_CAUSE_REVIEW_NOT_AUTO_ASTRA);
});

test('T22: Static repo text not executed owner chain → RUNTIME_UNPROVED', () => {
  const scheduler = createScheduler();
  const task = makeTask({ needs: ['local_python', 'real_consumer'], risk: 'high' });
  const result = scheduler.advise({
    task,
    resources: [],
    quota: makeQuota(),
    source_only_static_graph: true,
    executed_calls: 0
  });
  assert.equal(result.decision, DECISION_TYPES.RUNTIME_UNPROVED);
});

test('All 22 predeclared vector definitions are present in fixture', () => {
  const ids = vectors.cases.map(c => c.id);
  const expected = Array.from({ length: 22 }, (_, i) => `T${String(i + 1).padStart(2, '0')}`);
  assert.deepEqual(ids, expected);
  for (const c of vectors.cases) {
    assert.ok(c.expected, `${c.id} missing expected`);
    assert.ok(c.assert, `${c.id} missing assert`);
  }
});

test('Scheduler is pure: same input produces same output', () => {
  const scheduler = createScheduler();
  const task = makeTask({ needs: ['python'], risk: 'low' });
  const resources = [makeResource('OPENCODE_GO', { class: 'subscription_pool' })];
  const quota = makeQuota({ normalized_remaining: 0.5 });

  const result1 = scheduler.advise({ task, resources, quota });
  const result2 = scheduler.advise({ task, resources, quota });

  assert.deepEqual(result1, result2);
});

test('Scheduler produces no side effects on input objects', () => {
  const scheduler = createScheduler();
  const task = makeTask({ needs: ['python'], risk: 'low' });
  const resources = [makeResource('OPENCODE_GO', { class: 'subscription_pool' })];
  const quota = makeQuota({ normalized_remaining: 0.5 });

  const taskBefore = JSON.parse(JSON.stringify(task));
  const resourcesBefore = JSON.parse(JSON.stringify(resources));
  const quotaBefore = JSON.parse(JSON.stringify(quota));

  scheduler.advise({ task, resources, quota });

  assert.deepEqual(task, taskBefore);
  assert.deepEqual(resources, resourcesBefore);
  assert.deepEqual(quota, quotaBefore);
});
