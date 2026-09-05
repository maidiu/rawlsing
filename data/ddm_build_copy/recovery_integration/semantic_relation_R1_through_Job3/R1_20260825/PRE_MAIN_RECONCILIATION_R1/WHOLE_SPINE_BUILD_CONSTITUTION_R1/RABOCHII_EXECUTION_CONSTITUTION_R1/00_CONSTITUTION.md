# RABOCHII EXECUTION CONSTITUTION R1

Status: CANDIDATE GOVERNANCE INFRASTRUCTURE — requires Vozhd adoption before claiming global project authority.

Purpose: preserve full worker capability while preventing orchestration work from multiplying necessary runtime.

## 1. Universal laws

```
ACTIVITY != PROGRESS
MODEL_BUSY_STATE != EXTERNAL_WORK_IN_PROGRESS
FINISH = DELTA_TO_FROZEN_TERMINAL
WORKER_MAY_NOT_MOVE_ITS_OWN_FINISH_LINE
PROOF_STRENGTHENING != NEW_ACCEPTANCE_REQUIREMENT
PENDING != FAILED
FAIL_CLOSED != FAIL_STALE
LOCAL_WORKSPACE != PROJECT_STATE
DURABLE_EXACT_STATE SURVIVES WORKER_OR_TOOL_WINDOW_LOSS
SEMANTIC_CANDIDATE != EVIDENCE_EXECUTION_SHA != BRANCH_TIP != PR_SYNTHETIC_MERGE_SHA
INDEPENDENT_REVIEW != DUPLICATE_EXECUTION
PROFILE_TRANSITION_REQUIRES_EXPLICIT_AUTHORITY
TEMPORARY_INFRASTRUCTURE != SEMANTIC_PROOF
WAITING_CAN_BE_PROGRESS
```

A worker MUST always be able to name the still-open terminal claim advanced by its current substantial action. If it cannot, the action stops.

## 2. Runtime phases

A bounded worker phase is one of:

- `DISCOVER`
- `SEMANTIC_AUTHORITY`
- `IMPLEMENT`
- `VERIFY_REGRESSION`
- `HOSTILE_AUDIT`
- `REAL_EXECUTION`
- `INTEGRATE`
- `RECOVERY_FORENSIC`
- `CLOSURE_ONLY`
- `TERMINAL`

Profiles are phase adapters, not lifelong worker identities. Transition between substantive profiles requires an explicit authority/disposition ref.

Examples:
- REAL_EXECUTION discovers a code defect -> return/authorize IMPLEMENT; do not silently repair.
- IMPLEMENT discovers a missing authority -> return/authorize SEMANTIC_AUTHORITY; do not constitute authority inside implementation.
- INTEGRATE discovers semantic conflict -> stop fan-in and spawn an authorized semantic/repair phase.

## 3. Terminal claims and claim types

Work is organized around frozen terminal claims, not activity.

Supported claim types:

- `DETERMINISTIC_EXECUTION`
- `EXACT_IDENTITY`
- `EXISTENCE`
- `BOUNDED_ABSENCE`
- `SEMANTIC_INTERPRETATION`
- `AUTHORITY_COMPETENCE`
- `EMPIRICAL_REPLAY`
- `INDEPENDENT_AUDIT`
- `INTEGRATION_EQUIVALENCE`

Claim state is monotonic:

```
UNKNOWN -> READY -> IN_FLIGHT -> PROVEN
                         \-> REFUTED
                         \-> BLOCKED
```

A dispatched proof owner remains tracked until `PROVEN`, `REFUTED`, `CANCELLED`, or conclusively `UNAVAILABLE`.

An `IN_FLIGHT` owner may not disappear merely because an early observation is empty.

## 4. Proof ownership and multiplicity

Every claim declares:
- proof mode;
- required proof multiplicity;
- active proof owners.

For ordinary deterministic regression, required multiplicity is normally 1.

For explicitly independent hostile review, multiplicity may exceed 1 or the proof mode may require an independent reviewer.

Law:

```
SAME_PROPOSITION
+ SAME_PROOF_MODE
+ SUFFICIENT_PROOF_ALREADY_OWNED_OR_IN_FLIGHT
=> DUPLICATE_EXECUTION_FORBIDDEN
```

If a primary proof owner becomes green while an equivalent fallback is active:

```
PRIMARY_GREEN + FALLBACK_SAME_PROPOSITION => CANCEL_FALLBACK
```

unless the fallback was explicitly authorized as independent corroboration.

## 5. Evidence compatibility

A proof cannot satisfy a claim merely because it is green.

Its evidence compatibility must be verified against the claim's declared requirements, including as applicable:
- semantic candidate/relevant tree;
- test or court specification;
- runtime/interpreter;
- dependency versions;
- determinism flags/seeds;
- fixture/data identity;
- execution mode;
- authority/source snapshot.

An evidence execution SHA may contain nonsemantic workflow/evidence-only changes beyond the semantic candidate. Such evidence is admissible only after the relevant-tree delta is explicitly classified compatible.

A synthetic PR merge SHA is never silently substituted for the candidate SHA.

## 6. Evidence volatility and freshness

Evidence/observations are classified:

- `IMMUTABLE`: commit/blob/content-addressed object.
- `SNAPSHOT`: branch or repository state at a recorded instant.
- `EVENTUALLY_CONSISTENT`: newly dispatched CI/check visibility and similar propagation.
- `LIVE`: current external status/resource availability.

```
SEARCH_EMPTY != ABSENCE_PROVED
VALID_EVIDENCE != CURRENTLY_APPLICABLE_EVIDENCE
```

An eventually-consistent negative observation cannot immediately support a failure conclusion.

Before a blocker based on missing tests, CI, material, branch state, or artifact state, the worker MUST perform the fresh-state blocker gate:
1. refresh candidate/branch tip;
2. refresh every in-flight proof owner;
3. refresh relevant PR/check/run state;
4. refresh required artifact existence;
5. re-evaluate terminal claims;
6. only then emit BLOCKED.

## 7. Async discipline

```
EXTERNAL_PROOF_IN_FLIGHT => EQUIVALENT_ALTERNATE_EXECUTION_FORBIDDEN
```

An empty first status query after dispatch is `PENDING`, not `UNAVAILABLE`.

Use bounded observation/backoff appropriate to the external system. Do not create a second trigger merely because the first run has not propagated immediately.

Useful waiting is lawful when the critical path is an authoritative asynchronous owner.

## 8. Failure classification before fallback

Before fallback, classify the failure as one of:

- `TRANSIENT_ASYNC_LATENCY`
- `EXECUTION_ENVIRONMENT_FAILURE`
- `TOOL_CAPABILITY_MISSING`
- `SOURCE_MATERIALIZATION_FAILURE`
- `RESOURCE_EXHAUSTION`
- `SEMANTIC_CONTRADICTION`
- `AUTHORITY_GAP`
- `TEST_FAILURE`
- `STALE_STATE`

Fallback must match the failure class.

A semantic contradiction is not retried on a different machine.
Transient async latency does not justify rebuilding infrastructure.
An authority gap returns to authority ownership.
Resource exhaustion may justify a separately authorized execution-equivalent repair.

Fallback must be cheaper in total state/time/risk than escalation, or explicitly authorized.

## 9. Capability preflight

Before an execution-heavy phase, record the required capabilities actually available:
- repository read/write;
- local checkout;
- container execution;
- CI dispatch;
- CI observation;
- Library access;
- Library materialization;
- outbound network if required.

Do not discover basic platform capability by constructing throwaway infrastructure after the primary plan stalls.

Execution infrastructure is a platform concern, not a worker invention surface.

## 10. Mutation and resource envelopes

Every mutating phase declares its allowed write surface.

Mutations outside that envelope require explicit authority.

Temporary branches, PRs, workflows, source acquisition, Library use, or alternate infrastructure are NOT implicitly authorized by a generic instruction to "finish".

Parallel mutation requires both:
- claim independence;
- compatible/disjoint write jurisdiction.

```
WRITE_OVERLAP + CONCURRENT_IMPLEMENTATION
=> EXPLICIT_RECONCILIATION_PLAN_REQUIRED
```

## 11. Profile-specific stopping law

### DISCOVER
Parallelize distinct hypotheses. Maintain a coverage ledger for bounded absence claims. Every search must narrow the hypothesis space. Once the bounded surface closes the question, stop synonym hunting.

### SEMANTIC_AUTHORITY
Classify exact evidence once. Do not reread/reopen a classification absent a concrete contradiction. Stronger optional proof does not become a new acceptance requirement.

### IMPLEMENT
Smallest lawful diff. Focused test. One authoritative inherited court per deterministic proposition. No semantic redesign inside implementation.

### VERIFY_REGRESSION
Frozen candidate + frozen assertions. No production design. A red deterministic court is evidence and is not erased by rerunning.

### HOSTILE_AUDIT
Independent reasoning is intentional. Preserve reviewer independence; provide governing law and frozen candidate without unnecessary anchoring from implementer rationale.

### REAL_EXECUTION
Use stage receipts/checkpoints:
`MATERIALIZE -> HASH_VERIFY -> PROJECT -> VALIDATE -> INDEX -> EXECUTE -> REPLAY -> SEAL`.
Long runtime is lawful when liveness matches the declared stage. Reuse expensive valid intermediates when lawful.

### INTEGRATE
Verify exact ancestry/diffs/jurisdiction, merge, verify resulting ancestry, run prescribed affected court, freeze successor. Semantic surprises leave integration profile.

### RECOVERY_FORENSIC
Broad reconstruction is lawful because reconstruction is the task. It must not leak back as ordinary behavior in other profiles.

## 12. Liveness: no unexplained stall

No universal stopwatch defines failure.

Each phase declares a liveness model:
- async owner status/queue/run;
- execution stage + process/resource heartbeat;
- archaeology coverage/hypothesis reduction;
- implementation diff/test movement;
- integration ancestry/merge movement.

If observed behavior no longer matches the liveness model, reassess before doing more work.

## 13. Retry law

```
RETRY DOES NOT ERASE PRIOR EVIDENCE
```

Infrastructure-transient retries are allowed when classified.
Deterministic semantic/test failures are preserved and may not be laundered by repeated runs.

Court determinism mode must be declared when material:
- `EXACT`
- `SEEDED`
- `DISTRIBUTIONAL`
- `NONDETERMINISTIC_OBSERVATIONAL`

## 14. Resume / "finish" law

A continuation such as "finish" means:

1. refresh durable project state;
2. compute:
   - `ALREADY_DONE`
   - `CURRENTLY_IN_FLIGHT`
   - `STILL_REQUIRED`
   - `NO_LONGER_REQUIRED`;
3. execute only the delta to the previously frozen terminal.

It does NOT authorize reopening settled work or inventing stronger proof criteria.

## 15. Closure law

When all terminal claims are proven:

```
ALL_TERMINAL_CLAIMS_PROVEN => CLOSURE_ONLY
```

Legal closure actions:
- capture exact evidence refs;
- clean explicitly temporary state;
- write the required bounded return;
- issue the terminal;
- report exact terminal SHA/path.

No new archaeology, testing, redesign, or proof strengthening.

Semantic proof and repository hygiene are separate claims; do not conflate them.

## 16. Blocker taxonomy

Use a concrete blocker class:
- `BLOCKED_AUTHORITY`
- `BLOCKED_SEMANTIC_CONTRADICTION`
- `BLOCKED_EXECUTION_CAPABILITY`
- `BLOCKED_MATERIAL_UNAVAILABLE`
- `BLOCKED_RESOURCE`
- `BLOCKED_INTEGRATION`
- `BLOCKED_INSUFFICIENT_EVIDENCE`

Also permit non-blocking handoff states:
- `PENDING_EXTERNAL`
- `NEEDS_HQ_DECISION`

Do not call an active external dependency a blocker merely because it is not finished yet.

## 17. Context discipline

Every handoff should distinguish:
- `MUST_READ`
- `REFERENCE_IF_NEEDED`
- `FROZEN_FACTS_DO_NOT_REPROVE`
- `OPEN_QUESTIONS_ONLY`
- `FORBIDDEN_TO_REOPEN`

A frozen input fact may be challenged only by direct contradictory evidence.

## 18. Critical-path law

Optimize the path to the next authoritative project state, not worker utilization.

Every substantial action must either:
- advance the critical path; or
- protect its correctness.

Off-critical-path activity is not progress merely because tools are busy.

## 19. Incident regression: GT12 I03 scale-equivalence finish turn

The following behavior is explicitly forbidden:

1. exact-SHA CI is dispatched;
2. an immediate empty/lagging status observation is treated as CI failure;
3. a second trigger/branch/PR is created;
4. a local repository is manually reconstructed to rerun the same proposition;
5. the primary court becomes green;
6. fallback continues anyway;
7. worker emits a stale blocker from incomplete local evidence.

Correct behavior:
`DISPATCH -> TRACK OWNER -> WAIT/OBSERVE -> GREEN -> CLOSURE_ONLY`.

## 20. Adoption boundary

This document is governance candidate infrastructure until explicitly adopted by Vozhd/HQ.

Its existence does not itself:
- move main or PRE-MAIN;
- change empirical/semantic authority;
- alter GT12 candidate semantics;
- convert worker PASS into project acceptance.

## 21. Exceptional-task escape hatch

This constitution is not permitted to force a lawful but genuinely unmodeled task into a false profile or claim shape.

If the current task cannot be represented without distortion:

1. do not fabricate compliance;
2. enter `NEEDS_HQ_DECISION`;
3. name the exact rule/schema mismatch;
4. HQ may issue either:
   - a schema/governance revision; or
   - a one-time exact waiver naming the task, the waived protocol rule(s), permitted actions, expiry/terminal boundary, and non-waived authority limits.

A waiver is orchestration-only. It may not widen empirical, semantic, PRE-V3, V3, V2, source, Library, branch, or adoption authority beyond the underlying handoff.

A worker operating under a waiver must cite it in the return. Silent validator bypass is forbidden.

```
UNMODELED_LAWFUL_TASK != FORCE_INTO_WRONG_PROFILE
EXPLICIT_HQ_WAIVER != SILENT_PROTOCOL_BYPASS
```

## 22. REAL_EXECUTION write-ahead checkpoint law

REAL_EXECUTION workers must not treat the final terminal commit as the first durable project write.

When a stage produces a result whose recomputation is expensive, fragile, source/material dependent, or likely to exceed a later tool/execution window, that result must be made durable before another expensive stage begins.

```
EXPENSIVE_OR_FRAGILE_RESULT_PRODUCED
+ NOT_YET_DURABLE
=> NEXT_LEGAL_ACTION = PERSIST_CHECKPOINT
```

```
VOLATILE_RESULT + HIGH_RECOMPUTE_COST => CHECKPOINT_NOW
PROCESS_LOSS MUST NOT FORCE REEXECUTION OF A PROVEN EXPENSIVE STAGE
NONTERMINAL_CHECKPOINT != PROJECT_ACCEPTANCE
```

A durable checkpoint may be:
- a Git commit on the worker branch containing bounded evidence/payload material;
- an immutable content-addressed artifact with a recorded ref/hash and retrieval path available to the next turn;
- another explicitly governed durable execution artifact.

A local-only workspace path such as `/mnt/data/...` is volatile project state unless it is subsequently banked or referenced by an immutable artifact accessible after worker/tool loss.

For staged REAL_EXECUTION, prefer:

`MATERIALIZE -> CHECKPOINT`

`HASH_VERIFY/PROJECT/VALIDATE -> CHECKPOINT`

`INDEX/EXECUTE -> CHECKPOINT ACTUAL OBJECT IDENTITIES`

`EXTRACT -> CHECKPOINT PAYLOAD/MANIFEST`

`SEAL -> TERMINAL RETURN`

Checkpoint granularity is cost-sensitive. Cheap deterministic intermediates need not be persisted merely to create Git noise. Persist when recomputation/materialization is expensive, fragile, identity-bearing, or execution-window-sensitive.

### Atomic persistence

When a checkpoint consists of many already-prepared files/shards, prefer one bounded atomic Git object update:

`CREATE BLOBS -> CREATE TREE -> CREATE COMMIT -> UPDATE WORKER REF ONCE`

rather than a long sequence of individual file commits whose partial completion can exhaust the remaining execution window.

### Resume law

On `finish` or recovery:
1. inspect durable checkpoints first;
2. inspect already-prepared volatile workspace artifacts if still available;
3. verify their recorded hashes/identities;
4. persist them before any re-execution;
5. re-run an expensive stage only if the required result is genuinely unavailable or incompatible.

```
PREPARED_PAYLOAD_AVAILABLE => PERSIST_BEFORE_REEXECUTE
DURABLE_COMPATIBLE_CHECKPOINT_AVAILABLE => REEXECUTION_FORBIDDEN
```

### Persistence failure

If a result has been proved locally but cannot be persisted before the execution surface closes, the worker must report the exact volatile artifact set and enter a persistence-recovery state. A continuation is then `CLOSURE/PERSISTENCE_ONLY`, not a fresh REAL_EXECUTION authorization.
