# Coupled cold/cache repair handoff

Status: `DELIVERED_PENDING_RECEIVING`.  Full 12-ID MCR-C acceptance, final
100k paired economic receiving, and protected adoption remain open.

## Exact commands

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
  rawlsing_next/tests/test_pre553_source_backed_c11_facade.py \
  rawlsing_next/tests/test_pre553_carrier_execution.py \
  rawlsing_next/tests/test_pre553_i03_grouping.py \
  rawlsing_next/tests/test_pre553_w03_w04_completion.py \
  rawlsing_next/tests/test_pre553_w03_w04_cold.py
# 70 passed
```

## Cross-lane remaining

1. Benchmark lane: frozen 100k cold/cells/full-matrix paired measurements and
   economic thresholds at one integrated head.
2. HQ: final same-SHA 12-ID evidence and independent code/economic receiving.
3. Protected integration remains separately governed.

No original35/SAV/DTA/DB/source bytes, no science/native/actor/FF/N11/Sorok
issuance, no protected merge, no second canonical store or query engine.
