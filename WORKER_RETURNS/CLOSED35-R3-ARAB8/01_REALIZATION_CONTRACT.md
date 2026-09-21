# CLOSED35-R3-ARAB8 — Realization Contract

Schema: CLOSED35_R3_ARAB8_SOURCE_REALIZATION@1.0.0

Semantic owner: ARAB8_SEMANTIC_OWNER_V1

## 1. Court object

This contract defines one candidate-neutral source-specific semantic realization for the exact canonical source Arab Barometer Wave 8.sav with SHA-256 a5e83a953f03dd890e076a51da473051f1cfd1ca2e8ab93c2172eeb2517af998.

Physical delivery may later differ among A/B/C, but source identity, replay identity, physical/semantic state separation, variable nonalias, documentary routing jurisdiction, module topology, bounded UNKNOWN behavior, and weight/design nonselection are invariant.

This implementation is not a real-source execution, source-certification court, or whole-source physical-equivalence court.

## 2. Canonical source and replay identity

Canonical filename: Arab Barometer Wave 8.sav

Canonical SHA-256: a5e83a953f03dd890e076a51da473051f1cfd1ca2e8ab93c2172eeb2517af998

Format: SAV

Accepted physical mode: SAV_NATIVE_GOVERNED

Accepted source-reported character mode: UTF-8 / code 65001

Replay identity: SOURCE_SHA256+ROW_ORDINAL

The accepted packet records ID=0 for 2,400 rows. ID therefore remains a source attribute and may not replace the hard replay key.

The questionnaire's label "Respondent ID number" is documentary role evidence, not uniqueness authority.

## 3. ID=0 preservation law

For ID raw value 0:

physical state = ORDINARY_STORED_VALUE

raw value = 0

documentary role = RESPONDENT_ID_NUMBER

hard replay authority = false

ID=0 must not trigger row deletion, respondent nullification, deduplication, or identity repair.

COUNTRY+ID likewise has no hard replay authority.

## 4. BLOCK_ID physical and semantic law

The accepted snapshot establishes ordinary empty strings in BLOCK_ID.

For BLOCK_ID raw value "":

physical state = ORDINARY_STORED_VALUE

raw value = exact empty string

semantic state = BOUNDED_UNKNOWN

No conversion to SYSTEM_MISSING, null, NOT_ASKED, or inferred sampling block is authorized.

Exact BLOCK_ID scope and blank-state meaning remain BOUNDED_UNKNOWN.

## 5. Q1 and STRATUM remain distinct

Q1 carries exact source-native documentary authority as Governorate / first administrative division.

STRATUM remains a distinct source variable with BOUNDED_UNKNOWN design semantics at this evidence boundary.

The accepted packet states Q1==STRATUM physically across the exact snapshot.

Vector equality does not authorize:

- variable aliasing;
- semantic equivalence;
- dictionary replacement;
- identity replacement;
- geography-to-design semantic transfer;
- design-role inference.

Any later alias requires independent documentary authority and a superseding governed contract.

## 6. Documentary routing law

Routing and applicability are document-led.

Admitted exact rules:

### AB8_RT_Q1A_PAL_COUNTRY15

target: Q1A_PAL

documented condition: COUNTRY==15

applicability: APPLIES_FOR_COUNTRY_15

documentary authority: Wave 8 questionnaire p5

### AB8_RT_Q622C_IRQ_COUNTRY7_SPLITA

target: Q622C_IRQ_*

documented condition: COUNTRY==7 + SPLIT A

applicability: APPLIES_FOR_COUNTRY_7_SPLIT_A

topology: SELECT_ALL_THAT_APPLY

documentary authority: Wave 8 questionnaire p47

Physical missingness, blankness, observed frequency, field naming, or another wave's routing never supplies applicability authority.

All unjoined country/module routing remains BOUNDED_UNKNOWN.

## 7. Q622C_IRQ topology law

The accepted questionnaire supplies select-all topology while the source snapshot has zero native SPSS MR-set metadata.

Therefore:

- Q622C_IRQ member variables remain distinct;
- select-all documentary topology is preserved;
- scalar flattening is forbidden;
- native MR metadata must not be invented;
- physical absence/presence cannot replace documentary routing authority.

This is an EC10 source-module realization, not an EC08 native-MR claim.

## 8. Design / weight carrier law

Preserve all accepted source carriers individually:

WT

PSU

STRATUM

The Wave 8 questionnaire identifies PSU as a sampling variable.

Current authority does not establish a complete analytic design contract.

The following remain BOUNDED_UNKNOWN:

- WT estimand;
- WT normalization;
- WT default use;
- STRATUM design semantics;
- PSU analytic role beyond the documented sampling-carrier statement;
- governed population/cluster/stratum combination.

Presence, completeness, magnitude, field name, or Q1 equality cannot create those semantics.

## 9. Cross-wave firewall

Only Wave 8 source-native documentary authority may close Wave 8 source semantics in this realization.

Wave 1/2/5 labels, code meanings, weight roles, ID rules, routing rules, or typography are not substitutes.

Cross-wave semantic equivalence remains BOUNDED_UNKNOWN until a separate governed continuity authority closes it.

## 10. S35 edge-class binding

Exact applicable classes:

EC01 — FORMAT_FAMILY_SAV_DTA

Preserve exact source identity, row/variable incidence, raw storage, metadata, and replay identity.

EC05 — PHYSICAL_MISSINGNESS_MULTICLASS

Preserve ordinary blank BLOCK_ID separately from physical/system missing. Physical state never creates semantic routing.

EC07 — NATIVE_ID_SCOPE_COLLISION_OR_NONINJECTIVITY

Preserve repeated ID=0 rows and hard-lock replay to source SHA + row ordinal.

EC10 — FORM_MODULE_SKIP_ROUTING_CARRIERS

Preserve Q1A_PAL/Q622C_IRQ and other route/module carriers while applying only exact documentary rules.

EC12 — WEIGHT_DESIGN_MULTIPLICITY_AND_DOMAIN

Preserve WT/PSU/STRATUM individually; do not select/normalize/infer analytical design.

EC14 — COMPOUND_EDGE_INTERACTION_COURT

All constituent invariants must survive simultaneously. It adds no source-special physical adapter.

## 11. R35 physical hooks

R35-I01 schema:

PRE553_PHYSICAL_METADATA@1.0.0

R35-I02 schema for non-direct realizations:

FIABC_DERIVATIVE_PARENTAGE_BUNDLE@1.0.0

R35-I03 schemas:

FIABC_R35_I03_SOURCE_PHYSICAL_SCOPE@1.0.0

FIABC_R35_I03_CANONICAL_PHYSICAL_EXPECTATION@1.0.0

FIABC_R35_I03_CANDIDATE_PHYSICAL_REALIZATION@1.0.0

FIABC_R35_I03_WHOLE_SOURCE_PHYSICAL_EQUIVALENCE_RECEIPT@1.0.0

Required physical dimensions include physical metadata, variable order, raw storage values, physical missing states, missing declarations, source-row replay identity, route/module carriers, and weight/design variables.

These hooks carry no semantic authority and have not been executed here.

## 12. Candidate-neutral handoff

Future qualification order:

SOURCE IDENTITY FREEZE

then ARAB8_SEMANTIC_OWNER_V1 FREEZE

then independent Candidate A/B/C physical realization

then exact R35 physical receipts

then source-specific hostile semantic tests

then common A/B/C comparison.

A/B/C must carry one deterministic source-specific realization identity computed from this complete source law.

Candidate-local semantic reinterpretation is nonconforming.

## 13. Fail-closed and bounded-unknown law

Wrong source SHA:

BLOCKED__CANONICAL_SOURCE_ROOT_UNPROVED

Replay key changed from source SHA + row ordinal:

BLOCKED__REPLAY_IDENTITY_DIVERGENCE

ID=0 deleted/coerced into missing identity:

BLOCKED__NATIVE_ID_PHYSICAL_STATE_LOSS

BLOCK_ID blank coerced to SYSTEM_MISSING/null:

BLOCKED__PHYSICAL_MISSING_STATE_COLLAPSE

Q1/STRATUM aliased from equal vectors:

BLOCKED__UNAUTHORIZED_VARIABLE_ALIAS

Q622C_IRQ flattened or native MR metadata invented:

BLOCKED__MODULE_TOPOLOGY_LOSS_OR_INVENTION

Routing inferred from missingness:

BLOCKED__ROUTING_AUTHORITY_INVENTED

WT/PSU/STRATUM analytic role invented:

BLOCKED__WEIGHT_DESIGN_AUTHORITY_INVENTED

Wave 1/2/5 semantics imported:

BLOCKED__CROSS_WAVE_SEMANTIC_LEAKAGE

Candidate semantic law divergence:

BLOCKED__SEMANTIC_OWNER_DIVERGENCE

Lawful bounded unknowns rather than blockers:

- BLOCK_ID exact semantics;
- blank BLOCK_ID semantic meaning;
- WT estimand and normalization;
- STRATUM design semantics;
- PSU analytic design use beyond its documented sampling-variable role;
- semantic/causal reason Q1 and STRATUM are physically equal;
- country/module routing not closed by an exact Wave 8 documentary rule;
- cross-wave semantic equivalence.

## 14. Claim boundary

This realization proves source-specific implementation only.

It does not prove real-source execution, whole-source physical equivalence, A/B/C execution, I05, measured P2X, or source certification beyond accepted authority.
