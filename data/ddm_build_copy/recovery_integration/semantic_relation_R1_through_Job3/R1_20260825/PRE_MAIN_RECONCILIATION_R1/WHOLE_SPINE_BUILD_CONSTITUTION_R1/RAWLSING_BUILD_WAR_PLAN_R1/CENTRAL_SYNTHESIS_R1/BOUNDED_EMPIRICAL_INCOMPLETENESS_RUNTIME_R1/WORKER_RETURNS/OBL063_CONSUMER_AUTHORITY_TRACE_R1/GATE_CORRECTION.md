# OBL063 — CONSUMER-DRIVEN EMPIRICAL AUTHORITY GATE CORRECTION R1

## Disposition

The current WVS7 D11 gate is too strong **for source-local RAW empirical use**.

It is not too strong for population-generalizing use.

The code trace proves a concrete conflation:

`EmpiricalUniverse object existence`

has been operationally coupled to

`positive target + frame + actual-design documentary certification`

even though the dominant RAW single-universe consumers do not inspect those documentary fields.

## Exact code-level finding

`EmpiricalUniverse@1.0.0` requires the semantic field names:

- `target_population_and_sample_frame`
- `sampling_design_regime`

but the class has no family-specific validator beyond generic field presence.

C11 integrity additionally requires a nonempty `respondent_namespace`.

The source-backed C11 projector carries an EmpiricalUniverse object and exact respondent bindings into the release. It does not read target/frame/design to build respondent events, coordinates, routing facts, or RAW query incidence.

I03 source-local RAW execution:

- resolves the exact EmpiricalUniverse ref;
- iterates exact respondent identities;
- applies routing/risk-set authority;
- applies predicate and response-semantic authority;
- counts exact respondent support;
- returns an EmpiricalFact with exact provenance.

For `measure_kind = RAW`, `_weight_for()` returns exact 1 and does not consult WeightMeasureFact, design authority, estimand authority, target population, sample frame, or sampling design.

By contrast, `GOVERNED_WEIGHTED` explicitly requires positive `WEIGHT_DESIGN_ESTIMAND` authority, and `AUTHORIZED_COMPOSITE` explicitly requires pooling, nonduplication/source-relation, and estimand-composition authority.

Field Forge GT2 is stronger evidence for the actual structural path: it explicitly requires:

- `SINGLE_UNIVERSE`;
- `RAW`;
- no weighted numerator;
- no weighted denominator.

Therefore target/frame/design cannot lawfully remain a blanket prerequisite for Field Forge's source-local conditional-support input.

## Smallest correction

Do **not** create a new global audit campaign and do **not** weaken population claims.

Split source-universe admission into two authority ceilings.

### Lane S — SOURCE-LOCAL UNIVERSE/SCOPE ADMISSION

Purpose:

Allow exact source-local respondent evidence to exist and be queried without asserting national population representativeness.

Requirements:

- exact source artifact identity;
- exact source-scope identity;
- exact D12-style respondent namespace/replay identity where applicable;
- exact question/response semantics needed by the query;
- exact routing/risk-set authority needed by the query;
- explicit negative limits:
  - `NO_POPULATION_GENERALIZATION`
  - `NO_WEIGHTED_POPULATION_ESTIMAND_UNLESS_SEPARATELY_AUTHORIZED`
  - `NO_CROSS_UNIVERSE_POOLING_WITHOUT_RELATION_AUTHORITY`
  - `NO_NEAREST_COUNTRY_OR_WAVE_BACKFILL`

The existing `EmpiricalUniverse@1.0.0` object family can carry this lane without a new public family because the current public schema already separates exact source identity/respondent namespace from target/frame/design fields and consumers key on the exact universe ref.

For unknown target/frame/design content, the materialization contract must use explicit typed-unknown/not-certified semantic payloads. It may not invent values.

### Lane P — POPULATION-CERTIFIED USE

Purpose:

Authorize claims whose semantics are about a represented population rather than only the observed source respondents.

Required only when the consumer actually requests such a claim.

At minimum, the exact use must bind the positive authority appropriate to the operation:

- population target/coverage;
- frame/design where the claim depends on representative sampling;
- `WEIGHT_DESIGN_ESTIMAND` for governed weighted estimands;
- `TARGET_USE_PERMISSION` for the exact downstream population-level use;
- source-relation/pooling/comparability authority for multi-universe composition;
- temporal authority where the target use is time-scoped.

The existing WVS7 documentary recovery work belongs here.

## D11 correction

Replace the current effective law:

`TARGET+FRAME+DESIGN COMPLETE -> EmpiricalUniverse MAY EXIST`

with:

`EXACT SOURCE SCOPE + RESPONDENT NAMESPACE -> SOURCE-LOCAL EmpiricalUniverse MAY EXIST`

and independently:

`TARGET+FRAME+DESIGN + OPERATION-SPECIFIC AUTHORITY -> POPULATION-CERTIFIED USE MAY BE GRANTED`.

D11 therefore should become two bounded products, whether implemented as two subcourts or one object-plus-authority court:

1. source-local universe materialization;
2. population-certification overlay/permission.

The current 3/66 (now documentary prerequisite frontier 5/66 after the separate partial-recovery work) belongs to the **population-certification lane**, not to the source-local existence lane.

## WVS7 immediate consequence

D12 already establishes exact respondent/source-row identity across all 66 WVS7 source scopes.

That does **not** mean every WVS7 query is now executable:

- unresolved routing remains unresolved;
- missing question semantics remain missing;
- weight authority remains operation-specific;
- cross-source composition remains separately governed.

But absence of a national sample-frame PDF must no longer prevent a source scope from participating in a RAW single-universe query whose exact respondent, question, response, and routing semantics are otherwise authorized.

## OBL063 consequence

The generic OBL063 runtime contract remains valid and sufficient at the final driver/runtime ceiling:

- source-local evidence cannot masquerade as population evidence;
- missing channels cannot become zero;
- no implicit renormalization;
- model priors remain non-empirical.

One additional PRE553 admission/materialization seam is required upstream:

`SOURCE_LOCAL_EMPIRICAL_UNIVERSE_ADMISSION_R1`

This is a **profile/authority contract**, not a new public ontology family.

Its purpose is to allow exact source-local EmpiricalUniverse materialization with explicit population-use denial when target/frame/design are not fully certified.

## Consumer-specific population authority

Population certification is triggered by consumer semantics, not by archive membership.

Examples:

- RAW single-universe respondent distribution -> SOURCE_LOCAL is sufficient.
- Field Forge RAW conditional support -> SOURCE_LOCAL is sufficient.
- source-indexed multi-universe facts retained separately -> SOURCE_LOCAL per source is sufficient.
- governed weighted population estimate -> population/design/estimand authority required.
- pooled cross-country/cross-wave estimate -> population + relation/comparability/composition authority required.
- source-local DDM exploratory analysis -> SOURCE_LOCAL may be sufficient.
- ordinary V3 runtime -> consumes compiled structural products; no live respondent-level population certification prerequisite.

## Hard limits preserved

This correction does not authorize:

- treating source respondents as nationally representative;
- using weights without exact weight/design/estimand authority;
- pooling countries or waves by label;
- applying Field Forge relations as actor facts or causal mechanisms;
- bypassing routing authority;
- weakening audit/replay identity;
- declaring documentary recovery unnecessary where a population claim is actually consumed.

## Terminal

`D11_GATE_OVERSTRONG_FOR_SOURCE_LOCAL_RAW_USE__SOURCE_LOCAL_UNIVERSE_ADMISSION_REQUIRED__POPULATION_CERTIFICATION_RETAINED_AS_OPERATION_SPECIFIC_OVERLAY`
