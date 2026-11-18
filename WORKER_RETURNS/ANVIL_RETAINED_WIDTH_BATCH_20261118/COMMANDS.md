# Exact retained WIDTH128 Batch commands

From `/Users/matthewsmith/Desktop/ANVIL_ENGINEERING_EXECUTION_20261117/OWNER`:

```bash
python3 WORKER_RETURNS/ANVIL_RETAINED_WIDTH_BATCH_20261118/run_retained_width_batch.py
```

The script performs the exact preflight, materializes the existing fixture/query
catalog, extracts exact code `aee95429609c372564e996c2d3d3eb30e9253cbf` to a
read-only snapshot, and supervises one child:

```bash
python3 WORKER_RETURNS/ANVIL_FULL_WIDTH_BATCH_PREP_20261118/full_width_batch_driver.py \
  --snapshot /tmp/anvil_retained_width_snapshot \
  --contract WORKER_RETURNS/ANVIL_RETAINED_WIDTH_BATCH_20261118/sealed_contract.json \
  --runtime-catalog WORKER_RETURNS/ANVIL_RETAINED_WIDTH_BATCH_20261118/runtime_catalog.json \
  --current-authorizer width_current_scope:authorize \
  --baseline MEASUREMENT_PREP/WORKER_RETURNS/ANVIL_ROUTING_MATCHED_RUNNER_20261118/RUN_aee95429609c/baseline.json \
  --out WORKER_RETURNS/ANVIL_RETAINED_WIDTH_BATCH_20261118/BATCH_RESULT.json
```

The supervisor enforces: 240 s child, 6 GiB RSS, 4 GiB scratch, >=8 GiB free,
process-group termination, and no retry after a started Batch.
