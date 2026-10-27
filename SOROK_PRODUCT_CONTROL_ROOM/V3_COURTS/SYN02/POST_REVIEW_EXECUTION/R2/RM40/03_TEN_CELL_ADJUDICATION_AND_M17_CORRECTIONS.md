# SYN02-RM40-R2 — TEN-CELL ADJUDICATION AND M17 CORRECTIONS

**Status:** source-graded repair, not acceptance; no native grant.
**Pinned RM40:** `653d356d773ab025c4ed22e9d70ba8fc25d6f839`; **RRM40 review:** `0c181943e527613f4bc114684a1962949a549e20`.
**Branch:** `agent/sorok-syn02-rm40-r2-literal-v3-patch-map-r1`; **sealed startup:** `2da83f77d820b327169673386d52c4acefbbdd46`.

## 1. Reconciliation arithmetic

| Quantity | Value |
|---|---:|
| S05 baseline X | 126 |
| S05 baseline unmarked/dash | 354 |
| Total serialized cells | 480 |
| RM40/R2 final X | 124 |
| RM40/R2 final unmarked/dash | 356 |
| Adjudicated discrepancies | 10 |
| Retained X as `INDIRECT_CARRIER_ONLY` | 8 |
| Removed as `UNSUPPORTED` | 2 |

The final X count is 126 − 2 = 124, not 126 − 10. The eight retained discrepancies stay X because they are bounded historical carrier links; they are not Rule T, current consumer links, or direct semantic coverage. The two removed cells are M14/N02 and M39/N01.

## 2. Ten adjudicated cells

| M/N | S05 | Final | Relation | Exact source symbol(s) | Adjudication |
|---|---:|---:|---|---|---|
| M09/N01 | X | X | `INDIRECT_CARRIER_ONLY` | `Crack; update_cracks; ensure_min_cracks` | Crack/tension carrier has no need-axis or object field; it can only condition a later need-domain response through contradiction, not form a need/object. |
| M10/N01 | X | X | `INDIRECT_CARRIER_ONLY` | `Buffer; BufferCostProfile; update_buffers` | Buffer/Support carrier supplies resources/costs; it has no need axis, object, activity or motive formation. |
| M11/N01 | X | X | `INDIRECT_CARRIER_ONLY` | `Framework; update_framework_weights; enforce_framework_caps` | Framework mediates interpretation/capacity; it does not define a need, object, or formed motive. |
| M13/N01 | X | X | `INDIRECT_CARRIER_ONLY` | `PracticeStack; update_practice_stack` | PracticeStack is a practice-category carrier; no need axis, object, activity episode or motive is represented. |
| M14/N02 | X | — | `UNSUPPORTED` | `PeakRouting; update_loop_topology; update_solidarity_boundary; update_coherence` | PeakRouting boundary/loop/coherence has no care, caregiver, expectation, or scoped anticipation function. |
| M18/N01 | X | X | `INDIRECT_CARRIER_ONLY` | `RuptureShard; create_rupture_shard_from_event; update_wound_vector_from_rupture` | RuptureShard records a violated assumption/domain; it does not form a need, object, or motive target. |
| M19/N01 | X | X | `INDIRECT_CARRIER_ONLY` | `MetabolizationProcess; compute_metabolization_delta; update_metabolization_and_plasticity_step` | MetabolizationProcess changes capacity/biases over time; it has no need/object/activity formation field. |
| M24/N01 | X | X | `INDIRECT_CARRIER_ONLY` | `stability_threshold_inertia; stability_inertia_dissipation` | Stability inertia is a persistence/residue mechanism; it does not constitute a need or object. |
| M36/N01 | X | X | `INDIRECT_CARRIER_ONLY` | `infer_parent_baseline_and_regime; derive_child_expectation_baseline` | Parent baseline maps NEED_AXES to expectation labels; this is N02 expectation vocabulary, not a formed motive/object. |
| M39/N01 | X | — | `UNSUPPORTED` | `maybe_inject_rupture_at_band_age; _maybe_inject_rupture_at_band_age` | Age-band rupture injection has no need/object/activity relation; its old N01 crosswalk warning is stale. |

### M36/N01 carrier-only finding

M36/N01 is retained as `INDIRECT_CARRIER_ONLY`. `derive_child_expectation_baseline` maps parent categories into `NEED_AXES` expectation vocabulary (`v3/engine/expectation_baseline.py:107`), and `infer_parent_baseline_and_regime` produces the parent labels from behavior (`v3/io/parent_baseline_from_behavior.py:25`). This is **N02 expectation vocabulary**, not a formed need, object, activity episode, or motive. Calling it direct M01 coverage would relabel vocabulary as needs formation.

### Removed unsupported cells

- **M14/N02:** `PeakRouting`, `update_loop_topology`, `update_solidarity_boundary` and `update_coherence` configure global loop/boundary/coherence state. They contain no care episode, caregiver, expectation, or scoped anticipation relation. The old crosswalk X is removed.
- **M39/N01:** `maybe_inject_rupture_at_band_age` is an age-band, global-RNG injection after the year run; its server alias is imported and called outside the main year event loop. It does not form a need, object, or activity relation. The old N01 X is removed.

## 3. M17 exact-callable correction

### Prior error

RM40 named `create_gift_shard_from_event` and `create_disruption_shard_from_event`. Neither symbol exists in the selected source. Repeating either would make the patch map source-false even if the biological/psychological intent were plausible.

### Actual source facts

| Item | Exact value |
|---|---|
| Actual callable | `apply_gift_disruption_shards_from_events` |
| Kind | module-level function; returns `None`, mutates `BackboneState` |
| Definition | `v3/engine/expectation_events.py:103` |
| Call site | `v3/engine/effects/delta_templates.py:361-362` |
| Inputs | `state: BackboneState`; `selected_events: list[dict[str, Any]]` |
| Matching rule | event must have `expectation_type` in `fulfillment`/`violation` and `striving_object_id` matching an active striving |
| Output/mutation | appends `GiftShard` at `v3/core/state.py:339` or `DisruptionShard` at `v3/core/state.py:353`; one valence per event |
| Additional source risk | `malheur_risk` threshold uses `identity_load`; event label/dict is the authority |

The actual source therefore supports a witnessed-event shell and exact striving-object identifier seam, but not the prior fake function names and not a direct mixed-impression operation. R2 retains the event shell/ID seam and replaces mono-valence shards with a source-qualified `ImpressionRecord` target.

### Corrected patch target

- **Remove:** any `create_gift_shard_from_event` / `create_disruption_shard_from_event` reference.
- **Preserve:** witnessed selected event, `expectation_type`, active `striving_object_id`, label, and source identity.
- **Replace:** forced positive/negative shard valence with a mixed actor-relative `ImpressionRecord`; no measure is inferred from valence alone.
- **New adapter:** `neo_v3/actor/impression.py`; `record_impression(state: ActorSnapshotV1, event: EpisodeV1, access: AccessEnvelope) -> ImpressionRecord`.
- **First future consumer:** `CAN008.impression_create → C9` — `TO_BUILD`, not live.
- **Test:** `T-M17-IMPRESSION`; must fail when a selected event without an active striving ID creates an impression, and must preserve unknown/mixed valence without forcing a positive/negative scalar.

## 4. Other literal-kind corrections

| M | Prior shorthand/risk | Correct literal grain | Source location |
|---|---|---|---|
| M04 | possibly one hostage function | `ReproductionConstraints`; `update_reproduction_constraints`; `_derive_hostage_index`; `compute_hostage_index` in derived read path | `v3/core/state.py:58`; `v3/systems/reproduction.py:60`; `v3/psyche/gating.py:61`; `v3/core/derived.py:45` |
| M21 | slash composite `run_pressure_flow_cycle / ...` | separate functions `run_pressure_flow_cycle`, `_domain_charge_ledger`, `_channel_conductance`, `_update_memory`, `derive_vitality_profile`, `derive_insulation_profile` | `v3/psyche/flow.py:753/406/366/678`; `v3/psyche/vitality.py:85`; `v3/psyche/insulation.py:72` |
| M22 | field treated as callable | `child_model` field; `PASS1_SYSTEM` constant; `backbone_state_from_identity` function | `v3/core/state.py:549`; `v3/engine/prompts.py:11`; `v3/io/identity_to_backbone.py:209` |
| M23 | two-dial composite | fields `autonomy_condition`/`safety_condition` plus `autonomy_drive`/`safety_drive`; `autonomy_safety_micro_drift` function | `v3/core/state.py:555-558`; `v3/systems/autonomy_safety.py:27` |
| M25 | year function only | YAML `derived_indices_schedule`; `run_one_year`, `step_one_year`, `run_n_years`; order test | `v3/v3_yearly_step_order.yaml:21`; `v3/engine/yearly_step.py:12/102`; `v3/engine/step_runner.py:13`; `v3/tests/test_architecture_invariants.py:89` |
| M30 | one V2 callable | prose articulation plus `build_persona_sheet`/`prepare_conversation_turn`; not a second psyche | `v3/V3_UNDERLIES_V2_ARTICULATION.md`; `v3/io/persona_sheet.py:579`; `v2/conversation_engine.py:2079` |
| M31 | type matcher as V3 mechanism | V2 design docs plus V2 functions; optional noncausal archive only | `v2/ENNEAGRAM_EMERGENCE_SYSTEM.md`; `v2/PROBABILISTIC_ENNEAGRAM_SYSTEM.md`; `v2/enneagram_wisdom.py:615`; `v2/parent_type_inference.py:33/143` |
| M37 | `distill_memory filtering` label | server `run_simulation_for_session` callsite + persona backstory builder + distillation functions | `server/generation/simulation.py:71`; `v3/io/persona_sheet.py:579/470`; `v3/tools/distill_memory.py:218/72` |
| M39 | one canonical function | canonical `maybe_inject_rupture_at_band_age` plus server alias `_maybe_inject_rupture_at_band_age` | `v3/engine/effects/metabolization_effects.py:273`; `server/generation/simulation.py:13/539` |

## 5. What is not claimed

- No X is a permission, current import, Rule T authorization, source validation, or native science grant.
- No `INDIRECT_CARRIER_ONLY` link is a direct semantic implementation target.
- No line ref or symbol was copied from a summary when direct source was available; the local file hash is the identity gate.
- The ten-cell count does not imply ten code deletions or ten behavior changes. Eight are retained carrier evidence; two are removed assertions.
- This docket does not edit V3, C9/C12 storage, production, CAN/ADP, or source authority.
