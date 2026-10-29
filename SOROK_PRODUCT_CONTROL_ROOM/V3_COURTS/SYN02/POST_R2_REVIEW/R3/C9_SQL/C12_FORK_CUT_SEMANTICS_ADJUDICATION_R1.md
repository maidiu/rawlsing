# C12 cross-cut source exact: why the historical C9 test is RED on the repaired reader cut

**Status:** code-level differential interpretation + two actual version-specific test outcomes. `OWNER_FORK_SEMANTIC_SELECTION_HELD`. No original actor/Rule A/T or C11 grant.

## Exact directly inspected Python

At source `7bf2da302996491ddf34b9a039fea47ac982d135`:
`WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1/vendor/j/candidate/vendor/bp4/bp4/store.py`, Git blob `69a58f43dc70d320f2fc476eeac324c82c37ee59`, `C12Store.fork` establishes `fork_clock = self.last_clock(parent_branch_id)`, which uses nonperception last clock, then copies rows only with `clock<=fork_clock`, including perceptions. When the parent has a perception at clock 11 after a world event at clock 10, parent has that third perception while child created at world clock 10 only inherits first two. This explains the original historical expectation `len(parent_perceptions)==len(child_perceptions)` depending on *when* parent was measured: after postfork parent perception changes the count by design.

At source `68b058656254234f0af02df2a592aa6f8c6a8bd2`:
same file, Git blob `c94cd131f6d24737e43a2f3dd192ac2a7569eb18`, `C12Store.fork` now starts an explicit SQLite SAVEPOINT, checks parent integrity, finds `latest_perception = SELECT coalesce(max(clock),0) FROM perception...`, defines `fork_clock = max(self.last_clock(parent_branch_id), int(latest_perception))`, and copies **all** parent rows into new fork. The fork root is a digest of a typed `_fork_payload` including parent, clock, counts and row identities; `_fork_integrity` validates inherited exact prefix. A postworld perception at 11 is therefore part of the source-authorized fork prefix at 11, not dropped by imposing the older world-only clock 10.

**Direct executed contrary tests:**
- Run `40798932389`: writer 15/15 on old JOIN-E `7bf2...`; reader/fork 12/12 on later repaired JOIN-E `68b058...`, four reader SHA-256 pins match.
- Run `40798650310`: reader with old JOIN-E refuses source (12 source-integrity failures), correct hash guard.
- Run `40798810264`: writer historical `test_c6_same_count_perception_substitution_is_held` with later repaired JOIN-E **FAIL** at unchanged `len(root)==len(child)`: observed `2 != 3`. (14 other tests PASS.) Different fork cut, not an unknown CI skip.
- Original writer `c9_actor_r3.py` still has `c12_fork_guard` that treats perception-only suffix differently from newer repaired C12 actual fork. The actor-store/reader can be jointly tested on repaired C12 (12 reader cases pass), but the exact intended production fork clock/custody must be chosen by source owner. A green separate test on both is not the same thing as one adopted cut.

## Specific owner decision and executable acceptance

The competent C12+Sorok actor/storage owners must rule **which source cut is admissible for the C9 fork**, with distinct immutable actor/world/perception clocks and no suffix leakage. Test the following against the **same chosen cut**:
1. parent objective world event at effective t10, actor perception t11, selected fork at either t10 or t11 with explicitly captured per-source ordinal and branch epoch;
2. if fork at t10, *exclude* later perception t11 and keep its parent-only suffix; if at t11, *include* it and require source identity/receipt proving it belongs in the child prefix; never copy a later unqualified perception;
3. mutate parent after fork and prove the child immutable prefix unchanged and no wrong-actor private data surfaces; cold reopen/replay must agree with actual root and as-of, not just count;
4. observed C9 reader should surface only actor-eligible data; missing source/Rule T remains HELD, valid evaluated nochange not inferred;
5. source-severance of root/perception binding should fail the named reader downstream assertion, not generic Exception or a narrative description.

**No change to original frozen tests was made to resolve this discrepancy.** The historical earlier test remains relevant to its `7bf...` source cut; a new versioned acceptance test for `68b...` must be separately owned and reviewed before canonical source selection. No deletion or rewrite of the old expected count merely to obtain global green.
