# SRC16 common supervisor — native row-group correction

## Readiness

- **NATIVE SRC16 ADAPTER PRODUCER CHUNK ROWS: 512** (default corrected)
- **TEST_ONLY SOURCEFREE CHUNK ROWS: 2** (kept for fixture test only)
- **KEYED TEST_ONLY SOURCE THROUGH THE ACTUAL COMMON SUPERVISOR: PASS**
- **TWO DISTINCT CHILD PIDS: PASS**
- **SRC16 METADATA-ONLY PROFILE RESOLUTION VIA ACTUAL ADAPTER: PASS**
- **SRC16 NATIVE INITIAL BUILD: READY-INPUT, NOT RUN**
- **KEYED NO-DECODE RESUME: NOT PROVEN (honest residual)**
- No original source access or launch by this worker.

## Scale defect corrected

The actual source-adapter producer branch in
`common/sqlite_free_witness.py` previously passed `chunk_rows=2` for every
adapter profile. That produced tens of thousands of tiny Parquet row groups on
a real source and invalidated real performance/storage.

The branch now uses:

```python
chunk_rows=(2 if prof.kind == "sourcefree" else 512)
```

The real SRC16 adapter therefore uses the existing native 512-row default.
The sourcefree TEST_ONLY path keeps 2 where the fixture requires it. No gate,
benchmark, source read, or launch was added.

## Corrected call path

`generic_cli.py --mode src16-run` still routes to the existing common
supervisor; it does not call `build_single_pass` directly:

`common/sqlite_free_witness.py --mode run --source-adapter <private-profile>`

The common supervisor starts the producer child with the same adapter, waits
for producer termination, then starts the native reader child with the same
adapter. Existing caps, progress, and logs remain in force. The adapter checks
the exact config/current and requires the source path to match the exact
private grant before decode. No alternate source-path env override exists in
the child path.

## Sourcefree check

The actual common supervisor was run once with a keyed TEST_ONLY sourcefree
profile. Supervisor result:

```json
{"schema":"ANVIL_ALL35_WITNESS_SUPERVISOR@1","status":"COMPLETE",
 "producer_exit":0,"reader_exit":0,"abort":null,
 "elapsed":1.7461587350117043,"samples":6,
 "rss_peak":100450304,"free_min":38117892096}
```

Child receipts:

- producer PID `79174`; reader PID `79182`; **distinct PIDs**;
- producer/reader counts equal: 6 identities/events/routing/coordinates,
  1 universe, 1 question, 7 authority snapshots, 0 weights;
- no `.sqlite` artifact;
- TEST_ONLY chunk setting: 2.

## SRC16 metadata-only profile resolution

`generic_cli.py --mode src16-metadata` now constructs and resolves a source
profile through the **actual** `common/source_adapter.py` `Profile`; it no
longer relies on a standalone resolver helper. No source path is opened,
stat'ed, hashed, or decoded.

Result:

```json
{"status":"SRC16_METADATA_ADMISSION_PASS",
 "source_id":"SRC16","config_file_sha256":"1106de3e086032f5ac0b26fee0b56a147722399c80ac2841b70f0b851dea93b7",
 "config_canonical_sha256":"c26e8e71afbc629a9f19708cedb7b38cc2ba3cefb9ac53f11e0608044e64b534",
 "currentness":"CURRENT_GRANTED","revocation":null,
 "shape":{"rows":1613,"physical_slots":216,"response_slots":157,
 "coordinate_slots":2,"weight_slots":0},
 "negative_cases":[
 {"case":"other_source","code":"EXACT_REQUEST_MISMATCH","refused":true},
 {"case":"analysis_purpose","code":"EXACT_REQUEST_MISMATCH","refused":true},
 {"case":"incorrect_scope","code":"EXACT_REQUEST_MISMATCH","refused":true}],
 "source_read_performed":false}
```

A separate actual common-producer adapter denial with a denied purpose returned
`BindingRefusal: EXACT_REQUEST_MISMATCH` before decode. No source bytes were
opened.

## Exact direct common supervisor command

Private values are supplied only by the owner. The private profile is:

```json
{"kind":"src16","config":"$PRIVATE_SRC16_CONFIG",
 "binding_dir":"$PRIVATE_SRC16_GRANT_DIR",
 "source_path":"$PRIVATE_EXACT_SRC16_SOURCE"}
```

Exact command:

```bash
PYTHONPATH="$PRIVATE_CANDIDATE_TREE:$RETURN/common" \
PYTHONDONTWRITEBYTECODE=1 \
python3 -B "$RETURN/common/sqlite_free_witness.py" \
  --mode run \
  --source-adapter "$PRIVATE_SRC16_PROFILE" \
  --candidate-tree "$PRIVATE_CANDIDATE_TREE" \
  --candidate-patch "$PRIVATE_CANDIDATE_PATCH" \
  --config "$PRIVATE_SRC16_CONFIG" \
  --binding-dir "$PRIVATE_SRC16_GRANT_DIR" \
  --work-root "$PRIVATE_WORK_ROOT"
```

This is the direct common supervisor command; the owner launches it. It is not
run by this worker.

## Residual

Only the keyed **no-decode resume** path lacks an explicit typed-key witness
checkpoint test. Normal initial build and sourcefree keyed supervision are
tested. No new grant, scientific, or alternate-lifecycle issue was introduced.

## Files

- `common.patch`
- `common/sqlite_free_single_pass.py`
- `common/sqlite_free_witness.py`
- `common/source_adapter.py`
- `common/sourcefree_fixture.py`
- `common/streaming_estate.py`
- `generic_cli.py`
- `sourcefree_native_chunk.out`
- `sourcefree_native_chunk_receipts.json`
- `src16_native_metadata.out`
- `keyed_adapter_supervisor.out`
- `keyed_adapter_receipts.json`
- `sourcefree_test.out`
- `src16_metadata_test.out`
- `src16_denial.out`
- `receipt.json`

No original source read/run, private path/config/grant publication, per-wave
lifecycle, protected edit, new GSS writer, Q2/science, or DHIKR was added.
