# UNIVERSAL35 — measured universal-workload preparation reuse

**STATUS:** `COMPILE_PREPARATION_REUSE_IMPLEMENTED__SOURCEFREE_EXACT_IDENTITY_PASS__ACTUAL_SCALE_NOT_RUN`

- Base: C `e1e0aebe86162e5f45ee32edcb4f9050dd176a3e`
- Branch: `codex/pyat-universal35-compile-sharing-20261106-r1`
- Production changes: `pre553_universal_workload.py`, `pre553_native_workload_binding.py`, `pre553_issued_workload.py`
- Test: `rawlsing_next/tests/test_universal_workload_compile_reuse.py`
- No C facade/native adapter/D execution/A config/E/grammar/I03 kernel edit.

## FINDING

`compile_universal_workload` repeated immutable projection preparation for every
F1 response value: a full projection materialization, query/branch authority and
branch predicate, and an issued-workload envelope materialization each time.

The smallest existing-owner repair adds a bounded `PreparedProjectionCatalog`
created once per compile call and passed as an optional prepared input to
`build_projection_catalog` / `build_test_only_workload`. Per-value response
predicate, query, catalog, expected jobs and issued record are still built
individually. `NativeWorkload.envelope` reuses only the exact materialized
projection/catalog on that workload object; it does not use a global cache.

The change does not use or accept C r8 prebuilt-release reuse.

## MEASURED CONTROL

Stable sourcefree 10-value SAV bundle; same operations and callers before/after.

| Measure | Baseline | After |
|---|---:|---:|
| compile wall | 0.09481 s | 0.08208 s |
| execute wall | 0.64349 s | 0.46272 s |
| projection preparation | 10 per-value | 1 per compile |
| catalog builds | 10 | 10 per-value |
| issued workload builds | 10 | 10 per-value |

Exact identity was preserved for the controlled bundle
`content_hash=07c2640f8b9ba7c057feaea5a012d2748c13cc8f5edc4e02d4733aa69e4be334`:
operations hash `957d4fee…`, expected-jobs hash `2e0b2720…`, issued hash
`86b98772…`, execution result hash `db23a200…`, 10 facts, 10 receipts, 0 failed.
Changed sourcefree input produces a different content hash/expected jobs;
restore returns the original identity. Prepared bundle/as-of mismatch refuses
`PREPARED_PROJECTION_MISMATCH`.

## TESTS

```text
pytest rawlsing_next/tests/test_universal_workload_compile_reuse.py
# 2 passed in 2.34s

pytest rawlsing_next/tests/test_universal_workload.py
# 16 passed in 76.54s

pytest rawlsing_next/tests/test_universal_workload_custody.py \
       rawlsing_next/tests/test_pre553_original35_scale.py
# 8 passed in 20.28s
```

## LIMITS

- No original read, actual SRC09/SRC10 compile rerun, 600 s run, full estate or
  native fact claim. The observed SRC10 169.26 s materialize + >425.86 s compile
  at 601.8 s/zero facts remains a prior held negative, not retimed.
- Actual original facts remain zero. C prebuilt reuse validation fix, A
  coordinate consumer join and D actual composition remain separate.
- This is controlled engineering proof, not completed all35/16-GiB/native
  performance. No favorable full-path timing claim.

**PROGRAMMA_DELTA:** hoist exact immutable projection preparation once per
compile call and cache per-workload envelope preparation; preserve all
per-value query/authority/refusal/issued identities; sourcefree 10-value control
shows 13.4% compile and 28.1% execution reduction with exact identity. Actual
scale/native remains `NOT_RUN`.
