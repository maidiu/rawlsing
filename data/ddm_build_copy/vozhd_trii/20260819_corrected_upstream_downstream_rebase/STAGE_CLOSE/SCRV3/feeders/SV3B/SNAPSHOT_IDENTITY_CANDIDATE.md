# SV3B — OBJECTIVE ACTOR-FACT SNAPSHOT IDENTITY CANDIDATE

**Authority:** `NON_DISPOSITIVE_TO_SCRV3`  
**Purpose:** finite candidate for the comparator-facing actor-fact snapshot seam.  
**Does not create:** new V3 fact classes, comparator mappings, source applicability, PSEPF semantics, or developmental prior authority.

## 1. Separation theorem

The seam must preserve:

```text
V3 objective generated fact
!= comparator eligibility
!= empirical source coordinate
!= ActorComparatorReceipt
!= PSEPF
!= V3 developmental prior
```

An objective actor fact may enter a comparator snapshot only if it has a current accepted semantic owner and immutable identity. It may influence an empirical conditioner only if a separate exact `ACTOR_EMPIRICAL_COMPARATOR_AUTHORITY` rule explicitly permits that fact class/owner for the exact source coordinate, universe/scope and time relation.

## 2. Candidate object

Feeder candidate name:

`V3ObjectiveActorFactSnapshot@SV3B-0.1`

This is a **reference-only, query-minimal snapshot**. It is not a copy of `ActorCausalState`, a persona/profile object, a structural-position bundle, or a source-coordinate row.

Candidate fields:

```text
schema_id = V3_OBJECTIVE_ACTOR_FACT_SNAPSHOT
schema_version = SV3B-0.1
actor_id
snapshot_effective_time
v3_time_basis_id
v3_time_basis_version
requested_fact_slots[]
fact_bindings[]
missing_or_blocked_slots[]
owner_currentness_anchor_refs[]
snapshot_hash
integrity_state
```

### 2.1 `requested_fact_slots[]`

Each slot states only what the downstream comparator request is authorized to ask V3 to prove exists as an objective fact. Candidate fields:

```text
slot_id
requested_fact_family
required_owner_authority_id_or_allowed_owner_set
required_fact_semantic_class
multiplicity_contract
required_effective_time_relation
requesting_comparator_rule_ref
```

The slot is not permission to create a fact. It is a request for an already-owned fact.

### 2.2 `fact_bindings[]`

Each positive binding contains:

```text
slot_id
fact_ref
fact_hash
fact_record_type
fact_semantic_class
fact_owner_authority_id
fact_owner_authority_version
fact_owner_authority_hash
actor_id
fact_effective_from
fact_effective_until_or_null
fact_assertion_kind_or_state
semantic_scope_hash
owner_currentness_proof_ref
owner_currentness_proof_hash
```

No raw source coordinate label, prevalence, population distribution, comparator output, PSEPF value, belief, memory, persona or V2/session field belongs in this record.

### 2.3 `missing_or_blocked_slots[]`

Absence is first-class. Candidate state set:

- `ACTOR_PROPERTY_MISSING` — no exact owned fact exists for the requested slot at the snapshot effective time.
- `ACTOR_FACT_AUTHORITY_MISSING` — a purported fact lacks the required accepted owner authority/version/hash.
- `ACTOR_FACT_CURRENTNESS_UNKNOWN` — the owner contract cannot prove whether the fact applies at the requested effective time.
- `ACTOR_FACT_INTEGRITY_FAILURE` — ID/hash/owner/actor binding fails.
- `ACTOR_FACT_MULTIPLICITY_UNRESOLVED` — multiple current facts exist but the requesting comparator rule supplies no lawful multiplicity semantics.
- `ACTOR_FACT_CLASS_NOT_ELIGIBLE` — the requested source is belief, memory, persona, perceived relationship, V2/session/render output, unsupported structural-position shortcut, or another prohibited class.

These feeder-local snapshot states do not replace the D15 comparator terminal states. The projection layer maps unresolved positive use to the authoritative comparator outcomes `ACTOR_PROPERTY_MISSING`, `NO_COMPARATOR`, `AMBIGUOUS_COMPARATOR`, or `TEMPORAL_NONCOMPARABLE` as applicable.

## 3. Snapshot inclusion law

A fact binding is admissible only when all are true:

1. the record is actor-specific and immutable/content-verifiable;
2. its exact semantic owner is accepted and identified by authority ID/version/hash;
3. the owner contract classifies the record as objective generated fact/state, not actor belief/memory/persona/render/session material;
4. actor identity matches the snapshot actor exactly;
5. the fact is effective/current at `snapshot_effective_time` under the fact owner's own lifecycle law;
6. requested slot semantics do not require inference from a neighboring object;
7. no prohibited fallback supplied the fact.

`OBJECTIVE == TRUE` is necessary but not sufficient for comparator use.

## 4. Currentness law

Currentness is owner-defined, never reconstructed by convenience.

Examples:

- an ADP-009 position fact is current only under ADP-009 fact/event lifecycle semantics;
- an ADP-015 household membership fact is current only if its `effective_from`/ended lifecycle makes it active at the snapshot time;
- a CAN-009 embodied state record is current only under its own state-transition/currentness contract;
- an old immutable fact may remain valid historical evidence while being noncurrent for a later comparator request.

Forbidden currentness rules:

- mutable `latest` row;
- file/list/database order;
- nearest earlier value without an exact temporal rule;
- wall clock;
- transcript recency;
- source wave year alone;
- “still probably true.”

If currentness cannot be established, no positive comparator projection is produced.

## 5. Effective time

Three times remain distinct:

```text
actor fact effective time
!= source / historical survey time
!= V3 decision / comparator snapshot effective time
```

The snapshot owns only the V3-side binding of exact actor facts at `snapshot_effective_time`. It does not itself authorize alignment to source time. The comparator rule must carry the exact temporal relation. Failure to align becomes `TEMPORAL_NONCOMPARABLE` rather than nearest-time substitution.

`ADP-021` provides V3 effective-time coordination but does not manufacture actor age, demographic state, or a comparator coordinate.

## 6. Multiplicity law

Multiple simultaneously true objective facts are lawful where their owners allow them. The snapshot preserves them rather than selecting a winner.

Examples include multiple household memberships or multiple structural-position dimensions.

A comparator rule must explicitly declare how a slot handles multiplicity:

- `EXACT_ONE_REQUIRED`;
- `SET_MEMBERSHIP_ANY`;
- `SET_MEMBERSHIP_ALL`;
- `ROLE_FILTERED_EXACT_ONE`;
- another exact rule-owned form.

Without such authority, multiple candidate bindings yield `ACTOR_FACT_MULTIPLICITY_UNRESOLVED` and projection must fail closed as `AMBIGUOUS_COMPARATOR` or `NO_COMPARATOR` according to the comparator court.

No first-row, highest-score, newest, nearest or lexicographic winner is lawful.

## 7. Identity candidate

Canonical serialization candidate: RFC 8785 JCS UTF-8.

Identity projection:

```text
{
  schema_id,
  schema_version,
  actor_id,
  snapshot_effective_time,
  v3_time_basis_id,
  v3_time_basis_version,
  requested_fact_slots_sorted,
  fact_bindings_sorted,
  missing_or_blocked_slots_sorted,
  owner_currentness_anchor_refs_sorted
}
```

Candidate hash:

```text
snapshot_hash = SHA256(
  "rawlsing:v3:objective-actor-fact-snapshot:sv3b-0.1\n"
  || JCS(identity_projection)
)
```

Candidate snapshot ID:

```text
snapshot_id = "v3ofs:" + snapshot_hash
```

Sorting is canonical serialization only; it never selects a semantic winner.

## 8. Why the requested slot set participates in identity

A snapshot that proves `household_membership` and one that proves `household_membership + exact_region_fact` are not semantically interchangeable even when the underlying actor happens to have the same current records. Missing-slot state is part of the evidence contract and therefore part of snapshot identity.

This also prevents a downstream consumer from taking a narrow snapshot and silently treating it as proof that some unrequested actor fact was absent.

## 9. Why the full actor state is excluded

A comparator snapshot must be narrower than `ActorCausalState`.

Including the full actor state would expose prohibited material and create indirect conditioning paths through:

- belief/knowledge;
- memory;
- persona/voice;
- perceived relationship state;
- developmental middle-state/psyche;
- response history;
- unrelated structural/material state.

The snapshot therefore carries only exact requested objective fact refs plus explicit missing/block states and currentness proofs.

## 10. Replay/current-request rule

Historical replay may use an old snapshot exactly as originally hashed.

A new comparator request at a later effective time must construct or select a snapshot whose requested slots and currentness proofs are valid for that later time. It may not silently reuse an old snapshot because its fact objects are immutable.

Fact immutability is not perpetual snapshot currentness.

## 11. Feeder disposition

This candidate is suitable for SCRV3 synthesis because it closes the identity/currentness shape without inventing any positive fact class or comparator mapping.

The parent should retain the two independent gates:

```text
GATE 1: exact objective fact exists and is current under its V3 owner
GATE 2: exact comparator authority permits that fact class -> source coordinate projection
```

Failure of either gate is typed and fail-closed.
