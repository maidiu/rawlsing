# Post-G5 runtime hotfix — V550→V551 bridge applicability serialization

This is a post-G5 runtime-acceptance defect discovered by the first real downstream canary after the V550–V552J repair merged to `main`. It is **not** a mutation of the frozen 67-issue register and must not weaken the V551 contract.

Work on branch:
`agent/postg5-v550-v551-bridge-hotfix`

Open a draft PR against:
`main`

## Proven failure

Afrobarometer R1 / Lesotho produced a populated V550 shard (20 QUC rows, 230 response-authority rows, 99,420 bridge rows, 1,177 respondents, 23,540 response rows; V550 readiness `ready`), but V551 v3 rejects the bridge because the persisted bridge Parquet lacks the required column:

`directional_applicability_status`

The bridge builder already computes this field in `_bridge_additional_fields()` from the QUC/current authority contract with fail-closed `APPLICABILITY_UNRESOLVED` fallback. However `write_v551_bridge_index*()` materializes batches with `columns=V551_BRIDGE_INDEX_SCHEMA["required_columns"]`, and the current bridge schema omits `directional_applicability_status`. Pandas therefore silently drops the computed field before publication.

V551 is correct to reject the malformed bridge. **Do not** derive applicability from `directional_certification_status`, `current_directional_atom_eligible`, `directionality_status`, response intensity, or any other weaker/promotability field.

## Mandatory repair

1. Update the canonical V550 bridge schema so `directional_applicability_status` is persisted in `V551_BRIDGE_INDEX_SCHEMA["required_columns"]`, placed with the directional authority/applicability fields.
2. Verify by an explicit set-difference regression that **every** column required by `validate_v551_bridge_input_contract()` is present in the canonical V550 bridge schema. If any sibling omission exists, fix it only if it is already produced by the V550 bridge builder and required by V551; do not invent new semantics.
3. Add a focused serialization regression proving a bridge row with authoritative applicability survives the `DataFrame(..., columns=V551_BRIDGE_INDEX_SCHEMA["required_columns"])` publication path and passes `validate_v551_bridge_input_contract()`.
4. Add `directional_applicability_status` to `QUESTION_USE_CONTRACT_HASH_COLUMNS`. Applicability is now a governed QUC field consumed downstream; the QUC row hash must change if this authority state changes. Preserve all existing hash inputs.
5. Audit V550's empty-QUC/fallback DataFrame column declarations and schema sidecars. Where they enumerate the QUC/bridge contract explicitly, add the applicability field so valid-empty outputs expose the same typed schema as populated outputs.
6. Do not relax V551, do not change V551 signed-projection ownership, and do not infer applicability at V551 runtime.

## Recovery-path requirement

Confirm and document the safe recovery command/path for an already-completed V550 shard. `repair_v550_bridge_artifacts.py` is not sufficient because it starts from the already-persisted malformed bridge and cannot recover a dropped authoritative QUC field. Prefer `rebuild_v550_bridge_from_checkpoints.py`, which reconstructs checkpointed question tables and rebuilds the bridge without rerunning per-question execution. Do not claim a command was executed unless it actually was.

## Secondary J-series diagnosis — no speculative semantic change

The reported Lesotho V550 shard also lacks the shared respondent-substrate Parquet/manifest required by V550J. Diagnose whether this shard was built through a joint-capable orchestration path.

Known current behavior: the canonical all-wave smoke adds `--shared-respondent-substrate-mode write` when a joint registry is resolved. Therefore:
- if the failing invocation was direct/non-joint V550, report the exact J prerequisite flags needed for the next run/replay; do not call that a V550 semantic defect;
- if a canonical orchestration path attempted V550J after building V550 without requesting the shared substrate, identify the exact orchestration defect and include a minimal fix/test in this PR only if it is within the V550/J launch boundary and does not alter V550J semantics.

Do not let this secondary investigation delay the immediate V550→V551 schema correction.

## Write domain

Primary authorized files:
- `data/ddm_build_copy/ddm_v550_schema.py`
- `data/ddm_build_copy/ddm_v550_question_use.py`
- `data/ddm_build_copy/build_determinicity_wave_shard_v550.py` only for explicit empty/fallback schema declarations if required
- W02/post-G5-namespaced tests

Conditional orchestration file(s): only if the J substrate diagnosis proves the canonical launch path is wrong; report evidence before changing it.

Do not edit V551/V552/V550J/V551J/V552J semantic builders unless a test import is needed. Do not edit the frozen issue shards or historical G5 accounting.

## Tests

At minimum:
- V551-required bridge columns ⊆ V550 canonical bridge schema;
- `directional_applicability_status` survives schema-limited bridge serialization;
- authoritative `APPLICABLE_BY_AUTHORITY`, `NOT_APPLICABLE_BY_AUTHORITY`, and `APPLICABILITY_UNRESOLVED` values are preserved exactly;
- row-level certification cannot manufacture applicability;
- QUC hash changes when `directional_applicability_status` changes with all other governed fields held constant;
- valid-empty bridge/schema still carries the field;
- existing W02 V550 boundary tests and focused V551 bridge-input contract tests pass.

Run the strongest executable tests available and report exact commands/results. If the real Afrobarometer shard is not available in the worker environment, do not claim the real canary reran.

## Return

Commit to the assigned branch and open a draft PR against `main`.
Return:
- root cause confirmation;
- exact files changed;
- before/after behavior;
- test commands/results;
- whether any sibling V551-required bridge columns were also missing;
- safe checkpoint-replay recovery invocation shape;
- J-substrate diagnosis and whether it requires a separate fix;
- commit SHA and PR number.
