# R135 — exact commands

## Focused new proof

```sh
env PYTHONPATH=. /usr/local/bin/python3 -m pytest \
  rawlsing_next/tests/test_pre553_production_binding.py -q -o addopts=''
```

Result: `5 passed`.

## Affected existing regression

```sh
env PYTHONPATH=. /usr/local/bin/python3 -m pytest \
  rawlsing_next/tests/test_universal_source_projection.py::test_s3_exact_respondent_occasion_value_tuples_and_repeated_consumer \
  rawlsing_next/tests/test_universal_source_projection.py::test_s3_varied_respondent_and_occasion_counts \
  rawlsing_next/tests/test_universal_source_projection.py::test_s3_missingness_preserves_state_and_does_not_invent_support \
  rawlsing_next/tests/test_universal_workload_custody.py::test_r91_partial_resume_matches_uninterrupted_without_rerun \
  -q -o addopts=''
```

Result: `5 passed`; explicit TEST_ONLY path remains valid.

## Production transport call

Preparation (unsigned; no record created):

```python
workload = build_production_workload(
    bundle=external_bundle,
    catalog=external_catalog,
    requests=external_requests,
    discoveries=external_discoveries,
    descriptor=external_descriptor,
    decision_ref=external_decision_ref,
    source_factory_ref=external_source_factory_ref,
    original_u_root=external_u_root,
    expected_frontier_root=external_epre_root,
    original_wave_identity=external_wave_identity,
)
```

Execution only after external current issuance:

```python
result = execute_production_workload(
    workload=workload,
    resolver=external_current_resolver,
    source_factory=external_source_factory,
    host=external_host,
    purpose=external_purpose,
)
```

No raw source read or historical grant inference is part of this command.

## Synthetic proof receipt

`PROOF_RECEIPT.json` records the synthetic harness positive, value dependence,
restoration and exact refusals. It is not source occupancy.
