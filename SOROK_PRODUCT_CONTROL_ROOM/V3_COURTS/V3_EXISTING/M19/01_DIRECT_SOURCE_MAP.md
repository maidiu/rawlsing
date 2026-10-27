# M19 — direct source map

**Court:** HISTORICAL_V3 / EXACT_MECHANISM; X03 independent source return, awaiting independent review. **Coverage:** PARTIAL_WRONG_MEANING

**Source identity:** X03 sealed startup `2647a4cf25d8bb33a00471e1af9c5e58c2825efb`; direct read-only files are hashed in `WORKER_RETURNS/X03/SOURCE_IDENTITIES.json`. The S50-selected files are 31/31 exact. X03 files outside S50 were matched to `CAN_011_V3_MIDDLE_STATE/AUTHORITY.json`, `CAN_012_V3_RUPTURE_METABOLIZATION/AUTHORITY.json`, `CAN_010_V3_NEED_EXPECTATION_STRIVING/AUTHORITY.json`, `ADP_007_V3_ACTOR_INITIALIZATION/AUTHORITY.json`, or are explicitly local-source-only. The local staging zip `3f2c5ed9…` is not the TD-R05 archive `953c9149…`; archive-level exactness is not claimed.

**Claim ceiling:** historical source and sourcefree probe behavior at the cited grain. This is not current C9/C12 integration, a native person, a scientific law, or a source/actor/C8/C9/C11/C12/Pyat grant.


## Function and call-path map

| Symbol | File:lines | Inputs | Actual operation | State read/write | Callers/consumers | Test entry |
|---|---|---|---|---|---|---|
| `MetabolizationProcess` | `v3/core/state.py:386–418` | id, year/age, domain, assumption, severity, opacity, prediction error, mode, status, cluster, plasticity, IRR, narrators, frame, biases, triggers, counters | persistent process carrier | `metabolization_processes[]` | JSON; creation; yearly update; stability | presence only |
| `compute_metabolization_delta` | `v3/engine/effects/metabolization_effects.py:25–47,358–424` | cluster, mode, severity, narration support, malheur flag | cluster/mode/severity arithmetic; bias deltas; malheur multiplier | `returned deltas` | yearly update | one tuple test |
| `update_metabolization_and_plasticity_step` | `v3/engine/effects/metabolization_effects.py:521–599` | processes, plasticity, rendered_output, psych capacity | decrements plasticity; derives narration support from rendered text; applies cluster deltas/biases for raw/working; updates sensitivities | `processes, plasticity, psych capacity, narration_support` | yearly_step plasticity_and_metabolization_update | no transition/IRR test |
| `stability_inertia_dissipation` | `v3/systems/stability_inertia.py:17–83` | process status/IRR, narration support, inertia, derived | integration/IRR-drop/holding/sealed drains; clears flag | `stability_threshold_inertia; flag` | yearly_step stability_inertia_dissipation | no focused test |
| `stability spec` | `v3/docs/STABILITY_INERTIA_MAXIMAL_SPEC.md:33–93` | design text | specifies raw→working→provisional→integrated and sealed/chronic, IRR decay, prev update | `intended behavior` | documentation only | not executed |
| `Pass 1/persona consumers` | `v3/engine/llm_contract.py:754–765; v3/io/persona_sheet.py:928–934` | processes/status/plasticity | active count, domains, years left; no actual status history | `summary/persona` | Pass 1/V2 | presence only |

## What is actually run

- Creation sets status `"raw"` and plasticity 1–3 years. The yearly step decrements `plasticity_years_left` and `plasticity_window.years_left`, but never changes `status`; after three probe years the process remained `"raw"` with plasticity 3→0. The declared states `working/provisionally_narrated/integrated/sealed/chronic` have no producer in the read source.
- The yearly step applies cluster deltas and accumulates `downstream_biases` for every `"raw"`/`"working"` process even after plasticity reaches 0. No time window gates the cluster. In the probe, biases accumulated betrayal_expectancy 2→4→6 and reality_tolerance −1→−2→−3 over three years; nothing consumes those biases.
- `intrusive_return_rate` is set at creation (60 for high prediction error/opacity, else 40) and never updated; `intrusive_return_rate_prev` remains 50. `narrators` is never populated, so `narration_support.availability` is always 50; accuracy/warmth/coercion are scraped from last year’s rendered prose by `_analyze_narrative_for_support_quality`. A warm scene raises warmth 20→30 and aperture 54→55 in the probe, so rendered text becomes a causal input to psychological capacity.
- `stability_inertia_dissipation` can drain holding from insulation/support/coherence, and manual status `"integrated"` produces a larger drain (probe inertia 20→14.7735 vs 19.88675 raw). But no generated process ever reaches integration; IRR-drop is inert because IRR/prev never change; sealed leak requires statuses never produced. The only active source drain is holding, plus any manual status mutation.
- `is_malheur` is called with `proc.severity`; creation never produces `"malheur"` (it maps malheur intensity to micro), so the malheur multiplier is not reached through the yearly path. `sealed_candidate_years`, `post_plasticity_years`, and `start_plasticity_years` are never updated; `reactivation_triggers` is never populated.
- `create_rupture_shard_from_event` overwrites `state.plasticity_window` for each new rupture. Probe: a 3-year high rupture followed by a 2-year low rupture left the window at 2 years, not a merged/max/independent state.

## Real affordance

- Typed persistent process and JSON carrier exist.
- Cluster/mode/severity arithmetic is implemented and changes psychological capacity; the synthetic/creation probe shows real effects.
- Raw/working gating and holding-drain arithmetic exist; manual integration status produces a real stability drain.
- Plasticity decrement and sensitivity recalculations exist.
- The source documentation specifies a fuller lifecycle, which is evidence of intended but absent code, not evidence it runs.

## Source-level REDs

- Statuses are vocabulary only; no transition producer.
- IRR, narrators, meaning attempts, frame, triggers, and counters are never updated.
- Cluster effects continue indefinitely; plasticity is decrement-only and not a gate.
- Rendered prose text is treated as narrator/support evidence; render is not causal authority.
- `downstream_biases` have no consumer.
- Malheur is unreachable through the creation mapping; status integration/sealing/chronic are unreachable.
- Each new rupture overwrites the shared plasticity window.

## Tests actually covering this mechanism

- `test_metabolization_effects::test_compute_metabolization_delta_returns_tuples` checks types only.
- No test covers status transition, IRR, narrators, support, NO_CHANGE, stability drain, or recurrence.

## Probe evidence

Probe evidence: malheur process micro/raw; three years raw (3→2→1→0) with biases accumulating; raw inertia 20→19.88675 vs manual integrated 20→14.7735; neutral/warm/coercive prose changed warmth 20/30/20 and aperture 54/55/54; second rupture overwrote 3-year window to 2.

## Identity and authority note

CAN_012 and the historical maximal spec both state the missing transitions and forbid rendered-text causality. The source’s own `v3_yearly_step_order.yaml` says it derives support from narrators, but narrators are never set.

The source files and hashes are in `WORKER_RETURNS/X03/SOURCE_IDENTITIES.json`; the executable probe is `TEST_SOURCE_AND_LOGS/probe_x03.py` with output `probe_x03.json`. No production or source file was modified.
