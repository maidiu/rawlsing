# PYAT #997 — native P0/P1 evidence on the frozen Browser candidate

## Status

**`NATIVE_P0_P1_SCOPED_HARNESS_PASS__REPOSITORY_TESTS_68_OF_75__TEST_HARNESS_REVISE__NOT_G5`**

- Candidate: `2c476e739a263dd0069b54706c6cfa63b07190c1`
  (`PYAT #997 Agent B R5: ...`)
- Candidate product parent: `534fb6602cce60fd991abd7972ebd95c92f3146c`
- Branch: `agent/pyat997-native-proof-r1`
- Worktree: `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat997-native-proof`
- Product/test/source edits: **none**
- Integration: **UNMERGED**
- This is native executor evidence, **not** G5 acceptance and not a 998 import.

## Runtime / candidate preflight

- CWD exact: `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat997-native-proof`
- Python `3.11.3`, PyArrow `22.0.0`, DuckDB `1.5.2`, pyreadstat `1.3.2`, pytest `9.0.2`
- Product diff vs candidate HEAD: **empty**
- Candidate B R5 blobs:
  - `pre553_source_postconsumer_receipts.py` `fad3a96bb00bb3d4eb4c9e3e8c5e2d6ca970dcd8`
  - `test_pyat997_s1e_saved_native_first_consumer.py` `053926db84a022066535b3378d080338fe306983`
- Full pin log: `evidence/candidate_pins.txt`

## Actual repository test run

Command in handoff form:

```bash
python -B -m pytest -q -o addopts='' -p no:cacheprovider --junitxml=... \
  rawlsing_next/tests/test_pyat997_s1e_saved_native_first_consumer.py \
  rawlsing_next/tests/test_pyat997_s1e_saved_source_bridge.py \
  rawlsing_next/tests/test_pyat997_s1e_source_saved_body_bridge.py \
  rawlsing_next/tests/test_pyat960_s1e_source_i02.py \
  rawlsing_next/tests/test_pre553_source_direct_parquet_estate.py \
  rawlsing_next/tests/test_pyat991_s2d_saved_admission.py
```

Actual JUnit: **75 tests, 68 passed, 7 failed, 0 errors, 0 skipped, 32.053s**.

- `evidence/native_six_suite.txt`
- `evidence/native_six_suite.junit.xml`
- `evidence/native_six_suite_summary.json`
- R5 focused: **5 passed, 15 deselected in 6.46s**

### The seven failures are test-only defects, not a reproduced product failure

1. **Timestamped regenerated SAV/DTA fixtures** break exact-restore source roots:
   `source_to_saved...`, SAV/DTA `changed_source_cell...`, and the body-bridge
   restore test when run in the full suite. Two equal-value SAV files generated
   more than one second apart have different SHA-256 values; the body-bridge
   test passed on an isolated rerun. Probe: `evidence/test_failure_probe.txt`.
2. **`_native_i03` first-negative selection**:
   `test_pyat997_s1e_saved_source_bridge.py::_native_i03` returns the first fact
   from the first supported plan record. That is a country query with
   `RISK_SET_UNAVAILABLE`; the same plan contains actual supported query refs
   with denominator 5. The native harness scans all compiled query refs and
   selects a supported fact.
3. **Stale expected error strings**:
   - forged HELD promotion is actually refused earlier with
     `Q2_ORIGINAL_FROZEN_FATE_CENSUS_DRIFT`, not the test's later
     `Q2_OPERATION_FATE_OR_CLAIM_PROMOTED`;
   - `unresolved_routing` is refused as
     `Q2_REALIZATION_ROUTING_CENSUS_DRIFT`, not
     `Q2_REALIZATION_BODY_OR_ROUTING_CONTRADICTION`.
   Both are typed refusals before positive attribution.

No source/test repair was made on this read-only commission.

## Independent native harness

`WORKER_RETURNS/PYAT997_NATIVE_FIRST_CONSUMER_PROOF_R1/native_proof_harness.py`

It uses the existing frozen public/test-only APIs to drive:

```text
TEST_ONLY generated SAV
  -> Q2 SourceI02Handoff / SourceSavedBodySink (one decode, one cell pass)
  -> S2-C 13-family persisted Parquet/Zstd estate
  -> SavedC11Admission
  -> actual execute_saved_i03, execute_saved_i05, execute_saved_batch,
     execute_issued_workload
  -> join_saved_source_operation_fates
```

Actual result: **0 exit, PASS**.

### P0 actual cold native fact

- Baseline source SHA: `9a01ede0deaa07f876b61cdfccd0811f58ef47d40dd866c5538e9542612979b0`
- Logical root: `d84b11464d88fb4df273d2f210b76001871821c71df2ed56531cc103088cf1b3`
- Actual supported I03 fact:
  `urn:rawlsing:pre553:EmpiricalFact:sha256:f49a734cc77880acc9686ace0c73ad45817f5c37bfdb81212aa9e30ecd33621b`
- Typed state `SUPPORTED`; raw denominator `5`; numerator `5`
- Three supported and three negative actual I03 query results were observed in
  the compiled plan; the supported one above is the selected first-reader fact.
- 13-family counts: Universe 1, RespondentIdentity 5, QuestionVariableBinding 1,
  RespondentEvent 5, RoutingEligibilityFact 5, EmpiricalCoordinateFact 5,
  WeightMeasureFact 0, AuthoritySnapshot 7; zero-typed families preserved.
- 14 Parquet members; 29 body objects; no second body corpus; stage clean.

### Changed source and exact restore

- Changed source SHA: `ae16923ba0bab7dc9905808f91736c04dbf7785707f39056182ba926391474e6`
- Changed actual fact:
  `urn:rawlsing:pre553:EmpiricalFact:sha256:34745edc2af255679c4ac0e8b4ea33aa6bb0b3ccf596dae23fd862d3243390d2`
- Restored source SHA equals baseline; restored fact equals baseline exactly.
- Restored logical root equals baseline.
- Restored postconsumer join hash equals baseline:
  `fcc5ec968d87396d1909ba154aaf2c6561ea167b01c805dcd30417740192fc9e`

### P1 fate join

- 22 rows / 22 original operations
- preconsumer fates: **8 ELIGIBLE, 14 HELD**
- positive native-linked operations: **6**
- native discovery candidates exactly joined: **8**
- pending eligible operations: **2**
- issue grants created: **0**
- preconsumer handoff unchanged: **true**
- all original `issued_receipt_refs` empty: **true**
- noneligible rows have no native receipts: **true**
- Batch: one actual DISCOVERY unit, `COMPLETED`; issued workload has zero
  query requests and one discovery, so no Batch query unit was fabricated.
  The actual supported query is exercised directly through `execute_saved_i03`
  from the compiled plan.

### Negative refusals

- Held-to-ELIGIBLE promotion: `Q2_ORIGINAL_FROZEN_FATE_CENSUS_DRIFT`
- Q2 frontier mismatch: `Q2_R03_ORIGINAL_FRONTIER_HASH_DRIFT`
- No positive attribution before refusal.

## G4 resource evidence

| Measure | Actual |
|---|---:|
| Source rows | 5 |
| Retained estate bytes | 356,590 B |
| Peak staging bytes | 533,299 B |
| Source reads | 1 |
| Decode calls | 1 |
| Cell passes | 1 |
| Full C11 builds | 0 |
| Sampled process-tree peak RSS | 128,163,840 B |
| Process-tree samples | 145 at 10 ms |
| Parent `ru_maxrss` | 127,025,152 B |
| Full 100k / 6 GiB | **NOT_RUN** |

Process-tree evidence: `evidence/process_tree.json`,
`evidence/process_tree_run.txt`.

## Gates

- **G1 PASS_SCOPED** — exact candidate pins, cwd, runtime, imports, no product
  edits.
- **G2 PASS_SCOPED_NATIVE_HARNESS / REPOSITORY_TEST_HARNESS_REVISE** — actual P0
  cold fact, changed fact, exact source/root/fact restore; repository suite has
  test-only fixture/helper failures.
- **G3 PASS_SCOPED_NATIVE_HARNESS / REPOSITORY_TEST_HARNESS_REVISE** — actual
  fate join, held/frontier refusals, no false positive; repository suite not
  fully green.
- **G4 PASS_SCOPED_SMALL_FIXTURE** — resource counters above; no 100k claim.
- **G5 NOT_RUN** — distinct nonauthor required.

## Engineering / science / authority

- Engineering: native P0/P1 evidence executed on existing frozen APIs.
- Science: no original35 source/measurement/science acceptance.
- Authority: TEST_ONLY sourcefree; no production CURRENT, issuer, host or actor
  grant; no protected merge.
- #1006 baseline and new storage comparison: not run.

## Next dependency

Browser/test-harness owner should correct the three test-only issues and rerun
the six suites; then a distinct nonauthor G5 receives this native proof and the
exact candidate head. No product edit is requested from this return.

## Self-critique

- The repository suite is not green; 68/75 is the actual result.
- The harness is native evidence, not an independent G5.
- The Batch workload shape has no issued query unit; this is reported, not
  hidden.
- The exact source restore harness intentionally reuses the baseline source
  bytes; that exposes the test fixture timestamp defect rather than masking it.
- Original35 and 100k remain external.
