# D r13 evidence and commands

## Focused tests

```text
PYTHONDONTWRITEBYTECODE=1 /tmp/rawlsing-oct28-p1r1/venv/bin/python -B \
  -m pytest -q -p no:cacheprovider --tb=short \
  rawlsing_next/tests/test_pre553_original35_execution.py::test_existing_joint_engine_exact_requested_conditional_direction \
  rawlsing_next/tests/test_pre553_original35_execution.py::test_governed_facts_queries_become_exact_cold_e_envelopes
# 2 passed in 3.02s
```

## Actual conditioned-value probe

Asymmetric sourcefree SAV, explicit F2(B<-A) values `0` and `1`, serialized
request consumed by `consume_requested_joint_transport`.

- Baseline in-process and cold subprocess: both requests `OK`, one selection each,
  shared backing fact/query, distinct selected-result IDs; value rows match B|A.
- Tampered `conditioner_item_id`/`target_item_id`: both still `OK`; selection
  material carries the tampered IDs.
- Tampered backing fact/query refs: both still `OK`; selection material echoes
  fake refs.
- Empty requested values: one request still `OK` with zero selections.
- Requested value `9`: that request refuses `REQUESTED_CONDITIONER_VALUE_NOT_IN_PROFILE`;
  the other valid request continues.

## Preserved / limits

- Direction B|A and reverse A|B profiles, job/measure uniqueness, changed-cell
  dependent-row behavior and R10 ordering are previously demonstrated/accepted.
- E codec unchanged; missing permission/replay/cell test paths still fail.
- Actual original facts, authentic E handshake, all35/native/S3/science and
  protected acceptance remain NOT_RUN. No source data, 650 s/full-estate run,
  code repair or A/C/E/guide/progress/controller edit.
