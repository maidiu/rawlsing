# SYN02-RM40 — legacy migration and patch test specification

**Status:** `PATCH_AND_MIGRATION_SPECIFICATION__NO_IMPLEMENTATION__NO_NATIVE_GRANT`.
**Architecture target:** `321fa29bb3e51849a43cb7caf1600625bf215539`; **review target:** `ac55c36e42ded82957176896cbc5953db62f7209`; **commission seal:** `07ebb10eac214ebc909b92f24b459caf2d37d730`.
**Purpose:** translate the all-40 patch map and ten-cell adjudication into code-edit-ready F1/F2/F3 seams, source-version provenance, migration rules and negative tests. These are specifications, not merged code.

## 1. Patch landing zones

The future implementation must use new, uniquely owned modules; it must not edit old V3, S04/S05, the original atlas or current C9/C12 in this commission. Candidate landing areas:

```text
neo_v3/actor/schema.py             # ActorSnapshotV1, stable IDs, provenance
neo_v3/actor/ledger.py             # CanonicalEventV1, episode, receipt
neo_v3/derived/registry.py         # pure derived views
neo_v3/migration/v3_reader.py      # read-only legacy archive/classifier
neo_v3/migration/report.py         # decisions, quarantine, receipt
neo_v3/surface/readonly.py         # one-way surface/access view
neo_v3/memory/access_projector.py  # ADP16/17 feature allowlist
neo_v3/batch/proposal.py           # 3–5 proposed specifications
neo_v3/batch/realize.py            # source-owned event/interval shell
neo_v3/batch/receipt.py            # committed prefix/held suffix
neo_v3/source/resolver.py          # SourceRef, hash/role/scope verifier
```

These are candidate names. A future code owner may place equivalent modules only in its accepted package; no new `ActorStateV1`/`PersonState`/graph store may compete with the one actor authority.

## 2. F1 — pure derived, schema and migration

### 2.1 Retained/computed boundary

- `DerivedViewSpec` declares dependencies, owner, version and content hash.
- `DerivedViewValue` is keyed by exact `actor_snapshot_hash` and `view_version`.
- `compute_view(view_id, snapshot)` reads only the exact snapshot and returns a value; it does not mutate `snapshot`, `registers`, `metabolic_style`, or any persistent field.
- Old M26 `compute_all_derived` becomes a migration-only comparison/probe, not an actor writer.
- Old M38 schedule becomes a pure registry/declared dependency check; no stale cache is read as actor truth.
- Old M19/M29 `rendered_output`/narration support is not a derived actor value; it is a surface/diagnostic.

### 2.2 Exact migration functions

```text
read_legacy_v3(path, expected_fingerprint) -> LegacyV3Envelope
classify_legacy_field(path, value, source_ref) -> MigrationDecision
archive_legacy_atom(value, reason, source_ref) -> LegacyArtifactRef
migrate_legacy_actor(envelope, policy) -> MigrationResult
build_fresh_actor(initial_facts) -> ActorSnapshotV1
project_legacy_compatibility(actor) -> LegacyProjection (read-only)
validate_migration(result) -> MigrationStatus
```

`MigrationDecision` must carry `old_path`, `old_value`, `classification`, `new_target`, `reason`, `source_ref`, `archive_ref`, `rule/owner` and `confidence`. `MigrationResult` is all-or-nothing for a new actor; failure returns archived source plus `MIGRATION_HELD`/`INTEGRITY_FAILURE`, not a partial actor.

### 2.3 Migration classifications

| Legacy class | Treatment |
|---|---|
| Objective source-qualified event/interval/material fact | Map to a canonical source/event/material record with source owner, clock and hash. |
| Old durable carrier with a source/owner rule | Map to a typed record only where the source/rule qualifies; otherwise `CARRIER_ONLY`. |
| Derived old value (`registers`, `metabolic_style`, pressure-flow trace/cache) | Recompute as pure view or retain as read-only diagnostic; never actor causal state. |
| Rendered narrative/annotation/persona text | `SurfaceRecord`/`LegacyArtifact`; never memory/actor state. |
| `50`/`hopeful`/safe-home/class-age-religion/type/random/placeholder/fallback | `LEGACY_SYNTHETIC` archive; no causal import. |
| Missing/unknown/absent | `UNKNOWN`/`ABSENT`/`HELD`; no midpoint/default. |

Mandatory quarantine: M19 narrator-derived support, M26 hidden writes, M34 fallback, M35 placeholders, M36 unknown-parent defaults, M31 type-at-7/parent-type effects, M39 age-rupture, demographic crack/framework/practice/wound seeds, M17 mono-valence, M20 parent labels, M37 annotation-as-memory, M40 stored-persona clean-ready. Objective material facts may survive only with independent source and clock.

### 2.4 Source/version provenance

Every imported/changed actor state includes:

```text
SourceRef {source_id, path_or_uri, sha256, bytes, owner, role, scope, effective_time, source_cut}
RuleRef {owner, rule_id, version, content_hash, effective_time}
ActorSnapshotV1 {schema_version, actor_id, source_cut, clock, provenance, record_hash}
```

A source hash mismatch, missing role/scope, changed payload under the same idempotency key or unsupported source version fails closed. Migration is idempotent for identical source bytes/cut/version; a changed source requires a fresh decision and leaves the old actor unchanged.

## 3. F2 — actor-safe V2 and memory

### 3.1 One-way surface

- `SurfaceRecord` has `causal_write_permission=false`.
- V2/ADP017 reads `ActorVisibleSurface`; it cannot write actor state, create memory, or update `narration_support`.
- M29 immediate `render_year` body may be reused only as a pure text/render helper; the full old LLM band/status is not reused.
- M30 `/V3` one-person jurisdiction survives, but no age<17→35 substitution, parent narrative, or second narrating psyche.
- M37 `IntervalAnnotation` is separate from `MemoryRecord`/`previous_scene`; its text cannot be selected as an episode.
- M19 prose→psyche path is deleted from the new graph; `NarrationSupport` can be constructed only from exact narrator/support/practice refs under an owner rule.

### 3.2 Access-filtered memory

`select_accessible_features(realized_prefix, actor_access_refs, adp_feature_allowlist)` produces a deterministic model-visible packet with:

- no objective event IDs, ordinals, total counts, hidden suffix/gap labels;
- no inaccessible event content or indirect count/order leakage;
- only actor-accessible/ADP017-sourced features and explicitly graded uncertainty;
- a `belief_with_source` record distinct from fabricated positive sensory memory;
- a `NO_MEMORY`/`ACTOR_UNKNOWN` result when access is not established.

Any objective care that occurred but was not received is recorded in the world/coevent ledger, not in the actor's memory. Later testimony is a later source, never backdated childhood perception.

## 4. F3 — 3–5 event adapters

### 4.1 Envelope and admission

```text
BatchProposalV1 {
  call_id, actor_id, source_cut, proposals: ProspectiveSpec[3..5],
  self_account_proposal?, proposal_hash
}
ProspectiveSpec {
  opaque_proposal_id, conditional_world_facts[],
  possible_coactor_refs[], source_owner_refs[],
  actor_access_premises[], dependency_on_self_account?
}
CanonicalEventV1 {event_id, source_owner_ref, effective_time, parent_refs[], participants[], material_refs[], provenance, status}
ActorDecisionV1 {actor_id, event_ref, prior_actor_hash, RuleA_ref, RuleT_ref|NO_CHANGE_REF|HELD, after_actor_hash, receipt_ref}
```

1. Model text is a proposal only; no material event is created.
2. For each proposal in sequence, source/world owner realizes or denies the independent event and interval; a coactor may act differently from the proposal or not at all.
3. Actor access is checked before a Rule A response.
4. Rule A and Rule T are separate; missing rule returns `HELD_MISSING_RULE`, not `NO_CHANGE`.
5. Each event reads the actual preceding actor/world state; no `merge_deltas`, no premerge.
6. `three_to_five` accepts exactly 3–5 proposals; 0/1/2/6 are invalid; no fallback event.
7. The old M34 fallback and M33 mechanical sampler are not imported.
8. The M25 year/step spine becomes a slow interval/scaffold, not the causal batch unit.
9. The batch policy (prefix vs whole-atomic vs independent suffix) is `POLICY_UNDECIDED`; the shell may record but must not execute an irreversible multi-event batch until a competent owner chooses.

### 4.2 SCI05 and N+1

- Same-call first-half retrospective is proposed text, not admitted actor state.
- Second-half prospects that semantically depend on an unadmitted first-half interpretation are invalidated/held after call review.
- An optional dependency pointer is not proof of independence; absent pointer is not proof of nondependence.
- No extra ordinary LLM call between events.
- Render failure after an actual event commit does not erase the event/actor receipt, but the product is not `CLEAN`.

## 5. Negative and positive tests (specification, NOT_RUN)

### 5.1 Actual validation run by RM40

The only executed validation in this commission is the 480-cell/source-hash validator, not a psychological test. It checks:

- exactly 40 ordered M rows;
- exactly 12 N cells per row, 480 total;
- baseline 126 X / 354 dash and final 124 X / 356 dash;
- exactly ten changed cells;
- 59 source hashes and 31/31 S50 selected identities;
- no duplicate M/N cell, no missing M/N;
- unsupported M14/N02 and M39/N01 have no X; eight indirect cells retain X.

Command and receipt are recorded in `00_RETURN.md`; no source code test was run.

### 5.2 Future F1 tests

```text
pytest tests/neo_v3/test_pure_derived.py
pytest tests/neo_v3/test_legacy_migration.py
pytest tests/neo_v3/test_unknown_and_archive.py
```

- `test_compute_view_does_not_mutate_snapshot`: snapshot hash unchanged; `registers`/`metabolic_style` absent or exactly equal before/after.
- `test_migration_missing_parent_is_unknown`: no 50/hopeful/safe.
- `test_placeholder_and_demographic_atoms_are_archived`: no live tension/mediator/practice/wound.
- `test_migration_idempotent_and_changed_source_rejected`: same source/version same report; changed bytes fail closed.
- `test_migration_atomic_failure`: no partial actor.

### 5.3 Future F2 tests

```text
pytest tests/neo_v3/test_surface_one_way.py
pytest tests/neo_v3/test_adp_memory_access.py
pytest tests/neo_v3/test_narrator_severance.py
```

- Warm/coercive/annotation prose perturbation changes no actor snapshot or later semantic value.
- Removing one accessible ADP feature removes all direct and indirect mentions, IDs/count/order/gaps.
- A summary/belief can be sourced without fabricated episode; unseen care remains world-only.
- Old M37 annotation cannot appear in memory or previous scene.

### 5.4 Future F3 tests

```text
pytest tests/neo_v3/test_batch_3_5.py
pytest tests/neo_v3/test_event_ledger_and_admission.py
pytest tests/neo_v3/test_interval_and_policy_hold.py
pytest tests/neo_v3/test_self_account_dependency.py
```

- 3/4/5 accepted as proposals; 0/1/2/6 rejected; no fabricated filler.
- Event 1 realized, event 2 source-denied, suffix not materialized or remembered; selected event appears in canonical ledger.
- Reversing event 1/2 changes event-2 read, or lawful held/no-change; no premerge invariance.
- Missing Rule T -> held, not true no-change.
- Full-batch policy undecided -> holds before irreversible multi-event action.
- SCI05 denial invalidates dependent half2 proposals.
- No extra ordinary LLM call.

### 5.5 Future source/current tests

```text
pytest tests/neo_v3/test_source_refs.py
pytest tests/neo_v3/test_c9_c12_receipt.py
pytest tests/neo_v3/test_s48_s52_portability.py
```

- Source hash/role/scope mismatch fails closed.
- C9 actor commit/outbox/C12 mirror cold/fork/crash recovery preserves one actor version/receipt.
- S48/S52 hardcoded Mac/provider defaults are injected; S52 verifier does not override S52 errors under `_OPENING`+base_ok.
- No provider/model/account call in tests.

## 6. Effort and gate

| Work | Indicative effort | Gate |
|---|---:|---|
| F1 pure derived + migration + source resolver | 10–18 days | schema/C9 owner; no science |
| F2 surface + access memory + narrator severance | 6–12 days | ADP016/017/V2/SCI05 |
| F3 3–5 shell + ledger/admission + interval/policy holds | 12–20 days | C6/C8/C9/C12; policy owner |
| F3 concrete Rule A/T/world realization | 20+ days plus owner time | CAN/world/B/native owners |
| Current C9/C12 integration/cold/fork | 15–30 days | C9/C12/Pyat; not in this commission |

**Largest lawful immediate tranche:** F1 source/schema/pure-derived/migration + F2 one-way surface with no semantic rule. F3 can build the proposal/ledger/held shell, but cannot execute real 3–5 event formation until source/world/rule/policy owners issue. No fake coefficients, narrator-derived state, old default psychology or single fixture “person.”

**No implementation. No scientific issuance. No native grant.**
