# SYN02-B — new/old schema migration and compatibility design

**Status:** `CANDIDATE_SCHEMA_MIGRATION_DESIGN__NO_PRODUCTION_IMPLEMENTATION__NO_NATIVE_AUTHORITY`.
**Purpose:** define a versioned, fail-closed migration path from historical V3 `BackboneState` storage into a Neo-V3 actor schema without laundering synthetic defaults, demographic presets, placeholders, narrator-derived state or arbitrary numeric psychology into scientific or native authority.
**Source:** original V3 source read-only at `<USER_HOME>/Desktop/Rawlsing/Rawlsing_code_bundle_staging`; selected-file hashes in `ADAPTATION/B/SOURCE_PLANE_IDENTITIES.json`; 40/40 reviewed at selected source grain. The staging ZIP is not the TD-R05 archive; file identities control.

## 1. Design goals and non-goals

**Goals**

1. Preserve the historical source as an inspectable, replayable evidence carrier.
2. Give each durable, derived, diagnostic and surface object a different schema and writer.
3. Make missing/unknown/absent explicit; never substitute `0`, `50`, `100`, `hopeful`, `neutral`, `medium` or `safe`.
4. Separate start-of-person creation from existing-person migration.
5. Make migration atomic, idempotent, auditable and reversible by checkpoint.
6. Keep old compatibility projections read-only and causally inert.
7. Record source/rule/owner/permission identity for every imported fact.
8. Permit a valid-empty actor state when no source-backed fact exists.
9. Prevent old synthetic atoms from entering the new causal actor by relabeling.
10. Leave current C9/C12 session formats and native rules untouched; this is a candidate actor-schema design, not an issued session migration.

**Non-goals**

- No production migration script, no source edit, no current C9/C12 session-format change.
- No scientific rule for formation, metabolization, acquisition, typology, care or memory.
- No claim that old numeric values are empirical measurements.
- No blanket archive-wide identity claim.
- No deletion of historical evidence; rejected/synthetic atoms are archived with provenance.
- No downgrade support or automatic fallback from the new schema to legacy causal state.

## 2. Candidate schema versions and layers

```text
LEGACY_SCHEMA = "legacy_v3_backbone@1"
NEO_ACTOR_SCHEMA = "neo_v3.actor@1"
NEO_EVENT_SCHEMA = "neo_v3.event@1"
NEO_MIGRATION_SCHEMA = "neo_v3.legacy_migration@1"
```

These are candidate names in this design, not current Sorok session-format constants. A future owner must choose the actual version naming and release gate.

### 2.1 `ActorSnapshotV1` (candidate)

```text
ActorSnapshotV1 {
  schema_version: "neo_v3.actor@1",
  actor_id: ActorId,
  lineage: LineageRef,
  created_at: EffectiveTime,
  source_cut: SourceCutRef,
  clock: ActorClock,
  phase: DevelopmentPhaseRef?,
  material: MaterialState,
  constraints: MaterialConstraintRecord[],
  needs: NeedRecord[],
  expectations: ExpectationRecord[],
  mediators: MediatorRecord[],
  tensions: TensionRecord[],
  practices: PracticeRecord[],
  relations: RelationRecord[],
  motives: MotiveTargetRecord[],
  ruptures: RuptureRecord[],
  processes: MetabolizationProcessRecord[],
  access: AccessEnvelope,
  memory_refs: MemoryRef[],
  provenance: Provenance,
  diagnostics: DiagnosticRecord[]
}
```

`ActorSnapshotV1` contains only actor-owned durable records. It does not contain a global graph, a second psyche, a derived index cache, a rendered scene, an analyst account or a readiness verdict.

### 2.2 Canonical event and receipt records (candidate)

```text
CanonicalEventV1 {
  event_id, event_type, effective_time, interval_ref?,
  source_owner_ref, source_event_ref?, parent_event_refs[],
  participant_refs[], access_refs[], material_refs[],
  provenance, integrity, status
}

EpisodeV1 {
  episode_id, actor_id, canonical_event_ref,
  access_ref, received_features[], excluded_features[],
  provenance, integrity
}

ImpressionV1 {
  impression_id, actor_id, episode_ref, scope_refs[],
  mixed_components[], intensity?, opacity?, rule_ref,
  provenance, status
}

TransitionReceiptV1 {
  transition_id, actor_id, target_record_ref,
  operation, prior_hash, after_hash, rule_ref,
  causal_parent_refs[], support_refs[], receipt_status
}
```

The event/episode/impression/receipt split preserves objective event, actor access, actor-relative impression, durable transition and replay. A rendered scene is not any of these.

### 2.3 Derived and surface records

```text
DerivedViewSpec { view_id, dependencies[], rule/version/hash, owner }
DerivedViewValue { view_id, actor_snapshot_hash, value, computed_at, provenance }

SurfaceRecord {
  surface_id, actor_id, consumer, schema_version,
  rendered_payload, source_refs[], created_at,
  causal_write_permission: false
}
```

`DerivedViewValue` is never written into `ActorSnapshotV1`. `SurfaceRecord` is one-way; it may be consumed by V2/ADP017 but cannot create memory, durable state or a new event.

## 3. Migration modes

| Mode | Use | Behavior |
|---|---|---|
| `FRESH_ACTOR` | A new person with no historical V3 state | Create only source-qualified initial facts; unknown/absent is explicit; valid-empty allowed. |
| `LEGACY_READ_ONLY` | Inspect/compare an old V3 snapshot | Parse, hash, classify and display; no causal import or writes to the new actor. |
| `LEGACY_IMPORT_EXPLICIT` | An owner explicitly imports selected historical facts | Map only classified, source-bearing facts; archive all synthetic/unverified residues; require a migration receipt. |
| `COMPAT_PROJECTION` | Old consumers/tests need an old-shaped view | Produce `LegacyV3Projection` read-only; mark `causally_inert=true`; no write-back. |
| `MIGRATION_REJECTED` | Unknown required fact, corrupt structure or failed integrity | Block the whole migration; no partial actor snapshot. |

The default is `LEGACY_READ_ONLY`, not silent automatic import. A migration needs an explicit caller/owner decision, an exact source cut and a migration report.

## 4. Field-level migration matrix

| Legacy field/group | M | New destination | Classification | Required treatment |
|---|---|---|---|---|
| `BackboneState` envelope; `year`, `age`, `events_this_year` | M01, M25 | `ActorSnapshotV1` envelope; `ActorClock`; `CanonicalEventV1` ledger | `ADAPT` | Preserve source cut and chronology; split event ledger, durable state and surface; age is chronology, not developmental law. |
| `capacity.*` | M02 | `MaterialState` + `MaterialFact` with source/time | `ADAPT` | Keep source-qualified material facts; archive class/urban defaults; no 50 defaults. |
| `psychological_capacity.*` | M03 | `RegulatoryState` / source-backed `MediatorRecord` | `ADAPT` | Keep only interpretable regulation/availability evidence; unknown otherwise. |
| `reproduction_constraints.*`; hostage indices | M04 | `MaterialConstraintRecord`; one `compute_support_load` | `ADAPT` | Keep concrete constraints; remove duplicate hostage authority; no 0/100 optimistic defaults. |
| `domains.*` | M05 | `AppraisalProjection` (derived/read-only) | `ADAPT` | Do not store as universal causal compartments; compute a projection only when a rule/consumer exists. |
| `alienation`; `alienation_vector.*` | M06 | `EstrangementRecord`; `DerivedAlienationView` | `ADAPT` | Archive phantom `structural/affective/institutional`; fix lost delta; no dual scalar/vector truth. |
| `wound_vector.*`; identity wound seeds | M08 | `SensitivityRecord` with scope/source | `ADAPT` | Keep only evidenced sensitivities; archive class/minority/religion/age seeds and 50 defaults. |
| `cracks[]`; placeholder cracks | M09, M35 | `TensionRecord`; `LegacyArtifact` for placeholders | `ADAPT/REMOVE` | Map only episode-linked contradictions; archive placeholders and demographic seeds; no min count. |
| `buffers[]`; buffer costs | M10 | `SupportRecord` with resource/support/cost refs | `ADAPT` | Keep support concept; source the cost and whose activity provides it. |
| `frameworks[]`; framework recipes | M11 | `MediatorRecord`; archive seeded recipes | `ADAPT` | Keep stable mediator/acute-chronic technique; archive age/class/religion recipes and age-derived tenure. |
| `collective_infrastructure.*` | M12 | `InstitutionRef` / `ParticipationRef` / world-condition refs | `ADAPT` | Do not copy collective reality into actor state; bind to exact world entities and access. |
| `practice_stack.*`; practice seeds | M13 | `PracticeRecord` | `ADAPT` | Map only actual activity/support; archive SES/age/religiosity seeds and label/route increments. |
| `peak_routing.*`; topology/boundary/coherence | M14 | `OrientationConfiguration`; optional `FunctionalConnectionRecord` (C court) | `ADAPT/REWORK` | Preserve hysteresis technique; archive global enum as ontology; no learned relation by scalar switch. |
| `expectation_baseline`; parent defaults | M15, M36 | `ExpectationRecord`; `UnknownExpectation` | `DEEP ADAPT/REMOVE` | Archive `50→hopeful`; keep scope/evidence/contradiction; unknown is not normal. |
| `striving_objects[]` | M16 | `MotiveTargetRecord` | `ADAPT` | Keep object identity/lifecycle; archive age/proxy spawn, random support, retirement and hopeful fill. |
| `gift_shards[]`, `disruption_shards[]` | M17 | `ImpressionRecord` with mixed components | `DEEP ADAPT` | Preserve witnessed event shell; no forced one-valence label; record objective source/access. |
| `rupture_shards[]` | M18 | `RuptureRecord` | `ADAPT` | Keep carrier; add exact parents/actor basis/rule; archive age-band, global RNG and direct wound mapping. |
| `metabolization_processes[]` | M19 | `MetabolizationProcessRecord` | `ADAPT` | Keep process identity and raw/working compatibility; create lifecycle/IRR/support/NO_CHANGE; no prose support. |
| `active_magnets[]`; `relational_field` | M20 | `RelationRecord`; `ActorEntityRef`; `MagnetView` | `ADAPT` | Keep relation/decay carrier; archive mother/father labels and lost `who`; no label-to-practice. |
| `pressure_flow_history/memory`; `surface_psyche_profile`; `analyst_pressure_account` | M21, M07, M30 | `RouteTrace`; `DerivedView`; `AnalystDiagnostic` | `DEEP ADAPT` | Preserve trace/transaction; analyst-only data never becomes actor knowledge; no second psyche. |
| `child_model` | M22 | `DevelopmentalOrientation` or `UnknownChildHistory` | `DEEP ADAPT` | Keep fallible layer; archive safe-home defaults/taboos; no infant adult doctrine. |
| `autonomy_drive/safety_drive`; conditions | M23 | `ConditionRecord` | `ADAPT` | Keep actual condition/gap history; archive universal 65/68 drives and time increments. |
| `stability_threshold_inertia` | M24 | `ResidueRecord` / hysteresis history | `ADAPT` | Keep persistence technique; no universal drain, neutral point or fixed decay. |
| `yearly_integrity`; `generation_diagnostics`; `initial_state_provenance` | M01, M25, M40 | `DiagnosticRecord`; `Provenance`; `ReadinessVector` | `ADAPT` | Diagnostics are not actor facts; readiness is multi-gate; no clean-fixture person. |
| `rendered_output` | M29, M30, M37 | `SurfaceRecord` / `IntervalAnnotation` | `REUSE/ADAPT` | One-way surface; no memory or psyche write; structural annotation is not a scene. |
| `style_traits` | M31 (optional) | `SurfaceTraitView` or archive | `ADAPT/REPLACE` | Do not use as a causal type; optional descriptive view only. |
| `v5_runtime_input_*`; field injection | M32 | `SourceEnvelope`; `FieldInjectionDecision` | `ADAPT` | Keep inert refs/status/provenance; bind to current world/source; fail closed. |
| `registers`; `metabolic_style` | M26, M38 | `DerivedViewValue` | `REUSE/ADAPT` | Recompute; never persist as actor truth; no hidden writes. |
| `analyst_pressure_account`; surface allowlists | M07, M21, M30 | `AnalystDiagnostic`; `SurfaceRecord` | `ADAPT` | Separate analyst, actor-accessible and public; preserve allowlist/access filters. |
| Placeholder cracks/frameworks; random strivings/ruptures; Enneagram type; fallback event; annotation scene | M09, M11, M16, M31, M34, M35, M39, M37 | `LegacyArtifact` | `REMOVE/ARCHIVE` | Archive with `legacy_synthetic`/`not_causal`; never map into live actor records. |

## 5. Unknown, missing and absent semantics

The migration uses a three-way distinction:

| State | Meaning | Behavior |
|---|---|---|
| `KNOWN` | A source-bearing fact/record exists | Import with source ref, effective time, provenance and rule/owner. |
| `UNKNOWN` | A fact is expected but not established | Preserve `UNKNOWN`; block consumers requiring it; never substitute a midpoint. |
| `ABSENT` | The domain/record does not apply or is validly empty | Preserve valid-empty; no placeholder. |

`UNKNOWN` and `ABSENT` are not `0`, `50`, `100`, `medium`, `neutral`, `hopeful`, `safe`, `clean_ready` or a generated fallback. A missing scientific rule is `HELD_MISSING_RULE`; a denied source is `DENIED_CAUSAL_USE`; an integrity failure is `MIGRATION_INTEGRITY_FAILURE`. None is a lawful psychological `NO_CHANGE` unless an owner-issued rule says so.

## 6. Legacy synthetic atoms and anti-laundering

Every imported value receives a provenance label:

```text
LEGACY_OBSERVED       actual historical event/interval/activity evidence with source
LEGACY_DERIVED        old computed output; recompute or archive, never causal truth
LEGACY_SYNTHETIC      age/demographic/random/placeholder/default-generated value
LEGACY_SURFACE        rendered/persona/annotation text
LEGACY_DIAGNOSTIC     integrity, readiness, error, trace or analyst-only record
LEGACY_UNKNOWN        missing/unestablished/ambiguous
```

**Never promote** `LEGACY_SYNTHETIC`, `LEGACY_SURFACE`, `LEGACY_DIAGNOSTIC` or `LEGACY_DERIVED` into a causal actor record merely by changing its field name. The following are archived, not mapped to causal state:

- placeholder cracks/frameworks, minimum-count repair;
- religion/SES/minority/age framework/crack/practice/wound roots;
- random age-band rupture and random striving spawn/retirement;
- `50` parent/need/capacity defaults and `hopeful` fill;
- one-valence gift/disruption labels from an LLM event type;
- Enneagram type-at-7/parent-type effects;
- narrator keyword scores and annotation prose;
- premerged LLM event deltas and fabricated fallback events;
- stored `registers`/`metabolic_style` caches;
- `degraded_ready`/name-country-only readiness as person proof.

Archive records remain inspectable and hash-addressed, but carry `causally_inert=true`, `legacy_origin`, `source_cut`, `reason` and `migration_receipt_ref`. They cannot be selected by a new C9/C12 reader.

## 7. Start-of-person migration

A fresh actor is not built by filling a BackboneState with defaults.

1. Create `ActorSnapshotV1` with `actor_id`, lineage, source cut and clock.
2. Admit only independently authorized initial facts. Each `InitialFact` has owner, source/ref, effective time, rule/version/hash, evidence grade and uncertainty.
3. If no initial facts exist, return `VALID_EMPTY_INITIAL_DOMAIN_STATE`; do not instantiate capacities, needs, frameworks, cracks, practices, strivings, ruptures or a type.
4. If a required initial fact is unknown, block readiness or return a typed `MISSING_INITIAL_FACT`; do not infer it from country/class/religion/age/sex/family label.
5. `DevelopmentalOrientation` starts as `UNKNOWN`/valid-empty unless an owner-issued source establishes a specific orientation.
6. Do not seed mother/father, parents, school friends, community, safe home, religious framework or practice from age or demographics.
7. Initial `Capacity`/material facts must be source-qualified actual facts, not a universal `50` profile.

## 8. Existing-person migration

```text
read_legacy_v3(source_path, expected_fingerprint)
  -> parse LegacyV3Envelope
  -> validate envelope/source/integrity
  -> classify every field as KNOWN / UNKNOWN / ABSENT / SYNTHETIC / SURFACE / DERIVED / DIAGNOSTIC
  -> archive rejected/synthetic atoms
  -> map source-bearing durable facts and events
  -> build ActorSnapshotV1 + CanonicalEventV1 ledger + migration report
  -> validate required records/consumer needs
  -> commit atomically or fail closed
```

Required stages:

1. **Read-only validation:** parse the legacy state, verify schema shape and source fingerprint; no mutation.
2. **Field classification:** produce a per-field `MigrationDecision` with old path/value, classification, new target, reason and evidence.
3. **Event/interval reconstruction:** preserve old event identities only where they are canonical events with source/clock/access; never turn a premerged delta or fallback into an event.
4. **Durable state mapping:** create only source-qualified `TensionRecord`, `MediatorRecord`, `PracticeRecord`, `RuptureRecord`, `ProcessRecord`, `MotiveTargetRecord`, `ExpectationRecord` and relation records.
5. **Fabrication quarantine:** move placeholder/default/demographic/random/type/narrator/fallback atoms to `LegacyArtifact[]`.
6. **Readiness evaluation:** list missing required facts and block/HELD; do not backfill.
7. **Atomic commit:** write snapshot, event ledger, migration report and archive in one transaction; a failure leaves the target unchanged.
8. **Replay check:** re-running the same legacy input + source cut + migration version yields the same report and hashes.
9. **Compatibility projection:** optionally emit an old-shaped projection for inspection; mark it causally inert and non-writable.

### 8.1 Migration report example

```json
{
  "schema": "neo_v3.legacy_migration@1",
  "source": "legacy_v3_backbone@1",
  "source_fingerprint": "sha256:...",
  "actor_id": "actor:...",
  "migration_version": "1.0.0",
  "status": "PARTIAL_WITH_ARCHIVE",
  "fields": [
    {
      "old_path": "expectation_baseline.attachment",
      "old_value": "hopeful",
      "classification": "LEGACY_SYNTHETIC",
      "new_target": null,
      "reason": "unknown parent default; no actor care history",
      "archive_ref": "legacy_artifact:..."
    }
  ],
  "mapped_records": ["practice:..."],
  "unknown_required": ["material.time"],
  "archived_count": 3,
  "migration_receipt_hash": "sha256:..."
}
```

This is illustrative, not a committed schema; a future owner must version and test it.

## 9. Compatibility and backward compatibility

- Old JSON remains readable by a separate `LegacyV3Reader`; it does not construct a live Neo actor.
- `LegacyV3Projection` is a read-only, old-shaped view for audit/tests/persona comparison; it carries `causally_inert=true` and cannot write back.
- No downgrade from Neo actor state to legacy causal state is supported. Export is a projection, not a reverse migration.
- Existing old records are never deleted; they are archived with source cut, reason and hash.
- New readers must reject unknown/missing required records rather than silently applying defaults.
- Surface and diagnostic schemas are explicitly separate; an old `rendered_output` cannot become `MemoryRecord` by importing it.
- Migration version and source fingerprint are part of the actor snapshot; a different cut or version creates a new report/actor, not a hot rewrite.
- The current S39–S52/C9/C12 session formats are out of scope; no `SESSION_FORMAT_VERSION` change is claimed.

## 10. Atomicity, replay and failure

- `MIGRATION_INTEGRITY_FAILURE` on missing/tampered source identity, schema mismatch, incompatible record, missing required provenance or partial write.
- `MIGRATION_PARTIAL` is a reported outcome only if every unmapped field is explicitly `UNKNOWN`/`ARCHIVED` and the actor is blocked for consumers requiring it.
- `MIGRATION_COMMITTED` requires exact source cut, migration version, decisions, archive refs, snapshot hash and receipt hash.
- A failed migration must leave no half-built actor and no modified legacy file.
- Replay uses exact source bytes, source cut, migration version, owner decisions and archive policy; no wall-clock or filesystem order.
- A migration cannot create a scientific rule, native actor permission or readiness verdict.

## 11. Migration tests (design only, NOT_RUN)

1. Fresh actor with no facts → `VALID_EMPTY`; no fabricated capacity/needs/frameworks/cracks/strivings.
2. Absent parent → `UNKNOWN`, not `50`/`hopeful`/safe-home.
3. Placeholder crack/framework → archived, never a live `TensionRecord`/`MediatorRecord`.
4. Age/religion/SES presets → archived, never acquired practice/framework/sensitivity.
5. Random striving/rupture → archived with RNG provenance, never live motive/rupture.
6. One-valence gift/disruption → archived or converted only under a qualified mixed-impression rule; no forced single valence.
7. Old `rendered_output` → `SurfaceRecord`/`LegacyArtifact`, never `MemoryRecord`.
8. Old `registers`/`metabolic_style` → recomputed view, never stored actor truth.
9. Migration idempotence: same bytes/cut/version → identical report/hashes.
10. Atomic failure: injected error leaves target unchanged and no partial actor.
11. Required unknown → blocked/HELD, not `NO_CHANGE`.
12. Compatibility projection roundtrip → old-shaped view works read-only; no write-back.
13. Current C9 reader cannot consume a legacy projection or a surface record as causal state.
14. Malformed legacy values → `MIGRATION_INTEGRITY_FAILURE`, not optimistic conversion.

## 12. Effort and risk

| Work | Estimate | Risk | Dependency |
|---|---:|---|---|
| Schema types, provenance and migration report | 5–8 days | Medium | Actor architecture decision; no science rule needed for empty shell |
| Legacy reader/classifier/archive | 5–8 days | High | Exact source identities and field decisions |
| Fresh actor initialization | 4–6 days | High | ADP/initial-fact owner |
| Event ledger/snapshot transaction | 4–6 days | High | Canonical event contract |
| Compatibility projection/read-only tests | 3–5 days | Medium | Legacy readers; no causal reader |
| Existing-person migration/fixture suite | 8–12 days | High | Source owners and current C9/C12 boundary |
| **Migration foundation total (indicative)** | **29–45 days** | — | Engineering estimate only; excludes science/authority/current-native work |

These are effort estimates, not delivery commitments or authority. The largest lawful immediate migration tranche is schema + read-only reader + classification + archive + fresh valid-empty actor; it does not require a new scientific rule. Existing-person causal import and any C9/C12 consumption remain owner-gated.

## 13. Owners and stop conditions

- **Schema/migration engineering:** V3/C9/C12 schema owner; no production write in this commission.
- **Actor initial facts:** CAN010/CAN011/ADP and exact source owners.
- **World/material/relations:** C0/C8/ADP019/SDTF and source owners.
- **Memory/access:** ADP016/ADP017; retrospective causal use requires SCI05/owner.
- **Native/person:** C9/C12/Pyat C11/A0–A5 and competent human authority.
- **STOP:** if a required source fact/rule/owner is unavailable, return `UNKNOWN/HELD_MISSING_RULE` and continue only the lawful schema/archive work. Do not fill the gap with legacy defaults.
