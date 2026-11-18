# Writer tap / I02 proof timing instrument

## Status

**Test-only instrument frozen. Smoke PASS. No writer build/benchmark/query ran.**

- Received diagnosis: `2bdd689698a404e728fc395bbdd3dfd6df989348`
- Unchanged writer: `68aa7cac…`
- Writer SHA-256: `068fc525b6c117fbb3feba52f740f7e764674ff0b2a78f52e5b649b5fafe643a`
- I02 proof SHA-256: `b70e9a49b5d0a2445ed76053b04579fa0cbede2717286c7708dfb6f18ff016d2`
- No product edit.

## Instrument

`timed_writer.py` loads the existing width512 harness and the unchanged writer,
then transparently wraps:

- `_Sink.add/flush/close`
- `_IndexSink.add/flush/close`
- `build_sourcefree_direct_i02`
- `_verify_emitted_physical_payloads`
- `write_direct_estate` total

It records per-family, per-boundary count and elapsed time. Progress is written
atomically every 8,192 add events; no per-row verbose output. A cap retains the
last bounded progress receipt, with incomplete spans left incomplete rather than
inferred.

### Nesting and limits

- `_Sink.add` includes `_Sink.flush`; flush is nested, not additive.
- `_IndexSink.add` includes flush.
- I02 proof includes tap/sink/index/proof work.
- `proof_residual_not_pure_sql` is proof elapsed minus sink/index add inclusive.
  It is **not pure SQL**; it includes validation, inserts, hashes and SQLite
  overhead.
- `writer_residual_after_proof_verify` includes setup, hashing, fsync and
  publication; it is not a single stage.

## Smoke

```text
PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 python3 -B \
  WORKER_RETURNS/ANVIL_WRITER_TAP_PROOF_TIMING_20261118/timer_smoke.py
```

Result: **PASS**, 8 synthetic events, derived buckets present, no native build.

## Later diagnostic command

Run later under a supervisor, with the same 512×600 geometry and a new unique
root; never touch the preserved `.local-data-width512` stage:

```bash
SNAP=/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/anvil-scale-06ulz7
MP=/Users/matthewsmith/Desktop/ANVIL_ENGINEERING_EXECUTION_20261117/MEASUREMENT_PREP/WORKER_RETURNS/ANVIL_ENGINEERING_MEASUREMENT_PREP_20261117
PYTHONPATH="$SNAP:$MP:$MP/vendor" PYTHONDONTWRITEBYTECODE=1 \
python3 -B /Users/matthewsmith/Desktop/ANVIL_ENGINEERING_EXECUTION_20261117/IMPLEMENTER/WORKER_RETURNS/ANVIL_WRITER_TAP_PROOF_TIMING_20261118/timed_writer.py \
  --snapshot "$SNAP" \
  --out <NEW_UNIQUE_OWNED_ROOT> \
  --respondents 512 --questions 600 \
  --progress <NEW_UNIQUE_OWNED_ROOT>/progress.json
```

Caps: 600 s build / 6 GiB RSS / 4 GiB scratch / 8 GiB free. One run, no retry.
Sourcefree only. The preserved stage and live Batch are not touched.

## Limits

No actual writer run, no new geometry, no benchmark/query, no product edit, no
source/science/protected authority. This is a measurement instrument only.

**STOP for one later supervised timed writer diagnostic.**
