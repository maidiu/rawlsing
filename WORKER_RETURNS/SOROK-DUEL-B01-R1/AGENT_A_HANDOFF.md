# SOROK B01 AGENT A — adversarial construction handoff

**Packet:** B01, `Select existing material writer and bounded household state ABI`, CG-B.
**Grade:** `SOURCEFREE_S2_ONLY`. No native science, actor/human right, source right, Pyat rule, or protected merge is issued.
**Branch:** `codex/sorok-duel-b01-a-20261112-r1`.
**Implementation SHA:** `05a9b988ae039d44c55e636e1c610c01d89b4c1d`.
**Running contract SHA:** `08a323b490df4e2ddd0dca7f8b3cd394dfe17e0a` (programme PR #938).
**Protected inspection baseline:** `6a5c12f04323d74001f9632063ec907f4fc4468e`.

## 1. Exact artifact

Changed code:

| Path | Change |
|---|---|
| `WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1/developmental_recursion/p2_owner.py` | Added the bounded P2 material-fact envelope (`material_fact_source`, `validate_material_fact`, `write_material_fact`) and the read-only `P2Owner.material_fact(slot)` accessor. |
| `WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/house.py` | Added the bounded `p6_household` fixture, `establish_household`, `read_household`, `parent_choice_input`, strict source/place/owner/binding verification, and wired household admission into the ordinary `establish(session)` new-house path. |
| `WORKER_RETURNS/SOROK-DUEL-B01-R1/test_b01_household.py` | Four discriminating sourcefree tests: actual-root positive, changed-value/severance/restore/cold, PsycheStore-kitchen negative, writer refusal guard. |

Return/evidence files are under `WORKER_RETURNS/SOROK-DUEL-B01-R1/`.

Commands actually run from this worktree with the qualified environment:

```text
/private/tmp/rawlsing-oct28-p1r1/venv/bin/python -B -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-DUEL-B01-R1/test_b01_household.py
/private/tmp/rawlsing-oct28-p1r1/venv/bin/python -B -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/test_house.py
/private/tmp/rawlsing-oct28-p1r1/venv/bin/python -B -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1/tests/test_p2_owner.py \
  WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/test_actor_scene_context.py \
  WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests/test_p3_owner.py::test_process_reopens_same_actual_p2_root \
  WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests/test_p3_owner.py::test_actual_p2_root_configuration_and_combined_statehash
```

## 2. Governing contract

The frozen packet requires one admitted actual-root fixture carrying source-qualified household resources/place/owner read through P6; the negative is a PsycheStore kitchen `MEDIATOR` or a test-local `later_decision` treated as a world-owned fact; restoration is an identical cold root/material state reopening without a new owner or scheduler. The packet names `S47/P2` objective world plus P6 `house.py`, PW-02 and PW-10, and `SOURCEFREE_S2_ONLY`.

The governing user intent is in the frozen programme sources, especially:

- `20261111_ROLLING_PERSON_WORLD_DURATION_MATERIAL_MEDIATION_R1.md`: materiality is practical and ambient; reuse existing owners; no new universal life scheduler, separate money/house psychology, or duplicate world/time ledger.
- `32_ROLLING_PERSON_WORLD_OWNER_RECONCILIATION_20261111_R1.md` lines 56 and 64: PW-02 is `EXTEND_SELECTED_WORLD_OWNER` (dwelling/tenancy/resources through the existing writer); PW-10 is `INTEGRATE_SAFELY; NO_SECOND_LEDGER`.
- `02_SOROK_IMPLEMENTATION_PROGRAMME_R1.md` B01 and the programme proof-grain gate: sourcefree engineering is separate from native science/rights/merge authority.
- The two complete ChatGPT Library architecture records are **NOT_INSPECTED locally**; their identities and that source limitation are preserved. No contents are claimed from them.

CG-A cross-input comparison: I inspected the unmerged chain `8248711fb8ba4ac07c0b0e6e7dfc4decce9352b7` -> `384d4a4ac4973b83187d9a1e160f6d085d6aae19` -> `0213c844b26a8e69afeea6e499fea46e13444c69` -> `37c5842e04892421c9ce74a39956c3cdcf57f0f5` with `git show`. Its selected contract (world resources own dates/homes/material; PsycheStore is actor-scoped) is consistent with B01, but its `test_selected_common_readset.py` kitchen `MEDIATOR` plus test-local `later_decision` is exactly the negative pattern, and its `WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/sourcefree_p3_bridge.py` P3/P6 bridge was not copied, modified or presumed received. Its p2_owner.py blob pin no longer matches this branch; any future merge must reconcile that pin rather than presume the candidate.

Selected writer trace (exact import path):

```text
run_p6.experience "new"
  -> run_p5.new -> run_p4.new (p4_fixtures, P2/P3 owner already constructed)
  -> establish(case.base_owner.fanin.session) [house.py:377]
  -> world.resources["p6_house"] + session.product._checkpoint(...) [house.py:391]
  -> establish_household(session) [house.py:392]
  -> p2_owner.write_material_fact(session, slot="p6_household", document=...) [p2_owner.py:75]
  -> session.world(); world.resources[slot] = document
  -> session.product._checkpoint(branch_id, world.clock, world)
       BP4Product._checkpoint            bp4/product.py:101
       -> C12Store.checkpoint           bp4/store.py:216
       -> WorldState.snapshot           bp4/world.py:323
          (resources are inside the snapshot content hash)
  cold reopen
  -> S45Session.world                   r30a/first_session.py:194
  -> BP4Product._world(branch)          bp4/product.py:123
  -> WorldState.restore                 bp4/world.py:340
  -> C12Store.latest state/checkpoint
  -> P2Owner.snapshot hashes vars(session.world()) including resources
  -> P2Owner.material_fact("p6_household") [p2_owner.py:158]
  -> house.read_household(session) / house.parent_choice_input(session)
```

No new DB, scheduler, person ledger, actor owner, counter, or world clock was added. `p6_household` is one new entry in the existing `world.resources` and is therefore inside the existing P2 snapshot material hash.

## 3. Strongest achieved result

One ordinary P6 `new` on the actual sourcefree root now admits a `p6_household` document with:

```text
schema     SOROK_HOUSEHOLD_MATERIAL@1
grade      SOURCEFREE_FIXTURE
place      dwelling_id, kind, rooms (exactly the P6 house rooms), tenure=rented,
           tenancy {holder_actor_slot: "A", landlord_ref}
owner      actor_slot "A", actor_id from world.actor_state["A"], authority household_holder
resources  bounded bindings to existing world material:
           WORLD_RESOURCE:workshop {tool_available, material}
           ACTOR_STATE:A {cash, material_remaining, free_hours}
root       exact session root
branch     exact session branch
epoch      establishment world clock
source     content address of schema/grade/place/owner/bindings
```

`read_household(session)` verifies the exact stored field set, schema/grade, root, branch, epoch, source content address, place (including the actual P6 room set), owner identity against the actual root/world actor state, and every bound resource field. It resolves the live values, so the returned document carries actual resources rather than a copied ledger. It returns `source`, `material_hash`, the resolved place/owner/resources, and `world_state_hash`.

`parent_choice_input(session)` freezes the reusable read-only input:

```text
schema          SOROK_PARENT_CHOICE_INPUT@1
grade           SOURCEFREE_S2_ONLY
first_consumer  NONE_VERIFIED
parent_decision NOT_EVALUATED
parent_action   null
source          {owner: S47_P2_OBJECTIVE_WORLD, slot: p6_household,
                 ref: P6_HOUSEHOLD:<source>, hash: <source>,
                 material_hash: <resolved material hash>}
root_hash, branch_id, clock, epoch
household       {place, owner, resources}
read_boundary   {psyche_store: NOT_READ, parent_hidden_reason: NOT_READ,
                 model_prose: NOT_READ}
```

No parent act, utterance, motive, or decision is fabricated.

Demonstrated evidence (all in this worktree, exact logs in `evidence/`):

- **Positive producer → first consumer:** 4/4 B01 tests pass. The actual `new` path establishes the fixture; `read_household`, `parent_choice_input`, and `P2Owner.material_fact` read it from the checkpoint. The P2 owner read returns the same `source` and its own composite `state_hash`; the raw stored document is the documented bindings document.
- **Changed-value dependence:** changing actual `world.actor_state["A"]["cash"]` through the existing checkpoint changes the resolved household `resources` and `material_hash` while the fixture `source` stays the same; the parent input reflects the change. Restoring the value restores the exact baseline read and parent input.
- **Meaningful severance:** removing `p6_household` from the checkpointed world makes `read_household`/`parent_choice_input` refuse `P6_HOUSEHOLD_ABSENT` and the P2 owner read refuse `P2_MATERIAL_FACT_ABSENT`. Removing a bound world resource or changing source/root/owner is refused. Restoration re-admits and returns the exact baseline.
- **Cold restore:** a fresh Python subprocess opens `state/actual-p2`, reads the household and parent input, and returns byte-identical JSON to the restored baseline. Its episode/checkpoint/world-event/perception counts equal the restored counts, so the cold read added no owner or scheduler write.
- **Negative oracle:** a real `PsycheStore` is written with a `MEDIATOR` record whose payload is `{"room": "kitchen", ...}` and a test-local `later_decision` returns `ENTER_KITCHEN` from it. `parent_choice_input` still reports the actual dwelling/rooms and contains neither the mediator hash nor `"kitchen"`; after the world household is severed, the PsycheStore decision still says `ENTER_KITCHEN` while the world readers refuse. The writer also refuses a PsycheStore-record document with `P2_MATERIAL_FACT_PSYCH_RECORD_REFUSED`.
- **Regression:** the full protected P6 `test_house.py` suite passes 8/8; P2 owner 5/5, actor scene context 2/2, and the two selected P3 owner reopen/config tests 2/2 (an earlier separate run also passed the P3 non-test-only refusal test). See `evidence/p6_test_house_regression.log` and `evidence/adjacent_regression.log`.

## 4. Own hostile findings

These are the most serious weaknesses I found in my own work:

1. **P3 code-pin break for old state roots.** `p2_owner.py` is byte-hashed into `P3Owner._code_pins()` and therefore into `P3Owner.config_hash`. This change alters that pin. Fresh states created under the new code cold-reopen exactly (proved), but a state root created under the old `p2_owner.py` will refuse to reopen with `P3_CONFIG_CHANGED`/config mismatch. This is a real compatibility impact, not hidden. B02/B03 or HQ must either recreate old fixture roots or perform a deliberate pin migration; I did not invent a migration.
2. **Two checkpoints at house establishment.** `establish` commits `p6_house` and then `establish_household` commits the household at the same clock. Both are append-only checkpoints; the final world state is one coherent material state. It is not one atomic multi-writer transaction. B04/E03 own crash-atomic composite commit and recovery; B01 must not claim it.
3. **Household resources are bindings, not a copied ledger.** The fixture `source` identifies schema/grade/place/owner/bindings; the resolved `material_hash` identifies the current values. A consumer that treats `source` alone as the current resource value identity is wrong. This design deliberately avoids duplicating `world.resources`/`actor_state`, but the distinction is a real interface requirement.
4. **Reader verification is coupled to whole-session verification.** `P2Owner.material_fact` calls `session.verify()` before returning the fact, so an unrelated P6/S47 verification failure makes the owner-level household read fail closed. The P6 `read_household` itself only verifies the checkpointed world and household document. This is conservative, but it means the owner-level accessor is not the thinnest possible ad hoc read.
5. **One-shot fixture admission.** `establish_household` accepts the same document idempotently at the same epoch and refuses a different document (`P6_HOUSEHOLD_ALREADY_ESTABLISHED`). There is no B01 update/renew path; a caller that wants to change the fixture at a later clock must remove the slot first, and even then the new epoch differs. B03/B04 must add a recorded update operation rather than mutate this ABI silently.
6. **The fixture exists only in the `house` presentation scene.** `establish_gallery`/`establish_symbolic` do not establish a household, so household reads refuse there. This is intentional for B01 but means the ABI is not a universal scene fixture.
7. **My first test draft failed three ways and I repaired them, not the production contract.** I initially compared the P3 composed `state_hash` to the P2 owner `state_hash` (wrong layer), compared cold counts to pre-mutation counts rather than restored counts, and constructed the PsycheStore result without the receipt link/response ref required by the existing store. The corrected tests are in the committed file. The production behavior was not weakened to make them pass.
8. **The structural negative is coarse.** The test checks that `house.py` source has no `PsycheStore(`, `p3.state_store`, or `p3_psyche`; that is a guard against accidental imports, not a proof of all possible data flow. The runtime PsycheStore test is the substantive negative.

## 5. Unresolved challenges

- **Parent first consumer is not verified.** `parent_choice_input` is a frozen input ABI only. No parent identity, request, choice, hidden reason, utterance, or action is implemented; C01/C03/C04 must supply and prove the actual parent consumer.
- **B02/B03/B04/B05 are not implemented.** There is no historical calendar/as-of mapping, split period, home-period record, dwelling/noise/tenancy commitment, recurring cost, acquisition, refusal, or multicycle duration. The household place/resources ABI is only the B01 material base.
- **Pre-existing P6 chronology proof failure.** `SOROK-P6-CHRONOLOGY-PROOF-20261107-R1/test_p6_chronology_proof.py` fails its final `restored == baseline_view` assertion on `mii_exposure_id`/`mii`. I reproduced the identical failure at protected baseline `6a5c12f` in a fresh detached worktree. It is not caused by B01 and is not repaired here because MII presentation sequencing is outside this lease. Evidence: `evidence/preexisting_p6_chronology_failure.log`.
- **No crash/partial-failure reconciliation.** The material write is a single in-process mutation plus one checkpoint; a crash between them loses the uncommitted mutation (fail-safe) but there is no durable operation reservation or retry receipt for the household fixture. B04/E03 own that.
- **No native, scientific, rights, actor, human, or merge authority.** This is sourcefree engineering only.
- **No psychological evaluation.** The household/parent input is material only; no `MISSING_RULE` is evaluated as `NO_CHANGE`, and no trait, memory, motive or durable psychological transition is created.
- **No controller/provider cost measurement.** The commission's cost field is `UNKNOWN`; I did not instrument controller tokens/latency/process RSS in this session.
- **Full estate not run.** I ran the B01 tests, the full P6 house suite, the P2 owner suite, actor scene context, and selected P3 owner reopen/config tests. I did not run the entire 144/38/83/304 estate or the whole P3/engine suites.
- **Two ChatGPT Library architecture records remain NOT_INSPECTED locally.** No local copy/tool was located; no contents are asserted from them.

## 6. Likely attack surfaces for SAME B

- Try to smuggle a PsycheStore `MEDIATOR` through the **generic material envelope** using nested keys, a different `kind` location, or a record whose top-level fields avoid the deny set. The current guard is top-level field/kind based; a nested or renamed record can still be a bad fact for a *different* reader, though the household reader's strict field set refuses it.
- Try to bind `p6_household` to a world resource or actor slot outside the B01 bounded sets (`workshop`, `A`). The writer and reader should both refuse; verify there is no alias path.
- Try to change `place.rooms` while keeping a recomputed `source`. The reader compares against the actual `house.ROOMS`; a monkeypatched room set or a forged fixture should refuse. Try the same with owner actor id, tenancy holder, and branch.
- Try to use `P2Owner.material_fact` on a fork or a foreign branch. It binds root/branch/clock/world state; check whether a fork's copied checkpoint can legitimately carry the household and whether the read should follow the fork (it should).
- Try to make `parent_choice_input` look like a parent action by supplying a fixture whose `owner.authority` or place fields imply a decision. The frozen input has no action field; verify no hidden field is added by a later consumer.
- Try to reopen a pre-B01 state root and observe the P3 code-pin refusal. That is expected and disclosed; do not treat it as a household bug.
- Try to make the establishment idempotent at the same epoch but not at a later epoch, and check whether replacing via slot removal can produce a non-identical restore. The restoration test is same-clock only; a later-clock restoration is not claimed.
- Try to break the cold subprocess test by leaving an in-memory profile/gaze state that masks checkpoint state. The test uses a fresh process and compares counts; extend it to fork/copy the state and verify the household follows the branch.
- Try to make `p6_household` collide with the MI `sorok.historical_materialization.v1` resource or the existing `p6_house` slot. The writer allowlist is only `p6_household`; verify that remains true.

**Hardest concrete challenge for SAME B:** make the household establishment a **single** checkpoint with `p6_house` while keeping the household source/owner checks and the exact P2 snapshot binding, then prove a fork/copy cold reopen and a pre-B01 state-root migration story. If B can also make `parent_choice_input` consume the `P2Owner` composite snapshot directly (rather than a raw session) without broadening the ABI, that is a genuine improvement over this cut.

## 7. Rejected alternatives

- **Copy the resource values into the household document.** Rejected: duplicates `world.resources`/`actor_state`, creates a second material ledger and stale values, and contradicts the no-duplicate-ledger requirement. The binding-plus-live-resolution shape is the chosen alternative.
- **Write the household as a PsycheStore record.** Rejected by the packet negative oracle and by owner semantics: PsycheStore records are actor-bound psychological records; home/room/material facts are world-owned. The negative test demonstrates the leak that this would create.
- **Add a `HouseholdOwner`, new scheduler, new database, or universal household engine.** Rejected: the programme requires reuse of S47/P2/P6 and explicitly forbids a duplicate world/time/person ledger.
- **Put household fields inside the existing `p6_house` resource.** Rejected: `read_house` already has a strict fixture source/room/object/history contract; widening it would change the existing P6 reader and its provenance proofs. A separate `p6_household` resource keeps the new ABI bounded and additive.
- **Use `P2Owner.realize(ADMIT_EVENT)` for the fixture.** Rejected: a fixture is not an event; it would require a future event clock, participant/event circumstances, and would fabricate a world event. The bounded material-fact write uses the same checkpoint writer without inventing an event or a scheduler.
- **Duplicate the source/psych guard only in `house.py`.** Rejected: two implementations of the same envelope would drift. The generic envelope/writer lives in `p2_owner.py`; `house.py` adds the household-specific strict schema and resolution.
- **Add `replace=True` to B01.** Rejected as unnecessary update authority: B01 is one-shot fixture admission; removing it narrows the attack surface. Restoration is proved by re-establishment after severance at the same clock.
- **Adopt or modify the unmerged CG-A P3/P6 bridge.** Rejected: the commission says the candidates are not protected accepted and their bridge must not be duplicated/modified. I compared the CG-A contract and used its test-local `later_decision` pattern only as the negative oracle.

## 8. Proof boundaries

Do not claim any of the following from this return:

- Native SOROK CAN/ADP/Pyat N9/N10E/N10W science, actor rights, human validity, source/use rights, or protected merge.
- A parent decision, parent performed action, parent utterance, hidden motive, or parent first consumer. The parent input is `NONE_VERIFIED` and `NOT_EVALUATED`.
- B02 historical calendar/as-of, B03 dwelling/noise/tenancy commitments, B04 acquisition/refusal/recurring costs, B05 multicycle duration, or J1/J2.
- A new owner, scheduler, person-world ledger, economy, market simulator, or universal household model.
- Crash-atomic composite establishment, concurrent-writer safety, or exactly-once material retry.
- A cryptographic signature or authorization claim from `source`; it is a content address.
- Cold reopen of a state root created under the pre-B01 `p2_owner.py` pin. Same-code cold reopen is proved; old-pin compatibility is broken and disclosed.
- The pre-existing P6 chronology proof as green. It fails identically at baseline and on this branch for MII exposure sequencing; it is outside this packet.
- Full-estate or whole-programme coverage. Only the bounded B01 tests and listed adjacent suites were run.

## Measured cost and limits

Tests actually executed:

| Command | Result | Evidence |
|---|---|---|
| B01 packet tests | 4 passed in 32.93s | `evidence/b01_household.log` |
| Full P6 `test_house.py` | 8 passed in 151.38s | `evidence/p6_test_house_regression.log` |
| P2 owner + actor scene + P3 owner subset | 9 passed in 46.39s | `evidence/adjacent_regression.log` |
| Pre-existing P6 chronology proof at baseline and branch | 1 failed; identical `mii_exposure_id`/`mii` assertion | `evidence/preexisting_p6_chronology_failure.log` |

Controller/provider cost, token use, process RSS, and wall-clock product latency: `UNKNOWN`. No controller or provider instrumentation was available or invented here.

Hard limits: `SOURCEFREE_S2_ONLY`; same-code cold boundary; bounded actual P6 house scene; no parent consumer; no native/science/rights authority; no protected merge.
