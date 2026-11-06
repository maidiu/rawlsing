# SOROK #647 P2 permanent PROGRAMMA write-through — currentness correction

**RESULT:** `PERMANENT_DIRECT_WRITE_THROUGH__LIFECYCLE_ACCEPTED_SCOPED__INTERVAL_REPAIR_RUNNING__LATER_EVENT_REVIEW_RUNNING__FANIN_RETURNED_NOT_ACCEPTED__PR697_OPEN_UNMERGED__GUIDE_PENDING_INTEGRATION`.

This is the source guide branch for the selective receiving candidate. It updates the existing P2 currentness after the fanin return and the interval attempt-boundary defect. No new guide, schema, reporting project, product edit or protected write is created.

## 1. Exact currentness

- Lifecycle author cut `79b90e4a57cbd1b738a9b9484677736d1b6415ab`; focused independent `ACCEPT_SCOPED_TEST_ONLY` at `6398888f1d28152b5d29fef816f0bb45e77dd43b`, 5 tests `19.82s` plus 5 probe groups. Accepted scope is local UI lifecycle only; sidecar is not security/tamperproof; outside view retains portal shape; missing sidecar defaults `PORTAL`.
- Interval `bdadbc57c2664d3155a97853422e74b6128261f8`: 6 author tests `55.59s`; still author-tested candidate, not accepted. Independent review `sorok-p2-interval-later-independent-review-20261105-r1` is RUNNING. Concrete defect: standalone interval `admit_continuation` calls `adapter.do_help()` automatically, mixing observation with a user attempt. Original interval author repair `sorok-p2-interval-attempt-boundary-repair-20261105-r1` is RUNNING; no repair SHA or acceptance yet.
- Later-event `76fdb624afc7674f088d10c349bfe15ffd0b865a`: 5 author tests `84.85s`; still author-tested candidate under the same RUNNING review. Fanin observes the later opportunity without auto DO_HELP, but that is not acceptance.
- Product fanin RETURNED `579afc5fe63ff305ec49d4c8d42abc8475acf8bb` on `codex/sorok-p2-product-fanin-20261105-r1`; remote verified, 6 author tests `58.22s`, one S47 root, lifecycle + explicit interval + later-event opportunity, encounters `0` until explicit `DO_HELP` yields `1`; independent fanin review NOT_RUN, not accepted/integrated. `evidence/upstream_interval_auto_do_help.json` records the bypassed upstream defect.
- PR #697 remains open, ready and unmerged at `41bf45813fd0adeffd9b54e1306c2022abe96514`. Guide is isolated and pending integration. No dependent READY.

## 2. Changed existing guide records

- `00_HQ_WRITE_THROUGH_DECISION.md`, `10_RECONCILIATION_QUEUE_SOURCE_GAPS_AND_CLOSEOUT_CHECK_R1.md`: P2 currentness corrected; fanin no longer called running; interval no longer an unqualified positive.
- `07_GITHUB_ACCESSIBLE_ASSET_LOCATOR_R1.json`, `08_INITIAL_EVIDENCE_GRADED_DEPENDENCY_AND_SEAM_REGISTER_R1.json`, `09_INHERITED_144_FUNCTIONS_TO_WORKING_SPINE_R1.json`: lifecycle accepted, interval repair running, later-event review running, fanin returned/not accepted; new fanin/defect sources.
- `14_W7_RECURSIVE_PHASE_GATES_AND_WORK_PACKAGES_R1.jsonl`: existing interval/later/fanin fields on 20 rows updated; 668 rows/83 gates unchanged.
- `15_W7_VERSIONED_SEAMS_AND_GATE_JOIN_CANDIDATES_R1.jsonl`: existing fields on 8 seams updated; 38 seams unchanged.

## 3. Verification actually run

```text
python3 CROSS_HQ_CONTROL_ROOM/PROGRAMMA/verify_canonical_programma_r1.py
# PASS canonical tree: Pyat 782/892/62/82, FF 26/16, cross 18/16, Sorok 144/38, no prototype
# exit 0
```

JSON/JSONL parse, count validation and `git diff --check` passed. No product suite rerun; no running worker polled or invented.

## 4. NOT_RUN / limits

- Fanin independent review NOT_RUN; interval repair has no published SHA/acceptance; interval/later reviewer still RUNNING.
- Lifecycle scoped acceptance unchanged; interval/later not accepted.
- No product suite rerun, no native/human/B/Pyat rights, no protected merge.
- No dependent READY.

Exact published source-branch SHA is returned in the final chat readback after commit/push.
