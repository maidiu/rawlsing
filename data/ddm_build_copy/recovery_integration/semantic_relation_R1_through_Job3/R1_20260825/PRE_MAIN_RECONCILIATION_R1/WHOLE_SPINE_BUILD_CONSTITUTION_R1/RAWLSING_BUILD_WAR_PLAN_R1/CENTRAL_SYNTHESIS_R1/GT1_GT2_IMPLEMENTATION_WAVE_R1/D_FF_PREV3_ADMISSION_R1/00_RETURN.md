# RAWLSING GT12-D — FIELD FORGE RELATION → PRE-V3 ADMISSION IMPLEMENTATION R1

## Terminal

`PASS__GT12D_FF_PREV3_RELATION_ADMISSION_READY_FOR_CENTRAL_INTEGRATION`

## Exact scope

Repository: `maidiu/rawlsing`

Branch:

`agent/rabochii-warplan-gt12-d-ff-prev3-admission-r1`

Exact working ancestry:

`2c95e64b9be9eb9c730028c840e04596dc556893`

Immutable instruction/evidence ref:

`17b9abc5c8c3038d14670c6e68136bb868f5073a`

Frozen canary contract:

`a9416094cbb4653dd2de2e4aa7b67577a355560c`

Wave 1 central fan-in evidence:

`6a4bf89c5403459d43dcb925c1f98a7b30dd6f49`

Sibling GT1/GT2 implementation branches consumed: `NONE`.

No source acquisition was performed. PRE-MAIN and `main` were not moved. Current I04/P06, current PRE553 public object families/authority kinds, current M1 empirical path, M4, M5 and V3 guard code were not modified.

## Implemented production surface

Added:

`rawlsing_next/wave1_ff_prev3_relation_admission.py`

The module implements the W1D sibling jurisdiction at the exact frozen GT2 grain:

- rule contract: `FIELD_FORGE_RELATION_ADMISSION_RULE@1.0.0`;
- receipt contract: `PREV3_FIELD_FORGE_RELATION_ADMISSION@1.0.0`;
- owner: `PREV3_FIELD_FORGE_RELATION_ADMISSION_OWNER`;
- only accepted relation family: `EXACT_CONDITIONAL_SUPPORT_PROFILE_WITHIN_SCOPE@1.0.0`;
- only positive target use: `STRUCTURAL_MEDIATION_INPUT`;
- intended downstream contract: `M1_ADMITTED_FIELD_FORGE_RELATION_V554_INGRESS@1.0.0`.

The implementation is deliberately canary-scoped rather than a generic FIELD FORGE admission framework.

## Frozen GT2 bindings

The evaluator binds and checks:

- source family/wave: `Afrobarometer` / `R5`;
- source artifact: `Data/Afro Barometer Round 5.sav`;
- exact source SHA-256: `c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651`;
- risk set: `FIRST_GENUINE_CANARY_COMMON_COEXPOSURE_RISK_SET@1`;
- exact risk-set row count: `19,210`;
- exact member-set SHA-256: `0484fa5c0440c34e9b1f28b385f3ef6c3302eaeb11c3c5b663441553ea11313b`;
- ordered role 0 `CONDITIONER = Q86B` with question implementation `question_impl.phase0.2fb3a62609dad4c1306d`;
- ordered role 1 `TARGET = Q86A` with question implementation `question_impl.phase0.67f036c0efb7fb98ff4a`;
- exact Q86 source-structure identity `cssu.r1.afrobarometer.r5.d8478014cb0a506fe6c4`;
- exact relation rule/content identity supplied by the future integrated GT12-C producer;
- exact upstream relation authority/current-selection, semantic/scope/universe, dependency and replay closure.

D does not invent GT12-C's relation rule or participant refs. `make_gt2_relation_admission_rule(...)` requires those exact refs from central integration.

## Authority / permission law

This module does not widen `pre553_empirical_authority.AUTHORITY_KINDS`. Instead it carries a bounded content-addressed `RelationAdmissionAuthorityBinding` fixed to the frozen GT2 canary, Wave 1 central fan-in, exact operation, relation family, target use and downstream contract.

That binding owns only the relation-admission decision. It does not acquire upstream empirical or FIELD FORGE relation ownership.

Positive permission is exactly:

`STRUCTURAL_MEDIATION_INPUT`

and only when it is already inside the relation's permission ceiling.

`ADMISSION_PERMISSION ⊆ RELATION_PERMISSION_CEILING`.

No generic PRE-V3 permission exists.

## Typed-state law

Relation evidence state and admission decision remain separate.

`SUPPORTED` and `OBSERVED_ZERO` are the only frozen relation states eligible for positive GT2 admission. `OBSERVED_ZERO` is therefore preserved as zero evidence and is not silently converted into denial.

Typed upstream negative/blocker states remain nonpositive, including:

- `VALID_EMPTY` / `ZERO_DENOMINATOR_ABSTENTION`;
- `UNDEFINED_FOR_OBJECT` / `OUT_OF_SCOPE`;
- `DENIED`;
- `MISSING_AUTHORITY` / `UNRESOLVED_AUTHORITY`;
- `UNRESOLVED`;
- `NONCOMPARABLE` / `NO_TRANSPORT`;
- `BLOCKED_EXPLICIT_AUTHORITY`;
- `OBSERVABILITY_LIMIT`;
- `INTEGRITY_FAILURE`.

Applicable exact negative/limit refs on an otherwise positive relation block admission rather than being discarded.

## No-coercion firewall

The production module does not import `pre553_structural_admission.py` and does not call `evaluate_structural_empirical_admission(...)`.

It does not:

- subclass, alias or construct `EmpiricalFact`;
- construct `StructuralEmpiricalAdmission`;
- modify I04/P06 family allowlists;
- create current M1 `DIRECT_STRUCTURAL_EMPIRICAL_ADMISSION` material;
- create V553, V555 or V556 objects;
- infer actor state.

The positive receipt explicitly records these ceilings and remains a separate input for GT12-E's relation-specific M1 ingress.

## Information conservation / replay

Admission-local information loss is frozen as:

`NONE__REFERENCE_PRESERVING`.

The receipt preserves the upstream relation's own information-loss declaration separately and cannot improve or rewrite it.

Receipt identity is deterministic over exact relation identity, admission rule/authority/current-selection, target use, permission subset, upstream semantic/scope/universe/participant/negative/dependency closure and replay root.

`replay_gt2_relation_admission(...)` requires the exact historical relation, rule and authority material and rejects later reinterpretation or tampering.

## Focused hostile tests

Added:

`rawlsing_next/tests/test_wave1_ff_prev3_relation_admission.py`

Coverage includes:

- positive exact GT2 admission;
- `OBSERVED_ZERO` preservation;
- the frozen typed-negative family;
- target-use and downstream-contract mismatch;
- permission denial/widening;
- relation-rule/content-hash tamper;
- source/risk-set tamper;
- CONDITIONER/TARGET role-order tamper;
- information-loss rewrite;
- applicable negative refs;
- admission-authority denial;
- deterministic historical replay and replay tamper;
- duck-typed / EmpiricalFact-like input rejection;
- static no-I04/P06/no-M1-direct coercion assertion.

The focused module/test pair was executed locally in an isolated compatibility harness using only an API-compatible stand-in for the unchanged PRE553 `ExactRef` / `AuthorityRef` / canonical hashing utilities because this connector environment does not expose the repository checkout itself. Result:

`32 passed`

This is not represented as a real-checkout inherited regression run. Central fan-in remains responsible for executing the integrated branch with the repository-native W1G command and inherited I04/M1/M4/M5/V3 subset.

## Changed files

Exactly three D-lane additions are intended:

1. `rawlsing_next/wave1_ff_prev3_relation_admission.py`
2. `rawlsing_next/tests/test_wave1_ff_prev3_relation_admission.py`
3. `data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/GT1_GT2_IMPLEMENTATION_WAVE_R1/D_FF_PREV3_ADMISSION_R1/00_RETURN.md`

No sibling implementation output is consumed or reproduced.

## Central integration handoff

Central should bind GT12-C's actual relation rule/participant refs into `make_gt2_relation_admission_rule(...)`, feed its exact relation into `FieldForgeRelationEvidence`, require `AdmissionDecision.ADMITTED`, then hand the immutable `Prev3FieldForgeRelationAdmission` to GT12-E.

`RELATION_ADMITTED != M1_BASIS_ACCEPTED` remains binding until E's relation-specific ingress validates the receipt.

`PASS__GT12D_FF_PREV3_RELATION_ADMISSION_READY_FOR_CENTRAL_INTEGRATION`
