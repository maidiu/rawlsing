# B01 frozen household / parent-choice ABI

**Status:** sourcefree `SOURCEFREE_S2_ONLY`; additive B01 base, not a parent decision and not native science.
**Code:** `05a9b988ae039d44c55e636e1c610c01d89b4c1d`.

## P2 bounded material fact

```text
material_fact_source(document) -> sha256 content address
    excludes root, branch, epoch, source

validate_material_fact(document, *, root, branch, world_clock) -> detached document
    refuses psyche-store fields/kinds, missing schema/grade, wrong root/branch,
    invalid epoch/source, bad content address

write_material_fact(session, *, slot, document) -> {
    schema: SOROK_P2_MATERIAL_FACT_WRITE@1, status: WRITTEN|UNCHANGED,
    slot, root, branch, clock, epoch, source, world_hash
}
    slot is bounded to MATERIAL_FACT_SLOTS == {"p6_household"}
    writes through session.product._checkpoint (the actual S47/P2 writer)

P2Owner.material_fact(slot) -> {
    schema: SOROK_P2_MATERIAL_FACT_READ@1,
    slot, root, branch, clock, epoch, source,
    state_hash, world_hash, document
}
    slot is bounded to MATERIAL_FACT_SLOTS
    verifies the session and binds the read to the P2 composite snapshot
```

## P6 household

```text
HOUSEHOLD_SLOT = "p6_household"
HOUSEHOLD_SCHEMA = "SOROK_HOUSEHOLD_MATERIAL@1"
HOUSEHOLD_READ_SCHEMA = "SOROK_HOUSEHOLD_MATERIAL_READ@1"
HOUSEHOLD_GRADE = "SOURCEFREE_FIXTURE"

household_fixture(session) -> content document
establish_household(session, *, fixture=None) -> read document
read_household(session) -> read document
parent_choice_input(session) -> SOROK_PARENT_CHOICE_INPUT@1
```

Stored document fields are exactly:

```text
schema, grade, place, owner, resources, root, branch, epoch, source
```

`place` is exactly `dwelling_id`, `kind`, `rooms`, `tenure`, `tenancy`.
`rooms` must equal `list(house.ROOMS)`.
`tenancy` is exactly `holder_actor_slot`, `landlord_ref`.
`owner` is exactly `actor_slot`, `actor_id`, `authority="household_holder"`;
the actor id must match `world.actor_state[actor_slot]` and the root actor set.
`resources.bindings` is a non-empty bounded list:

```text
{"kind": "WORLD_RESOURCE", "slot": "workshop",
 "fields": ["tool_available", "material"]}
{"kind": "ACTOR_STATE", "actor_slot": "A",
 "fields": ["cash", "material_remaining", "free_hours"]}
```

Only those world-resource/actor slots and scalar field values are admitted in B01.
`read_household` resolves live values and returns:

```text
schema, grade, root, branch, clock, epoch, source, material_hash,
place, owner, resources, world_state_hash
```

`source` identifies the fixture/bindings; `material_hash` identifies the
current resolved values. A changed world value changes `material_hash`,
leaves `source` unchanged, and does not create a second resource value copy.

`parent_choice_input` is read-only and explicitly not a parent act:

```text
first_consumer  = NONE_VERIFIED
parent_decision = NOT_EVALUATED
parent_action   = null
source.owner    = S47_P2_OBJECTIVE_WORLD
source.slot     = p6_household
source.ref      = P6_HOUSEHOLD:<source>
source.hash     = <source>
source.material_hash = <material_hash>
read_boundary   = {psyche_store: NOT_READ,
                   parent_hidden_reason: NOT_READ,
                   model_prose: NOT_READ}
```

## Invariants

- No PsycheStore record is accepted as household material; the writer refuses
  top-level psyche fields and `MEDIATOR`/`TENSION`/`PRACTICE`/`V3MS_*` kinds.
- A world household read requires exact root, branch, epoch, source content
  address, place, owner, tenancy holder and bound resource fields.
- Establishment is one-shot at a given epoch; the same document at the same
  epoch is idempotent, a different document is `P6_HOUSEHOLD_ALREADY_ESTABLISHED`.
  There is no B01 update path.
- Readers are pure: they append no episode, checkpoint, world event or perception.
- No new owner, scheduler, person-world ledger, clock or database.
- Cold same-code reopen is proved; pre-B01 `p2_owner.py` code-pin roots are not
  compatible and need recreation or deliberate migration.
