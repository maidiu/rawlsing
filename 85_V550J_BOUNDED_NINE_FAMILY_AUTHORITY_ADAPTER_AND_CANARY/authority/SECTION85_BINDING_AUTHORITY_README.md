# Section 85 Binding Authority

This directory now contains the canonical binding surface for bounded Section 85
diagnostic orchestration. Runners and gates should read these files before
assuming database relation names, source aliases, stage output locations, or
legacy artifact names.

## Files

- `section85_binding_authority.json`
  Governing DB relation bindings, source-family aliases, stage order,
  V551J compatibility aliases, and privacy rules.

- `section85_stage_artifact_authority.csv`
  Per-scope, per-stage artifact references for the nine-family 20-variable
  diagnostic surface. Rows include the canonical reference path, the latest
  observed path when available from the 2026-08-04 rerun evidence, and SHA-256
  for observed artifacts.

## Mandatory Database Bindings

- QSM relation: `question_structural_mapping`
- Canonical registry relation:
  `rawlsing_authority_reconcile_ar_20260719t213835z.canonical_question_registry`
- Preferred respondent relation:
  `public.v_ddm_response_long_facet_ready_authority`

The stale relation
`rawlsing_authority_reconcile_ar_20260719t213835z.question_structural_mapping`
is explicitly forbidden for Section 85 diagnostics.

## Compatibility Boundary

Some V551J downstream gates were written against older or stricter artifact
names. The authority file records these as compatibility aliases. A runner may
map from the current emitted artifact to the legacy expected artifact only after
checking that the required semantic fields are present.

Do not treat a renamed V551J artifact as missing authority. Also do not pass a
gate merely because an alias exists. The payload still has to satisfy the
functional contract.

## Privacy Boundary

`v550_shared_respondent_substrate.parquet` is runtime-private respondent-level
data. It may be used by V550/V550J resume or no-database execution, but it must
not be copied into ordinary nonrespondent diagnostic packages, Git, or later
handoff ZIPs.
