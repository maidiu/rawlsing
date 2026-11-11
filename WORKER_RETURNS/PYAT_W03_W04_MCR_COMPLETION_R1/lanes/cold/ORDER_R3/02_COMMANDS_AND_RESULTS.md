# CC-F01 commands and results

Runner: `/usr/local/bin/python3` 3.11.3, sourcefree S2 only, no 100k matrix.

## Review parity probe

```sh
PYTHONPATH=. /usr/local/bin/python3 \
  WORKER_RETURNS/PYAT_W03_W04_MCR_COMPLETION_R1/lanes/cold/ORDER_R3/probes/cold_parity_probe.py
```

RED at intake: `event_sequence_parity=false`, `selector_yield_parity=false`,
`selector_yield_differences=3`, `consumer_material_parity=true`.

GREEN at candidate: `event_sequence_parity=true`, `selector_yield_parity=true`,
`selector_yield_differences=0`, `consumer_material_parity=true`.

## Focused courts

```sh
PYTHONPATH=. /usr/local/bin/python3 -m pytest -q -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_w03_w04_cold.py
# 18 passed

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
# 73 passed
```

JUnit/log receipts: `proof_43_sourcefree_junit.xml`, `proof_73_focused.txt`.
