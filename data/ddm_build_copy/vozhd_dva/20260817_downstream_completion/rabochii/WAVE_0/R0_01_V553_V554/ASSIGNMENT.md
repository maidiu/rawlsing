# R0-01 — V553/V554 Boundary, POSTG5-004, and Information Preservation

## Identity

- **Worker ID:** R0-01
- **Branch:** `agent/vozhd-dva-r0-01-v553-v554`
- **Target PR base:** `agent/vozhd-dva-wave0-integration`
- **Prongs:** V553 entry/temporal semantics; V553→V554 producer-consumer continuity
- **Known issue:** `POSTG5-004`

## Mission

Repair the already-adjudicated V552J→V553 consumer mismatch and perform a bounded producer/consumer audit of the current V553→V554 boundary. Determine what canonical V552J information V553 actually consumes, what V553 produces, what V554 consumes, which distinctions are preserved or transformed, and where downstream starvation or silent loss is already visible.

This is **not** a general V553 or V554 redesign. The worker may implement the isolated `POSTG5-004` repair and the tests needed to prove it. All broader semantic changes are findings for Vozhd Dva adjudication.

## System position

`canonical V552J handoff/index artifacts → V553 temporal harmonization/pressure semantics → V554 seed/structural affordance contract → later mediation/pressure-flow consumers`

The worker must protect both sides of the seam: V553 must consume current V552J lawfully, and its outputs must retain enough typed temporal/structural information for V554 and later vertical slices.

## Canonical read set — read in order

1. `data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/README.md`
2. `data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/CONSTRAINTS_PRIORITIES.md`
3. `data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/CAPABILITY_MATRIX.md`
4. `data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/rabochii/WAVE_0/README.md`
5. `data/ddm_build_copy/issue_register/20260816/index.json` — specifically `POSTG5-004` and `POSTG5-005`.
6. `data/ddm_build_copy/ddm_v552j_handoff.py`
7. `data/ddm_build_copy/ddm_v552j_schema.py`
8. `data/ddm_build_copy/compile_v552j_structural_handoff.py`
9. `data/ddm_build_copy/compile_v552j_runtime_safe_structural_handoff.py`
10. `data/ddm_build_copy/ddm_v553_repo_discovery.py`
11. `data/ddm_build_copy/ddm_v553_harmonization.py`
12. `data/ddm_build_copy/ddm_v553_temporal_identity.py`
13. `data/ddm_build_copy/ddm_v553_schema.py`
14. `data/ddm_build_copy/ddm_v553_temporal_pressure.py`
15. `data/ddm_build_copy/compile_v553_wave_harmonization.py`
16. `data/ddm_build_copy/compile_v553_wave_harmonization_from_repo.py`
17. `data/ddm_build_copy/compile_v553_temporal_pressure_field.py`
18. `data/ddm_build_copy/ddm_v554_seed_contract.py`
19. `data/ddm_build_copy/compile_v554_thin_layer.py`
20. `data/ddm_build_copy/ddm_v5_build_standard.py`
21. `data/ddm_build_copy/ddm_v5_thin_end_to_end.py` — only the V552J→V554 orchestration portions.

Inspect existing tests touching V552J/V553 handoff behavior as needed, especially `data/ddm_build_copy/test_w06_v552j_join.py` and `data/ddm_build_copy/tests/test_w05_final_cross_stage.py`.

## Frozen external facts

- Current repository code is the implementation authority.
- V550–V552J are closed by default.
- `POSTG5-004` has already ruled that the obsolete contract is repaired **on the V553 consumer side**. Do not modify V552J merely to recreate a legacy packet.
- V553 is responsible for temporal/cross-wave structural semantics, not actor biography or psyche.
- V554 may transform V553 output into bounded affordances, but it may not silently erase distinctions later mediation/pressure-flow consumers need.
- Negative authority, absence, noncomparability, uncertainty, contradiction, and provenance are meaningful states and must not be collapsed into generic emptiness.

## Upstream contract

Treat current canonical V552J outputs as the admissible producer surface, including the current structural join/input/handoff indexes and V553 handoff manifest exposed by the V552J implementation. Determine their exact filenames/columns from code; do not infer an obsolete packet into existence.

## Downstream obligations

Audit whether V553 provides V554 with enough information to support at least:

- temporal identity and historical coordinate;
- persistence/drift/rupture distinctions;
- structural/relation/target/driver/channel identity where authorized upstream;
- direction/magnitude or component information where lawfully derivable;
- uncertainty/confidence and comparability status;
- absence/noncomparability/negative-authority distinctions;
- lineage back to V552J evidence/structural authority;
- enough typed structure to avoid forcing V554 to reconstruct semantics from labels.

Do not decide V555/V556 semantics. If a downstream need is visible, record it as a producer-consumer obligation.

## Authorized write domain

Production changes are limited to the V553 consumer-side repair required by `POSTG5-004`, plus narrowly necessary V553 tests/fixtures. Expected files include only where actually required:

- `data/ddm_build_copy/ddm_v553_repo_discovery.py`
- `data/ddm_build_copy/ddm_v553_harmonization.py`
- `data/ddm_build_copy/ddm_v553_temporal_pressure.py`
- `data/ddm_build_copy/compile_v553_wave_harmonization*.py`
- new focused tests under `data/ddm_build_copy/tests/` or `data/ddm_build_copy/test_*` following existing conventions.

Do not change V554 production semantics in Wave 0. Audit it and report findings.

Worker report files:

- `data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/rabochii/WAVE_0/R0_01_V553_V554/RESULT.md`
- `.../R0_01_V553_V554/RESULT.json`

## Prohibited scope

- No V550/V550J/V551/V551J/V552/V552J changes unless the worker first proves the consumer-side repair is impossible and returns a cross-hook.
- No V555+ production changes.
- No actor generation, persona, biography, psyche, dialogue, or Enneagram assignment.
- No general source-family redesign.

## Required work

1. Reproduce/code-trace `POSTG5-004` precisely.
2. Repair V553 to consume the canonical V552J output surface.
3. Add focused tests proving current canonical artifacts are accepted and the obsolete packet is not required.
4. Inventory the semantically relevant fields/states entering V553 from V552J.
5. Inventory V553 outputs relevant to V554.
6. Trace V554 consumption/transformation of those outputs.
7. Identify each meaningful information loss, conflation, reconstruction, or unjustified placeholder as a finding.
8. Identify each V553 field/state that later vertical slices will need preserved.
9. Do **not** implement broad semantic deepening; return the requirements to Vozhd Dva.

## Acceptance evidence

At minimum:

- focused tests for the `POSTG5-004` repair;
- evidence that canonical V552J artifacts can drive the V553 consumer path without the obsolete packet;
- a producer→consumer field/state trace in `RESULT.md`;
- explicit findings for any semantic loss or downstream requirement;
- no modifications outside authorized scope.

## Return format

Use `rabochii/WAVE_0/REPORT_FORMAT.json` exactly for `RESULT.json`. `RESULT.md` should summarize:

1. repair performed;
2. tests;
3. V552J→V553 contract as actually observed;
4. V553→V554 preservation/loss table;
5. cross-hooks requiring Vozhd Dva adjudication.

Open a draft PR against `agent/vozhd-dva-wave0-integration`. Do not merge it.
