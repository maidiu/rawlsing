# ASTRA-C02 — Objective World Root Contract Candidate R1

## Status

`PASS__PREV3_OBJECTIVE_WORLD_RELEASE_AND_VALID_TIME_BOOTSTRAP_R1_ONLY`

This is a **bounded candidate contract**, not self-adoption and not production runtime. It is returned to Sub-Vozhd II / HQ at `GATE-WORLD`.

## Scope grounding

- Worker branch: `agent/rabochii-astra-c02-world-release-valid-time-r1`
- Exact commissioned start: `7689d794ad09975a0313fa95c74ff82d85e63dc2`
- Frozen dispatch parent: `2a88795031d80cb5bc49979c34ace0dd2427ca6e`
- Clean semantic floor preserved: `3468673673db2f3de804d6e825585f86ff98e870`
- Branch is six commits ahead of that floor and the floor is the merge base.
- No sibling return was consumed as authority.
- No production-code scope was granted.
- OBL063 quarantine remains intact: `6cf605b0c63f6a4ec66170bb8dc00b3060002d1a`, `9b60d3936ad7919f0b5583b4024a821e4591c9c8`, `80e948e7bea5ff430b40f86942459a91a590683b`.

## Finding

The A3W circularity is removed by separating **objective world validity** from the **V3 runtime cursor**.

The objective world/release root must exist first, from PRE-V3-owned immutable release, repository, scope and valid-time inputs. A later V3 runtime cursor may select or query a slice of that already-authorized world; it cannot authenticate the root, supply missing objective truth, or mint valid time.

This preserves the current M4/M5 division:

1. M4/V557 owns immutable publication governance.
2. M4/V558 owns immutable repository identity, indexes, exact context selection and resolution receipts.
3. A smallest new PRE-V3 world/time owner binds those already-authorized objects to an objective release/root and concrete world-validity basis.
4. M5 remains downstream: it deterministically replays M4 resolution and may materialize `ResolvedStructuralContext` only after explicit currentness authority.
5. V3 remains downstream of the objective world. Structural context eligibility has no actor-state mutation effect.

## Candidate type

`PREV3_OBJECTIVE_WORLD_RELEASE_ROOT_R1`

Canonical constructor material:

```text
schema = PREV3_OBJECTIVE_WORLD_RELEASE_ROOT_R1
release_authority_ref
repository_ref
publication_bundle_ref
index_manifest_ref
objective_world_scope_ref
valid_time_authority_ref
world_validity_ref
predecessor_world_root_ref | null
```

Identity:

```text
root_id = PREV3WORLD:<semantic_hash(canonical constructor material)>
```

Required consistency checks:

```text
repository_ref.kind == V558_REPOSITORY_BUNDLE
publication_bundle_ref == repository.publication_bundle_ref
index_manifest_ref == repository.index_manifest.ref
release_authority_ref is exact and content-addressed
valid_time_authority_ref is exact and content-addressed
world_validity_ref is a typed concrete objective validity/currentness instance
objective_world_scope_ref is objective-only
predecessor_world_root_ref, when present, is immutable history
```

The root constructor **does not** call M4 resolution and **does not** depend on M5 or V3. That makes the bootstrap DAG acyclic.

## Valid-time law

`world_validity_ref` is not a clock reading. It is the exact objective-world validity/currentness instance whose semantics are authorized by `valid_time_authority_ref`.

The following are insufficient:

- wall clock time;
- a bare timestamp literal;
- `latest`, `default`, or fuzzy selection;
- a study-world/designator string such as `V3_SIM_WORLD_R1`;
- an untyped hash with no competent owner semantics;
- a V3 runtime cursor;
- an actor request.

The world root carries the **objective validity basis**. A runtime cursor is only a downstream **selection coordinate** over that validity. If M5 later uses a `decision_effective_time_ref`, that reference must not be allowed to bootstrap or retroactively authenticate the world root it consumes.

This also preserves the SDTF currentness firewall:

```text
CURRENT(D1' CONSTITUTION)
!= CURRENT(MECHANISM RULE)
!= CURRENT(RULE APPLICATION)
!= CURRENT(CONSEQUENCE FACT)
!= CURRENT(WITNESS/STATE SUPPORT)
```

A world root therefore does not declare every contained fact current. It binds the release and the exact validity/currentness authorities from which per-object decisions remain provable.

## Exact existing reuse

### M4/V557 publication

Reuse `SCR5578_V557_IMMUTABLE_PUBLICATION_BUNDLE@1.0.0`. C02 does not republish producer objects or alter producer permission ceilings.

### M4/V558 repository

Reuse `SCR5578_STRUCTURAL_PRIOR_REPOSITORY@1.0.0` and its mandatory logical indexes:

`OBJECT_IDENTITY`, `TEMPORAL`, `GEOGRAPHIC`, `FINITE_STRATUM`, `GENERATED_POSITION_REQUIREMENT`, `NEGATIVE_LIMIT`, `PROVENANCE`.

The root binds the exact repository and its exact publication/index identities. It does not resolve by mutable alias.

### M4/V558 resolver

Reuse `V558_CONTEXT_RESOLVER_POLICY@1.0.0` with SHA-256 `4e34517b78547ef555c4025abff4f682b6eb201a3dfda2cce2c4ec3bec9b6f2f`.

Context resolution remains exact and fail-closed. The resolver emits selection records and a `V558REC:` receipt; it does not fabricate a `ResolvedStructuralContext`.

### M5

Reuse `M5_STRUCTURAL_CURRENTNESS_RECEIPT@1.0.0` and the M5 RSC materializer only after exact M4 replay. M5 requires both a structural-currentness basis and a decision-effective-time reference. That requirement is downstream evidence binding, not authority to create the world root.

## Objective entity/position ownership

C02 does **not** close GAP-PREV3-014 by assigning all entity/position production to the world root.

For actor-, entity-, relation-, or position-indexed objective context, the query must carry exact refs emitted by the competent objective domain producer. Those refs need provenance and valid time. A demographic coordinate, V3 subject materialization receipt, generated-person state, or person request cannot stand in for an objective position fact.

Thus:

```text
WORLD_ROOT_OWNER != OBJECTIVE_POSITION_PRODUCER
OBJECTIVE_ACTOR_POSITION != PERSON_STATE
```

GAP-PREV3-014 remains a separate owner-allocation problem; C02 proves only that world bootstrap cannot absorb it as a fallback.

## Resolution/replay path

```text
objective producers + objective time authority
        |
        v
V557 immutable publication
        |
        v
V558 immutable repository/indexes
        |
        v
PREV3_OBJECTIVE_WORLD_RELEASE_ROOT_R1
        |
        +--> exact ContextQuery + exact objective bindings
        |         |
        |         v
        |    V558 exact resolver
        |         |
        |         v
        |    V558 resolution receipt
        |         |
        |         v
        |    M5 explicit currentness -> RSC
        |
        +--> historical predecessor roots remain replayable
                  |
                  v
       V3 runtime cursor selects/consumes; never authors root
```

Replay law:

- the same canonical constructor tuple must reproduce the same `PREV3WORLD:` identity;
- a changed repository, scope, world-validity ref, authority ref, or predecessor relation produces a different successor identity;
- old roots are immutable and remain historical replay anchors;
- no global actor reset follows world succession.

## Relation to A3W

A3W correctly proved that it could not lawfully manufacture a world/context receipt from a designator, missing canonical tuple, or missing temporal anchor.

C02 does not overwrite that blocker. It identifies the upstream contract that A3W lacked:

```text
accepted objective world root
+ exact repository/query authority
+ exact objective bindings where required
+ downstream query-time selector when the operation is time-sliced
```

The implementation/population court remains GAP-PREV3-021. C02 authorizes no synthetic first-canary receipt.

## PASS basis

The contract court passes because the dependency direction is now finite and acyclic, exact existing M4/M5 responsibilities are reused without semantic widening, objective valid time is owned upstream of V3, actor/entity/position production is not silently reassigned, and all missing implementation/source/qualification work remains separately named.

### Separate status fields

- **Authority:** bounded candidate returned to Sub-Vozhd II / HQ; no self-adoption.
- **Code body:** not authorized; none modified.
- **Source instance:** not required for this ownership/contract court.
- **Qualification result:** C02 static contract/replay case court PASS only; production materialization, real-data proof, replay execution and independent qualification remain downstream.

## Successor

`GATE-WORLD`

The next lawful successor is the separately commissioned world/root implementation and real-data materialization grain for GAP-PREV3-021, after HQ/Sub-Vozhd II accepts or narrows this candidate.
