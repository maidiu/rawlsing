# FFIF005 — FFX002-XC DEPENDENCY

## 1. Scope

The first FFX002 R2 canary is local and does not require mapping authority. The optional FFX002-XC extension does.

FFX002-XC must consume frozen local outputs. It may not modify the local common semantic manifests or rebuild local views to improve cross-context alignment.

## 2. Mandatory pre-transport freeze per context

Before any cross-context comparison:

- exact `COMMON_SEMANTIC_INPUT_MANIFEST` ref/hash;
- governed respondent/exposure/risk-set authority;
- estimand and weight/design refs;
- exact local view refs/hashes and method/loss manifests;
- local claim identity and invariant refs;
- local support/uncertainty;
- CVCR/representation status from FFIF004 where applicable: `VIEW_ROBUST`, `VIEW_INDEXED_BUT_ADMISSIBLE`, `MULTI_VIEW_REQUIRED`, or `UNRESOLVED`;
- source/instrument topology refs;
- all local TTAR/PRA/role refs.

An `UNRESOLVED` local invariant cannot become a positive transport premise.

## 3. Mandatory mapping freeze

Before computing target transport output, freeze:

- exact FFX002-XC claim identity and preservation predicate;
- exact endpoint local object/component refs;
- candidate-generation log;
- edge-level identity/TTAR/PRA/role authority refs;
- complete admissible map family `H` and cardinality/bound;
- correspondence type and direction per edge;
- selected map or finite retained map set;
- outcome-independent selection/tie/unresolved rule;
- target-outcome firewall and `mapping_plan_hash`;
- alternative-map and saturation-null plan;
- map-multiplicity decision rule;
- allowed invariant and forbidden inference list;
- exact measurement-portability status ref (which may be `NOT_ADJUDICATED`).

## 4. Execution order

1. verify local hashes and representation statuses;
2. verify every edge authority and plan containment;
3. attest mapping-plan hash before target score;
4. run registered map(s) without retuning;
5. run type-constrained saturation/null and alternative maps;
6. separately report map, representation, semantic-input, and claim-scope dependence;
7. emit bounded transport status or `NO_TRANSPORT`.

## 5. Hard stop states

- `BLOCKED__LOCAL_OBJECT_NOT_INDEPENDENTLY_FROZEN`
- `BLOCKED__LOCAL_INVARIANT_UNRESOLVED`
- `NO_AUTHORIZED_MAP`
- `INVALID_MAPPING_PLAN__TARGET_OUTCOME_LEAK`
- `INVALID_MAPPING_PLAN__TTAR_LEAK`
- `INVALID_MAPPING_PLAN__PRA_LEAK`
- `NO_IDENTIFIABLE_MAP`
- `NONDISCRIMINATIVE_MAPPING_SPACE`
- `RESULT_MAP_DEPENDENT`
- `REPRESENTATION_DEPENDENT_TRANSPORT`
- `RISK_SET_ESTIMAND_COMPATIBILITY_UNRESOLVED`
- `NO_TRANSPORT`

No stop state may be repaired by widening `H` after observing results.

## 6. Cross-dependence reporting

FFX002-XC must keep separate:

- `MAP_DEPENDENCE`: fixed local views/claim, alternate authorized map;
- `REPRESENTATION_DEPENDENCE`: fixed semantic inputs/map/claim, alternate lawful local view;
- `SEMANTIC_INPUT_DEPENDENCE`: alternate TTAR/common semantic manifest;
- `CLAIM_SCOPE_DEPENDENCE`: alternate invariant/domain/estimand/quantifier.

A semantic-input or claim mismatch is not ordinary mapping sensitivity.

## 7. Claim ceiling

FFX002-XC may emit only the declared exact/order/rank/topology/conditional/motif/signature recurrence status under the frozen mapping plan. It may not emit measurement portability, category identity, same social position, common field/capital/mechanism, temporal equivalence, or homology.

