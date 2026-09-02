# RAWLSING BUILD WAR PLAN R1 — WAVE 1 ENABLE CENTRAL FAN-IN R1

## Terminal

`PASS__WAVE1_ENABLE_CENTRAL_FANIN__GT1_GT2_EXACT_CANARY_SELECTED__READY_FOR_PARALLEL_IMPLEMENTATION`

## Evidence consumed

- W1A terminal: `f8ce19a56365856a88c58cd44a83502f66659d48`
- W1B terminal: `7d1bb7a03cfc4bf9532c92b03747944e5aecf2c0`
- W1C terminal: `e0f32d0777b7962be085442d13a28bddab9e57db`
- W1D terminal: `c2977601499b69fb988b284e04eacf0494b037c6`
- W1E terminal: `74f544b2abcc2a16408f285eb930fbe4c7b93040`
- W1F terminal: `540b2fa632d0b0de608998a1b511f2653e85ab10`
- W1G terminal: `5921ac6be266b51088edc7a5f9c1c60467d5c983`
- GT0 hostile rereview PASS: `19ea48a7f0742c721e28b4ac51e6c205d01f5497`
- GT0 real-checkout gate PASS: `3b28d96459f11ec6502dc2bc0864d57c22de6d28`

No sibling planning artifact is promoted merely because it exists. This fan-in makes the project-level selection below.

## GT0 disposition

GT0 is now semantically and executably closed PASS at its audited grain.

Exact executed candidate:

`ed1482517e0eebe2228e838dc6a24b97db879fc9`

Real-checkout execution result:

`214 passed`.

A separate central adoption record is banked on `agent/vozhd-gt0-canonicalization-adoption-r1`. PRE-MAIN and `main` remain unmoved by this fan-in.

## First positive empirical substrate selection

Central selects Afrobarometer R5 and deliberately does NOT continue F0 merely for continuity.

Exact governed substrate:

- source: `Data/Afro Barometer Round 5.sav`
- source SHA-256: `c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651`
- source rows: `51,587`
- respondent carrier: `FFP014_R5_CURRENT_RESPONDENT_CARRIER@1`
- respondent carrier identity: `sha256:6c2277e8832c8f070d1213f8f68adf54f115e4978f59702d150ab69fffd4a6d5`
- common coexposure risk set: `FIRST_GENUINE_CANARY_COMMON_COEXPOSURE_RISK_SET@1`
- risk-set members: `19,210`
- risk-set semantic member-set SHA-256: `0484fa5c0440c34e9b1f28b385f3ef6c3302eaeb11c3c5b663441553ea11313b`
- selected response facts: `670,631` rows, SHA-256 `98526cf33e5344c6e2d5c6ad4b16826ee678b4648be2ada395e4f3ce70fe1709`
- selected exposure facts: `670,631` rows, SHA-256 `0920c350aeb900b5922cf3872f86609de6a8cebb8d3991680dc9ee40e85b06ce`

The bounded eight-variable substrate has exactly one response and one proved-exposure fact per variable for every risk-set respondent. No executable-J inference from source-block membership is needed.

## GT1 selection

`GT1_R5_Q86A_RAW_UNARY_EXACT_RISK_SET`

- operand: `Q86A`
- question implementation: `question_impl.phase0.67f036c0efb7fb98ff4a`
- source structure: `cssu.r1.afrobarometer.r5.d8478014cb0a506fe6c4`
- scope: exact 19,210-member common coexposure risk set above
- query shape: `SINGLE_UNIVERSE__RAW_UNARY_SOURCE_NATIVE_DISTRIBUTION`
- measure: `RAW`
- weights: `NOT_APPLICABLE`
- source-native domain only; no recode/harmonization
- target use: `GT1_POSITIVE_EMPIRICAL_FACT_ONLY__NO_STRUCTURAL_OR_ACTOR_PROMOTION`

GT1 acceptance requires one producer-owned current I03 `EmpiricalFact` plus deterministic replay and exact typed-negative behavior.

## GT2 empirical input selection

GT2 uses the same source/scope and adds `Q86B`:

- Q86B question implementation: `question_impl.phase0.2fb3a62609dad4c1306d`
- I03 empirical input shape: exact two-target Q86A x Q86B source-native joint distribution over the same 19,210-member risk set
- exact same-respondent incidence is already proved on this bounded substrate
- raw/unweighted
- no portability, pooling, transport, discovery, source retirement or physical architecture choice

The complete source-native Q86A and Q86B state domains must be frozen from exact governed source metadata/projection before execution. No state code may be interpreted as ordinal or metric merely because it is numeric.

## GT2 FIELD FORGE relation selection

Central selects the weak actor-independent relation family:

`EXACT_CONDITIONAL_SUPPORT_PROFILE_WITHIN_SCOPE@1.0.0`

with claim-constitutive ordered roles:

- `CONDITIONER = Q86B`
- `TARGET = Q86A`

The relation consumes the exact producer-owned Q86A x Q86B joint empirical fact and asserts only the exact conditional-support count profile within the frozen risk set:

- for each exact source-native Q86B state, the exact denominator/support count;
- for each exact source-native Q86A state within that condition, the exact joint support count;
- exact zero and valid-empty states preserved;
- no ratio, metric distance, causal direction, population generalization or baseline redistribution claim is required for GT2.

`CONDITIONER != CAUSE`

`TARGET != EFFECT`

`CONDITIONAL_SUPPORT_PROFILE != PRESSURE_MECHANISM`

The relation owns only this actor-independent conditional-support relation commitment. It does not re-own source/query/respondent/risk-set/measurement semantics.

## Why not EXACT_SUPPORT_WITHIN_SCOPE

W1C correctly ranked unary support as cheaper only if it adds a genuine relation commitment. For GT2, central chooses the conditional-support profile because the same-respondent substrate is already proved and this gives a genuinely relational asymmetric object without paying transport, weight, strong-noun, PRA/TTAR or actor authority.

## FF -> PRE-V3 admission constitution

Central accepts W1D's type split as the implementation contract:

- rule: `FIELD_FORGE_RELATION_ADMISSION_RULE@1.0.0`
- receipt: `PREV3_FIELD_FORGE_RELATION_ADMISSION@1.0.0`
- owner jurisdiction: `PREV3_FIELD_FORGE_RELATION_ADMISSION_OWNER`

This is a sibling jurisdiction to current I04/P06.

It MUST NOT:

- call I04 with a FIELD FORGE relation;
- coerce a relation into `EmpiricalFact`;
- fabricate `StructuralEmpiricalAdmission`;
- widen current I04/P06 allowlists.

Positive admission only narrows the relation permission ceiling to the exact downstream target use.

## M1 relation-basis constitution

Central accepts W1E's separate relation-specific ingress design:

- ingress contract: `M1_ADMITTED_FIELD_FORGE_RELATION_V554_INGRESS@1.0.0`
- basis kind: `ADMITTED_FIELD_FORGE_RELATION`
- first signature: `V554-SIG-004-NONTEMPORAL-ADMITTED-RELATION-EXACT`

The first GT2 relation is intentionally non-temporal at this target-use grain. New V553 meaning is therefore not required.

The relation-specific ingress must preserve current empirical M1 behavior unchanged, reuse `M1Evaluation`/F1/F2/B1 shapes where exact, and use a relation-specific equivalence key. Empirical-direct and admitted-relation bases never deduplicate across basis classes merely because they appear semantically similar.

## Downstream reuse

After lawful relation admission + relation-specific M1 ingress:

- reuse current M1/V554 execution;
- use current direct `V554_TO_V557_DIRECT` handoff;
- reuse current M4 V557 governance/publication and V558 exact repository/resolution;
- V555 is absent unless a separately owned route is required;
- V556 is absent for GT2 unless separately required; `ZERO_V556_OBJECTS` remains lawful;
- M5 runtime structural-context validation is optional but useful as a firewall proof;
- V3 must traverse the actual current zero-positive guard and remain `DENY_ZERO_EFFECT`.

GT2 does NOT authorize positive actor mutation.

## Execution environment

Use W1G's command law at fan-in:

- exact candidate SHA check;
- clean checkout before/after;
- CPython 3.11.x baseline for repository-native parity unless a separately recorded compatibility run is used;
- `python -m pytest`;
- `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`;
- `PYTHONHASHSEED=0`;
- `PYTHONDONTWRITEBYTECODE=1`;
- exact dependency/version/test-path receipt.

Only claim-triggered optional dependencies may be installed.

## Remaining gates

The implementation wave still must prove, not assume:

1. exact governed R5 -> `GovernedC11Projection` / C11 release binding for Q86A/Q86B at the selected risk set;
2. exact production AuthoritySnapshot/query/predicate/target-use bindings for GT1 and the Q86A x Q86B joint fact;
3. exact source-native state-domain preservation;
4. relation producer semantics and deterministic reconstruction from the joint fact;
5. exact W1D admission implementation;
6. exact W1E M1 relation ingress and minimal M4 accepted-contract adaptation;
7. end-to-end GT2 resolution with V3 zero effect;
8. focused + inherited real-checkout regression;
9. one bounded hostile audit because a new FF->PRE-V3/M1 authority boundary is being introduced.

No broader architecture court is activated.

Terminal:

`PASS__GT1_GT2_CANARY_AND_SEAMS_FROZEN__READY_FOR_IMPLEMENTATION_WAVE`
