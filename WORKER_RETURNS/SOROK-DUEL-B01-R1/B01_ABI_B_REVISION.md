# B01 household / parent-choice ABI — B revision

**Status:** sourcefree `SOURCEFREE_S2_ONLY`; additive normal-branch ABI, fork-provenance extension, and deliberately documented P3 code-pin break.
**Implementation SHA:** `160cbbd0ae00fb965004085c0e07c872384fe0ff`.
**Base A ABI:** `B01_ABI.md` and `AGENT_A_HANDOFF.md` at `edbb4b344d54731a527fd415a965bc848ed964e1`.
**Supersedes for fork semantics:** the exact-branch invariant in `B01_ABI.md` §Invariants and A's handoff line 155. Same-branch behavior is unchanged.

## Normal same-branch contract (unchanged)

```text
material_fact_source(document) -> sha256 content address
    excludes root, branch, epoch, source
validate_material_fact(document, *, root, branch, world_clock) -> detached document
write_material_fact(session, *, slot, document) -> write receipt
P2Owner.material_fact(slot) -> SOROK_P2_MATERIAL_FACT_READ@1

house.establish_household(session, *, fixture=None) -> read document
house.read_household(session) -> SOROK_HOUSEHOLD_MATERIAL_READ@1
house.parent_choice_input(session) -> SOROK_PARENT_CHOICE_INPUT@1
```

On the current branch, `P2Owner.material_fact` keeps A's exact verification and key set: full `Session.verify()`, exact branch validation, `snapshot().state_hash`, and no `state_scope` key. `establish_household` still validates exactly against the current branch before writing. The stored household fields and source/place/owner/binding rules are unchanged.

## C12 fork provenance (new)

A real C12 fork copies checkpoint rows up to its fork clock. The copied `p6_household` and `p6_house` keep their establishment `branch`; the session branch is the child. The readers now accept that stored branch when it is the current branch or a **verified ancestor**:

```text
branch_is_ancestor(session, branch, epoch) -> bool
    true for current branch
    true for an ancestor only when:
      - session lineage validates (when the joined validator exists);
      - the qualified C12 store proves the copied prefix/shared root;
      - the parent chain reaches the stored branch without a cycle;
      - epoch <= fork_clock on every copied fork edge;
    false for siblings, foreign branches, malformed rows, missing store,
    invalid epoch, or a fact established after the fork.
```

`read_household` returns:

- `branch` = current read branch (child);
- `source` = stable content/schema hash;
- `material_hash` = bound current-state hash, which changes on a fork even when resolved values are identical;
- `place`, `owner`, `resources` = resolved live values from the child checkpoint.

The stored document retains its establishment branch as provenance. Reads are pure: no episode, checkpoint, world event, perception, owner, scheduler, or branch is written.

`read_house` uses the same predicate. The existing P6 house source/root/room/object/history checks remain unchanged. On a child branch, P6 actions commit to the child, but event bodies retain the parent house `branch` as provenance; consumers must not equate that provenance with `session.branch_id`.

## P2Owner.material_fact on a fork

An ancestor read additionally validates the actual C12 branch preimages and does not pretend unrelated S46/S47 interval state was forked. It returns:

```text
schema             SOROK_P2_MATERIAL_FACT_READ@1
grade              TEST_ONLY_S47_OWNER_NOT_NATIVE_DEVELOPMENTAL_SCIENCE
slot               p6_household
root               S45 root hash
branch             current child branch
clock              child world clock
epoch              establishment epoch
source             content/schema hash (stable)
state_hash         world/events/encounters hash with intervals marker
state_scope        C12_FORK_WITHOUT_S46_INTERVAL_STATE   [fork only]
world_hash         digest of the child world snapshot
document           stored envelope with its establishment branch
```

`state_scope` is absent on same-branch reads. A non-ancestor branch is refused with `P2_MATERIAL_FACT_ROOT_OR_BRANCH_MISMATCH`.

## Consequences for queued/active work

- **Pair3 C01:** normal household/parent schemas are unchanged; `P2Owner.material_fact` normal reads are unchanged. However, B's `house.py` imports the new `p2_owner.branch_is_ancestor`. A mixed cut of B `house.py` with A `p2_owner.py` is an import failure. C01 must rebase/reconcile both files together; do not presume C01 saw this revision.
- **B02/B03:** may use the fork-aware read. Do not treat the parent `document.branch` as current write authority. A later household update/replacement path is still required for moves/renewals.
- **B04/E03:** the two-checkpoint establishment and one-shot household update are unchanged; crash atomicity is still theirs.
- **P3 roots:** any `p2_owner.py` byte change alters `P3Owner._code_pins()/config_hash`. A-era and pre-B01 roots refuse cold reopen with `P3_CONFIG_CHANGED`. No migration is invented here.
- **Full P6 cold experience on a fork:** still blocked by the P2 owner/P3 branch binding outside this lease; this revision proves an in-process verified-owner fork read/action, not a cold fork reopen.

## Proof boundaries

No native/science/rights/human/merge authority. No parent decision, action, utterance, or motive. No B02–B05 calendar/tenancy/acquisition/duration. No crash-atomic commit. No same-root PsycheStore injection. No full-estate coverage. The two Library architecture sources remain NOT_INSPECTED locally.
