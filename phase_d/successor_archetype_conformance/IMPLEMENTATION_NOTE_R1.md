# Phase-D Closeout Implementation Note

## Governing separation

V550 diagnostic empirical surfaces are aggregate, same-respondent observation
surfaces. They are not semantic certification surfaces and remain
`diagnostic_artifact=true` and `not_direct_evidence=true`. V551 relation
evidence remains behind the full semantic-certification gate.

The implementation defect was that the three V550 diagnostic permissions were
derived from the same `v551` gate as V551 relation evidence. This erased lawful
co-travel when a governed member was semantically blocked or uncertified.

The repaired model derives diagnostic eligibility from observationally
admissible QUC facts: a response-semantics contract hash, a non-technical
topology, and a semantic role that is either relation evidence or structural
context. Structural context can be a diagnostic feature, but never an anchor
and never V551 relation evidence. Admin, technical, and missingness fields
remain excluded.

## Exact control points

- `derive_question_use_eligibility()` controls V551 versus diagnostic QUC
  permissions.
- `ddm_v550_question_use.py` carries those permissions without resetting them
  merely because directional atom certification is false.
- `ddm_v550_clouds.py` preserves diagnostic structural-context features and
  emits relation-anchor/context-feature co-travel without semantic promotion.
- `compile_positioned_relational_evidence.py` scans an explicit allowlist and
  resolves cloud anchor/cotravelling variables through exact governed
  implementation-ID crosswalks.

No semantic authority, Job-3 decision, frozen candidate order, routing truth,
threshold, or V550J authority was changed.
