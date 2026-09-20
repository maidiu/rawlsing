# FIABC-W3-Q01 — Integrated Acceptance Criteria

These criteria are review law for the Wave-3 fan-in. They do not create semantic authority and they do not prescribe sibling module names. An integrated implementation may expose equivalent evidence through its own receipts, but every criterion below must be decidable from exact, replayable evidence.

## A. Diagnostic successor (I01)

PASS requires all of the following:

- every quantitative diagnostic output is explicitly diagnostic-only and has a product identity distinct from `EmpiricalFact@1.0.0`;
- no diagnostic code path mints or mutates an `EmpiricalFact`, an `AuthoritySnapshot`, a `DiscoveryAuthority`, or `StructuralEmpiricalAdmission`;
- diagnostic score/value cannot prune, add, remove, reorder for reachability, or otherwise control the exact I05 frontier;
- diagnostic score/value cannot satisfy structural admission or semantic interpretation authority;
- exact product identity binds the exact input facts, queries, C11/releases, authority closure, replay determinants and algorithm/formula identity;
- unavailable, noncomparable, underpowered, invalid, unresolved and not-applicable states survive as typed states; they are not upgraded to `SUPPORTED` because a scalar can be computed.

Mandatory negative fixtures: `Q01-DIAG-001` through `Q01-DIAG-004`.

## B. Effective-N successor (I02)

PASS requires:

- numeric effective-N exists only when an exact weight is positively authorized at the same joint/risk-set/query scope;
- the result binds exact authorized weight identity, design authority, estimand authority, `sum_w`, `sum_w2`, scope and replay identity;
- no field name, label, frequency, availability, candidate convenience, or respondent count selects a weight;
- RAW/unweighted workloads retain `NOT_APPLICABLE` / `WEIGHT_NOT_AUTHORIZED` (as exact current law requires) and no numeric effective-N;
- invalid weights, zero/degenerate sums, mismatched scope, missing authority or inferred/default weight fail closed.

Mandatory fixtures: `Q01-NEFF-001` through `Q01-NEFF-004` plus both PASS controls.

## C. Candidate C production binding (I03)

PASS requires:

- candidate identity and frozen owner policy remain C, including the zero-accelerator physical state;
- semantic execution converges to the common C11/I03/I05 core without moving ownership into Candidate C;
- accelerators are optional and nonauthoritative;
- LiTS accelerator names are a subset of `{CACC1,CACC2}` and only their frozen scope can use them;
- WVS7 has zero applicable accelerators;
- CACC3 does not exist in the implementation, config, receipt or fallback table;
- LiTS q310 and q311 remain in the workload and use exact-source-backed realization when outside accelerator scope;
- no current-tree Candidate-B facade is substituted for the frozen Candidate-C experimental identity.

Mandatory fixtures: `Q01-CANDC-001` through `Q01-CANDC-005` plus LiTS/WVS PASS controls.

## D. Runtime packaging rebind (I04)

PASS requires exact content identity for the four bounded packaging repairs:

- LiTS R6S materializer blob `9406bacfd928393f6a159a46216aa1f7ec129f34`;
- Node4A carrier blob `504944f9533b7385d201076e2e834b8a9446dee8`;
- WVS runtime package blob `e04e84b76f8b4eb53905276dd025938bf2e5f6fe`;
- WVS projection materializer blob `11b28416aac5a4899706150721f2f8ac8bb6ee43`.

Also required:

- frozen candidate owner commit remains `0b96b8de9aac774566f872cf0630ebd4ddeb70e6` where that identity defines the experiment;
- frozen B owner blob `7c509c2098d0030f253344eb3f682471378812a8` is not replaced by current-tree facade blob `c3647800f52fa81fdef34be6692207e092c48ee2` merely because the latter is convenient;
- lawful immutable historical authority/replay roots remain resolvable and are not rejected solely because they are historical paths;
- rebinding does not re-adjudicate or move source semantics.

Mandatory fixtures: `Q01-PKG-001`, `Q01-PKG-002` and PASS control.

## E. Independent parity oracle (I05)

PASS requires:

- oracle freeze precedes candidate start/output;
- freeze receipt proves `candidate_outputs_seen = 0` and no candidate-owned roots were consulted;
- expected truth origin is exact source + frozen candidate-neutral authority/common semantic producers, or accepted immutable LiTS prior truth plus current candidate-neutral exact refs where Wave-2 allows it;
- oracle dependency closure contains no candidate output/repository/cache/session/transformed carrier;
- candidate output cannot fill a missing expected field after freeze;
- pairwise A/B/C equality and same-candidate self-replay are corroboration only, never the independent oracle;
- full fixed frontier, typed states, ExactRefs, learned-product identity, replay and authority closure are compared; partial frontier or collapsed negative states cannot PASS;
- oracle identity remains immutable after candidate execution begins.

Mandatory fixtures: `Q01-ORACLE-001` through `Q01-ORACLE-003` and PASS control.

## F. Equal-work instrumentation (I06)

PASS requires:

- six source×candidate cells have distinct fresh process lifecycles where they are executed; stopped cells preserve typed unreached telemetry rather than numeric zeros;
- each candidate starts with no reachable prior-candidate `_SESSIONS`, scratch/durable state or RSS history, except explicitly retained same-candidate warm state within the same lifecycle;
- RSS is candidate-process-local;
- canonical metrics are immutable/write-once, with per-phase values separately named;
- candidate-total and phase CPU accounting does not double-count overlapping intervals;
- uncaptured telemetry is typed `MEASUREMENT_NOT_CAPTURED`/lawful null, never synthetic numeric zero;
- read/write/rewrite bytes are observed event counters; endpoint size remains a state-size measure only;
- scratch is a high-water observation;
- rebuild/invalidation/stale/corrupt/interruption fields require actual exercised lifecycle actions and post-action parity, not formula-assigned or law-string surrogates.

Mandatory fixtures: `Q01-METRIC-001` through `Q01-METRIC-005` and PASS control.

## G. Mechanized succession preflight (I07)

PASS requires every comparison-required obligation row to close:

`accepted authority -> current authoritative owner -> executable binding -> live governed consumption -> invariant/cost classification`.

Repository presence, importability, a worker-return copy, or a historical receipt cannot substitute for the live edge when live consumption is required. PASS also requires closed negative-state law, source×candidate capability, independent oracle and equal-work accounting; illegal preterminal deferral blocks.

Mandatory fixture: `Q01-PREFLIGHT-001` and PASS control. B05's own blocker replay suite remains additionally required after fan-in.

## H. Final I05 terminal verifier (I08)

A court PASS is accepted only when the terminal is:

`GOVERNED I05 LEARNED EMPIRICAL PRODUCT + EXACT SEMANTIC / REPLAY / OUTPUT IDENTITY + COVERAGE + CONSTITUENT I03 FACT CLOSURE`.

Required inputs include succession-preflight PASS, independent-oracle PASS and terminal receipts for all admitted source×candidate cells. C11 and I03 must pass as intermediate invariants but neither may be treated as the final successful terminal. Later lifecycle work must reproduce the same terminal identities.

Mandatory fixtures: `Q01-TERM-001`, `Q01-TERM-002` and PASS control.

## Global acceptance rule

The integrated tree is not qualified for local materialization or measured P2X merely because these return-local fixture tests pass. Qualification requires both:

1. this contract's negative fixtures reject exactly as specified and positive controls pass; and
2. the real integrated sibling outputs/receipts are projected into the same evidence dimensions and pass every applicable criterion above, with their own focused unit/integration tests green.

Any unresolved field is a BLOCK at that grain. No warning/partial PASS converts unresolved semantics, parity, accounting, capability, coverage or terminal identity into a measured comparison authorization.
