# Full-width writer stage diagnosis

## Verdict

**`DIAGNOSIS_INSUFFICIENT_FOR_SUBSTAGE__WRITING_AGGREGATE_ONLY`**

No cap receipt exists yet. `BUILD_SUPERVISION.json` records an earlier
`ModuleNotFoundError`, not a 600 s cap. The current stage file says only:

```text
stage = writing
context_seconds ≈ 0.00133
width_population_seconds ≈ 0.12537
```

That is not evidence the build hit any cap. No current-cap claim is made.

## Exact writer

Unchanged at accepted baseline `68aa7cac…`:

- `rawlsing_next/pre553_source_direct_parquet_estate.py`
- SHA-256 `068fc525b6c117fbb3feba52f740f7e764674ff0b2a78f52e5b649b5fafe643a`

`write_direct_estate` lines 460–602 wraps all thirteen family streams in one
`build_sourcefree_direct_i02` pass. The coarse `writing` stage covers:

1. `_Sink.add`/`flush`/`close` for all families and `_IndexSink` for event
   locators;
2. `build_sourcefree_direct_i02` full stream consumption and SQLite proof;
3. event locator census;
4. `_verify_emitted_physical_payloads` full physical re-read/hash/census;
5. manifest hashing/fsync, publication and directory fsync.

The stage file cannot distinguish these. If the supervisor hits 600 s, it can
report only `stage="writing"`, not which mechanism consumed the time.

## Observable partial stage

One read-only observation of `.local-data-width512/.s2c-stage-f5vlsu4x` showed:

- `RespondentIdentity.parquet` 99,217 B
- `RespondentEvent.parquet` 73,836,555 B
- `event_locator.parquet` 18,602,867 B
- `QuestionVariableBinding.parquet` 100,778 B
- `.s2b-direct-stage-…tmp` **1,200,836,608 B**
- `.s2b-direct-stage-…tmp-journal` 12,542,328 B

This proves the one-pass writer/I02 proof phase was active and that a large I02
proof scratch existed. It does **not** attribute wall time to sink writes versus
I02 proof. No polling or wait was performed.

## Historical granularity

| Build | Wall | RSS peak | Scratch peak | Stage split |
|---|---:|---:|---:|---|
| 10k×5 | 210.423 s | 234,422,272 B | 535,740,432 B | total only |
| 128×600 | 293.956 s | 200,609,792 B | 826,683,762 B | total only |
| 512×600 | unknown | unknown | unknown | `writing` only |

## Missing measurement

A precise attribution requires writer-internal timestamps/counts:

- per-family `_Sink.add` and `flush`;
- `_IndexSink.add`/`flush`;
- start/end and consumed rows for `build_sourcefree_direct_i02`;
- `_verify_emitted_physical_payloads`;
- manifest hash/fsync/publish;
- family file/row-group growth.

None exists in the current writer. Minimal nonproduction diagnostic: after a
cap/failure, inspect the retained stage directory read-only—family file
presence/sizes, Parquet footer rows/row groups, I02 SQLite temp/journal sizes,
and `BUILD_STAGES`/`BUILD_SAMPLES`. This localizes family/sink vs proof/publish
boundaries. Distinguishing `tap`/`_Sink` cost from I02 proof requires a
test-only harness around those internal boundaries; no product edit is justified.

## Concrete post-cap audit

No build is started or retried. If a cap receipt appears, run only:

```bash
find /Users/matthewsmith/Desktop/ANVIL_ENGINEERING_EXECUTION_20261117/MEASUREMENT_PREP/WORKER_RETURNS/ANVIL_WIDTH512_BOUNDED_CONSTRUCTION_20261118/.local-data-width512 \
  -maxdepth 3 -type f -exec stat -f '%N %z' {} \;
```

Then read Parquet footers of retained family files for row/row-group counts.
This is read-only metadata work.

No source/science/product rights. Correctness at
`aee95429609c372564e996c2d3d3eb30e9253cbf` / receipt
`bbc3114f70fa6948f4f3c6a55aa7d3cf5f23cef1` is not reopened.

**STOP for a cap receipt and read-only stage audit.**
