# Bench lane return — W03/W04 physical economy

**Author status:** `INCOMPLETE`
**Lane:** `pyat-w03-w04-mcr-bench-r1`; existing OpenCode DeepSeek V4.1 Flash MAX session/model, no worker/model/provider/effort switch.
**Worktree:** `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-w03-w04-mcr-bench-r1`
**Branch:** `agent/pyat-w03-w04-mcr-bench-r1`

## Start/PR/source state

- Observed dispatch anchor: `a5f21266a91b9b00041a1fbdc6a31d5bc0949fe4`. It is a **contract-only, source-less anchor** (HEAD tree has only the three MCR files). I did not silently treat that as the frozen source.
- Source was restored from the exact source-anchor commit `1b0c8dc4c4c6350aa77f70fea9470f5b18aa21dc`; `git diff 46b73256..1b0c8dc4 -- rawlsing_next` is empty. The three contract files are present.
- Frozen PR895 source: `46b7325637e68f78ccc7487d4b1abc7009c5ac0b`; remote `refs/pull/895/head` readback remains `46b73256`.
- Contract source: `5a891a311c70f4cb8c09864008b33405362f7c7c`.
- Protected baseline: `4f3413fc5c37b589be3412f826bf8f68ee617d4a`.
- Reviewed compact blobs retained: production `986f327aa18053edc61bd837cdded02bbf8388d9`; test `8e8effa58579af0c3326ecd4af7e159947abe4ec`. Prior review `9999c0afac5d7d7eb72ad0df602da4b232a49565` read; no reacceptance.

## Delivered

- `rawlsing_next/bench_w03_w04_physical.py` — full CLI:
  `--scenario cold,cells-and-hash,full-matrix --profiles narrow,wide,repeat --rows 100000 --repetitions 3 --jsonpath`.
- `rawlsing_next/tests/test_bench_w03_w04_physical.py` — 7 focused benchmark tests.
- `.github/workflows/pyat-w03-w04-physical-economy.yml` — selected W03/W04 tests plus 256-row full-matrix smoke; smoke explicitly is not 100k acceptance.
- `WORKER_RETURNS/PYAT_W03_W04_MCR_COMPLETION_R1/lanes/bench/` — compact machine receipts, full raw hashes, resource comparison, prior-capital/ABI proof.

All profiles use the existing governed physical-cell → projection → I02/C11 validation/seal → compact → real `CarrierNeutralResearchExecutor` I03/I05 path. Full-matrix also uses `ParquetC11Carrier` persist/reopen and fresh-process delete/rebuild. No hand-built statistical oracle, second C11 engine, production source carrier/engine edit, or alternate query engine.

## Actual measurements

Selected tests: **50 passed** (`test_bench_w03_w04_physical.py` plus the selected W03/W04 regression set) in 16.81 s.

1,000-row paired matrix (one fresh process per section; current 46b vs protected 4f3413):

| Profile | Cold wall / RSS | Warm wall / cache |
|---|---|---|
| narrow | 8.17 s / 197.7 MB vs 6.998 s / 210.2 MB; cold wall **+16.7% regression** | 4.44 s vs 4.08 s; cache hit |
| wide | 16.76 s / 344.6 MB vs 17.96 s / 379.3 MB (−6.7%, −9.1%) | 7.79 s vs 9.54 s (−18.4%) |
| repeat | 20.15 s / 345.9 MB vs 20.30 s / 381.2 MB (−0.7%, −9.3%) | 11.38 s vs 13.18 s (−13.6%) |

100,000-row narrow cold (same fixture/host; current 46b vs protected 4f3413):

- current: **777.53 s**, **5,923,426,304 B** peak, 300,000 cells, `SUPPORTED` fact
- protected: **997.04 s**, **5,240,467,456 B** peak, 300,000 cells, `SUPPORTED` fact
- wall ratio **0.7798**; **RSS ratio 1.1303 = +13.0% cold-RSS regression**

**The user's >=15% cold-median-RSS target is not met.** The 100k narrow wall improved, but its RSS regressed. No PASS is claimed. The narrow cold wall regression and 100k RSS regression are preserved in `proof_02_resource_comparison.json`.

## Remaining boundary

- `100000` wide and repeat, and the final three-repetition candidate matrix, are **NOT_RUN**; they must run at an HQ-pinned integrated candidate head, not this pre-integration 46b source.
- Final target requires >=15% cold median RSS and repeat-heavy warm wall <=90%; current measurements do not satisfy it.
- No 100k downsizing is labeled as a pass. The 100k narrow child remained under 6 GiB; no cap failure occurred. The benchmark enforces the declared measurement cap when the platform exposes RLIMIT_AS.
- Independent code/resource review at final immutable head remains required. Whole 12-ID MCR coverage and protected receiving remain HQ/integration responsibilities; this lane does not claim all 12 passed.
- Grouped/Batch/P41 are `NOT_APPLICABLE` to this selected sourcefree physical fixture; no handbuilt substitute is used. No original35/source/native/science/actor effect, source-byte copy, S3, protected merge, CI waiver, new worker, model change, or production/existing-test/HQ/peer write.
- Quota UNKNOWN.

## Exact code blobs

```text
eeb60c1a46db3ed072ec333dfd5d075fda3f71c0  rawlsing_next/bench_w03_w04_physical.py
d487c413507f2834a411351ae47d41abd7d6227f  rawlsing_next/tests/test_bench_w03_w04_physical.py
a12f5dcde35f4d89ff281f1ec2f02200c4ac2e36  .github/workflows/pyat-w03-w04-physical-economy.yml
```

The final remote SHA is reported in the terminal return after the lane-only commit and push.
