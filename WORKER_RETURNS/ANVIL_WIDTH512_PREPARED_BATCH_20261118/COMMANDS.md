# WIDTH512 prepared Batch commands

From `/Users/matthewsmith/Desktop/ANVIL_ENGINEERING_EXECUTION_20261117/OWNER`:

```bash
python3 WORKER_RETURNS/ANVIL_WIDTH512_PREPARED_BATCH_20261118/run_width512_batch.py
```

The script checks the sealed contract and 14 manifest members, verifies the
exact I02/release/family and exact WIDTH512 F2 operation refs, rejects a
competing WIDTH512 writer, materializes the exact fixture/query catalog, and
supervises one child running the existing repaired driver against the retained
estate. It enforces 600 s child, 6 GiB RSS, 4 GiB scratch, >=8 GiB free and
process-group termination; there is no retry after native start.
