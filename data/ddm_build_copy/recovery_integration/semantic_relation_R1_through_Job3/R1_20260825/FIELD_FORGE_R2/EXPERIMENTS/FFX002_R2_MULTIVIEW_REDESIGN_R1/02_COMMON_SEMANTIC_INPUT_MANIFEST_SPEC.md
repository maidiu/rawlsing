# COMMON_SEMANTIC_INPUT_MANIFEST — SPECIFICATION

Status: `DESIGN_CANDIDATE__REQUIRED_BY_FFX002_R2__NO_AUTHORITY_MINTED`

## 1. Purpose

The manifest is the exact semantic boundary between governed empirical preparation and representation-local method choice.

It proves that all FFX002 R2 arms are answering questions over the same empirical state universe. It does not itself make observations current, mint TTARs, adjudicate PRA, or restore respondent carriers.

## 2. Required fields

| field | exact content | hardness / owner |
|---|---|---|
| `manifest_schema_version` | exact schema identifier | HARD / FFX002 design |
| `current_execution_sha` | exact accepted execution base | HARD / project currentness |
| `observation_substrate_ref` | immutable governed observation/provenance substrate ref + hash | HARD / project empirical authority |
| `respondent_entity_binding_ref` | exact governed respondent identity carrier/binding | HARD / project authority |
| `exposure_risk_set_ref` | respondent x measurement actual exposure/opportunity materialization + predicate provenance | HARD / project authority |
| `source_scope_ref` | exact source/release/wave/context/form/module/split coordinates required for identity/routing | HARD |
| `source_native_measurement_refs` | exact qimpl/source-variable/measurement identities and source-structure member roles | HARD |
| `qimpl_measurement_binding_refs` | CURRENT qimpl -> CURRENT empirical measurement bindings | HARD |
| `response_state_semantics_ref` | substantive response/value semantics | HARD |
| `special_state_semantics_ref` | DK/refused/not-asked/routed-nonapplicable/not-in-form/unresolved/etc. distinctions | HARD |
| `ttar_execution_sequence` | ordered TTAR IDs + input/output hashes | HARD when any transform occurs |
| `post_transform_state_manifest` | exact state IDs after all lawful semantic transforms | HARD |
| `claim_scope_ref` | mechanically bounded claim scope | HARD |
| `estimand_ref` | exact population/sample target | HARD |
| `weight_design_refs` | exact weight purpose/carrier/design refs or explicit NONE | HARD as estimand requires |
| `analytic_role_authority_refs` | PRA and other role refs governing position/disposition/supplementary/conditioning/diagnostic/exclude | HARD |
| `ancestry_disjointness_receipt` | recursive active position/disposition ancestry check | HARD for cross-space claims |
| `unresolved_noncomparable_manifest` | unresolved/noncomparable states retained as first-class | HARD |
| `source_native_ancestry_ref` | replayable ancestry beneath project/analytic identity | HARD |
| `loss_profile` | cumulative inherited + project-authorized information loss, typed by transform | HARD |
| `holdout_generation_inputs_hash` | inputs permitted to generate the partition; not final outcomes | HARD before execution |
| `canonicalization_spec` | field ordering, encoding, null/list rules, hash algorithm | HARD |
| `manifest_hash` | content hash computed after canonicalization excluding this field itself | HARD |

No descriptive labels, prose interpretation, axis names, or decorative metadata belong in the hash boundary unless required to distinguish governed semantic identity.

## 3. Canonicalization

Recommended canonical payload:
- UTF-8;
- sorted object keys;
- arrays retain semantically meaningful declared order;
- set-valued arrays sort by immutable ID;
- explicit typed null vs empty collection;
- no timestamps unless time is part of semantic identity;
- hash algorithm fixed by execution authority, preferably SHA-256.

`manifest_hash = HASH(canonical_payload_without_manifest_hash)`

Each arm emits:
- `arm_id`;
- `received_manifest_hash`;
- independently recomputed `manifest_hash`;
- `attestation_status`.

Only `ATTESTED_EQUAL` may proceed.

## 4. What MUST occur before the fork

Any operation that changes at least one of these propositions:

- `SAME_STATE`
- `DIFFERENT_STATE`
- `ORDER_RELATION`
- `CATEGORY_MEMBERSHIP`
- `COMPARABLE_FOR_CLAIM`
- `SEMANTIC_ELIGIBILITY`
- `SPECIAL_STATE_IDENTITY`
- `EMPIRICAL_UNIT_IDENTITY`
- `RISK_SET_MEMBERSHIP`
- `ESTIMAND_IDENTITY`
- `ANALYTIC_ROLE_ADMISSION`

Examples:
- category collapse or regrouping;
- binning continuous values;
- ordinal reordering;
- string/category crosswalks;
- source-version harmonization;
- DK/refused/nonapplicable pooling;
- semantic eligibility exclusions;
- claim-scope transport mapping;
- PRA changes.

Such an operation requires typed authority. Where it is a semantic/equivalence transform, it requires TTAR ancestry and ordered execution before the representation fork.

## 5. What MAY occur after the fork

A representation-local operation is permitted only if the frozen semantic state identity and eligibility remain unchanged.

Permitted examples:
- geometry dimension retention;
- regularization;
- metric selection from preregistered lawful families;
- nonsemantic display rotation;
- configuration indexing;
- compact summary pruning that never deletes underlying source facts;
- conditional estimator choice;
- smoothing across observations while predictions remain over the same frozen outcome states;
- graph layout;
- latent optimizer choice under a preregistered model.

If an operation needs a merged state, changed order, new eligibility rule, or altered risk set, it is not method-local.

## 6. Common-input variants

A semantically lawful sensitivity analysis may create a new common variant:

`CSI_VARIANT_ID = HASH(parent_manifest_hash + authorized_delta_ttar_refs + new_claim_or_estimand_ref_if_any)`

All arms must receive that new manifest independently.

Never compare:
- geometry on semantic variant V2
against
- configuration/conditional on semantic variant V1
as if the difference were representation sensitivity.

That is input sensitivity.

## 7. Fail-closed statuses

- `COMMON_INPUT_ATTESTED`
- `COMMON_INPUT_MISSING_HARD_FIELD`
- `COMMON_INPUT_UNRESOLVED_AUTHORITY`
- `COMMON_INPUT_TTAR_SEQUENCE_UNPROVED`
- `COMMON_INPUT_ANCESTRY_UNREPLAYABLE`
- `COMMON_INPUT_ARM_HASH_DIVERGENCE`
- `COMMON_INPUT_RISK_SET_DIVERGENCE`
- `COMMON_INPUT_ESTIMAND_DIVERGENCE`

Any non-attested state blocks FFX002 R2 execution.
