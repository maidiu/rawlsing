# COMMANDS AND EVIDENCE — W03/W04 economic method recheck

All local commands were run with:

```text
cd /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-w03-w04-mcr-economics-review-r1
```

or with an explicit `git -C /Users/matthewsmith/Desktop/Rawlsing_Worktrees/...` for read-only ref inspection. No production, existing-test, workflow, author, HQ, or protected file was edited.

## 1. Exact refs and source blobs

```text
git rev-parse --abbrev-ref HEAD
git rev-parse HEAD
git rev-parse 1d7007a34fdf9cb7cdd30ec581e7d94523047da7
git rev-parse 07f37e47893fdbc956766cea7d3ef550f064d8c7
git rev-parse f9aedf8e2b570174881cef627dc6a24b78031ed7
git rev-parse 46b7325637e68f78ccc7487d4b1abc7009c5ac0b
git rev-parse 4f3413fc5c37b589be3412f826bf8f68ee617d4a
git rev-parse 5a891a311c70f4cb8c09864008b33405362f7c7c
git hash-object rawlsing_next/bench_w03_w04_physical.py rawlsing_next/tests/test_bench_w03_w04_physical.py
git diff --stat 1d7007a34fdf9cb7cdd30ec581e7d94523047da7 dec934dde -- rawlsing_next/bench_w03_w04_physical.py rawlsing_next/tests/test_bench_w03_w04_physical.py
```

Results are recorded in `PROBE/source_and_evidence_hashes.txt`. The `1d7007a..dec934dde` source diff is empty; the exact source carries the repaired benchmark.

## 2. Commission and author evidence

```text
sha256sum PYAT_W03_W04_MCR_C_Commission.md
sha256sum WORKER_COMMISSIONS/PYAT_W03_W04_MCR_COMPLETION_R1/REQUIRED_OBLIGATIONS.tsv
sha256sum WORKER_RETURNS/PYAT_W03_W04_MCR_COMPLETION_R1/lanes/bench/ECONOMIC_R3/{evidence_summary.json,cap_falsifier.json,gate_no_baseline.json,current_81a4_64_both.json,baseline_protected_4f_64_both.json,warm_restarts_3.json}
```

The small author evidence was copied read-only into `EVIDENCE_AUTHOR_R3/` with its own `SHA256SUMS.txt`:

- `00_RETURN.md`, `01_METHOD_CORRECTION_MATRIX.md`, `02_EVIDENCE.md`, `03_REPRODUCIBLE_RETURN.md`
- `evidence_summary.json`
- `cap_falsifier.json`
- `gate_no_baseline.json`
- `warm_restarts_3.json`

The raw 64-row current/baseline receipts remain in the author lane; their exact hashes are recorded, and the review uses extracted values from those receipts.

## 3. Focused benchmark tests

```text
cd /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-w03-w04-mcr-economics-review-r1
TMPDIR="$PWD/WORKER_RETURNS/PYAT_W03_W04_MCR_COMPLETION_R1/reviews/economic-method-recheck/PROBE/TMP" \
PYTHONDONTWRITEBYTECODE=1 \
python3 -m pytest -q -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_bench_w03_w04_physical.py
```

Observed: `13 passed in 21.97s` (`PROBE/bench_focused.log`). The temporary test temp directory was removed after the run.

## 4. 64-row gate audit from author raw receipts

A read-only Python audit loaded:

```text
WORKER_RETURNS/PYAT_W03_W04_MCR_COMPLETION_R1/lanes/bench/ECONOMIC_R3/current_81a4_64_both.json
WORKER_RETURNS/PYAT_W03_W04_MCR_COMPLETION_R1/lanes/bench/ECONOMIC_R3/baseline_protected_4f_64_both.json
```

and called `bench_w03_w04_physical._acceptance_gate(current_results, baseline, Namespace(rows=64, repetitions=1, ...), current_source_head)`.

Output `PROBE/gate_64.json`:

```text
pass=false
cold_pass=true
cold_rss_improvement=0.38985324285939715
warm_pass=false
repeat_wall_ratio=1.4471204317004478
retention_decision=DO_NOT_RETAIN__NONBENEFICIAL_OR_REGRESSION_OR_MISMATCH
final_shape=false
regressions=[]
```

This matches the author's `00_RETURN`: cold wide diagnostic improvement 38.99%, warm repeat 1.447, no final pass.

## 5. Gate falsifiers

`PROBE/gate_other_regression_probe.json`: synthetic selected cold-wide/warm-repeat metrics, plus a 20% cold-narrow regression. Result: `pass=false`, with `REGRESSION_RSS_GT_10_PERCENT` and `REGRESSION_WALL_GT_10_PERCENT`. This shows the current universal regression ban; the frozen contract requires reporting and justified correction for other-profile >10% regressions.

`PROBE/gate_identity_and_cap_probe.txt`: synthetic baseline with only schema/source_head/rows/profiles/repetitions/host. Result: `pass=true`, no `actual_event_counts`, no command, no baseline sha256; `gate_keys` has no cap fields and no event/command/hash fields.

`PROBE/method_probe_summary.txt`: combines gate, warm-clock, cap, cold-policy, and derived-hit observations.

## 6. Warm-clock audit from raw 64-row receipts

Read-only extraction from `current_81a4_64_both.json` and `baseline_protected_4f_64_both.json`, full-matrix repeat warm:

```text
baseline 4f: parent_wall=2.8039397379616275, firstconsumer=0.1173207729589194,
             normal_current_cold_build=1.0187454270198941, canonical_reopen=0.3325802650069818
current 07f: parent_wall=2.723282056977041, firstconsumer=0.12202858598902822,
             normal_current_cold_build=0.45536904397886246, canonical_reopen=0.6877955499803647
baseline cold repeat: parent_wall=1.881862765061669, firstconsumer=0.12545281706843525
```

The gate uses `median_parent_wall_seconds`; the current warm parent includes canonical reopen/consumer after the derived first consumer. The 1.447 ratio therefore is not the frozen startup-to-first-consumer clock.

## 7. Cold no-policy vs inherited policy probe

Clean cold 16:

```text
cd /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-w03-w04-mcr-economics-review-r1
env -u RAWLSING_C11_ACCELERATOR_POLICY -u RAWLSING_C11_ACCELERATOR_DIR \
  PYTHONDONTWRITEBYTECODE=1 \
  python3 -m rawlsing_next.bench_w03_w04_physical \
  --scenario cold --profiles narrow --rows 16 --repetitions 1 \
  --source-root . --root "$L/clean_cold_root" \
  --jsonpath "$L/clean_cold_16.json"
```

Inherited-policy cold 16:

```text
RAWLSING_C11_ACCELERATOR_POLICY="$L/env_policy/accelerator-policy.json" \
  PYTHONDONTWRITEBYTECODE=1 \
  python3 -m rawlsing_next.bench_w03_w04_physical \
  --scenario cold --profiles narrow --rows 16 --repetitions 1 \
  --source-root . --root "$L/env_cold_root2" \
  --jsonpath "$L/env_cold_16b.json"
```

Observed:

```text
clean:             derived_cache_files=0, canonical_files=None, status=NO_GOVERNED_DERIVED_CACHE_WRITE,
                   cold_metric=56,971,264, process_peak=56,983,552
inherited policy:  derived_cache_files=0, canonical_files=None, status=NO_GOVERNED_DERIVED_CACHE_WRITE,
                   cold_metric=102,768,640, process_peak=102,780,928
                   actual file: env_policy/derived-accelerator/c11-events-f.parquet (22,412 B)
```

The hidden derived file is recorded with sha256 in `PROBE/env_policy_cache_observation.txt`, then removed. The zero base-root counters are not proof that no policy cache was written.

## 8. Same-size/same-mtime derived corruption probe

A small sourcefree `_build_release` probe wrote a derived parquet, flipped one byte while preserving size and mtime, and rebuilt. Output `PROBE/derived_envelope_probe.txt`:

```text
file c11-events-e.parquet
before_size 22412 before_mtime_ns 1794369225243866887
after_size 22412 after_mtime_ns 1794369225243866887
derived_hit True
derived_write False
status HIT_EXACT_ENVELOPE_AND_MTIME
release_refs_equal True
event_count 32
```

The derived-hit status is metadata-only; a same-size/same-mtime corrupt file is reported as an exact envelope/mtime hit.

## 9. Cap falsifier

Read from `EVIDENCE_AUTHOR_R3/cap_falsifier.json`:

```text
status=BLOCKED_EXACT_DEPENDENCY
blocked_reason=CHILD_RSS_EXCEEDED_AUTHORIZED_CAP_BEFORE_COMPLETION
cap_bytes=8388608
cap_enforced=true
cap_peak_sampled_bytes=15986688
returncode=-9
```

The monitor can kill an 8 MiB process; the acceptance gate does not require this cap evidence for a successful final run.

## 10. Three fresh warm processes

`EVIDENCE_AUTHOR_R3/warm_restarts_3.json` records:

```text
warm PIDs: 78863, 78906, 78951
derived hits: true, true, true
canonical hits: true, true, true
cache_write_amortization: 0.06812232499942183
```

This is a 16-row narrow diagnostic. The amortization is canonical-only (`0.204367/3`); the derived write is not separately timed.

## 11. What was not run

No 100k matrix, no final three-repetition three-profile matrix, no original source/respondent/SAV/DTA/DB/native workload, no production/test/workflow edit, no merge, no installation, no new worker, no model/provider/account/effort change. CI/proof CC-F03/F04 and the independent cold-order/MCR-validator work are outside this review.

The exact source at `dec934dde` is available for the final pinned run, but this review does not accept the final source or evidence.
