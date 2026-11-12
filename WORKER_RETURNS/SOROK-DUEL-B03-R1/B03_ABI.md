# B03 frozen dwelling / feasibility / mother-input ABI

**Status:** sourcefree `SOURCEFREE_S2_ONLY`; B01-dependent bounded material construction. Not a purchase, mother decision, native science, or protected merge.
**Code:** `99333985190d872d825a1ec205db224179daa4af`.

## World resource

```text
DWELLING_SLOT = "p6_dwelling"
DWELLING_SCHEMA = "SOROK_DWELLING_MATERIAL@1"
DWELLING_READ_SCHEMA = "SOROK_DWELLING_MATERIAL_READ@1"
DWELLING_GRADE = "SOURCEFREE_FIXTURE"
```

The stored document is written through `p2_owner.write_material_fact`, the same
S47/P2 `session.product._checkpoint` path as B01. Its fields are exactly:

```text
schema, grade, home, space, acoustics, costs, root, branch, epoch, source
```

`home` is exactly `dwelling_id`, `kind`, `rooms`, `tenure`, `tenancy`.
`tenancy` is exactly `holder_actor_slot`, `landlord_ref`, `instrument_policy`,
`lease_constraints`.
`space` is exactly `usable_room`, `floor_area_m2`, `clearance_m2`,
`ceiling_height_m`.
`acoustics` is exactly `wall_construction`, `sound_rating_db`,
`max_indoor_loudness_db`, `neighbor_shared_walls`, `quiet_hours`.
`costs` is exactly `monthly_rent`, `rent_due_now`, `currency_unit`.
`source` is the content address excluding root/branch/epoch/source.

`home` must be consistent with the B01 `p6_household` place/owner/landlord and
the actual P6 room set. B03 commits tenancy/noise/space/cost changes; a different
home identity requires a future household re-establishment ABI. The B03 fixture
is a rented two-room home; owned/other tenure and an empty lease-constraint set
are not implemented.

## Writer / readers

```text
dwelling_fixture(session) -> content document
establish_dwelling(session, *, facts=None) -> read document   # one-shot
commit_dwelling(session, *, facts=None) -> read document      # selected facts
read_dwelling(session) -> DWELLING_READ schema
material_feasibility(session, request=None) -> MATERIAL_FEASIBILITY schema
mother_material_input(session, request=None) -> MOTHER_MATERIAL_INPUT schema
```

`commit_dwelling` writes a new `p6_dwelling` source at the current sourcefree
clock; it does not debit, purchase, mutate `p6_house` objects, or create a
second ledger. On a child fork it writes a child-owned dwelling and leaves the
parent branch unchanged; the inherited B01 household remains parent-owned.

## Provenance

`read_dwelling` and the B01 `read_household` expose:

```text
provenance = {
  stored_branch, current_branch, inherited,
  scope = "P6_MATERIAL_FACT_ONLY",
  fork_state = "CURRENT_BRANCH" | "C12_FORK_WITHOUT_S46_INTERVAL_STATE"
}
```

Fork reads are material/C12-scoped, not full P3 composite state. The actual
establishment branch is preserved in the stored document; the read current
branch is the session branch. `branch_is_ancestor` verifies the actual copied
C12 prefix rows for each fork edge (episode/world event/checkpoint/perception),
not mutable `root_counts` metadata.

## Concrete request and feasibility

```text
DRUM_KIT_REQUEST_SCHEMA = "SOROK_DRUM_KIT_REQUEST@1"
fields: schema, grade, request_id, kind, setup,
        footprint_m2, loudness_db, purchase_price, currency_unit
```

`DRUM_KIT_REQUESTS["acoustic"]` = 2.4 m^2, 95 dB, 180 units.
`DRUM_KIT_REQUESTS["junior"]` = 1.2 m^2, 70 dB, 40 units.

Bounded rule order:

1. tenancy `prohibited` -> `REFUSED_TENANCY`; `UNKNOWN` -> `UNKNOWN_TENANCY_POLICY`;
2. `loudness_db > max_indoor_loudness_db` -> `REFUSED_NOISE`; max unknown -> `UNKNOWN_ACOUSTICS`;
3. `footprint_m2 > floor_area_m2 - clearance_m2` -> `REFUSED_SPACE`; area/clearance unknown -> `UNKNOWN_SPACE`;
4. currency mismatch -> `UNKNOWN_CURRENCY`; cash or rent unknown -> `UNKNOWN_AFFORDABILITY`; price > live cash - rent due -> `REFUSED_AFFORDABILITY`.

Status is `REFUSED` if any reasons, else `UNKNOWN` if any unknowns, else
`ADMISSIBLE`. Quiet hours are a condition, not a refusal by themselves. The
result carries `material_reader=house.material_feasibility`,
`possession_created=false`, `mother_decision=NOT_EVALUATED`, `parent_action=null`.

`mother_material_input` is the frozen later-mother material input:
`first_consumer=NONE_VERIFIED`, `mother_decision=NOT_EVALUATED`,
`parent_action=null`, `possession_created=false`, with the dwelling, household,
feasibility and request. No mother action, utterance, trait, class label or
drum-kit object is created.

## Invariants

- No PsycheStore record is a dwelling fact; no class/social label creates a trait.
- No drum kit becomes a possession or a `p6_house` object; feasibility is not purchase.
- Readers are pure: no episode, checkpoint, world event or perception on read.
- Legacy P3 roots created under a different `p2_owner.py` byte cut are incompatible
  with this final code; fresh sourcefree roots are required. P3 migration is not
  part of B03.
- Fork reads use material/C12 provenance only; do not describe them as full P3
  composite state or compare the scoped hash to a full P3 identity.
