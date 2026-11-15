# ZAK-04S R6 — V553 relation identity, rupture meaning, and consumer authority

**Protected:** 6a5c12f04323d74001f9632063ec907f4fc4468e. **Documentary parent PR #1055:** 2bb5d0759270e8d9340cb012fdf3e11042dac27b. Historical V553 completing architecture distinct from live legacy implementation and unexecuted P5 assignment.

## Major newly recovered functional discontinuity
The V553 delta builder creates `delta_id` as `v553_delta_{from_wave}_to_{to_wave}` (no temporal key) but returns `pd.DataFrame(rows, columns=V553_CROSS_WAVE_DELTA_INDEX_SCHEMA["required_columns"])`, and the required-columns list omits `delta_id`. Pandas projects that extra value out. The temporal-field reader calls `delta_row.get("delta_id")` and immediately skips absent/empty identifiers. Therefore the authored `source_delta_ids_json` join is empty through this specific producer→consumer path even for real computed delta values. `temporal_pressure_key`/wave metrics still exist in the delta table: data is not globally absent. Simply adding `delta_id` to schema is inadequate: same wave pair at two pressure keys would collide. The historical accepted P3 architecture instead requires exact from_observation_id/to_observation_id and source-grained identity.

## Precise observation boundary (do not overstate)
`_build_v553_temporal_pressure_observation_index` creates `observation_id` using key and wave and returns `pd.DataFrame(rows)` (unprojected). The generic `write_frame_artifact` persists actual columns, so unlike `delta_id`, physical observation IDs are not shown lost. However the old declared `V553_TEMPORAL_PRESSURE_OBSERVATION_INDEX_SCHEMA` does not list `observation_id` as a required field, and current delta outputs do not preserve those endpoints.

## Source-level rupture mistakes
Delta producer emits comparability_status `authorized_comparable` or `probe_only`; rupture reader tests `== "comparable"`. Under exact produced delta rows every rupture interpretation_permission is False and even an authorized structural delta receives a `probe_only_temporal_field` blocked reason. Separately `direction_reversal` is triggered by a single signed delta of magnitude >=0.35, not a directional change over successive deltas. The current candidate code does not read governed rule_id/rule_version. Under historical V553 completion ruling, qualitative rupture annotations remain disabled absent such a rule. No event or causal actor claim is earned.

## Handoff and audit proof
Actual V553 v554_handoff_index holds temporal keys, counts, permission labels, and known gaps but not complete governed structural refs and exact observation endpoint IDs required by historical P5 G17/G18. Present V554 remains a heuristic table reader, not an exact DAG handoff consumer; R5's two routes stay valid. The current V553 forbidden-inference audit unconditionally writes `violation_detected=False` and does not inspect output content, so it is not substantive verification though other code/guards may protect behavior.

## What is already known; what remains
Prior SI-R00 had already found V552J rematching, key averaging and incomplete governed structural reference set; these are inherited findings, not claimed novel. W06 watchers operate primarily by checking source substrings and contain an expectedFailure typed summary watcher, not selected-wave S2 proof. P5 exact V553-to-V554 consumer test named in a blocked assignment was not located at the protected code cut or indexed code search. Completion status cannot be upgraded.

**Delivery:** eight bounded operation cases; 20 exact evidence rows; 8 source-static OP traces and 16 shapes; eight explicit first readers, 5 causal chain rows, 5 unexecuted negative falsifiers, 3 proposed shared-seam updates; no original historical T count inflation.

**Recommendation, not implementation:** Separate future V553 completion owner should conserve both physical obs IDs and terminal refs, emit key-scoped exact temporal relation identity and observation endpoints, preserve signed and typed statuses, keep qualitative rupture disabled absent governed versioned rule, and prove lawful V554 consumption without heuristic aggregates. No broad rebuild or native actor declaration warranted.

**Terminal:** `ZAK04S_R6_DELTA_ID_SCHEMA_PROJECTION_LOSS_PROVED_S1__RUPTURE_COMPARABILITY_GATE_INERT_POSITIVE__EXACT_HANDOFF_G17_G18_OPEN__NO_ENGINEERING`.
