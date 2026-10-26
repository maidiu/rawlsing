# R137 commands

## Focused repair tests (actual: 10 passed)

```sh
env PYTHONPATH=. /usr/local/bin/python3 -m pytest \
  rawlsing_next/tests/test_pre553_production_binding.py -q -o addopts=''
```

## Listed affected regression (actual: 4 passed)

```sh
env PYTHONPATH=. /usr/local/bin/python3 -m pytest \
  rawlsing_next/tests/test_universal_source_projection.py::test_s3_exact_respondent_occasion_value_tuples_and_repeated_consumer \
  rawlsing_next/tests/test_universal_source_projection.py::test_s3_varied_respondent_and_occasion_counts \
  rawlsing_next/tests/test_universal_source_projection.py::test_s3_missingness_preserves_state_and_does_not_invent_support \
  rawlsing_next/tests/test_universal_workload_custody.py::test_r91_partial_resume_matches_uninterrupted_without_rerun \
  -q -o addopts=''
```

## Synthetic proof receipt

```sh
env PYTHONPATH=. /usr/local/bin/python3 .r61/r137-production-repair/make_proof.py
```

Output: `evidence/PROOF_RECEIPT.json` (repeated topology, `SUPPORTED`, 2/2 support, exact refusals, restore).

## R136 frozen probe replay

```sh
env PYTHONPATH=. /usr/local/bin/python3 -m pytest \
  .r61/r137-production-repair/probes/test_r136_production.py -q -o addopts=''
```

Actual: `2 passed, 3 errors`. The three errors are the expected refusal exceptions for the three R136 negative probes; the frozen probe bodies assert a returned result. See `00_RETURN.md`.
