# SRC16 shared SQLite-free runner — real key wiring

## Readiness

- **KEYED SOURCEFREE THROUGH THE ACTUAL COMMON SUPERVISOR/PRODUCER/READER: PASS**
- **SRC16 EXACT METADATA ADMISSION/NEGATIVE RESOLVER: PASS**
- **SRC16 NATIVE SOURCE: READY-INPUT, NOT RUN; checkpoint key-resume remains a separate proof**
- No original source access or launch by this worker.

## Surgical common-operator patch

Patch target: `MEASUREMENT_PREP@1f8b61b81…`.

`common/sqlite_free_single_pass.py` now:

- derives `row_native_keys_from_transport` from the **same already-admitted
  incidence**;
- passes those keys through the existing projection and spooling calls;
- no second decode and no production-projection monkeypatch.

`common/sqlite_free_witness.py` now has one common `--sourcefree` branch:
the existing supervised `--mode run` creates its child producer, waits for
producer exit, then launches the real fresh reader. It uses the existing
progress file, stderr logs, RSS/free-space caps and supervisor receipt.

`generic_cli.py` is the per-wave source adapter/CLI:

- `sourcefree`: shared common build/reader path with a generated keyed fixture;
- `src16-metadata`: exact config load plus exact existing private resolver
  admission/negative checks;
- `src16-run`: exact config/source/binding/request injection into the same
  common `build_single_pass`; provided for owner launch only.

Private SRC16 paths/config values/grant bytes are read only from owner-supplied
environment variables and are never printed or Git-published. The explicit
SRC16 key refusal was removed because the common build now injects keys.

## Actual supervisor evidence

Command (private candidate tree is supplied by env; no private path published):

```bash
ANVIL_CANDIDATE_TREE="$PRIVATE_CANDIDATE_TREE" \
PYTHONPATH="$PRIVATE_CANDIDATE_TREE:$RETURN/common" \
python3 "$RETURN/common/sqlite_free_witness.py" \
  --mode run --sourcefree \
  --candidate-tree "$PRIVATE_CANDIDATE_TREE" \
  --candidate-patch "<exact candidate patch>" \
  --config "<unused sourcefree config path>" \
  --binding-dir "<existing binding dir>" \
  --work-root "$PRIVATE_WORK_ROOT"
```

Result:

```json
{"schema":"ANVIL_ALL35_WITNESS_SUPERVISOR@1","status":"COMPLETE",
 "producer_exit":0,"reader_exit":0,"abort":null,
 "elapsed":2.0158314689761028,"samples":7,
 "rss_peak":109633536,"free_min":37048590336,
 "caps":{"rss":6442450944,"startup_free_floor":26907826727,
 "in_flight_free_floor":8589934592,
 "staging_budget":18317892135,"wall_cutoff":null}}
```

Producer and reader receipts:

- keyed sourcefree: 10 identities/events/routing/coordinates, 1 universe,
  1 question, 7 authority snapshots, 0 weights;
- producer schema `ANVIL_STREAM_C11_ESTATE@1`;
- reader counts equal producer counts;
- no `.sqlite` artifact under the supervisor root;
- producer exit 0, producer gone before reader, reader exit 0.

The direct shared sourcefree CLI (`generic_cli.py --mode sourcefree`) also
passes with the common key path and no monkeypatch.

## SRC16 exact metadata admission

- source: SRC16 / GSS1972.sav
- source SHA-256 `e368fc0f…`
- config file SHA-256 `1106de3e…`
- canonical `c26e8e71…`
- 1,613 rows; 216 physical slots; 157 response slots; 2 coordinates;
  0 weights
- purpose/scope construction-only, `CURRENT_GRANTED`, no revocation
- exact private resolver admitted the exact request
- negative resolver cases: other source, analysis purpose, incorrect scope all
  refused with `EXACT_REQUEST_MISMATCH`
- source read: **false**
- no private path/config value/grant bytes printed.

## Native launch form — not run

```bash
ANVIL_CANDIDATE_TREE="$PRIVATE_CANDIDATE_TREE" \
ANVIL_SRC16_GRANT_DIR="$PRIVATE_SRC16_GRANT_DIR" \
ANVIL_SRC16_CONFIG="$PRIVATE_SRC16_CONFIG" \
ANVIL_SRC16_SOURCE_PATH="$PRIVATE_EXACT_SRC16_SOURCE" \
PYTHONPATH="$PRIVATE_CANDIDATE_TREE:$RETURN/common:$RETURN" \
python3 "$RETURN/generic_cli.py" --mode src16-run --root "$PRIVATE_WORK_ROOT"
```

The exact SRC16 key-slot pass-through exists in the common build now. Owner
launch is not performed by this worker.

## Residual

- The common build derives and uses keys in the normal one-pass path. Checkpoint
  serialization of exact typed key witnesses for a **keyed resume** is not yet
  proven; the existing compact checkpoint/resume remains valid for sourcefree
  non-keyed and its prior tests. This is the precise residual; no sourcefree
  fixture or source launch is blocked in the normal no-resume path.

## Files

- `common/sqlite_free_single_pass.py`
- `common/sqlite_free_witness.py`
- `common/sourcefree_fixture.py`
- `common/streaming_estate.py`
- `generic_cli.py`
- `sourcefree_test.out`
- `sourcefree_supervisor.out`
- `src16_metadata_test.out`
- `receipt.json`

No per-wave lifecycle, duplicate investigation, protected edits, DHIKR,
original source read, or new GSS writer was added.
