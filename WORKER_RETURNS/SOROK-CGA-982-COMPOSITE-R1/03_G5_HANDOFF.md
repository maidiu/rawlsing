# One independent G5 receiving handoff

**Exact source cut:** `ff30c13eea54e37e2dc8edfa73a7c7447127b735`.
**Base:** `4cbf67398d742eeab0853d047b6c2239c84b8348`.
**Branch:** `agent/sorok-cga-982-composite-stale-receipt-20261113-r1`.
**Report HEAD:** the commit containing this file; verify with `git rev-parse HEAD`.
**Remote branch:** `origin/agent/sorok-cga-982-composite-stale-receipt-20261113-r1`.
**Draft PR:** not created; the credential returned HTTP 403 for pull-request creation. See `06_PUBLICATION_STATUS.md`. The branch and exact cut are the delivery subject.

The receiving reviewer must be a genuinely separate nonauthor under #977. The author does not self-approve and does not declare G5 acceptance.

## Required inspection

1. Verify the report HEAD is a direct descendant of `4cbf67398` and that the only implementation change after the base is `WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/situated.py` (base blob `1433d68857...`, final blob `56d9b2e399...`).
2. Verify P4 `response.py` (`730d5692...`), `run_p4.py` (`b99d8e82...`), `sourcefree_p3_bridge.py` (`a041785f...`) and the P4 scope test (`728799b1...`) are byte-identical to #992.
3. Inspect both trust boundaries:
   - P4 foreground scope cannot redirect the source-issued P3 formation after a real SAY.
   - P6 actor access cannot accept a stale authentic receipt, a copied interval, a forged receipt identity, or a same-clock other-operation conduct.
4. Confirm the check executes before the enclosing P4 turn is appended, using only already-persisted owner episodes (`S46_INTERVAL_STATE`, `S46_DOMAIN_ISSUANCE`, `P6_HOUSE_CONDUCT`, world event), not a future ledger entry.
5. Run the original G5 hostile test unweakened (blob `a1453e799d...`), the D1 contract test (blob `30701f83ee...`), and the new current-operation tests.
6. Run the six-group 37-test #977 baseline using the source-pinned receiver asset (blob `2b489ba1ed...`).
7. Run the P4 source-owner 7, Agent B #986 6, Agent A/B + P4 CLI + P5 14, and P6 45 groups.
8. Exercise cold reopen, same-request retry, and a later operation that supersedes the earlier receipt.
9. Verify source/actor/root/branch/readset/sensory-cue preservation from the logs and blobs.
10. Return one G1–G5 verdict. Only the separate receiver may recommend `ACCEPT_SCOPED_SOURCEFREE_S2_FOR_HQ` and, separately, `INTEGRATION_READY_FOR_HQ`; otherwise `REVISE_EXACT_DEFECT`, `HOLD_EXTERNAL`, or a specifically demonstrated ownership blocker.

## Expected minimum

- Original G5 stale receipt refuses.
- A genuine current `APPROACH` receipt authorizes.
- Old interval, copied current interval, forged identity, and same-clock other-operation receipt refuse.
- Cold reopen and retry conserve the current operation.
- 37/37, 7/7, 6/6, 7/7, 14/14 and 45/45 pass at the exact cut.
- P4 and P6 source/actor/root/branch/readset/sensory-cue preservation holds.

## Evidence

`EVIDENCE.json`, `04_TEST_MATRIX.json`, `02_EXECUTION.md` and `evidence/`. The D1 and G5 author/reviewer branches were not modified.
