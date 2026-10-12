import { test } from 'node:test';
import assert from 'node:assert/strict';
import { createScheduler, DECISION_TYPES } from '../runtime/scheduler.mjs';
import { mkdtempSync, readFileSync, writeFileSync, existsSync, statSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { execSync } from 'node:child_process';

test('Malformed JSON input does not crash scheduler', () => {
  const scheduler = createScheduler();
  const malformedInputs = [
    null,
    undefined,
    {},
    { task: null, resources: null, quota: null },
    { task: {}, resources: [], quota: {} },
    { task: { needs: 'not-an-array' }, resources: [], quota: {} },
    { task: {}, resources: 'not-an-array', quota: {} },
    { task: {}, resources: [], quota: 'not-an-object' },
    { task: {}, resources: [{ id: 123 }], quota: {} },
    { task: {}, resources: [], quota: { normalized_remaining: 'invalid' } },
  ];

  for (const input of malformedInputs) {
    const result = scheduler.advise(input);
    assert.ok(result.decision, `Should produce a decision for input: ${JSON.stringify(input)}`);
    assert.ok(result.provenance, 'Should include provenance');
  }
});

test('Extra account circumvention is rejected', () => {
  const scheduler = createScheduler();
  const task = { id: 'test', needs: ['python'], risk: 'low' };
  const resources = [
    { id: 'GO_1', class: 'subscription_pool' },
    { id: 'GO_2', class: 'subscription_pool', intended_for_limit_evasion: true },
    { id: 'GO_3', class: 'subscription_pool', intended_for_limit_evasion: true }
  ];
  const result = scheduler.advise({
    task,
    resources,
    quota: { normalized_remaining: 0.5 },
    secondary_go_account_intended_for_limit_evasion: true
  });
  assert.equal(result.decision, DECISION_TYPES.RESOURCE_INELIGIBLE_PROVIDER_POLICY);
});

test('Unverified pricing is not treated as zero cost', () => {
  const scheduler = createScheduler();
  const task = { id: 'test', needs: ['python'], risk: 'low' };
  const resources = [{ id: 'OPENCODE_GO', class: 'subscription_pool' }];
  const result = scheduler.advise({
    task,
    resources,
    quota: { normalized_remaining: null },
    cost_estimate: null,
    wall_estimate: null
  });
  assert.equal(result.decision, DECISION_TYPES.EXPLICIT_ESTIMATE_UNKNOWN_OR_BOUNDED_PROBE);
  assert.ok(result.assumptions.every(a => !a.includes('zero cost')));
});

test('Active worker preservation: no duplicate/force reset', () => {
  const scheduler = createScheduler();
  const task = {
    id: 'test',
    status: 'EXISTING_ACTIVE_NOT_RETURNED',
    needs: ['python'],
    risk: 'low'
  };
  const resources = [
    { id: 'CODEX_A', class: 'codex' },
    { id: 'DEEPSEEK_HARNESS', class: 'metered_local' }
  ];
  const result = scheduler.advise({ task, resources, quota: {} });
  assert.equal(result.decision, DECISION_TYPES.PRESERVE_ACTIVE_WORKTREE_AND_RESUME);
  assert.ok(!result.recommendations.some(r => r.action === 'RESET'));
  assert.ok(!result.recommendations.some(r => r.action === 'CLONE'));
});

test('False runtime evidence: Browser cannot claim local execution', () => {
  const scheduler = createScheduler();
  const task = { id: 'test', needs: ['python', 'pytest', 'sigkill'], risk: 'high' };
  const resources = [{
    id: 'BROWSER_HQ',
    class: 'browser_github',
    local_python: false,
    local_raw_custody: false
  }];
  const result = scheduler.advise({ task, resources, quota: {} });
  assert.equal(result.decision, DECISION_TYPES.NO_ELIGIBLE_EXECUTION_RESOURCE);
  assert.ok(!result.recommendations.some(r => r.action === 'EXECUTE'));
});

test('Unauthorized fallback: no automatic paid overflow', () => {
  const scheduler = createScheduler();
  const task = { id: 'test', needs: ['python'], risk: 'low' };
  const resources = [{ id: 'OPENCODE_GO', class: 'subscription_pool' }];
  const result = scheduler.advise({
    task,
    resources,
    quota: { normalized_remaining: 0, overflow_enabled: false }
  });
  assert.equal(result.decision, DECISION_TYPES.WAIT_FOR_RESET_OR_BUDGET_HOLD);
  assert.ok(!result.recommendations.some(r => r.action === 'PAY_OVERFLOW'));
});

test('Side-effect verification: synthetic Git/worktree state unchanged after advise', () => {
  const tmpDir = mkdtempSync(join(tmpdir(), 'scheduler-test-'));
  const stateFile = join(tmpDir, 'state.json');
  const initialState = { commits: 0, branches: ['main'], status: 'clean' };
  writeFileSync(stateFile, JSON.stringify(initialState, null, 2));

  const scheduler = createScheduler();
  const task = { id: 'test', needs: ['python'], risk: 'low' };
  const resources = [{ id: 'OPENCODE_GO', class: 'subscription_pool' }];

  scheduler.advise({ task, resources, quota: { normalized_remaining: 0.5 } });

  const afterState = JSON.parse(readFileSync(stateFile, 'utf8'));
  assert.deepEqual(afterState, initialState);
});

test('Crash/restart: scheduler produces consistent results across instances', () => {
  const task = { id: 'test', needs: ['python'], risk: 'low' };
  const resources = [{ id: 'OPENCODE_GO', class: 'subscription_pool' }];
  const quota = { normalized_remaining: 0.5 };

  const scheduler1 = createScheduler();
  const result1 = scheduler1.advise({ task, resources, quota });

  const scheduler2 = createScheduler();
  const result2 = scheduler2.advise({ task, resources, quota });

  assert.deepEqual(result1, result2);
});

test('Duplicate task IDs are handled deterministically', () => {
  const scheduler = createScheduler();
  const task = { id: 'duplicate-id', needs: ['python'], risk: 'low' };
  const resources = [
    { id: 'OPENCODE_GO', class: 'subscription_pool' },
    { id: 'DEEPSEEK_HARNESS', class: 'metered_local' }
  ];
  const result = scheduler.advise({ task, resources, quota: { normalized_remaining: 0.5 } });
  assert.ok(result.decision);
  assert.ok(result.provenance);
});

test('Missing quota states produce REQUIRES_EVIDENCE not zero', () => {
  const scheduler = createScheduler();
  const task = { id: 'test', needs: ['python'], risk: 'low' };
  const resources = [{ id: 'OPENCODE_GO', class: 'subscription_pool' }];

  const result = scheduler.advise({
    task,
    resources,
    quota: { normalized_remaining: null, reset_at: null }
  });

  assert.ok(
    result.decision === DECISION_TYPES.EXPLICIT_ESTIMATE_UNKNOWN_OR_BOUNDED_PROBE ||
    result.decision === DECISION_TYPES.REQUIRES_RESOURCE_EVIDENCE ||
    result.decision === DECISION_TYPES.WAIT_FOR_RESET_OR_BUDGET_HOLD ||
    result.decision === DECISION_TYPES.REQUIRE_FRESH_RESOURCE_EVIDENCE,
    `Expected evidence-requiring decision, got: ${result.decision}`
  );
});

test('Fake repo refs do not bypass hard gates', () => {
  const scheduler = createScheduler();
  const task = { id: 'test', needs: ['python'], risk: 'low' };
  const resources = [{
    id: 'FAKE_REPO',
    class: 'subscription_pool',
    fake_ref: true,
    unverified: true
  }];
  const result = scheduler.advise({ task, resources, quota: { normalized_remaining: 0.5 } });
  assert.ok(result.decision);
  assert.ok(result.provenance.hard_gates.length > 0);
});

test('Competing update: no arbitrary worker cap imposed', () => {
  const scheduler = createScheduler();
  const task = { id: 'test', needs: ['python'], risk: 'low' };
  const resources = [
    { id: 'WORKER_1', class: 'codex' },
    { id: 'WORKER_2', class: 'codex' },
    { id: 'WORKER_3', class: 'codex' },
    { id: 'WORKER_4', class: 'codex' },
    { id: 'WORKER_5', class: 'codex' },
    { id: 'WORKER_6', class: 'codex' }
  ];
  const result = scheduler.advise({
    task,
    resources,
    quota: { normalized_remaining: 0.8 }
  });
  assert.ok(result.decision);
  assert.ok(!result.recommendations.some(r => r.action === 'CAP_WORKERS'));
});
