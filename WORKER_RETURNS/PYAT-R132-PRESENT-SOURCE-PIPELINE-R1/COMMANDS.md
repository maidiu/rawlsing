# R132 — exact commands

Run from `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/r61-r01`.

## Actual bounded attempt (executed)

```sh
env PYTHONPATH=. python3 \
  WORKER_RETURNS/PYAT-R132-PRESENT-SOURCE-PIPELINE-R1/runtime/r132_present_pipeline.py \
  --output .r61/r132-present-source-pipeline/attempt/no_runtime.json
```

Observed: exit `2`, status
`BLOCKED__CURRENT_NATIVE_RUNTIME_MODULE_NOT_PROVIDED`, source read `false`.
The wrapper validates the local S44 handoff and imports the current native
`rawlsing_next.pre553_issued_workload` API; it does not read source.

## Execute only after the exact current runtime is supplied

```sh
RUNTIME_MODULE=<operator-authenticated-runtime-module> \
env PYTHONPATH=. python3 \
  WORKER_RETURNS/PYAT-R132-PRESENT-SOURCE-PIPELINE-R1/runtime/r132_present_pipeline.py \
  --runtime-module "$RUNTIME_MODULE" \
  --output .r61/r132-present-source-pipeline/attempt/admitted_run.json
```

The module must provide exactly:

- `resolver` — `CurrentDecisionResolver` returning the exact current
  `IssuedWorkloadRecord`;
- `workloads` — a mapping containing `SRC27` as `NativeWorkload` or tuple of
  such packets;
- `source_factory` — exact source factory bound to the admitted workload;
- `host` and `purpose` — authenticated strings matching the current decision.

The native call is:

```python
result = execute_issued_workload(
    workload,
    runtime.resolver,
    source_factory=runtime.source_factory,
    host=runtime.host,
    purpose=runtime.purpose,
    allow_test_only=False,
    prior_receipts=(),
    max_units=None,
)
```

The source factory is called only after current admission.

## Missing owner decisions

`SRC27:SOURCE_HOST_PURPOSE`, `SRC27:COMPLETE_NATIVE_U`,
`SRC27:RESPONSE_ROUTING_CARRIER`, `SRC27:SCIENTIFIC_E_PRE`,
`SRC27:CONSUMER_PURPOSE`.

The current source edition/host/purpose, scientific U/Epre, and consumer scope
must be issued by their competent owners. The historical AS2B LiTS-I source
identity in the S44 handoff is evidence only and does not authorize a fresh read.

## Not executed

No raw source read, decoder, sample expansion, checkpoint replay, source-free
fixture run, new engine, CI/prod action, or FF/V553 consumer.
