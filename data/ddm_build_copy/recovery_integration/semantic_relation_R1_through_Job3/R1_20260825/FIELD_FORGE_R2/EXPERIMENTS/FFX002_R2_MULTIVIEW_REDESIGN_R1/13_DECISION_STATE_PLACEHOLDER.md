# FFX002 R2 — DECISION-STATE PLACEHOLDER / DISAGREEMENT HOOK

Status: `INTERIM_EXPERIMENT_OUTPUT_GRAMMAR__NOT_FINAL_CROSS_VIEW_DISAGREEMENT_DOCTRINE`

## 1. Why this is a placeholder

The experiment must be executable without waiting for a future general doctrine of multi-view disagreement. It therefore emits typed evidence sufficient for later adjudication without inventing a universal rule now.

No majority vote among methods. No master score.

## 2. Hard-invalid states

These are immediately usable:

- `EXPERIMENT_INVALID__COMMON_INPUT`
- `EXPERIMENT_INVALID__POSTFORK_SEMANTIC_DIVERGENCE`
- `EXPERIMENT_INVALID__RESPONDENT_OR_EXPOSURE_AUTHORITY`
- `EXPERIMENT_INVALID__ESTIMAND_DIVERGENCE`
- `EXPERIMENT_INVALID__ANCESTRY_CONTAMINATION`
- `EXPERIMENT_INVALID__HOLDOUT_LEAKAGE`
- `EXPERIMENT_INVALID__PROVENANCE_UNREPLAYABLE`

An invalid experiment cannot identify a losing view.

## 3. View-level result candidates

After hard gates:

- `VIEW_REDUNDANT`
- `VIEW_ADDS_INCREMENTAL_VALUE`
- `VIEW_ADDS_VALUE_BUT_DESTROYS_CRITICAL_INVARIANT`
- `VIEW_INVALID_ON_CANARY`
- `VIEW_METHOD_SENSITIVE`
- `WEAKER_VIEW_SUFFICIENT`
- `MULTI_VIEW_RETENTION_REQUIRED`
- `REPRESENTATION_DEPENDENCE_MATERIAL`
- `NO_MATERIAL_ROLE_SEPARATION_ON_CANARY`

These statuses may co-occur as structured fields rather than being forced into one scalar winner.

## 4. Required disagreement payload

When two lawful views materially differ, emit:

`VIEW_DISAGREEMENT {
  query_id;
  common_manifest_hash;
  view_a;
  view_b;
  view_a_answer_ref;
  view_b_answer_ref;
  material_difference_metric;
  invariants_required_by_query;
  invariant_status_a;
  invariant_status_b;
  loss_manifest_a;
  loss_manifest_b;
  hostile_status_a;
  hostile_status_b;
  support_uncertainty_a;
  support_uncertainty_b;
  representation_specific_claims[];
  unresolved_reason;
}`

This is enough for a later FFIF004-style court to distinguish invalidity, different invariant preservation, insufficient evidence, or nonreducible representation dependence.

## 5. Provisional terminal experiment states

A future execution worker may return one of these bounded summaries while preserving the full vector:

- `WEAKER_VIEW_SUFFICIENT`
- `MULTI_VIEW_RETENTION_REQUIRED`
- `ONE_OR_MORE_VIEWS_INVALID_ON_CANARY`
- `REPRESENTATION_DEPENDENCE_MATERIAL__DOCTRINAL_HANDOFF_REQUIRED`
- `NO_MATERIAL_ROLE_SEPARATION_ON_CANARY`
- typed experiment invalid state.

It may not return `MASTER_REPRESENTATION_SELECTED`.

## 6. Supersession hook

A later accepted disagreement doctrine may replace the mapping from evidence vector to terminal summary without changing:
- common semantic input law;
- raw view outputs;
- invariant registry;
- loss manifests;
- hostile results;
- query results;
- ablation results.

That separation prevents future interpretation doctrine from contaminating experiment production.
