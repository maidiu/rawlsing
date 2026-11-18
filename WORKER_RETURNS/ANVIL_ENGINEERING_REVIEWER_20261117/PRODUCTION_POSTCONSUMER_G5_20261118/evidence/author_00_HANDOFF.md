# ANVIL production postconsumer — prepared exact-type seam

## Status

**Implementation complete; frozen for distinct nonauthor review.**

- Branch: `agent/anvil-engineering-cut1-20261117-r1`
- Starting HEAD: `6b5402658a342a32180e281c62f4762729e37220`
- Code/test commit: **`01dc90cb0d1c5c7cdcf5cb29a02bc0cfda650efd`**
- Product change: exact `join_saved_source_operation_fates` type guard plus
  indispensable `PreparedSavedC11Admission` import only.
- New focused test: `rawlsing_next/tests/test_anvil_prepared_saved_postconsumer_join.py`
- Own return: `WORKER_RETURNS/ANVIL_ENGINEERING_PRODUCTION_POSTCONSUMER_20261118/`
- Product edits outside the authorized file/test: **NONE**
- Source/science/current/issuer/writer/schema/protected rights: **NONE**
- Self-acceptance: **NONE**

## Exact production diff

```text
rawlsing_next/pre553_source_postconsumer_receipts.py
+ from rawlsing_next.pre553_prepared_saved_i03 import PreparedSavedC11Admission
...
- or type(admission) is not SavedC11Admission
+ or type(admission) not in (
+     SavedC11Admission, PreparedSavedC11Admission,
+ )
```

- Baseline blob: `4bf3d8e38227df01c20308fd421b552f3cc0badc`
- Current blob: `0a2e7b899ebd392761d38b8ceb175f0bf81c6378`
- Baseline exact guard line: 272
- Current exact guard: line 273
- No `isinstance`, base proxy, subclass acceptance, generic admission, or
  other guard relaxation.
- Producer/runner exact types, `runner.repository is admission`, all source/
  I02/release/manifest/authority/U-root/current/replay checks, independent
  native revalidation, v1 0-QUERY/1-DISCOVERY guard, and optional v2 checks
  are retained unchanged.

## RED -> GREEN

Baseline focused run against the old guard:

```text
7 failed, 1 passed
exit 1
```

`evidence/red_focused.txt`

Post-fix focused run:

```text
8 passed
exit 0
7.86 s
```

`evidence/green_focused.txt`

`green_focused_run1.txt` is an intermediate test-code typo in the witness, not
a product failure; the corrected focused suite is the green evidence above.

## Real sourcefree join parity

`evidence/postconsumer_witness.py` uses the existing sourcefree Q2/native
fixture, authentic R03 v2 issuer, actual saved Batch, and actual
`join_saved_source_operation_fates`. No synthetic admission or forged positive
is used.

Fixture:

- source SHA-256: `8d1f2ad10f4abfb949c10e590b0440a065f57c9ac146d8603de74a8714dc80dd`
- estate manifest SHA-256: `4de8bbf7e93b17d4f83330cb58a16e1740c5014d14048f294b9bedf0a253832e`
- 13-family table; 5 respondents; 1 query binding; 5 events/coordinates.
- Source stats: one fixture snapshot acquisition, `full_c11_builds=0`,
  `cleanup_complete=true`.

Compiler:

- v1: **0 QUERY / 1 DISCOVERY**
- R03 v2 TEST_ONLY issuance: **12 QUERY / 1 DISCOVERY**
- v2 original U root: `ac9d5a0bd6c8620a192ec52c6b3379c1eeeac858c49cd415473bc81f00428ec1`

Actual base and prepared results:

| Property | Base `SavedC11Admission` | Prepared `PreparedSavedC11Admission` |
|---|---|---|
| Batch units | 13 | 13 |
| States | all COMPLETED | all COMPLETED |
| Prepared index builds | n/a | **1** |
| Join operations | 22 | 22 |
| ELIGIBLE / HELD | 8 / 14 | 8 / 14 |
| Positive native-linked | 6 | 6 |
| Pending eligible | 2 | 2 |
| Native units rechecked | 13 | 13 |
| Discovery candidates joined | 8 | 8 |
| Issue grants | 0 | 0 |
| Result hash | `9ff0e289b6fe4e3a428291c85e26398dec21d6abc7c61af91412e1bb09df0ec7` | same |
| Rows / audit / native refs / replay | reference | **equal** |

The focused test explicitly asserts complete row equality, audit equality,
result-hash equality, exact 22/6/2/14 counts, 13 completed units, one prepared
index build, and all Batch provenance refs equal.

## Negative coverage

New focused tests pass for:

- arbitrary admission object;
- exact base subclass and prepared subclass;
- foreign runner bound to the base repository;
- manifest drift;
- external I02 root drift;
- CURRENT revoked after a valid prepared Batch;
- unissued/fabricated query in the saved manifest;
- forged completed receipt with changed native output refs.

Existing affected suites also pass:

- `test_pyat997_s1e_saved_native_first_consumer.py` — 24 tests, including
  changed legitimate source input, changed native fact, exact restore, source
  and current refusals, missing receipt/fate guards, and fabricated issuer
  negatives.
- `test_pyat997_r03_governed_query_issuer_v2.py` — 8 tests, including actual
  saved Batch without source reopen and postconsumer guards.
- `test_anvil_prepared_saved_batch_cut1.py` — 5 tests, prepared Batch cut.
- New focused suite — 8 tests.

**Affected suite combined: 45 passed, exit 0, 32.03 s.**

`evidence/affected_suite.txt`

Explicit changed-input/restore:

```text
1 passed, 23 deselected, exit 0, 3.97 s
```

`evidence/changed_restore.txt`

## Commands

```bash
PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q \
  -o addopts='' -p no:cacheprovider \
  --basetemp=WORKER_RETURNS/ANVIL_ENGINEERING_PRODUCTION_POSTCONSUMER_20261118/tmp/affected \
  rawlsing_next/tests/test_anvil_prepared_saved_postconsumer_join.py \
  rawlsing_next/tests/test_anvil_prepared_saved_batch_cut1.py \
  rawlsing_next/tests/test_pyat997_r03_governed_query_issuer_v2.py \
  rawlsing_next/tests/test_pyat997_s1e_saved_native_first_consumer.py
```

## Resource bounds

- Focused suite: wall 8.52 s, user 8.09 s, sys 1.50 s, parent max RSS
  **129,728,512 B**.
- Bounded witness: wall 3.32 s, user 3.58 s, sys 0.57 s, parent max RSS
  **126,971,904 B**.
- No subprocess inside the witness; existing child process tests are bounded
  pytest cases.
- Staging memory: **NOT_MEASURED**.
- No 100k/6 GiB/full benchmark matrix.

`evidence/focused_resource.time`, `evidence/postconsumer_witness.time`

## Provenance

- Owner request read from
  https://github.com/maidiu/rawlsing/issues/997#issuecomment-6968569543
  (saved as `evidence/owner_request_997_comment_6968569543.json`).
- CUT2 joined return and `evidence/joined_probe.py` were read.
- Existing R3/archive and prior untracked evidence untouched.
- No locality author file touched.
- Protected/current/source/issuer/writer/evaluator/actor changes: none.

## Limits and incompletions

- Scoped sourcefree TEST_ONLY engineering; no original35, native science,
  production CURRENT, protected merge, or #998/#1009 closure claim.
- Independent native revalidation is retained; the prepared Batch optimization
  applies only to the initial Batch, not to the postconsumer revalidation.
- 45 targeted nodes, not a full matrix.
- No independent G5 or self-acceptance.
- Return-root temp fixtures and the pre-existing untracked files are not
  committed.

## Review handoff

Frozen code/test commit: **`01dc90cb0d1c5c7cdcf5cb29a02bc0cfda650efd`**

Distinct nonauthor reviewer must verify the exact two-file diff, real
base/prepared 22-operation fate parity, 13 completed units/one prepared build,
typed negatives, changed-input/restore, source/current/replay guards, and
resource bounds. Do not merge, rebase, or broaden this grant.

**STOP for independent review.**
