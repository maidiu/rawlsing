# W03/W04 full-scale native handoff

**Status:** `DURABLE_HANDOFF_ACTIVE` — real baseline child launched; measurements incomplete; no acceptance is claimed.

**Candidate/execution cut:** `e06b5037846c2662e0f8500f391da4dc56364a5f`
**Protected baseline:** `4f3413fc5c37b589be3412f826bf8f68ee617d4a`
**Runtime benchmark blob:** `6c72f7d67c16fe79b9260032f6ace4085c6f1f3d`
**Benchmark test blob:** `c765799a1ed54d3f74283b1f493d8a3e5256d9e7`
**Host:** 16 GiB (`17179869184` bytes), same host node for baseline/candidate; 6 GiB (`6442450944` bytes) sampled-RSS cap.
**Disk observed before launch:** approximately 5.4 GiB free; the driver records exact free bytes and refuses below a 512 MiB safety floor without claiming a PASS.

## Baseline checkout

Reused existing read-only source-only sparse checkout:

`/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/pyat-w03-w04-baseline-4f3413`

`git rev-parse HEAD` is `4f3413fc5c37b589be3412f826bf8f68ee617d4a`; `git diff --quiet -- rawlsing_next` is clean. Only pre-existing untracked `__pycache__` directories exist. No other owner worktree is repurposed or wiped.

## Driver and native supervisor

Driver: `run_fullscale.py` in this directory. It runs one existing benchmark child at a time, records every child PID/argv/cwd/completion, saves the baseline JSON SHA-256 before candidate comparison, and writes raw receipts under `raw/`.

The driver uses the existing qualified CLI:

```text
python -B -m rawlsing_next.bench_w03_w04_physical
```

Exact serial stages:

```text
# 1. baseline combined
python -B -m rawlsing_next.bench_w03_w04_physical \
  --scenario cold,full-matrix --profiles narrow,wide,repeat \
  --rows 100000 --repetitions 3 \
  --source-root /private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/pyat-w03-w04-baseline-4f3413 \
  --root <native-run>/cache/baseline-combined \
  --jsonpath <FULL_SCALE_R1>/raw/baseline_combined_cold_fullmatrix.json \
  --cap-bytes 6442450944

# 2. candidate combined, exact baseline bytes
python -B -m rawlsing_next.bench_w03_w04_physical \
  --scenario cold,full-matrix --profiles narrow,wide,repeat \
  --rows 100000 --repetitions 3 \
  --source-root <candidate> \
  --root <native-run>/cache/candidate-combined \
  --jsonpath <FULL_SCALE_R1>/raw/candidate_combined_cold_fullmatrix.json \
  --baseline-json <FULL_SCALE_R1>/raw/baseline_combined_cold_fullmatrix.json \
  --cap-bytes 6442450944 --acceptance-gate

# 3. baseline cells-and-hash
python -B -m rawlsing_next.bench_w03_w04_physical \
  --scenario cells-and-hash --profiles narrow,wide \
  --rows 100000 --repetitions 3 \
  --source-root /private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/pyat-w03-w04-baseline-4f3413 \
  --root <native-run>/cache/baseline-cells \
  --jsonpath <FULL_SCALE_R1>/raw/baseline_cells_and_hash.json \
  --cap-bytes 6442450944

# 4. candidate cells-and-hash, exact baseline bytes
python -B -m rawlsing_next.bench_w03_w04_physical \
  --scenario cells-and-hash --profiles narrow,wide \
  --rows 100000 --repetitions 3 \
  --source-root <candidate> \
  --root <native-run>/cache/candidate-cells \
  --jsonpath <FULL_SCALE_R1>/raw/candidate_cells_and_hash.json \
  --baseline-json <FULL_SCALE_R1>/raw/baseline_cells_and_hash.json \
  --cap-bytes 6442450944
```

Baseline generation is diagnostic; its `NO_BASELINE`/non-gate result is never acceptance. Candidate combined is the only `--acceptance-gate` invocation. The candidate cells case is paired raw evidence, not a full-matrix acceptance substitute.

## Exact native launch

```text
cd /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-w03-w04-mcr-verifier-repair-r1
/usr/local/bin/python3 \
  /Users/matthewsmith/Desktop/Rawlsing_Controller/local-automation/launch.py \
  --binding WORKER_RETURNS/PYAT_W03_W04_MCR_COMPLETION_R1/lanes/bench/FULL_SCALE_R1/native/binding.json \
  --job WORKER_RETURNS/PYAT_W03_W04_MCR_COMPLETION_R1/lanes/bench/FULL_SCALE_R1/native/job.json
```

Native job/session: `NATIVE_W03_W04_FULLSCALE`; HQ recipient `01a15c1e-5446-7ef3-80bb-9ff5c2cb27da`; notify enabled; finite supervisor; no recurring model poll or goal wakeup. This is native OS process supervision, not original native science/actor execution.

## Expected evidence after actual run

- `raw/baseline_combined_cold_fullmatrix.json` and its external SHA-256 receipt.
- `raw/candidate_combined_cold_fullmatrix.json`.
- `raw/baseline_cells_and_hash.json` and `raw/candidate_cells_and_hash.json`.
- `proof_02_cold_rss.json` and `proof_10_resource_matrix.json` as lossless views/references of the combined raw candidate with command/provenance/raw SHA-256.
- `proof_03_cost_comparison.json` from the actual candidate cells result.
- `run_summary.json` with stage statuses, child PIDs/commands, cap evidence, disk, and acceptance outcome.

No proof_02/03/10 PASS placeholder exists yet. Final gate status and independent receiving remain pending.
