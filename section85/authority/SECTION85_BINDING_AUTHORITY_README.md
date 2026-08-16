# Section 85 Binding Authority

This directory contains the canonical binding surface for bounded Section 85
diagnostic orchestration. Runners and gates read these files before assuming
database relation names, source aliases, stage output locations, or producer
readiness semantics.

## Files

- `section85_binding_authority.json`
  Governing DB relation bindings, source-family aliases, stage order, privacy
  rules, the repository-relative path rebase, and the active typed-stage
  acceptance contract reference.

- `section85_typed_stage_contract.json`
  Active Section 85 acceptance authority for producer run integrity, evidence
  state, downstream permission, and producer-bound artifact identity. At Gate
  G2, V551 v3.0 is frozen and active here. V551J/V552/V552J entries name the
  exact producer hooks still required after G3A/G3B/G4 without inventing their
  not-yet-merged stage semantics.

- `section85_stage_artifact_authority.csv`
  Historical per-scope, per-stage observation ledger retained for provenance.
  Rows include artifact references and 2026-08-04 observed paths/hashes. Its
  historical prose -- including the old V551 `row count must be nonzero for
  pass` wording -- is **not executable readiness authority**.

## Typed producer-state rule

Section 85 no longer treats any of the following as proof of a healthy or
usable producer run:

- a nonempty JSON object;
- a nonzero artifact row count;
- `ready_for_review` / `ready_for_v552j_joint_evidence` booleans;
- packet/certified/review cardinality by itself;
- free-text readiness labels.

Current producer acceptance uses `rawlsing_pipeline_boundary_v1` and keeps three
questions separate:

1. `run_integrity_status` -- did the producer safely and coherently complete?
2. `evidence_status` -- what evidence state was actually produced?
3. `downstream_permission_status` -- is the requested evidence-dependent
   operation authorized?

A valid no-evidence or repair-only producer may therefore have integrity `PASS`
without permission to perform an evidence-dependent downstream operation. That
is not compiler failure and it is not observed numeric zero.

### V551 at Gate G2

V551 v3.0 is frozen. Section 85 requires its typed producer manifest, exact run
and source/wave/country-or-shard identity, and the producer-declared
`artifact_file_sha256` for all three canonical Parquet artifacts:

- `directional_candidate_adjudication.parquet`
- `relation_evidence_atoms.parquet`
- `directional_distribution_coverage.parquet`

`relation_evidence_atoms` may contain zero rows. Zero rows do **not** fail run
integrity when the V551 v3.0 manifest is internally valid and reports a lawful
typed evidence state such as `NOT_APPLICABLE` or `APPLICABLE_UNRESOLVED`.

### Pending producer hooks

The generic Section 85 typed-state adapter is ready for V551J and V552J, but
their final producer contracts are not frozen at Gate G2. Until those workers
merge:

- V551J executable acceptance is `AWAITING_G3B_PRODUCER_HOOK`.
- V552 executable acceptance is `AWAITING_G3A_PRODUCER_HOOK`.
- V552J executable acceptance is `AWAITING_G4_PRODUCER_HOOK`.

The required hook is not a guessed filename or boolean. It is the producer's
actual shared-boundary document with final schema/contract version, typed
integrity/evidence/permission fields, exact producer scope identity, and
producer-declared artifact-file SHA-256 values.

## Repository-relative path rule

The curated source transfer moved this package to `section85/`. The artifact
ledger is retained as historical evidence, so some rows still carry the former
package prefix and historical Desktop observation paths. Neither is executable
authority.

Before a historical ledger `canonical_reference` is used as a path reference,
consumers apply `canonical_reference_rebase` from
`section85_binding_authority.json`. The exact legacy package prefix maps to
`section85/`; if a legacy prefix survives normalization, execution fails closed.
`observed_latest_path` is provenance only and must never resolve current
artifacts.

Active Section 85 code, tests, and execution instructions use repository-relative
`section85/`, `data/ddm_build_copy/`, and `data/ddm_registries/` paths only.

## Mandatory Database Bindings

- QSM relation: `question_structural_mapping`
- Canonical registry relation:
  `rawlsing_authority_reconcile_ar_20260719t213835z.canonical_question_registry`
- Preferred respondent relation:
  `public.v_ddm_response_long_facet_ready_authority`

The stale relation
`rawlsing_authority_reconcile_ar_20260719t213835z.question_structural_mapping`
is explicitly forbidden for Section 85 diagnostics.

## Historical V551J compatibility notes

Old Section 85 material recorded compatibility mappings among V551J review and
readiness filenames. Those mappings remain provenance/diagnostic notes only.
They cannot establish current run integrity, evidence status, downstream
permission, contract version, producer identity, or artifact hash. In
particular, a legacy ready boolean cannot substitute for the G3B producer-bound
typed contract.

## Privacy Boundary

`v550_shared_respondent_substrate.parquet` is runtime-private respondent-level
data. It may be used by V550/V550J resume or no-database execution, but it must
not be copied into ordinary nonrespondent diagnostic packages, Git, or later
handoff ZIPs.
