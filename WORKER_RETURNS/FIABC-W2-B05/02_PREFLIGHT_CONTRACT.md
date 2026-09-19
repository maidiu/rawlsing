# FIABC-W2-B05 — Succession Preflight Contract

Contract ID: `RAWLSING_FIABC_SUCCESSION_PREFLIGHT@1.0.0`

Schema: `RAWLSING_FIABC_SUCCESSION_MANIFEST@1.0.0`

## Purpose

This preflight is the mechanical gate between accepted functional-inheritance law and any measured P2X result that HQ might later treat as architecturally dispositive.

It does not create semantic authority, choose the comparison boundary, repair Candidate C, define a new parity oracle, or settle the measurement constitution. Those burdens remain with their competent courts. The preflight only asks whether the exact outputs needed from those courts have been supplied and whether the executable graph demonstrably consumes them.

The governing chain is mandatory at the exact comparison-required function grain:

`inherited obligation -> accepted authority -> current authoritative owner -> executable binding -> live consumer -> A/B/C invariant + cost class`.

A repository file, historical carrier, accepted doctrine, or current module by itself cannot satisfy more than its own node in that chain.

## Input freeze

Before candidate measurement begins, the court must freeze one manifest instance that validates against `01_SUCCESSION_MANIFEST_SCHEMA.json` and record its content SHA-256.

The freeze must identify:

- exact source set and source identities;
- exact candidate set;
- exact claim/workload scope;
- exact comparison terminal and boundary adjudication;
- exact candidate-neutral upstream producer outputs;
- exact function-chain rows required before the terminal;
- exact A/B/C invariants;
- exact source×candidate capability dispositions;
- exact independent parity-oracle material;
- exact measurement/accounting constitution.

Candidate output may not rewrite any of those expected-truth or accounting definitions.

## Evidence classes

The preflight distinguishes evidence instead of silently harmonizing it:

- `ACCEPTED_AUTHORITY`: competent semantic or governance authority;
- `CURRENT_IMPLEMENTATION`: code/resource that is the current owner or binding at the pinned ref;
- `HISTORICAL_EVIDENCE`: genealogy or old execution evidence, never current authority by mere survival;
- `GOVERNED_EXECUTION_RECEIPT`: live execution evidence from the exact code/ref under review;
- `ACCEPTED_WORKER_RETURN`: a bounded accepted worker finding;
- `COURT_ADJUDICATION`: a competent court decision;
- `MEASUREMENT_CONSTITUTION`: the accepted equal-work/accounting definition;
- `BOUNDARY_ADJUDICATION`: the accepted comparison-cut decision.

A worker claim can direct the preflight to evidence, but cannot be promoted into a stronger evidence class without an exact adopted ref.

## Deterministic check sequence

### P00 — Schema and manifest identity

PASS requires:

- JSON Schema validation;
- frozen manifest content hash recorded before candidate execution;
- all evidence refs contain a repository path, supplied ref, and resolved commit SHA;
- optional Git blob/content hashes match when declared.

BLOCK codes:

- `PF_SCHEMA_INVALID`
- `PF_MANIFEST_NOT_PREOUTPUT_FROZEN`
- `PF_REF_UNRESOLVED`
- `PF_REF_CONTENT_MISMATCH`
- `PF_FLOATING_OR_FUZZY_REF`

### P01 — Comparison boundary and function inclusion

PASS requires an accepted boundary adjudication and a complete disposition for every inherited function relevant to the claim scope.

For each function, exactly one must hold:

1. `REQUIRED_BEFORE_TERMINAL`; or
2. `INTENTIONALLY_DEFERRED_BEYOND_TERMINAL` with exact deferment authority tied to the chosen boundary.

`UNRESOLVED_BOUNDARY` cannot PASS.

BLOCK codes:

- `PF_COMPARISON_TERMINAL_UNRESOLVED`
- `PF_OBLIGATION_UNMAPPED`
- `PF_DEFERMENT_UNPROVED`

### P02 — Accepted semantic/manual authority

For every required function, all semantic propositions used by the executable graph must resolve to exact accepted authority whose scope matches the source, object, operation, and target use.

Presence of a label, source field, empirical pattern, historical carrier, or mechanically binder-valid value cannot substitute for authority.

BLOCK codes:

- `PF_AUTHORITY_MISSING`
- `PF_AUTHORITY_SCOPE_MISMATCH`
- `PF_AUTHORITY_AMBIGUOUS`
- `PF_SEMANTIC_INFERENCE_SUBSTITUTION`

If `GENUINELY_MISSING` is asserted, the manifest must show that historical accepted authority, another current owner, a disconnected exact binding, a superseded implementation, and intentional deferral were checked first.

Additional BLOCK code:

- `PF_MISSINGNESS_NOT_FALSIFIED_FIRST`

### P03 — Current authoritative owner / anti-resurrection

The current-owner node must identify a current owner at the exact pinned ref and must carry currentness evidence.

A historical or superseded implementation may remain useful evidence, but it cannot satisfy this slot.

BLOCK codes:

- `PF_CURRENT_OWNER_UNRESOLVED`
- `PF_OWNER_SUPERSEDED_OR_HISTORICAL`
- `PF_OWNER_AUTHORITY_JURISDICTION_MISMATCH`

### P04 — Executable owner-to-consumer binding

PASS requires a concrete binding from the current owner to the named consumer entrypoint plus a contract-level receipt proving the bound object is accepted by the production consumer shape.

Module presence, importability elsewhere, or a worker-return copy does not prove this edge.

The check must detect:

- missing fan-in;
- stale path binding;
- producer/consumer schema mismatch;
- wrapper shadowing/recursion;
- substitution of a fixture for a production object.

BLOCK codes:

- `PF_EXECUTABLE_BINDING_MISSING`
- `PF_BINDING_REF_STALE`
- `PF_BINDING_OWNER_MISMATCH`
- `PF_PRODUCER_CONSUMER_CONTRACT_MISMATCH`
- `PF_WRAPPER_SHADOWS_CURRENT_OWNER`
- `PF_SYNTHETIC_FIXTURE_SUBSTITUTION`

### P05 — Live governed consumption

Static reachability is necessary but not sufficient.

For every required function whose court claim depends on live execution, PASS requires a governed receipt from the exact execution code commit showing the named consumer reached and consumed the bound current owner.

The receipt must be after all repairs declared prerequisite for that court run. A receipt from an older branch/tip cannot validate newer wiring.

BLOCK codes:

- `PF_LIVE_CONSUMER_DISCONNECTED`
- `PF_LIVE_RECEIPT_MISSING`
- `PF_LIVE_RECEIPT_CODE_REF_MISMATCH`
- `PF_LIVE_RECEIPT_PREDATES_REQUIRED_REPAIR`

### P06 — Negative-state and provenance conservation

PASS requires explicit law and live preservation for all claim-relevant distinctions, including where applicable:

- physical missingness versus semantic response state;
- routing unknown versus inapplicable versus nonmember;
- governance BLOCKED versus empirical values;
- typed UNKNOWN versus Python absence;
- all-missing versus empty versus unsupported topology;
- source-local unresolved relation versus inferred equivalence;
- `VALID_EMPTY` versus unavailable/unresolved/integrity failure;
- `DENIED`/`NONCOMPARABLE` versus ordinary scalar value.

Replay/provenance closure must retain exact source, authority, dependency, and result identities required by the comparison terminal.

BLOCK codes:

- `PF_NEGATIVE_STATE_LAW_UNRESOLVED`
- `PF_NEGATIVE_STATE_COLLAPSE`
- `PF_REPLAY_PROVENANCE_UNCLOSED`
- `PF_AUTHORITY_CLOSURE_UNPROVED`

### P07 — A/B/C invariant closure and independent parity oracle

Every invariant marked as cross-candidate must be PROVED at the selected comparison terminal.

The oracle must be candidate-neutral and frozen before candidate output. Executing the same candidate twice and comparing it with itself is repeatability evidence, not an independent parity oracle.

BLOCK codes:

- `PF_ABC_INVARIANT_UNRESOLVED`
- `PF_ORACLE_NOT_PREOUTPUT_FROZEN`
- `PF_ORACLE_DERIVED_FROM_CANDIDATE_OUTPUT`
- `PF_SELF_REPLAY_USED_AS_PARITY`
- `PF_FIXED_FRONTIER_UNRESOLVED`

### P08 — Source×candidate production capability

For each in-scope source×candidate cell, the manifest must identify the lawful capability contract and the production realization that can execute it.

A synthetic fixture, test-only determinant, partial preimage set, or another source's accelerator cannot be treated as production qualification.

A cell with genuine missing capability remains a typed blocker unless a competent scope court proves the candidate is lawfully outside the experiment and the court definition is updated before measurement.

BLOCK codes:

- `PF_SOURCE_CANDIDATE_CAPABILITY_MISSING`
- `PF_SOURCE_PORTABILITY_UNPROVED`
- `PF_PARTIAL_PREIMAGE_SET`
- `PF_UNAUTHORIZED_NOT_APPLICABLE_ESCAPE`

### P09 — Equal-work and cost-accounting closure

Semantic truth ownership and cost ownership are separate required fields.

PASS requires the accepted measurement constitution to prove:

- exact candidate-local start/stop boundaries;
- symmetric preserved-work treatment;
- candidate-isolated wall/CPU/memory accounting;
- observed I/O/bytes semantics where claimed;
- symmetric cold/warm/rebuild/invalidation/interruption definitions;
- no process-global RSS carryover treated as candidate-local;
- no overwritten terminal metric used as the intended accumulated/cold value;
- identical metric method identity across A/B/C for fields being compared.

Documentary formulas or law hashes may be retained as evidence but cannot be mislabeled as observed candidate work.

BLOCK codes:

- `PF_EQUAL_WORK_ACCOUNTING_UNRESOLVED`
- `PF_SEMANTIC_COST_OWNERSHIP_CONFLATED`
- `PF_CANDIDATE_START_STOP_UNRESOLVED`
- `PF_PRESERVED_WORK_ASYMMETRIC`
- `PF_METRIC_NOT_CANDIDATE_LOCAL`
- `PF_METRIC_METHOD_MISMATCH`
- `PF_METRIC_OVERWRITTEN`
- `PF_DOCUMENTARY_VALUE_MISLABELED_OBSERVED`

### P10 — Failure-scope and lifecycle integrity

Common infrastructure, source-wide, candidate-local, and court-wide failures must retain their correct scope. A common infrastructure failure cannot become evidence against only the candidate that happened to encounter it first.

Lifecycle receipts must show verifier and stage sequencing consistent with the accepted state machine.

BLOCK codes:

- `PF_FAILURE_SCOPE_AMBIGUOUS`
- `PF_FAILURE_SCOPE_MISCLASSIFIED`
- `PF_LIFECYCLE_ORDER_MISMATCH`
- `PF_TERMINAL_HISTORY_STALE_FOR_RETRY`

## PASS law

The only PASS condition is:

1. P00-P10 all PASS for the exact frozen claim scope;
2. every required function chain reaches a LIVE consumer at the required grain;
3. every deferred function has competent boundary authority;
4. no source×candidate cell is silently omitted;
5. all cross-candidate invariants and the independent oracle are closed;
6. equal-work accounting is closed by the competent measurement court.

There is no partial or warning PASS. Unresolved proof state is a BLOCK at the exact unresolved grain.

## Output

A conforming evaluator emits a deterministic check list with one status per check plus exact evidence refs and one overall status:

- `PASS`, only when every normative check passes; or
- `BLOCK`, with one or more failure codes above.

The evaluator must not auto-repair, mint authority, change comparison scope, infer a missing relation, or rewrite candidate/accounting semantics.
