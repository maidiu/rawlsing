# RECEIVING TEST AND CAS PREFLIGHT — RRIF-F0

## 1. Frozen state and isolation

- PRE-MAIN pin: `8e44ca9c751049d65e6def47600b5c073ee04b29`
- Live PRE-MAIN readback: `refs/remotes/origin/integration/pre-main-reconciliation-r1` = same SHA at preflight.
- E4F candidate: `f2c0af3273d612bff0a7bd2407532b52caf4348b`
- E5 candidate: `96e6d49ac18274332751c5fbb87c6ed370e8fd9c`
- E4FR: `review/pyat-rrif-e4fr-d02-corrected-consumer-hostile-20261101-r1` = PRE-MAIN, no returned review.
- E6: `review/pyat-rrif-e6-b5m2-postpatch-hostile-20261101-r1` = PRE-MAIN, no returned review.
- All test runs used detached/sparse throwaway worktrees. No active worker worktree or PRE-MAIN was run in or modified.
- Every pytest command used `PYTHONDONTWRITEBYTECODE=1`, `-p no:cacheprovider`, and a JUnit receipt.

## 2. PRE-MAIN baseline source-free regressions

### 2.1 Accepted B5 and M2 baseline

Worktree: `/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/rrif-e4f-premain-8e44ca9c` at `8e44ca9c...`.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. python3 -m pytest -q -p no:cacheprovider \
  --junitxml=/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/rrif_f0_baseline_b5_m2.xml \
  rawlsing_next/tests/test_pre553_learned_product_lifecycle.py \
  rawlsing_next/tests/test_pre553_learned_product_release.py
```

Result:

```
...................................................................      [100%]
67 passed in 0.50s
```

Exit `0`. B5 39/39 and M2 28/28. Log: `rrif_f0_baseline_b5_m2.log`, 99 bytes, sha256 `64041cf0f4b8731d24bbb9fc7fb66abff2fbba60b3b13bcee3f11edd532adf11`.

### 2.2 PRE-MAIN E2 independent hostile baseline

The E5 E2 hostile test file was extracted to a temp path; it imports only current public APIs and the accepted M2 test helpers.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. python3 -m pytest -q -p no:cacheprovider --tb=line \
  --junitxml=/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/rrif_f0_baseline_e2_hostile.xml \
  /var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/rrif-f0-overlay/test_pre553_e5_s06g_independent_hostile.py
```

Result:

```
FFFFFFFFFF                                                               [100%]
10 failed in 0.17s
```

Exit `1`. This is the expected PRE-MAIN defect-presence RED, not an E5 regression. Log: `rrif_f0_baseline_e2_hostile.log`, 5740 bytes, sha256 `9e61249cee46fa4e7a1d1d49b55414b807056eeda77963b5fbc4e55f13bf588b`.

### 2.3 E1 D02 explicit real-Timestamp RED

Worktree: `/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/rrif-e4f-startup-ffd03934` at E1 `ffd03934d...`.

A source-free pyreadstat SAV and DTA fixture with one `DATETIME` column was decoded through `iter_cells`; an aware `datetime` subclass and a one-level `.item()` wrapper were passed to the E1 helper.

```
sav str '2008-04-05 06:07:08' str
dta str '2008-04-05 06:07:08' str
AwareDT str '2008-04-05 06:07:08+00:00'
Wrapper str '2008-04-05 06:07:08+00:00'
```

E1 D02 remains explicitly RED. It was not tested into green by selecting only green cases. Log: `rrif_f0_e1_d02_red.log`, 148 bytes, sha256 `ffe2c9ffafbce188ed7702dfe8467298e3565105dd1ae513b1add8820154364b`.

## 3. E4F receiving-shape preflight

Worktree: `/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/rrif-f0-e4f-f2c0af32` at `f2c0af327...`.

### 3.1 E1 33 + E4F 12

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q -p no:cacheprovider \
  --junitxml=/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/rrif_f0_e4f_33_12.xml \
  rawlsing_next/tests/test_rrif_e1_c3_d01_declared_encoding_admission.py \
  rawlsing_next/tests/test_rrif_e1_c3_d02_opaque_datetime_carrier.py \
  rawlsing_next/tests/test_rrif_e1_c3_current_integration_regressions.py \
  rawlsing_next/tests/test_rrif_e4f_d02_real_datetime_subclass.py
```

Result: `45 passed in 1.01s`, exit `0`. This is 11 D01 + 18 E1 D02 + 4 integration + 12 E4F.

Log: `rrif_f0_e4f_33_12.log`, 99 bytes, sha256 `bfc985343e110a04ef0eae2c0999821705b89ba8bbda9f6015d33b1eb0130eeb`.

### 3.2 E4F selected regressions

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q -p no:cacheprovider \
  --junitxml=/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/rrif_f0_e4f_selected_194.xml \
  rawlsing_next/tests/test_rrif_e1_c3_d01_declared_encoding_admission.py \
  rawlsing_next/tests/test_rrif_e1_c3_d02_opaque_datetime_carrier.py \
  rawlsing_next/tests/test_rrif_e1_c3_current_integration_regressions.py \
  rawlsing_next/tests/test_universal_source_byte_custody.py \
  rawlsing_next/tests/test_pre553_sr06_decoder_carrier.py \
  rawlsing_next/tests/test_fiabc_lm1_r1e_n1_physical_boundary.py \
  rawlsing_next/tests/test_fiabc_lm2_r1j_sav_representation_authority.py \
  rawlsing_next/tests/test_fiabc_lits_i_representation_authority.py \
  rawlsing_next/tests/test_universal_source_projection.py \
  rawlsing_next/tests/test_universal_workload.py \
  rawlsing_next/tests/test_r35_i01_physical_metadata.py \
  rawlsing_next/tests/test_pre553_source_backed_c11_facade.py \
  tests/test_ee_p2x_darwin_court_driver.py \
  tests/test_fiabc_final_measurement_telemetry_closure.py
```

Result:

```
194 passed, 1 skipped in 139.20s (0:02:19)
```

Exit `0`. The skip is the same environmental pyreadstat writer limitation recorded by E1/E4/E4F.

Log: `rrif_f0_e4f_selected_194.log`, 283 bytes, sha256 `87bc077062e8cffcc7cfc41aedfa42a6e5ff8a3f3c3ff159d1fc4fdc07e93942`.

This confirms receiving-shape feasibility. It is not an independent E4FR review and does not approve the candidate.

## 4. E5 receiving-shape preflight

Worktree: `/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/rrif-f0-e5-96e6d49ac` at `96e6d49ac...`.

The frozen S06FR overlay was extracted from `1b5b6072...:rawlsing_next/tests/test_hq284_s06fr_native_review.py` (blob `a25cf5a5ecec4b473ccceaec8a032747d804da7d`, sha256 `fea7cb29f6056996fd999cf50ddc227671024946e32af313f7954b1d30eecf30`). The E2 test is the E5 file at blob `9a469ad0940216e02967c94159db943d2979154a`.

### 4.1 Unfiltered full court

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. python3 -m pytest -q -p no:cacheprovider --tb=line -rA \
  --junitxml=/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/rrif_f0_e5_unfiltered.xml \
  rawlsing_next/tests/test_pre553_learned_product_lifecycle.py \
  rawlsing_next/tests/test_pre553_learned_product_release.py \
  rawlsing_next/tests/test_pre553_s06g_atomic_integrity.py \
  rawlsing_next/tests/test_pre553_e5_s06g_independent_hostile.py \
  rawlsing_next/tests/test_pre553_ee14_selected_current_asof_hq260.py \
  rawlsing_next/tests/test_pre553_learned_world_composition.py \
  /var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/rrif-f0-overlay/test_hq284_s06fr_native_review.py
```

Result:

```
14 failed, 179 passed in 17.54s
```

Exit `1`. No skips/errors. Per-court:

| Court | Tests | Pass | Fail |
|---|---:|---:|---:|
| Accepted B5 | 39 | 39 | 0 |
| Accepted M2 | 28 | 26 | 2 |
| S06G repair | 42 | 42 | 0 |
| E2 independent hostile | 10 | 10 | 0 |
| Adjacent EE14 asof + world | 45 | 45 | 0 |
| Frozen S06FR overlay | 29 | 17 | 12 |
| Total | 193 | 179 | 14 |

The two M2 failures are the unchanged accepted tests `test_17_binding_cannot_resolve_different_release` and `test_18_endpoint_failover_only_among_same_release`, failing with `M2ReleaseError: RELEASE_UNAVAILABLE` at foreign release/binding registration. The twelve overlay failures are preserved `OBSERVED` defect-presence assertions, not modern acceptance tests.

Log: `rrif_f0_e5_unfiltered.log`, 35236 bytes, sha256 `6448afa55d319e14a3fc740448e474e1e89d6bfd82ba746ae2c1139aa5f077ff`.

### 4.2 Filtered selection is not green

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. python3 -m pytest -q -p no:cacheprovider --tb=line \
  -k 'not OBSERVED and not test_17_binding_cannot_resolve_different_release and not test_18_endpoint_failover_only_among_same_release' \
  --junitxml=/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/rrif_f0_e5_filtered.xml \
  <same six local files and frozen overlay>
```

Result: `179 passed, 14 deselected in 12.40s`, exit `0`. This is a selection, not a green full suite. Log: `rrif_f0_e5_filtered.log`, 276 bytes, sha256 `9b947b6fbd0b66d22e85c235d22360b5ac78730eae8f3e264b03beb4853dc6d4`.

### 4.3 Collision check

E4F payload paths and E5 payload paths have an empty intersection. A non-mutating `git merge-tree --write-tree --messages` between exact E4F and exact E5 exited `0` with no conflict message and produced tree `d3faba8905802abb505e2cb1b1a7d3cf43b36bdc`. This proves path-level receiving feasibility, not merge authority.

Receipt: `rrif_f0_merge_tree.txt`, 42 bytes, sha256 `552ae5ce42e9e83553c721fb311b9c5f781cf625621cd4e260de9ecf140583fc`.

## 5. Minimal receiving preflight tool

Files:

- `receiving_preflight.py` — read-only Git observation plus a pure fail-closed evaluator.
- `test_receiving_preflight.py` — 12 synthetic gate tests.

Test command:

```sh
cd WORKER_RETURNS/PYAT_RRIF_F0_RECEIVING_PREFLIGHT_20261101_R1
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q -p no:cacheprovider test_receiving_preflight.py
```

Result: `12 passed in 0.03s`, exit `0`. Log: `rrif_f0_preflight_tests.log`, 99 bytes, sha256 `c90552887b15f0dd338283c6b09a470ebacdbd4677c68174867fe21155a8b633`.

The tests prove refusal for:

- absent reviewer receipt;
- reviewer branch still at PRE-MAIN or equal to candidate;
- reviewer not distinct, wrong reviewed SHA, missing receipt path;
- changed PRE-MAIN head;
- wrong before/after blob;
- changed file outside the allowlist;
- payload collision;
- missing M2 owner decision;
- wrong conflict-test set;
- filtered selection claimed as green;
- selected payload empty while any gate is blocked.

They also prove the only path to `receiving_ready` is both gates fully satisfied.

## 6. Live CAS preflight refusal

Command (from the F0 worktree, read-only against the canonical object database):

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  WORKER_RETURNS/PYAT_RRIF_F0_RECEIVING_PREFLIGHT_20261101_R1/receiving_preflight.py \
  --repo /Users/matthewsmith/Desktop/rawlsing_r02v_r2_canonical \
  --allowlist WORKER_RETURNS/PYAT_RRIF_F0_RECEIVING_PREFLIGHT_20261101_R1/EXACT_PATCH_PATH_AND_BLOB_ALLOWLIST.json \
  --premain-ref refs/remotes/origin/integration/pre-main-reconciliation-r1 \
  --json-out /var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/rrif_f0_live_pending.json
```

Result: exit `2`.

```
observed_premain_head: 8e44ca9c751049d65e6def47600b5c073ee04b29
g1_e4f_d02: BLOCKED
  REVIEWER_BRANCH_ABSENT
  MISSING_EXACT_INDEPENDENT_REVIEW_RECEIPT
  all five test receipts missing
g2_e5_s06g: BLOCKED
  REVIEWER_BRANCH_STILL_AT_PREMAIN_NO_RETURN
  MISSING_EXACT_INDEPENDENT_REVIEW_RECEIPT
  all six test receipts missing
  MISSING_M2_OWNER_COMPATIBILITY_DECISION
receiving_ready: false
selectable_payload: []
```

Log: `rrif_f0_live_pending.log`, 1673 bytes, sha256 `53382696e63a3b05e3c5c05ee37ec4bf3e4584dfdf6d2e05f0878ad7bd93b8bd`.

The E4FR branch was not even locally fetched at the time of this read-only check, so the gate correctly refused rather than inferring a review from the remote branch name. E6 existed locally at PRE-MAIN and was refused as "still at PRE-MAIN". This is the required no-match/CAS refusal.

## 7. Receipts required before selection

The integrator must supply a receipts JSON matching `receipts_template` in the allowlist. Minimum fields:

### E4F gate

- `review.verdict = ACCEPT`
- `review.reviewed_sha = f2c0af3273d612bff0a7bd2407532b52caf4348b`
- `review.reviewer_branch = review/pyat-rrif-e4fr-d02-corrected-consumer-hostile-20261101-r1`
- live reviewer SHA, distinct from author and candidate
- nonempty `receipt_path`
- `reviewer_distinct_from_author = true`
- test receipts: E1 33/0/0 PASS, E4F 12/0/0 PASS, selected 194/0/1 PASS, real SAV/DTA first seam PASS, G01 2 expected pre-existing failures with baseline-identical true.

### E5 gate

- E6 review exactly as above for `96e6d49ac18274332751c5fbb87c6ed370e8fd9c`.
- M2 owner decision `ACCEPT_FIXTURE_AMENDMENT`, binding the exact E5 SHA, both conflict tests, a named owner, and a decision reference.
- test receipts: unfiltered 179 passed/14 failed/2 accepted conflicts/12 historical defect presence; filtered 179/14 deselected marked `SELECTION_NOT_GREEN`; accepted B5 39/0; S06G 42/0; E2 10/0; adjacent 45/0.

## 8. Disabled approvals

The allowlist JSON records all disabled approvals, including:

- E1 alone;
- E4 rejection as acceptance;
- E4F before E4FR;
- E5 before E6 and the M2 owner;
- E5 filtered selection as green;
- wholesale branch cherry-pick/merge;
- old S06F owner, R9 broker, or G01 import;
- G01 repair/authority;
- source-native, actor, N11/N12, Sorok, PROGRAMMA;
- protected PRE-MAIN write/merge/force-push/branch deletion/self-adoption;
- scientific, source-rights, licence, issuer/use, release authority.

## 9. No protected write

The preflight uses `git rev-parse`, `git diff --name-only`, `git show`, and `git merge-tree` read-only. It does not checkout, fetch, merge, cherry-pick, write refs, delete branches, or execute source-native code. The test worktrees are detached and disposable.
