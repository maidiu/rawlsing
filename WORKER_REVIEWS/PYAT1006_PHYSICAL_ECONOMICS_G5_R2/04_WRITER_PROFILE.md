# Writer profile — independent 2k call-boundary check

Sourcefree TEST_ONLY; accepted writer unchanged.  The profile is a 2k
call-boundary decomposition, not a 100k extrapolation.  Author 2k: 38.277 s
unprofiled / 108.106 s cProfile.  R2: 41.425 s / 116.386 s on this host.

## Stage overlap

| stage | R2 2k unprofiled s | author 2k unprofiled s |
|---|---:|---:|
| writer wall | 41.425 | 38.277 |
| direct-I02 proof (inclusive) | 27.629 | 25.181 |
| reread/re-encode proof | 13.364 | 12.691 |
| root hashing | 0.202 | 0.183 |
| direct + reread + root | 41.195 | 38.055 |
| `_row` total (nested) | 13.028 = 6.685 + 6.343 | 11.999 = 6.010 + 5.989 |

Direct + reread + root equals wall within 0.6% (R2) / 0.6% (author).  `_row` is
inside both passes, not additive.  The 100k stage totals remain the independent
R1 baseline receipts (writer 2,943.177 s, direct proof 2,218.465 s, reread
710.960 s, root 11.005 s); this profile does not extrapolate them.

## Call-boundary nesting (R2 2k unprofiled)

- `_Sink.add` 7.207 s = `_row` first pass 6.685 s + Parquet flush 0.518 s.
- `_insert_object` 4.901 s contains `validate_public_object` 3.816 s.
- `logical_root` 1.082 s; candidate projection hash 0.457 s; replay hash
  0.717 s; relation checks 0.432 s.
- Reread/re-encode 13.364 s contains verify `_row` 6.343 s, `_object_row`
  4.817 s and semantic hashing 2.027 s.
- Therefore the inclusive direct-I02 proof contains first-pass body/Parquet
  work, insertion, validation, relations, logical-root and hashing; it is not a
  SQLite-only stage.  The original 100k 2,249.7 s / R1 2,218.5 s figure must be
  read the same way.

## cProfile relative shares

R2 cProfile wall 116.386 s (author 108.106 s); relative only.

| item | R2 | author |
|---|---:|---:|
| `semantic_hash` calls | 96,000 | 96,000 |
| `semantic_projection` calls | 40,992 | 40,992 |
| first-pass objects | 22,501 | 22,501 |
| hashes per object | 4.266 | 4.266 |
| SQLite `execute` exclusive | 4.354 s (3.74% of wall) | 4.562 s (4.22%) |
| `canonicalize` exclusive | 12.470 s | 11.527 s |
| `isinstance` exclusive | 13.372 s | 12.342 s |

The cProfile count agreement is exact; the exclusive-time difference is host
and instrumentation variance.  SQLite execute is not the dominant cost;
canonical projection/identity/object validation and JSON/body reconstruction
dominate.  Call-boundary wrappers are a subset for functions imported directly;
the cProfile counts are the complete witness.

## Proposal status

The author's bounded per-build memo of the already-computed immutable semantic
projection/hash remains **NOT IMPLEMENTED and NOT MEASURED as a gain**.  The
96,000/40,992 counts support the premise that validation and insertion re-hash
the same frozen objects, but they do not establish the memo's wall-time or
memory benefit.  Removing the reread/re-encode proof is explicitly not proposed
here.  No writer optimization or owner grant is accepted.

## Limits

- 2,000 respondents / 6,490 events / weights / chunk 512 only.
- cProfile overhead; relative shares only.
- SQLite timing is cProfile exclusive, not a separate SQL trace.
- No 10k/100k writer rerun in this recheck; R1 writer receipts are frozen.
- No production change, SLA or writer handoff.
