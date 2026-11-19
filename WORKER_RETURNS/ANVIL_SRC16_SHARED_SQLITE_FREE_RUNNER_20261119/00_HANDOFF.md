# SRC16 common supervisor injection — corrected call path

## Readiness

- **KEYED TEST_ONLY SOURCE THROUGH THE ACTUAL COMMON SUPERVISOR: PASS**
- **TWO DISTINCT CHILD PIDS: PASS**
- **SRC16 METADATA PREFLIGHT/NEGATIVE RESOLVER: PASS**
- **SRC16 NORMAL INITIAL BUILD: READY-INPUT, NOT RUN**
- **KEYED NO-DECODE RESUME: NOT PROVEN (honest residual)**
- No original source access or launch by this worker.

## Corrected call path

The previous `generic_cli.py --mode src16-run` direct `build_single_pass` call
was removed. `src16-run` now writes a private source profile and invokes:

`common/sqlite_free_witness.py --mode run --source-adapter <private-profile>`

The existing common supervisor then:

1. starts its producer child with the same source adapter;
2. samples RSS/free-space and waits for producer exit;
3. starts its native reader child with the same source adapter;
4. writes existing supervisor/reader logs, progress and caps.

The source adapter loads the exact per-wave config and active resolver, and
compares the selected source path to the exact private grant **before decode**.
No alternate source-path override exists in the child path.

The common sourcefree branch remains valid and is compatible with this adapter.

## Key pass-through

`common/sqlite_free_single_pass.py` derives
`row_native_keys_from_transport` from the same admitted incidence and passes the
keys to the existing projection and spooling path. No production projection
monkeypatch and no extra decode are used.

## Actual keyed supervisor evidence

The TEST_ONLY keyed source profile was injected into the actual common CLI:

```json
{"schema":"ANVIL_ALL35_WITNESS_SUPERVISOR@1","status":"COMPLETE",
 "producer_exit":0,"reader_exit":0,"abort":null,
 "elapsed":1.7374180470360443,"samples":6,
 "rss_peak":100347904,"free_min":37034422272,
 "caps":{"rss":6442450944,"startup_free_floor":26907826727,
 "in_flight_free_floor":8589934592,
 "staging_budget":18317892135,"wall_cutoff":null}}
```

Child receipts prove:

- producer PID `77002`; reader PID `77010`; **distinct PIDs**;
- producer/reader counts equal: 6 identities/events/routing/coordinates,
  1 universe, 1 question, 7 authority snapshots, 0 weights;
- no `.sqlite` artifact.

The earlier direct helper pass is not used as the acceptance evidence.

## SRC16 metadata preflight and denial

Exact SRC16 metadata:

- source SHA `e368fc0f…`
- config file `1106de3e…`, canonical `c26e8e71…`
- 1,613 rows / 216 physical slots / 157 response slots / 2 coordinates /
  0 weights
- construction-only, `CURRENT_GRANTED`, no revocation
- exact request admitted
- other source / analysis purpose / incorrect scope refused with
  `EXACT_REQUEST_MISMATCH`
- source read: false

A real common-producer adapter denial was also executed with a denied purpose
before any decode:

```json
{"code":"BindingRefusal","detail":"EXACT_REQUEST_MISMATCH","status":"REFUSED"}
```

No source bytes were opened.

## Exact owner launch form

Private environment values are supplied only by the owner and are not published:

```bash
ANVIL_CANDIDATE_TREE="$PRIVATE_CANDIDATE_TREE" \
ANVIL_CANDIDATE_PATCH="$PRIVATE_CANDIDATE_PATCH" \
ANVIL_SRC16_GRANT_DIR="$PRIVATE_SRC16_GRANT_DIR" \
ANVIL_SRC16_CONFIG="$PRIVATE_SRC16_CONFIG" \
ANVIL_SRC16_SOURCE_PATH="$PRIVATE_EXACT_SRC16_SOURCE" \
PYTHONPATH="$PRIVATE_CANDIDATE_TREE:$RETURN/common:$RETURN" \
python3 "$RETURN/generic_cli.py" --mode src16-run --root "$PRIVATE_WORK_ROOT"
```

This routes through the common supervisor; it is not a direct build command.
Owner launch is not performed by this worker.

## Residual

Only the keyed **no-decode resume** path lacks an explicit typed-key witness
checkpoint test. Normal initial build and sourcefree keyed supervision are
tested. This is not a new grant, scientific, or alternate-lifecycle issue.

## Files

- `common.patch`
- `common/sqlite_free_single_pass.py`
- `common/sqlite_free_witness.py`
- `common/source_adapter.py`
- `common/sourcefree_fixture.py`
- `common/streaming_estate.py`
- `generic_cli.py`
- `sourcefree_supervisor.out`
- `keyed_adapter_supervisor.out`
- `sourcefree_test.out`
- `src16_metadata_test.out`
- `src16_denial.out`
- `receipt.json`

No original source read/run, private path/config/grant publication, per-wave
lifecycle, protected edit, new GSS writer, Q2/science, or DHIKR was added.
