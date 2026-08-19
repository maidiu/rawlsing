# D15 — MATERIALIZATION AND CACHE POLICY

## 1. Policy selection

D15 selects:

`C11_CANONICAL__EXACT_REPLAY_DEFAULT__BOUNDED_IDENTITY_EXACT_CACHES_OPTIONAL__CACHE_NEVER_AUTHORITY`

The policy optimizes repeated exact work without narrowing D12's future-authorized query/discovery frontier.

## 2. Universal cache key law

Every cache entry is keyed by all semantic dimensions that can change the answer, including as applicable:

- C11 semantic content identity;
- EmpiricalUniverse ID(s);
- target question/component tuple and arity;
- exact predicate AST/hash;
- risk-set/routing/applicability identity;
- response topology/domain identity;
- raw/governed measure and weight basis;
- time/geography/source scope;
- authority snapshot IDs/versions/hashes;
- uncertainty method identity;
- comparator receipts/rules;
- discovery algorithm/coverage identity;
- structural admission identity.

If any required dimension differs, it is a cache miss.

## 3. Cache authority law

1. Cache content is never the sole durable authority for a D12 terminal distinction.
2. Cache miss falls back to exact C11 replay.
3. Cache eviction cannot make a lawful future query impossible.
4. Cache presence cannot authorize a query or downstream use.
5. Stale cache identity produces miss/invalidation, not silent reuse.
6. No cache may repair missing C11 information.

## 4. Fixed E1 cache

**Object:** exact unary/conditional EmpiricalFact.

**Class:** optional bounded cache.

**Justification:** repeated identical predicate/target grouping may avoid respondent scans.

**Semantic key:** exact query spec + C11/authority identities.

**Invalidation:** any target, predicate, risk set, topology, source, measure, weight authority, C11 content or method version change.

**Miss:** exact query engine.

**Authoritative:** never.

## 5. Fixed E2 / J-way cache

**Object:** complete exact pair/J-way contingency.

**Class:** optional bounded cache; high potential value for repeated expensive joints.

**Justification:** avoids repeated same-respondent J-way binding for an exactly matching query.

**Boundary:** answers only its exact condition/target/risk-set/scope/topology/measure identity. It cannot be reconditioned on a new coordinate or risk set.

**Invalidation/miss/authority:** same rules as E1.

## 6. Branch predicate/member cache

**Object:** exact member set for a DiscoveryResultReceipt branch.

**Class:** optional cache.

**Justification:** avoids repeated branch predicate evaluation before branch-conditioned queries.

**Key:** C11 identity + exact branch predicate/ancestry + DiscoveryAuthority + algorithm/coverage identity.

**Invalidation:** any branch predicate, source/risk-set, authority, C11 content or discovery-version change.

**Miss:** deterministic branch membership replay from C11.

**Authoritative:** branch receipt/predicate/replay law is canonical; member set cache is not.

## 7. Actor comparator receipt cache

`ActorComparatorReceipt` is canonical when it is part of a durable reverse-field/history record; otherwise identical resolution may be cached.

**Key:** actor objective fact refs/hashes + effective time + comparator authority + source/coordinate identity.

**Invalidation:** actor fact mutation/new effective value, comparator rule/crosswalk version, source semantic version/time scope change.

**Miss:** exact ActorComparabilityService.

## 8. Temporal/source component fact cache

Per-wave/source exact EmpiricalFacts may be cached when repeated temporal or cross-universe comparisons reuse them.

They remain source-indexed. A cache may not collapse multiple universes into one aggregate key.

## 9. Positioned-subject possibility-field cache

**Object:** exact source-indexed field for one exact actor-fact/comparator/query/source identity.

**Class:** optional cache.

**Justification:** repeated V3/runtime access can avoid rebuilding exact J-way field.

**Invalidation:** any actor objective fact/effective time, comparator, source applicability, target/query, C11 content, measure, uncertainty authority change.

**Miss:** PossibilityFieldService exact rebuild.

**Authoritative:** semantic field is canonical; the cached physical copy is not the durable empirical authority and may be regenerated.

## 10. Structural admission cache/materialization

`StructuralEmpiricalAdmission` is a durable canonical receipt when used by structural production. Its underlying EmpiricalFact may remain derivable unless repeated workload justifies a fixed fact cache.

V553 must be able to replay the admission's empirical input from C11 if its local cached fact disappears.

## 11. E3 / E4

E3 cloud/network and E4 scalar association metrics are `DIAGNOSTIC_ONLY` cache classes.

They may be retained for navigation, authoring, debugging or discovery proposal heuristics, but:

- they are evictable;
- they cannot serve as deep empirical authority;
- structural/reverse uses must reference exact underlying EmpiricalFact;
- deleting them must not affect AT01–AT19 terminal behavior.

## 12. Current answer/country distributions

During migration these may remain materialized for compatibility with current structural consumers.

Target policy:

- answer distribution: derive on demand, optionally cache hot identities;
- country distribution: optional cache because current structural/temporal consumers may repeat stable source scopes.

Compatibility materialization is retired only after structural-admission parity gates pass.

## 13. Checkpointing

Checkpoint/restart artifacts are operational, not semantic authority, unless a particular receipt is required for historical deterministic replay.

D15 does not mandate the current per-question checkpoint amplification. Target checkpoint granularity is implementation-time policy constrained by:

- restart correctness;
- deterministic replay;
- no lost canonical receipt;
- no change in discovery coverage from resume.

## 14. Physical indexing

Indexes, projections, inverted maps, respondent→event adjacency, question→event partitions and coordinate→respondent indexes are permitted noncanonical accelerators.

They must be exactly rebuildable from C11 and authority manifests. D15 does not select a database-specific index family because D14 live selectivity/cardinality is unknown.

## 15. Cache tuning after implementation

D14 leaves hit rates/query mixes unknown. Therefore initial implementation should expose instrumentation for:

- cache hit/miss by semantic object class;
- build/replay cost;
- bytes;
- invalidation frequency/reason;
- cold/warm W01–W17 latency;
- stale-key prevention.

Operational policy can tune thresholds after measurement without changing semantic architecture.

## 16. Source snapshots are not cache

Source/native snapshots remain a safety/evidence retention layer until source→C11 equivalence is positively certified. They are not evictable under ordinary cache policy.

## 17. Final cache theorem

The target can cache expensive exact facts aggressively where real reuse justifies it because the cache boundary is narrow and identity-exact.

It does not need to preserve the present broad artifact suite merely to obtain speed.

`CACHE != AUTHORITY` and `CACHE MISS -> EXACT C11 REPLAY` are binding invariants.
