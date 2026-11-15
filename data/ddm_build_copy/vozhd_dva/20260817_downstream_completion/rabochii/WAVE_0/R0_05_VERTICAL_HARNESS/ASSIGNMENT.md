# R0-05 — Vertical Fixture and Continuity Test Harness

## Identity

- **Worker ID:** R0-05
- **Branch:** `agent/vozhd-dva-r0-05-vertical-harness`
- **Target PR base:** `agent/vozhd-dva-wave0-integration`
- **Prong:** vertical fixtures / executable downstream continuity

## Mission

Build the smallest useful test/fixture infrastructure that lets Vozhd Dva and later implementation workers prove semantic continuity across V553→V558. The harness should expose information loss and jurisdiction violations early without requiring the full 35-wave corpus or finished V3/V2.

This is the main Wave-0 infrastructure task besides the isolated `POSTG5-004` repair. The worker may add test/fixture code, but may **not** change stage production semantics to make the tests pass.

## System position

`reference upstream structural/temporal inputs → V553 → V554 → V555 → V556 → V557 → V558 → reference consumer assertions`

The harness is not a toy persona generator. It is a semantic continuity court for a small finite set of hard cases.

## Canonical read set — read in order

1. `data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/README.md`
2. `data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/CONSTRAINTS_PRIORITIES.md`
3. `data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/CAPABILITY_MATRIX.md`
4. `data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/STRATEGY_AND_GATES.md`
5. `data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/rabochii/WAVE_0/README.md`
6. `data/ddm_build_copy/ddm_v5_build_standard.py`
7. `data/ddm_build_copy/ddm_v5_walking_skeleton.py`
8. `data/ddm_build_copy/ddm_v5_thin_end_to_end.py`
9. `data/ddm_build_copy/ddm_pipeline_boundary_contract.py`
10. `data/ddm_build_copy/ddm_pipeline_boundary_consumer.py`
11. `data/ddm_build_copy/ddm_pipeline_final_contracts.py`
12. `data/ddm_build_copy/ddm_v553_schema.py`
13. `data/ddm_build_copy/ddm_v553_temporal_pressure.py`
14. `data/ddm_build_copy/ddm_v554_seed_contract.py`
15. `data/ddm_build_copy/ddm_v555_life_course_mediation.py`
16. `data/ddm_build_copy/ddm_v556_pressureflow.py`
17. `data/ddm_build_copy/ddm_v557_renderer_contract.py`
18. `data/ddm_build_copy/ddm_v558_runtime_input_gate.py`
19. `data/ddm_build_copy/tests/test_w05_final_cross_stage.py`
20. `data/ddm_build_copy/tests/test_w05_pipeline_boundary_contract.py`
21. `data/ddm_build_copy/test_w06_downstream_typed_state_watchers.py`
22. `data/ddm_build_copy/test_w03_v551j_v3_fail_closed.py`

## Frozen external facts

- Current thin-build success does not prove downstream semantic continuity.
- The harness must distinguish artifact-shape success from semantic-preservation success.
- Tests should fail when a required distinction is silently dropped, even if all stage processes exit successfully.
- The five finite vertical slices are fixed Wave-0 targets:
  1. temporal persistence / drift / rupture;
  2. contradictory inter-strata pressure;
  3. mediation with buffering / amplification;
  4. pressure-flow with attractor prerequisites;
  5. uncertainty / absence / noncomparability / forbidden inference.
- Enneagram-like attractor formation is part of the design, but this harness tests prerequisites/continuity, not finished personality assignment.
- V553–V558 may not emit concrete biography, psyche, dialogue, or persona facts.

## Fixture design requirements

Prefer a compact, deterministic, synthetic/reference fixture that can exercise multiple slices without becoming a second data model. It should contain enough typed structure to represent:

- at least two time points/waves with one persistent relation, one drift, and one rupture-like change;
- at least two structural pressures that conflict or pull in different directions;
- at least one mediation route with a buffering/amplifying condition;
- enough route information to test that pressure-flow/attractor prerequisites survive downstream;
- explicit uncertainty;
- explicit absence or noncomparability distinct from zero/neutral;
- provenance/authority identifiers that can be checked for survival;
- a forbidden direct-persona inference case that must fail closed.

The worker may use mocks/reference packets when production stages cannot yet express the intended semantics, but every mock must state which future producer obligation it represents.

## Authorized write domain

The worker may create new test/fixture infrastructure under a dedicated namespace such as:

- `data/ddm_build_copy/tests/vozhd_dva_wave0/`
- `data/ddm_build_copy/tests/fixtures/vozhd_dva_wave0/`

or another equally isolated test-only location consistent with repository conventions.

The worker may add helper code used only by these tests if necessary.

Worker report files:

- `data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/rabochii/WAVE_0/R0_05_VERTICAL_HARNESS/RESULT.md`
- `.../R0_05_VERTICAL_HARNESS/RESULT.json`

## Prohibited scope

- No production semantic edits to V553–V558.
- No changes to V550–V552J.
- No full-data 35-wave qualification in this assignment.
- No V3/V2 implementation.
- No weakening assertions just because current scaffolds cannot satisfy them; mark expected/current gaps explicitly instead.

## Required work

1. Inventory existing cross-stage test conventions and reusable helpers.
2. Define the fixture grain and stable identifiers.
3. Implement a deterministic fixture/fixture builder.
4. Implement executable assertions for the five slices where current contracts make this possible.
5. Where a slice cannot yet traverse production code, create a clearly marked reference-consumer/expected-contract test that demonstrates the missing obligation without pretending it passes today.
6. Add assertions separating semantic readiness from process/artifact-shape readiness.
7. Add at least one information-loss failure case.
8. Add at least one forbidden-inference/fail-closed case.
9. Keep runtime cost small enough for routine PR use.
10. Return a mapping from each test to the producer/consumer capability it protects.

## Acceptance evidence

At minimum:

- deterministic fixture(s);
- runnable focused test command;
- clear PASS/expected-fail/current-gap accounting;
- five-slice coverage map;
- one semantic-loss detector;
- one forbidden-inference detector;
- no production semantic modifications.

If current stages prevent all five slices from executing end-to-end, that is acceptable in Wave 0: encode the missing contracts cleanly and report the blocked slices. Do not fake green status.

## Return format

Use `rabochii/WAVE_0/REPORT_FORMAT.json` exactly for `RESULT.json`. `RESULT.md` should include:

1. fixture design;
2. test inventory;
3. current pass/fail/gap matrix by vertical slice;
4. producer-consumer obligations surfaced by failures;
5. recommendations for Wave 1 CI placement.

Open a draft PR against `agent/vozhd-dva-wave0-integration`. Do not merge it.
