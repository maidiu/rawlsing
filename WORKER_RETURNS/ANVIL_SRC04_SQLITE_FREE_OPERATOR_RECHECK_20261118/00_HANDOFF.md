# SQLite-free operator integration — independent recheck

## Verdict

**NOT READY — actual cold reader blocker.**

The new joined cut materially fixes the writer and producer paths, but the actual
`sqlite_free_witness.py --mode reader` still refuses on a sourcefree stream
estate:

`AttributeError: 'NoneType' object has no attribute 'content_hash'`

The reader at `sqlite_free_witness.py:353` dereferences
`estate.reconstructed_v1_release_ref`, while `StreamVerifiedEstate.__init__`
sets that attribute to `None`. The sourcefree writer and separate audit work;
the actual reader receipt does not.

## Evidence

- Source cut: `20e265633e3ded64fd6f031c1b1b0c1e90db2661`
- Manifest verified: 24/24 files exact.
- Sourcefree normal stream writer: 1 universe, 90 identities/events/routing/
  coordinates, 7 authority snapshots, 0 weights; no `.sqlite` files.
- Progress observed through `checkpoint_ready`, `stream_start`,
  `family_written`, `footers_verified`, `published`, `reopened_validation`.
- Actual CLI reader: refused with the `AttributeError` above.
- Exact metadata preflight: `RUNTIME_OVERLAY_QUALIFIED`; source path not opened;
  q217 held; 177/3/181 scoped counts.
- Separate CLI audit: PASS, read-only, no SQLite calls, 369 records.

## Required repair

Use a stream-native release identity in the actual reader instead of dereferencing
the legacy `reconstructed_v1_release_ref` on a stream estate: read
`receipt["i02"]["release"]`/`StreamRoots.release` for the present stream field and
make the accepted-legacy comparison explicitly false/not-applicable, or set a
typed stream release ref in `StreamVerifiedEstate` and update that comparison.
Also add `streaming_estate.py` to the runtime digest pins.

## Scope and limits

Sourcefree fixture only; no original source, staging access, legacy R4
interference, code edits, or full benchmark. Remaining width/resource questions
are bounded: only a 90-row/369-record fixture was exercised; proof scratch was
199,473 B, retained fixture estate 3,818,492 B. Real authorized construction
still requires its external grant/current gate.
