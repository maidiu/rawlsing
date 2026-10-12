# RCM01 Pure Advisory Scheduler — Design

## Architecture

The scheduler is a **pure, side-effect-free** decision function implemented as a Node.js ES module (`runtime/scheduler.mjs`). It takes injected snapshots (task, resources, quota, context) and returns typed decisions with full provenance.

### Core Principles

1. **Hard gates before scoring**: Source/privacy, intelligence/risk, host/runtime, worktree/branch, reviewer independence, scientific authority, and budget/quota gates are evaluated BEFORE any money/quota/latency scoring.
2. **No side effects**: Input objects are deep-cloned; no mutations occur. No provider login, billing API, OpenCode launch, or GitHub write.
3. **Deterministic**: Same input always produces same output. Tie-break by resource ID.
4. **Unknown ≠ zero**: Missing cost/time/quota values are explicitly null and trigger evidence-requiring decisions.
5. **No dispatch**: The scheduler recommends only; it never launches, dispatches, or mutates external state.

### Decision Types

All 22 predeclared adversarial vectors map to explicit decision types:

| Vector | Decision Type |
|--------|--------------|
| T01 | NO_ELIGIBLE_EXECUTION_RESOURCE |
| T02 | BROWSER_SCIENCE_OWNER_OR_SCIENTIFIC_HOLD |
| T03 | WAIT_FOR_RESET_OR_BUDGET_HOLD |
| T04 | SHARED_POOL_EXHAUSTED |
| T05 | CONSIDER_CODEX_B_IF_INDEPENDENCE_AND_BUDGET_ALLOW |
| T06 | PRESERVE_ACTIVE_WORKTREE_AND_RESUME |
| T07 | INTAKE_EXISTING_RETURN |
| T08 | REVIEW_INELIGIBLE |
| T09 | SERIALIZE_COLLIDING_WRITES_CONTINUE_ORTHOGONAL |
| T10 | SCIENTIFIC_HOLD |
| T11 | EXPLICIT_ESTIMATE_UNKNOWN_OR_BOUNDED_PROBE |
| T12 | LOCAL_EVIDENCE_COLLECTOR_WITH_BROWSER_HQ_OWNER |
| T13 | COUNT_SCIENTIFIC_PRODUCT |
| T14 | ADVISORY_ONLY_PUBLICATION_HOLD |
| T15 | REQUIRE_FRESH_RESOURCE_EVIDENCE |
| T16 | PROVIDER_PRIVACY_INELIGIBLE |
| T17 | HALT_AND_PRESERVE_LOCAL_STATE |
| T18 | BLOCK_STARTUP_NO_CLONE_RESET |
| T19 | REVIEW_INVALIDATED_BY_CHANGED_CANDIDATE |
| T20 | RESOURCE_INELIGIBLE_PROVIDER_POLICY |
| T21 | HQ_ROOT_CAUSE_REVIEW_NOT_AUTO_ASTRA |
| T22 | RUNTIME_UNPROVED |

### Hard Gate Order

1. `source_privacy` — Provider training/export restrictions
2. `intelligence_risk` — Model competence for risk level
3. `host_runtime` — Local execution capability
4. `worktree_branch` — Worktree and remote state
5. `reviewer_independence` — Reviewer ≠ implementer
6. `scientific_authority` — Qualified issuer present
7. `budget_quota` — Budget available or overflow permitted

### Scoring (after hard gates)

Resources are scored on:
- Local execution capability (+10)
- Raw custody (+5)
- Codex remaining usage (up to +10)
- Subscription pool remaining fraction (up to +10)
- Cost efficiency (up to +10)
- Review capability (+3)
- Critical path (+2)
- Tool match (+3 per matching tool)

### API

```javascript
import { createScheduler, DECISION_TYPES } from './runtime/scheduler.mjs';

const scheduler = createScheduler();
const result = scheduler.advise({
  task: { id, needs, risk, status },
  resources: [{ id, class, role, local_python, remaining_usage, ... }],
  quota: { normalized_remaining, overflow_enabled, reset_at },
  // context overrides...
});

// result.decision — typed decision string
// result.provenance — hard gates evaluated
// result.recommendations — ranked recommendations
// result.assumptions — explicit assumptions
// result.counterfactuals — alternative tradeoffs
```

## Test Suite

- `tests/scheduler.test.mjs` — All 22 predeclared vectors
- `tests/hostiles.test.mjs` — Malformed inputs, side-effect verification, crash/restart

## Constraints

- No provider/billing/web login
- No dispatch implementation
- No edit of Space Bunny dispatcher
- No automatic paid provider or Codex usage
- All inputs from Git-tracked commission packet
