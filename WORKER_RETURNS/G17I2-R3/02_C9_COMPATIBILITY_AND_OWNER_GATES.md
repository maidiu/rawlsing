# C9 R3B / C12 durability compatibility and owner gates

**Status:** `C9_DURABILITY_HOLD__NO_ADAPTER__NO_DURABLE_REOPEN`.

The G17 patch is a bounded, pure-material C9 handoff. It is not a C9 actor store and not a C12 durability consumer. The original C9 R3B branch is a separate, unlaunched test-only actor/mirror harness with a different interface. No merge or adapter is authorized here.

## 1. What the G17 patch actually consumes

`c9_handoff_consumer.receive_handoff(handoff, material)` accepts a dict with schema `SOROK_G17_C9_MATERIAL_HANDOFF@1` and an owner-canonical `material_joint_opportunity` event. It refuses:

- `MATERIAL_SOURCE_NOT_AUTHENTIC` when the material dict is not exactly the canonical owner event;
- `SEVERED_MATERIAL_SOURCE` when the material event is not in the handoff causal parents;
- `MATERIAL_REF_MISMATCH` / `MATERIAL_PAYLOAD_MISMATCH` when the ref or payment/task/units payload differs;
- `AFTERSTATE_NOT_MATERIAL_CONSERVING` when the after-state is not the material-conserving result.

On success it returns an in-memory receipt with `status: ACCEPTED`, `e2_later_authority: HOLD_UNISSUED`, null route probability/selection weight and `person_or_child_generated: false`.

There is **no SQLite write**, no actor row, no receipt table, no outbox, no mirror, no branch/epoch, no C12 store and no cold-reopen state. The cold-process test is a fresh process re-executing the same pure function, not a durable reopen.

## 2. C9 R3B source and interface

Original C9 R3B branch: `agent/rabochii-sorok-20261029-c9-r3b-recovered-writer-reader-real-fanin-r1` at `fac064c9c3370d598e9b7469af652ae3504bc4ba`. It is an **unlaunched** commission/source recovery, not an accepted G17 consumer.

- Writer: `SOROK_PRODUCT_CONTROL_ROOM/V3_COURTS/SYN02/POST_R2_REVIEW/R3/C9_SQL/c9_actor_r3.py`, Git blob `67f34f699220ec1407e7e8f0d58ed328e88a36af`, SHA-256 `ee4765e28d80531e6b5450296ed209ef4e3303b827910bbf20b73dfaba52725e`.
- Reader: `.../C9_READER/actor_reader.py`, Git blob `5ef6a278a56968b8f9ccf700ae58e636a0999b5f`, SHA-256 `331cdae8523fce84c2a531f735104d1ebefe93e371c7d8da2d91f806ee717e98`.
- Writer interface: `ActorAuthority.publish(PublishRequest)` over actor/branch/version/receipt/attempt/requalification/outbox/world-receipt SQL tables; decision kinds and Rule T statuses are explicit.
- Reader interface: `read_actor_snapshot(source, database, actor_id, branch_id, branch_epoch, source_cut)` over actor SQLite and exact C12 fork/mirror state; it requires exact C12 source hashes and raises `FORK_HELD`/`C12_*` on mismatch.

Neither interface imports or accepts `SOROK_G17_C9_MATERIAL_HANDOFF@1`. The G17 candidate imports only `lab_sgi1.joint`; no path imports `c9_actor_r3` or `actor_reader`. There is no shared table, handoff schema, actor head, branch epoch, outbox or C12 mirror binding. **Interface mismatch is structural, not a configuration gap.**

## 3. C12 durability boundary

The G17 evidence has no C12 write/read. It does not create a C12 branch, perception, checkpoint, fork, mirror or root. Therefore:

- **Cold-process replay** = new Python process, same source, same in-memory deterministic path. It can show source-level repeatability, not durable state.
- **Durable C9 reopen** = process exit, SQLite/other store persists, a later process reads actor head/version/receipt and a same-assertion consumer. Not performed.
- **C9/C12 interoperability** = one selected C9 writer store plus C12 fork/perception state and a later reader. Not performed; no adapter.
- The C9 R3B reader’s exact C12 source pins and fork guard are a separate source contract; the G17 three-file overlay does not alter them.

The original C9 R3B return records a C12 perception/FORK_HELD issue and a source-owner freeze gate. Those remain **HOLD** and are not repaired by the G17 material patch.

## 4. Owner gates

### G17 original author / C9 handoff owner

1. Confirm whether exact canonical material equality (`material == material_joint_opportunity(effective_index, permit, material_units)`) is the intended owner law, including whether any owner-issued alternative schema exists.
2. Confirm the recursive future-child partition traversal scope (dict/list/tuple/string; repeated reads) and whether values or only field names are in scope.
3. Confirm `receive_handoff`’s bounded receipt is sufficient for the material handoff, or require a durable C9 actor record.

### C9 R3B owner

4. Decide whether a G17 handoff adapter to `PublishRequest`/actor SQL is authorized; if yes, specify the exact source cut, branch/epoch, receipt/version mapping and failure semantics.
5. Resolve the C9 R3B C12 perception/fork source conflict and select the canonical C12 source cut.
6. Decide whether the outbox/mirror and C12 fork guard are part of the first durable consumer, and who owns the cross-database ACID/no-claim boundary.

### C12 owner

7. Confirm whether the G17 material handoff should write any C12 state; if not, keep C12 durability out of this cut. If yes, supply the owner-approved branch/perception contract and cold-reopen consumer.

### Incumbent HQ / separate reviewer

8. Assign a source-qualified reviewer distinct from this worker and the original G17/C9/C12 owners.
9. Do not merge, adopt or update PRE-MAIN/PR #514/#516/#519/#521 on this return.

## 5. First material consumer

The first actual consumers in the tested cut are:

- `lab_sgi1.continuation.continue_person` / `forward_continuation` for the material continuation;
- `run_pipeline`’s `FutureChildPartitionGuard` before proposal/selection/commit;
- `c9_handoff_consumer.receive_handoff` for the bounded C9 material handoff.

No production, durable C9, C12 or native consumer is proved. The smallest future durable consumer would be an owner-authorized C9 R3B adapter that persists an accepted material receipt and later reopens it through the C9 reader with the selected C12 source; that adapter does not exist here.

## 6. FINDING / INTERPRETATION / HQ ACTION / OWNER

**FINDING:** G17 material authentication and recursive future-child refusal are genuinely repaired at the pure-source level, and the C9 handoff refuses forged canonical material. But the patch has no persistent C9 actor store and no C12 branch/mirror; C9 R3B is a separate unlaunched harness with incompatible interfaces.

**INTERPRETATION:** The patch is sufficient for the bounded sourcefree G17 security replay, not for durable C9/C12 custody. Treating cold-process replay as durable reopen would overclaim.

**HQ ACTION:** Accept only the bounded G17 engineering result; send the C9 R3B/C12 adapter question to the original owners; require a separate reviewer. Do not merge or promote.

**OWNER:** Original G17 author/C9 handoff owner; C9 R3B writer/reader owner; C12 owner; incumbent Sorok HQ; separate reviewer.

## 7. RUN / NOT_RUN

- **RUN:** G17 original reviewer 11/3, patched reviewer 14/14, author 13/13, cold-process replays, additional 3/3 hostiles.
- **NOT RUN:** C9 R3B 15/12 runtime suites, durable C9 reopen, C12 adaptation, native CAN/ADP/SCI05/C11/C12, original survey source, production.
- **NOT CLAIMED:** full C9 E1/RULE_A/RULE_T/E2, native person/practice, durable C9/C12, merge/adoption.
