# SOROK RRIF FINAL-E — INDEPENDENT FINAL VERDICT

## Terminal verdict

**REVISE_EXACT_RECEIVING_DEFECT.**

The repaired candidate passes its own 35-test sourcefree court, but the actual
clean PRE-MAIN receiving path **does not**. The additive patch omits the R3
extension needed by the repaired consumer, so the six RRIF-E tests, nine R3
extension tests and the first-consumer CLI fail after a real R2-base staging.

Do not merge or call this packet ready for PRE-MAIN. RRIF may close at
historical/sourcefree owner-held scope only after the exact packet is corrected
or explicitly declared an archive with no live receiver; it may not close as an
accepted, ready-to-receive software transfer.

## Exact evidence

| Item | Value |
|---|---|
| Review branch | `review/sorok-rrif-final-e-exact-receiver-20261031-r1` |
| Dispatch | `f136e9c397a457eecdc4e7c1f993ac1638529ba7` |
| Code under review | `8d9585296ff264b947559f4a78f49f73ca45e53a` |
| PRE-MAIN readback | `8e44ca9c751049d65e6def47600b5c073ee04b29` |
| Original R2 precondition | `598d9e9eaba5143950c63317705fd09104fbf463` |
| R2 source manifest | `7cfcb4679e36b522e83cc7120dbc166ce61dd220099c2aca8f5c9ddb5252c126` |
| R2 base files | 459 |
| E additive patch SHA | `11d4cf23fcb57d79e33a79511cf3c57d3ea53e63f4f5aeb3573608892a20bbb5` |
| Candidate rrif_r2 files | 640 |
| Staged PRE-MAIN patched files | 466 |
| R3 extension files omitted by patch | 174 |
| Candidate tests | 35 passed (20 R2 + 9 R3 + 6 E) |
| Staged R2-only tests | 20 passed |
| Staged E tests | collection failure: `ModuleNotFoundError: c12_guard` |
| Staged R3 tests | `file or directory not found` (`rrif_r3_extension`) |
| Staged first consumer | failure: `ModuleNotFoundError: c12_guard` |

## Three courts

**ENGINEERING — REVISE.** The code-under-review candidate is functional when
its full 640-file candidate tree is present. The receiving packet is not: the
patch adds only the E delta, not the R3 extension that `joined/c12_custody.py`
imports. The base-plus-patch stage therefore cannot run the promised 26/35-test
or first-consumer path. The receiving packet's `PATCH_APPLY_TEST.md` 26/26 claim
is reproducible only in a candidate copy that already contains the omitted R3
extension; it is not a clean PRE-MAIN validation.

**SOURCE SCIENCE — HOLD.** The code is sourcefree TEST_ONLY. It does not issue
CAN008/CAN011 Rule A/T, ADP/SCI05, native B/C8/C9/C12, Pyat world/N11/N12, C11,
or human A5. C12 repair is self-consistency only; `OWNER_ANCHOR_REQUIRED` remains.

**AUTHORITY — HOLD.** No owner adoption, PRE-MAIN merge, production DB, native
person or human participant is present. The reviewer does not merge or adopt.

## Exact bounded repair

1. Add the complete required `rrif_r3_extension/**` closure to the receiving
   patch (or remove every dependency on it and re-scope the tests/first consumer,
   but the required R3 tests cannot then be claimed).
2. Regenerate `RRIF_R2_CANDIDATE_SOURCE_PREIMAGE.json` after the complete staged
   tree; include `first_consumer_cli.py` and all extension files. Current file
   lists 638 entries while the clean stage has 466 files and omits the CLI.
3. Make `apply.sh` verify the exact R2 `SOURCE_MANIFEST.json` hash and 444 rows
   before patching. It currently checks only that `joined/session.py` exists.
4. Replace the unsafe rollback recommendation (`git checkout --` + `git clean -fd`)
   with removal limited to review-created files in an isolated worktree.
5. Rerun 20 R2 + 9 R3 + 6 E and the first consumer on the real clean PRE-MAIN
   base. Only then may the owner review an `ACCEPT_SCOPED` transfer.

## RRIF closure

At historical/sourcefree scope, the evidence is sufficiently complete for an
explicit owner-held source packet: the candidate's own 35 tests pass, the actual
C9/C12/CP-A5 incompatibilities are typed, and native/owner holds are explicit.
That is **not** permission to call the current receiving packet ready. Final
recommendation: **close RRIF only as a sourcefree/owner-held historical packet
after recording this REVISE; do not transfer the current patch to PRE-MAIN.**
