# R141 commands

## Focused preserved + successor (actual: 19 passed)

```sh
env PYTHONPATH=. /usr/local/bin/python3 -m pytest \
  rawlsing_next/tests/test_pre553_production_binding.py \
  rawlsing_next/tests/test_pre553_source_read_admission.py \
  -q -o addopts=''
```

## Preserved repeated positive + TEST_ONLY regression (actual: 4 passed)

```sh
env PYTHONPATH=. /usr/local/bin/python3 -m pytest \
  rawlsing_next/tests/test_universal_source_projection.py::test_s3_exact_respondent_occasion_value_tuples_and_repeated_consumer \
  rawlsing_next/tests/test_universal_source_projection.py::test_s3_varied_respondent_and_occasion_counts \
  rawlsing_next/tests/test_universal_source_projection.py::test_s3_missingness_preserves_state_and_does_not_invent_support \
  rawlsing_next/tests/test_universal_workload_custody.py::test_r91_partial_resume_matches_uninterrupted_without_rerun \
  -q -o addopts=''
```

## R141 scope receipt

```sh
env PYTHONPATH=. /usr/local/bin/python3 .r61/r141-private/make_proof.py
```

Outputs `evidence/PROOF_RECEIPT.json`: six R138 successor refusals, preserved
2/2 six-cell repeated positive, value change/restore, R140 control counts.
