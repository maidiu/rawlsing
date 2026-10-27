# SYN02-B — complete M01–M40 function disposition and adaptation matrix

**Status:** `SYN02_B_DESIGN_RETURN__SOURCE_REVIEWED_DISPOSITION_MATRIX__NO_IMPLEMENTATION__NO_NATIVE_GRANT`.
**Scope:** all forty historical V3/V2/PFF mechanisms, reviewed at their selected-source/focused-test grain, with a function-level old→new adaptation decision. This is not a current C9/C12 implementation, not a rule issuance and not a production edit.
**Source/authority:** original source read-only at `<USER_HOME>/Desktop/Rawlsing/Rawlsing_code_bundle_staging`; file identities in `ADAPTATION/B/SOURCE_PLANE_IDENTITIES.json`. The 40 families have independent scoped review through X01–X05 and RX01–RX05; the exact author/reviewer SHAs are in `SOURCE_PLANE_IDENTITIES.json` and `ATLAS.json`. The local staging ZIP is not the TD-R05 archive; file-level identity controls.

## 1. Decision summary

| Decision | Count | M IDs |
|---|---:|---|
| **REUSE** | 3 | M26, M29, M30 |
| **ADAPT** | 31 | M01–M25, M27, M28, M32, M37, M38, M40 (M14 rework; M15/M17/M21/M22 deep rework) |
| **REPLACE** | 3 | M31 (causal Enneagram matcher), M33 (mechanical event sampler), M39 (age-band rupture injection) |
| **REMOVE** | 3 | M34 (fallback fabrication), M35 (placeholder repair), M36 (unknown-parent defaults) |
| **RESEARCH_UNDECIDED** | 0 | None of the forty is left undecided at the engineering disposition level; several *semantic* rules remain undecided and are marked HOLD/owner-gated. |

The dispositions are not a claim that 31 mechanisms already have scientifically valid semantics. `ADAPT` means a carrier, trace, operator or discipline is reusable only after a stated semantic replacement. `REPLACE` means the old causal mechanism is not the right machine even if a record shell survives. `REMOVE` means no causal/scientific reuse; preserve the source as historical evidence and diagnostic material only.

## 2. M01–M10

| M | Old source functions | Old input → output / consumer | Disposition | Retain / replace semantics | New correspondence | First new consumer | Effort / risk | Proof; N links |
|---|---|---|---|---|---|---|---|---|
| M01 | BackboneState; hash_jsonable; GenerationIntegrityAccumulator | state ↔ persisted snapshot/diagnostics; json_codec, yearly_step, server | ADAPT | Keep explicit state, provenance and integrity carrier; end field conflation. | ActorSnapshotV1 + ActorHistory + ActorSnapshotStore | ActorHistoryReader → C9 | M 3–5d / Med | X01/RX01; N11,N12 |
| M02 | Capacity; update_capacity; update_health_drift | events/state → bounded material fields; yearly_step, derived AC/hostage | ADAPT | Keep typed material carrier; replace 50 defaults and annual scalar drift. | MaterialState + record_material_fact + project_capability | EventRealization / C9 | M 3–5d / High | X05/RX05; N01,N06 |
| M03 | PsychologicalCapacity; update_framework_weights; derive_vitality_profile | state → regulation/vitality fields; derived, summary, flow | ADAPT | Keep only source-backed regulation states; split fatigue, assisted regulation, ability and power. | RegulatoryState + record_regulation | CAN008/C9 read | L 6–10d / High | X02/RX02; N01,N04 |
| M04 | ReproductionConstraints; update_reproduction_constraints; _derive_hostage_index | events/field → constraints and duplicate hostage; yearly_step, gating | ADAPT | Keep concrete constraints; single support-load authority; separate objective fact from subjective burden. | MaterialConstraintRecord + compute_support_load | C9 / world interval | M 3–5d / Med | X05/RX05; N01,N06,N07,N12 |
| M05 | DomainState; update_domains; compute_baseline_load; apply_expression_gating | events → scalar A/S/V/Aim and expression; summary, persona, flow | ADAPT | Keep only a derived appraisal projection; no universal domains or single winning channel. | AppraisalProjection + project_domain_appraisal | C9 read-only view | L 6–10d / High | X02/RX02; N03,N04 |
| M06 | AlienationVector; update_alienation; apply_deltas_to_state | events → scalar/vector alienation; derived mis_aim, summary | ADAPT | Keep four-dimension carrier; fix phantom fields and clamp loss; derive estrangement from relations/activity. | EstrangementRecord + DerivedAlienationView | C9 / derived view | M 3–5d / Med | X05/RX05; N07,N10 |
| M07 | Registers; apply_expression_gating; build_persona_sheet; build_reply_prompt | derived state → access/expression gates; V2 surface | ADAPT | Keep graded access/expression concept; use ADP017; no narration-created memory. | AccessEnvelope + project_expression_access | ADP017/V2 read | M 3–5d / Med | X05/RX05; N04,N07,N09 |
| M08 | WoundVector; seed_wound_vector_from_identity; update_wound_vector_from_rupture | identity/rupture → sensitivities; scoring, flow, persona | ADAPT | Keep scoped persistent sensitivity; remove demographic seeds and automatic rupture increments. | SensitivityRecord + record_sensitivity | CAN008/C9 | L 6–10d / High | X02/RX02; N02,N03,N05,N08 |
| M09 | Crack; update_cracks; ensure_min_cracks | events/seeds → crack objects; derived crack load, persona | ADAPT | Keep episode-linked tension; remove placeholders, demographic seeds and fixed counts. | TensionRecord + transition_tension | C9 / CAN011 | L 6–10d / High | X03/RX03; N05 |
| M10 | Buffer; BufferCostProfile; update_buffers | events → buffer strength and costs; derived insulation | ADAPT | Keep support/cost-as-practice concept; require actual source, resource and relation. | SupportRecord + apply_support | C9 / CAN011 | M 3–5d / Med | X02/RX02; N02,N03,N04,N07,N08 |

## 3. M11–M20

| M | Old source functions | Old input → output / consumer | Disposition | Retain / replace semantics | New correspondence | First new consumer | Effort / risk | Proof; N links |
|---|---|---|---|---|---|---|---|---|
| M11 | Framework; update_framework_weights; enforce_framework_caps | seeds/events → weights/operators; capacity, summary, persona | ADAPT | Keep acute/chronic operator technique; remove demographic acquisition and fixed tenure. | InterpretiveMediatorRecord + apply_mediator_use | C9 / CAN011 | L 6–10d / High | X03/RX03; N04,N05,N09,N10 |
| M12 | CollectiveInfrastructure; update_collective_infrastructure | events → five actor scalars; topology/derived | ADAPT | Keep reference to collective conditions; move institutions/ties to world owner. | InstitutionRef + ParticipationRef | World/C9 | M 3–5d / High | X05/RX05; N06,N07,N12 |
| M13 | PracticeStack; update_practice_stack | seeds/events/flow → six scalars; derived, flow, persona | ADAPT | Keep persistent practice carrier; require actual activity, support, object and loss. | PracticeRecord + transition_practice | C9 / CAN011 | L 6–10d / High | X03/RX03; N05,N06,N10 |
| M14 | PeakRouting; update_loop_topology; update_solidarity_boundary; update_coherence | state/events → global topology, boundary, coherence; derived/persona | ADAPT | Keep hysteresis technique; reject global enum and event-label boundary without reception. | OrientationConfiguration + FunctionalConnectionRecord (candidate) | C9 / SYN02-C | L 6–10d / High | X03/RX03; N04,N05,N08 |
| M15 | NEED_AXES; derive_child_expectation_baseline; infer_parent_baseline_and_regime | identity/parent → expectation labels; striving/Pass1 | ADAPT | Keep finite need vocabulary; create scoped expectations with actual care evidence and unknown. | NeedAxis + ExpectationRecord + record_expectation | C9 / CAN010/011 | L 6–10d / High | X01/RX01; N01,N02,N03,N08 |
| M16 | StrivingObject; spawn_striving_objects_for_age; update_existing_objects; update_striving_step | age/baseline → proxy objects; events/summary/persona | ADAPT | Keep object identity and event seam; remove age/random spawn and active-list deletion. | MotiveTargetRecord + transition_motive | C9 / CAN010/011 | L 6–10d / High | X03/RX03; N01,N05,N06,N10 |
| M17 | GiftShard; DisruptionShard; create_gift/disruption_shard_from_event | event label → one-valence shard; delta/persona | ADAPT | Keep witnessed event shell; replace forced valence with mixed actor-relative impression. | ImpressionRecord + record_impression | C9 / CAN008 | L 6–10d / High | X01/RX01; N02,N03,N05,N08,N09 |
| M18 | RuptureShard; create_rupture_shard_from_event; update_wound_vector_from_rupture | event/age → shard/process/wound; metabolization/persona | ADAPT | Keep immutable rupture carrier; require exact admission, actor basis and rule; no age ritual. | RuptureRecord + admit_rupture | CAN012 / C9 | L 6–10d / High | X03/RX03; N03,N05,N08 |
| M19 | MetabolizationProcess; compute_metabolization_delta; update_metabolization_and_plasticity_step | process/rendered prose → capacity/biases; persona/stability | ADAPT | Keep process carrier and cluster compatibility; create status/IRR/support lifecycle; no prose causality. | MetabolizationProcessRecord + transition_metabolization | CAN012 / C9 | XL 12–20d / High | X03/RX03; N02,N03,N05,N08,N09,N10 |
| M20 | Magnet; apply_selected_magnets_to_state; update_active_magnets_step; build_relational_field_projection | candidate/state → magnet/field; summary/persona | ADAPT | Keep orientation/decay; bind to exact entity/relation history; remove unconditional parent labels and `who` loss. | RelationRecord + ActorEntityRef + MagnetView | C9 / world | L 6–10d / High | X05/RX05; N04,N07,N10,N12 |

## 4. M21–M30

| M | Old source functions | Old input → output / consumer | Disposition | Retain / replace semantics | New correspondence | First new consumer | Effort / risk | Proof; N links |
|---|---|---|---|---|---|---|---|---|
| M21 | run_pressure_flow_cycle; _domain_charge_ledger; _channel_conductance; _update_memory; derive_vitality_profile; derive_insulation_profile | state/year → route traces, psych proxies; post-year/derived/summary | ADAPT | Keep transaction, trace, conductance feedback and snapshot; reject conserved-substance and single-winner ontology. | RouteTrace + run_route_cycle_transactional + DerivedView | C9 / ANALYST-only view | XL 12–20d / High | X02/RX02; N02,N03,N04,N05,N07,N08,N09,N12 |
| M22 | child_model; backbone_state_from_identity; PASS1_SYSTEM | identity → typed child model/prompt; scoring/summary | ADAPT | Keep a fallible developmental orientation carrier; unknown stays unknown; no infant adult theology. | DevelopmentalOrientation + UnknownChildHistory | CAN010/011 / C9 | L 6–10d / High | X01/RX01; N01,N02,N09,N10 |
| M23 | autonomy_drive/safety_drive; autonomy_condition/safety_condition; autonomy_safety_micro_drift | state/derived → conditions and traces; derived stability | ADAPT | Keep condition/gap trace; remove universal 65/68 drive defaults; ground in actual relations. | ConditionRecord + record_safety_autonomy | C9 / CAN008 | M 3–5d / Med | X02/RX02; N01,N03,N04 |
| M24 | stability_threshold_inertia; stability_inertia_dissipation | process/derived → inertia; stability/flow | ADAPT | Keep persistence/hysteresis idea; no universal drain/neutral point; support-dependent receipts. | ResidueRecord + record_hysteresis | C9 / CAN011 | M 3–5d / Med | X02/RX02; N02,N05,N08 |
| M25 | run_one_year; step_one_year; run_n_years; test_step_order_immutable | config/state → annual mutation; server | ADAPT | Keep explicit dependency order; replace year-as-causal-unit with event/interval plus slow process. | advance_interval + run_event_sequence | C9/C12 batch | L 6–12d / High | X04/RX04; N06,N11,N12 |
| M26 | DerivedIndices; compute_all_derived; assert_no_derived_fields_in_backbone; test_no_derived_fields_in_backbone_state | state → projected indices; all readers | REUSE | Keep pure derived views and exact dependency declaration; remove hidden writes. | DerivedViewRegistry + compute_view | all read-only views | M 3–6d / Low | X05/RX05; N11,N12 |
| M27 | parse_candidate_packet; build_pass1_prompt; run_llm_band_year | LLM text → candidates/selected deltas; server band | ADAPT | Keep proposal-only contract/caps/provenance; split batch proposal from realization. | BatchProposal + propose_batch | event realization | M 3–6d / Med | X04/RX04; N07,N11 |
| M28 | score_event_candidate; select_candidates; run_llm_band_year; apply_deltas_to_state | packet/selection → merged state deltas; band | ADAPT | Keep finite selection/provenance; add hard admissibility, named RNG and NO_CHANGE; no premerge. | CanonicalEvent + admit_event + select_event | C9/CAN008 | M 3–6d / High | X04/RX04; N07,N11 |
| M29 | build_render_packet; build_pass2_prompt; render_year; test_llm_no_backbone_mutation | packet → surface only; V2/persona | REUSE | Keep immediate render nonmutation and surface allowlist; never treat output as memory/cause. | SurfaceRecord + render_surface | V2 / ADP017 | S 1–3d / Low | X04/RX04; N09,N11,N12 |
| M30 | design articulation; build_persona_sheet; prepare_conversation_turn | state → V2 surface; V2 | REUSE | Keep one-person jurisdiction and read-only V2; no second psyche or narration authority. | ActorVisibleSurface + read_surface | V2/ADP016/017 | S 1–3d / Low | X05/RX05; N09,N10,N11,N12 |

## 5. M31–M40

| M | Old source functions | Old input → output / consumer | Disposition | Retain / replace semantics | New correspondence | First new consumer | Effort / risk | Proof; N links |
|---|---|---|---|---|---|---|---|---|
| M31 | match_life_course_to_type; infer_parent_type; get_parent_type_effects_for_child | life/parent data → type/effects; V2 | REPLACE | Retain optional noncausal description only; remove type-at-birth, random end matcher and parent-type determinism. | OptionalTypologyView + archive_enneagram | V2 only | S 1–3d / Med | X05/RX05; no direct N; optional descriptive |
| M32 | normalize_v5_runtime_input_bundle; attach_v5_runtime_input_bundle; build_v5_field_bridge_injection; get_field_injection_for_year | world bundle → inert refs/field numerics; server | ADAPT | Keep inert source carrier/status/provenance; bind to current world/time owner; fail closed. | SourceEnvelope + field_injection_decision | world/C9 | M 3–6d / High | X05/RX05; N12 |
| M33 | _pseudo_seed; _one_event; sample_events | state/year → generic events/deltas; yearly_step | REPLACE | Keep serialization/conditioning shell; replace random event causality with source-owned world events. | WorldEventSource + realize_world_event | C9/CAN008 | L 6–12d / High | X04/RX04; N06,N11 |
| M34 | parse_candidate_packet_with_fallback; make_fallback_event; fallback_candidate_packet_if_empty; run_llm_band_year | empty packet → fabricated event; band | REMOVE | Remove all fabrication; retain explicit no-event/held/NO_CHANGE path. | NoEventRecord + hold_missing_proposal | C9 event admission | S 1–3d / Low | X04/RX04; N11 |
| M35 | ensure_min_cracks; ensure_min_frameworks; run_one_year | missing counts → placeholder atoms; yearly_step | REMOVE | Remove placeholder objects; diagnostics may remain but never causal state. | ValidEmpty + diagnose_placeholder | C9 / migration | S 1–3d / Low | X05/RX05; no direct N; removal supports all valid-empty |
| M36 | infer_parent_baseline_and_regime; derive_child_expectation_baseline | absent parent → 50/hopeful; expectation/child | REMOVE | Remove unknown→normal/positive conversion; preserve unknown/missing with source or block. | UnknownExpectation | C9 / CAN010/011 | S 1–3d / Low | X01/RX01; N02 |
| M37 | run_simulation_for_session; build_persona_sheet; _trajectory_backstory_from_snapshots; distill_memory filtering | non-LLM state → annotation scene/backstory; V2 | ADAPT | Keep interstitial accounting/annotation metadata; exclude from memory/previous scene; no state summary as lived memory. | IntervalAnnotation + surface separation | C9/ADP016 | M 3–6d / Med | X04/RX04; N06,N09,N11 |
| M38 | derived_indices_schedule; _compute_derived_after_step; get_derived_schedule | config/step → derived schedule; yearly_step | ADAPT | Keep fail-fast equality; one canonical registry and no hidden writes or stale caches. | DerivedRegistry | C9/scheduler | M 3–6d / Low | X04/RX04; N06,N11 |
| M39 | _maybe_inject_rupture_at_band_age; maybe_inject_rupture_at_band_age | age/RNG → rupture/wound; server | REPLACE | Keep only rupture record as evidence; require admitted world/actor event; remove age ritual. | AdmittedDisruption + admit_rupture_event | CAN012/C9 | M 3–6d / High | X04/RX04; N03,N05,N08,N11 (candidate; stale crosswalk) |
| M40 | _validate_persona_for_store_write; _golden_eligibility_for_session_dir; GenerationIntegrityAccumulator; _generation_state_is_ready | generation verdict → store/persona readiness; server | ADAPT | Keep graded integrity; readiness is multi-gate (engine/rule/source/actor/memory/consumer), not name/country. | ReadinessVector + assess_person_readiness | store/C9 | M 3–6d / Med | X05/RX05; N11,N12 |

## 6. Family-level adaptation design

### 6.1 State, provenance and derived discipline (M01, M26, M38, M40)
`BackboneState` is a useful explicit envelope, but it conflates durable actor facts, derived projections, animation/render surfaces and diagnostics. The replacement is a versioned `ActorSnapshotV1` with separate stores for canonical event history, actor-visible memory/access, durable middle-state records and surface output. `compute_all_derived` must become a pure `DerivedViewRegistry`; no derived function may write `registers`, `metabolic_style` or any other persisted actor field as a side effect. `yearly_integrity` and generation diagnostics remain diagnostic and cannot establish actor readiness. Readiness is a vector of independent gates: executable engine, accepted scientific rule, source/actor permission, migrated provenance, accessible memory and actual consumer.

### 6.2 Material life and independent world (M02, M04, M12, M20, M23, M32, M37)
The old material fields are scalar constraints with fabricated defaults, not care/work schedules. Retain typed material facts only with a source and a clock; derive feasible activity/access from real intervals. Replace `CollectiveInfrastructure` actor scalars with references to independently owned institutions, ties and participation. Replace `Magnet` labels with exact entity/relationship refs; never seed mother/father from identity. Keep the inert V5 source envelope and green/blocked provenance idea, but the world owner must supply the facts. Structural annotations may remain non-memory metadata; they are not scenes or remembered care.

### 6.3 Needs, expectations and motives (M15, M16, M22)
Need-axis names can remain a finite vocabulary. They do not carry an actor vector at birth. `ExpectationRecord` is scoped, evidence-bearing, unknown-capable and can hold love and material insufficiency at once. `MotiveTargetRecord` is formed through activity, recognition, object access, support and contradiction. Remove age/proxy spawn, random support, `setdefault(hopeful)`, active-list deletion and parent/child stereotypes. "Not-yet-thinkable", "imposed", "forbidden", "supported" and "contested" are design statuses, not automatic labels.

### 6.4 Interpretive and practical middle state (M03, M08, M09, M10, M11, M13, M14, M24)
`CAN011`'s three kinds are the terminal abstraction: `MEDIATOR`, `TENSION`, `PRACTICE`. The old `Framework`, `Crack`, `PracticeStack`, `Buffer`, `WoundVector` and `PeakRouting` are compatibility projections, not a fixed six-module psyche. Acquisition, use, scope, conflict, dormancy/reactivation, support and loss require explicit records and owners. Preserve the framework acute/chronic arithmetic and topology/boundary hysteresis only as computational techniques; do not infer a newly learned relation from a scalar regime switch. The optional `FunctionalConnectionRecord` is a SYN02-C research candidate for genuinely acquired connections; it is not an automatic Hebbian graph and is not adopted here.

### 6.5 Interpressure and route history (M05, M21)
`run_pressure_flow_cycle` contains real transactional route simulation, per-domain charge/trace bookkeeping, grooves/conductance feedback and separate analyst/surface outputs. Preserve the transaction boundary, trace and snapshot; reject conserved psychological substance, one winning channel and universal coefficients. The new `RouteTrace` is a computational record read by a governed appraisal/transition, not an actor autobiographical memory. A changed route value can alter later selection; that is not yet a new learned relation.

### 6.6 Rupture and multi-year processing (M17, M18, M19, M24, M39)
Keep the typed shard/process carriers and the visible distinction between embedded event record, metabolization process and surface. Remove forced valence, age-band injection, direct wound mapping, global RNG, rendered-prose support, indefinite cluster accumulation and dead status vocabulary. The new `RuptureRecord` and `MetabolizationProcessRecord` require exact event parents, actor basis, rule/version, support refs and `NO_CHANGE`; integration is not healing and chronic is not a personality type. The old age-band path is replaced, not adapted.

### 6.7 Scheduler, LLM proposal and render (M25, M27, M28, M29, M30, M33, M34, M37, M38)
The old yearly spine is a valid slow-process ordering technique, not the event/human time unit. Replace `sample_events`, premerged selected deltas, forced fallback and age rupture with a canonical event/interval path. Keep Pass 1's proposal-only boundary and Pass 2's immediate render nonmutation. A batch proposal is not an event; realization must be source/world/actor-admitted; each event reads the preceding state; the next LLM call's first half is retrospective and the second half opens the next batch. No ordinary LLM call between events. Render output is one-way surface and cannot become memory or psyche through keyword statistics.

### 6.8 V2, typology and readiness (M31, M37, M40)
V2 owns expression and actor-limited access, not a second life simulation. The historical Enneagram matcher is replaced: no type at birth, no random age-7 crystallization and no parent-type causal table. A type label, if retained at all, is an optional noncausal description with explicit evidence. Readiness is a multi-gate product state; a stored persona is not a person and a clean generation verdict is not scientific/source/native acceptance.

## 7. Two-way N/M completeness

The following is the candidate design map. It uses the reviewed N→M candidates and the M→N links in `ATLAS.json`, with one explicit correction: M39 has no direct M→N row in the current atlas, but the reviewed N03/N05/N08/N11 text treats rupture admission as relevant. This design maps M39 to those requirements and flags the crosswalk correction for HQ; it does not edit the atlas.

### 7.1 M → N

| M | N candidates |
|---|---|
| M01 | N11, N12 |
| M02 | N01, N06 |
| M03 | N01, N04 |
| M04 | N01, N06, N07, N12 |
| M05 | N03, N04 |
| M06 | N07, N10 |
| M07 | N04, N07, N09 |
| M08 | N02, N03, N05, N08 |
| M09 | N05 |
| M10 | N02, N03, N04, N07, N08 |
| M11 | N04, N05, N09, N10 |
| M12 | N06, N07, N12 |
| M13 | N05, N06, N10 |
| M14 | N04, N05, N08 |
| M15 | N01, N02, N03, N08 |
| M16 | N01, N05, N06, N10 |
| M17 | N02, N03, N05, N08, N09 |
| M18 | N03, N05, N08 |
| M19 | N02, N03, N05, N08, N09, N10 |
| M20 | N04, N07, N10, N12 |
| M21 | N02, N03, N04, N05, N07, N08, N09, N12 |
| M22 | N01, N02, N09, N10 |
| M23 | N01, N03, N04 |
| M24 | N02, N05, N08 |
| M25 | N06, N11, N12 |
| M26 | N11, N12 |
| M27 | N07, N11 |
| M28 | N07, N11 |
| M29 | N09, N11, N12 |
| M30 | N09, N10, N11, N12 |
| M31 | — (optional noncausal description only) |
| M32 | N12 |
| M33 | N06, N11 |
| M34 | N11 |
| M35 | — (removal supports valid-empty across N; no direct positive mapping) |
| M36 | N02 |
| M37 | N06, N09, N11 |
| M38 | N06, N11 |
| M39 | N03, N05, N08, N11 (candidate correction; current atlas row empty) |
| M40 | N11, N12 |

### 7.2 N → M

| N | Historical/candidate M links |
|---|---|
| N01 | M02, M03, M04, M15, M16, M22, M23 |
| N02 | M08, M10, M15, M17, M19, M21, M22, M24, M36 |
| N03 | M05, M08, M10, M15, M17, M18, M19, M21, M23, M39 |
| N04 | M03, M05, M07, M10, M11, M14, M20, M21, M23 |
| N05 | M08, M09, M11, M13, M14, M16, M17, M18, M19, M21, M24, M39 |
| N06 | M02, M04, M12, M13, M16, M25, M33, M37, M38 |
| N07 | M04, M06, M07, M10, M12, M20, M21, M27, M28 |
| N08 | M08, M10, M14, M15, M17, M18, M19, M21, M24, M39 |
| N09 | M07, M11, M17, M19, M21, M22, M29, M30, M37 |
| N10 | M06, M11, M13, M16, M19, M20, M22, M30 |
| N11 | M01, M25, M26, M27, M28, M29, M30, M33, M34, M37, M38, M40, M39 |
| N12 | M01, M04, M12, M20, M21, M25, M26, M29, M30, M32, M40 |

`M31` and `M35` are not positive contributors to a Neo requirement. M31 may survive only as optional noncausal description; M35 is removed, and its absence is a precondition for valid-empty records. M39’s corrected placement is called out rather than silently inserted into the central atlas.

## 8. What is not claimed

- No new psychological law, coefficient, age threshold, acquisition rule, relation edge or native rule is issued.
- No current S39–S52 assembled C9/C12 person exists in this checkout; no current consumer was run.
- No source permission, actor/source, C8/C9/C11/C12, Pyat or production grant.
- The 40-family source review is selected-file/function/test scoped; it is not a claim that every archived V3 body was re-read in this commission.
- The new names in this matrix are candidate interfaces, not implemented functions.
