# Section 85 Binding Authority

This directory contains the canonical binding surface for bounded Section 85
diagnostic orchestration. Runners and gates read these files before assuming
database relation names, source aliases, stage output locations, or producer
readiness semantics.

## Active files

- `section85_binding_authority.json` — repository-relative path rules, database
  bindings, privacy rules, active runners, and exact merged producer versions.
- `section85_typed_stage_contract.json` — executable Section85 acceptance
  contract for run integrity, evidence state, downstream permission, exact
  producer identity, canonical Parquet declarations, and serialized hashes.
- `section85_stage_artifact_authority.csv` — historical 2026-08-04 observation
  ledger retained for provenance only. Its old row-count/readiness prose is not
  executable authority.

## G4 exact producer boundary

Gate G4 is merged. Section85 no longer has any `AWAITING_G3B_PRODUCER_HOOK` or
`AWAITING_G4_PRODUCER_HOOK` acceptance path.

The active V551J producer contract is:

- shared boundary: `rawlsing_pipeline_boundary_v1`
- schema: `v2.2.3`
- compiler: `v551j_joint_evidence_contract_v2_2_3`

The active V552J producer contract is:

- shared boundary: `rawlsing_pipeline_boundary_v1`
- schema: `v1.0`
- compiler: `v552j_structural_join_v1`

Before a producer surface is used, Section85 verifies the exact supported
contract/schema/compiler version, typed `run_integrity_status`,
`evidence_status`, and `downstream_permission_status`, exact run/source/wave and
country-or-shard identity, manifest-declared canonical Parquet artifacts,
producer-declared `artifact_file_sha256`, declared row counts, and artifact
scope. V552J additionally rehashes the exact V551J and V552 producer manifests
recorded in its own lineage block.

The following are never readiness authority:

- a nonempty JSON object;
- a nonzero artifact or packet count;
- `ready_for_review`;
- `ready_for_v552j_joint_evidence`;
- a free-text `READY_*` label;
- historical filename aliases.

## Typed state distinctions

Run integrity, evidence state, and permission are separate questions.

For V551J, all of these can describe a healthy producer run:

- `PASS / PRESENT / ALLOW` — certified evidence may be consumed by the
  evidence-dependent operation;
- `PASS / PRESENT / DENY` — valid review-only evidence exists, but the
  evidence-dependent operation is not authorized;
- `PASS / VALID_EMPTY / NOT_APPLICABLE` — the producer completed coherently and
  emitted no joint evidence;
- `PASS / NOT_APPLICABLE / NOT_APPLICABLE` — the branch is non-applicable;
- `PASS / APPLICABLE_UNRESOLVED / DENY` — applicable repair debt or unresolved
  evidence remains explicit.

For V552J, `VALID_EMPTY`, `NOT_APPLICABLE`, and `APPLICABLE_UNRESOLVED` remain
separate from observed numeric zero. `OBSERVED_ZERO` is accepted only as an
observed measurement row in the canonical structural join, with an actual zero
pressure value and the producer's explicit observed-zero contract. It is never
manufactured from missing or unresolved evidence.

## Preserved V551 boundary

W01's resolved V551 v3.0 adaptation remains intact. V551 uses
`rawlsing_pipeline_boundary_v1`, schema/compiler `v3.0`, and the three canonical
Parquet artifacts:

- `directional_candidate_adjudication.parquet`
- `relation_evidence_atoms.parquet`
- `directional_distribution_coverage.parquet`

Zero relation-evidence atoms do not by themselves fail run integrity.

## Delegated implementations

`_legacy_run_section85_diagnostic_smoke_matrix.py` and
`_g2_run_bounded_nine_v550j_v551j_v552j.py` are preserved implementation
modules, not alternate acceptance authorities. They are loaded only through the
active Section85 entrypoints, which replace obsolete producer-consumer gates
before execution.

## Repository-relative path rule

The curated source transfer moved this package to `section85/`. Historical
ledger paths may still contain the former package prefix or Desktop observation
paths. Neither is executable authority.

Before a historical ledger `canonical_reference` is used as a path reference,
apply `canonical_reference_rebase` from `section85_binding_authority.json`. The
legacy package prefix maps to `section85/`; if it survives normalization,
execution fails closed. `observed_latest_path` is provenance only.

Active Section85 code uses repository-relative `section85/`,
`data/ddm_build_copy/`, and `data/ddm_registries/` paths.

## Mandatory database bindings

- QSM relation: `question_structural_mapping`
- Canonical registry relation:
  `rawlsing_authority_reconcile_ar_20260719t213835z.canonical_question_registry`
- Preferred respondent relation:
  `public.v_ddm_response_long_facet_ready_authority`

The stale relation
`rawlsing_authority_reconcile_ar_20260719t213835z.question_structural_mapping`
is forbidden for Section85 diagnostics.

## Privacy boundary

`v550_shared_respondent_substrate.parquet` is runtime-private respondent-level
data. It may be used by V550/V550J execution but must not be copied into ordinary
nonrespondent diagnostic packages, Git, or later handoff ZIPs.
