# Cold lane handoff

## Public interface

`build_source_backed_c11_repository(source, projection, *, cache=None,
batch_size=10000, current_authorities=(), cold: bool | None = None)`

- `cold=None` (default): cold path for `ExactPhysicalCellStream` when
  `RAWLSING_C11_ACCELERATOR_DIR` is absent; otherwise existing eager/compact
  path.
- `cold=True`: force the cold streaming path for an exact stream.
- `cold=False`: force the existing eager/compact path.

The new public helper `build_cold_source_backed_c11_release(stream, projection)`
is additive.  Existing callers need no change.

## Verification commands actually run

```sh
PYTHONPATH=. /usr/local/bin/python3 -m pytest -q -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_c11_execution_view.py \
  rawlsing_next/tests/test_pre553_c11_cold_reopen_i03.py \
  rawlsing_next/tests/test_pre553_source_backed_c11_facade.py \
  rawlsing_next/tests/test_pre553_carrier_execution.py \
  rawlsing_next/tests/test_pre553_i03_grouping.py
# 43 passed

PYTHONPATH=. /usr/local/bin/python3 -m pytest -q -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_c11_execution_view.py \
  rawlsing_next/tests/test_pre553_c11_cold_reopen_i03.py \
  rawlsing_next/tests/test_pre553_carrier_execution.py \
  rawlsing_next/tests/test_pre553_i03_grouping.py \
  rawlsing_next/tests/test_pre553_source_backed_c11_facade.py \
  rawlsing_next/tests/test_pre553_route_b_production.py \
  rawlsing_next/tests/test_pre553_w03_w04_cold.py
# 62 passed
```

## Exactness checks

The cold release equals the eager release for:

- `release_ref`, `replay_manifest.ref`, `source_release_manifest_hash`;
- every public-object `ref` and `as_dict`;
- every internal-record `ref`;
- M01–M18 coverage;
- route-B fixtures with missing optional weight and valid-empty frontiers;
- repeated/ordered/missing/zero topology materialization.

## Refusals retained

- duplicate physical row/slot;
- incomplete projected slot;
- wrong source SHA;
- unbound response value/state;
- cross-source fixture;
- original execution remains `NOT_RUN`.

## Cross-lane notes

- Bench lane should use `cold=True` for cold profiles even if it configures a
  cache root, so the cold path is measured unambiguously.
- Persistence lane owns `_pre553_c11_execution_view.py` and
  `pre553_parquet_carrier.py`; this lane did not edit either.
- The final 100k paired median RSS and repeat wall thresholds are not claimed
  here.  HQ must integrate and the benchmark lane must measure at one immutable
  head.

## Status

`DELIVERED_PENDING_RECEIVING` for the cold lane implementation.  Whole
W03/W04 MCR-C remains incomplete and HQ-owned.  No final MCR self-acceptance.
