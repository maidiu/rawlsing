# Combined execution

## Exact environment

- Candidate checkout: `c8e739470beb0dc65ad70c419a906e483a12ca8f`, clean detached worktree before testing.
- Python 3.11.3 in a temporary venv with pytest 9.2.0, pandas 3.1.1, pyreadstat 1.3.7, pyarrow 26.0.1, duckdb 2.0.0.
- No GitHub Actions. No project dependency files changed.
- Exclusive local lease and environment: `evidence/LEASE.json`, `evidence/ENVIRONMENT.txt`.

## Combined command

One pytest process over all scoped packet files:

```bash
PYTHONPATH=$PWD PYTHONDONTWRITEBYTECODE=1 TMPDIR=<lease>/tmp \
python -B -m pytest -q -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_pyat940_s1b_b01_b04.py \
  rawlsing_next/tests/test_pyat940_s1b_b01_historical_parity.py \
  rawlsing_next/tests/test_pyat940_s1b_b04_projection_guard_repair.py \
  rawlsing_next/tests/test_pyat940_s1b_b05_b06.py \
  rawlsing_next/tests/test_pyat940_s1b_b07_b08.py \
  rawlsing_next/tests/test_pyat940_s1b_b08_wide_dta_cell_cap.py \
  rawlsing_next/tests/test_pyat940_s1b_b09.py \
  rawlsing_next/tests/test_pyat940_s1b_factory_key_repair.py \
  rawlsing_next/tests/test_pyat940_s1d_current_permissions.py \
  rawlsing_next/tests/test_pyat940_s1d_a_counter_cache_binding.py \
  rawlsing_next/tests/test_pyat940_s1d_b_cache_custody.py \
  rawlsing_next/tests/test_universal_workload_custody.py \
  rawlsing_next/tests/test_pyat940_s2f_a_counter_provenance.py \
  rawlsing_next/tests/test_pyat940_s2f_b_negative_and_multisource.py \
  rawlsing_next/tests/test_pyat940_s2f_durable_closure.py \
  rawlsing_next/tests/test_pyat940_s2f_fresh_process.py \
  rawlsing_next/tests/test_pyat960_s2g_a_counter_subset.py \
  rawlsing_next/tests/test_pyat960_s2g_b_adversarial.py \
  rawlsing_next/tests/test_pyat960_s2g_b_repair_mr01.py \
  rawlsing_next/tests/test_pyat960_s2g_durable_lifecycle.py \
  rawlsing_next/tests/test_pyat960_s2g_fresh_process.py \
  rawlsing_next/tests/test_pre553_source_backed_c11_facade.py \
  rawlsing_next/tests/test_universal_workload.py \
  rawlsing_next/tests/test_pre553_empirical_query.py
```

## Results

- First combined run: **202 passed, 0 failed, 0 skipped**, 806.16 s (`evidence/combined_suite.log`).
- Independent monitored rerun: **202 passed, 0 failed, 0 skipped**, 633.94 s (`evidence/combined_suite_monitored.log`).
- Monitored process-tree peak RSS: **434,765,824 B**; scratch peak **53,653,504 B**; 1,042 samples (`evidence/combined_resources.json`).
- The combined count is the actual count of this one command. It is not a sum of packet-specific counts.

## Vertical evidence

The scoped combined execution includes actual native consumers; no mock producer was substituted. The strongest joined multi-packet vertical is native/S2-F→S2-G:

- S2-G resource harness: process-tree peak RSS **112,549,888 B**; retained disk **32,499 B**; cold/repeat **0.08735/0.08464 s**; `source_opens=0`; artifact files 2; logical 283,854 B; consumer `2690cdbeadabb0e90179d726029fa8b765995a15a1da26d7fe72bba0819bd597` (`evidence/s2g_resources.out`).
- MR01 wrong-release case: **REFUSED** with `consumer determinant release is not the selected fact source release`.
- Valid multi-release matching-release positive: consumer `879ea8e7710178b2dd02fe71ec2f1a7f1bcf02da33b40912c1e42eb505762660`, S2-F root `8ab33706…`.
- S1-B and S1-D are exercised in the same process but are not claimed as a single invented cross-packet chain with S2-F/S2-G.

## Known out-of-scope RED

`rawlsing_next/tests/test_universal_world_binding.py`: **17 passed, 1 failed** in 580.18 s. Exact error:

```text
TypeError: resume_joined_workloads() missing 1 required keyword-only argument: 'resolver'
```

This is the frozen S1-D `BLOCKED_OWNERSHIP` caller, outside the literal grant. It is preserved and excluded from the 202 count; the scoped aggregate is not a whole-repository green claim.
