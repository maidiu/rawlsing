# C05-R1B — C05-R2 Execution Prerequisite Spec

Readiness state:
`C05R2_SPEC_READY__EXECUTION_NOT_AUTHORIZED_UNTIL_HQ_ADOPTS_EXACT_PRODUCTION_RULE_AUTHORITY`

C05-R2 is the downstream production-instance construction/execution court. This file does not launch it.

## 1. Hard gate: HQ adoption

Before C05-R2 may treat any production discovery program as authoritative, HQ must adopt an exact immutable rule-authority artifact that either adopts or explicitly amends `C05R1B_PRODUCTION_DISCOVERY_RULE_PROFILE@1.0.0`.

The adoption must itself bind an exact authority ref/commit and must not rely on this worker return merely being present in Git.

If HQ does not adopt a complete eleven-field profile, C05-R2 must stop before benchmark/execution with a named authority blocker.

## 2. Exact production-instance manifest required before data access

For each source-universe/release court, C05-R2 must construct and seal a machine-readable manifest containing at least:
- adopted rule-profile identity/ref/hash;
- production operation identity;
- frozen I05 algorithm identity;
- exact `C11LogicalRelease` ref;
- exact empirical-universe ref;
- exact source snapshot/retention identity and SHA-256;
- effective-time/release identity;
- complete authority-registry closure refs;
- complete risk-set ref inventory and exclusions;
- complete measure-basis/weight/design/estimand inventory and exclusions;
- complete topology inventory and exclusions;
- complete predicate-atom catalog with exact refs/kinds/ancestry/scope;
- complete query-template catalog with exact refs/target/risk/measure/topology scope;
- mechanically derived K;
- mechanically derived J;
- mechanically derived recursive-depth closure;
- complete accepted-family/form rule expansion;
- validation-kind binding per rule;
- support/uncertainty settings already authorized for the exact operation/query bundle;
- canonical candidate grammar material;
- grammar semantic hash and exact grammar ref;
- exact `DiscoveryAuthority@1.0.0` semantic projection/ref;
- exact pruning/RNG/tie-order settings;
- compiled candidate identities in canonical hash order;
- candidate count and evaluated-frontier pre-execution identity/hash;
- exact replay/provenance determinants.

The manifest must be frozen before the first observed response value is used to evaluate any candidate.

## 3. Authority preflight

C05-R2 must prove before execution:
1. `DiscoveryAuthority.typed_state == EXACT_BOUNDED_AUTHORIZED`;
2. coverage is `COMPLETE_FOR_EXACT_DECLARED_FRONTIER`;
3. candidate grammar schema is the frozen exact I05 schema;
4. grammar ref hashes the exact grammar material;
5. positive exact `DISCOVERY_FRONTIER` authority covers both DiscoveryAuthority and DiscoveryResultReceipt for the proposed operation;
6. pruning is `NONE_EXACT_EVALUATE_ALL`;
7. RNG is `NONE`;
8. tie order is `CANONICAL_CANDIDATE_HASH_ORDER`;
9. algorithm identity is `PRE553_I05_EXACT_BOUNDED_DISCOVERY@1.0.0`;
10. source/risk/measure/topology scopes contain every atom/query scope admitted by the catalogs;
11. grammar J exactly equals topology-scope J;
12. every rule validation kind is accepted and authorized;
13. no diagnostic token controls reachability or becomes validation truth;
14. no source/release/risk/measure/topology exclusion was introduced from observed data or performance measurements.

Any failure is a pre-execution authority failure, not a reason to improvise a smaller frontier.

## 4. Catalog completeness proof

C05-R2 must emit an exact catalog-construction receipt showing:
- every governed semantic object/risk/measure/topology input considered;
- eligibility or exact exclusion reason for each;
- no frequency/support/effect/diagnostic field was consulted for catalog admission;
- canonical ordering and duplicate collapse;
- deterministic derivation of K/J/depth from the sealed catalogs;
- deterministic full rule expansion across all accepted families/forms.

A source semantic object may be excluded only for a reason authorized by the adopted rule profile, such as non-finite/unresolved predicate authority, exact scope incompatibility, unsupported topology or missing positive source-composition authority.

## 5. Source-backed I03 facade gate

Before full I05 execution, C05-R2 must have an implementation that satisfies `SOURCE_BACKED_I03_FACADE_PROPOSAL.md` after HQ adoption/implementation authority.

At minimum it must demonstrate on exact frozen inputs:
- exact release/source-hash resolution with no latest/fuzzy fallback;
- source-backed/no-cache I03 parity with the accepted logical oracle;
- exact respondent/risk/denominator identity;
- typed MISSING/DK/REFUSAL/IAP/NOT_ASKED/routing states;
- governed NOT rather than physical-row complement;
- exact RAW and authorized weighted/design estimands with no fallback;
- topology-general 0/1/many event parity including order/rank/repetition;
- exact same-respondent joints/cotravel;
- exact multi-universe noncollapse/composition gating;
- exact fact/ref/replay identity;
- stale/tampered cache fail-closed behavior;
- cache deletion changes only cost, not reachable semantics.

No permanent full event payload table may be introduced as a correctness dependency merely to make the court convenient.

## 6. Freeze-before-benchmark law

Only after sections 1–5 pass may C05-R2 benchmark or execute the production frontier.

Performance measurements may include:
- atom/template/rule/candidate counts;
- grammar/frontier compile time;
- source-open/decode cost;
- number of I03 query evaluations;
- physical events/cells processed;
- peak RSS;
- scratch/disk/cache footprint;
- elapsed time;
- cacheless versus lawful regenerable-session-cache performance;
- replay cost.

Measurements may not retroactively shrink or tune the frozen frontier in the same court. If resource limits are hit, return the exact physical/resource blocker against the unchanged frontier.

## 7. Mandatory hostile preflight

Before claiming a general production execution pass, C05-R2 must re-establish that the adopted instance/generator still reaches the accepted hostile terrains:
- XOR with zero unary signal;
- Simpson reversal;
- minority/nonmodal departure;
- recursive subgroup forks with exact ancestry;
- pair/same-respondent cotravel;
- higher-order conditioner configurations;
- same-marginals/different-joint and higher-order joints;
- routing asymmetry/zero overlap;
- typed negative/special states;
- RAW versus weighted/design divergence;
- ordered/ranked/repeated topology;
- multi-universe disagreement/noncomparability;
- exact negative/coverage fail-closed behavior.

These are capability witnesses, not a substitute for exhaustive production frontier execution.

## 8. Production execution pass conditions

A successful exact production run must show:
- the execution authority/ref is exactly the pre-data frozen one;
- the evaluated frontier ref matches the pre-execution compiled frontier;
- every candidate receives an accepted terminal coverage state;
- `candidate_count == covered_candidate_count`;
- no candidate was skipped due to score, support, prevalence, runtime cost or cache availability;
- all returned EmpiricalFact and DiscoveryResultReceipt refs pass exact identity validation;
- replay using the same exact source/release/authority bundle reproduces the same semantic results;
- source-backed I03 parity holds throughout;
- any unsupported/noncomparable/underpowered/unavailable state remains typed rather than silently dropped.

## 9. Failure classes C05-R2 must distinguish

C05-R2 must not collapse these:
- `RULE_AUTHORITY_NOT_ADOPTED`;
- `PRODUCTION_INSTANCE_AUTHORITY_INCOMPLETE`;
- `CATALOG_CONSTRUCTION_INCOMPLETE_OR_DATA_DEPENDENT`;
- `SOURCE_BACKED_I03_FACADE_PARITY_FAILURE`;
- `SOURCE_OR_AUTHORITY_IDENTITY_FAILURE`;
- `FRONTIER_COMPILE_INTEGRITY_FAILURE`;
- `RESOURCE_HARD_GATE_WITH_SEMANTICS_UNCHANGED`;
- `EXECUTION_OR_REPLAY_INTEGRITY_FAILURE`;
- `COMPLETE_EXACT_FRONTIER_EXECUTED`.

A resource hard gate is not semantic authority to prune, and an authority failure is not a performance result.

## 10. Architecture boundary

C05-R2 may measure source-backed/no-cache and lawful optional-session-cache implementations, but it may not infer that those measurements alone select persistence architecture A/B/C unless HQ separately authorizes that architectural decision.

## 11. C05-R2 readiness conclusion

The execution prerequisite surface is complete enough to launch C05-R2 **only after HQ adopts an exact production rule profile and authorizes the concrete facade implementation seam**.

Until then:
`C05R2_NOT_LAUNCHED__WAITING_ON_BINDING_HQ_RULE_AUTHORITY`.
