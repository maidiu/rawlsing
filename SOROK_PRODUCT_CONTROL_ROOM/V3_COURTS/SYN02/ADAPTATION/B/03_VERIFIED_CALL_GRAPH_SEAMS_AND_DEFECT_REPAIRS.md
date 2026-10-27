# SYN02-B — verified call graph, seams and defect repairs

**Status:** `HISTORICAL_SOURCE_AUDITED_CALL_GRAPH__CURRENT_INTEGRATION_UNTRACED__NO_IMPLEMENTATION__NO_NATIVE_GRANT`.
**Scope:** actual historical source paths, callers/callees, state mutations and consumers for the 40 families, plus the source-level repairs required before any Neo-V3 reuse. This is a design/seam document, not a current C9/C12 execution report.
**Source identity:** 59 directly hashed source files in `ADAPTATION/B/SOURCE_PLANE_IDENTITIES.json`; 31/31 S50 selected identities are exact per X01/RX01/RX03/RX04/RX05; 40/40 mechanism families have scoped independent reviews. The local staging ZIP `3f2c5ed9…` is not the TD-R05 archive `953c9149…`; file-level identity controls.

## 1. Historical annual call graph

### 1.1 Annual spine

`v3/engine/yearly_step.py:12–99` `run_one_year` loads the configured steps, resets yearly integrity/micro trace, optionally inserts placeholder cracks/frameworks, executes each step in order, clamps after each, checks derived schedule declarations, and increments `year`/`age` after the steps. `v3/v3_yearly_step_order.yaml` has **19 core steps** but **20 configured steps**; the appended step is `active_magnets_update`.

Exact configured sequence:

```text
field_update
autonomy_safety_micro_drift
event_sampling
reproduction_constraints_update
capacity_update
health_drift_update
buffers_update
frameworks_update
domains_update
cracks_and_alienation_update
plasticity_and_metabolization_update
stability_inertia_dissipation
striving_update
practice_and_infrastructure_update
topology_and_boundary_update
attention_and_capture_update
strategy_and_signal_effects
style_trait_drift
render_layer
active_magnets_update
```

`render_layer` is the 19th core step and executes before `active_magnets_update` and before the year/age increment. After the loop, `run_pressure_flow_cycle(state)` runs (`yearly_step.py:68–70`). The server then may run `run_llm_band_year` after `run_one_year` at selected ages (`server/generation/simulation.py:541–549`); `v3/run_and_print.py:123–139` runs its final band after its year loop, not after each year. This distinction matters for any claim of annual “second half” behavior.

### 1.2 LLM band

```text
state_summary_from_backbone
 -> Pass 1 LLM proposal
 -> parse_candidate_packet_with_fallback
 -> score/select candidates
 -> delta_from_event / delta_from_magnet
 -> merge_deltas
 -> apply_deltas_to_state (all selected events/magnets at once)
 -> compute_all_derived
 -> build_render_packet
 -> Pass 2 LLM render_year
```

`run_llm_band_year` (`v3/engine/run_llm_band.py:146–431`) does not append selected events to `state.events_this_year`; it records their IDs in `yearly_integrity.llm_band.selected_event_ids`. The server `year_record["event_ledger"]` is the mechanical sampler list; LLM selections are in `llm_band_ledger`. The band mutates capacity/domains/wounds/practice and may create shards/ruptures before rendering.

`parse_candidate_packet_with_fallback` (`v3/engine/llm_contract.py:159–211`) fabricates a minimal `practice` event when both candidate lists are empty. `run_llm_band_year` also has a first-candidate fallback if selection returns nothing. These are not lawful no-event paths.

### 1.3 Pass 2 and post-render

`render_year` (`v3/render/phenomenology.py:55–156`) writes only `state.rendered_output`; direct `backbone_hash` is unchanged. With a render packet it may call Pass 2 twice (initial + corrective retry). The direct function is nonmutating, but a Pass-2 callback exception is caught inside `render_year`, which writes a no-scene fallback without an integrity marker; the surrounding band can still report `applied`. The band applies psychic deltas before this render, so the direct isolation does not make the whole band transactional.

The next year's `update_metabolization_and_plasticity_step` reads the previous `rendered_output` through `_analyze_narrative_for_support_quality`, writes `narration_support`, and applies cluster deltas to `psychological_capacity` for raw/working processes (`v3/engine/effects/metabolization_effects.py:541–599`). This is a direct source-level narrator-text→psyche edge; it requires an active process and is not the immediate `render_year` call. `NarrationSupport.availability` comes from process `narrators` (never populated by generated processes), while accuracy/warmth/coercion come from prose words.

### 1.4 Pressure flow

`run_pressure_flow_cycle` (`v3/psyche/flow.py:753+`) builds a charge ledger, computes channel conductance, simulates domain routes transactionally (`_simulate_domain_routes_transactionally`, `:547–574`), and commits a route snapshot (`_commit_route_state`, `:570+`). It preserves useful trace/provenance and a transaction boundary for the route object, but the old selector is one winner per domain; grooves affect conductance, not channel choice. RX02’s correction remains binding: route-value changes can alter a later selection; that is not proof of a newly learned relation edge. Pre-route live-state writes can survive exceptions; the transaction is route-object-only, not a whole-actor rollback.

### 1.5 Derived and readiness

`compute_all_derived` (`v3/core/derived.py:322–359`) writes `state.metabolic_style` and `state.registers` while computing derived values. `assert_no_derived_fields_in_backbone` (`v3/core/invariants.py:346–350`) checks only six names and misses those two. `_compute_derived_after_step` (`v3/engine/yearly_step.py:173–191`) recomputes all derived values for any scheduled field; the equality check is real, but it does not prevent hidden writes or stale unscheduled fields.

`server/generation/store.py:183–242` validates a stored persona for live use with name/country checks and returns `clean_ready`; `server/session_state.py:35–57` treats `degraded_ready` as ready. `server/generation/simulation.py:807–844` blocks fresh store writes when generation readiness is blocked, but the stored-persona live-use path is weaker. A clean fixture or stored persona is not a native person.

## 2. Current-currentness boundary

| Layer | Verified status | Consequence |
|---|---|---|
| Historical V3 source | `HISTORICAL_SOURCE_AUDITED / HISTORICAL_RUN` at selected direct-file and reviewed-test grain | Reusable evidence, not current integration. |
| Current S39–S52 | Separate worker return modules, not one assembled native source tree in this checkout; S48 exact `9fe0d066e4bf61ab6819a1f56e42d6d07956c2f7`; S49 natural B source empty; S52 withheld | `CURRENT_INTEGRATION_UNTRACED`; no current C9/C12 person. |
| S48 | One current-source event, one product call, cache/replay, source-owner hold; no 3–5 batch | Reuse transport, not N11. |
| CAN008 R2 | Generic person×event coupling adopted; concrete Rule A not issued | No event semantics issued here. |
| CAN011 | `V3MS_MEDIATOR/TENSION/PRACTICE`, valid-empty, owner-governed transitions; no concrete Rule T | No acquisition/transition rule issued here. |
| ADP016/017 | Memory/access distinctions; no native admission | No autobiographical memory write from prose. |
| Pyat/C9/C12 | Native source/actor/permission held | No production or native person grant. |

The current source is not imported by the historical `BackboneState`; the old code is a reservoir, not a live C9/C12. Current C9/C12 effective imports and assembled runtime remain `CURRENT_UNKNOWN` for this commission. The S48/S49/S52 evidence is documentary/static from RC and prior reviews; no current runtime was executed.

## 3. Seam contracts: old → new

| Old seam | Actual source role | New seam contract | First consumer | Owner |
|---|---|---|---|---|
| `BackboneState` / `json_codec` | Large persisted actor envelope; conflates durable, derived, surface and diagnostics | `ActorSnapshotV1` + separate `CanonicalEventV1` ledger + `SurfaceRecord`/`DiagnosticRecord`; no conflation | ActorHistoryReader / C9 | V3/C9/C12 schema |
| `run_one_year` / `v3_yearly_step_order.yaml` | 20-step annual mutation | `run_event_sequence` per realized event + `advance_interval` for slow activity; dependency-order assertions retained | C9/C12 event loop | C6/C8/C9 |
| `run_llm_band_year` | Pass1 proposal, premerge, apply, Pass2 | `propose_batch` → source-owned realization → per-event CAN008/011 or NO_CHANGE → interval; no premerge | Event realization / CAN008 | C8/C9/CAN |
| `sample_events` / M33 | Mechanical event/delta generator | `WorldEventSource` / `realize_world_event` with participants, access, material facts, clock and source | Canonical ledger / C9 | ADP019/C8/world |
| `parse_candidate_packet_with_fallback` / M34 | Fabricated practice fallback | `NoEventRecord`/`HELD`; no fabricated event | Event admission | C8/C9 |
| `select_candidates` / M28 | Soft score, no hard admissibility, unseeded surprise | `admit_event` hard gate + named RNG/ADP020 + explicit no-event/no-change | Event ledger | C8/ADP020 |
| `apply_deltas_to_state` | Merged arbitrary psych deltas | Per-event actor-relative impression/transition; event 2 reads state after event 1 | CAN008/CAN011 | CAN/C9 |
| `render_year` | Immediate surface only | `render_surface` one-way; `SurfaceRecord` cannot enter actor memory/state | V2/ADP017 | V2/ADP016/017 |
| `persona_sheet` / V2 | Read-mostly narrative surface; annotation leak | `ActorVisibleSurface` with access filtering; annotation never memory/previous scene | V2 | ADP016/017/V2 |
| `compute_all_derived` | Computes but writes registers/metabolic_style | `DerivedViewRegistry` pure views; recompute on load; no actor writes | all views | V3/C9 |
| `update_metabolization_and_plasticity_step` | Rendered prose becomes narration support; raw processes accumulate indefinitely | `MetabolizationProcessRecord` with actual support refs and CAN012 transitions; no prose causality | CAN012/C9 | CAN012/ADP020/021 |
| `maybe_inject_rupture_at_band_age` | Age/global RNG rupture/wound | `AdmittedDisruption` from exact source event; no age ritual | CAN012 | CAN012/ADP019 |
| `v5_bridge` / field injection | Inert carrier plus integrity-blind consumer merge | `SourceEnvelope` + fail-closed `FieldInjectionDecision` | world/C9 | world/ADP019 |
| `store` readiness | Name/country/usable flag; `degraded_ready` accepted | `ReadinessVector` multi-gate; no fixture/persona proof | store/C9 | V3/C9/native owner |

## 4. Defect repair register

Each repair is a design action for a new implementation branch; no old source file is edited in this commission.

| ID | Defect and exact source | Required repair | Owner | Falsifier |
|---|---|---|---|---|
| D01 | M06 phantom alienation: `systems/alienation.py` and `delta_templates.py` write `structural/affective/institutional`; `clamp_all` resets scalar from four-field vector | Replace with `EstrangementRecord` or pure `DerivedAlienationView`; no dual truth; retain only source-qualified dimensions | CAN011/C9 | Same event changes no real estrangement record; phantom fields never persist. |
| D02 | M04 duplicate hostage: `_derive_hostage_index` (`psyche/gating.py`) vs `compute_hostage_index` (`core/derived.py`) | One canonical `compute_support_load`; private gates consume the same view | C9/world | Two authority outputs differ on same state. |
| D03 | M07 `or 50/80` and zero-as-missing in `gating.py:148–188`; stale `expressed_aim` | Explicit `UNKNOWN`/`ABSENT`; recompute or hold; never coerce zero/midpoint | ADP017/C9 | Missing field is not treated as 50/80 or stale value. |
| D04 | M05 `expressed_aim` can remain stale under zero load; `gating.py:185–188` | Expression is a derived/read-only access view; recompute from current access and rule | CAN011/ADP017 | Zero load cannot preserve old expression. |
| D05 | M30 optional country/identity fallback in persona path | Explicit unknown identity; no fabricated country/person | ADP017/V2 | Unknown identity remains unknown and does not become a persona fact. |
| D06 | M15/M36 absent parent→50→hopeful; safe-home child model | `UNKNOWN`/`ABSENT`; require actual caregiver history or hold | CAN010/CAN011 | Missing parent never becomes hopeful/safe. |
| D07 | M17 one-valence Gift/Disruption labels | `ImpressionRecord` with mixed components/objective source/access; no label authority | CAN008/CAN011 | Same event can produce mixed/ambiguous/no durable change. |
| D08 | M21 one-winner `_pick_channel`; no multi-stream recruitment | Multi-stream `RouteTrace` or CAN008-R2-style joint evaluation; preserve routing trace | CAN008/C9 | Two simultaneous pressures retain distinct effects. |
| D09 | M21 pre-route live writes vs route-only transaction (`flow.py`) | Whole-actor transaction boundary or explicit committed-prefix policy | C6/C9 | Failure leaves no unaudited actor write. |
| D10 | M19/M30 narrator prose→psyche (`metabolization_effects.py:541–599`) | One-way surface; support only from actual narrator/support/practice refs; SCI05/ADP owner | CAN012/ADP016/017/SCI05 | Perturbing prose alone changes no actor state. |
| D11 | M26/M38 hidden derived writes (`derived.py:322–334`) and fixed-name invariant | Pure `DerivedViewRegistry`; include all cached names or stop caching; recompute on load | V3/C9 | `compute_view` leaves actor snapshot hash unchanged. |
| D12 | M09 future/incorrect crack origin and demographic seeds | Episode-linked `TensionRecord` with effective/source refs; no future timestamps | CAN011 | Origin cannot postdate formation or be fabricated from demographics. |
| D13 | M16/M39 random strivings and age rupture (`striving_objects.py`, `metabolization_effects.py:273–332`) | Named ADP020 streams only if a rule permits; otherwise no spawn/injection; source event parent | CAN010/012/ADP020 | Same state/source/replay produces same lawful outcome; no age-alone rupture. |
| D14 | M19 status/IRR/narrators/meanings never update | CAN012 status/IRR/support transition; no universal ladder; explicit NO_CHANGE | CAN012/C9 | Process status has a producer, or valid-empty persistence is explicit. |
| D15 | M27/M28 selected events premerged/outside `events_this_year` | Canonical event ledger; per-event apply; no merge before sequence | C8/C9 | Selected event appears in ledger; reversed events differ. |
| D16 | M34 forced fallback/practice fabrication | `NoEventRecord`/`HELD`; no fabricated event | C8/C9 | Empty valid packet produces no practice delta. |
| D17 | M29/M28 Pass2 failure no rollback; `applied` status | Transactional event/render split; failure status; rollback or accepted-prefix receipt | C6/C8/C9 | Callback failure cannot leave silent applied psychic state. |
| D18 | M20 `who` drop and unconditional mother/father seeds | Exact `ActorEntityRef`/`RelationRecord`; no fabricated parent; preserve entity IDs | ADP019/C9/world | Removing parent record removes parent relation; no label-only parent. |
| D19 | M31 Enneagram type at 7, random matcher, parent-type effects | Remove causal matcher; optional noncausal descriptive view only | V2/owner | No type at birth or parent-type causal effect; archive old type. |
| D20 | M32 blocked numeric injection merge (`field.py`) | Fail-closed `FieldInjectionDecision`; blocked source cannot apply numerics | world/C9 | Blocked bridge + existing values cannot be accepted as fresh world facts. |
| D21 | M09/M35 placeholder cracks/frameworks | Remove placeholder objects; valid-empty/diagnostics only | CAN011/C9 | No placeholder count can satisfy a causal invariant. |
| D22 | M40 stored readiness bypass; `degraded_ready` accepted | `ReadinessVector` with generation/rule/source/actor/memory/consumer gates; block stored legacy unless all required gates positive | C9/native | Blocked/degraded stored persona cannot become `clean_ready`. |
| D23 | M37 annotation/marker leak into backstory/previous scene | `IntervalAnnotation` separate; exclude from memory and previous-scene selection; tag all structural paths | ADP016/V2 | No annotation/marker appears in memory or previous scene. |
| D24 | M25 19-core/20-configured confusion and year-as-causal-unit | Keep 20-step order as slow scaffold; separate event/interval clocks; test exact executed list | C6/C9 | A year tick cannot stand in for an event; core/configured counts explicit. |
| D25 | S48 one-call transport misdescribed as N11 | Keep as transport/refusal; create 3–5 batch/interval/retrospective seam under N11/C9/ADP/SCI05 | S48/C9/ADP | One event per call is not 3–5 sequential recursion. |

## 5. Source-verified positive/fault evidence used in this design

The following are reviewed-source facts, not new executions by SYN02-B:

- **M14:** two consecutive-year topology transition and one-step boundary reversal are real; no learned relation edge was found. RX03 reproduced 71 focused tests; RX04 reproduced 77 scheduler/event tests; RX05 reproduced 28 material/actor tests.
- **M19:** rendered prose requires an active raw/working process to affect next-year psychological capacity; RX03’s targeted probe showed warm aperture 55 vs neutral 54 and a severed reader removes the difference. Direct `render_year` remains nonmutating.
- **M25/M27/M28/M29:** X04/RX04 confirmed 19 core/20 configured, selected events absent from `events_this_year`, premerged application, fallback fabrication, derived writes, and no Pass-2 rollback after mutation.
- **M31/M35/M40:** RX05 confirmed type-at-7/parent-type effects, placeholder inclusion without demonstrated class change, and stored-persona live-use acceptance of blocked/degraded/generation verdicts.
- **M39:** X04/RX04 confirmed age-band global RNG, no event ledger, and direct wound mutation; RX03 additionally confirmed malheur→process micro and event-path/age-path wound disagreement.
- **S48:** RX04 reproduced 12 exact-cut source-owner/replay/hold tests; S48 is one current-source event per call with empty natural B candidate source.

No *current* C9/C12 integration or native person is established by any of these facts.

## 6. Current source and owner boundary

The current S39–S52 modules are separate worker-return source paths, not a single native imported tree. S48 is exact one-call transport; S49 natural B source is empty; S52 is withheld; current C9/C12 has no demonstrated same-person CAN011 earned-state → later CAN008 semantic read. The historical V3 source does not supply that integration.

`CAN008 R2` generic coupling, `CAN011` middle-state kinds, `ADP016/017` memory/access and `SDTF` objective classes are documentary adopted interfaces, not concrete rules for this actor or this mechanism. The future new call graph must name exact rule/version/hash, source/actor access, clock and first consumer for every edge.

## 7. Tests and claim ceiling

- **Executed by SYN02-B:** none required for design; no new sourcefree test was necessary for a disputed source claim. Existing reviewed source/test evidence is cited at author/reviewer SHAs.
- **NOT_RUN:** current C9/C12 native person, S39–S52 assembled runtime, new migration/schema tests, new event/interval scheduler, new actor-state formation tests, live provider, Pyat source/actor, A0–A5.
- **Claim ceiling:** historical source/adaptation design only. Do not call a sourcefree historical test a native person, a proposed function an implementation, or a migration proposal a production migration.
