# SRC04 SQLite-free construction cut

## Verdict

**Executable isolated cut complete.** The normal sourcefree path now writes typed
Parquet with streaming identity/coverage reconciliation, deterministic hashes
and Parquet footer checks. It does **not** build `.i02-proof.sqlite` and does
not run the synchronous read-back audit. The old SQLite path remains only as an
explicit separate audit in the parity test.

- Base: `bf59f7d708ea250445234776de318ddf620be6ea`
- Frozen writer/reader tree:
  `MEASUREMENT_PREP/private-runtime/SRC04_OVERLAY_REPLAY_1795040438/tree`
- Reviewed compact runner:
  `b3dd74d16c71f9f63b10510af041ec83a1b5c3de`
- No edit to the active candidate tree; PIDs 11521/11526 were not touched.
- No source file, original respondent data or staging was read.
- No source launch, giant benchmark, or DHIKR work.

## Files

- `streaming_estate.py` — normal sourcefree writer and fresh reader.
- `test_streaming_cut.py` — smallest sourcefree old/new parity and refusals.
- `sqlite_free_wiring.patch` — exact isolated descendant patch for
  `single_pass_handoff.py` (route normal and resume calls to the new writer).
- `evidence_metrics.json` — measured old/new fixture split.
- `test.out` — focused test output.

## Normal path

`write_streaming_estate()`:

1. consumes the 13 typed family streams once;
2. writes bounded Parquet row groups through the existing typed Parquet writer;
3. rejects duplicate exact refs through a compact temporary dbm identity index and rejects family census mismatch;
4. checks all required families and event-locator count;
5. hashes members and checks each Parquet footer row count;
6. writes an atomically unpublished staging directory and a deterministic
   stream proof manifest;
7. publishes only after ordinary invariants pass.

No SQLite connection, no `.i02-proof.sqlite`, no `.s2b-direct-stage` full proof,
and no synchronous Parquet body read-back are used in this normal path.

`verify_streaming_estate()` fresh-reads the new proof schema, checks the exact
manifest hash, roots, members, family footers and locator footer, and requires a
live current/authorization callback. It does not read source bytes.

## Physical proof version

The old physical root is a byte hash of the SQLite certificate; it cannot be
reproduced without that file. The cut therefore explicitly uses:

- proof schema: `ANVIL_STREAM_C11_ESTATE@1`
- proof version: `STREAM_TYPED_IDENTITY_COVERAGE@1`
- new physical root binding: stream proof hash
- `legacy_i02` recorded separately when an independently held old root is
  supplied.

When `expected_i02` is supplied, the test proves the **logical** root is equal
to old I02. The new physical root is not claimed equal. Existing old estates
remain readable by the unchanged legacy reader; the new reader reads the new
schema.

## Focused parity

The test uses the existing 5-row sourcefree fixture only.

- old/new family counts equal;
- each Parquet member byte-equal old vs new;
- logical identity equal when old expected roots supplied;
- old legacy reader still opens old estate;
- new fresh reader opens new estate with exact roots/counts;
- duplicate exact ref refused;
- dropped family/object census refused;
- locator-count mismatch refused;
- revoked current callback refused;
- `sqlite3.connect` patched to fail during normal new writer and no `.sqlite`
  appears under the new root.

Measured fixture split (`evidence_metrics.json`):

```json
{"new_bytes":357449,"new_seconds":0.072488,"old_bytes":356685,"old_seconds":0.189664,"read_back_audit":false,"sqlite_proof_built":false}
```

The tiny fixture is evidence for the cut, not a full-scale performance claim.

## Commands

```bash
PYTHONPATH="MEASUREMENT_PREP/private-runtime/SRC04_OVERLAY_REPLAY_1795040438/tree:\
MEASUREMENT_PREP/WORKER_RETURNS/ANVIL_ALL35_ORIGINAL_WITNESS_RUNNER_20261118:\
IMPLEMENTER/WORKER_RETURNS/ANVIL_SRC04_SQLITE_FREE_CONSTRUCTION_20261118" \
python3 -B -m pytest -q -o addopts='' -p no:cacheprovider \
  IMPLEMENTER/WORKER_RETURNS/ANVIL_SRC04_SQLITE_FREE_CONSTRUCTION_20261118/test_streaming_cut.py
```

Wiring patch:

```bash
patch -p1 < /path/to/ANVIL_ENGINEERING_EXECUTION_20261117/IMPLEMENTER/WORKER_RETURNS/ANVIL_SRC04_SQLITE_FREE_CONSTRUCTION_20261118/sqlite_free_wiring.patch
```

The patch is an isolated descendant; it was not applied to the active tree or
product. The new module must be present beside the patched runner.

## Boundaries retained

- Compact checkpoint/resume remains in the runner; its spool is not rebuilt or
  read as a second corpus.
- Expected I02 is checked when supplied; Q2, current/revocation, exact evidence
  and replay are not weakened.
- The old SQLite path remains callable as explicit audit, not normal path.
- No new analytical engine, no second durable object corpus, no equivalent full
  SQLite under another name, no whole-object graph.
- No source rights, science, protected refs, grants or live selection changes.

**Remaining limitation:** without an independently supplied legacy `expected_i02`,
the normal path records the explicit stream proof schema and new physical root;
it does not pretend the SQLite byte hash is reproducible. This is a versioned
proof change, not an equality claim.
