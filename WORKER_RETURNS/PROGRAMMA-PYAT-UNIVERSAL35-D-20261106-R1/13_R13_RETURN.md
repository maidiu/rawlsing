# PROGRAMMA PYAT — Universal35 D r13: exact requested conditioner-value realization

**STATUS:** `D_R13_CONDITIONER_VALUES_CARRIED_AND_SELECTED__SAME_BACKING_JOINT_EXACT_VALUE_RESULTS__SOURCEFREE_ONLY`
**BRANCH:** `codex/pyat-universal35-d-20261106-r1`
**INPUT:** `cca6f2b0b46029b0684f539dd58b0f6b0e6a0d6d` / code `70d0f0fe45e0b383879ae625526cee6af03f2572`
**G R12 REVIEW:** `dcbb8b1bcfcf7ff2dd34492c55e40ba4f2fca108` — direction/counts pass; requested-value realization REVISE.

## 1. FINDING | INTERPRETATION | ACTION | OWNER

| FINDING | INTERPRETATION | ACTION | OWNER |
|---|---|---|---|
| **R13-1. Exact conditioner values are carried in the request matrix.** `execute_requested_two_target_joints` accepts explicit requested values per operation ID, validates them against the plan pair's `conditioner_values`, and records them in every result/transport request. | `F2(B <- A; A=0)` and `F2(B <- A; A=1)` remain distinct requests even with the same backing joint/fact/query. No synthetic fact/query change is forced. | Preserve request/backing identities. | D + G |
| **R13-2. Cold D consumer applies requested values.** `consume_requested_joint_transport` reloads the artifact, calls accepted E envelope ingestion under explicit caller ceiling, and selects only matching already-derived conditioner rows. Each selection has its own deterministic selected-result ID material referencing request ID, exact value, backing fact/query, permission and row. | No out-of-band test filter. Unmatched values type-refuse; no unfiltered OK, empty false positive or unknown coercion. | Preserve value-specific selection. | D + E |
| **R13-3. Measure binding is exact, not first-SAMPLE.** JOINT request requires a unique RAW/SAMPLE measure matching `estimand=RAW_OBSERVED_SAMPLE`, null weight/design and variance `NONE`; missing/ambiguous/weighted refuses. | No arbitrary `measure_plans[0]` or weighted enablement. | Preserve exact measure binding. | D |
| **R13-4. Exact asymmetric results pass.** Same backing `P(B|A)` joint supports A=0 denom 6 `{B0:6,B1:0}` and A=1 denom 6 `{B0:2,B1:4}` with different selection IDs. Reverse `P(A|B)` remains denom 8 `{A0:6,A1:2}` and denom 4 `{A0:0,A1:4}`. | Changed source cell changes only the dependent value row; restore exact. | G focused closure. | D + E + G |

## 2. TEST / EXACT MATRIX

```text
PYTHONDONTWRITEBYTECODE=1 /tmp/rawlsing-oct28-p1r1/venv/bin/python -B \
  -m pytest -q rawlsing_next/tests/test_pre553_original35_execution.py::test_existing_joint_engine_exact_requested_conditional_direction \
  rawlsing_next/tests/test_pre553_original35_execution.py::test_governed_facts_queries_become_exact_cold_e_envelopes \
  -p no:cacheprovider --tb=short
2 passed in 3.07s
```

Requested matrix:
- `F2(B <- A; A=0)` → denom 6, B0=6, B1=0.
- `F2(B <- A; A=1)` → denom 6, B0=2, B1=4.
- `F2(A <- B; B=0)` → denom 8, A0=6, A1=2.
- `F2(A <- B; B=1)` → denom 4, A0=0, A1=4.
- Same `P(B|A)` 0/1 requests share backing fact/query refs but have distinct selected-result IDs/counts.
- Changed sourcefree B cell changes A=0 row to `{B0:5,B1:1}` while A=1 row unchanged; restore exact.
- Unknown operation/value and weighted measure refuse before false artifact; missing permission/replay still fail closed.

## 3. LIMITS

- Sourcefree engineering only; not original35/native/S3/science, population estimate or actor/person inference.
- Original run remains blocked by A coordinate and C/D scale; no 650s retry.
- E codec unchanged; no new probability/counter/fact engine; no A/C/kernel/grammar/guide/controller/protected edit.

## 4. PROGRAMMA_DELTA

```text
PROGRAMMA_DELTA — Universal35 D r13 requested conditioner-value realization
- Identity: codex/pyat-universal35-d-20261106-r1@6c66654c7f2882b94b9ad8a74ee438c77844af2f; input cca6f2b0b.
- Function: explicit requested F2 ID(s)+conditioner value(s) -> exact RAW/SAMPLE JOINT backing -> accepted E full profile -> cold D value-specific selected rows/results.
- Evidence: B|A 0/1 and reverse A|B exact denominators/counts; same backing joint, distinct selected IDs; changed cell/restore; unknown value/weighted/measure refusal.
- Limits: controlled sourcefree only; original data/native/science NOT_RUN.
```

## 5. BOUNDARY

Author evidence only; no fabricated permission/fact/query, no pooled OR, no forced roles/arity, no protected merge or self-review. G focused semantic closure requested.
