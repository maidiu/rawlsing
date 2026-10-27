# SYN02-RM40 — all-forty original-to-new function patch matrix

**Status:** `RM40_SOURCE_LEVEL_PATCH_DESIGN__NO_PRODUCTION_IMPLEMENTATION__NO_NATIVE_GRANT`.
**Architecture target:** `321fa29bb3e51849a43cb7caf1600625bf215539`; **independent hostile review:** `ac55c36e42ded82957176896cbc5953db62f7209`; **commission seal:** `07ebb10eac214ebc909b92f24b459caf2d37d730`.
**Source access:** actual read-only local historical source at `<USER_HOME>/Desktop/Rawlsing/Rawlsing_code_bundle_staging`; 59 B file hashes rehashed, 31/31 S50 selected identities rehashed, 40/40 reviewed mechanisms. The local staging ZIP is not the TD-R05 archive; full path+SHA for each M is in `02_VERIFIED_480_CELL_M_TO_N_CROSSWALK.json`.

This is the literal function-level repair map requested by RM40, not the generic repeated S04 module catalog. It gives the old callable, current readers/writers, dangerous policy, retained invariant, proposed replacement and test gate for every M. No new code is claimed implemented.

## 1. Disposition summary

| Decision | Count | IDs |
|---|---:|---|
| **REUSE** | 3 | M26 (invariant), M29 (immediate render body), M30 (one-person invariant) |
| **ADAPT** | 31 | M01–M25, M27, M28, M32, M37, M38, M40 |
| **REPLACE** | 3 | M31, M33, M39 |
| **REMOVE** | 3 | M34, M35, M36 |
| **RESEARCH_UNDECIDED** | 0 | — |

The three REUSE cases are not whole-body reuse: M26 must become pure; M29 is immediate-render only and must not be followed by narrator-to-psyche feedback; M30 preserves one-person jurisdiction and read-only V2, not age/parent substitutions.

## 2. M01–M10

| M | Source file/path (primary hash) | Literal callable | Actual callers | Reads → writes | Dangerous old policy | Retained invariant | New patch + first consumer | Disposition | Test/fixture | Science/authority gate |
|---|---|---|---|---|---|---|---|---|---|---|
| M01 | v3/core/state.py (19e968d45e9d81eb…; full hashes in 02) | BackboneState; hash_jsonable; GenerationIntegrityAccumulator | json_codec; yearly_step; server; persona_sheet | state fields ↔ persisted JSON/diagnostics; no canonical event ledger | durable, derived, surface and diagnostics share one mutable envelope | explicit snapshot/provenance/integrity/hash | ActorSnapshotV1 + ActorHistory + ActorSnapshotStore; ActorHistoryReader→C9 | ADAPT | migration roundtrip + provenance fixture | C9/C12 schema owner |
| M02 | v3/core/state.py (19e968d45e9d81eb…; full hashes in 02) | Capacity; update_capacity; update_health_drift | yearly_step; derived AC/hostage; summary | events/state → capped time/money/health/support; no actual interval | 50 defaults and class/urban scalar-as-capacity | typed material carrier, bounded deltas, provenance | MaterialState + record_material_fact + project_capability; EventRealization/C9 | ADAPT | material interval + unknown-default fixture | C0/C8/SDTF/world |
| M03 | v3/core/state.py (19e968d45e9d81eb…; full hashes in 02) | PsychologicalCapacity; update_framework_weights; derive_vitality_profile | frameworks; yearly_step; derived; summary; flow | capacity/framework state → psych/vitality projections | one scalar family stands for fatigue, ability, power and assisted regulation | typed regulation/availability carrier, not one causal vector | RegulatoryState + record_regulation; CAN008/C9 read | ADAPT | regulation/assistance separation fixture | CAN008/CAN011/ADP |
| M04 | v3/core/state.py (19e968d45e9d81eb…; full hashes in 02) | ReproductionConstraints; update_reproduction_constraints; _derive_hostage_index | yearly_step; prosperity gate; gating | event/field → constraints and two hostage values | duplicate hostage authority; 0/100 optimistic defaults; objective constraint treated as felt burden | concrete constraint carrier and bounded support load | MaterialConstraintRecord + compute_support_load; C9/world interval | ADAPT | 52.5 vs 100 duplicate-hostage fixture | C0/C8/SDTF/world |
| M05 | v3/core/state.py (19e968d45e9d81eb…; full hashes in 02) | DomainState; update_domains; compute_baseline_load; apply_expression_gating | yearly_step; summary; persona; flow | events → A/S/V/Aim and expressed aim | fixed universal domains and one winning channel | concurrent appraisal projection and access-gated expression | AppraisalProjection + project_domain_appraisal; C9 read-only | ADAPT | multi-stream/zero-load expression fixture | CAN008/CAN011/ADP017 |
| M06 | v3/core/state.py (19e968d45e9d81eb…; full hashes in 02) | AlienationVector; update_alienation; apply_deltas_to_state | yearly_step; derived mis-aim; summary | events → scalar + four vector dimensions; phantom old fields | phantom structural/affective/institutional writes; clamp loses delta | four-dimension estrangement carrier with one derived view | EstrangementRecord + DerivedAlienationView; C9/derived | ADAPT | phantom-field/clamp-loss fixture | CAN011/C9 |
| M07 | v3/core/state.py (19e968d45e9d81eb…; full hashes in 02) | Registers; apply_expression_gating; build_persona_sheet; build_reply_prompt | yearly_step; persona; V2 conversation | derived state → public/private/inner gates; V2 surface | 50/80 defaults, zero-as-missing, stale expression; narration can look causal | graded access/expression envelope, ADP017 boundary | AccessEnvelope + project_expression_access; ADP017/V2 read | ADAPT | zero-load/stale-expression fixture | ADP017/V2 |
| M08 | v3/core/state.py (19e968d45e9d81eb…; full hashes in 02) | WoundVector; seed_wound_vector_from_identity; update_wound_vector_from_rupture | identity; rupture; scoring; flow; persona | identity/rupture → seven sensitivities | class/minority/religion/age seeds; automatic rupture increment | typed scoped sensitivity carrier, no demographic origin | SensitivityRecord + record_sensitivity; CAN008/C9 | ADAPT | demographic-seed/rupture-path fixture | CAN008/CAN012/ADP |
| M09 | v3/core/state.py (19e968d45e9d81eb…; full hashes in 02) | Crack; update_cracks; ensure_min_cracks | yearly_step; derived crack load; persona; Pass1 | events/seeds → crack list; only intensify-range cap | placeholders, future origin years, demographic/age cracks; no lifecycle | episode-linked tension carrier and bounded event delta | TensionRecord + transition_tension; C9/CAN011 | ADAPT | placeholder/future-origin fixture | CAN011/ADP |
| M10 | v3/core/state.py (19e968d45e9d81eb…; full hashes in 02) | Buffer; BufferCostProfile; update_buffers | yearly_step; derived insulation; capacity | events → strength/cost and capacity deduction | support/cost has no actual provider/resource/relation | support-with-resource/cost carrier | SupportRecord + apply_support; C9/CAN011 | ADAPT | support-cost/source fixture | CAN011/world |

## 3. M11–M20

| M | Source file/path (primary hash) | Literal callable | Actual callers | Reads → writes | Dangerous old policy | Retained invariant | New patch + first consumer | Disposition | Test/fixture | Science/authority gate |
|---|---|---|---|---|---|---|---|---|---|---|
| M11 | v3/core/state.py (19e968d45e9d81eb…; full hashes in 02) | Framework; update_framework_weights; enforce_framework_caps | yearly_step; capacity; summary; persona | seed/events → weights + acute/chronic operator; tenure | age/class/religion recipes; age-derived tenure; no acquisition/use | acute/chronic operator and stable mediator identity | InterpretiveMediatorRecord + apply_mediator_use; C9/CAN011 | ADAPT | age-seed/acute-chronic fixture | CAN011/CAN010 |
| M12 | v3/core/state.py (19e968d45e9d81eb…; full hashes in 02) | CollectiveInfrastructure; update_collective_infrastructure | yearly_step; topology; derived; persona | events → five actor scalars | institutions/ties/power copied into actor; zero-as-unknown | typed collective condition references | InstitutionRef + ParticipationRef; world/C9 | ADAPT | collective/world separation fixture | C0/C8/ADP019 |
| M13 | v3/core/state.py (19e968d45e9d81eb…; full hashes in 02) | PracticeStack; update_practice_stack | yearly_step; derived; flow; persona | seed/events/flow → six practice scalars | SES/age/religiosity seeds; label/route increments; no activity/support | persistent practice carrier and actual activity seam | PracticeRecord + transition_practice; C9/CAN011 | ADAPT | activity/support/loss fixture | CAN011/SDTF |
| M14 | v3/core/state.py (19e968d45e9d81eb…; full hashes in 02) | PeakRouting; update_loop_topology; update_solidarity_boundary; update_coherence | yearly_step; derived peak; persona | state/events → topology, boundary, coherence | global enum/scalar threshold; event-label boundary; no relation edge | consecutive-year hysteresis, one-step bounded boundary technique | OrientationConfiguration + optional FunctionalConnectionRecord; C9/SYN02-C | ADAPT | hysteresis/reversal + no learned-edge fixture | CAN008/CAN011/SYN02-C |
| M15 | v3/core/state.py (19e968d45e9d81eb…; full hashes in 02) | NEED_AXES; derive_child_expectation_baseline; infer_parent_baseline_and_regime | identity; striving; Pass1; scoring | parent/identity → need-axis labels | unknown parent 50 → hopeful; flat labels; no care history | finite need vocabulary + scoped expectation carrier | NeedAxis + ExpectationRecord + record_expectation; C9/CAN010/011 | ADAPT | missing-parent/coexisting-care fixture | CAN010/011/ADP015 |
| M16 | v3/core/state.py (19e968d45e9d81eb…; full hashes in 02) | StrivingObject; spawn_striving_objects_for_age; update_existing_objects; update_striving_step | events; Pass1; persona; yearly_step | age/baseline → proxy objects; random support/retirement | age spawn, unseeded RNG, hopeful fill, deleted retired history | stable object ID and event-attachment seam | MotiveTargetRecord + transition_motive; C9/CAN010/011 | ADAPT | activity-vs-age/replay fixture | CAN010/CAN011/ADP020 |
| M17 | v3/core/state.py (19e968d45e9d81eb…; full hashes in 02) | GiftShard; DisruptionShard; create_gift/disruption_shard_from_event | expectation events; delta application; persona | event label → one-valence shard | mono-valence and LLM label authority; no mixed reception | witnessed event shell and mixed impression carrier | ImpressionRecord + record_impression; C9/CAN008 | ADAPT | same-event-mixed/nochange fixture | CAN008/CAN011/ADP016 |
| M18 | v3/core/state.py (19e968d45e9d81eb…; full hashes in 02) | RuptureShard; create_rupture_shard_from_event; update_wound_vector_from_rupture | delta_templates; server age hook; persona | event/age → shard/process/wound | age/global RNG; malheur→micro; direct wound mapping; no parents | immutable rupture carrier and explicit admission seam | RuptureRecord + admit_rupture; CAN012/C9 | ADAPT | severity/wound-path fixture | CAN012/ADP019 |
| M19 | v3/core/state.py (19e968d45e9d81eb…; full hashes in 02) | MetabolizationProcess; compute_metabolization_delta; update_metabolization_and_plasticity_step | delta_templates; yearly_step; stability; persona | process/rendered prose → psych capacity/biases; status/IRR | prose support; no status producer; indefinite deltas; dead counters | process identity, raw/working carrier, cluster compatibility | MetabolizationProcessRecord + transition_metabolization; CAN012/C9 | ADAPT | narrator-severance + status/nochange fixture | CAN012/ADP020/021 |
| M20 | v3/core/state.py (19e968d45e9d81eb…; full hashes in 02) | Magnet; apply_selected_magnets_to_state; update_active_magnets_step; build_relational_field_projection | Pass1; yearly_step; summary; persona | candidate/state → magnet/field | parent labels, lost who, label-to-practice; structural field conflated | relation/decay carrier, exact entity reference | RelationRecord + ActorEntityRef + MagnetView; C9/world | ADAPT | who/entity/parent-label fixture | C8/ADP019/C9 |

## 4. M21–M30

| M | Source file/path (primary hash) | Literal callable | Actual callers | Reads → writes | Dangerous old policy | Retained invariant | New patch + first consumer | Disposition | Test/fixture | Science/authority gate |
|---|---|---|---|---|---|---|---|---|---|---|
| M21 | v3/psyche/flow.py (6da4effde2b1ccb7…; full hashes in 02) | run_pressure_flow_cycle; _domain_charge_ledger; _channel_conductance; _update_memory; derive_vitality/insulation | yearly_step; derived; summary; V2 | state/year → route traces and psych proxies | one-winner channel, conserved-substance metaphor, pre-route writes survive | transactional route snapshot, trace, conductance memory | RouteTrace + run_route_cycle_transactional + pure DerivedView; C9 | ADAPT | multi-pressure/transaction fixture | CAN008/C9/C6 |
| M22 | v3/core/state.py (19e968d45e9d81eb…; full hashes in 02) | child_model; backbone_state_from_identity; PASS1_SYSTEM | identity; Pass1; scoring; summary | identity → child model/taboos/possible world | safe-home defaults, adult categories, no actual care history | fallible developmental orientation carrier | DevelopmentalOrientation + UnknownChildHistory; CAN010/011/C9 | ADAPT | unknown-parent/no-infant-ideology fixture | CAN010/011/ADP017 |
| M23 | v3/core/state.py (19e968d45e9d81eb…; full hashes in 02) | autonomy_drive/safety_drive; autonomy_condition/safety_condition; autonomy_safety_micro_drift | yearly_step; derived stability/flow | state/derived → drives/conditions/gap trace | universal 65/68 drives; time increments treated as repair/erosion | actual condition/gap trace without universal drive | ConditionRecord + record_safety_autonomy; C9/CAN008 | ADAPT | actual-support vs default-drive fixture | CAN008/world |
| M24 | v3/core/state.py (19e968d45e9d81eb…; full hashes in 02) | stability_threshold_inertia; stability_inertia_dissipation | yearly_step; derived stability/health/flow | process/derived → inertia and drains | annual drain, neutral point, unsupported integration/sealed paths | source-bounded residue/hysteresis carrier | ResidueRecord + record_hysteresis; C9/CAN011 | ADAPT | support-dependent drain/nochange fixture | CAN011/ADP |
| M25 | v3/v3_yearly_step_order.yaml (90496a2cc852ca00…; full hashes in 02) | run_one_year; step_one_year; run_n_years; test_step_order_immutable | server; run_and_print; tests | config/state → annual mutation; 19 core/20 configured | year is causal unit; render/active magnets inside year; no event/interval | explicit order, dependency assertions, year-record hash | advance_interval + run_event_sequence; C9/C12 | ADAPT | 19/20 + reversed-event/batch fixture | C6/C8/C9/C12 |
| M26 | v3/core/state.py (19e968d45e9d81eb…; full hashes in 02) | DerivedIndices; compute_all_derived; assert_no_derived_fields_in_backbone | all readers; yearly_step; tests | state → derived indices; writes metabolic_style/registers | hidden persistent derived writes; narrow name invariant | pure projection lookup and snapshot-hash stability | DerivedViewRegistry + compute_view; all read-only consumers | REUSE (invariant) | derived no-write/snapshot fixture | C9 engineering |
| M27 | v3/engine/llm_contract.py (f024debf7b8a637e…; full hashes in 02) | parse_candidate_packet; build_pass1_prompt; run_llm_band_year | server LLM band; Pass1 | text → candidates; selected → band | proposal boundary real but selected events become premerged state | proposal-only schema/caps/provenance | BatchProposal + propose_batch; event realization | ADAPT | 3–5 proposal/no-state fixture | C6/C8/ADP019 |
| M28 | v3/engine/scoring.py (36833287c72ffa40…; full hashes in 02) | score_event_candidate; select_candidates; run_llm_band_year; apply_deltas_to_state | LLM band; delta application | packet/selection → selected events/merged deltas | no hard admissibility; unseeded surprise; premerge; no ledger | finite scoring/caps and mutation provenance shell | CanonicalEvent + admit_event + select_event; CAN008/C9 | ADAPT | source-admission/ledger/nochange fixture | C8/ADP020/C9 |
| M29 | v3/engine/llm_contract.py (f024debf7b8a637e…; full hashes in 02) | build_render_packet; build_pass2_prompt; render_year; test_llm_no_backbone_mutation | server; persona; V2 | packet → rendered_output only | immediate pure but downstream prose can feed M19; retry/callback edge | immediate render hash stability and surface allowlist | SurfaceRecord + render_surface; V2/ADP017 | REUSE (immediate body) | render-hash/prose-severance fixture | V2/ADP017 |
| M30 | v3/V3_UNDERLIES_V2_ARTICULATION.md (5a0f11276a830b95…; full hashes in 02) | V3_UNDERLIES_V2_ARTICULATION; build_persona_sheet; prepare_conversation_turn | server; V2 chat | state → V2 surface | one person is real, but age<17→35, parent narrative and prose feedback leak | one-person jurisdiction and read-only surface | ActorVisibleSurface + read_surface; V2/ADP016/017 | REUSE (invariant) | V2 no-write/age-parent fixture | V2/ADP016/017 |

## 5. M31–M40

| M | Source file/path (primary hash) | Literal callable | Actual callers | Reads → writes | Dangerous old policy | Retained invariant | New patch + first consumer | Disposition | Test/fixture | Science/authority gate |
|---|---|---|---|---|---|---|---|---|---|---|
| M31 | v2/ENNEAGRAM_EMERGENCE_SYSTEM.md (95f8876926dda96a…; full hashes in 02) | match_life_course_to_type; infer_parent_type; get_parent_type_effects_for_child | V2 life generation; parent narrative | life/parent data → type and type effects | type at 7, random end matcher, parent-type determinism | none causal; optional forensic typology only | OptionalTypologyView + archive_enneagram; V2 only | REPLACE | type-at-7/parent-effect fixture | V2/native descriptive |
| M32 | v3/io/v5_bridge.py (31700b4031a62b0b…; full hashes in 02) | normalize_v5_runtime_input_bundle; attach_v5_runtime_input_bundle; build_v5_field_bridge_injection; get_field_injection_for_year | server; field update | world bundle → inert refs/field numerics | hardcoded source; integrity-blind merge; numeric field applies despite blocked status | inert source carrier, status/provenance, fail-closed gate | SourceEnvelope + field_injection_decision; world/C9 | ADAPT | blocked-bundle/merge fixture | C0/C8/ADP019 |
| M33 | v3/engine/event_engine.py (b57e7ef4df5dabd9…; full hashes in 02) | _pseudo_seed; _one_event; sample_events | yearly_step; event ledger | state/year → 0–3 generic events/deltas | random kind/delta causality; no actor/access/coactor/source | event IDs/labels/conditioning serialization shell | WorldEventSource + realize_world_event; C9/CAN008 | REPLACE | mechanical-vs-source event fixture | C8/ADP019 |
| M34 | v3/engine/llm_contract.py (f024debf7b8a637e…; full hashes in 02) | parse_candidate_packet_with_fallback; make_fallback_event; fallback_candidate_packet_if_empty; run_llm_band_year | LLM band; Pass1 | empty packet → fabricated practice event | manufactures a practice event and deltas | only integrity/degradation diagnostics | NoEventRecord + hold_missing_proposal; C9 admission | REMOVE | empty-packet no-mutation fixture | C8/C9 |
| M35 | v3/core/invariants.py (81298f3fc51b46cd…; full hashes in 02) | ensure_min_cracks; ensure_min_frameworks; run_one_year | yearly_step; invariants | missing count → placeholder crack/framework | fabricated minimum psychological objects; filter hides them but load counts | diagnostic counts only | ValidEmpty + diagnose_placeholder; C9/migration | REMOVE | valid-empty/placeholder fixture | CAN011/C9 |
| M36 | v3/io/parent_baseline_from_behavior.py (4e5be6448a5b76c4…; full hashes in 02) | infer_parent_baseline_and_regime; derive_child_expectation_baseline | identity; expectation; Pass1 | absent parent → 50/hopeful and child model | unknown becomes normal/hopeful/safe; no actual care | typed unknown/absent carrier | UnknownExpectation + record_expectation; C9 | REMOVE | missing-parent unknown fixture | CAN010/011/ADP015 |
| M37 | server/generation/simulation.py (5d68ffe3bc6902dc…; full hashes in 02) | run_simulation_for_session; build_persona_sheet; _trajectory_backstory_from_snapshots; distill_memory filtering | server; persona; V2 | non-LLM state → annotation scene/backstory | annotation enters backstory/previous scene; final run_and_print rerender can overwrite | interstitial accounting/annotation metadata separate from memory | IntervalAnnotation + surface separation; ADP016/V2 | ADAPT | annotation/no-scene/previous-scene fixture | ADP016/V2 |
| M38 | v3/v3_yearly_step_order.yaml (90496a2cc852ca00…; full hashes in 02) | derived_indices_schedule; _compute_derived_after_step; get_derived_schedule | yearly_step; config; tests | config/step → derived schedule | two declarations; stale unscheduled fields; compute writes state | fail-fast equality and explicit schedule | DerivedRegistry + compute_view; C9 interval scheduler | ADAPT | schedule mismatch/cache fixture | C9 engineering |
| M39 | server/generation/simulation.py (5d68ffe3bc6902dc…; full hashes in 02) | _maybe_inject_rupture_at_band_age; maybe_inject_rupture_at_band_age | server after run_one_year | age/RNG → shard/process/wound | age band/global RNG/outside ledger; malheur micro; event path no wound | only rupture record/template as forensic candidate | AdmittedDisruption + admit_rupture_event; CAN012/C9 | REPLACE | age/seed/ledger/wound fixture | CAN012/ADP019/020 |
| M40 | server/generation/store.py (eb592702327427a2…; full hashes in 02) | _validate_persona_for_store_write; _golden_eligibility_for_session_dir; GenerationIntegrityAccumulator; _generation_state_is_ready | server store; session state | generation verdict → stored/persona readiness | name/country clean_ready; degraded stored accepted; fixture is not person | graded integrity and multi-gate readiness concept | ReadinessVector + assess_person_readiness; store/C9 | ADAPT | blocked/degraded/clean stored fixture | C9/C12/native |

## 6. Patch seam rules

1. Every `New patch` entry is a **proposed** new module/type/function; none is an existing import.
2. A patch may retain an old data carrier only after the old dangerous read/write is removed or quarantined.
3. No patch may import old demographic/age/type/default psychological values as a formed actor fact.
4. A patch that writes actor state must name a source/event/access/rule/effective-clock/receipt; otherwise it returns `UNKNOWN`, `HELD`, or `VALID_EMPTY`.
5. First consumer is a potential C9/CAN008 reader, not a current import. Current production Rule A/T registries are empty; S48 is one-call; S49 natural B is empty; S52 is withheld.
6. A source patch that changes a shared carrier must also update the migration projection and a negative test; otherwise it is not patch-ready.
7. The 480-cell N/M matrix and the ten mismatch adjudications in `02`/`03` are the compatibility authority for this patch matrix, not the old S04 module-name table.

## 6a. Projected patch location and test fixture

These are **future edit locations**, not modules present in this tree. They are the concrete landing zones for the row-level `New patch` entries above.

| M | Projected patch module | Planned test fixture |
|---|---|---|
| M01 | `neo_v3/actor/schema.py` | `tests/neo_v3/test_actor_snapshot.py` |
| M02 | `neo_v3/actor/material.py` | `tests/neo_v3/test_material_interval.py` |
| M03 | `neo_v3/actor/regulation.py` | `tests/neo_v3/test_regulation.py` |
| M04 | `neo_v3/actor/constraints.py` | `tests/neo_v3/test_support_load.py` |
| M05 | `neo_v3/actor/appraisal.py` | `tests/neo_v3/test_multi_stream.py` |
| M06 | `neo_v3/actor/estrangement.py` | `tests/neo_v3/test_alienation_repair.py` |
| M07 | `neo_v3/surface/access.py` | `tests/neo_v3/test_access_envelope.py` |
| M08 | `neo_v3/actor/sensitivity.py` | `tests/neo_v3/test_sensitivity_source.py` |
| M09 | `neo_v3/actor/tension.py` | `tests/neo_v3/test_tension_lifecycle.py` |
| M10 | `neo_v3/actor/support.py` | `tests/neo_v3/test_support_source.py` |
| M11 | `neo_v3/actor/mediator.py` | `tests/neo_v3/test_mediator_use.py` |
| M12 | `neo_v3/world/institution.py` | `tests/neo_v3/test_institution_ref.py` |
| M13 | `neo_v3/actor/practice.py` | `tests/neo_v3/test_practice_activity.py` |
| M14 | `neo_v3/actor/orientation.py` | `tests/neo_v3/test_hysteresis_no_edge.py` |
| M15 | `neo_v3/actor/expectation.py` | `tests/neo_v3/test_scoped_expectation.py` |
| M16 | `neo_v3/actor/motive.py` | `tests/neo_v3/test_motive_activity.py` |
| M17 | `neo_v3/actor/impression.py` | `tests/neo_v3/test_mixed_impression.py` |
| M18 | `neo_v3/actor/rupture.py` | `tests/neo_v3/test_rupture_admission.py` |
| M19 | `neo_v3/actor/metabolization.py` | `tests/neo_v3/test_narrator_severance.py` |
| M20 | `neo_v3/actor/relation.py` | `tests/neo_v3/test_entity_relation.py` |
| M21 | `neo_v3/psyche/route.py` | `tests/neo_v3/test_route_transaction.py` |
| M22 | `neo_v3/actor/development_orientation.py` | `tests/neo_v3/test_unknown_child.py` |
| M23 | `neo_v3/actor/conditions.py` | `tests/neo_v3/test_condition_source.py` |
| M24 | `neo_v3/actor/residue.py` | `tests/neo_v3/test_residue_support.py` |
| M25 | `neo_v3/runtime/scheduler.py` | `tests/neo_v3/test_event_interval.py` |
| M26 | `neo_v3/derived/registry.py` | `tests/neo_v3/test_pure_derived.py` |
| M27 | `neo_v3/llm/batch.py` | `tests/neo_v3/test_batch_proposal.py` |
| M28 | `neo_v3/runtime/admission.py` | `tests/neo_v3/test_event_admission.py` |
| M29 | `neo_v3/surface/render.py` | `tests/neo_v3/test_surface_one_way.py` |
| M30 | `neo_v3/surface/read.py` | `tests/neo_v3/test_v2_one_person.py` |
| M31 | `neo_v3/legacy/typology.py` | `tests/neo_v3/test_no_causal_type.py` |
| M32 | `neo_v3/source/field.py` | `tests/neo_v3/test_source_gate.py` |
| M33 | `neo_v3/world/event_source.py` | `tests/neo_v3/test_world_event.py` |
| M34 | `neo_v3/runtime/no_event.py` | `tests/neo_v3/test_no_fallback.py` |
| M35 | `neo_v3/actor/valid_empty.py` | `tests/neo_v3/test_no_placeholder.py` |
| M36 | `neo_v3/actor/unknown.py` | `tests/neo_v3/test_unknown_parent.py` |
| M37 | `neo_v3/surface/annotation.py` | `tests/neo_v3/test_annotation_not_memory.py` |
| M38 | `neo_v3/derived/schedule.py` | `tests/neo_v3/test_derived_schedule.py` |
| M39 | `neo_v3/actor/admitted_disruption.py` | `tests/neo_v3/test_admitted_disruption.py` |
| M40 | `neo_v3/runtime/readiness.py` | `tests/neo_v3/test_readiness_gates.py` |

## 7. High-risk special cases

- **M19:** the old later-year reader consumes `rendered_output` through `_analyze_narrative_for_support_quality` and can alter psychological capacity for a raw/working process. The patch must sever prose causality and use explicit narrator/support/practice refs; direct `render_year` purity alone is insufficient.
- **M21:** preserve transactional route snapshot, per-domain trace and conductance-history technique; remove conserved-substance language and one-winner universal ontology. The route object transaction does not rollback independent world facts or all actor pre-route writes.
- **M25:** 19 `core_steps` versus 20 configured `steps`; `active_magnets_update` is appended. Keep explicit dependency order as a slow process, not the event/interval unit.
- **M26:** `compute_all_derived` writes `state.metabolic_style` and `state.registers`; the six-name invariant misses them. The patch must make derived views pure and preserve snapshot hash.
- **M27/M28:** proposal text is not an event; selected events currently premerge deltas and are absent from `state.events_this_year`. The patch must create canonical event rows and per-event application.
- **M29:** immediate `render_year` is hash-stable; full LLM band is not. Keep only the immediate render body and make `SurfaceRecord` one-way.
- **M30:** V2 one-person jurisdiction survives, but parent narrative, age<17→35 and later prose→psyche must be severed.
- **M37:** server per-year annotation and `run_and_print` final rerender both exist; neither may author memory. Separate `IntervalAnnotation` from scene/memory.
- **M38:** one canonical derived registry; no stale unscheduled fields or hidden state writes.
- **M31/33/39:** replace causal Enneagram matcher, mechanical event sampler and age-rupture injection; retain only forensic archive shells.
- **M34/35/36:** remove fallback event, placeholder objects and unknown→hopeful defaults entirely.

## 8. Source identity and test receipt

The full 59-file B hash register, 31/31 S50 selected manifest, 40 M source file lists and each of the 480 M×N cells are in `02_VERIFIED_480_CELL_M_TO_N_CROSSWALK.json`. The ten direct S04/S05 mismatches are adjudicated in `03_TEN_DISCREPANCY_SOURCE_ADJUDICATION.md`. No old file is edited, no new psychological coefficient is invented, and no current C9/C12 integration is claimed.
