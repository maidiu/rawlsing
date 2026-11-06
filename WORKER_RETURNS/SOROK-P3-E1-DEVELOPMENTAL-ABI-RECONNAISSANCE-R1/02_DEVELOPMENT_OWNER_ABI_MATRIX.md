# DevelopmentOwner ABI matrix — exact source and target fields

**Scope:** compare the received #704 ABI with B1, B2, B3A, BP2P4J, HQ300, M01, P2Owner and the local V3 copy. No native rule is inferred from a field match. `TEST_ONLY` labels are preserved.

## 1. Received ABI (protected `c852d751`)

`WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1/developmental_recursion/contracts.py`:

```text
StateIdentity(root: str, actor: str, branch: str, clock: int, state_hash: str)

EventProposal(
  event_id: str,
  event_time: int,
  operation: str,
  source_refs: tuple[str, ...],
  participants: tuple[str, ...],
  circumstances: Mapping[str, Any],
  interval: Mapping[str, Any] | None,
)

RealizedEvent(
  operation_id: str,
  proposal_hash: str,
  before: StateIdentity,
  after: StateIdentity,
  status: str,                         # REALIZED | IMMEDIATE_ONLY | NO_CHANGE | HELD | REFUSED | OMITTED
  objective: Mapping[str, Any],
  accessible: Mapping[str, Any],
  consequences: Mapping[str, Any],
  readset: tuple[str, ...],
  receipt_ref: str,
)

DevelopmentOwner(
  snapshot() -> StateIdentity,
  validate_proposal(proposal) -> None,
  realize(operation_id, proposal, expected) -> RealizedEvent,
)
```

`BatchEngine.run_batch(batch_id, proposals)` requires 3–5 proposals, rejects duplicate event IDs, validates all proposals before claiming the batch, binds the journal to root/actor/branch, reserves an operation before `owner.realize`, and requires the owner to resolve an operation ID idempotently or raise an ambiguous HOLD. `engine.history(batch_id)` validates the stored chain against the current owner identity. `RecursionCycle` calls the provider only between batches and stores retrospective impressions outside canonical owner state.

The engine does **not** define a psychological state schema, rule registry, target record, memory record or later psychological consumer. Those are owner responsibilities.

## 2. P2Owner — the current production-shaped owner

`WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1/developmental_recursion/p2_owner.py`:

| ABI member | Current implementation | Exact source fields | Missing for P3 |
|---|---|---|---|
| `snapshot()` line 63 | `StateIdentity(fanin.root_hash, actor, session.branch_id, session.clock(), digest({"world","events","intervals","encounters"}))` | `fanin.root_hash`; `root["actor_ids"][0]`; `session.branch_id`; `session.clock()`; `world().actor_state`; `read_events()`; `read_interval_states()`; `read_encounters()` | No mediator/tension/practice/memory/claim rows in the hash; no psychological state table |
| `validate_proposal()` line 79 | Requires `operation == "ADMIT_EVENT"`, `source_refs == (self.source_ref,)`, `participants == tuple(root["actor_ids"])`, circumstances keys `{history_refs, language_context}`, future event time, interval `{mode, span}` | `source_ref = P2_INPUT:digest({case, source})`; `history_refs` resolved against native E1 IDs/hashes; S43 `milieu_id`; `ACTUAL`/`SCHEDULED_ONLY` | No CAN-008 rule ID, target authority, state predicate, psychological source/readset |
| `realize()` line 140 / `_realize()` line 194 | `BEGIN IMMEDIATE` on `operations`; stale/root/branch/clock hash check; optional interval; `s.admit_event`; `s.read_event`; `s.read_s43_event`; `s.read_c9_conditioning`; `RealizedEvent` | `P2_EVENT:e1_event_hash`; `material_state_changed`; `interval`; `immediate_response`; `durable_psychological_transition = "MISSING_RULE"`; `independent_B = "CONTROLLED_SOURCEFREE_PARTICIPANT_ONLY"` | No psychological effect commit; no source-qualified target receipt; no later psychological read |
| `actor_experience()` line 147 | Actor-specific perception projection | E1/action hash; actor alias; perception receipts; `project_event` with `perceived_by_user` removed | No ADP-017 claim permission or M6 envelope |
| `snapshot()` state hash | `digest(material)` | `world` (vars), `events`, `intervals`, `encounters` | A psychological change would not change `state_hash`; the engine would not detect it |
| Operation recovery | `operations(id, proposal, before_state, result)`; resolved result or `P2_AMBIGUOUS_PRIOR_OPERATION_HOLD` | `digest(proposal.document())`; `canonical(expected.document())` | This is the correct custody pattern to reuse in the extension |

P2 actor material fields observed in the S45–S47 closure include `cash`, `free_hours`, `completed_units`, `material_remaining`, `tools_remaining`, `projects`, `skill`/work fields. These are material/economy fields; they are not CAN-011 or ADP-016 state.

## 3. B1 — the executed narrow adapter

`WORKER_RETURNS/SOROK-V2-HQ324-B1-COUPLED-DEVELOPMENT-R1/bfirst.py` at `c0f4588c158b40c8903b4aae2f292eae5238b8a0`, blob `94ffc52847e4c8ae760212d1bc8543594ba793fa`.

| B1 object | Exact fields | Engine mapping | Adapter operation |
|---|---|---|---|
| `Event` line 101 | `event_id, actor_id, time, world_ref, objective_occurrence, project, relation_refs, power_ref, offers[(counterpart, words, plan)], interrupted, admission_grade, provenance, hash` | `EventProposal.event_id`; `event_time`; `circumstances["b1"]`; `participants` | Rebuilds `Event` from proposal; fixes `actor_id='child'`, `admission_grade='ADMITTED_SYNTHETIC_FIXTURE_ONLY'` |
| `HistoryEpisode` line 71 | `episode_id, actor_id, counterpart, project, time, activity, outcome, actor_access, parent_refs, provenance, hash` | No direct engine field | Remains inside B1 state; adapter verifies the immutable prehistory |
| `Participant` line 85 | `actor_id, project, history`, `offer()` line 90 | No direct engine field | B1's authored counterpart offer; adapter does not claim independent B |
| `propose()` line 161 | `schema, actor_id, event_ref, time, response_rule_ref, prior_response_history_hash, before_state_hash, before_target_hash, uptake, recruited, practical_activity, target_proposals, actor_surface, status, hash` | `RealizedEvent.objective` / `accessible` / `consequences` | Kept intact; `actor_surface` is the accessible projection |
| `TestOnlyCAN011Owner.validate()` line 239 | Permission binding; target identity/operation/kind/time/parents/payload/rule checks | No engine field | Called inside B1 `Store.commit()`; not bypassed |
| `Store` line 278 | `checkpoint(id,body)`, `occurrence(hash,body)`, `joint_receipt(hash,body)` | Owner's durable store | Adapter adds `b1_owner_meta`, `b1_source`, `b1_operations` in the same SQLite file |
| `Store.admit_fixture()` line 298 | `INSERT OR IGNORE occurrence`; admission grade check | No engine field | Called before response commit; occurrence survives response rollback |
| `Store.commit()` line 304 | `BEGIN IMMEDIATE`; occurrence check; stale response; exact `propose()` rerun; same-time order; owner decisions; middle/transitions/responses; checkpoint; joint receipt; rollback | `RealizedEvent` construction | Adapter calls it and maps `COMMITTED`/`TRANSACTION_ABORTED_ROLLBACK` to engine status/refusal |
| `mode_for()` line 152 / `propose()` match block | Reads `state["history"]`; later reads `state["middle"]` ACTIVE records by `target_refs == [project, counterpart]` | Later first consumer | The probe proves the later event reads the stored mediator |

Adapter additions (only these):
- `StateIdentity(root, 'child', branch, clock, digest(B1 state))`; clock is `max(history.time, middle.effective_from, responses.time)`.
- Project-level `source_ref = "B1_FIXTURE:" + digest({initial_state, RESPONSE_RULE.hash, UPDATE_RULE.hash, REGISTRY.hash})`.
- `b1_owner_meta(root, branch, actor, source_ref)` and `b1_source(body)` for foreign-root/source-severance checks.
- `b1_operations(id, proposal_hash, before_state, status, result, refusal)` with `RESERVED -> COMPLETE|REFUSED`; a RESERVED row raises `B1_AMBIGUOUS_PRIOR_OPERATION_HOLD`.
- `RealizedEvent.status`: `REALIZED` if B1 has a target proposal or practical action; `NO_CHANGE` if the response is valid-empty; `IMMEDIATE_ONLY` for a journal-only control.
- `consequences`: `durable_psychological_transition = "TEST_ONLY_B1_V3MS_MEDIATOR"`, `native_science = "NOT_ISSUED"`, `middle_state_ids`, `middle_state_record_hashes`, `recruited`, `practical_activity`, `target_proposal_count`, `source_rule_ids`.

The adapter's default initial state is B1's default `initialize(prehistory())`. A non-default prehistory must be supplied again on reopen; otherwise the stored source reference and the reconstructed initial state disagree and the adapter refuses.

Exact incompatibilities that prevent B1 from being used directly:
- B1 has no `StateIdentity`, root, branch or state hash.
- B1 has no operation ID; its exact replay is deterministic but not an owner receipt.
- B1's source is a synthetic prehistory and authored rule, not an original CAN/ADP issuance.
- B1's actor is `child`; its event grammar is `project`/`offers`/`interrupted`, not P2 `history_refs`/`language_context`/`interval`.
- B1's store is a checkpoint JSON, not the P2 S47 SQLite root.
- B1's mediator is CAN-011-shaped but not the P2 actor's psychological state.

## 4. B3A — strong transaction, wrong boundary

`WORKER_RETURNS/SOROK-20261018-B3A-SCHEMA-READSET-REPAIR-R1/candidate/integration.py` at `16f15a125ba54cdf17f5d41be2d851bbcd2240d7`, blob `d3a324bb93c17fdaf12670dd153aeb138d9c426a`.

| B3A member | Exact fields/behavior | Engine mapping | Incompatibility |
|---|---|---|---|
| `Integration.run(data)` line 194 | `data` frame: `case_id, actor, event, actors, evidence, utterances, exposures, readset, capability, as_of, proposals, lineage, ledger, origin_event_id`; atomic staging and publication | No `EventProposal` mapping | Requires a frame translator; not a `DevelopmentOwner` |
| `Integration._run()` line 245 | `qualify`, `prepare`, `admit`, `projected_loss`, `scene_at`, `m2.eligible`, `response`, `target_owner.validate`, `b3_source`/`b3_transition`/`b3_response`/`b3_clock`/`b3_m2_sources`/`b3_preimage`/`b3_audit` | No engine fields | No operation ID, root/branch/state hash, or engine `RealizedEvent` |
| `Integration.middle()` line 176 | `SELECT body FROM b3_transition ORDER BY id` | Later reader | `response()` line 119 uses `active = [x for x in middle if lifecycle == ACTIVE and targets == [object_ref]]`; it is a frame function, not an owner read |
| `Integration.snapshot()` line 157 | All result-set rows | No exact `state_hash` | `_database_snapshot()` line 160 adds schema + `schema_version`/`user_version`/`application_id`; this is a logical DB readset, not `StateIdentity` |
| `target_owner.validate()` line 9 | `registry_id/version/snapshot_hash`, `before_target_hash`, `actor`, `kind='V3MS_PRACTICE'`, `rule`, `rule_hash`, `targets`, `payload={'procedure':'CHECK_LOCK','scope':'garage'}`, `effective_from`, `lifecycle='ACTIVE'`, `causal_parents`, `actor_memory_access='NOT_GRANTED'`, `grade='TEST_ONLY_RESEARCH_RULE_UNCALIBRATED'` | CAN-011-shaped target | Authored rule `B3_WITNESSED_REPEATED_SECURITY_PRACTICE@1`; requires two `PRACTICE_COMPLETED` with `LOCK_CHECK_CONFIRMED` and a new practice after the event |
| `response()` line 119 | `routes`, `material_actor_activity`, `independent_offer_refs`, `admissible_routes`, `practical_actions`, `selected_affect=None`, `selected_belief=None`, `current_consequence`, `actor_safe` | Later consumer | No `DevelopmentOwner` return; action `CHECK_LOCK` is a sourcefree option, not a native E2 |

B3A is the best existing *transaction shell* for sourcefree state effects, and its independent I2 accepted the schema/readset repair. It is not the smallest P3 adapter because it requires the B2/M2 closure and a frame translation.

## 5. HQ300, M01 and BP2P4J

| Source | State/clock | Transaction | Later reader | Why not `DevelopmentOwner` |
|---|---|---|---|---|
| HQ300 `run_positive_chain()` `positive_chain.py:89` | In-memory `ChainEventLedger` entries; `AdmittedEvent` has `event_id, event_hash, issuer_authority_id/version, event_kind, effective_causal_time, actor_scope, world_ref, world_as_of, admission_state, public_features`; `OwnerPrestate`; `GeneratedMemoryState` | Typed checks then ledger append; H9 reverse-chronology guard | `read_effects("CAN008_CURRENT_RESPONSE_EFFECT")`; prior `BUFFER` -> `DEFLECT`, else `AMPLIFY` | No durable store, no root/branch/clock, no operation receipt; production registry empty |
| M01 `Cell.prepare()` `cell.py:66`, `read_owner()` line 90, `later()` line 127 | In-memory `FixtureOwnerState` (`memories`, `memory_transitions`, `claims`, `stances`, `state_sets`) + `ChainEventLedger`; source hash binds implementation | Checkpoint/restore; all streams validated before journal commit | Memory `BUFFER`/`DEFLECT`/`AMPLIFY`; epistemic `REROUTE`/`BLOCK` | No durable owner, no root/branch/operation ID; audit receipt is not an actor render envelope; `MECHANISM_IDENTIFICATION_HOLD` |
| BP2P4J `JoinedProduct` `product.py:47` | `C12Store` SQLite + `bp2_join.json`; `joined_source()` line 121; `verify_join()` line 150 | BP2 C8/C9/E2 and BP4 C10/C12; practice materialized into projects/tools | BP4 A0/A2; offscreen repair requires tool/material | Separate C8/C9/C10/C12 product and world; no #704 root/branch; huge vendored closure |

## 6. Original V3 local copy

The exact protected archive is **not present**. The P3 ADP-016 authority records expected archive SHA-256 `953c9149bd03877206e3cb440d1f4db35dea6473af30b97fd23b7e76c6fc0086`; the local untracked `Rawlsing_code_bundle_staging.zip` is `3f2c5ed925273153a4f300f75e54524729f0b4fef9974957be1f3cd887c91289`. The local `v3/` directory is therefore `LOCAL_UNVERIFIED_ARCHIVE_COPY_NOT_EXACT_PROTECTED_BYTES`.

Observed local V3 fields (not requalified):

- `v3/core/state.py:501 BackboneState`: `year, age, field, calibration_regime, boundary_map, strata_salience, strata_stack, events_this_year, micro_trace_this_year, capacity, psychological_capacity, reproduction_constraints, domains, alienation, alienation_vector, wound_vector, cracks, buffers, frameworks, frameworks_dormant, collective_infrastructure, practice_stack, peak_routing, intensity_and_capture, style_traits, rendered_output, rupture_shards, metabolization_processes, initial_state_provenance, yearly_integrity, pressure_flow_history, pressure_flow_memory, surface_psyche_profile, analyst_pressure_account, generation_diagnostics, plasticity_window, narration_support, metabolic_style, expectation_baseline, striving_objects, gift_shards, disruption_shards, registers, child_model, active_magnets, v5_*, autonomy/safety, stability_threshold_inertia`.
- `v3/psyche/flow.py:753 run_pressure_flow_cycle`: assigns sublimation channels, computes baseline load, applies expression gating, builds a charge ledger, resolves vitality, simulates domain routes transactionally, appends history, updates memory and commits route state.
- `v3/engine/yearly_step.py:10 run_one_year`: executes a configured step order, increments `year`/`age`, applies awareness puncture counters and one post-year pressure-flow cycle.
- `v3/engine/step_runner.py:11 run_n_years`: loops years.

These are 0–100 numeric, yearly, fixed-module machinery. They are not the 3–5-event P3 state model and are not current scientific law. The `flow.py` transactional route commit is reusable as a *pattern*, not as a schema or coefficient source.

## 7. Exact first missing adapter

The production seam is:

```text
P2Owner.snapshot()                  -> add psychological rows to state_hash
P2Owner.validate_proposal()         -> optionally validate psychological rule/source metadata
P2Owner._realize()                  -> after s.admit_event/read_event/read_c9:
                                       commit psychological effect with durable receipt
P2Owner (new later reader)          -> next event/action path reads psychological row
```

Required target type, not yet present:

```text
PsychologicalRecord(
  record_id, root, branch, actor, kind,        # CAN011 MEDIATOR|TENSION|PRACTICE, ADP016 memory, ...
  lifecycle, target_refs, payload,
  source_rule_id, source_rule_version, source_rule_hash,
  causal_parent_refs, effective_from, effective_to,
  receipt_hash, prior_record_hash
)
```

Required owner operations:

```text
snapshot() -> StateIdentity with digest(material + psychological)
realize(operation_id, proposal, expected) ->
  if operation exists: return stored receipt or ambiguous HOLD
  if expected != snapshot: refuse stale
  validate proposal
  reserve operation
  admit P2 event/interval
  apply source-qualified psychological effect atomically or hold MISSING_RULE
  return RealizedEvent with psychological consequence receipt
```

The probe adapter implements exactly this pattern for B1, but with B1's state and rule. It is the compatibility witness; the P2 seam is the production task.

## 8. Test oracle for the future adapter

A future P2 psychological owner must preserve the probe's oracles:

1. Valid root/actor/source/clock produces a committed record and a changed `state_hash`.
2. Same 3–5 proposals replayed after cold reopen return the same history and do not duplicate the record.
3. A byte-identical later event produces a different computed action/eligibility only when the prior record exists.
4. A foreign root, wrong actor, stale clock, wrong source/rule hash, or missing rule is refused before durable mutation.
5. The production zero-positive guard still returns `DENY_ZERO_EFFECT`.
6. A dormant record remains stored without forced outward behavior.
7. Exact source severance breaks the later consumer; exact byte restoration restores the result.
8. No model/provider call between events; no prose impression becomes state.
