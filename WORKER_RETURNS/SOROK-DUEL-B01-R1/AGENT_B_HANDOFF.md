# SOROK B01 AGENT B — constructive counterstrike

**Packet:** B01, `Select existing material writer and bounded household state ABI`, CG-B.
**Grade:** `SOURCEFREE_S2_ONLY`. No native science, actor/human right, source right, Pyat rule, S14/A5 grant, or protected merge is issued.
**Branch:** `codex/sorok-duel-b01-b-20261112-r1`.
**Opponent frozen HEAD:** `edbb4b344d54731a527fd415a965bc848ed964e1`.
**Implementation SHA:** `160cbbd0ae00fb965004085c0e07c872384fe0ff`.
**Running contract SHA:** `08a323b490df4e2ddd0dca7f8b3cd394dfe17e0a` (PR #938).
**Protected inspection baseline:** `6a5c12f04323d74001f9632063ec907f4fc4468e`.
**No remote/protected push; this branch is isolated for HQ.**

## 1. Exact revised artifact

Changed code/tests at implementation SHA `160cbbd0ae00fb965004085c0e07c872384fe0ff`:

| Path | Change |
|---|---|
| `WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1/developmental_recursion/p2_owner.py` | Added read-only `branch_is_ancestor`; `P2Owner.material_fact` now follows a verified C12 fork while normal same-branch reads keep A's exact schema and verification. Only `material_fact` changed on the class; constructor/`validate_proposal`/`realize`/participant methods are untouched. |
| `WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/house.py` | `read_household` accepts a stored branch that is the current branch or a verified C12 ancestor; `read_house` uses the same provenance rule. Same-branch behavior is unchanged. |
| `WORKER_RETURNS/SOROK-DUEL-B01-R1/test_b01_household.py` | Added fork, world-resource value, bound-resource/owner severance, P6 action-on-fork, and read-purity tests. Existing A tests retained. |

Return/evidence files are under `WORKER_RETURNS/SOROK-DUEL-B01-R1/`. The ABI revision is `B01_ABI_B_REVISION.md`. Machine records are `PROGRAMMA_DELTA.json` and `impact.json`; A's records are retained as `PROGRAMMA_DELTA_A.json` and `impact_A.json`.

Commands actually run from this worktree with the qualified environment:

```text
/private/tmp/rawlsing-oct28-p1r1/venv/bin/python -B -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-DUEL-B01-R1/test_b01_household.py
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

## 2. My own reconstruction, written before trusting A

I read the frozen programme, task packets, relay contract, #911 owner-reconciliation source, and the user-directed material/duration requirement before reading A's handoff or diff. My reconstruction was:

- B01 must use the **existing** S47/P2 objective-world writer and the existing P6 `house.py` reader. It must not create a household engine, scheduler, second ledger, or actor-psychology owner.
- One admitted actual-root fixture must carry source-qualified household place, owner, and resources from the world into P6. A changed bound value must be visible; removing the fact or a bound source must refuse; the same cold root/material state must reopen without a new owner or write on read.
- PsycheStore `MEDIATOR`/practice records and test-local `later_decision` are actor/psychology records, not world facts. They may not stand in for place/tenure/resources.
- The parent-choice input is only a selected read boundary. The parent first consumer is `NONE_VERIFIED` until CG-C exists. No parent act, utterance, or hidden reason may be fabricated.
- `source` is schema/content identity; a bound value hash must be distinguishable and must change when the bound world value changes. A fork is a copied world state, not a rewrite of the source. A legitimate C12 fork should therefore still see the copied household unless an own-owner update explicitly replaces it.
- B01's public household schema should remain usable by Pair3 C01; any ABI change must be explicit and must not silently assume C01 saw it.

The two complete ChatGPT Library conceptual/operational files remain **NOT_INSPECTED locally**; I do not claim their contents. The #911 reconciliation and all frozen programme files were read.

## 3. Independently verified strengths of A

These survive independent examination and are preserved:

1. **Writer selection is real.** A used the existing P6/S47 checkpoint path (`p6_household` inside `world.resources`) and did not add a new database, clock, scheduler, actor owner, or household engine. The positive chain through `run_p6.experience("new")`, C12 checkpoint, cold reopen, and `house.read_household` is actual in this worktree, not a story fixture.
2. **The content/binding split is correct.** `material_fact_source` excludes `root/branch/epoch/source`; `read_household.material_hash` binds the resolved values and state. Changing A's `cash` changes `material_hash` while `source` stays stable. I preserved this and extended the test to a **world resource** (`workshop.material`), not only actor cash.
3. **The negative direction is substantively guarded.** `house.py` has no PsycheStore import; the writer refuses top-level psyche fields/kinds; a PsycheStore mediator and a test-local `later_decision` produce no household input even after world severance. A's separate-store negative is an evidence gap, not a production leak; see §4.4.
4. **Same-branch cold and severance are real.** The fresh-subprocess cold test reopens identical household/parent JSON with unchanged episode/checkpoint/world-event/perception counts. Removing `p6_household` refuses all three readers; restoring it returns the baseline.
5. **P6 regression was not weakened.** A did not modify `test_house.py`; the full P6 house suite remains green. I re-ran it after my changes.
6. **A disclosed the P3 code-pin cost honestly.** That disclosure is correct and important; I confirmed and widened it in §4.2.

A's fork attack surface at handoff line 155 correctly said the read "should" follow the fork. The implementation did not. That is the central defect below.

## 4. Defects established

### 4.1 Consequential defect: a legitimate C12 fork loses the copied household and house

**Evidence:** `evidence/a_head_fork_refusal.log` was produced with A's exact HEAD `edbb4b344...` in a detached worktree. On a normal `fork_alt("fork-child")`:

```text
parent_branch= first_session
read_household_before_fork= first_session
child_branch= fork-child
read_household REFUSED P6_HOUSEHOLD_SOURCE_OR_ROOT_MISMATCH
parent_choice_input REFUSED P6_HOUSEHOLD_SOURCE_OR_ROOT_MISMATCH
read_house REFUSED P6_HOUSE_SOURCE_OR_ROOT_MISMATCH
material_fact REFUSED P2_SOURCE_OR_STATE_VERIFICATION_FAILED
```

The C12 fork really copied the checkpoint rows (`shared_root.equal=True`), and the child world contains the copied `p6_household` and `p6_house` documents. Both documents still carry the parent `branch` as provenance. A's readers compared that stored branch to the current child branch with equality. `P2Owner.material_fact` additionally called full `Session.verify()`, which refuses `S46_STATE_BRANCH_MISMATCH` because S46/S47 are deliberately not forked. Thus a copied world fact became unreadable on the fork.

This is not a synthetic edge: `test_mii.py::test_actual_p2_branch_fork_isolates_derivative_scope` uses a real C12 fork, and the packet's restoration/provenance requirement is about identical material state. A's fork refusal also contradicted A's own stated expectation in the handoff.

### 4.2 Consequential cost: p2_owner byte changes invalidate P3 code-pin roots

A disclosed that pre-B01 P3 roots fail under the new pin. The repair necessarily changes `p2_owner.py` again. I confirmed the wider consequence with an actual A-era state root created at `edbb4b344...`:

```text
state_created_by=edbb4b344d54731a527fd415a965bc848ed964e1
OPEN_REFUSED RecursionRefusal P3_CONFIG_CHANGED
```

Evidence: `evidence/p3_code_pin_a_era.log`. This is a real `BREAKING_INTERFACE` effect: A-era roots (and pre-B01 roots) require recreation or a deliberate P3 pin migration. I did not invent a migration or mutate a P3 config. This is not repaired here because `P3Owner`/pin migration is outside B01's writer lease.

### 4.3 Evidence gap: A's claimed bound-resource severance was not directly tested

A's handoff says removing a bound world resource or changing source/root/owner is refused. The committed test file only removed the `p6_household` slot and changed `cash`; it did not remove `workshop`, remove actor `A`, or change the owner `actor_id`. The production behavior is correct (verified by the new test), but the claim was not established by A's evidence. I added:
- `test_world_resource_value_changes_material_hash_not_source`;
- `test_bound_resource_and_owner_severance_refuse_and_restore`.

### 4.4 Incomplete negative: A's PsycheStore is not the P6 root's own psyche store

A's runtime negative writes a separate `PsycheStore` under `tmp_path`, not `state/actual-p2/p3_psyche.sqlite3`. The structural no-import guard and the household's strict stored schema are the substantive protections; the runtime test proves a test-local decision is not read, but it does not prove the actual P6 root's PsycheStore is ignored. I did not claim that stronger result. It remains an attack surface in §7.

### 4.5 Refuted accusation: A did not weaken P6 house semantics to make the fixture pass

A left `test_house.py` unchanged and its suite passes. My initial suspicion that A had silently altered the existing house reader was wrong; only the additive household path was added. I record the false suspicion and its refutation.

## 5. Corrections implemented

### 5.1 Read-only branch provenance, not rebinding

Added module-level `branch_is_ancestor(session, branch, epoch)` in `p2_owner.py:45`. It accepts:
- the current branch; or
- a strict C12 ancestor proven by the existing qualified store: `Session._lineage_result()` (when available), `store.inherits_verified_prefix()` (row/shared-root verification), parent-chain rows, and `epoch <= fork_clock` at every copied fork edge.

It refuses missing stores, malformed rows, cycles, non-ancestor branches, invalid epochs, and a fact established after the fork. It performs no write.

### 5.2 `read_household` and `read_house`

`house._read_household_document` now takes an optional `branch_ok` predicate. `read_household` passes the C12 provenance predicate; `establish_household` still uses exact current-branch validation before writing. Stored `branch` remains the establishment provenance; the returned read's `branch` is the current branch. `source` is unchanged; `material_hash` is the bound current-state hash. `read_house` uses the same predicate, so the pre-existing P6 house reader can read the copied house on a child branch while retaining its source/root/object/history checks.

This is provenance-following, not a new fact: no checkpoint, episode, world event, perception, owner, scheduler, or branch is created by a read. The new test asserts unchanged episode/checkpoint/world-event/perception counts across fork reads.

### 5.3 `P2Owner.material_fact`

Normal same-branch reads are deliberately unchanged: full `s.verify()`, exact branch validation, `snapshot().state_hash`, and A's exact read keys (no `state_scope`). A's test asserts the normal read has no `state_scope`.

For a verified ancestor fact, `material_fact`:
- proves ancestry with `branch_is_ancestor`;
- verifies the actual C12 branch preimages (`c12_verify`) rather than pretending unrelated S46/S47 interval state exists on an unforked branch;
- validates the material envelope against the **stored** branch while returning the **current** branch;
- computes a material state hash over world/events/encounters with the explicit marker `intervals: "NOT_FORKED_ON_C12_BRANCH"`;
- adds the optional `state_scope: "C12_FORK_WITHOUT_S46_INTERVAL_STATE"` only on ancestor reads.

A non-ancestor/foreign branch is refused. The P2 constructor, proposal validation, realization, and participant methods are untouched.

### 5.4 Tests added

- `test_c12_fork_carries_ancestor_household_without_rebinding_source`: real P6 new → real C12 fork → household and parent input read on child; `source` stable; `material_hash` bound value changes; `P2Owner.material_fact` document retains parent provenance and reports current child branch; P6 `read_house`, `scene`, and a real `GO` action work on the child; reads are pure; a foreign stored branch is refused and restored.
- `test_world_resource_value_changes_material_hash_not_source`: changes `workshop.material`, sees resolved world binding and `material_hash` change, `source` stay stable, restores exactly.
- `test_bound_resource_and_owner_severance_refuse_and_restore`: removes/restores `workshop` and actor `A`, changes/restores owner `actor_id`, and verifies exact refusals and restoration.
- Normal read compatibility assertion: no `state_scope` on the same-branch `P2Owner.material_fact` result.

## 6. Proof of improvement

Measured in this worktree; logs in `evidence/`:

| Command | Result | Evidence |
|---|---|---|
| B01 suite | **7 passed in 61.18s** | `evidence/b01_household_b.log` |
| Full P6 `test_house.py` | **8 passed in 163.14s** | `evidence/p6_test_house_b.log` |
| Full P6 `test_mii.py` | **18 passed in 231.99s** | `evidence/p6_test_mii_b.log` |
| P2 owner + actor scene + selected P3 reopen/config | **9 passed in 54.58s** | `evidence/adjacent_b.log` |
| A HEAD fork probe | household/parent/house/material-fact all refused after fork | `evidence/a_head_fork_refusal.log` |
| A-era P3 root reopen | `P3_CONFIG_CHANGED` under B code | `evidence/p3_code_pin_a_era.log` |

The changed-value positive now covers both an actor-state bound value and a world-resource bound value. The negative covers a real PsycheStore mediator and a test-local decision. The cold same-branch subprocess test remains green. The new fork test is the actual producer→first-reader proof at the C12 boundary: it uses the real P6 `new`, real fork rows, the child checkpoint, the household reader, and a real P6 `GO` action.

## 7. New attack surfaces

1. **P3 code-pin migration is not solved.** Any p2_owner byte change invalidates old P3 roots. A-era roots now fail as well. B02/B03 or HQ must either recreate roots or add a deliberate, reviewed pin migration. This is the largest cost of the repair.
2. **`house.py` now imports the new `p2_owner.branch_is_ancestor` symbol.** Pair3 C01, if it merges B's `house.py` while keeping A's `p2_owner.py`, will fail at import. C01 must rebase both files together; do not presume it saw these edits. This is an exact `BREAKING_INTERFACE` for mixed cuts.
3. **Fork state hash is scoped.** On an ancestor read, `state_hash` intentionally omits S46 interval state and carries `state_scope = C12_FORK_WITHOUT_S46_INTERVAL_STATE`. Consumers must not treat it as the full composite P3 hash or compare it across forks as if intervals existed.
4. **Child P6 events retain parent house provenance.** On a child branch, P6 `GO`/inspect/outward event bodies still carry the parent `house["branch"]`; the session branch is the child. This is provenance-consistent with `encounter.movement_evidence`, but a new consumer must not assume `event.body.branch == session.branch_id`.
5. **Fork verification is C12/lineage, not S46/S47.** A fork does not copy S46/S47 state; reading a world material fact on a fork therefore verifies the world/C12 branch and lineage, not unrelated period owners. Full P6 `experience` on a cold fork remains blocked by P2/P3 branch binding; not claimed.
6. **Same-root PsycheStore negative remains unproved.** The actual P6 `p3_psyche.sqlite3` was not injected with a mediator; only a separate store was. The source guard is strong but not a same-root runtime proof.
7. **`inherits_verified_prefix` read cost is unmeasured on large roots.** It verifies shared row hashes per fork edge; bounded B01 roots are small. No token/RSS instrumentation was available.
8. **Ancestor acceptance is broader than the household fact.** `read_house` now accepts an ancestor house document for all P6 house reads, including writes on the child. The full P6/MII suites pass, but this semantic widening deserves independent attack.
9. **One-shot establishment and two checkpoints remain.** `establish_household` still refuses a different document at a later epoch and `establish` still writes `p6_house` then household in two checkpoints. B04/E03 own crash-atomicity/update.

## 8. Surviving disagreements and limits

- **Fork inheritance semantics vs rebinding.** I chose read-only ancestor provenance: the copied document keeps its establishment branch; the read reports the current branch; writes on the child stay on the child branch. A/C01 should attack whether a child must instead explicitly rebind/re-establish the household before any write, and whether provenance in event bodies is acceptable downstream.
- **Full composite state on fork.** S46/S47 are not forked. I did not fabricate a full P3 composite hash. If a later consumer requires one, S46 fork support or a real period migration must be built by the S46/P3 owners.
- **`parent_choice_input` still takes a raw session.** A's suggested improvement (consume the P2Owner composite snapshot directly) is not implemented. The function remains a frozen read with `first_consumer=NONE_VERIFIED`; C03 must bind a real parent consumer.
- **P3 pin migration.** Not implemented; see §7.1. I will not call old roots compatible.
- **Same-root PsycheStore negative.** Not established; see §7.6.
- **Cold fork and full `run_p6.experience` on a fork.** Not proved; the P2 owner binding/P3 config path outside B01 refuses. The fork proof is an in-process verified-owner read/action at the documented boundary.
- **No parent decision/action/utterance, no B02–B05, no calendar, no duration, no acquisition/refusal, no crash atomicity, no native/science/rights/human/merge authority.** The two Library architecture sources remain NOT_INSPECTED locally.

## 9. Challenge to Agent A

1. **Falsify ancestor inheritance.** Construct a legitimate fork where reading the copied household is wrong—e.g., the parent replaced/revoked it after the fork, the child has its own new occupancy, or C03 requires a child-owned fact. Show the expected refusal or rebind boundary. If my read-only provenance is too permissive, repair it; if it is right, prove why.
2. **Solve or explicitly price the P3 pin break.** Provide a safe migration for A-era/baseline P3 roots or prove they are disposable test roots. Do not silently recreate accepted roots.
3. **Attack the P6 event-provenance widening.** Trace a child `GO`/inspect through C04/C03 or any later consumer. Prove that a parent `branch` in the event body cannot be mistaken for current-branch authority; or propose the minimal rebind.
4. **Make the negative same-root.** Inject a `MEDIATOR` into the actual P6 root's `p3_psyche.sqlite3` and show `read_household`/`parent_choice_input` still ignore it, then sever the world fact and show the world reader refuses while the PsycheStore decision remains.
5. **Make `parent_choice_input` consume the P2Owner snapshot directly** without broadening the public input schema, and prove it refuses an uncommitted/foreign session view. A identified this as the hard improvement; I did not take it.
6. **Prove or hold cold fork.** If a cold fork must read the household through P6, fix the P2/P3 binding path within the correct owner lease; otherwise state the exact blocked edge. Do not claim the in-process fork proof is cold.
7. **Re-run the exact regression commands above** and attack `branch_is_ancestor` with a sibling branch, a post-fork child replacement, a forged branch row, and a grandchild fork.

## Measured cost and limits

Test wall time: 61.18s + 163.14s + 231.99s + 54.58s = 510.89s of executed suites in this return, plus A-head/A-era probes. Controller/provider token, latency, process RSS, retry, and USD instrumentation: `UNKNOWN`; none was available or invented. No full-estate run, no protected merge, no native/science/rights/human claim.

**Bottom line:** A selected the right existing writer and built a real cold world-owned household reader. I confirmed and preserved that. The fork defect is real and repaired at the actual P2/P6 readers, with the P3 code-pin break explicitly retained as a breaking cost rather than hidden. The next round should attack the provenance semantics and the pin migration, not re-litigate whether the original household writer was real.
