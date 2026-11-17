# Snapshot reference

The full corrected candidate was extracted from exact target
`06e88a5ac7e4c14362a97a046f44e25d8eec4162` into this directory for guard
execution. The bulk tree was not retained in the review commit to avoid
duplicating the authoritative candidate; this directory retains its exact
120-file `PACKAGE_MANIFEST.target.json` and the verification log.

Reproduce the full snapshot with:

```
git archive 06e88a5ac7e4c14362a97a046f44e25d8eec4162 \
  WORKER_RETURNS/ANVIL_ARCHITECTURE_20261117 | tar -x -C R2_RECHECK/snapshot
```

The independent guard run is recorded in `../RUNS/v2_guard_baseline_independent.txt`;
the target manifest is 120/120 verified in `../RUNS/refs_target_manifest.txt`.
