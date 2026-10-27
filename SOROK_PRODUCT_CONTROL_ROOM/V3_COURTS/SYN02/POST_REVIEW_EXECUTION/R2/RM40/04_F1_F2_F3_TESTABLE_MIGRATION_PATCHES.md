# SYN02-RM40-R2 — F1/F2/F3 TESTABLE MIGRATION PATCHES

**Status:** build-ready design and test specification; code not edited; no sourcefree behavioral test executed.
**Branch:** `agent/sorok-syn02-rm40-r2-literal-v3-patch-map-r1`; **startup:** `2da83f77d820b327169673386d52c4acefbbdd46`; **RM40:** `653d356d773ab025c4ed22e9d70ba8fc25d6f839`; **RRM40:** `0c181943e527613f4bc114684a1962949a549e20`.

## 0. Non-negotiable boundaries

- F1/F2/F3 are future adapter specifications, not live imports. No adapter below is implemented or wired.
- `WAIT_FOR_C9_C12_STORAGE_OWNER_FREEZE` applies to F1.1. No actor CAS, outbox, C9 transaction, QualifiedC12Store DDL, or C12 persistence is assumed or rewritten.
- No current RP0-R2 output is being reproduced from memory. F1.1 uses typed placeholder ports until the physical RP0-R2 contract is available; absence of that contract is a HOLD, not a reason to invent storage behavior.
- No new Rule A/Rule T, no CAN/ADP/SCI05 issuance, no C11 weld/C12/A5 release, no native science. The eight retained RM40 carrier links are not permissions.
- The old actor is read-only historical material. Objective facts may migrate; synthetic scores, age/type assignments, placeholders, narrator-derived material and absent-parent hopeful defaults are quarantined, not silently defaulted.
- No actor B from a fixture. B, care and time remain explicit slots; a test fixture cannot become a person or world event source.

## 1. F1 — pure derived/read adapters and legacy migration

### F1.1 `WAIT_FOR_C9_C12_STORAGE_OWNER_FREEZE` — read-only actor/derived source

**Target:** `neo_v3/derived/read_port.py` plus `neo_v3/actor/migration.py`.
**Purpose:** let a derived view be computed from an explicit snapshot without mutating the actor or assuming C9/C12 storage.
**Status:** `TO_BUILD`; storage-dependent portions blocked until physical owner freeze.

```python
from dataclasses import dataclass
from typing import Protocol, Sequence

@dataclass(frozen=True)
class ActorSnapshotV1:
    actor_id: ActorId
    source_cut: SourceCutRef
    facts: tuple[CanonicalFactRefV1, ...]
    unknown: tuple[UnknownRefV1, ...]

@dataclass(frozen=True)
class DerivedViewRequestV1:
    view_id: ViewId
    actor_id: ActorId
    source_cut: SourceCutRef
    access: AccessEnvelope

@dataclass(frozen=True)
class DerivedViewValueV1:
    view_id: ViewId
    value: object
    source_fact_ids: tuple[FactId, ...]
    status: Literal["OK", "HELD", "UNKNOWN"]
    warnings: tuple[str, ...]

class C9ActorHistoryPort(Protocol):
    """Placeholder only; physical RP0-R2 must supply the real contract."""
    def read_snapshot(self, actor_id: ActorId, source_cut: SourceCutRef) -> ActorSnapshotV1: ...

class C12DerivedStorePort(Protocol):
    """Placeholder only; no QualifiedC12Store DDL is owned here."""
    def write_view(self, value: DerivedViewValueV1) -> None: ...

def compute_view(snapshot: ActorSnapshotV1, request: DerivedViewRequestV1) -> DerivedViewValueV1:
    """Pure: no mutation, no event append, no implicit storage read."""
    ...
```

**Exact patch rules:**

1. `compute_view` may read only `snapshot.facts`, `snapshot.unknown`, `request.view_id` and `request.access`; it may not read global state, old `BackboneState`, `rendered_output`, or a C12 store.
2. If `request.source_cut != snapshot.source_cut`, return `HELD` with `SOURCE_CUT_MISMATCH`; do not substitute a newer snapshot.
3. If a view is not registered, return `HELD` with `UNKNOWN_VIEW`; do not compute a best-effort value.
4. `write_view` is called only by an injected owner port. The adapter itself returns a value and never imports C9/C12 writers.
5. No event ID, count, gap, actor-visible surface, or V2 text is produced by this layer.

**Deterministic sourcefree tests (future):**

- `T-F1.1-PURE`: deep-copy/freeze the input snapshot, call `compute_view`, assert all bytes and tuple identities unchanged; assert no `state.events_this_year`/`gifted_shards` mutation.
- `T-F1.1-CUT`: mismatched source cut returns `HELD/SOURCE_CUT_MISMATCH`; no view value.
- `T-F1.1-PORT`: calling a storage-dependent path without a physical port raises/returns `HELD/STORAGE_OWNER_FREEZE`; it does not touch files or SQLite.
- `T-F1.1-NO-DEFAULT`: an absent fact yields `UNKNOWN`, never `50`, `hopeful`, `0`, or a fabricated object.

**Consumer:** `C9.derived_view_read` — `TO_BUILD`, pending owner storage freeze.
**Source mapping:** M21 transaction trace, M26 derived views, M38 schedule/cache; all are read-only or explicitly held.

### F1.2 legacy actor/world migration

**Target:** `neo_v3/actor/migration.py` and `neo_v3/world/migration.py`.
**Function:** `migrate_legacy_actor(source: LegacyActorSourceV1, ports: MigrationPortsV1) -> MigrationRecordV1`.
**Status:** `TO_BUILD`; migration can be tested against frozen fixtures without live C9/C12.

**Retained objective material:** source-qualified actor facts, event IDs, care/time observations, material constraints, relationship/entity references, explicit unknown/missing markers, provenance hashes, and legacy diagnostics.
**Quarantined material:** `synthetic_default_50`, `absent_parent_hopeful`, `age_or_type_assignment`, `placeholder_crack_or_framework`, `narrator_secondary_interpretation`, `derived_cache_value`, and any `rendered_output` text used as memory or cause.

**Migration record:**

```python
@dataclass(frozen=True)
class QuarantineRefV1:
    legacy_path: str
    field: str
    category: Literal["synthetic_default_50", "absent_parent_hopeful", "age_or_type",
                      "placeholder", "narrator_prose", "derived_cache"]
    source_sha256: str
    action: Literal["QUARANTINE", "DROP", "ARCHIVE_ONLY"]

@dataclass(frozen=True)
class MigrationRecordV1:
    actor_id: ActorId
    source_cut: SourceCutRef
    retained_facts: tuple[CanonicalFactRefV1, ...]
    unknowns: tuple[UnknownRefV1, ...]
    quarantine: tuple[QuarantineRefV1, ...]
    status: Literal["OK", "PARTIAL_HELD", "BLOCKED"]
```

**Rules:**

1. Missing parent/care evidence is `UNKNOWN`/`BLOCKED`, never `50`, `hopeful`, or `safe home`.
2. Age/type/enneagram/rupture-at-age material cannot become a cause, disposition, need or expectation. It can only be archived as a noncausal description, and M31 remains `RULE_HELD`.
3. M09 cracks, M35 minimum cracks/frameworks, M34 fallback events and M36 unknown-parent defaults are dropped from causal input. Diagnostics may retain counts, never objects.
4. M19 `rendered_output` and M37 annotation prose cannot become `NarrationSupport`, memory, a prior scene or a state summary. Preserve only a separate annotation record with source hash and no memory-read API.
5. M12 institutions/ties move to world owner; M32 source refs remain inert until `field_injection_decision` admits them. No legacy scalar is copied into an actor as institutional reality.
6. Migration is idempotent: the same source + cut yields the same retained/quarantine IDs; no writes to C9/C12.

**Tests:**

- `T-F1.2-OBJECTIVE`: event ID, source-qualified fact, care/time and constraint survive with the same hash; values are not clamped to 50.
- `T-F1.2-MISSING`: absent parent produces `UnknownRefV1`, not `hopeful`/`50`; M36 adapter returns `UnknownExpectation` and no person surface.
- `T-F1.2-AGE-TYPE`: age/type/enneagram inputs appear only under `ARCHIVE_ONLY`; no need/object/consumer receives them.
- `T-F1.2-PLACEHOLDER`: seeded crack/framework inputs produce `ValidEmpty` diagnostics, not objects; no placeholder IDs in normal state.
- `T-F1.2-NARRATOR`: rendered prose/annotation is archived with a digest and is unreadable through memory/surface ports.
- `T-F1.2-IDEMPOTENT`: two migrations produce identical record hashes and no state/event/count change.

### F1.3 derived invariant replacement (M26/M38)

**Target:** `neo_v3/derived/registry.py`; `neo_v3/core/invariants.py` replacement.
**Reason:** current `compute_all_derived` assigns `state.metabolic_style` and `state.registers` at `v3/core/derived.py:322-334`; the existing invariant checks six fixed names and misses those writes.
**Patch:** replace the fixed-name assertion with a full-snapshot before/after fingerprint over all fields, including `registers`, `metabolic_style`, caches and schedule-derived values. A write is a hard failure; a stale cache is a held/degraded result, never a silent value.

**Tests:** `T-M26-DERIVED` (all fields unchanged after every registered view), `T-M38-SCHEDULE` (schedule equality; no missing/stale view), `T-F1.3-WRITE` (deliberate hidden write fails with field name and before/after digest).

## 2. F2 — actor-safe packet, one-way surface and SCI05 refusal

### F2.1 allowlisted `SurfacePacketV1`

**Target:** `neo_v3/surface/packet.py`.
**Function:** `build_surface_packet(actor: ActorSnapshotV1, access: AccessEnvelope, request: SurfaceRequestV1) -> SurfacePacketV1`.
**Status:** `TO_BUILD`; no V2/SCI05 consumer is live.

```python
@dataclass(frozen=True)
class SurfacePacketV1:
    actor_id: ActorId
    source_cut: SourceCutRef
    access: AccessEnvelope
    visible_facts: tuple[ActorVisibleFactV1, ...]
    event_refs: tuple[ActorVisibleEventRefV1, ...]
    count_buckets: tuple[CountBucketV1, ...]
    gaps: tuple[GapMarkerV1, ...]
    packet_digest: str

@dataclass(frozen=True)
class GapMarkerV1:
    gap_id: GapId
    value: Literal["UNKNOWN", "WITHHELD", "NOT_OBSERVED"]
    reason_code: str  # no free text
```

**Serializer rules:**

1. Allowlist exact keys only. Unknown keys are rejected, not copied through a dict or `**kwargs`.
2. No raw event ID unless the event is actor-visible under `AccessEnvelope`; otherwise emit a stable opaque reference or omit it. Do not encode hidden IDs in labels or errors.
3. Counts are bucketed (for example `0`, `1`, `2-3`, `4+`); exact counts are not a backdoor leak. Gaps are explicit `UNKNOWN`/`WITHHELD`/`NOT_OBSERVED`, never zero or a fabricated event.
4. Exclude source paths, prompts, provider metadata, token counts, internal process IDs, narrator prose, prior-scene memory, other actors, secrets, and quarantine fields.
5. `packet_digest` covers exactly the emitted fields; a digest mismatch is a hard error. Access filtering happens before serialization, not after text generation.
6. The packet is immutable and one-way. No API on `SurfacePacketV1` writes actor state, memory or events.

**Tests:**

- `T-F2.1-ALLOWLIST`: unknown field and nested `**` dict are rejected; only allowlisted fields survive round-trip.
- `T-F2.1-EVENT-ID`: non-visible event ID does not appear in serialized bytes, nested labels, errors or digest inputs; visible ID appears exactly once.
- `T-F2.1-COUNT-GAP`: exact count 1/2/4 maps to buckets; a missing observation is `WITHHELD`/`UNKNOWN`, never `0`; no gap becomes an event.
- `T-F2.1-DIGEST`: field mutation changes digest; digest mismatch fails closed.
- `T-F2.1-NO-WRITE`: after packet build, the actor digest, event list, count and memory are unchanged.

### F2.2 one-way V2 surface and SCI05 refusal

**Target:** `neo_v3/surface/read.py`; `neo_v3/surface/sci05.py`.
**Status:** `TO_BUILD`; `V2.surface_read` and any SCI05 call remain outside this branch.

- `read_surface(actor, access) -> ActorVisibleSurfaceV1` is read-only and returns a frozen packet. V2 cannot write back, create memory, instantiate a second psyche, or introduce a narrator as a causal source.
- If a V2/SCI05 request requires a fact not present in the packet, return `IMPLICIT_DEPENDENCE_REFUSED` with a typed reason. It must not infer the missing fact from prose, previous output, actor identity, provider metadata or another model call.
- SCI05 generated text cannot authorize internal state change. Any request for such a change is refused as `SCI05_INTERNAL_SELF_CHANGE_REFUSED`; it is not forwarded to an owner.
- M30's one-person jurisdiction is preserved; age/parent substitutions and story feedback are not.

**Tests:** `T-F2.2-ONE-WAY` (surface call leaves actor digest/events/memory unchanged), `T-F2.2-HIDDEN-DEP` (missing hidden fact -> refusal), `T-F2.2-SCI05` (generated self-change -> refusal; no state delta), `T-F2.2-NO-NARRATOR` (narrator/prose field not accepted).

## 3. F3 — proposal-to-event sequential adapter and guarded 3–5 shell

**Targets:** `neo_v3/llm/batch.py`, `neo_v3/runtime/admission.py`, `neo_v3/runtime/event_sequence.py`.
**User-settled constraint:** 3–5 proposals per batch; N+1 two-half retrospection after the batch; no ordinary LLM turn between the 3–5 events (in the current scope).
**Unselected:** world-batch failure/partial policy. F3 therefore cannot perform irreversible world actions; it may only propose and hold.

### F3.1 proposal (no mutation)

```python
@dataclass(frozen=True)
class BatchProposalV1:
    actor_id: ActorId
    source_cut: SourceCutRef
    candidates: tuple[ProspectiveSpecV1, ...]  # 3..5 only
    provenance: ProposalProvenanceV1
    status: Literal["PROPOSED", "HELD", "REFUSED"]

def propose_batch(actor: ActorSnapshotV1, prompt: PromptEnvelopeV1, source: SourceRef) -> BatchProposalV1:
    """Parse/validate only; never apply a delta or write actor state."""
    ...
```

Rules: exactly 3–5 candidates; every candidate has a source/conditioning ref; duplicate IDs and premerged deltas are rejected; empty is `NoEventRecord`, never fallback; no global RNG; no state mutation. N+1 retrospection is a separate half-event record and is not inserted as an ordinary fourth/fifth event.

### F3.2 admission (one actual event at a time)

```python
@dataclass(frozen=True)
class CanonicalEventV1:
    event_id: EventId
    actor_id: ActorId
    interval: IntervalRef
    source_refs: tuple[SourceRef, ...]
    admission: Literal["ADMITTED", "HELD", "NO_EVENT"]

def admit_event(actor: ActorSnapshotV1, proposal: ProspectiveSpecV1, source: SourceRef) -> CanonicalEventV1 | NoEventRecordV1:
    """Append one canonical event when source/rule/admission checks pass; otherwise hold/no-event."""
    ...
```

Rules: no premerged capacity/domain/wound/practice deltas; no event without an independent source; no fallback/placeholder; no actor B fixture; admission order is one event at a time; B/care/time are explicit, source-qualified slots. `WorldEventSource` is not allowed to synthesize an event from actor state, age, type, narrator text or random choice.

### F3.3 guarded 3–5 shell

```python
@dataclass(frozen=True)
class EventSequenceShellV1:
    proposals: BatchProposalV1
    events: tuple[CanonicalEventV1 | NoEventRecordV1, ...]
    status: Literal["DRY_RUN", "HELD", "REFUSED"]

def run_guarded_sequence(actor, prompt, source, world: WorldPerformancePort) -> EventSequenceShellV1:
    """Propose and admit at most 5; world performance is not called in this branch."""
    raise NotImplementedError("WAIT_FOR_WORLD_FAILURE_PARTIAL_POLICY")
```

The shell can be exercised as a **dry run** only. `world.perform`/`commit` is represented by a port but never invoked; any irreversible world call returns `HELD/WORLD_PERFORMANCE_UNAUTHORIZED`. If the batch is empty/partial, the result is explicit no-event/held; it cannot silently become a successful 3–5 batch.

**Tests:**

- `T-F3.1-COUNT`: 3, 4, 5 accepted; 0, 2, 6 refused; duplicate IDs refused.
- `T-F3.1-PURE`: proposal leaves actor/event/count/memory digests unchanged; premerged delta key is refused.
- `T-F3.1-EMPTY`: empty source/parse yields `NoEventRecordV1`; no fallback event, no practice/crack placeholder.
- `T-F3.2-ONE`: one admitted proposal creates exactly one canonical event; no capacity/domain/wound/practice keys appear in the event envelope.
- `T-F3.2-SOURCE`: missing/unauthorized source yields `HELD`, not an event; no actor B fixture is accepted.
- `T-F3.2-NO-PREMERGE`: after admission, old `apply_deltas_to_state` path is not called; event row is the only new causal record.
- `T-F3.3-NO-WORLD`: shell is `DRY_RUN`; a spy `WorldPerformancePort.perform` count is zero and irreversible commit is refused.
- `T-F3.3-PARTIAL`: partial batch yields held/no-event with reason; no invented event count; policy remains `UNSELECTED`.

## 4. Patch ledger and sourcefree levels

| Patch | Future path | Import/signature | First consumer | Test level | Current status |
|---|---|---|---|---|---|
| F1.1 | `neo_v3/derived/read_port.py` | `compute_view(ActorSnapshotV1, DerivedViewRequestV1) -> DerivedViewValueV1` | `C9.derived_view_read` | sourcefree pure + frozen snapshot | `TO_BUILD`; `WAIT_FOR_C9_C12_STORAGE_OWNER_FREEZE` |
| F1.2 | `neo_v3/actor/migration.py` | `migrate_legacy_actor(LegacyActorSourceV1, MigrationPortsV1) -> MigrationRecordV1` | C9 migration/read-only archive | sourcefree frozen fixture | `TO_BUILD` |
| F1.3 | `neo_v3/core/invariants.py` | full-snapshot before/after invariant | every derived view | sourcefree | `TO_BUILD` |
| F2.1 | `neo_v3/surface/packet.py` | `build_surface_packet(...) -> SurfacePacketV1` | `ADP017`/V2 packet | sourcefree allowlist/serialization | `TO_BUILD` |
| F2.2 | `neo_v3/surface/read.py` | `read_surface(ActorSnapshotV1, AccessEnvelope) -> ActorVisibleSurfaceV1` | `V2.surface_read` | sourcefree one-way/refusal | `TO_BUILD` |
| F3.1 | `neo_v3/llm/batch.py` | `propose_batch(...) -> BatchProposalV1` | event realization | sourcefree count/purity | `TO_BUILD` |
| F3.2 | `neo_v3/runtime/admission.py` | `admit_event(...) -> CanonicalEventV1 | NoEventRecordV1` | `C8.event_admit` | sourcefree admission | `TO_BUILD` |
| F3.3 | `neo_v3/runtime/event_sequence.py` | `run_guarded_sequence(...) -> EventSequenceShellV1` | C9 batch | sourcefree dry run | `TO_BUILD`; world policy `UNSELECTED` |

## 5. Execution status

| Command/level | Result |
|---|---|
| Structural JSON validator `05_VALIDATE_R2.py` | run after writing; see `00_RETURN.md` |
| Source identity 59/59 and S50 31/31 | rehashed locally; see `02` and `00_RETURN.md` |
| Proposed sourcefree behavioral tests above | `NOT_RUN` |
| Real model/product calls | `NOT_RUN` |
| Old V3/C9/C12/production edits | `NONE` |

These tests are specifications for the future adapter PRs. This return does not claim any has passed, and no test fixture substitutes for actor B, world performance, source authority or scientific issuance.
