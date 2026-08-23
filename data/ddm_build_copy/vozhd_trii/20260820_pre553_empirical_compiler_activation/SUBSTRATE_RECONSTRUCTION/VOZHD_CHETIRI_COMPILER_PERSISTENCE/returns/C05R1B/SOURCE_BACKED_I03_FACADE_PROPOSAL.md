# C05-R1B — Source-Backed I03 Facade Proposal

State: `PROPOSAL_SEAM__C04_SOURCE_BACKED_EXECUTABILITY_CARRIED_UNCHANGED`

This file does not implement or benchmark a facade. It states the exact semantic contract a later implementation must satisfy so the accepted I05 engine can consume source-backed I03 without making a permanent canonical event carrier a correctness dependency.

## 1. Accepted source-backed foundation

Carried as authoritative prior result:

`C04_PASS__FULL_I03_FRONTIER_SOURCE_BACKED_EXECUTABLE`

C04 established that every frozen I03 logical/public primitive is exactly source-backable through carrier-neutral C11 using exact source truth plus governed semantic/topology/routing/weight/source-relation authority and replay receipts. No authoritative permanent full respondent/event payload table and no mandatory regenerable session materialization is required for correctness.

C04 also established that optional decoded frames, wave images, vectors, masks and similar execution images are lawful only when deterministically regenerable, fully keyed by semantic determinants, fail-closed when stale/mismatched, non-authoritative, and removable without changing truth.

## 2. Facade semantic API

A later facade implementation SHALL expose to I05 the same frozen logical inputs/outputs already consumed by `execute_empirical_query`:

Inputs:
- exact `C11LogicalRelease` ref(s);
- exact `EmpiricalPredicate@1.0.0`;
- exact `EmpiricalQuerySpec@1.0.0`;
- exact immutable `AuthorityRegistry` closure.

Outputs:
- the exact same `QueryExecutionResult` / `EmpiricalFact@1.0.0` semantic projection and ExactRefs required by frozen I03;
- exact risk-member and denominator-member identity where the current replay law requires it;
- exact typed zero/negative/unavailable/noncomparable/integrity states;
- exact replay/provenance refs independent of physical cache/layout choices.

I05 must not be able to tell, semantically, whether I03 was served from a permanent carrier, a source scan, a decoded session image, a vector cache, or a mixture of those, provided exact I03 fact/replay identity is unchanged.

## 3. Persistence/state classification

| Surface | Required class | Source-backed status | Contract |
|---|---|---|---|
| exact raw source artifact/snapshot and SHA-256 | authoritative persistent source input | `SOURCE_BACKED__ACCEPTED_C04` | Must remain reachable/verifiable by exact immutable identity; no mutable-path substitution |
| exact source-native row ordinal/respondent identity law | authoritative persistent source input / semantic side authority as applicable | `SOURCE_BACKED__ACCEPTED_C04` | Preserve source-scoped identity; row ordinal remains irreducible replay identity where no safe native respondent ID exists |
| native variable/question identity, ordering, raw typed values, native missing metadata, native topology metadata | authoritative persistent source input | `SOURCE_BACKED__ACCEPTED_C04` | Source truth only; source bytes do not acquire semantics they do not contain |
| native↔canonical question/coordinate/value/state mappings | persistent semantic/replay side material | `SOURCE_BACKED__ACCEPTED_C04` | Exact authority required where not derivable from immutable source |
| topology/component/subitem/multiplicity/order/rank/repetition authority | persistent semantic/replay side material | `SOURCE_BACKED__ACCEPTED_C04` | No scalarization, first-only selection, deduplication or order loss |
| routing/applicability/risk-set rules or exact governed membership + replay closure | persistent semantic/replay side material | `SOURCE_BACKED__ACCEPTED_C04` | Must determine eligibility independently of tested response condition/missingness |
| weight source/basis/state/design/estimand/normalization authority | persistent semantic/replay side material | `SOURCE_BACKED__ACCEPTED_C04` | No default weight=1 and no weighted→RAW fallback |
| source-universe relation/comparability/nonduplication/pooling authority | persistent semantic/replay side material | `SOURCE_BACKED__ACCEPTED_C04` | No implicit cross-universe pooling/joining |
| predicate grammar/query authority and exact target-domain authority | persistent semantic/replay side material | `SOURCE_BACKED__ACCEPTED_C04` | Required to interpret lawful query shapes and zero-cell completion |
| exact release/source/universe/replay/provenance manifests and published-output receipts | persistent semantic/replay side material | `SOURCE_BACKED__ACCEPTED_C04` | Must preserve exact replay and historical geometry |
| parser/source handle, decoded query projections, respondent streams | transient session state | `SOURCE_BACKED__ACCEPTED_C04` | May be streamed/discarded; cannot define truth |
| respondent/risk/denominator masks; predicate masks; target event gathers; weight vectors; joint accumulators | transient session state | `SOURCE_BACKED__ACCEPTED_C04` | Regenerable from source + authority; cache absence never means semantic absence |
| decoded frame/wave image, Arrow/DuckDB image, vector bundle, reusable mask bank | optional regenerable cache | `SOURCE_BACKED__ACCEPTED_C04` | Optional optimization only; exact complete invalidation key required; no-cache path remains lawful |
| exact cached I03 query results/facts | optional regenerable cache unless separately published | `R1B_PROPOSAL_SEAM` | May be reused only when exact query/predicate/release/authority/risk/measure/topology/replay identity matches; otherwise recompute |
| `DiscoveryResultReceipt` and adopted learned empirical discovery products | persistent learned product | `R1B_PROPOSAL_SEAM` | Persist exact learned result identity, dependencies, authority refs, frontier/candidate refs and replay closure; never back-promote into source truth |
| production `DiscoveryAuthority` + grammar/catalog/frontier manifest after HQ adoption | persistent semantic/replay side material | `R1B_PROPOSAL_SEAM` | Required by I05 authority-before-data; proposal is not binding until adopted |

## 4. Exact open/resolve contract

For every I03 call made by I05, the facade must:

1. resolve the exact named C11 release; never `latest`/default/fuzzy/nearest;
2. verify the exact source snapshot and source hash/retention identity;
3. resolve the complete exact predicate/query authority closure;
4. resolve exact universe, risk-set, routing/applicability, topology, target-domain and measure authority;
5. fail closed on absent/conflicting authority before fabricating any semantic result;
6. construct the governed respondent/risk universe before predicate negation or condition evaluation;
7. evaluate exact recursive predicate semantics for the same scoped respondent;
8. gather target events under exact 0/1/many topology and preserve occurrence identity/order/rank/multiplicity;
9. apply only the exact requested/authorized measure basis;
10. complete exact target domains including supported zero cells;
11. emit the same EmpiricalFact/replay identity as the accepted logical I03 executor.

Partial source reads, parser failure, stale cache, cache miss, missing routing authority or interrupted execution may never be laundered into zero support, valid empty, refutation or I05 negative coverage.

## 5. Cache identity and invalidation law

Any retained accelerator/session image must be keyed by every semantic determinant it represents. At minimum where applicable:
- exact source SHA/snapshot/release/universe ref;
- source-native identity law;
- exact question/coordinate/value/state refs;
- semantic projection authority refs;
- topology authority refs;
- routing/risk-set authority refs;
- exact predicate/query refs;
- target-domain ref;
- measure/weight/design/estimand refs;
- source-relation/composition refs;
- replay/protocol/tie-order identity.

A key mismatch means cache miss and recomputation/fail-closed handling, not best-effort reuse. Cache identity is excluded from semantic truth except where a separately governed physical audit explicitly records it.

## 6. Exact negative / NOT contract

The facade must preserve C04's governing distinction:

`GOVERNED NOT(P) = { r in exact governed risk set : P(r) is exactly false }`

It is never physical-row complement. `ROUTING_UNKNOWN`, `RULE_UNAVAILABLE`, MISSING, DK, REFUSAL, IAP and NOT_ASKED remain typed as governed. An absent physical source cell is not automatically false. A failed or incomplete scan cannot produce a negative.

I05 `COMPLETE_FOR_EXACT_DECLARED_FRONTIER` is additionally separate from any single I03 zero/negative result: the former requires terminal coverage of every frozen candidate.

## 7. Multi-universe and measure contract

The facade executes exact universes independently unless an exact positive composition/relation/nonduplication/estimand bundle authorizes a composite I03 query. It never cross-joins respondents across universes by convenience.

RAW and governed weighted/design estimands remain separate. Weight authority failure produces typed measure failure; it does not default to RAW or unit weights.

## 8. What is settled versus proposed

### Authoritatively settled before C05-R1B
- frozen I03 public/logical object families and execution semantics;
- exact source/release resolution and no mutable-latest substitution;
- source-backed executability of all frozen I03 primitives;
- no semantic requirement for a permanent full respondent/event payload table;
- no correctness requirement for a mandatory session materialization;
- semantic necessity of exact source identity plus independent semantic/topology/routing/weight/source-relation/replay side authority;
- exact negative/routing/topology/measure/multi-universe noncollapse;
- optional-cache non-authority and no-cache executability.

### Proposed here, not yet authoritative
- the exact production I05 rule profile and operation identity;
- the deterministic production atom/query catalog construction rules;
- maximal finite K/J/recursive closure;
- one-DiscoveryAuthority-per-exact-universe/release production policy;
- all-authorized-risk/all-authorized-measure/all-supported-topology production scope;
- persistence of the adopted production DiscoveryAuthority/grammar/catalog/frontier manifest as semantic/replay side material;
- persistence policy for learned I05 products/receipts beyond existing object/replay requirements;
- exact concrete facade API implementation, session layout, caching technology and performance policy.

### C01/C02/C02R2 boundary
Authority 35 places this cell after architecture closure and forbids new semantic families, causal owners, structural shortcuts or survey-to-psyche paths. This proposal therefore treats the closed compiler/discovery/learned-world lifecycle obligations carried into C05 as binding constraints, but it does **not** claim that C01/C02/C02R2 selected a physical I03 facade, cache technology, event-carrier schema, or production discovery scope. Those physical/production choices are not backfilled by inference here.

## 9. Facade acceptance oracle for C05-R2

A later source-backed facade implementation is acceptable only if, for the exact same frozen query/predicate/release/authority inputs:
- source-backed/no-cache execution yields the same exact EmpiricalFact refs and typed states as the accepted logical oracle;
- optional cache/session-image execution yields identical semantic facts/replay identity;
- cache deletion changes cost only;
- stale/tampered/mismatched cache or source/authority identity fails closed;
- routing, typed negatives, weighted estimands, topology-general events, arbitrary-arity joints and multi-universe noncollapse retain parity;
- I05 receives no physical-carrier-specific semantic vocabulary.

## 10. Result

`SOURCE_BACKED_I03_FACADE_SEMANTIC_CONTRACT_PROPOSED__NO_PERMANENT_EVENT_CARRIER_REQUIRED__IMPLEMENTATION_AND_PERFORMANCE_DEFERRED`

The facade seam is sufficiently specified for a later implementation/execution court **conditional on HQ adoption of the production rule profile**. C05-R1B itself performs no implementation or benchmark.