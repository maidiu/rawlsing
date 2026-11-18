# NEXT EXECUTABLE COMMAND — ROUTING MATCHED RUNNER

PREP ONLY; not run. Use the exact frozen repaired routing candidate, not `73b480...` (rejected REVISE_EXACT_DEFECT).

```bash
python3 WORKER_RETURNS/ANVIL_ROUTING_MATCHED_RUNNER_20261118/routing_matched_runner.py \
  --baseline-commit 68aa7cac7cce7057fefd458ef4a06bec2dede1b2 \
  --candidate-commit <FROZEN_REPAIRED_ROUTING_COMMIT> \
  --outdir WORKER_RETURNS/ANVIL_ROUTING_MATCHED_RUNNER_20261118/RUN_<SHORT_SHA>
```

The runner creates distinct temporary snapshots from the two exact commits, launches one fresh process/session per variant, runs `f2_forward_raw` and `f2_reverse_raw` once each on the frozen WIDTH128 estate, and writes per-variant JSON plus `COMPARISON.json`. It compares exact full payloads, fact/replay/provenance refs, cells and risk/denominator identity sets; it reports H/S/Q/O, setup vs operation routing work, row-group/file counters, scratch/RSS samples and total setup+operation cost. Baseline and candidate are never the same session with an adapter disabled.

Caps: per child 600 s, total 900 s, process-tree RSS 6 GiB, scratch 4 GiB, 0.25 s sampling/process-group abort. One measured pair only; no rebuild, no matrix, no extrapolation/speedup claim. Sourcefree TEST_ONLY; no native/source/science/actor/CURRENT/protected acceptance.
