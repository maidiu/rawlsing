# PROGRAMMA PYAT — Universal35 D r14: cold transport binding repair

**STATUS:** `D_R14_COLD_CONSUMER_DERIVES_AUTHORITATIVE_REFS__TAMPERED_METADATA_AND_EMPTY_VALUES_REFUSED__VALUE_MATRIX_PRESERVED`
**BRANCH:** `codex/pyat-universal35-d-20261106-r1`
**INPUT:** `7cafd1fd3830454ad4833ba98a7d68eb1a9e610f` / code `6c66654c7f2882b94b9ad8a74ee438c77844af2f`
**G R13 REVIEW:** `6158fd23d37705d87f62166cf522c97321d13702` — REVISE cold request binding.

## 1. FINDING | INTERPRETATION | ACTION | OWNER

| FINDING | INTERPRETATION | ACTION | OWNER |
|---|---|---|---|
| **R14-1. Cold consumer derives authoritative fact/query/role identities from the accepted envelope.** It decodes the exact `EmpiricalFact`/`EmpiricalQuerySpec`, derives query target refs and fact/query refs, and compares request metadata against those actual identities. | Tampered `conditioner_ref`, `target_ref`, `fact_refs`, `query_refs` or request binding are now typed refused instead of echoed into selection identity. | G focused closure. | D + G |
| **R14-2. Request metadata is bound by a deterministic request-binding ID.** Transport carries the binding of operation ID, role item IDs, values, actual role refs, fact/query refs; consumer recomputes it from the decoded envelope and refuses mismatch. | Single-field tampering cannot produce OK; selection material uses derived refs, not unverified request echoes. | Preserve. | D |
| **R14-3. Empty/noncanonical/ambiguous conditioner values are refused.** Empty values refuse `REQUESTED_CONDITIONER_VALUES_EMPTY`; `None` refuses `REQUESTED_CONDITIONER_VALUE_NONCANONICAL`; unknown values refuse `REQUESTED_CONDITIONER_VALUE_NOT_IN_PROFILE`; duplicate/noncanonical profile states refuse. | `OK` now requires at least one exact canonical selection. No zero-selection OK. | Preserve. | D + E |
| **R14-4. Value-specific positive matrix remains exact.** Same `P(B|A)` backing fact/query supports A=0 denom 6 `{B0:6,B1:0}` and A=1 denom 6 `{B0:2,B1:4}` with distinct selection IDs. Reverse `P(A|B)` remains denom 8 `{A0:6,A1:2}` and denom 4 `{A0:0,A1:4}`. | Changed sourcefree cell changes the dependent row; restore exact. | Preserve. | D + E + G |

## 2. TEST / EVIDENCE

```text
PYTHONDONTWRITEBYTECODE=1 /tmp/rawlsing-oct28-p1r1/venv/bin/python -B \
  -m pytest -q rawlsing_next/tests/test_pre553_original35_execution.py::test_existing_joint_engine_exact_requested_conditional_direction \
  rawlsing_next/tests/test_pre553_original35_execution.py::test_governed_facts_queries_become_exact_cold_e_envelopes \
  -p no:cacheprovider --tb=short
2 passed in 3.82s
```

Tamper/refusal checks:
- wrong `conditioner_ref` / `target_ref` → typed refusal.
- fake `fact_refs` / `query_refs` → typed refusal.
- empty values → `REQUESTED_CONDITIONER_VALUES_EMPTY`.
- `None` value → `REQUESTED_CONDITIONER_VALUE_NONCANONICAL`.
- unknown value → `REQUESTED_CONDITIONER_VALUE_NOT_IN_PROFILE`.
- permission/replay mutation still fail closed; no OK with zero selections.

## 3. LIMITS

- Sourcefree engineering only; original empirical facts remain zero; no native/S3/science/protected acceptance.
- Original run remains blocked by A coordinate/C scale; no 650s retry.
- E codec/kernel/grammar unchanged; no new statistical engine or probability computation.
- Full35 plan accounting unchanged; requested subset proof only.

## 4. PROGRAMMA_DELTA

```text
PROGRAMMA_DELTA — Universal35 D r14 cold request binding
- Identity: codex/pyat-universal35-d-20261106-r1@ab7a6b606f15bd47c29d962da8c8c9db542710de; input 7cafd1fd3.
- Function: cold consume -> decode accepted fact/query -> derive role/backing refs -> validate request binding -> canonical value selection from actual E profile.
- Evidence: A0=6/0, A1=2/4, reverse 8/4 and 0/4; changed cell/restore; tampered refs/empty/None/unknown refused; no zero-selection OK.
- Limits: controlled sourcefree only; original data/native/science NOT_RUN.
```

## 5. BOUNDARY

Author evidence only; no fabricated permission/fact/query, no pooled OR, no forced roles/arity, no protected merge or self-review. G focused independent closure requested.
