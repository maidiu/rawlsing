# Actual Lane A native carrier — receipt adapter

`actual_carrier.py` consumes the actual Lane A durable product format without
storage conversion or a source reread:

- `public_objects.pkl` — native public C11 objects
- `internal_records.pkl` — native internal C11 records
- `replay_manifest.json`
- bundle `receipt.json` / `LOCAL_RELEASE_RECEIPT.json`
- `RELEASE_RECEIPT.json`
- `PRIMARY_RUN.json`

The adapter requires all three receipt/primary files, exact receipt SHA-256
pins, stream byte hashes and line counts, replay-manifest identity, source and
release identity, source-release manifest hash, M01–M18 coverage, and the
recomputed semantic release hash. It then rehydrates the native
`C11LogicalRelease` through the existing native C11 factory and serves it to the
same issuer/executor.

A missing or incomplete product returns a precise pending/refusal record. It
does not read a growing bundle or treat a metadata-only receipt as success.

## Exact execute command

```sh
PYTHONPATH=. python3 campaign_src04_completion/empirical/run_native_workload.py \
  --mode execute \
  --carrier-receipt <LOCAL_RELEASE_RECEIPT.json> \
  --carrier-receipt-sha256 <exact> \
  --release-receipt <RELEASE_RECEIPT.json> \
  --release-receipt-sha256 <exact> \
  --primary-run <PRIMARY_RUN.json> \
  --primary-run-sha256 <exact> \
  --source-sha 2a48ba4b2f23d022a2dfe4b8a0cc685febbd82579b5434f9ecd96ed4c1243d18 \
  --consumer
```

`--bundle-dir` may be supplied when the receipt is not stored beside the pickle
streams. The previous Parquet carrier option remains available for other
products but is not required.

## Focused native proof

`test_authorized_execution.py` writes a real native pickle carrier from the
labelled nonrespondent fixture, reloads it through this adapter, and verifies
the release identity. It also mutates the public stream and requires an exact
refusal. This is transport/identity discrimination only, not original SRC04
qualification.

## D consumer

Execution assembly imports the accepted Lane D consumer as a read-only
dependency. The bridge creates the exact `ProducerBundle` and bounded discovery
when Lane D is joined. If the dependency is absent, the exact status is
`D_CONSUMER_DEPENDENCY_NOT_JOINED`; no D author files are modified.
