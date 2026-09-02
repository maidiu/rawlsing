# RAWLSING — GT1 + GT2 FROZEN CANARY CONTRACT R1

## Status

`FROZEN_FOR_BOUNDED_IMPLEMENTATION__NO_SEMANTIC_WIDENING`

## Common upstream substrate

- family: `Afrobarometer`
- wave: `R5`
- exact source: `Data/Afro Barometer Round 5.sav`
- source SHA-256: `c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651`
- source row count: `51,587`
- admitted respondent carrier: `FFP014_R5_CURRENT_RESPONDENT_CARRIER@1`
- respondent carrier identity: `sha256:6c2277e8832c8f070d1213f8f68adf54f115e4978f59702d150ab69fffd4a6d5`
- exact risk set: `FIRST_GENUINE_CANARY_COMMON_COEXPOSURE_RISK_SET@1`
- risk-set row count: `19,210`
- risk-set semantic member-set SHA-256: `0484fa5c0440c34e9b1f28b385f3ef6c3302eaeb11c3c5b663441553ea11313b`
- selected response-fact carrier SHA-256: `98526cf33e5344c6e2d5c6ad4b16826ee678b4648be2ada395e4f3ce70fe1709`
- selected exposure-fact carrier SHA-256: `0920c350aeb900b5922cf3872f86609de6a8cebb8d3991680dc9ee40e85b06ce`

Within this bounded risk set, Q86A and Q86B each have exactly one response and one proved-exposure fact per respondent. No executable-J inference from source-block membership is required.

## Exact operands

### Q86A

- source-native variable: `Q86A`
- question implementation: `question_impl.phase0.67f036c0efb7fb98ff4a`
- current source structure: `cssu.r1.afrobarometer.r5.d8478014cb0a506fe6c4`

### Q86B

- source-native variable: `Q86B`
- question implementation: `question_impl.phase0.2fb3a62609dad4c1306d`
- same exact current Q86 source structure family at R5 grain

The exact source-native response-state domains for Q86A and Q86B must be frozen from governed source metadata/projection. Preserve native state identity including exact missing/administrative states required by the query contract. Numeric source codes are identities only unless a separate authority supplies order/metric meaning.

## GT1

ID:

`GT1_R5_Q86A_RAW_UNARY_EXACT_RISK_SET@1`

Required empirical operation:

`SINGLE_UNIVERSE__RAW_UNARY_SOURCE_NATIVE_DISTRIBUTION`

Exact scope:

`FIRST_GENUINE_CANARY_COMMON_COEXPOSURE_RISK_SET@1`

Measure:

`RAW`

Weights:

`NOT_APPLICABLE`

Required result:

one current producer-owned I03 `EmpiricalFact` for the exact Q86A source-native distribution on the exact 19,210-member risk set, with exact query/predicate/authority/target-use identity and deterministic replay.

GT1 target-use ceiling:

`GT1_POSITIVE_EMPIRICAL_FACT_ONLY__NO_STRUCTURAL_OR_ACTOR_PROMOTION`

## GT2 empirical input

ID:

`GT2_R5_Q86A_X_Q86B_RAW_JOINT_EXACT_RISK_SET@1`

Required empirical operation:

exact two-target source-native Q86A x Q86B joint distribution over the same exact 19,210-member risk set.

- raw/unweighted;
- exact common eligible risk set;
- complete exact source-native target domains;
- meaning-bearing target order frozen as `[Q86B condition dimension, Q86A target dimension]` for later relation projection, while the empirical joint fact itself remains producer-owned and does not assert causality;
- deterministic replay;
- typed zero/empty/unavailable/integrity states preserved.

## GT2 FIELD FORGE relation

Relation family/id:

`EXACT_CONDITIONAL_SUPPORT_PROFILE_WITHIN_SCOPE@1.0.0`

Exact roles:

- `CONDITIONER = Q86B`
- `TARGET = Q86A`

Positive relation semantics:

From the exact producer-owned Q86A x Q86B joint empirical fact, emit the exact actor-independent conditional-support COUNT profile within the frozen risk set:

- one exact Q86B source-native condition-state identity at a time;
- exact denominator/support count for each Q86B state;
- exact joint support count for each Q86A state under each Q86B state;
- exact participant identities, roles, cardinality/order, scope and risk-set identity;
- exact producer fact/query/authority/replay refs;
- `NONE__REFERENCE_PRESERVING` relation handoff information-loss declaration;
- deterministic relation reconstruction.

No ratio is required for GT2. No order, distance, effect size, causal direction, baseline comparison, population generalization or redistribution/mechanism claim is made.

Binding anti-inferences:

`CONDITIONER != CAUSE`

`TARGET != EFFECT`

`CONDITIONAL_SUPPORT_PROFILE != CONDITIONAL_REDISTRIBUTION_MECHANISM`

`CONDITIONAL_SUPPORT_PROFILE != PRESSURE_PATHWAY`

`CONDITIONAL_SUPPORT_PROFILE != STRUCTURAL_MECHANISM`

`POPULATION_FACT != ACTOR_FACT`

## GT2 PRE-V3 admission

New rule family:

`FIELD_FORGE_RELATION_ADMISSION_RULE@1.0.0`

New positive receipt family:

`PREV3_FIELD_FORGE_RELATION_ADMISSION@1.0.0`

Owner jurisdiction:

`PREV3_FIELD_FORGE_RELATION_ADMISSION_OWNER`

Target use for GT2:

`STRUCTURAL_MEDIATION_INPUT`

Admission permission must be an exact subset of the relation permission ceiling.

This service is a sibling of current I04/P06. It MUST NOT coerce the relation into `EmpiricalFact` or `StructuralEmpiricalAdmission`, and it MUST NOT widen I04/P06.

## GT2 M1/V554 ingress

New ingress contract:

`M1_ADMITTED_FIELD_FORGE_RELATION_V554_INGRESS@1.0.0`

New basis kind:

`ADMITTED_FIELD_FORGE_RELATION`

Signature:

`V554-SIG-004-NONTEMPORAL-ADMITTED-RELATION-EXACT`

This GT2 target use requires no new V553-owned temporal meaning. If implementation discovers that temporal semantics are actually required, fail closed; do not relabel the relation as an existing V553 object.

The new ingress may reuse current `M1Evaluation` / F1/F2/B1 downstream shapes where semantically exact, but empirical-direct and admitted-relation basis classes remain distinct and never deduplicate across class by resemblance.

## GT2 downstream terminal

After positive M1/V554:

- use actual direct `V554_TO_V557_DIRECT` handoff;
- use actual M4 V557 governance/publication;
- use actual M4 V558 repository/exact resolution;
- V555 not required;
- V556 not required; `ZERO_V556_OBJECTS` lawful;
- optional M5 RSC/currentness check may be used;
- actual authoritative V3 zero-positive guard MUST be traversed;
- no accepted positive transition authority exists at this grain;
- actor state/ledger/RNG/scheduler remain exact zero effect.

Expected GT2 terminal:

`POSITIVE_PREV3_STRUCTURAL_WORLD__V3_ZERO_EFFECT_PASS`

## Forbidden scope widening

Do not invoke or close merely to execute GT1/GT2:

- J01-B;
- general production discovery;
- source pooling/backfill;
- measurement portability;
- cross-context transport;
- source retirement;
- survey weighting/population estimand authority;
- universal geometry;
- persistent/source-backed/hybrid winner;
- V555/V556 semantics;
- strong FIELD/CAPITAL/HEGEMONY/HOMOLOGY/PRESSURE/MECHANISM nouns;
- any V3 actor transition or V2 expression authority.
