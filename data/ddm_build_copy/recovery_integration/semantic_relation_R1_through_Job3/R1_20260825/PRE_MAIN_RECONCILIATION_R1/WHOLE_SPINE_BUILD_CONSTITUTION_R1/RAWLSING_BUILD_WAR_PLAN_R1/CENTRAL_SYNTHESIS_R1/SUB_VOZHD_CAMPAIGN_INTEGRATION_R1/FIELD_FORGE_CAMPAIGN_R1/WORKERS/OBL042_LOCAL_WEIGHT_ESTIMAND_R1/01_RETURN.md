# RABOCHII RETURN — FIELD FORGE OBL042 LOCAL WEIGHT / ESTIMAND / PROVENANCE R1

Terminal:

`PASS__FIELD_FORGE_OBL042_LOCAL_WEIGHT_ESTIMAND_PROVENANCE_AUTHORITY_CANDIDATE_GREEN__NO_HOMOLOGY_ADMISSION__NO_ADOPTION`

Worker branch:

`agent/rabochii-field-forge-c-obl042-local-weight-estimand-r1`

Exact starting HEAD:

`7c3bad90b50522e9e5369a420d07aa0d9f3c41d0`

Immutable HQ prerequisite / continuation ref:

`4ec035d02e81f0468c4a5157f91b51ad0126e4fb`

Project-current prerequisite:

`ADOPTED__FIELD_FORGE_OBL040_OBSERVABILITY_ROUTING_RELATION_AUTHORITY__EXACT_BOUNDED_GRAIN__OBL040_CLOSED`

Candidate identity:

`FIELD_FORGE_OBL042_LOCAL_WEIGHT_ESTIMAND_PROVENANCE_AND_HOMOLOGY_REFUSAL_AUTHORITY@1.0.0`

`OBL006_NOT_PREREQUISITE_FOR_THIS_LOCAL_GRAIN`

`NO_PROJECT_CURRENT_ADOPTION`

## 1. Holding

The minimum lawful local OBL042 authority is a **producer-preserving weight/estimand provenance contract plus contamination diagnostic**, not a new owner of weights, populations, estimands, geometry, transport, or homology.

A local weighted/design-based FIELD FORGE assertion is admissible only when its receipt binds the exact upstream authority that gives the selected weight its exact role for the exact target and estimand.

Core law:

`WEIGHT_VARIABLE_PRESENT != AUTHORIZED_WEIGHT_ROLE`

`AUTHORIZED_WEIGHT_ROLE_FOR_ESTIMAND_A != AUTHORIZED_WEIGHT_ROLE_FOR_ESTIMAND_B`

`WEIGHTED_SAMPLE != TARGET_POPULATION`

`UNWEIGHTED_RELATION != DEFAULT_POPULATION_RELATION`

`BLOCK_SIZE != WEIGHT`

## 2. Minimum local Weight–Estimand Provenance Receipt

For every weighted/design-based local assertion, bind as applicable:

1. `weight_object_id` — exact producer-owned variable/design object identity;
2. `weight_authority_ref` — immutable producer/governance authority for its semantics;
3. `weight_purpose` — exact governed role/purpose;
4. `target_universe_id` — exact eligible universe / target population;
5. `estimand_id` — exact estimand or representation target;
6. `scope_context_time` — exact validity grain;
7. `design_provenance` — sampling/design authority where relevant;
8. `calibration_provenance` — calibration/poststratification/raking/benchmark authority where relevant;
9. `combination_rule` — exact rule and authority if multiple weight/design components are combined;
10. `support_and_risk_set_ref` — exact denominator/support/risk-set identity required by the assertion;
11. `geometry_dependency_state` — exact relation between weighting and any geometry commitment;
12. `measurement_ancestry_diagnostic` — exact shared-input / derived-input / circularity receipt;
13. `permission_negative_authority` — exact permission and negative-state ceiling;
14. `provenance_closure` — immutable dependency closure;
15. `replay_determinants` — sufficient exact inputs/identities to deterministically reconstruct the assertion.

No omitted field is silently inferred from column name, dataset convention, storage path, questionnaire block, software default or common survey practice.

## 3. Governed weight-purpose law

A weight is lawful for a FIELD FORGE assertion only under an exact producer/governance statement that binds that weight to the assertion's target and estimand.

Examples of distinctions that must remain explicit where present in producer authority include:

- design/base weight;
- nonresponse adjustment;
- poststratification/calibration/raking component;
- population-scaling weight;
- treatment/oversample correction;
- mode/frame-specific correction;
- other exact producer-defined purpose.

OBL042 does not standardize these categories and does not infer them from names. It preserves the producer's exact purpose identity.

If no exact governed role can be established:

`WEIGHT_ROLE = MISSING_AUTHORITY`

and the weighted assertion is blocked at that grain.

The underlying unweighted local descriptive relation may remain lawful if independently authorized, but it must not be promoted to a population/estimand claim.

## 4. Target population / universe and estimand binding

The same observed sample may support different lawful assertions only under their separately governed target/estimand bindings.

A receipt must distinguish at minimum:

- observed sample/risk set;
- eligible universe;
- target population;
- representation target;
- estimand;
- support/zero-denominator state.

`SAMPLE_SUPPORT != TARGET_UNIVERSE != ESTIMAND`.

Population language is forbidden unless the exact target/estimand authority is present.

A generic statement that a dataset is "weighted" or "representative" cannot substitute for exact binding.

## 5. Design/calibration provenance

Where a claim depends on sampling design, calibration, poststratification, treatment of oversamples, strata/cluster corrections or analogous producer-defined design features, the exact authority and dependency chain must be retained.

OBL042 does not reconstruct or reinterpret a producer design from variable coappearance or names.

If design/calibration provenance needed by the claim is missing or unresolved, preserve the exact blocker rather than replacing it with an ordinary value or an unqualified weight use.

## 6. Weight↔geometry dependency provenance

OBL042 does **not** choose or mint a geometry family.

For each assertion, record one of the following exact states:

### A. `NO_GEOMETRY_REQUIRED`

The weighted/design-based assertion is fully specified over a lawful nongeometric local relation and no geometry dependency exists.

### B. `CURRENT_GEOMETRY_AUTHORITY_REF`

The assertion depends on a separately project-current lawful geometry relation. Bind:

- exact geometry relation identity;
- exact current authority ref;
- direction of dependence;
- which weight/estimand choices depend on that relation or vice versa;
- scope/context/time;
- replay determinants.

### C. `GEOMETRY_AUTHORITY_MISSING_OR_NOT_CURRENT`

The desired weighted assertion needs a geometry commitment that is not yet project-current at that grain. The assertion is blocked rather than borrowing a candidate, historical geometry, embedding or storage layout.

Therefore the current OBL041 candidate, while independently relevant to the campaign, is **not** consumed here as project-current authority unless and until HQ adopts it.

`CANDIDATE_GEOMETRY != CURRENT_GEOMETRY_AUTHORITY`.

## 7. Measurement-ancestry / circularity diagnostic

OBL042 may diagnose provenance dependence among constructed relations without promoting that dependence into social-theoretical semantics.

For every compared/combined local object where shared ancestry could matter, compute or preserve a replayable ancestry receipt over exact producer/transform/relation dependencies.

At minimum distinguish:

- `DISJOINT_OBSERVED_INPUT_ANCESTRY` — no shared governed observed inputs identified at inspected closure;
- `SHARED_OBSERVED_INPUT_ANCESTRY` — one or more exact observed inputs are shared;
- `SHARED_DERIVED_INPUT_ANCESTRY` — one or more upstream derived/transform objects are shared;
- `DIRECT_CONSTRUCTION_DEPENDENCY` — one object directly consumes the other or its sufficient statistic;
- `MUTUAL_OR_CYCLIC_CONSTRUCTION` — circular dependency exists and the asserted independent comparison is invalid unless separately resolved;
- `ANCESTRY_UNRESOLVED` — dependency closure is insufficient to decide.

These states are **contamination/circularity diagnostics only**.

They may support warnings such as:

- apparent similarity may be partly construction-induced;
- two views are not independent evidence;
- a comparison is circular;
- an estimand or geometry depends on the same measurements later used to evaluate it.

They do not establish substantive structural sameness.

`SHARED_MEASUREMENT_ANCESTRY != HOMOLOGY`

`CIRCULARITY_DIAGNOSTIC != HOMOLOGY`

`RECURRENCE != HOMOLOGY`

## 8. Homology refusal

At this OBL042 grain:

`HOMOLOGY = BLOCKED_EXPLICIT_AUTHORITY`.

No amount of:

- shared variables;
- shared source lineage;
- repeated questionnaire ancestry;
- similar weights;
- similar geometry;
- correlated local statistics;
- repeated conditional shape;
- recurrence across time/context;
- common normalized coordinates;
- common block size;
- common ancestry diagnostic

self-mints `HOMOLOGY`.

A future competent authority would require its own exact semantic admission court. This candidate does not identify or create that court.

## 9. Local-only / transport refusal

This authority is local to the exact governed object/context grain.

It does not authorize external political-group transport or any cross-context identity/equivalence map.

Outside an authorized typed map:

`NO_TRANSPORT / NONCOMPARABLE`.

OBL006 remains claim-conditional and dormant unless a named concrete Field Forge claim actually requires external political-group transport.

No local weight, population scaling, quantile/rank transformation, normalization or calibration can substitute for cross-context mapping authority.

`SAME_WEIGHT_SCALE != SAME_POPULATION != SAME_ESTIMAND != TRANSPORT_AUTHORITY`.

## 10. Strong-noun and political-power firewall

This candidate does not create or support admission of:

- `FIELD`;
- `FIELD_SPECIFIC_CAPITAL` / `CAPITAL`;
- strong social-mechanism `CONVERSION`;
- `HOMOLOGY`;
- `HEGEMONY / SUBHEGEMONY`;
- political-power alignment;
- pressure/mechanism strong nouns;
- V3 actor belief/identity/history/realization.

Weighted prevalence or weighted association is not hegemony, capital, field position, conversion or actor realization.

## 11. Exact negative / limit / provenance states

Preserve the narrowest truthful state as applicable:

- `OBSERVED_ZERO`;
- exact zero difference;
- `VALID_EMPTY`;
- `ZERO_DENOMINATOR_ABSTENTION`;
- `UNDEFINED_FOR_OBJECT`;
- `OUT_OF_SCOPE`;
- `DENIED`;
- `MISSING_AUTHORITY` / `UNRESOLVED_AUTHORITY`;
- `OBSERVABILITY_LIMIT`;
- `NONCOMPARABLE` / `NO_TRANSPORT`;
- `NO_GEOMETRY_REQUIRED`;
- `BLOCKED_EXPLICIT_AUTHORITY`;
- `ANCESTRY_UNRESOLVED`;
- `CIRCULARITY_BLOCKED` where a claimed independent construction is cyclic;
- `INTEGRITY_FAILURE` / replay failure.

None may be repaired into a numeric weight, distance, comparison, population claim or homology admission.

## 12. Producer-ownership firewall

OBL042 owns only the FIELD FORGE receipt/diagnostic identity and replay contract above.

It does not re-own upstream semantics for:

- weight variables/design objects;
- weight purpose;
- target population/universe;
- estimand;
- sample design/calibration;
- source/respondent/routing/measurement facts;
- transforms/equivalences;
- permissions/provenance.

`DIRECT_REFERENCE != SEMANTIC_REOWNERSHIP`.

## 13. Historical stress evidence — nonbinding only

Historical FFIF012E tip `3ee4e1f6503529f32930edc528d5f09c75dd3c2c` was consulted only as corroborating evidence that multiple source families carry purpose-specific weight contracts and no universal default, and that silent weight/estimand selection can manufacture geometry.

Historical FFIF012G tip `752b7769ae139d046568de9ae7aedcadb539905a` was consulted only as corroborating evidence that one family does not imply one common estimand/design and that recurrence does not establish homology.

Neither historical docket is current authority. Operative authority is adopted FIELD FORGE R2 + project-current OBL040 + exact HQ narrowed OBL042 commission.

## 14. Adoption scope requested later

If independently hostile-reviewed and accepted by HQ, the exact adoption grain should be only:

`FIELD_FORGE_OBL042_LOCAL_WEIGHT_ESTIMAND_PROVENANCE_AND_HOMOLOGY_REFUSAL_AUTHORITY@1.0.0`

It would create the local provenance/diagnostic contract and refusal laws above. It would not adopt a specific weight for any unnamed claim, choose a geometry family, establish transport, admit homology, or execute OBL043.

## Terminal

`PASS__FIELD_FORGE_OBL042_LOCAL_WEIGHT_ESTIMAND_PROVENANCE_AUTHORITY_CANDIDATE_GREEN__NO_HOMOLOGY_ADMISSION__NO_ADOPTION`

`WORKER_PASS != PROJECT_CURRENT`

`WORKER_PASS != OBL043_AUTHORIZED`

Return phase: `CLOSURE_ONLY`.
