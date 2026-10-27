# SYN02-RM40-R2 — ALL-40 LITERAL SYMBOL / CALLSITE / PATCH PLAN

**Status:** `SCOPED_SOURCE_AND_ENGINEERING_REPAIR__NOT_ACCEPTED__NO_NATIVE_GRANT`
**Branch:** `agent/sorok-syn02-rm40-r2-literal-v3-patch-map-r1`
**Sealed startup:** `2da83f77d820b327169673386d52c4acefbbdd46`
**Pinned RM40:** `653d356d773ab025c4ed22e9d70ba8fc25d6f839`
**Independent RRM40 review:** `0c181943e527613f4bc114684a1962949a549e20`
**Source root:** read-only `/Users/matthewsmith/Desktop/Rawlsing/Rawlsing_code_bundle_staging`; source cut `07ebb10eac214ebc909b92f24b459caf2d37d730`.
**Code edited:** NO. **Source/current owner files rewritten:** NO. **Native science issued:** NO.

## 1. Scope and acceptance facts

- This plan repairs RM40 at truthful symbol grain. It does not claim the old V3 functions have valid new semantics, does not implement adapters, and does not rewrite accepted S04/S05/RM40 records.
- Matrix accepted arithmetic: baseline S05 **126 X / 354 dash**; corrected **124 X / 356 dash** of **480** serialized cells. Ten discrepancies were adjudicated; eight historical relations remain `INDIRECT_CARRIER_ONLY`; M14/N02 and M39/N01 are `UNSUPPORTED` and removed. These are **not ten toggles**.
- Unique source identity: **59/59** unique source paths rehashed on the local staging tree; **31/31** S50 selected files match SHA-256 and byte length. The local staging ZIP is not the TD-R05 archive; file identity controls.
- The ten adjudicated cells are exactly: M09/N01, M10/N01, M11/N01, M13/N01, M14/N02, M18/N01, M19/N01, M24/N01, M36/N01, M39/N01. M36/N01 points to **N02 expectation vocabulary**, not direct need/object formation.
- Each M row below gives the exact case-sensitive symbol(s), truthful symbol kind, source location, hash registry, caller/callsite, reads/writes/effects, hazard, retained invariant, future adapter signature/type, owner, migration, independent consumer, test ID, and patch target. A future consumer is `TO_BUILD` or `RULE_HELD`; it is **not** a live import.
- New adapter names and paths are proposed API, not current production. `WAIT_FOR_C9_C12_STORAGE_OWNER_FREEZE` applies to F1.1; no actor CAS/outbox or C12 DDL is assumed.

## 2. Per-mechanism literal source and patch contract

### M01 — ADAPT — callable

- **Exact symbols (class + function):** `BackboneState; hash_jsonable; GenerationIntegrityAccumulator`
- **Source location:** `v3/core/state.py:501; v3/core/year_record.py:15; v3/core/generation_integrity.py:13`; primary hash file `v3/core/state.py` SHA-256 `19e968d45e9d81eb7629f1c237dbc55119fec8fc7db0b29e2b39b2476d12ada2`.
- **Caller/callsite:** yearly_step.py:12; server/generation/simulation.py:71; persona_sheet.py:579.
- **Reads / writes / effects:** persisted actor fields; JSON; generation diagnostics → snapshot/checkpoint; rendered_output/diagnostics; large mutable actor envelope.
- **Historical hazard:** durable, derived, surface and diagnostic fields share one owner.
- **Retain / replace:** explicit snapshot, provenance, hash, integrity, JSON carrier.
- **New adapter:** `neo_v3/actor/schema.py`; import `from neo_v3.actor.schema import ActorSnapshotV1, ActorSnapshotStore`; signature `def load_actor(actor_id: ActorId, source_cut: SourceCutRef) -> ActorSnapshotV1`; output type `ActorSnapshotV1`.
- **Owner / migration:** actor; map actor envelope; archive noncanonical legacy defaults.
- **First future semantic consumer:** ActorHistoryReader.load → C9 — **TO_BUILD** (not a live import).
- **Runnable sourcefree test ID:** `T-M01-SNAPSHOT`; test asserts held/no-change/degraded behavior, not inherited psychology.
- **Requested patch:** `neo_v3/actor/schema.py :: def load_actor(actor_id: ActorId, source_cut: SourceCutRef) -> ActorSnapshotV1`.
- **All direct source files:** `v3/core/state.py` (`19e968d45e9d…`); `v3/core/year_record.py` (`4bbd7518a6ec…`); `v3/core/generation_integrity.py` (`5265aac2fda4…`).

### M02 — ADAPT — callable

- **Exact symbols (class + function):** `Capacity; update_capacity; update_health_drift`
- **Source location:** `v3/core/state.py:18; v3/systems/capacity.py:55; v3/systems/health_drift.py:15`; primary hash file `v3/core/state.py` SHA-256 `19e968d45e9d81eb7629f1c237dbc55119fec8fc7db0b29e2b39b2476d12ada2`.
- **Caller/callsite:** yearly_step.py:113-148; derived.py:45-58; llm_contract.py:666.
- **Reads / writes / effects:** events; Capacity fields → capacity fields; annual capped material drift.
- **Historical hazard:** 50 defaults; class/urban scalar substituted for real work/care/time.
- **Retain / replace:** typed material carrier and bounded event delta.
- **New adapter:** `neo_v3/actor/material.py`; import `from neo_v3.actor.material import MaterialState, MaterialFact; from neo_v3.runtime.event import CanonicalEventV1`; signature `def apply_material_event(state: ActorSnapshotV1, event: CanonicalEventV1, fact: MaterialFact) -> MaterialState`; output type `MaterialState`.
- **Owner / migration:** actor; retain source-qualified facts; archive 50/class defaults.
- **First future semantic consumer:** EventRealization.material_read → C9 — **TO_BUILD** (not a live import).
- **Runnable sourcefree test ID:** `T-M02-MATERIAL`; test asserts held/no-change/degraded behavior, not inherited psychology.
- **Requested patch:** `neo_v3/actor/material.py :: def apply_material_event(state: ActorSnapshotV1, event: CanonicalEventV1, fact: MaterialFact) -> MaterialState`.
- **All direct source files:** `v3/core/state.py` (`19e968d45e9d…`); `v3/systems/capacity.py` (`cae31ffd4006…`); `v3/systems/health_drift.py` (`ba4608b7b9ab…`).

### M03 — ADAPT — callable

- **Exact symbols (class + functions):** `PsychologicalCapacity; update_framework_weights; derive_vitality_profile`
- **Source location:** `v3/core/state.py:41; v3/systems/frameworks.py:33; v3/psyche/vitality.py:85`; primary hash file `v3/core/state.py` SHA-256 `19e968d45e9d81eb7629f1c237dbc55119fec8fc7db0b29e2b39b2476d12ada2`.
- **Caller/callsite:** frameworks.py:74-101; yearly_step.py:135; flow.py:753.
- **Reads / writes / effects:** capacity/framework/process state → psych capacity and vitality profile; operator/delta capacity mutation.
- **Historical hazard:** one scalar family stands for fatigue, ability, power and assisted regulation.
- **Retain / replace:** typed regulation/availability carrier and provenance.
- **New adapter:** `neo_v3/actor/regulation.py`; import `from neo_v3.actor.regulation import RegulatoryState, record_regulation`; signature `def record_regulation(state: ActorSnapshotV1, event: CanonicalEventV1, support_refs: list[SupportRef]) -> RegulatoryState`; output type `RegulatoryState`.
- **Owner / migration:** actor; map only source-backed regulation; UNKNOWN otherwise.
- **First future semantic consumer:** CAN008.recruit(regulation_ref) → C9 — **TO_BUILD** (not a live import).
- **Runnable sourcefree test ID:** `T-M03-REGULATION`; test asserts held/no-change/degraded behavior, not inherited psychology.
- **Requested patch:** `neo_v3/actor/regulation.py :: def record_regulation(state: ActorSnapshotV1, event: CanonicalEventV1, support_refs: list[SupportRef]) -> RegulatoryState`.
- **All direct source files:** `v3/core/state.py` (`19e968d45e9d…`); `v3/systems/frameworks.py` (`0d59fc6e1770…`); `v3/psyche/vitality.py` (`56fed88e3729…`).

### M04 — ADAPT — callable

- **Exact symbols (class + functions):** `ReproductionConstraints; update_reproduction_constraints; compute_hostage_index; _derive_hostage_index`
- **Source location:** `v3/core/state.py:58; v3/systems/reproduction.py:60; v3/core/derived.py:45; v3/psyche/gating.py:61`; primary hash file `v3/core/state.py` SHA-256 `19e968d45e9d81eb7629f1c237dbc55119fec8fc7db0b29e2b39b2476d12ada2`.
- **Caller/callsite:** yearly_step.py:131; gating.py:153; derived.py:324.
- **Reads / writes / effects:** events; field; constraints → constraints; scalar hostage; constraint deltas and duplicate support-load formula.
- **Historical hazard:** two hostage authorities (52.5 vs 100.0); 0/100 optimistic defaults.
- **Retain / replace:** concrete constraint carrier; one support-load view.
- **New adapter:** `neo_v3/actor/constraints.py`; import `from neo_v3.actor.constraints import MaterialConstraintRecord, compute_support_load`; signature `def compute_support_load(constraints: MaterialConstraintRecord, access_refs: list[SupportRef]) -> SupportLoadView`; output type `MaterialConstraintRecord`.
- **Owner / migration:** actor + world interval; map concrete constraints; drop duplicate scalar authority.
- **First future semantic consumer:** C9.support_load_read / world interval — **TO_BUILD** (not a live import).
- **Runnable sourcefree test ID:** `T-M04-SUPPORT-LOAD`; test asserts held/no-change/degraded behavior, not inherited psychology.
- **Requested patch:** `neo_v3/actor/constraints.py :: def compute_support_load(constraints: MaterialConstraintRecord, access_refs: list[SupportRef]) -> SupportLoadView`.
- **All direct source files:** `v3/core/state.py` (`19e968d45e9d…`); `v3/systems/reproduction.py` (`6f3a815d7ef6…`); `v3/psyche/gating.py` (`4a82c7c91828…`); `v3/core/derived.py` (`e479fc3eba21…`).

### M05 — ADAPT — callable

- **Exact symbols (class + functions):** `DomainState; update_domains; compute_baseline_load; apply_expression_gating`
- **Source location:** `v3/core/state.py:72; v3/systems/domains.py:50; v3/psyche/gating.py:122; v3/psyche/gating.py:152`; primary hash file `v3/core/state.py` SHA-256 `19e968d45e9d81eb7629f1c237dbc55119fec8fc7db0b29e2b39b2476d12ada2`.
- **Caller/callsite:** yearly_step.py:113; persona_sheet.py:579; flow.py:753.
- **Reads / writes / effects:** events only in update_domains; domain/gate state → domain A/S/V/Aim/expressed_aim; event deltas plus expression gating.
- **Historical hazard:** fixed universal domains; one winning channel; stale expressed_aim.
- **Retain / replace:** pure appraisal projection and access-gated expression.
- **New adapter:** `neo_v3/actor/appraisal.py`; import `from neo_v3.actor.appraisal import AppraisalProjection, project_domain_appraisal`; signature `def project_domain_appraisal(state: ActorSnapshotV1, event: CanonicalEventV1, access: AccessEnvelope) -> AppraisalProjection`; output type `AppraisalProjection`.
- **Owner / migration:** actor; derive read-only view; archive fixed baseline scores.
- **First future semantic consumer:** CAN008.appraisal_view → C9 read-only — **TO_BUILD** (not a live import).
- **Runnable sourcefree test ID:** `T-M05-APPRAISAL`; test asserts held/no-change/degraded behavior, not inherited psychology.
- **Requested patch:** `neo_v3/actor/appraisal.py :: def project_domain_appraisal(state: ActorSnapshotV1, event: CanonicalEventV1, access: AccessEnvelope) -> AppraisalProjection`.
- **All direct source files:** `v3/core/state.py` (`19e968d45e9d…`); `v3/systems/domains.py` (`24e5215763a1…`); `v3/psyche/gating.py` (`4a82c7c91828…`).

### M06 — ADAPT — callable

- **Exact symbols (class + functions):** `AlienationVector; update_alienation; apply_deltas_to_state`
- **Source location:** `v3/core/state.py:95; v3/systems/alienation.py:20; v3/engine/effects/delta_templates.py:254/318`; primary hash file `v3/core/state.py` SHA-256 `19e968d45e9d81eb7629f1c237dbc55119fec8fc7db0b29e2b39b2476d12ada2`.
- **Caller/callsite:** yearly_step.py:154; run_llm_band.py:269.
- **Reads / writes / effects:** events; scalar/vector alienation → scalar plus nonexistent structural/affective/institutional attrs; delta lost at clamp; phantom attrs remain.
- **Historical hazard:** active path does not update four real dimensions.
- **Retain / replace:** four-dimension estrangement carrier and derived view.
- **New adapter:** `neo_v3/actor/estrangement.py`; import `from neo_v3.actor.estrangement import EstrangementRecord, record_estrangement`; signature `def record_estrangement(state: ActorSnapshotV1, episode: EpisodeV1, delta: EstrangementDelta) -> EstrangementRecord`; output type `EstrangementRecord`.
- **Owner / migration:** actor; map only source-qualified dimensions; discard phantom fields.
- **First future semantic consumer:** C9.estrangement_view / derived — **TO_BUILD** (not a live import).
- **Runnable sourcefree test ID:** `T-M06-ESTRANGEMENT`; test asserts held/no-change/degraded behavior, not inherited psychology.
- **Requested patch:** `neo_v3/actor/estrangement.py :: def record_estrangement(state: ActorSnapshotV1, episode: EpisodeV1, delta: EstrangementDelta) -> EstrangementRecord`.
- **All direct source files:** `v3/core/state.py` (`19e968d45e9d…`); `v3/systems/alienation.py` (`2209d8171a14…`); `v3/engine/effects/delta_templates.py` (`7d99ddf26fd4…`).

### M07 — ADAPT — callable

- **Exact symbols (class + functions):** `Registers; apply_expression_gating; build_persona_sheet; prepare_conversation_turn`
- **Source location:** `v3/core/state.py:114; v3/psyche/gating.py:152; v3/io/persona_sheet.py:579; v2/conversation_engine.py:2079`; primary hash file `v3/core/state.py` SHA-256 `19e968d45e9d81eb7629f1c237dbc55119fec8fc7db0b29e2b39b2476d12ada2`.
- **Caller/callsite:** yearly_step.py; server; V2.
- **Reads / writes / effects:** derived capacity/wound; persona state → registers; V2 surface; access gates and persona output.
- **Historical hazard:** 50/80 defaults; zero-as-missing; stale expression; no V2 access consumer.
- **Retain / replace:** graded access/expression envelope with ADP017 filtering.
- **New adapter:** `neo_v3/surface/access.py`; import `from neo_v3.surface.access import AccessEnvelope, project_expression_access`; signature `def project_expression_access(state: ActorSnapshotV1, relation_refs: list[RelationRef], audience: AudienceRef) -> AccessEnvelope`; output type `AccessEnvelope`.
- **Owner / migration:** actor surface; recompute access; archive defaults; no narration memory.
- **First future semantic consumer:** ADP017.access_filter → V2 — **TO_BUILD** (not a live import).
- **Runnable sourcefree test ID:** `T-M07-ACCESS`; test asserts held/no-change/degraded behavior, not inherited psychology.
- **Requested patch:** `neo_v3/surface/access.py :: def project_expression_access(state: ActorSnapshotV1, relation_refs: list[RelationRef], audience: AudienceRef) -> AccessEnvelope`.
- **All direct source files:** `v3/core/state.py` (`19e968d45e9d…`); `v3/psyche/gating.py` (`4a82c7c91828…`); `v3/io/persona_sheet.py` (`4a0009533443…`); `v2/conversation_engine.py` (`766bee296379…`).

### M08 — ADAPT — callable

- **Exact symbols (class + functions):** `WoundVector; seed_wound_vector_from_identity; update_wound_vector_from_rupture`
- **Source location:** `v3/core/state.py:130; v3/psyche/channels.py:36; v3/engine/effects/metabolization_effects.py:239`; primary hash file `v3/core/state.py` SHA-256 `19e968d45e9d81eb7629f1c237dbc55119fec8fc7db0b29e2b39b2476d12ada2`.
- **Caller/callsite:** identity_to_backbone.py:592; metabolization_effects.py:332.
- **Reads / writes / effects:** identity/rupture; WoundVector → seven sensitivity scalars; demographic seed and direct wound bump.
- **Historical hazard:** class/minority/religion/age seeds; automatic rupture mapping.
- **Retain / replace:** scoped persistent sensitivity carrier.
- **New adapter:** `neo_v3/actor/sensitivity.py`; import `from neo_v3.actor.sensitivity import SensitivityRecord, record_sensitivity`; signature `def record_sensitivity(state: ActorSnapshotV1, episode: EpisodeV1, basis_refs: list[EvidenceRef]) -> SensitivityRecord`; output type `SensitivityRecord`.
- **Owner / migration:** actor; archive demographic seeds; map only episode-qualified sensitivity.
- **First future semantic consumer:** CAN008.sensitivity_read → C9 — **TO_BUILD** (not a live import).
- **Runnable sourcefree test ID:** `T-M08-SENSITIVITY`; test asserts held/no-change/degraded behavior, not inherited psychology.
- **Requested patch:** `neo_v3/actor/sensitivity.py :: def record_sensitivity(state: ActorSnapshotV1, episode: EpisodeV1, basis_refs: list[EvidenceRef]) -> SensitivityRecord`.
- **All direct source files:** `v3/core/state.py` (`19e968d45e9d…`); `v3/psyche/channels.py` (`2d00bf6b8720…`); `v3/engine/effects/metabolization_effects.py` (`d4775271ca09…`).

### M09 — ADAPT — callable

- **Exact symbols (class + functions):** `Crack; update_cracks; ensure_min_cracks`
- **Source location:** `v3/core/state.py:151; v3/systems/cracks.py:25; v3/core/invariants.py:253`; primary hash file `v3/core/state.py` SHA-256 `19e968d45e9d81eb7629f1c237dbc55119fec8fc7db0b29e2b39b2476d12ada2`.
- **Caller/callsite:** yearly_step.py:29; cracks.py; derived.py:180.
- **Reads / writes / effects:** events; crack list → crack intensity/latent; placeholder list; only intensify-range cap; placeholders inserted.
- **Historical hazard:** placeholder pathology; demographic/age seeds; no activation/deactivation.
- **Retain / replace:** episode-linked tension carrier and bounded event delta.
- **New adapter:** `neo_v3/actor/tension.py`; import `from neo_v3.actor.tension import TensionRecord, transition_tension`; signature `def transition_tension(state: ActorSnapshotV1, episode: EpisodeV1, operation: TensionOp) -> TensionRecord`; output type `TensionRecord`.
- **Owner / migration:** actor; map only episode-linked tension; archive placeholders/demographic atoms.
- **First future semantic consumer:** CAN011.create_tension → C9 — **TO_BUILD** (not a live import).
- **Runnable sourcefree test ID:** `T-M09-TENSION`; test asserts held/no-change/degraded behavior, not inherited psychology.
- **Requested patch:** `neo_v3/actor/tension.py :: def transition_tension(state: ActorSnapshotV1, episode: EpisodeV1, operation: TensionOp) -> TensionRecord`.
- **All direct source files:** `v3/core/state.py` (`19e968d45e9d…`); `v3/systems/cracks.py` (`b11a87e87be2…`); `v3/core/invariants.py` (`81298f3fc51b…`).

### M10 — ADAPT — callable

- **Exact symbols (class + functions):** `Buffer; BufferCostProfile; update_buffers`
- **Source location:** `v3/core/state.py:176; v3/core/state.py:164; v3/systems/buffers.py:73`; primary hash file `v3/core/state.py` SHA-256 `19e968d45e9d81eb7629f1c237dbc55119fec8fc7db0b29e2b39b2476d12ada2`.
- **Caller/callsite:** yearly_step.py:113; derived.py:167.
- **Reads / writes / effects:** events; buffers; capacity → buffer strength; capacity deductions; cost subtraction.
- **Historical hazard:** support/cost has no actual provider, resource, relation or timing.
- **Retain / replace:** support-with-resource/cost carrier.
- **New adapter:** `neo_v3/actor/support.py`; import `from neo_v3.actor.support import SupportRecord, apply_support`; signature `def apply_support(state: ActorSnapshotV1, support_ref: SupportRef, activity: ActivityRef) -> SupportRecord`; output type `SupportRecord`.
- **Owner / migration:** actor + world support; map source-qualified support; archive 0 defaults.
- **First future semantic consumer:** CAN011.support_record → C9 — **TO_BUILD** (not a live import).
- **Runnable sourcefree test ID:** `T-M10-SUPPORT`; test asserts held/no-change/degraded behavior, not inherited psychology.
- **Requested patch:** `neo_v3/actor/support.py :: def apply_support(state: ActorSnapshotV1, support_ref: SupportRef, activity: ActivityRef) -> SupportRecord`.
- **All direct source files:** `v3/core/state.py` (`19e968d45e9d…`); `v3/systems/buffers.py` (`9c9ed09001da…`).

### M11 — ADAPT — callable

- **Exact symbols (class + functions):** `Framework; update_framework_weights; enforce_framework_caps`
- **Source location:** `v3/core/state.py:187; v3/systems/frameworks.py:33; v3/systems/frameworks.py:104`; primary hash file `v3/core/state.py` SHA-256 `19e968d45e9d81eb7629f1c237dbc55119fec8fc7db0b29e2b39b2476d12ada2`.
- **Caller/callsite:** yearly_step.py:135; derived.py; persona_sheet.py.
- **Reads / writes / effects:** seeds/events; framework weights/tenure → weight, tenure, capacity/psych; acute/chronic operator; dormancy.
- **Historical hazard:** age/class/religion seeds; age-derived tenure; no acquisition/use.
- **Retain / replace:** acute/chronic operator and stable mediator carrier.
- **New adapter:** `neo_v3/actor/mediator.py`; import `from neo_v3.actor.mediator import InterpretiveMediatorRecord, apply_mediator_use`; signature `def apply_mediator_use(state: ActorSnapshotV1, mediator_ref: MediatorRef, activity_ref: ActivityRef) -> InterpretiveMediatorRecord`; output type `InterpretiveMediatorRecord`.
- **Owner / migration:** actor; map source-qualified mediator; archive demographic recipes.
- **First future semantic consumer:** CAN011.mediator_lookup → C9 — **TO_BUILD** (not a live import).
- **Runnable sourcefree test ID:** `T-M11-MEDIATOR`; test asserts held/no-change/degraded behavior, not inherited psychology.
- **Requested patch:** `neo_v3/actor/mediator.py :: def apply_mediator_use(state: ActorSnapshotV1, mediator_ref: MediatorRef, activity_ref: ActivityRef) -> InterpretiveMediatorRecord`.
- **All direct source files:** `v3/core/state.py` (`19e968d45e9d…`); `v3/systems/frameworks.py` (`0d59fc6e1770…`).

### M12 — ADAPT — callable

- **Exact symbols (class + function):** `CollectiveInfrastructure; update_collective_infrastructure`
- **Source location:** `v3/core/state.py:218; v3/systems/infrastructure.py:25`; primary hash file `v3/core/state.py` SHA-256 `19e968d45e9d81eb7629f1c237dbc55119fec8fc7db0b29e2b39b2476d12ada2`.
- **Caller/callsite:** yearly_step.py:160; topology.py; derived.py.
- **Reads / writes / effects:** events; five actor scalars → five infrastructure scalars; event deltas.
- **Historical hazard:** institutions/ties/power copied into actor; zero-as-unknown.
- **Retain / replace:** typed references to collective conditions.
- **New adapter:** `neo_v3/world/institution.py`; import `from neo_v3.world.institution import InstitutionRef, ParticipationRef`; signature `def bind_institution(state: ActorSnapshotV1, institution_ref: InstitutionRef) -> ParticipationRef`; output type `ParticipationRef`.
- **Owner / migration:** world; move institution/collective facts to world; archive actor scalars.
- **First future semantic consumer:** C8.world_relation_read → C9 — **TO_BUILD** (not a live import).
- **Runnable sourcefree test ID:** `T-M12-INSTITUTION`; test asserts held/no-change/degraded behavior, not inherited psychology.
- **Requested patch:** `neo_v3/world/institution.py :: def bind_institution(state: ActorSnapshotV1, institution_ref: InstitutionRef) -> ParticipationRef`.
- **All direct source files:** `v3/core/state.py` (`19e968d45e9d…`); `v3/systems/infrastructure.py` (`a062192707bb…`).

### M13 — ADAPT — callable

- **Exact symbols (class + function):** `PracticeStack; update_practice_stack`
- **Source location:** `v3/core/state.py:231; v3/systems/practices.py:19`; primary hash file `v3/core/state.py` SHA-256 `19e968d45e9d81eb7629f1c237dbc55119fec8fc7db0b29e2b39b2476d12ada2`.
- **Caller/callsite:** yearly_step.py:160; flow.py:500; persona_sheet.py.
- **Reads / writes / effects:** events/seed scalars; practice values → six practice scalars; event/label/route increment.
- **Historical hazard:** SES/age/religiosity seeds; no actual activity/support/loss.
- **Retain / replace:** persistent practice carrier and activity seam.
- **New adapter:** `neo_v3/actor/practice.py`; import `from neo_v3.actor.practice import PracticeRecord, transition_practice`; signature `def transition_practice(state: ActorSnapshotV1, activity_ref: ActivityRef, operation: PracticeOp) -> PracticeRecord`; output type `PracticeRecord`.
- **Owner / migration:** actor; map only enacted/source-qualified practice; archive seeds.
- **First future semantic consumer:** CAN011.practice_lookup → C9 — **TO_BUILD** (not a live import).
- **Runnable sourcefree test ID:** `T-M13-PRACTICE`; test asserts held/no-change/degraded behavior, not inherited psychology.
- **Requested patch:** `neo_v3/actor/practice.py :: def transition_practice(state: ActorSnapshotV1, activity_ref: ActivityRef, operation: PracticeOp) -> PracticeRecord`.
- **All direct source files:** `v3/core/state.py` (`19e968d45e9d…`); `v3/systems/practices.py` (`b984397e5e8c…`).

### M14 — ADAPT — callable

- **Exact symbols (class + functions):** `PeakRouting; update_loop_topology; update_solidarity_boundary; update_coherence`
- **Source location:** `v3/core/state.py:257; v3/systems/topology.py:50; v3/systems/boundary.py:43; v3/systems/coherence.py:18`; primary hash file `v3/core/state.py` SHA-256 `19e968d45e9d81eb7629f1c237dbc55119fec8fc7db0b29e2b39b2476d12ada2`.
- **Caller/callsite:** yearly_step.py:166; derived.py:135; persona_sheet.py.
- **Reads / writes / effects:** state infrastructure/practice/boundary; events → loop enum, boundary, coherence; fixed threshold switches; one-step boundary.
- **Historical hazard:** global enum; event-label boundary; no relation edge.
- **Retain / replace:** consecutive-year hysteresis and bounded reversal technique.
- **New adapter:** `neo_v3/actor/orientation.py`; import `from neo_v3.actor.orientation import FunctionalConnectionRecord, OrientationConfiguration, transition_orientation`; signature `def transition_orientation(state: ActorSnapshotV1, relation_refs: list[RelationRef], operation: OrientationOp) -> OrientationConfiguration`; output type `OrientationConfiguration + FunctionalConnectionRecord`.
- **Owner / migration:** actor + world relation; archive enum as ontology; preserve hysteresis evidence.
- **First future semantic consumer:** C9.configuration_read / SYN02-C — **TO_BUILD** (not a live import).
- **Runnable sourcefree test ID:** `T-M14-HYSTERESIS`; test asserts held/no-change/degraded behavior, not inherited psychology.
- **Requested patch:** `neo_v3/actor/orientation.py :: def transition_orientation(state: ActorSnapshotV1, relation_refs: list[RelationRef], operation: OrientationOp) -> OrientationConfiguration`.
- **All direct source files:** `v3/core/state.py` (`19e968d45e9d…`); `v3/systems/topology.py` (`4e3b9b64399d…`); `v3/systems/boundary.py` (`e8c2495f5bd0…`); `v3/systems/coherence.py` (`1bf8c1bee7a4…`).

### M15 — ADAPT — constant

- **Exact symbols (constant + functions):** `NEED_AXES; derive_child_expectation_baseline; infer_parent_baseline_and_regime`
- **Source location:** `v3/core/state.py:305; v3/engine/expectation_baseline.py:107; v3/io/parent_baseline_from_behavior.py:25`; primary hash file `v3/core/state.py` SHA-256 `19e968d45e9d81eb7629f1c237dbc55119fec8fc7db0b29e2b39b2476d12ada2`.
- **Caller/callsite:** identity_to_backbone.py:514; striving_objects.py:256; llm_contract.py:735.
- **Reads / writes / effects:** parent/identity; need-axis rules → expectation labels; child model; 50/50/50 and hopeful fill.
- **Historical hazard:** unknown parent→hopeful; flat labels; no actual care.
- **Retain / replace:** finite need vocabulary and scoped expectation carrier.
- **New adapter:** `neo_v3/actor/expectation.py`; import `from neo_v3.actor.expectation import NeedAxis, ExpectationRecord, record_expectation`; signature `def record_expectation(state: ActorSnapshotV1, care_episode: EpisodeV1, axis: NeedAxis) -> ExpectationRecord`; output type `ExpectationRecord`.
- **Owner / migration:** actor; preserve axes; archive hopeless/hopeful defaults; unknown remains unknown.
- **First future semantic consumer:** CAN010.expectation_read → C9 — **TO_BUILD** (not a live import).
- **Runnable sourcefree test ID:** `T-M15-EXPECTATION`; test asserts held/no-change/degraded behavior, not inherited psychology.
- **Requested patch:** `neo_v3/actor/expectation.py :: def record_expectation(state: ActorSnapshotV1, care_episode: EpisodeV1, axis: NeedAxis) -> ExpectationRecord`.
- **All direct source files:** `v3/core/state.py` (`19e968d45e9d…`); `v3/engine/expectation_baseline.py` (`632e1e608bfc…`); `v3/io/parent_baseline_from_behavior.py` (`4e5be6448a5b…`).

### M16 — ADAPT — callable

- **Exact symbols (class + functions):** `StrivingObject; spawn_striving_objects_for_age; update_existing_objects; update_striving_step`
- **Source location:** `v3/core/state.py:313; v3/engine/striving_objects.py:127/216/242`; primary hash file `v3/core/state.py` SHA-256 `19e968d45e9d81eb7629f1c237dbc55119fec8fc7db0b29e2b39b2476d12ada2`.
- **Caller/callsite:** yearly_step.py:146; expectation_events.py:169; llm_contract.py:741.
- **Reads / writes / effects:** age/baseline; static map; state.striving_objects → striving objects; random support/feasibility; active list; age spawn/random retirement.
- **Historical hazard:** age/proxy spawn; unnamed RNG; hopeful setdefault; retired history removed.
- **Retain / replace:** stable object identity and exact event seam.
- **New adapter:** `neo_v3/actor/motive.py`; import `from neo_v3.actor.motive import MotiveTargetRecord, transition_motive`; signature `def transition_motive(state: ActorSnapshotV1, activity_ref: ActivityRef, object_ref: ObjectRef) -> MotiveTargetRecord`; output type `MotiveTargetRecord`.
- **Owner / migration:** actor; map only activity-formed targets; archive age/random objects.
- **First future semantic consumer:** CAN010.motive_target_read → C9 — **TO_BUILD** (not a live import).
- **Runnable sourcefree test ID:** `T-M16-MOTIVE`; test asserts held/no-change/degraded behavior, not inherited psychology.
- **Requested patch:** `neo_v3/actor/motive.py :: def transition_motive(state: ActorSnapshotV1, activity_ref: ActivityRef, object_ref: ObjectRef) -> MotiveTargetRecord`.
- **All direct source files:** `v3/core/state.py` (`19e968d45e9d…`); `v3/engine/striving_objects.py` (`78c79a9312b0…`).

### M17 — ADAPT — callable

- **Exact symbols (class + function (corrected actual)):** `GiftShard; DisruptionShard; apply_gift_disruption_shards_from_events`
- **Source location:** `v3/core/state.py:339/353; v3/engine/expectation_events.py:103; v3/engine/effects/delta_templates.py:361-362`; primary hash file `v3/engine/expectation_events.py` SHA-256 `307ae929a43935170a2f792b4a702a02ac54819a4fa897aa3fef4a099a96cb49`.
- **Caller/callsite:** delta_templates.py:361-362; run_llm_band.py.
- **Reads / writes / effects:** selected events with expectation_type + active striving_object_id → gift_shards/disruption_shards; one-valence positive or negative shard.
- **Historical hazard:** nonexistent create_gift/disruption_shard functions; mono-valence; label authority.
- **Retain / replace:** witnessed event shell and exact striving ID seam.
- **New adapter:** `neo_v3/actor/impression.py`; import `from neo_v3.actor.impression import ImpressionRecord, record_impression`; signature `def record_impression(state: ActorSnapshotV1, event: EpisodeV1, access: AccessEnvelope) -> ImpressionRecord`; output type `ImpressionRecord`.
- **Owner / migration:** actor; archive one-valence shards; map only mixed/source-qualified impressions.
- **First future semantic consumer:** CAN008.impression_create → C9 — **TO_BUILD** (not a live import).
- **Runnable sourcefree test ID:** `T-M17-IMPRESSION`; test asserts held/no-change/degraded behavior, not inherited psychology.
- **Requested patch:** `neo_v3/actor/impression.py :: def record_impression(state: ActorSnapshotV1, event: EpisodeV1, access: AccessEnvelope) -> ImpressionRecord`.
- **All direct source files:** `v3/core/state.py` (`19e968d45e9d…`); `v3/engine/expectation_events.py` (`307ae929a439…`); `v3/engine/effects/delta_templates.py` (`7d99ddf26fd4…`).

### M18 — ADAPT — callable

- **Exact symbols (class + functions):** `RuptureShard; create_rupture_shard_from_event; update_wound_vector_from_rupture`
- **Source location:** `v3/core/state.py:369; v3/engine/effects/metabolization_effects.py:144/239`; primary hash file `v3/engine/effects/metabolization_effects.py` SHA-256 `d4775271ca097e99e615cee19b381a478ad6d90a25051c5fce1b1e0e3c1adb1e`.
- **Caller/callsite:** delta_templates.py:355; simulation.py:539; maybe_inject.
- **Reads / writes / effects:** event/rupture data; WoundVector → rupture_shards; process; wound_vector; shard/process creation; wound bump on age path.
- **Historical hazard:** age/global RNG; malheur→micro; direct wound; no parents.
- **Retain / replace:** immutable rupture carrier and exact event seam.
- **New adapter:** `neo_v3/actor/rupture.py`; import `from neo_v3.actor.rupture import RuptureRecord, admit_rupture`; signature `def admit_rupture(state: ActorSnapshotV1, event: CanonicalEventV1, basis: RuptureBasis, rule: RuleRef) -> RuptureRecord`; output type `RuptureRecord`.
- **Owner / migration:** actor; map only admitted rupture; archive age/random/wound atoms.
- **First future semantic consumer:** CAN012.rupture_admit → C9 — **TO_BUILD** (not a live import).
- **Runnable sourcefree test ID:** `T-M18-RUPTURE`; test asserts held/no-change/degraded behavior, not inherited psychology.
- **Requested patch:** `neo_v3/actor/rupture.py :: def admit_rupture(state: ActorSnapshotV1, event: CanonicalEventV1, basis: RuptureBasis, rule: RuleRef) -> RuptureRecord`.
- **All direct source files:** `v3/core/state.py` (`19e968d45e9d…`); `v3/engine/effects/metabolization_effects.py` (`d4775271ca09…`).

### M19 — ADAPT — callable

- **Exact symbols (class + functions):** `MetabolizationProcess; compute_metabolization_delta; update_metabolization_and_plasticity_step`
- **Source location:** `v3/core/state.py:392; v3/engine/effects/metabolization_effects.py:358/521`; primary hash file `v3/core/state.py` SHA-256 `19e968d45e9d81eb7629f1c237dbc55119fec8fc7db0b29e2b39b2476d12ada2`.
- **Caller/callsite:** yearly_step.py:138; stability_inertia.py:40; persona_sheet.py:928.
- **Reads / writes / effects:** process fields; prior rendered_output; psych capacity → process biases/plasticity; narration_support; psych capacity; cluster deltas and prose support.
- **Historical hazard:** rendered prose becomes support; no status/IRR producer; indefinite deltas.
- **Retain / replace:** process carrier and raw/working shell.
- **New adapter:** `neo_v3/actor/metabolization.py`; import `from neo_v3.actor.metabolization import MetabolizationProcessRecord, transition_metabolization`; signature `def transition_metabolization(state: ActorSnapshotV1, process_ref: ProcessRef, support_refs: list[SupportRef], rule: RuleRef) -> MetabolizationProcessRecord`; output type `MetabolizationProcessRecord`.
- **Owner / migration:** actor; map process identity; archive prose-derived support/status defaults.
- **First future semantic consumer:** CAN012.process_read → C9 — **TO_BUILD** (not a live import).
- **Runnable sourcefree test ID:** `T-M19-PROCESS`; test asserts held/no-change/degraded behavior, not inherited psychology.
- **Requested patch:** `neo_v3/actor/metabolization.py :: def transition_metabolization(state: ActorSnapshotV1, process_ref: ProcessRef, support_refs: list[SupportRef], rule: RuleRef) -> MetabolizationProcessRecord`.
- **All direct source files:** `v3/core/state.py` (`19e968d45e9d…`); `v3/engine/effects/metabolization_effects.py` (`d4775271ca09…`); `v3/systems/stability_inertia.py` (`5a11c8b07eaf…`).

### M20 — ADAPT — callable

- **Exact symbols (class + functions):** `Magnet; apply_selected_magnets_to_state; update_active_magnets_step; build_relational_field_projection`
- **Source location:** `v3/core/state.py:205; v3/engine/active_magnets.py:25/58; v3/systems/relational_field.py:13`; primary hash file `v3/core/state.py` SHA-256 `19e968d45e9d81eb7629f1c237dbc55119fec8fc7db0b29e2b39b2476d12ada2`.
- **Caller/callsite:** run_llm_band.py:270; yearly_step.py:146; persona_sheet.py.
- **Reads / writes / effects:** magnet candidates/state; strata → active magnets; relational projection; intensity/decay; label heuristics.
- **Historical hazard:** parent labels; who dropped; label-to-practice; secret origin.
- **Retain / replace:** entity/relation reference, decay and field projection shell.
- **New adapter:** `neo_v3/actor/relation.py`; import `from neo_v3.actor.relation import RelationRecord, ActorEntityRef, MagnetView`; signature `def record_relation(state: ActorSnapshotV1, entity_ref: ActorEntityRef, history: RelationHistory) -> RelationRecord`; output type `RelationRecord`.
- **Owner / migration:** actor + world relation; map exact entity refs; archive mother/father labels.
- **First future semantic consumer:** C8.relation_read → C9/world — **TO_BUILD** (not a live import).
- **Runnable sourcefree test ID:** `T-M20-RELATION`; test asserts held/no-change/degraded behavior, not inherited psychology.
- **Requested patch:** `neo_v3/actor/relation.py :: def record_relation(state: ActorSnapshotV1, entity_ref: ActorEntityRef, history: RelationHistory) -> RelationRecord`.
- **All direct source files:** `v3/core/state.py` (`19e968d45e9d…`); `v3/engine/active_magnets.py` (`68a7b75aa4bb…`); `v3/systems/relational_field.py` (`75cfd5f27528…`).

### M21 — ADAPT — callable

- **Exact symbols (functions):** `run_pressure_flow_cycle; _domain_charge_ledger; _channel_conductance; _update_memory; derive_vitality_profile; derive_insulation_profile`
- **Source location:** `v3/psyche/flow.py:753/406/366/678; v3/psyche/vitality.py:85; v3/psyche/insulation.py:72`; primary hash file `v3/psyche/flow.py` SHA-256 `6da4effde2b1ccb7c346f73b17632ceee3a7a8c37a63a10f096753d070ab1d3d`.
- **Caller/callsite:** yearly_step.py:68; derived.py; persona_sheet.py.
- **Reads / writes / effects:** state capacity/domains/wounds/practice/memory → route trace, psych proxies, pressure history; transactional route snapshot; conductance memory.
- **Historical hazard:** conserved-substance/one-winner ontology; pre-route writes.
- **Retain / replace:** route-scoped transaction, trace and conductance feedback.
- **New adapter:** `neo_v3/psyche/route.py`; import `from neo_v3.psyche.route import RouteTrace, run_route_cycle_transactional`; signature `def run_route_cycle_transactional(state: ActorSnapshotV1, pressure_refs: list[PressureRef]) -> RouteTrace`; output type `RouteTrace`.
- **Owner / migration:** actor psyche; retain exact trace as derived/diagnostic; remove universal conservation.
- **First future semantic consumer:** CAN008.route_trace_read → ANALYST-only — **TO_BUILD** (not a live import).
- **Runnable sourcefree test ID:** `T-M21-ROUTE`; test asserts held/no-change/degraded behavior, not inherited psychology.
- **Requested patch:** `neo_v3/psyche/route.py :: def run_route_cycle_transactional(state: ActorSnapshotV1, pressure_refs: list[PressureRef]) -> RouteTrace`.
- **All direct source files:** `v3/psyche/flow.py` (`6da4effde2b1…`); `v3/psyche/vitality.py` (`56fed88e3729…`); `v3/psyche/insulation.py` (`c8dd5f96111d…`); `v3/core/derived.py` (`e479fc3eba21…`).

### M22 — ADAPT — field

- **Exact symbols (field + constant + functions):** `child_model; PASS1_SYSTEM; backbone_state_from_identity`
- **Source location:** `v3/core/state.py:549; v3/engine/prompts.py:11; v3/io/identity_to_backbone.py:209`; primary hash file `v3/core/state.py` SHA-256 `19e968d45e9d81eb7629f1c237dbc55119fec8fc7db0b29e2b39b2476d12ada2`.
- **Caller/callsite:** identity_to_backbone.py:558; prompts.py:107; scoring.py:148.
- **Reads / writes / effects:** identity; parent baseline/regime → child_model; prompt content; safe-home defaults and hardcoded rules.
- **Historical hazard:** field/constant treated as a literal callable; infant adult theology.
- **Retain / replace:** fallible orientation carrier and unknown-safe history.
- **New adapter:** `neo_v3/actor/development_orientation.py`; import `from neo_v3.actor.development_orientation import DevelopmentalOrientation, record_developmental_orientation`; signature `def record_developmental_orientation(state: ActorSnapshotV1, care_history: CareHistoryRef) -> DevelopmentalOrientation`; output type `DevelopmentalOrientation`.
- **Owner / migration:** actor development; map source-qualified orientation; archive safe-home/taboos.
- **First future semantic consumer:** CAN010.child_orientation_read → C9 — **TO_BUILD** (not a live import).
- **Runnable sourcefree test ID:** `T-M22-DEVELOPMENT`; test asserts held/no-change/degraded behavior, not inherited psychology.
- **Requested patch:** `neo_v3/actor/development_orientation.py :: def record_developmental_orientation(state: ActorSnapshotV1, care_history: CareHistoryRef) -> DevelopmentalOrientation`.
- **All direct source files:** `v3/core/state.py` (`19e968d45e9d…`); `v3/io/identity_to_backbone.py` (`cb29c9595ac4…`); `v3/engine/prompts.py` (`4702de205905…`).

### M23 — ADAPT — field

- **Exact symbols (fields + function):** `autonomy_drive; safety_drive; autonomy_condition; safety_condition; autonomy_safety_micro_drift`
- **Source location:** `v3/core/state.py:555-558; v3/systems/autonomy_safety.py:27`; primary hash file `v3/core/state.py` SHA-256 `19e968d45e9d81eb7629f1c237dbc55119fec8fc7db0b29e2b39b2476d12ada2`.
- **Caller/callsite:** yearly_step.py:113; derived.py:202; health_drift.py.
- **Reads / writes / effects:** state/derived autonomy/safety → condition fields; micro trace; drift/repair of conditions.
- **Historical hazard:** universal 65/68 drives; annual increments treated as evidence.
- **Retain / replace:** actual condition/gap trace.
- **New adapter:** `neo_v3/actor/conditions.py`; import `from neo_v3.actor.conditions import ConditionRecord, record_safety_autonomy`; signature `def record_safety_autonomy(state: ActorSnapshotV1, event: EpisodeV1, access: AccessEnvelope) -> ConditionRecord`; output type `ConditionRecord`.
- **Owner / migration:** actor; archive universal drives; map source-qualified conditions.
- **First future semantic consumer:** CAN008.condition_read → C9 — **TO_BUILD** (not a live import).
- **Runnable sourcefree test ID:** `T-M23-CONDITION`; test asserts held/no-change/degraded behavior, not inherited psychology.
- **Requested patch:** `neo_v3/actor/conditions.py :: def record_safety_autonomy(state: ActorSnapshotV1, event: EpisodeV1, access: AccessEnvelope) -> ConditionRecord`.
- **All direct source files:** `v3/core/state.py` (`19e968d45e9d…`); `v3/systems/autonomy_safety.py` (`fdb6ae0d78bb…`).

### M24 — ADAPT — field

- **Exact symbols (field + function):** `stability_threshold_inertia; stability_inertia_dissipation`
- **Source location:** `v3/core/state.py:560; v3/systems/stability_inertia.py:17`; primary hash file `v3/core/state.py` SHA-256 `19e968d45e9d81eb7629f1c237dbc55119fec8fc7db0b29e2b39b2476d12ada2`.
- **Caller/callsite:** yearly_step.py:139; derived.py:235.
- **Reads / writes / effects:** processes/narration_support/inertia/derived → inertia; section flag; holding/integration/IRR/sealed drains.
- **Historical hazard:** universal drain/neutral point; unsupported status paths.
- **Retain / replace:** source-bounded residue/hysteresis carrier.
- **New adapter:** `neo_v3/actor/residue.py`; import `from neo_v3.actor.residue import ResidueRecord, record_hysteresis`; signature `def record_hysteresis(state: ActorSnapshotV1, process_ref: ProcessRef, support_refs: list[SupportRef]) -> ResidueRecord`; output type `ResidueRecord`.
- **Owner / migration:** actor; archive fixed inertia; map only supported residue.
- **First future semantic consumer:** CAN011.residue_read → C9 — **TO_BUILD** (not a live import).
- **Runnable sourcefree test ID:** `T-M24-RESIDUE`; test asserts held/no-change/degraded behavior, not inherited psychology.
- **Requested patch:** `neo_v3/actor/residue.py :: def record_hysteresis(state: ActorSnapshotV1, process_ref: ProcessRef, support_refs: list[SupportRef]) -> ResidueRecord`.
- **All direct source files:** `v3/core/state.py` (`19e968d45e9d…`); `v3/systems/stability_inertia.py` (`5a11c8b07eaf…`).

### M25 — ADAPT — config

- **Exact symbols (config + functions + test):** `derived_indices_schedule; run_one_year; step_one_year; run_n_years; test_step_order_immutable`
- **Source location:** `v3/v3_yearly_step_order.yaml:21/60; v3/engine/yearly_step.py:12/102; v3/engine/step_runner.py:13; v3/tests/test_architecture_invariants.py:89`; primary hash file `v3/v3_yearly_step_order.yaml` SHA-256 `90496a2cc852ca00ef99c8bd4fcb2b41c9aa43c4aaa9108d3ac8cce0ebe22ffc`.
- **Caller/callsite:** server/generation/simulation.py:538; run_and_print.py:123.
- **Reads / writes / effects:** config/state/derived → year/age; all step state; rendered_output; 19 core/20 executed annual mutation.
- **Historical hazard:** year is causal unit; render/active magnets inside year; no event clock.
- **Retain / replace:** explicit order, schedule assertions, hash/replay.
- **New adapter:** `neo_v3/runtime/scheduler.py`; import `from neo_v3.runtime.scheduler import advance_interval, run_event_sequence`; signature `def advance_interval(state: ActorSnapshotV1, interval: IntervalRef) -> list[CanonicalEventV1]`; output type `CanonicalEventV1`.
- **Owner / migration:** runtime/scheduler; use old 20-step order as slow scaffold; archive annual default semantics.
- **First future semantic consumer:** C9.event_sequence / C12 batch — **TO_BUILD** (not a live import).
- **Runnable sourcefree test ID:** `T-M25-SCHEDULER`; test asserts held/no-change/degraded behavior, not inherited psychology.
- **Requested patch:** `neo_v3/runtime/scheduler.py :: def advance_interval(state: ActorSnapshotV1, interval: IntervalRef) -> list[CanonicalEventV1]`.
- **All direct source files:** `v3/v3_yearly_step_order.yaml` (`90496a2cc852…`); `v3/engine/yearly_step.py` (`da3147c3da7f…`); `v3/engine/step_runner.py` (`5a737c1704ea…`); `v3/tests/test_architecture_invariants.py` (`bb2baec1c57d…`).

### M26 — REUSE (invariant) — callable

- **Exact symbols (class + functions + test):** `DerivedIndices; compute_all_derived; assert_no_derived_fields_in_backbone; test_no_derived_fields_in_backbone_state`
- **Source location:** `v3/core/derived.py:14/322; v3/core/invariants.py:346; v3/tests/test_architecture_invariants.py:123`; primary hash file `v3/core/derived.py` SHA-256 `e479fc3eba21734752c372742fb2ee247cbdde6a73ac42545dc30b5039301360`.
- **Caller/callsite:** yearly_step.py:189; all derived readers.
- **Reads / writes / effects:** BackboneState → derived return; metabolic_style; registers; hidden persistent writes.
- **Historical hazard:** fixed-name invariant misses registers/metabolic_style.
- **Retain / replace:** pure projection concept and exact dependency declaration.
- **New adapter:** `neo_v3/derived/registry.py`; import `from neo_v3.derived.registry import DerivedViewRegistry, compute_view`; signature `def compute_view(snapshot: ActorSnapshotV1, view_id: ViewId) -> DerivedViewValue`; output type `DerivedViewValue`.
- **Owner / migration:** derived/read-only; clone/freeze old state; recompute views; archive caches.
- **First future semantic consumer:** all read-only C9 views — **TO_BUILD** (not a live import).
- **Runnable sourcefree test ID:** `T-M26-DERIVED`; test asserts held/no-change/degraded behavior, not inherited psychology.
- **Requested patch:** `neo_v3/derived/registry.py :: def compute_view(snapshot: ActorSnapshotV1, view_id: ViewId) -> DerivedViewValue`.
- **All direct source files:** `v3/core/state.py` (`19e968d45e9d…`); `v3/core/derived.py` (`e479fc3eba21…`); `v3/core/invariants.py` (`81298f3fc51b…`); `v3/tests/test_architecture_invariants.py` (`bb2baec1c57d…`).

### M27 — ADAPT — callable

- **Exact symbols (functions):** `parse_candidate_packet; build_pass1_prompt; run_llm_band_year`
- **Source location:** `v3/engine/llm_contract.py:87; v3/engine/prompts.py:107; v3/engine/run_llm_band.py:146`; primary hash file `v3/engine/llm_contract.py` SHA-256 `f024debf7b8a637e91c546689a0bed31baff55d98f1378b06cb82ebb4c0fe9cf`.
- **Caller/callsite:** server generation; run_and_print.py:139.
- **Reads / writes / effects:** LLM text; state summary → CandidatePacket; selected state via band; proposal then mutation.
- **Historical hazard:** selected proposals become backbone deltas; no canonical event.
- **Retain / replace:** proposal-only/caps/provenance contract.
- **New adapter:** `neo_v3/llm/batch.py`; import `from neo_v3.llm.batch import BatchProposal, propose_batch`; signature `def propose_batch(state: ActorSnapshotV1, prompt: str) -> BatchProposal`; output type `BatchProposal`.
- **Owner / migration:** runtime/LLM proposal; retain parser/provenance; split effects.
- **First future semantic consumer:** event realization proposal queue — **TO_BUILD** (not a live import).
- **Runnable sourcefree test ID:** `T-M27-PROPOSAL`; test asserts held/no-change/degraded behavior, not inherited psychology.
- **Requested patch:** `neo_v3/llm/batch.py :: def propose_batch(state: ActorSnapshotV1, prompt: str) -> BatchProposal`.
- **All direct source files:** `v3/engine/llm_contract.py` (`f024debf7b8a…`); `v3/engine/prompts.py` (`4702de205905…`); `v3/engine/run_llm_band.py` (`120e17746221…`).

### M28 — ADAPT — callable

- **Exact symbols (functions):** `score_event_candidate; select_candidates; run_llm_band_year; apply_deltas_to_state`
- **Source location:** `v3/engine/scoring.py:32/197; v3/engine/run_llm_band.py:146; v3/engine/effects/delta_templates.py:254`; primary hash file `v3/engine/scoring.py` SHA-256 `36833287c72ffa40d0ece1ebc66fb0d685a92fc71aab1d211be9b21bfd0a82cb`.
- **Caller/callsite:** run_llm_band.py:240/269.
- **Reads / writes / effects:** packet/summary/state → merged capacity/domain/wound/practice deltas; premerged application.
- **Historical hazard:** no hard admission; unseeded surprise; no event ledger; fallback.
- **Retain / replace:** finite selection/caps/provenance shell.
- **New adapter:** `neo_v3/runtime/admission.py`; import `from neo_v3.runtime.admission import CanonicalEventV1, admit_event, select_event`; signature `def admit_event(state: ActorSnapshotV1, proposal: ProspectiveSpec, source: SourceRef) -> CanonicalEventV1`; output type `CanonicalEventV1`.
- **Owner / migration:** event ledger; discard merged deltas; rebuild event rows.
- **First future semantic consumer:** C8.event_admit → C9/CAN008 — **TO_BUILD** (not a live import).
- **Runnable sourcefree test ID:** `T-M28-ADMISSION`; test asserts held/no-change/degraded behavior, not inherited psychology.
- **Requested patch:** `neo_v3/runtime/admission.py :: def admit_event(state: ActorSnapshotV1, proposal: ProspectiveSpec, source: SourceRef) -> CanonicalEventV1`.
- **All direct source files:** `v3/engine/scoring.py` (`36833287c72f…`); `v3/engine/run_llm_band.py` (`120e17746221…`); `v3/engine/effects/delta_templates.py` (`7d99ddf26fd4…`).

### M29 — REUSE (immediate body) — callable

- **Exact symbols (functions + test):** `build_render_packet; build_pass2_prompt; render_year; test_llm_no_backbone_mutation`
- **Source location:** `v3/engine/llm_contract.py:791; v3/engine/prompts.py:132; v3/render/phenomenology.py:55; v3/tests/test_architecture_invariants.py:51`; primary hash file `v3/render/phenomenology.py` SHA-256 `f2f18c1d9ba705212846af41b33cb1dfd2ad986dae4b686873687c2e6d1a653d`.
- **Caller/callsite:** run_llm_band.py:380; server; persona.
- **Reads / writes / effects:** render packet/state → rendered_output only; immediate one-way surface.
- **Historical hazard:** full band not render-only; retry/callback; downstream prose feedback.
- **Retain / replace:** immediate render body and surface allowlist.
- **New adapter:** `neo_v3/surface/render.py`; import `from neo_v3.surface.render import SurfaceRecord, render_surface`; signature `def render_surface(input: RenderInput) -> SurfaceRecord`; output type `SurfaceRecord`.
- **Owner / migration:** surface; retain render body; archive any causal read.
- **First future semantic consumer:** V2.surface_read / ADP017 — **TO_BUILD** (not a live import).
- **Runnable sourcefree test ID:** `T-M29-RENDER`; test asserts held/no-change/degraded behavior, not inherited psychology.
- **Requested patch:** `neo_v3/surface/render.py :: def render_surface(input: RenderInput) -> SurfaceRecord`.
- **All direct source files:** `v3/engine/llm_contract.py` (`f024debf7b8a…`); `v3/engine/prompts.py` (`4702de205905…`); `v3/render/phenomenology.py` (`f2f18c1d9ba7…`); `v3/tests/test_architecture_invariants.py` (`bb2baec1c57d…`).

### M30 — REUSE (invariant) — prose_abstraction

- **Exact symbols (prose abstraction + functions):** `build_persona_sheet; prepare_conversation_turn`
- **Source location:** `v3/V3_UNDERLIES_V2_ARTICULATION.md (prose; no callable line); v3/io/persona_sheet.py:579; v2/conversation_engine.py:2079`; primary hash file `v3/io/persona_sheet.py` SHA-256 `4a0009533443baef2786fc498c7f8db3ead7d133d8ee7e97e6d7128d4322a00e`.
- **Caller/callsite:** server; V2 chat.
- **Prose/design artifacts (not callables):** v3/V3_UNDERLIES_V2_ARTICULATION.md (design articulation; prose, not a callable).
- **Reads / writes / effects:** state/persona state → V2 prompt/surface; one-person surface.
- **Historical hazard:** age<17→35; parent narrative; prose feedback.
- **Retain / replace:** one-person/read-only V2 jurisdiction.
- **New adapter:** `neo_v3/surface/read.py`; import `from neo_v3.surface.read import ActorVisibleSurface, read_surface`; signature `def read_surface(state: ActorSnapshotV1, access: AccessEnvelope) -> ActorVisibleSurface`; output type `ActorVisibleSurface`.
- **Owner / migration:** surface read/V2; remove age/parent substitutions; no write-back.
- **First future semantic consumer:** V2.actor_visible_read / ADP016/017 — **TO_BUILD** (not a live import).
- **Runnable sourcefree test ID:** `T-M30-V2`; test asserts held/no-change/degraded behavior, not inherited psychology.
- **Requested patch:** `neo_v3/surface/read.py :: def read_surface(state: ActorSnapshotV1, access: AccessEnvelope) -> ActorVisibleSurface`.
- **All direct source files:** `v3/V3_UNDERLIES_V2_ARTICULATION.md` (`5a0f11276a83…`); `v3/io/persona_sheet.py` (`4a0009533443…`); `v2/conversation_engine.py` (`766bee296379…`).

### M31 — REPLACE — prose_abstraction

- **Exact symbols (docs + functions):** `match_life_course_to_type; infer_parent_type; get_parent_type_effects_for_child`
- **Source location:** `v2/ENNEAGRAM_EMERGENCE_SYSTEM.md (prose; no callable line); v2/PROBABILISTIC_ENNEAGRAM_SYSTEM.md (prose; no callable line); v2/enneagram_wisdom.py:615; v2/parent_type_inference.py:33/143`; primary hash file `v2/enneagram_wisdom.py` SHA-256 `95c018092eae44f319bead262c7d815c477df85ede4f7574e2b08aeff17ce34d`.
- **Caller/callsite:** V2 life generation.
- **Prose/design artifacts (not callables):** v2/ENNEAGRAM_EMERGENCE_SYSTEM.md; v2/PROBABILISTIC_ENNEAGRAM_SYSTEM.md (design documents; prose, not callables).
- **Reads / writes / effects:** life/parent data → type and type effects; random type/effects.
- **Historical hazard:** type-at-7, parent-type determinism.
- **Retain / replace:** optional forensic/noncausal label only.
- **New adapter:** `neo_v3/legacy/typology.py`; import `from neo_v3.legacy.typology import OptionalTypologyView, archive_enneagram`; signature `def archive_enneagram(value: LegacyType) -> LegacyArtifact`; output type `OptionalTypologyView`.
- **Owner / migration:** legacy archive; archive type; no causal import.
- **First future semantic consumer:** V2.optional_typology_view — **RULE_HELD** (not a live import).
- **Runnable sourcefree test ID:** `T-M31-TYPE`; test asserts held/no-change/degraded behavior, not inherited psychology.
- **Requested patch:** `neo_v3/legacy/typology.py :: def archive_enneagram(value: LegacyType) -> LegacyArtifact`.
- **All direct source files:** `v2/ENNEAGRAM_EMERGENCE_SYSTEM.md` (`95f8876926dd…`); `v2/PROBABILISTIC_ENNEAGRAM_SYSTEM.md` (`3a63f8caa258…`); `v2/enneagram_wisdom.py` (`95c018092eae…`); `v2/parent_type_inference.py` (`b05632d01c48…`).

### M32 — ADAPT — callable

- **Exact symbols (functions):** `normalize_v5_runtime_input_bundle; attach_v5_runtime_input_bundle; build_v5_field_bridge_injection; get_field_injection_for_year`
- **Source location:** `v3/io/v5_bridge.py:40/78; v3/io/v5_field_bridge.py:35; v3/io/field_injection.py:273`; primary hash file `v3/io/v5_bridge.py` SHA-256 `31700b4031a62b0b5ff8257691e460ce47c983f86daaec72f1011bd6f2823baa`.
- **Caller/callsite:** server; field update.
- **Reads / writes / effects:** V5 bundle/field inputs → inert refs; field numbers; integrity-blind merge.
- **Historical hazard:** hardcoded source; blocked values apply.
- **Retain / replace:** inert SourceRef/status/provenance and fail-closed gate.
- **New adapter:** `neo_v3/source/field.py`; import `from neo_v3.source.field import SourceEnvelope, field_injection_decision`; signature `def attach_source_envelope(state: ActorSnapshotV1, envelope: SourceEnvelope) -> None`; output type `SourceEnvelope`.
- **Owner / migration:** source/field + actor; retain source refs; archive old V5 payload.
- **First future semantic consumer:** C8.source_envelope_read → world/C9 — **TO_BUILD** (not a live import).
- **Runnable sourcefree test ID:** `T-M32-SOURCE`; test asserts held/no-change/degraded behavior, not inherited psychology.
- **Requested patch:** `neo_v3/source/field.py :: def attach_source_envelope(state: ActorSnapshotV1, envelope: SourceEnvelope) -> None`.
- **All direct source files:** `v3/io/v5_bridge.py` (`31700b4031a6…`); `v3/io/v5_field_bridge.py` (`444ed1e07443…`); `v3/io/field_injection.py` (`d3750fdb61eb…`).

### M33 — REPLACE — callable

- **Exact symbols (functions):** `_pseudo_seed; _one_event; sample_events`
- **Source location:** `v3/engine/event_engine.py:22/31/127`; primary hash file `v3/engine/event_engine.py` SHA-256 `b57e7ef4df5dabd996dc7de19c1c2c273ad90ee89d73570df1fd85674dd98ded`.
- **Caller/callsite:** yearly_step.py:124.
- **Reads / writes / effects:** state/year/slot → events_this_year; random generic event deltas.
- **Historical hazard:** mechanical random event causality.
- **Retain / replace:** event ID/label/conditioning serialization shell.
- **New adapter:** `neo_v3/world/event_source.py`; import `from neo_v3.world.event_source import WorldEventSource, realize_world_event`; signature `def realize_world_event(source: SourceRef, proposal: ProspectiveSpec) -> CanonicalEventV1`; output type `CanonicalEventV1`.
- **Owner / migration:** world event source; archive mechanical events; map only source-owned.
- **First future semantic consumer:** C8.world_event_read → C9/CAN008 — **TO_BUILD** (not a live import).
- **Runnable sourcefree test ID:** `T-M33-WORLD-EVENT`; test asserts held/no-change/degraded behavior, not inherited psychology.
- **Requested patch:** `neo_v3/world/event_source.py :: def realize_world_event(source: SourceRef, proposal: ProspectiveSpec) -> CanonicalEventV1`.
- **All direct source files:** `v3/engine/event_engine.py` (`b57e7ef4df5d…`).

### M34 — REMOVE — callable

- **Exact symbols (functions):** `parse_candidate_packet_with_fallback; make_fallback_event; fallback_candidate_packet_if_empty; run_llm_band_year`
- **Source location:** `v3/engine/llm_contract.py:159/173/190; v3/engine/run_llm_band.py:146`; primary hash file `v3/engine/llm_contract.py` SHA-256 `f024debf7b8a637e91c546689a0bed31baff55d98f1378b06cb82ebb4c0fe9cf`.
- **Caller/callsite:** run_llm_band.py:216/244.
- **Reads / writes / effects:** empty packet/candidates → fabricated fallback event/deltas; forces a practice event.
- **Historical hazard:** fabricated event and psychic delta.
- **Retain / replace:** integrity/degraded diagnostics only.
- **New adapter:** `neo_v3/runtime/no_event.py`; import `from neo_v3.runtime.no_event import NoEventRecord, hold_missing_proposal`; signature `def hold_missing_proposal(state: ActorSnapshotV1, reason: HoldReason) -> NoEventRecord`; output type `NoEventRecord`.
- **Owner / migration:** runtime no-event; archive fallback; no event import.
- **First future semantic consumer:** C8.no_event_read → C9 admission — **TO_BUILD** (not a live import).
- **Runnable sourcefree test ID:** `T-M34-NO-EVENT`; test asserts held/no-change/degraded behavior, not inherited psychology.
- **Requested patch:** `neo_v3/runtime/no_event.py :: def hold_missing_proposal(state: ActorSnapshotV1, reason: HoldReason) -> NoEventRecord`.
- **All direct source files:** `v3/engine/llm_contract.py` (`f024debf7b8a…`); `v3/engine/run_llm_band.py` (`120e17746221…`).

### M35 — REMOVE — callable

- **Exact symbols (functions):** `ensure_min_cracks; ensure_min_frameworks; run_one_year`
- **Source location:** `v3/core/invariants.py:253/277; v3/engine/yearly_step.py:12`; primary hash file `v3/core/invariants.py` SHA-256 `81298f3fc51b46cda8d72d0db914b672b17b9a35e13004fe59a9b0e29dada5e3`.
- **Caller/callsite:** yearly_step.py:29/42; invariants.py.
- **Reads / writes / effects:** crack/framework count → placeholder crack/framework; minimum objects.
- **Historical hazard:** fabricated psychological content.
- **Retain / replace:** degraded/diagnostic counts only.
- **New adapter:** `neo_v3/actor/valid_empty.py`; import `from neo_v3.actor.valid_empty import ValidEmpty, diagnose_placeholder`; signature `def diagnose_placeholder(state: ActorSnapshotV1) -> ValidEmpty`; output type `ValidEmpty`.
- **Owner / migration:** actor diagnostics; archive placeholders; no causal import.
- **First future semantic consumer:** C9.valid_empty_read / migration — **TO_BUILD** (not a live import).
- **Runnable sourcefree test ID:** `T-M35-VALID-EMPTY`; test asserts held/no-change/degraded behavior, not inherited psychology.
- **Requested patch:** `neo_v3/actor/valid_empty.py :: def diagnose_placeholder(state: ActorSnapshotV1) -> ValidEmpty`.
- **All direct source files:** `v3/core/invariants.py` (`81298f3fc51b…`); `v3/engine/yearly_step.py` (`da3147c3da7f…`).

### M36 — REMOVE — callable

- **Exact symbols (functions):** `infer_parent_baseline_and_regime; derive_child_expectation_baseline`
- **Source location:** `v3/io/parent_baseline_from_behavior.py:25; v3/engine/expectation_baseline.py:107`; primary hash file `v3/io/parent_baseline_from_behavior.py` SHA-256 `4e5be6448a5b76c413492ec2a83b62d9e9a2247ce131a094727d974a17cf750b`.
- **Caller/callsite:** identity_to_backbone.py:518; expectation.
- **Reads / writes / effects:** parent/identity; rules → parent scores; expectation labels; 50→hopeful/safe-home.
- **Historical hazard:** unknown parent becomes positive normal.
- **Retain / replace:** typed unknown/absent and need-axis vocabulary.
- **New adapter:** `neo_v3/actor/unknown.py`; import `from neo_v3.actor.unknown import UnknownExpectation`; signature `def unknown_expectation(axis: NeedAxis, reason: UnknownReason) -> UnknownExpectation`; output type `UnknownExpectation`.
- **Owner / migration:** actor unknown; archive default path; preserve unknown.
- **First future semantic consumer:** CAN010.unknown_expectation_read → C9 — **TO_BUILD** (not a live import).
- **Runnable sourcefree test ID:** `T-M36-UNKNOWN`; test asserts held/no-change/degraded behavior, not inherited psychology.
- **Requested patch:** `neo_v3/actor/unknown.py :: def unknown_expectation(axis: NeedAxis, reason: UnknownReason) -> UnknownExpectation`.
- **All direct source files:** `v3/io/parent_baseline_from_behavior.py` (`4e5be6448a5b…`); `v3/engine/expectation_baseline.py` (`632e1e608bfc…`).

### M37 — ADAPT — callsite

- **Exact symbols (functions + callsite):** `run_simulation_for_session; build_persona_sheet; _trajectory_backstory_from_snapshots; distill_persona_sheet_backstory; _preprocess_backstory`
- **Source location:** `server/generation/simulation.py:71; v3/io/persona_sheet.py:579/470; v3/tools/distill_memory.py:218/72`; primary hash file `server/generation/simulation.py` SHA-256 `5d68ffe3bc6902dc60b90625443a03127cf0d04b4eed4327270a3a0226bc78d1`.
- **Caller/callsite:** server; persona; V2.
- **Reads / writes / effects:** non-LLM year state; backstory → annotation scene; backstory; per-year render and final rerender.
- **Historical hazard:** annotation as memory; final path overwrites.
- **Retain / replace:** interstitial accounting/annotation metadata separate.
- **New adapter:** `neo_v3/surface/annotation.py`; import `from neo_v3.surface.annotation import IntervalAnnotation, record_interval_annotation`; signature `def record_interval_annotation(interval: IntervalRef, material_facts: list[MaterialFact]) -> IntervalAnnotation`; output type `IntervalAnnotation`.
- **Owner / migration:** surface annotation; archive annotation text; no memory import.
- **First future semantic consumer:** ADP016.annotation_read → C9 — **TO_BUILD** (not a live import).
- **Runnable sourcefree test ID:** `T-M37-ANNOTATION`; test asserts held/no-change/degraded behavior, not inherited psychology.
- **Requested patch:** `neo_v3/surface/annotation.py :: def record_interval_annotation(interval: IntervalRef, material_facts: list[MaterialFact]) -> IntervalAnnotation`.
- **All direct source files:** `server/generation/simulation.py` (`5d68ffe3bc69…`); `v3/io/persona_sheet.py` (`4a0009533443…`); `v3/tools/distill_memory.py` (`6bece5ef6602…`).

### M38 — ADAPT — config

- **Exact symbols (config + functions):** `derived_indices_schedule; _compute_derived_after_step; get_derived_schedule`
- **Source location:** `v3/v3_yearly_step_order.yaml:21; v3/engine/yearly_step.py:173; v3/core/config_loader.py:61`; primary hash file `v3/v3_yearly_step_order.yaml` SHA-256 `90496a2cc852ca00ef99c8bd4fcb2b41c9aa43c4aaa9108d3ac8cce0ebe22ffc`.
- **Caller/callsite:** yearly_step.py:55/189.
- **Reads / writes / effects:** step schedule/state → derived fields/cache; two schedule surfaces.
- **Historical hazard:** stale unscheduled fields; hidden writes.
- **Retain / replace:** fail-fast equality and explicit dependency order.
- **New adapter:** `neo_v3/derived/schedule.py`; import `from neo_v3.derived.schedule import DerivedRegistry, compute_view`; signature `def compute_view(snapshot: ActorSnapshotV1, view_id: ViewId) -> DerivedViewValue`; output type `DerivedViewValue`.
- **Owner / migration:** derived/scheduler; recompute views; archive stale cache.
- **First future semantic consumer:** C9.derived_schedule_read / scheduler — **TO_BUILD** (not a live import).
- **Runnable sourcefree test ID:** `T-M38-SCHEDULE`; test asserts held/no-change/degraded behavior, not inherited psychology.
- **Requested patch:** `neo_v3/derived/schedule.py :: def compute_view(snapshot: ActorSnapshotV1, view_id: ViewId) -> DerivedViewValue`.
- **All direct source files:** `v3/v3_yearly_step_order.yaml` (`90496a2cc852…`); `v3/engine/yearly_step.py` (`da3147c3da7f…`); `v3/core/config_loader.py` (`5f953d9661f6…`).

### M39 — REPLACE — callsite

- **Exact symbols (function + alias + callsite):** `maybe_inject_rupture_at_band_age; _maybe_inject_rupture_at_band_age`
- **Source location:** `v3/engine/effects/metabolization_effects.py:273; server/generation/simulation.py:13/539`; primary hash file `v3/engine/effects/metabolization_effects.py` SHA-256 `d4775271ca097e99e615cee19b381a478ad6d90a25051c5fce1b1e0e3c1adb1e`.
- **Caller/callsite:** server after run_one_year.
- **Reads / writes / effects:** state.age; global random; templates → rupture shards/process/wound; age probability injection.
- **Historical hazard:** age/global RNG/outside ledger/wound.
- **Retain / replace:** only rupture/process archive shell.
- **New adapter:** `neo_v3/actor/admitted_disruption.py`; import `from neo_v3.actor.admitted_disruption import AdmittedDisruption, admit_rupture_event`; signature `def admit_rupture_event(state: ActorSnapshotV1, event: CanonicalEventV1, rule: RuleRef) -> AdmittedDisruption`; output type `AdmittedDisruption`.
- **Owner / migration:** actor disruption; archive age injections; no causal import.
- **First future semantic consumer:** CAN012.admitted_disruption_read → C9 — **TO_BUILD** (not a live import).
- **Runnable sourcefree test ID:** `T-M39-DISRUPTION`; test asserts held/no-change/degraded behavior, not inherited psychology.
- **Requested patch:** `neo_v3/actor/admitted_disruption.py :: def admit_rupture_event(state: ActorSnapshotV1, event: CanonicalEventV1, rule: RuleRef) -> AdmittedDisruption`.
- **All direct source files:** `server/generation/simulation.py` (`5d68ffe3bc69…`); `v3/engine/effects/metabolization_effects.py` (`d4775271ca09…`).

### M40 — ADAPT — callable

- **Exact symbols (class + class + functions):** `GenerationIntegrityAccumulator; _generation_state_is_ready; _golden_eligibility_for_session_dir; _validate_stored_persona_for_live_use; _validate_persona_for_store_write`
- **Source location:** `v3/core/generation_integrity.py:13; server/session_state.py:53; server/generation/store.py:77/183/245`; primary hash file `server/generation/store.py` SHA-256 `eb592702327427a22b5d901337e6ee8b251b164ad41fe8848b165a14730a942c`.
- **Caller/callsite:** server store/session.
- **Reads / writes / effects:** generation verdict; persona name/country → readiness/store acceptance; clean_ready even degraded/blocked.
- **Historical hazard:** name/country-only and degraded accepted.
- **Retain / replace:** graded integrity and multi-gate readiness concept.
- **New adapter:** `neo_v3/runtime/readiness.py`; import `from neo_v3.runtime.readiness import ReadinessVector, assess_person_readiness`; signature `def assess_person_readiness(actor: ActorSnapshotV1, gates: ReadinessGates) -> ReadinessVector`; output type `ReadinessVector`.
- **Owner / migration:** session readiness; recompute readiness; archive stored-persona clean_ready.
- **First future semantic consumer:** C12.readiness_gate / store — **TO_BUILD** (not a live import).
- **Runnable sourcefree test ID:** `T-M40-READINESS`; test asserts held/no-change/degraded behavior, not inherited psychology.
- **Requested patch:** `neo_v3/runtime/readiness.py :: def assess_person_readiness(actor: ActorSnapshotV1, gates: ReadinessGates) -> ReadinessVector`.
- **All direct source files:** `server/generation/store.py` (`eb5927023274…`); `server/generation/simulation.py` (`5d68ffe3bc69…`); `server/session_state.py` (`9c9c3b0e2b3b…`); `v3/core/generation_integrity.py` (`5265aac2fda4…`).

## 3. Exact ten-cell reconciliation

| M/N | S05 | Final | Final relation | Why the mark changes or stays |
|---|---:|---:|---|---|
| M09/N01 | X | X | `INDIRECT_CARRIER_ONLY` | Crack/tension carrier has no need-axis or object field; it can only condition a later need-domain response through contradiction, not form a need/object. |
| M10/N01 | X | X | `INDIRECT_CARRIER_ONLY` | Buffer/Support carrier supplies resources/costs; it has no need axis, object, activity or motive formation. |
| M11/N01 | X | X | `INDIRECT_CARRIER_ONLY` | Framework mediates interpretation/capacity; it does not define a need, object, or formed motive. |
| M13/N01 | X | X | `INDIRECT_CARRIER_ONLY` | PracticeStack is a practice-category carrier; no need axis, object, activity episode or motive is represented. |
| M14/N02 | X | — | `UNSUPPORTED` | PeakRouting boundary/loop/coherence has no care, caregiver, expectation, or scoped anticipation function. |
| M18/N01 | X | X | `INDIRECT_CARRIER_ONLY` | RuptureShard records a violated assumption/domain; it does not form a need, object, or motive target. |
| M19/N01 | X | X | `INDIRECT_CARRIER_ONLY` | MetabolizationProcess changes capacity/biases over time; it has no need/object/activity formation field. |
| M24/N01 | X | X | `INDIRECT_CARRIER_ONLY` | Stability inertia is a persistence/residue mechanism; it does not constitute a need or object. |
| M36/N01 | X | X | `INDIRECT_CARRIER_ONLY` | Parent baseline maps NEED_AXES to expectation labels; this is N02 expectation vocabulary, not a formed motive/object. |
| M39/N01 | X | — | `UNSUPPORTED` | Age-band rupture injection has no need/object/activity relation; its old N01 crosswalk warning is stale. |

M17 is not one of the ten crosswalk cells. Its correction is a symbol-identity repair: the prior map named `create_gift_shard_from_event` / `create_disruption_shard_from_event`, which do not exist. The actual callable is `apply_gift_disruption_shards_from_events` (`v3/engine/expectation_events.py:103`), called from `v3/engine/effects/delta_templates.py:361-362`. The retained target remains mixed actor-relative `ImpressionRecord`, not mono-valence gift/disruption shards.

## 4. Literal-symbol audit notes

- M01 is a `BackboneState` class plus serialization/hash helpers and an integrity accumulator; it is not one function.
- M15 is primarily the `NEED_AXES` constant plus expectation functions; M22 is a persisted field/constant/prompt plus constructor; M23 is four persisted fields plus a micro-drift function; M24 is a field plus dissipation function.
- M25 is YAML schedule/config plus runner functions and an architecture test; M26 is a derived class/function plus invariant/test; M29 is a render function/test; M30 is a V2 design articulation plus persona functions.
- M31 is V2 prose/type code only, retained as an optional noncausal archive view; it is not a current V3 literal patch target. M37 references a server callsite plus persona/distillation functions; M39 names both canonical and server-side alias callsites.
- M17 exact names are corrected here; no fake function is carried into the machine matrix. No row silently substitutes a class, field, YAML entry or prose label for a callable.

## 5. Source identity registry (59/59 rehashed)

| # | Path | SHA-256 | Bytes |
|---:|---|---|---:|
| 1 | `server/generation/simulation.py` | `5d68ffe3bc6902dc60b90625443a03127cf0d04b4eed4327270a3a0226bc78d1` | 48212 |
| 2 | `server/generation/store.py` | `eb592702327427a22b5d901337e6ee8b251b164ad41fe8848b165a14730a942c` | 17787 |
| 3 | `server/session_state.py` | `9c9c3b0e2b3bff700af127e03805166102920019d6acd099ee8270fbe63bc15a` | 4824 |
| 4 | `v2/ENNEAGRAM_EMERGENCE_SYSTEM.md` | `95f8876926dda96a33c36925aedacee65645c74863cff68241e6b67457f819ab` | 7291 |
| 5 | `v2/PROBABILISTIC_ENNEAGRAM_SYSTEM.md` | `3a63f8caa258b5d00c4baa5bbe064eacf4b3a0fed3a83560dd2469d1b5654106` | 7926 |
| 6 | `v2/conversation_engine.py` | `766bee296379f0faadbede55106bcee0123e9563c965d0e28f8806cedea06135` | 114499 |
| 7 | `v2/enneagram_wisdom.py` | `95c018092eae44f319bead262c7d815c477df85ede4f7574e2b08aeff17ce34d` | 40181 |
| 8 | `v2/parent_type_inference.py` | `b05632d01c48f52a5bed36b07b094ac770cada81f51951d78b7bea61e4e66cf3` | 8760 |
| 9 | `v3/V3_UNDERLIES_V2_ARTICULATION.md` | `5a0f11276a830b959df72653016ca77848dbd81de4adb9fa641bd4244c4f4ced` | 11091 |
| 10 | `v3/core/config_loader.py` | `5f953d9661f61081187898c3ad06b4567bc4fa99d3d7cd856d30cdd961f78577` | 2646 |
| 11 | `v3/core/derived.py` | `e479fc3eba21734752c372742fb2ee247cbdde6a73ac42545dc30b5039301360` | 15671 |
| 12 | `v3/core/generation_integrity.py` | `5265aac2fda4d6e6ac62927353518045f215d7d1916930e19e980b6d77eff214` | 4493 |
| 13 | `v3/core/invariants.py` | `81298f3fc51b46cda8d72d0db914b672b17b9a35e13004fe59a9b0e29dada5e3` | 14846 |
| 14 | `v3/core/state.py` | `19e968d45e9d81eb7629f1c237dbc55119fec8fc7db0b29e2b39b2476d12ada2` | 26310 |
| 15 | `v3/core/year_record.py` | `4bbd7518a6ec8bc8dd22758a2f9e876882253dfd59021a998a6d541b23e5cfc2` | 2537 |
| 16 | `v3/engine/active_magnets.py` | `68a7b75aa4bb98f7251f72a05747425edb40d24edbe06611ce998e7b6c26a391` | 3689 |
| 17 | `v3/engine/effects/delta_templates.py` | `7d99ddf26fd45b52e5e3c10074066ba5e06d17cdaf1fabad06298af3770815f0` | 19066 |
| 18 | `v3/engine/effects/metabolization_effects.py` | `d4775271ca097e99e615cee19b381a478ad6d90a25051c5fce1b1e0e3c1adb1e` | 24610 |
| 19 | `v3/engine/event_engine.py` | `b57e7ef4df5dabd996dc7de19c1c2c273ad90ee89d73570df1fd85674dd98ded` | 8371 |
| 20 | `v3/engine/expectation_baseline.py` | `632e1e608bfc674a241e57bafa24e91834a2b8bdc3e4ed326dae6fca4e695d43` | 5048 |
| 21 | `v3/engine/expectation_events.py` | `307ae929a43935170a2f792b4a702a02ac54819a4fa897aa3fef4a099a96cb49` | 6436 |
| 22 | `v3/engine/llm_contract.py` | `f024debf7b8a637e91c546689a0bed31baff55d98f1378b06cb82ebb4c0fe9cf` | 39455 |
| 23 | `v3/engine/prompts.py` | `4702de20590579c3c4543dfa5139aa4a3ce6df47ed1aee2c92c800d5a3038d57` | 17502 |
| 24 | `v3/engine/run_llm_band.py` | `120e177462219e8ccd5d5e0d7fdb23de993639f5af8be6c40a06db36e0b37a38` | 18926 |
| 25 | `v3/engine/scoring.py` | `36833287c72ffa40d0ece1ebc66fb0d685a92fc71aab1d211be9b21bfd0a82cb` | 12955 |
| 26 | `v3/engine/step_runner.py` | `5a737c1704eaa6dc2c67f6c2db3118a6daa8a213b44d559bc37eadbc9c09d95a` | 1183 |
| 27 | `v3/engine/striving_objects.py` | `78c79a9312b05aa51220d09bb63c91cafd6bb204f2c398ac1876b1ef3144c1c3` | 10950 |
| 28 | `v3/engine/yearly_step.py` | `da3147c3da7ff2724a61dd26d595055668899c83beb541400f58633568b92acb` | 9190 |
| 29 | `v3/io/field_injection.py` | `d3750fdb61eb73471612cad5c7d7c530da9519c93469a17f4f70a9b2505df0aa` | 10141 |
| 30 | `v3/io/identity_to_backbone.py` | `cb29c9595ac495c3b69b693d4c58a278e9ef1f63a7a8917d8e407920fbd3bdda` | 33465 |
| 31 | `v3/io/parent_baseline_from_behavior.py` | `4e5be6448a5b76c413492ec2a83b62d9e9a2247ce131a094727d974a17cf750b` | 3732 |
| 32 | `v3/io/persona_sheet.py` | `4a0009533443baef2786fc498c7f8db3ead7d133d8ee7e97e6d7128d4322a00e` | 47740 |
| 33 | `v3/io/v5_bridge.py` | `31700b4031a62b0b5ff8257691e460ce47c983f86daaec72f1011bd6f2823baa` | 3791 |
| 34 | `v3/io/v5_field_bridge.py` | `444ed1e074439d006d341808386ca31e0616ac99ce11f5b99f9d101791ff9eea` | 2804 |
| 35 | `v3/psyche/channels.py` | `2d00bf6b8720879e610160e58455f983e1e63fbe8ceef1a93f46844de8a3f111` | 8787 |
| 36 | `v3/psyche/flow.py` | `6da4effde2b1ccb7c346f73b17632ceee3a7a8c37a63a10f096753d070ab1d3d` | 40775 |
| 37 | `v3/psyche/gating.py` | `4a82c7c91828b87bb61cd651c777159f04b5733e64158f8679a24efcec1ccfc6` | 8911 |
| 38 | `v3/psyche/insulation.py` | `c8dd5f96111d3b247ddcf27b876d09c05460b06d7961193bff039e39e5967d28` | 5886 |
| 39 | `v3/psyche/vitality.py` | `56fed88e37299862774b2401c9a7e43363de6d6bb47a78f8f4744dcc6f91e912` | 6506 |
| 40 | `v3/render/phenomenology.py` | `f2f18c1d9ba705212846af41b33cb1dfd2ad986dae4b686873687c2e6d1a653d` | 7320 |
| 41 | `v3/systems/alienation.py` | `2209d8171a14f18c252e847e2d0beb113d574e1378c49d2fb7e7f43513106207` | 1490 |
| 42 | `v3/systems/autonomy_safety.py` | `fdb6ae0d78bbb93041217e7cd98f16526c97d924393c9f6fd51aa56a128b0e56` | 4496 |
| 43 | `v3/systems/boundary.py` | `e8c2495f5bd0699f5737a9e137dd327ec3d8c6953af262460ab03998f249a9c4` | 3020 |
| 44 | `v3/systems/buffers.py` | `9c9ed09001dad364ab4011ee29e8ea2df3c332745db736b1a6e1dbe56e332b35` | 2789 |
| 45 | `v3/systems/capacity.py` | `cae31ffd4006601aa860fbb011d1a23697a07a8cc1f0dc8e2897d5f2ed1531c3` | 1797 |
| 46 | `v3/systems/coherence.py` | `1bf8c1bee7a4197e3fb1eea34c89aed115edd3602c92c91888ada6790f575c4a` | 1011 |
| 47 | `v3/systems/cracks.py` | `b11a87e87be216d78c84f76ff645e26a39bb40512475558c95a279c78796bec3` | 2598 |
| 48 | `v3/systems/domains.py` | `24e5215763a11e439075ea7a0f4ac32ae425856a9fd4624744d4a2a744758280` | 2079 |
| 49 | `v3/systems/frameworks.py` | `0d59fc6e177009da92e39eb61ea729eace97f50392baa93999cb6513f81dd2cb` | 4559 |
| 50 | `v3/systems/health_drift.py` | `ba4608b7b9ab5dc758085ea90ed6eef64b4e40cc20790508e6623e51dc13995b` | 7961 |
| 51 | `v3/systems/infrastructure.py` | `a062192707bb6697c6d38a1ef3a72ca0ac6daedb759a38fd2fcb2cf4e219c235` | 1445 |
| 52 | `v3/systems/practices.py` | `b984397e5e8c24b68d94a6ef06e7cdd7bb07513db45a5480b48f154ece79720d` | 1301 |
| 53 | `v3/systems/relational_field.py` | `75cfd5f27528ee00306de353b730d50ab3fc028970c11afcf84edea7eea7b8cd` | 3059 |
| 54 | `v3/systems/reproduction.py` | `6f3a815d7ef6c5e7fd6003c4b4fd1b3bf1b2dc90cedcdcd332088737ee701916` | 2226 |
| 55 | `v3/systems/stability_inertia.py` | `5a11c8b07eafe2b8f1d7e9864c9cb066a5c45f19c2c45a8d4223b3a64c394c78` | 3521 |
| 56 | `v3/systems/topology.py` | `4e3b9b64399dfcfad67a431729d9443767d5e074080ef6b51bc1c8df48711560` | 3792 |
| 57 | `v3/tests/test_architecture_invariants.py` | `bb2baec1c57de169a2e1e05533b9721b4b05191403ff4993d61df17ac29d05fa` | 5686 |
| 58 | `v3/tools/distill_memory.py` | `6bece5ef66029581b27fd9d813e32d7d9239d2cde2c243a3df220d58c47d7cc2` | 18685 |
| 59 | `v3/v3_yearly_step_order.yaml` | `90496a2cc852ca00ef99c8bd4fcb2b41c9aa43c4aaa9108d3ac8cce0ebe22ffc` | 16520 |

## 6. S50 selected identity

**31/31 selected files verified.** The full per-file path/SHA-256/byte list is attached as `s50_selected_files` in `02_CORRECTED_SOURCE_GRADED_40X12.json`; no selected identity is inferred from the archive name.

## 7. Limits

- `TO_BUILD` means no adapter is imported by C9/C12/V2 today. `RULE_HELD` means the optional archive view cannot become causal without owner action.
- No behavioral sourcefree test was run for the proposed adapters. `05_VALIDATE_R2.py` validates counts, IDs, marks, relations, symbol records, source hashes and the sealed artifact references.
- Engineering acceptance is not self-issued. A distinct independent hostile review must inspect this plan and the machine JSON; science and authority remain HOLD.
