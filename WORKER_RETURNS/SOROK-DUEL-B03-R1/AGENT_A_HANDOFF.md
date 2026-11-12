# SOROK B03 AGENT A — adversarial construction handoff

**Packet:** B03 `Commit selected inhabited dwelling/tenancy/noise/space/resource facts` (CG-B).
**Depends on:** B01, frozen at B's return `362719b40a35a66fa2fb1c3490db8eb5b8e9167c`.
**Grade:** `SOURCEFREE_S2_ONLY`. No native science, actor/human right, source right, Pyat rule, S14/A5 grant, or protected merge. This is constructive author work, not independent terminal receiving; one independent nonauthor receiving is required per coherent tranche/join.
**Branch:** `codex/sorok-duel-b01-a-relay-b03-20261112-r1`.
**Implementation SHA:** `99333985190d872d825a1ec205db224179daa4af` (final tested tree).
**B03 feature commit:** `6deb7b71d0f8d761ae7734868c693dcb5dd253d8`; final prefix hardening commit: `993339851`.
**Running contract SHA:** `08a323b490df4e2ddd0dca7f8b3cd394dfe17e0a`.
**Protected inspection baseline:** `6a5c12f04323d74001f9632063ec907f4fc4468e`.

## 1. Exact artifact

Code at `99333985190d872d825a1ec205db224179daa4af`:

| Path | Change |
|---|---|
| `WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/house.py` | Added the bounded `p6_dwelling` material facts, `dwelling_fixture`, `establish_dwelling`, `commit_dwelling`, `read_dwelling`, `material_feasibility`, `mother_material_input`; wired `establish_dwelling(session)` into the ordinary `establish` new-house path; added B01 fork provenance to `read_household`/`parent_choice_input`. |
| `WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1/developmental_recursion/p2_owner.py` | Added `p6_dwelling` to `MATERIAL_FACT_SLOTS`; added `_copied_prefix_equal` and integrated it into `branch_is_ancestor` (B01 relay repair). |
| `WORKER_RETURNS/SOROK-DUEL-B03-R1/test_b03_dwelling.py` | 8 B03 positive/negative/changed-value/severance/cold/fork/child-commit tests. |
| `WORKER_RETURNS/SOROK-DUEL-B01-R1/test_b01_fork_provenance.py` | 4 B01 fork provenance/epoch/prefix/action tests. |

Return files: this handoff, `PROGRAMMA_DELTA.json`, `impact.json`, `B03_ABI.md`, `00_RETURN.md`, `evidence/`.

Commands (qualified environment):

```text
/private/tmp/rawlsing-oct28-p1r1/venv/bin/python -B -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-DUEL-B03-R1/test_b03_dwelling.py
/private/tmp/rawlsing-oct28-p1r1/venv/bin/python -B -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-DUEL-B01-R1/test_b01_household.py \
  WORKER_RETURNS/SOROK-DUEL-B01-R1/test_b01_fork_provenance.py
/private/tmp/rawlsing-oct28-p1r1/venv/bin/python -B -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/test_house.py
/private/tmp/rawlsing-oct28-p1r1/venv/bin/python -B -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/test_mii.py
/private/tmp/rawlsing-oct28-p1r1/venv/bin/python -B -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1/tests/test_p2_owner.py \
  WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/test_actor_scene_context.py \
  WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests/test_p3_owner.py::test_process_reopens_same_actual_p2_root \
  WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests/test_p3_owner.py::test_actual_p2_root_configuration_and_combined_statehash
```

## 2. Governing contract

B03 must commit selected inhabited dwelling, tenancy, noise/acoustics, space and resource facts through the existing P2 world writer and a bounded P6 material/house adapter; a concrete drum-kit availability must depend on those committed conditions, with legitimate refusal/unknowns. The negative is house description treated as psyche, social class directly creating a trait, or an impossible object appearing. Reopening the root must give exact housed facts and legitimate unknowns. Producer owner: `P2 world + bounded P6 material/house adapter`; terminal consumer: `later material feasibility reader and mother decision candidate`; PW-02/PW-09; `SOURCEFREE_S2_ONLY`.

The frozen programme sources remain binding: `20261111_ROLLING_PERSON_WORLD_DURATION_MATERIAL_MEDIATION_R1.md`, `32_ROLLING_PERSON_WORLD_OWNER_RECONCILIATION_20261111_R1.md` (PW-02 `EXTEND_SELECTED_WORLD_OWNER`, PW-09 consequential ordinary activity), the 27-task programme and relay contract. The two complete ChatGPT Library architecture records remain **NOT_INSPECTED locally**; their identities and that limitation are preserved. No contents are claimed.

B03 keeps B01/B02/B04 boundaries: no new calendar/as-of (B02), no purchase/action/admission (B04), no multicycle duration (B05), no mother decision/utterance (C03/C04). The mother decision candidate is represented only by `mother_material_input` with `first_consumer=NONE_VERIFIED`.

## 3. Strongest achieved result

One ordinary P6 `new` now establishes `p6_household` (B01) and `p6_dwelling` through the same actual S47/P2 checkpoint writer:

```text
p6_dwelling schema  SOROK_DWELLING_MATERIAL@1
grade               SOURCEFREE_FIXTURE
home                dwelling_id, kind, rooms, tenure,
                    tenancy {holder_actor_slot, landlord_ref,
                             instrument_policy, lease_constraints}
space               usable_room, floor_area_m2, clearance_m2, ceiling_height_m
acoustics           wall_construction, sound_rating_db, max_indoor_loudness_db,
                    neighbor_shared_walls, quiet_hours
costs               monthly_rent, rent_due_now, currency_unit
binding             exact root, branch, epoch, source content address
```

`read_dwelling` verifies the exact stored field set, source, root/branch/epoch, home/tenancy/space/acoustics/costs schema, the B01 household place/owner/landlord and the P6 room set. It exposes `source`, `material_hash`, `household_source`, `household_material_hash`, `world_state_hash`, and a `provenance` object (`stored_branch`, `current_branch`, `inherited`, `scope=P6_MATERIAL_FACT_ONLY`, `fork_state`). It is a pure reader; it appends no checkpoint, episode, world event or perception.

`material_feasibility(session, request)` is the actual material first consumer. It evaluates a concrete request against committed conditions and live household resources:

- default acoustic kit `{2.4 m^2, 95 dB, 180 units}` -> `REFUSED`, reasons `REFUSED_NOISE`, `REFUSED_AFFORDABILITY`;
- junior kit `{1.2 m^2, 70 dB, 40 units}` -> `ADMISSIBLE`;
- committed `instrument_policy=prohibited` -> `REFUSED_TENANCY`;
- committed tight space -> `REFUSED_SPACE`;
- committed `max_indoor_loudness_db=UNKNOWN` -> `UNKNOWN` / `UNKNOWN_ACOUSTICS`, never `NO_CHANGE`;
- live actor cash 55 -> 30 flips junior to `REFUSED_AFFORDABILITY`; restore returns exact baseline;
- `conditions` carries the quiet-hours policy; `possession_created=false`; `material_reader=house.material_feasibility`; `mother_decision=NOT_EVALUATED`; `parent_action=null`.

`mother_material_input(session, request)` freezes the later mother-decision material input: the dwelling, household, feasibility, request, `first_consumer=NONE_VERIFIED`, `mother_decision=NOT_EVALUATED`, `parent_action=null`, `possession_created=false`. No mother act, utterance, hidden reason, trait, class label or drum-kit object is created.

B01 relay repair preserved: B's read-only C12 ancestor provenance is kept; `read_household`/`parent_choice_input` now label inherited material-only provenance; `branch_is_ancestor` verifies the actual copied C12 prefix rows, not mutable `root_counts`. The full P6 house/MII suites remain green.

Evidence (all in this worktree):

- B03 suite **8 passed in 46.01s** (`evidence/b03_dwelling.log`);
- B01 suite + A fork provenance **11 passed in 74.88s** (`WORKER_RETURNS/SOROK-DUEL-B01-R1/evidence/a_relay_b01.log`);
- B01+B03 combined **19 passed in 113.82s** (`evidence/b01_b03_relay.log`);
- full P6 `test_house.py` **8 passed in 158.53s** (`evidence/p6_test_house.log`);
- full P6 `test_mii.py` **18 passed in 226.44s** (`evidence/p6_test_mii.log`);
- P2 owner + actor scene + selected P3 reopen/config **9 passed in 50.92s** (`evidence/adjacent.log`);
- pre-existing P6 chronology proof **1 failed** on `mii_exposure_id`/`mii`, unchanged from baseline `6a5c12f` (`evidence/p6_chronology_pre_existing.log`).

## 4. Own hostile findings

1. **The dwelling is constrained to the B01 home identity.** `read_dwelling` cross-checks `dwelling_id`, `kind`, room set, tenure, holder and landlord against `p6_household`. B03 can commit tenancy/noise/space/cost changes but cannot represent a different home/occupancy on a child fork without a future household re-establishment ABI. This is disclosed, not hidden.
2. **Child fork can commit its own material facts.** `commit_dwelling` on a child writes a child-owned `p6_dwelling` source and leaves the parent branch's dwelling unchanged (tested). The inherited `p6_household` remains parent-owned. A consumer must read both provenances; they can differ.
3. **`sound_rating_db`, `wall_construction`, `neighbor_shared_walls` and `monthly_rent` are committed/read but not used by the bounded feasibility rule.** The rule uses `max_indoor_loudness_db`, space/clearance, rent due and live cash. This is a material-context boundary, not an acoustic propagation or economic model.
4. **`mother_material_input` reads the dwelling/household twice** (once directly, once through `material_feasibility`). Under the P6 command lock this is consistent; a future concurrent multi-writer consumer should either hold one read snapshot or accept the hash cross-check. The test asserts the nested sources match.
5. **Three same-clock checkpoints at establishment** (`p6_house`, household, dwelling) remain. It is one coherent world state, not one atomic multi-writer transaction. B04/E03 own crash-atomic composite commit/recovery.
6. **P3 code-pin cost.** `p2_owner.py` is hashed into `P3Owner._code_pins()`; this cut invalidates P3 roots from A's `edbb4b344`, B's `160cbbd0a`/`362719b40`, and earlier B01 cuts. Fresh roots at this final code reopen and cold-test exactly. No migration or pin weakening was performed; P3 migration is Pair2/shared-receiving scope.
7. **Ancestor provenance relabel remains possible.** The source excludes `branch`; changing the stored branch to another verified ancestor preserves the source and is accepted. The material content is unchanged, but the provenance label could be misattributed. A checkpoint-history binding is not added.
8. **My initial B03 test draft failed on a quoted-word assertion (`class_to_trait`/`psyche_store` marker strings) and on reading the parent C12 state path (`["world"]["resources"]`); I repaired the tests, not the production contract.** Production behavior was not weakened to make them pass.

## 5. Unresolved challenges

- **Mother decision/utterance:** not built. `mother_material_input` is material input only; C03/C04 own the parent choice, performed utterance and Nadia-qualified uptake.
- **B02/B04/B05 and J1/J2:** not implemented. No historical calendar/as-of, no purchase/action/admission, no recurring costs/debits/refusals, no multicycle duration.
- **Child new occupancy:** different dwelling/room/owner/landlord on a fork is refused by the B01 household cross-check; requires a future household re-establishment ABI.
- **Tenure scope:** the B03 fixture is a rented two-room home. Owned/other tenure, vacant lease constraints or a different home identity are not implemented; the household place/tenure cross-check is deliberate.
- **Scene scope:** B03 is established only in the ordinary P6 house scene. The gallery/symbolic presentation fixtures have no `p6_dwelling`; `read_dwelling`/`material_feasibility` refuse there. This is a bounded actual-house fixture, not a universal scene importer.
- **Same-root PsycheStore negative:** not proved; the structural no-import guard and world-first readers are the protection. A valid mediator injected into the actual `p3_psyche.sqlite3` is a remaining attack.
- **Cold fork:** in-process verified-owner fork reads/actions are proved; full cold `run_p6.experience` on a fork is blocked by P2/P3 branch binding and not claimed.
- **P3 pin migration:** not solved; out of this lease.
- **Ancestor relabel / checkpoint-history provenance:** not solved.
- **Cost:** UNKNOWN; no controller/provider token, latency, RSS or retry instrumentation was available or invented.
- **Full estate:** not run. Only the bounded B01/B03/P6/adjacent suites were executed.
- **Native/science/rights/human/merge:** held. Two Library architecture records remain NOT_INSPECTED locally.

## 6. Likely attack surfaces for SAME B

1. **Rule completeness:** try a request whose numeric conditions pass but which is materially impossible in the P6 room; try class/tenure words as if they were traits; try an unknown `clearance_m2`, currency, rent or wall rating. The reader must refuse/UNKNOWN, never create a possession or a psychological state.
2. **Cross-resource consistency:** commit a dwelling whose home identity differs from `p6_household`; the cross-check should refuse. Try a child-owned dwelling with an inherited household; verify both provenances and parent isolation.
3. **Child new occupancy:** define or reject a household re-establishment ABI. Do not silently widen the dwelling cross-check.
4. **Bound resources:** remove `workshop`/actor `A`/cash; change owner id; the household or dwelling reader must refuse or return a legitimate unknown, not a fabricated verdict.
5. **Fork provenance:** relabel the stored branch to another verified ancestor; tamper `root_counts` plus a copied prefix row; create a grandchild/sibling/post-fork checkpoint. Our actual-row prefix check and provenance marker should be attacked.
6. **Cold/restore:** reopen at a different clock; commit a dwelling after time advances; restore exact baseline. The cold test is same-clock and subprocess; a later-clock commit is a source change, not a byte-exact restore.
7. **Mother input:** make `mother_material_input` look like a mother action or a trait; the frozen markers must stay `NONE_VERIFIED`/`NOT_EVALUATED`/`null` and no event/possession may be written.
8. **P3 pin:** do not weaken code pins or rewrite accepted state. Prove the old/new boundary and keep fresh fixture roots at the final coherent code.

**Hardest concrete challenge for SAME B:** bind the stored establishment branch to the actual C12 checkpoint history so an ancestor relabel is refused, while preserving read-only fork inheritance and the material-only `state_scope`; then prove the same-root PsycheStore negative and a child new-occupancy boundary without inventing a second household ledger.

## 7. Rejected alternatives

- **Write the dwelling as a PsycheStore record or a class/tenure psychology.** Rejected: house/material facts are world-owned; PsycheStore is actor-scoped. Extra `social_class`/`trait` fields are refused.
- **Create a new household/dwelling owner, simulator or ledger.** Rejected: reuse B01/P2/P6; the dwelling is one `world.resources` entry through the existing checkpoint writer.
- **Put the drum kit into `p6_house` objects when admissible.** Rejected: an availability verdict is not a possession; a purchase/action is B04. The test proves the kit never appears in the house/objects.
- **Let `material_feasibility` perform a purchase, debit or mother act.** Rejected: B04/C03 own that; B03 returns a material verdict/input only.
- **Use a social-class label to infer a trait or drum-kit availability.** Rejected: the ABI has no class field; extra fields are refused; the rule uses material space/acoustics/tenancy/cost facts.
- **Copy live resource values into the dwelling document.** Rejected: duplicates B01/world state; the dwelling holds committed conditions plus the household cross-link, and affordability reads live household cash.
- **Claim old P3 roots compatible.** Rejected: the p2_owner byte change invalidates them; no migration was invented.
- **Claim fork-only state is full P3 composite.** Rejected: `provenance.fork_state` and `state_scope` explicitly say `C12_FORK_WITHOUT_S46_INTERVAL_STATE`; the scope is material-only.

## 8. Proof boundaries

Do not claim any of the following from this return:

- Native SOROK CAN/ADP/Pyat N9/N10E/N10W science, actor rights, human validity, source/use rights, or protected merge.
- A mother decision, performed utterance, hidden reason, trait, or mother first consumer. `first_consumer=NONE_VERIFIED`, `mother_decision=NOT_EVALUATED`.
- B04 purchase/action, B02 calendar/as-of, B05 multicycle duration, J1/J2, or J3.
- A new household/dwelling simulator, economy, market, or duplicate ledger.
- Owned/other tenure or a different home identity; B03 is a rented two-room fixture and cross-checks the B01 household place/tenure.
- A possession created by feasibility; `possession_created=false` and the house objects are unchanged.
- An acoustic propagation model; the bounded rule uses declared max loudness/space/cost facts and commits the rest as context.
- Crash-atomic composite establishment, concurrent-writer safety, or exactly-once material retry.
- Cold fork/full P6 experience on a fork; only in-process verified-owner fork reads/actions are proved.
- P3 old-root compatibility or a pin migration.
- Ancestor-relabel-proof provenance; that remains an attack surface.
- The pre-existing P6 chronology proof as green.
- Full-estate or whole-programme coverage.
- The two Library architecture records' contents; they remain NOT_INSPECTED locally.

## Measured cost and limits

Executed suites: 8 B03 + 11 B01 + 8 P6 house + 18 P6 MII + 9 adjacent; combined B01+B03 19 passed. The pre-existing chronology proof still fails on MII exposure sequencing at both baseline and this cut. Controller/provider token, latency, process RSS, retry and USD cost: **UNKNOWN**. Hard limits: `SOURCEFREE_S2_ONLY`, same-code cold boundary, material-only fork scope, one bounded actual P6 house fixture, no parent consumer, no native/science/rights authority, no protected merge.
