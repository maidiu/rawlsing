# W04 F01/F02/F03 RED to GREEN

## RED baseline

| Finding | Independent RED at `605ce4c4` | Required repair |
|---|---|---|
| `W04-F01` | Ordinary process setting `PYTEST_CURRENT_TEST` + `RAWLSING_C11_ACCELERATOR_DIR` obtained an accepted policy and wrote one cache file. | Remove production legacy/test-marker authorization; migrate existing test helper to explicit policy file. |
| `W04-F02` | Patched directory fsync raised `OSError`; destination existed and no exception surfaced. | Make directory fsync fail closed; cache safe miss/abort; canonical persist raises and cleans only new publication. |
| `W04-F03` | Old hidden `.c11-events-orphan` survived `prune` under max_files=1/max_age=1. | Include stale hidden staging in age/budget retention without deleting active writers or canonical Parquet. |

The RED evidence is retained in review `b5f919e65cd2dcc3df46818026a5dc9581566955`,
`reviews/persistence/FINDINGS.jsonl` and `probes/adversarial_probe.json`; it is
not rewritten by this repair.

## GREEN implementation

### F01

- `load_policy()` only reads `RAWLSING_C11_ACCELERATOR_POLICY`.
- No `PYTEST_CURRENT_TEST` or `RAWLSING_C11_ACCELERATOR_DIR` authorization path
  remains.
- Existing cache test helper creates an explicit private policy file in
  `tmp_path`; all prior assertions and selector/poison/ref/topology tests remain.
- Ordinary spoof process: `load_policy() is None`, zero cache files.

### F02

- `fsync_dir()` raises through directory open/fsync failures.
- Cache `commit()` removes a destination made visible before a failed post-replace
  directory fsync, yielding a safe miss; a later healthy execution rebuilds.
- `ParquetC11Carrier.persist()` removes only the newly published target after a
  failed post-replace parent fsync; the prior complete canonical release remains
  reopenable.
- Replace failures remain observed; no partial target is accepted.

### F03

- Retention includes hidden `.c11-events-*` staging files.
- Stale staging older than the bounded grace/age is removed and accounted;
  active staging inside the grace window is not deleted as an active writer.
- Canonical Parquet is outside the disposable cache root and preserved.
- Regression: old orphan removed, active staging retained, canonical release
  reopens exactly.

## GREEN evidence

- Full selected sourcefree suite: `45 passed in 15.52s`.
- Source-backed facade regression: `10 passed in 4.65s`.
- Focused repair selections: `cache_policy 3`, `invalidation 1`, `recovery 7`,
  `boundary 1`.
- Ordinary spoof: zero cache writes.
- No 100000-event benchmark or economic acceptance is claimed.
- Whole 12-ID MCR-C and protected receiving remain open.
