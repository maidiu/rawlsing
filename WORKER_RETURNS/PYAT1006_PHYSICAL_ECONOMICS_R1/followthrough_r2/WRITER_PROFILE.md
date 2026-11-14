# Direct-I02 writer profile — measured diagnosis

## Scope and scale limit

The accepted writer was profiled unchanged with the existing `fixture_1006`
sourcefree generator: 2,000 respondents, 6,490 events, weights, chunk_rows=512.
The absolute unprofiled run is 38.277 s; the cProfile run is 108.106 s and its
relative shares are used only as a call-boundary decomposition.  The 10k/100k
stage totals are the independently measured review/baseline receipts, not
extrapolated from this 2k profile.

## Stage wall decomposition

| stage | 2k absolute | 10k (independent) | 100k (independent) |
|---|---:|---:|---:|
| writer wall | 38.277 s | 197.202 s | 2,943.177 s |
| direct I02 proof (inclusive) | 25.181 s | 130.416 s | 2,218.465 s |
| reread/re-encode proof | 12.691 s | 60.033 s | 710.960 s |
| root hashing | 0.183 s | 1.102 s | 11.005 s |
| total `_row` (nested; 2k split measured) | 11.999 s (6.010 + 5.989) | 46.572 s | 507.703 s |
| retained Parquet | 6,300,407 B | 31,117,712 B | 310,178,695 B |

At 2k, direct proof + reread + root hashing = 38.055 s against 38.277 s wall.
The 100k sum is 2,940.430 s against 2,943.177 s wall.  `_row` is nested inside
the two passes, not additive; only the 2k run measured the first/verify split.

## What the 2249.7 s (author) / 2218.5 s (review) direct-I02 inclusive stage contains

1. `tap` feeds each source object to `_Sink.add`: first-pass `_row` body_json /
   typed-lane construction and Parquet row-group writes.
2. `_insert_object` verifies `semantic_hash(obj.semantic_projection())` against
   the exact ref digest, extracts all exact identity/selector fields and inserts
   the corpus row into the temporary SQLite proof.
3. `validate_public_carrier_object` revalidates exact carrier closure and
   authority refs; `_walk_authority_refs` resolves them.
4. Event occurrence uniqueness, relation checks, candidate-projection hash and
   disk-sorted replay-manifest hash, coverage and `_logical_root` are computed.
5. SQLite commits, certificate header and physical publication hashing happen
   after the stream (some are outside the build timer).

## Call-boundary evidence (2k unprofiled)

- `_Sink.add` inclusive 6.507 s (`_row` 6.010 s; Parquet flush 0.505 s).
- `_insert_object` inclusive 4.494 s; `validate_public_carrier_object` 3.413 s.
- `logical_root` 0.968 s; relation checks 0.356 s; candidate/replay hashes 1.010 s.
- `_object_row` first pass 4.466 s; `_row` verify pass 5.989 s; reread total 12.691 s.
- cProfile exclusive: `canonicalize` 11.527 s, `isinstance` 12.342 s,
  `semantic_hash` 0.210 s, `sqlite3.Connection.execute` 4.562 s.
  SQLite execute is ~4.2% of the inflated profile wall; the direct I02 stage is
  dominated by canonical projection/identity/object validation and JSON/body
  reconstruction, not by SQLite alone.
- cProfile counts: 96,000 `semantic_hash` calls and 40,992
  `semantic_projection` calls for 22,501 first-pass writer objects (~4.3 hashes
  per object).  This is the measured duplicate-work witness behind the memo
  proposal; the call-boundary wrappers are a subset because some modules
  imported the function directly.

Compact receipt: `evidence/writer_profile_summary.json`.

## Smallest owner-consistent proposal (NOT IMPLEMENTED)

**Memoize the immutable exact semantic projection/content hash once per object
within the one-pass direct-I02 build and reuse it in both
`validate_public_carrier_object` and `_insert_object`.**  Those two boundaries
currently re-hash the same frozen object.  Keep one full semantic/identity/
checksum verification, all source/I02 roots, omission/body/locator proofs and
current/authority checks; do not remove any validation.  The memo is
per-build, immutable-keyed and bounded.  This is local to the builder and does
not change schema, Parquet layout, body_json or reader ABI.

**Not proposed here:** removing the second full reread/re-encode proof,
body_json, or any integrity check.  That is a versioned proof/identity policy
change requiring separate owner approval and hostile requalification.  This
return does not implement or measure the writer memo; it is a conditional
owner-handoff candidate only.
