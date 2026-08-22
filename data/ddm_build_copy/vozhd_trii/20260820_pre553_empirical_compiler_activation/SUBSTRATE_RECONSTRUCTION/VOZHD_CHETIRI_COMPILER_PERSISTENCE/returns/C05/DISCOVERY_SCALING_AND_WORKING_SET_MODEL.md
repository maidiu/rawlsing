# DISCOVERY SCALING AND WORKING-SET MODEL

## Status

This is a **lawful analytical model, not a measured production benchmark**. A concrete production grammar/frontier was not frozen, so C05 does not invent candidate counts or wall times.

## Symbols

- `R`: respondents in the governed risk universe.
- `Q`: decoded source questions/variables.
- `A`: exact predicate atoms in the discovery grammar.
- `T`: exact query templates.
- `K`: maximum conditioner arity.
- `J`: maximum target arity.
- `B`: governed recursive branch depth/branch count, if present in the grammar.
- `U`: separate source-universe/time scopes.
- `C`: compiled candidate count.
- `E`: total exact I03 query executions after within-session exact-key reuse.
- `D(R,Q)`: one frozen source decode/traversal cost.

## Candidate-growth surfaces

The exact engine expands authority-declared rules. Depending on grammar form, candidate growth includes:

- `SINGLE_ATOM`: O(A)
- `AND_COMBINATIONS`: `sum_{k<=K} choose(A,k)` over the declared atom set
- `AND_CARTESIAN_GROUPS`: product of declared group cardinalities
- `XOR_EXACTLY_ONE_COMBINATIONS`: combinatorial in the declared atom set/arity
- `BASE_QUERY` with enumerated target cells: proportional to governed cell-domain size
- `JOINT_DEPENDENCE`: governed joint template plus its marginal template set
- `REVERSAL_GRID`: exposure-positive × exposure-negative × declared strata × target templates
- recursive subgroup/branch families: additional candidates only where the pre-search grammar explicitly enumerates the branch ancestry/frontier; current exact I05 does not adaptively grow the frontier from scores.

Thus the engine is **exact-bounded, not globally finite by schema alone**. The actual `C` is known only after a concrete authority/grammar instance is supplied and compiled.

## Native-reread pathology

A naive source-backed implementation that reopens/decodes SAV/DTA for each exact query has a worst physical shape near:

`COST_NATIVE_REREAD ≈ E * D(R,Q)`

and can become pathological long before the semantic frontier is exhausted.

This is exactly why C03 selected-column timings cannot establish I05 feasibility: I05 may generate many repeated baselines, conditioned variants, joint cells, and branch-scoped queries.

## One-session decoded image

A lawful session can amortize decode:

`COST_SESSION ≈ D(R,Q) + BUILD_STATE + EXECUTE(E,R)`

where `BUILD_STATE` may contain exact typed state vectors, risk-set vectors, topology occurrence maps, respondent identity, and optional predicate masks. This state is execution-only if it is exactly rebuildable from immutable source + governed authority.

Deletion of the session image is lawful only if rebuilding it yields the same:

- predicate membership;
- target cell topology;
- raw/weighted support;
- candidate identities;
- terminal coverage states;
- frontier/completeness receipt;
- replay identity.

C05 could not run this deletion experiment because no production program instance/source-backed facade is frozen at launch.

## Bitmap/mask law

Bitmaps can make exact conjunctions and complements close to word-parallel operations, but a mask is safe only as a projection of richer governed state. Required noncollapse includes:

- respondent identity;
- eligible/routed risk universe;
- MISSING/DK/REFUSAL/IAP/NOT_ASKED and other typed states;
- zero support versus observed zero;
- zero/one/many occurrence topology;
- order/rank/repeated/MR identity;
- source-universe/time identity;
- raw versus governed-weighted measure basis.

A finite bitmap catalog must never become the set of questions I05 is allowed to ask. Uncached lawful predicates require an exact scan/reconstruction fallback.

## Repeated sessions

Three regimes are distinct:

1. **cold/no cache:** raw source decode + exact state rebuild + frontier execution;
2. **warm transient session:** one decode reused across all candidates in one run;
3. **regenerable cross-session cache:** optional exact-key indexes/masks reused only if keyed to immutable source/release/authority/grammar identities and delete-safe.

The court needs measured cold/warm/rebuild runs after a concrete frontier is frozen. None is lawfully available yet.

## Exhaustive absence

Exact negative is not “no candidate found before time ran out.” For current exact I05 it requires:

- one exact declared frontier ref/hash;
- `candidate_count == covered_candidate_count`;
- every candidate in a terminal typed coverage state;
- exact replay and authority closure.

That completeness material is small canonical/replay state relative to a full event carrier and must be retained independently of acceleration choices.

## Performance evidence required to close C05 later

For at least one pinned SAV and one pinned DTA production program session, record:

- compiled `C`, candidate families, K/J, branches, universes/time scopes;
- exact I03 query count before/after within-session reuse;
- source opens and decoder invocations;
- cold, warm, repeated, and delete/rebuild wall/CPU time;
- current/peak RSS;
- scratch peak and optional cache size;
- exact parity of facts, receipts, frontier hash and replay identity;
- whether any native reread occurs after session-image build;
- cleanup and cache deletion witness.
