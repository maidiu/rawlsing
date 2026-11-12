# SOROK B01 AGENT A RELAY — counterstrike and B03 handoff

**Packet:** B01 counterstrike, then the same pair's B03 bounded construction.
**Grade:** `SOURCEFREE_S2_ONLY`. No native science, actor/human right, source right, Pyat rule, S14/A5 grant, or protected merge. This is constructive author work, not independent terminal receiving.
**Frozen B return:** `362719b40a35a66fa2fb1c3490db8eb5b8e9167c`.
**B implementation:** `160cbbd0ae00fb965004085c0e07c872384fe0ff`.
**A relay branch:** `codex/sorok-duel-b01-a-relay-b03-20261112-r1`.
**A relay code SHA:** `6deb7b71d0f8d761ae7734868c693dcb5dd253d8`.
**Running contract SHA:** `08a323b490df4e2ddd0dca7f8b3cd394dfe17e0a`.
**Protected inspection baseline:** `6a5c12f04323d74001f9632063ec907f4fc4468e`.

## 1. B's valid findings and improvements, explicitly acknowledged

1. **The fork refusal was real and consequential.** At A's `edbb4b344`, `house.read_household`, `house.read_house` and `P2Owner.material_fact` compared the stored establishment branch to the current child branch and/or called full `Session.verify()`; a legitimate C12 fork copied the world/checkpoint rows but not S46/S47 interval state, so those readers refused a copied house/household. I inspected A's code and B's `evidence/a_head_fork_refusal.log`; B's description is accurate. B's read-only ancestor provenance is the correct direction: the copied document keeps its establishment branch and the read reports the current branch without rebinding or writing.
2. **B's `state_scope` is honest and necessary.** `P2Owner.material_fact` on an ancestor does not pretend the S46 interval state exists; it reports `C12_FORK_WITHOUT_S46_INTERVAL_STATE`. I preserved that exact limitation and propagated it to the P6 consumer.
3. **B's added tests close real A evidence gaps.** A's handoff claimed bound-resource/owner severance but did not directly test removing `workshop`/actor `A` or changing the owner id. B's tests do. A's world-value change test covered actor `cash`; B's covers `workshop.material`.
4. **B did not weaken P6 semantics.** The full P6 `test_house.py` and `test_mii.py` suites remain green. B's disclosure of the P3 code-pin break is correct and important.

## 2. B's invalid or incomplete findings

### 2.1 Incomplete: shared-prefix validation still trusted mutable branch metadata

B's `branch_is_ancestor` calls `inherits_verified_prefix`, which delegates to `shared_root_equal`. For parent/child branches, that method compares only `root_counts` rows copied into the child. `root_counts` lives in the mutable `branch` table and is not covered by `_lineage_result`'s checks (which compare parent/fork clock/root hash/created clock, not counts). I demonstrated on B's exact code that:

```text
UPDATE branch SET root_counts='{}' WHERE branch_id='child';
```

leaves `read_household` and `P2Owner.material_fact` succeeding. If a copied prefix row is then corrupted, B's prefix check inspects zero rows and passes; only the later `c12_verify` on the `P2Owner` ancestor path might catch it, and `house.read_household` does not call `c12_verify` at all. This is a real hole in the claimed shared-prefix/provenance guarantee.

**Repair:** added `_copied_prefix_equal` in `p2_owner.py`, called for every parent edge in `branch_is_ancestor`. It compares the actual copied rows `(seq, hash)` for `episode`, `world_event`, `checkpoint` and `(seq, event_id, actor_id)` for `perception`, against the parent rows with `clock <= fork_clock`. It ignores mutable `root_counts`; a hostile `root_counts={}` no longer disables the check. Test: `test_actual_copied_prefix_not_mutable_root_counts`.

### 2.2 Incomplete: fork provenance was exposed only at `P2Owner.material_fact`, not the actual P6 consumer

On a child fork, `read_household` returned `branch="child"` with `source` from the parent, and `parent_choice_input` returned the child branch with no indication that the fact was inherited or that S46 interval state was absent. A consumer could treat that as a child-owned/full composite read. B's own P6 event test also notes that child P6 event bodies retain parent house provenance; B disclosed the widening but did not surface it in the parent input.

**Repair:** `read_household` and `parent_choice_input` now carry an additive `provenance` object:

```text
stored_branch, current_branch, inherited,
scope = "P6_MATERIAL_FACT_ONLY",
fork_state = "CURRENT_BRANCH" | "C12_FORK_WITHOUT_S46_INTERVAL_STATE"
```

`parent_choice_input.source` also carries `stored_branch`, `inherited`, `fork_state`. This is not a full P3 composite claim and not a rebind; it explicitly labels material-only scope. Tests: `test_fork_provenance_is_explicit_and_not_full_composite`.

### 2.3 Incomplete: post-fork clock boundary was not tested at the actual consumer

B's test forks and reads, but does not establish a fact with an epoch after the child fork clock and then attempt to read it on the child. I added `test_fact_after_fork_clock_is_refused_and_restored`: a stored household epoch later than the child's fork clock is refused by both `read_household` and `P2Owner.material_fact`, then restored. This confirms the epoch boundary is enforced at the actual P6 consumer, not only in B's helper.

### 2.4 Not a defect: the fork `state_hash` is scoped, and B did not claim otherwise

B labels the ancestor `state_hash` with `state_scope=C12_FORK_WITHOUT_S46_INTERVAL_STATE`. I did not find B claiming it is a full P3 composite hash. A consumer must not compare it to a full P3 identity; the P6 provenance marker now makes that boundary explicit.

### 2.5 Not a defect: child P6 event bodies retain parent house provenance

A child `GO` is stored on the child branch, while the event body's `branch` field is the parent `p6_house` provenance because `encounter.movement_evidence` binds house provenance separately from the session branch. I tested both facts: the event is stored on the child branch; it is absent from the parent branch; `body.branch` is the parent house provenance. This is a documented provenance boundary, not a rewrite. Test: `test_child_p6_action_is_stored_on_child_with_parent_house_provenance`.

## 3. New defects discovered independently

1. The mutable `root_counts` prefix bypass in B's fork repair (above).
2. The fork provenance/scope gap at `read_household` and `parent_choice_input` (above).
3. The child-fork **new occupancy** boundary: B's read-only inheritance is right for copied facts, but `establish_household` remains one-shot, so a child cannot represent a genuinely new home/tenure identity. B03 demonstrates that a child can commit its own **tenancy/noise/space/cost** facts while keeping the inherited `p6_household` home identity; a different `dwelling_id`/room set/owner/landlord still requires a future household re-establishment ABI. I did not fake that boundary.
4. Provenance relabel remains possible between verified ancestors: because `material_fact_source` excludes `branch`, changing a stored household branch from the establishment ancestor to another verified ancestor keeps the source valid and is accepted by `branch_is_ancestor`. The material content is unchanged, but the stored provenance label could be misattributed. I did not add a checkpoint-history provenance ledger in this round; this remains an attack surface.
5. The B03 acoustic/material rule uses the committed `max_indoor_loudness_db`, space and rent/cash facts. `sound_rating_db`, `wall_construction`, `neighbor_shared_walls` and `monthly_rent` are committed and read, but are not used in the bounded feasibility verdict; a later consumer may use them. This is a declared rule boundary, not a claim of an acoustic propagation model.

## 4. Repairs implemented and demonstrated effects

### 4.1 B01 C12 provenance

- `p2_owner.py`: added `_copied_prefix_equal` and integrated it into `branch_is_ancestor`; added `p6_dwelling` to `MATERIAL_FACT_SLOTS`. No constructor/validate/realize/participant change.
- `house.py`: added `provenance` to `read_household` and `parent_choice_input`; added `stored_branch`/`inherited`/`fork_state` to the parent input source.
- Tests: `test_b01_fork_provenance.py` (4 tests): grandchild provenance, post-fork epoch refusal/restore, mutable `root_counts` + prefix corruption refusal/restore, child event storage/provenance.

### 4.2 B03 bounded dwelling/tenancy/noise/space/resource construction

New `p6_dwelling` material fact written through the **same** `p2_owner.write_material_fact` -> `session.product._checkpoint` path:

```text
schema  SOROK_DWELLING_MATERIAL@1
grade   SOURCEFREE_FIXTURE
home    dwelling_id, kind, rooms, tenure, tenancy {holder_actor_slot,
        landlord_ref, instrument_policy, lease_constraints}
space   usable_room, floor_area_m2, clearance_m2, ceiling_height_m
acoustics wall_construction, sound_rating_db, max_indoor_loudness_db,
        neighbor_shared_walls, quiet_hours
costs   monthly_rent, rent_due_now, currency_unit
root/branch/epoch/source content-addressed
```

It cross-checks the B01 household place/owner/landlord and P6 room set. `read_dwelling` is the actual material reader; it accepts only verified C12 ancestor provenance on forks and reports `provenance.stored_branch/current_branch/inherited/fork_state`.

`material_feasibility(session, request)` evaluates a concrete drum-kit request against committed facts:

- default acoustic kit (`2.4 m^2`, 95 dB, 180 units) -> `REFUSED` with `REFUSED_NOISE`, `REFUSED_AFFORDABILITY`;
- junior kit (`1.2 m^2`, 70 dB, 40 units) -> `ADMISSIBLE`;
- committed prohibited tenancy -> `REFUSED_TENANCY`;
- committed tight space -> `REFUSED_SPACE`;
- committed unknown acoustics -> `UNKNOWN` / `UNKNOWN_ACOUSTICS`, never `NO_CHANGE`;
- changed live actor cash 55 -> 30 flips junior from `ADMISSIBLE` to `REFUSED_AFFORDABILITY`; restore returns exact baseline.

`mother_material_input` is the frozen input for the later mother decision candidate: `first_consumer=NONE_VERIFIED`, `mother_decision=NOT_EVALUATED`, `parent_action=null`, `possession_created=false`, `material_reader=house.material_feasibility`. No mother act, utterance, trait, class label or drum-kit object is created. Tests: `test_b03_dwelling.py` (8 tests), including class/trait extra-field refusal, unknown facts, severance/restore/cold subprocess, fork provenance, and child-owned tenancy commit without parent mutation.

## 5. Regressions and negative controls tested

| Command | Result | Evidence |
|---|---|---|
| B01 suite + A fork-provenance suite | **11 passed in 71.14s** | `WORKER_RETURNS/SOROK-DUEL-B01-R1/evidence/a_relay_b01.log` |
| B03 suite | **8 passed in 41.89s** | `WORKER_RETURNS/SOROK-DUEL-B03-R1/evidence/b03_dwelling.log` |
| B01 + B03 combined | **19 passed in 115.63s** | `WORKER_RETURNS/SOROK-DUEL-B03-R1/evidence/b01_b03_relay.log` |
| Full P6 `test_house.py` | **8 passed in 154.83s** | `WORKER_RETURNS/SOROK-DUEL-B03-R1/evidence/p6_test_house.log` |
| Full P6 `test_mii.py` | **18 passed in 226.76s** | `WORKER_RETURNS/SOROK-DUEL-B03-R1/evidence/p6_test_mii.log` |
| P2 owner + actor scene + selected P3 reopen/config | **9 passed in 44.00s** | `WORKER_RETURNS/SOROK-DUEL-B03-R1/evidence/adjacent.log` |
| Pre-existing P6 chronology proof | **1 failed** on `mii_exposure_id`/`mii`; same failure at baseline `6a5c12f` and on this branch | `WORKER_RETURNS/SOROK-DUEL-B03-R1/evidence/p6_chronology_pre_existing.log` |

Negative controls exercised: PsycheStore kitchen `MEDIATOR` and test-local `later_decision` ignored/refused; material writer refuses psyche records/foreign root/source/epoch; foreign branch and post-fork epoch refused; mutable `root_counts` plus prefix mismatch refused; extra `social_class`/`trait`/bad policy refused; no possession, no mother action, no psyche read; cold subprocess identical with unchanged counts.

## 6. Requirements still unfulfilled

- **Parent/mother first consumer:** `NONE_VERIFIED`. C03/C04 must bind the parent decision, performed utterance and qualified uptake. `mother_material_input` is only the material input.
- **B02 historical calendar/as-of, B04 purchase/action, B05 multicycle duration, J1/J2:** not implemented. B03's feasibility is not a purchase, action, or home-period/calendar.
- **P3 code-pin migration:** any P3 root created under A's `edbb4b344`, B's `160cbbd0a`/`362719b40`, or an earlier p2_owner byte cut will refuse cold reopen under the final code. Fresh sourcefree fixtures are created and tested at the final code. P3 migration is Pair2/shared-receiving scope; no migration, pin weakening or accepted-state rewrite was performed.
- **Partial-fork state scope:** fork-only reads are material/C12-scoped; they are not full P3 composite state and the `state_scope`/`provenance.fork_state` must be preserved by consumers. Cold fork/full `run_p6.experience` on a fork is not proved; P2/P3 branch binding remains outside B01.
- **Same-root PsycheStore negative:** A's runtime negative used a separate store; B noted the gap. The structural no-import guard and world-first readers are the substantive protection. A same-root injected mediator test remains unproved.
- **Child new occupancy:** B03 child commits can change tenancy/noise/space/cost facts but must keep the inherited home identity; a different dwelling/room/owner/landlord needs a future household re-establishment ABI.
- **Ancestor provenance relabel:** changing the stored branch to another verified ancestor keeps the content source valid; no checkpoint-history provenance verifier is added.
- **Acoustic rule scope:** `max_indoor_loudness_db`, space and affordability are the B03 decision facts; wall rating/construction/neighbor count/monthly rent are committed context, not a propagation/economic model.
- **Native/science/rights/human/merge:** held. Two ChatGPT Library architecture records remain NOT_INSPECTED locally; no contents claimed.
- **Cost:** UNKNOWN. No controller/provider token, latency, RSS or retry instrumentation was available or invented.
- **Full estate:** not run. The listed bounded suites are the evidence.

## 7. Exact artifact and execution receipts

Changed code at `6deb7b71d0f8d761ae7734868c693dcb5dd253d8`:

| Path | Change |
|---|---|
| `WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1/developmental_recursion/p2_owner.py` | `p6_dwelling` material-fact slot; `_copied_prefix_equal`; `branch_is_ancestor` now verifies actual copied prefix rows. |
| `WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/house.py` | B01 fork provenance at the P6 consumer; B03 dwelling writer/reader/feasibility/mother input and `establish` wiring. |
| `WORKER_RETURNS/SOROK-DUEL-B01-R1/test_b01_fork_provenance.py` | 4 fork-provenance/attack tests. |
| `WORKER_RETURNS/SOROK-DUEL-B03-R1/test_b03_dwelling.py` | 8 B03 material/negative/restore/cold/fork tests. |

Commands used the qualified environment:

```text
/private/tmp/rawlsing-oct28-p1r1/venv/bin/python -B -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-DUEL-B01-R1/test_b01_household.py \
  WORKER_RETURNS/SOROK-DUEL-B01-R1/test_b01_fork_provenance.py
/private/tmp/rawlsing-oct28-p1r1/venv/bin/python -B -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-DUEL-B03-R1/test_b03_dwelling.py
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

The B03 return directory carries its own `AGENT_A_HANDOFF.md`, `PROGRAMMA_DELTA.json`, `impact.json`, `B03_ABI.md` and evidence logs.

## 8. Strongest remaining attack surfaces for SAME B

1. **Ancestor provenance relabel.** Change the stored household/dwelling `branch` to a different verified ancestor without changing `source`; does the consumer detect the false provenance? The current answer is no. A checkpoint-history provenance binding or source inclusion of the establishment branch would be a genuine repair; do not fake it with another root-count check.
2. **Same-root PsycheStore injection.** Inject a valid `MEDIATOR` into the actual P6 root's `p3_psyche.sqlite3` and prove `read_household`/`read_dwelling`/`material_feasibility` ignore it; then sever the world fact and prove refusal while the PsycheStore decision remains. This is the strongest remaining negative.
3. **Child new occupancy.** Make a child fork with a different `dwelling_id`/room set/owner/landlord while preserving the B01 household identity; the current B03 cross-check refuses. If this is legitimate, define the minimal household re-establishment ABI and its provenance; if not, prove the refusal is correct.
4. **Cold fork.** Reopen the child branch in a fresh process and read the household/dwelling/feasibility. The in-process fork proof is not cold; P2/P3 branch binding currently blocks full `run_p6.experience` on a fork.
5. **Prefix verification cost/robustness.** `_copied_prefix_equal` reads the actual rows per fork edge. Attack it with a grandchild, a sibling, a post-fork child checkpoint, a corrupted perception row, and a forged lineage meta/branch row. Confirm the exact refusal and restoration.
6. **B03 rule boundary.** Try to make a class/tenure label directly create a trait or a possession; try a request that is admissible under the numeric rule but impossible in the P6 house; try an unknown `clearance_m2`/currency/rent. The current reader should refuse/UNKNOWN, never create an object or a psychological state.
7. **P3 pin migration.** Do not solve it by weakening code pins. If a migration is genuinely required, it belongs to the P3/Pair2 receiving scope; prove the old/new root boundary and keep fresh fixture roots at the final code.

**Hardest concrete challenge for SAME B:** preserve B's read-only ancestor semantics while binding the stored establishment branch to the actual C12 history, so a relabel between verified ancestors is refused without inventing a second ledger; then prove the same-root PsycheStore negative and a cold fork at the actual P6 consumer.
