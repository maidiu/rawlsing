# R140 commands

## Focused sourcefree suites (actual: 18 passed)

```sh
env PYTHONPATH=. /usr/local/bin/python3 -m pytest \
  rawlsing_next/tests/test_pre553_production_binding.py \
  rawlsing_next/tests/test_pre553_source_read_admission.py \
  -q -o addopts=''
```

## Preserved repeated positive + explicit TEST_ONLY regression (actual: 4 passed)

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
env PYTHONPATH=. /usr/local/bin/python3 .r61/r140-private/make_proof.py
```

Outputs `evidence/PROOF_RECEIPT.json`: predecode authorized R04 custody and 14
zero-open refusals; discovery 150/150 candidates, 98 supported + 52 valid-empty
receipts, 330 facts, no-drop, restore.
