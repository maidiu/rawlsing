# SOROK #647 P2 permanent PROGRAMMA write-through — final focused closure

**RESULT:** `P2_REPAIRED_SOURCES_CLOSED_SCOPED__INTERVAL_76D5_ACCEPT__LATER_B716_ACCEPT__INTEGRATED_25D_ACCEPT_332E_PRESERVED__4B2_FINAL_CUT_CLOSURE_RUNNING__PR699_PR697_UNMERGED`.

This existing-record write-through records the independent focused closure of the two repaired public surfaces and preserves the prior integrated acceptance. It is not a new guide, registry, reporting project, product edit or protected write.

## 1. Exact independent focused closure

Closure: `3e04b6c7bb8af09c8506d8cf1310d923cbf4ea81` at `WORKER_RETURNS/SOROK-P2-PUBLIC-REPAIRS-FOCUSED-CLOSURE-20261105-R1`.

- Interval `76d5a3d13e0219c1a085ebadd55071de2dd90e7d` — `ACCEPT_SCOPED_TEST_ONLY`:
  - original privacy walker, action oracle and receipt oracle PASS;
  - 29/29 actual receipt files exist; zero reserved public keys `admission`/`c9`;
  - public keys are `admission_status`/`c9_public`;
  - primary no-auto-help positive `89b334` preserved; old `bdadbc57` and `7a256ed4` REVISE remain historical;
  - publication-receipt placeholders are non-gating, exact SHA supplied by review.
- Later `b71624f21d0bc638e8817f3929cc6c01ab8b0f61` (code `4bdba46c4d3a667a9cd7845eb57caa980df76373`) — `ACCEPT_SCOPED_TEST_ONLY`:
  - 0 public privacy hits; engineering output remains opt-in;
  - observation encounters `0→0`; explicit help `0→1`, ACTUAL refuse / SCHEDULED accept;
  - source/history/cold/cut-restore intact;
  - old `76fdb624` REVISE `f1a28724` remains historical.
- No full inherited 6/8/7/55 suite rerun.

## 2. Product and receiving currentness

- Integrated `25d40806d15516b7f7ffa04f47bc651022c6f2b0` remains `ACCEPT_SCOPED_TEST_ONLY` under review `332e00cb3da51b859a408a31f820b1afd7fe8fc0`.
- Current `4b2fed81c3f513eb4262ad5de277ce519c74c614` imports both repaired sources exactly; independent final-cut closure is RUNNING as `sorok-p2-final-cut-independent-closure-20261105-r1`; final receiving delta is RUNNING. **Do not promote 4b2 yet.**
- PR699 is draft/unmerged at `aa9ebbb533198acfa7056147f8cae3deb246ffe2`; PR697 remains open/unmerged at `41bf45813fd0adeffd9b54e1306c2022abe96514`.
- Lifecycle scoped acceptance `6398888f1d28152b5d29fef816f0bb45e77dd43b` and accepted `41bf` are preserved.
- No automatic dependent READY, native/human/B grant or protected promotion.

## 3. Changed existing guide records

- `00_HQ_WRITE_THROUGH_DECISION.md`, `10_RECONCILIATION_QUEUE_SOURCE_GAPS_AND_CLOSEOUT_CHECK_R1.md`: final focused-closure currentness.
- `07/08/09`: `hq_p2_interval_later_20261105` and `hq_p2_product_fanin_20261105` updated with exact acceptances, old REVISE preservation and 4b2 running state; counts conserved.
- `14`: 20 existing rows updated; 668 rows/83 gates unchanged.
- `15`: 8 existing seams updated; 38 seams unchanged.

## 4. Verification actually run

```text
python3 CROSS_HQ_CONTROL_ROOM/PROGRAMMA/verify_canonical_programma_r1.py
# PASS canonical tree: Pyat 782/892/62/82, FF 26/16, cross 18/16, Sorok 144/38, no prototype
# exit 0
```

JSON/JSONL parse, count validation and `git diff --check` passed. No product tests rerun; no running task polled.

## 5. PR body delta text for HQ connector

```text
Reconcile the final focused closure into PROGRAMMA #647:
- interval 76d5a3d13e ACCEPT_SCOPED_TEST_ONLY at 3e04b6c7: 29/29 receipt files, zero reserved keys admission/c9, privacy/action/receipt oracles PASS; primary no-auto-help positive 89b334 and old bdad/7a REVISE preserved; receipt placeholders non-gating.
- later b71624f21 ACCEPT_SCOPED_TEST_ONLY at 3e04b6c7: 0 privacy hits; observation 0->0, explicit help 0->1 ACTUAL refuse/SCHEDULED accept; source/history/cold/cutrestore intact; old 76fdb/f1a287 REVISE preserved.
- integrated 25d acceptance 332e preserved.
- current 4b2 imports both repairs exactly but final cut closure sorok-p2-final-cut-independent-closure-20261105-r1 and final receiving delta are RUNNING; do not promote 4b2.
- PR699 draft unmerged at aa9ebbb5; PR697 open unmerged at 41bf4581.
- lifecycle 6398888f and accepted 41bf preserved; no automatic dependent READY/native/human/B/protected promotion; no product or guide-schema edit.
```

Exact published source-branch SHA is returned in the final chat readback after commit/push.
