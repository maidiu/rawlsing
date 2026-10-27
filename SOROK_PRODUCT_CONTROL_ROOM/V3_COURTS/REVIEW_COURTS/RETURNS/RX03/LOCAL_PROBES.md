# RX03 independent sourcefree probes

**Date:** 2026-10-26. **Target:** X03 `e81dd633b419d35619014bdf99f894ad4f98c5a5`. **Surface:** local macOS / OpenCode / DeepSeek V4.1-Flash selected session; no LLM/provider call. **Source:** `/Users/matthewsmith/Desktop/Rawlsing/Rawlsing_code_bundle_staging`, read-only, with `PYTHONDONTWRITEBYTECODE=1` and `python3 -B`.

## P1 — source identity

```text
X03 SOURCE_IDENTITIES: 35 files; 35/35 SHA-256 exact; 0 missing.
S50 selected manifest: 31/31 exact.
Local staging zip: 3f2c5ed925273153a4f300f75e54524729f0b4fef9974957be1f3cd887c91289
TD-R05 archive:  953c9149bd03877206e3cb440d1f4db35dea6473af30b97fd23b7e76c6fc0086
```

Whole-archive identity is not claimed; file-level identity is exact.

## P2 — 71 focused tests

```sh
RAWLSING_STAGING_ROOT=<source> PYTHONDONTWRITEBYTECODE=1 \
python3 -B <X03>/TEST_SOURCE_AND_LOGS/run_v3_tests.py \
  v3/tests/test_metabolization_effects.py \
  v3/tests/test_step_logic.py \
  v3/tests/test_v5_framework_dormancy.py \
  v3/tests/test_invariants.py \
  v3/tests/test_wave4.py \
  v3/tests/test_architecture_invariants.py \
  v3/tests/test_step_sanity.py \
  v3/tests/test_llm_contract.py \
  v3/tests/test_v5_baseline_load.py \
  v3/tests/test_v5_alienation.py
```

Result: **71 passed in 16.96s**. X03 reports 71 passed in 14.55s; count reproduced, timing differs. The full `v3/tests` suite was **not** run by RX03; X03's full-suite attempt stopped after 15 collected tests at 180s and is not counted as a pass/fail.

## P3 — X03 probe rerun

`probe_x03.py` completed with exit 0. Key independent observations:

```text
cracks default: 2 active placeholders (intensity 5, latent 5)
framework synthetic: binding 51.5, 53.0, 51.5 across 3 calls (acute/acute/chronic)
practice child: study 25, care 30, organizing 35, craft 35, spiritual 80, risk 20
practice adult: study 55, care 26, organizing 19, craft 33, spiritual 50, risk 18
topology: self_contained counter 1 -> reciprocal on call 2
boundary: universal -> universal without gate; universal -> expanding at repression 75
rupture malheur event: process severity micro, status raw; create-only wounds unchanged
direct malheur wound update: abandonment 50 -> 69
three update years: status raw; plasticity 3 -> 0; IRR 60 -> 60; narrators empty
stability: raw inertia 20 -> 19.88675; manual integrated 20 -> 14.7735
narrative scores: neutral [50,20,20]; warm [50,30,20]; coercive [50,20,44]
```

The X03 probe is nondeterministic in sampled modes; exact mode/bias outputs are not stable receipts.

## P4 — urgent narrator-to-psyche edge

Targeted sourcefree test with one raw `sensitivity_exposure` process:

```text
warm rendered scene + raw process   -> narration_support warmth 30; aperture 55
neutral rendered scene + raw process -> narration_support warmth 20; aperture 54
warm rendered scene, no process      -> psychological capacity 50/50/50/50/50
neutral rendered scene, no process   -> psychological capacity 50/50/50/50/50
warm scene, reader monkeypatched to (50,50,50) -> aperture 54
neutral scene, reader monkeypatched to (50,50,50) -> aperture 54
```

Interpretation: the positive edge is real at sourcefree grain; it requires a raw/working process. The no-process path is a **sourcefree no-change boundary**, not a native CAN012 NO_CHANGE. The monkeypatch is a **severed-reader fault** at the exact `_analyze_narrative_for_support_quality` edge, not a production fault injection.

Immediate `render_year` after `compute_all_derived` leaves the backbone hash unchanged and writes only `rendered_output`; the narrator effect is in the **next-year** `update_metabolization_and_plasticity_step`, which reads the previous `rendered_output`. The edge is not inside `render_year`.

## P5 — RNG/replay

- `update_striving_step` calls `update_existing_objects` and `spawn_striving_objects_for_age` without an RNG; both create unnamed `random.Random()`.
- Five fresh age-14 calls produced different object/value sets; exact labels are run-dependent.
- Retirement seed scan (0..5) remaining: `[1,0,1,0,0,1]`. X03's own `probe_x03.json` also shows retirement at seeds 1, 3, 4, contradicting the dossier's "only at seed 1" wording.
- `create_rupture_shard_from_event` uses unnamed RNG for mode; independent runs produced different modes (e.g. collapse vs assimilation) for the same state.
- `maybe_inject_rupture_at_band_age` uses module-global `random.random/choices`; 14/20 seeds injected at age 14.

## P6 — additional source checks

- No source writer found for `working`/`provisionally_narrated`/`integrated`/`sealed`/`chronic` process status.
- No source writer found for `narrators`, `intrusive_return_rate` after creation, or `intrusive_return_rate_prev`.
- No consumer found for `downstream_biases`.
- `enforce_framework_caps` does not enforce `max_active`; `assert_frameworks_limits` exists as a year-end fail-fast check.
- `persona_sheet.py` reads nonexistent `metabolization_mode`: `_sacred_ruptured` is always false; the unresolved-rupture voice note still emits, missing only the mode text.

## Limits

Sourcefree historical arithmetic/probe behavior only. No current C9/C12, Pyat, native person, LLM/V2 run, respondent data or production edit. No result is a scientific rule or native permission.
