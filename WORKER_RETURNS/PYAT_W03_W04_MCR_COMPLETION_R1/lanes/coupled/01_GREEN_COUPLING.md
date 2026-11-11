# GREEN coupled cold + governed cache

Candidate: `69d96bb1bf2c2ccc79f49299054bfae6120987b7`

## Normal entrypoint

`build_source_backed_c11_repository` now keeps streaming cold construction as
the default for an exact physical stream and attaches the existing governed
cache to that same release:

- explicit private policy + no legacy env -> exactly **1** derived cache file;
- second build -> same release, one file, cache file mtime unchanged (read hit);
- fresh Python process -> same release, one file, mtime unchanged;
- `cold=False` in a fresh policy root -> same exact release, one cache file;
- no policy / legacy-only env -> no cache write;
- revoked policy -> no stale supported result; corrupt cache is a safe miss;
- restored policy -> exact release and rebuilt authenticated cache;
- full typed I03/I05 material is identical across cold miss and cache hit.

## Reused existing owners

- `_pre553_w04_cache` explicit policy, private-root validation, retention and
  `enforce_after_write`;
- `_BodyCacheWriter` atomic staging/fsync/replace;
- existing cache envelope fields: schema, policy root, authority root, source,
  projection, release, release manifest, replay, member root;
- existing `_CompressedBodies` / `_EventLane` / `_CompactPublicObjects`;
- no second store, query engine or semantic authority.

## Test receipts

```text
43 passed  frozen sourcefree court (proof_43_sourcefree_junit.xml)
70 passed  full selected cold/cache/topology/consumer suite (proof_70_focused.txt)
15 passed  focused test_pre553_w03_w04_cold.py
12 passed  test_pre553_w03_w04_completion.py
```

## Small development measurement (not 100k)

5,000 rows / 30,000 events, explicit policy active, sequential subprocess peak
RSS:

| Path | Peak RSS | Wall |
|---|---:|---:|
| eager/compact | 384.3 MiB | 41.20s |
| streaming cold + governed cache | 309.8 MiB | 37.14s |

RSS reduction: **19.4%**; wall reduction: **9.9%**.  This is development-only;
the frozen 100k benchmark remains the benchmark lane/HQ obligation.

## Known limit

The normal cold path and the diagnostic eager fallback derive selectors in
different exact member order (cell-construction order vs release-ref order), so
they can occupy distinct cache files in the same policy root.  The normal cold
default uses and reuses one authenticated file.  This is a cross-path cache
economy limit, not a fact/identity/stale-cache failure.
