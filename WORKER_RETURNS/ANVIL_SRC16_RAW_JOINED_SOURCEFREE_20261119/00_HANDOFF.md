# SRC16 raw joined sourcefree candidate

## Verdict

**PASS for the isolated sourcefree composition; original GSS1972 execution is
not run.** One sourcefree saved-estate build is cold-traversed through actual
I03, I05 and saved Batch with the existing tiny fixture.

## Patch order and identities

1. `patches/01_handoff_raw_lane.patch` — R1 raw handoff lane.
2. `patches/02_query_predicate_guard.patch` — R1 leaf-local unresolved guard.
3. `patches/03_i05_unresolved_repair.patch` — R2 `EVALUATED_UNRESOLVED`.
4. `patches/04_saved_batch_prior_cache.patch` — R3 prior-output validation /
   completed-receipt reexecution.

Exact hashes, base hashes and post-patch hashes are in `JOINED_EVIDENCE.json`.
`SETUP.sh` reproduces the isolated candidate; `GSS1972_HANDOFF.md` contains the
owner-only construction/fresh-reader command.

## Outcomes

- one saved-estate build: yes
- cold I03: positive `SUPPORTED`, denominator 8
- cold I05: native facts `UNRESOLVED`; receipt `EVALUATED_UNRESOLVED` /
  `COVERAGE_LIMITED`
- valid empty: distinct `EVALUATED_VALID_EMPTY` / `VALID_EMPTY`
- saved Batch: `COMPLETED`, full manifest coverage, operational execution only
- corrected changed-predicate path: refused with `SAVED_BATCH_PREDICATE_BINDING_MISMATCH`
- exact same-root reuse: preserved, 3/3 receipt records equal
- forged completed prior receipts: not retained; reexecuted
- changed prior output: `PRIOR_OUTPUT_MISMATCH`; legitimate partial resume preserved
- current authority denial: `DirectEstateError` for direct I05 and prior-receipt
  Batch
- mapped parity: exact; SAV expected/raw/control 1/1/1, DTA 2/2/2
- saved-row deletion: one mapped event removed from the saved sections, the
  estate fully rebuilt through `write_streaming_estate`, cold reopened, and the
  equality check fails on the exact missing response; original estate restored
  and cold reopen is equal again
- no in-memory set deletion is used as the proof
- declared missingness: separate `MISSING` and `INVALID_UNRESOLVED` states in
  raw lane evidence

## Files

- `JOINED_EVIDENCE.json`
- `TRACE.json` (sanitized actual I03/I05/Batch fields)
- `raw_lane_joined.out`
- `i03_joined.out`
- `joined_trace.py`
- `SETUP.sh`
- `GSS1972_HANDOFF.md`
- `patches/01..04`
