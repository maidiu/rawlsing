# PROGRAMMA PYAT — Universal35 D r12: exact requested F2 direction

**STATUS:** `D_R12_F2_CONDITIONER_FIRST_JOINT_QUERY_DIRECTION_REPAIRED__ASYMMETRIC_PROFILE_EXACT__SOURCEFREE_ONLY`
**BRANCH:** `codex/pyat-universal35-d-20261106-r1`
**INPUT:** `e4f336972c6c341451ba6e511a2f3c428fc7fb5f` / code `ca4ef1aa207859a7c93493a39f3a3571564df710`
**G:** `e81c71c798c579227039f5b4b371159fc40fde73` — genuine engine/cold profile positive; direction semantics REVISE.

## 1. FINDING | INTERPRETATION | ACTION | OWNER

| FINDING | INTERPRETATION | ACTION | OWNER |
|---|---|---|---|
| **R12-1. Native JOINT query target order is now conditioner-first, target-second.** For requested F2 pair target `B`, conditioner `A`, the JOINT operation targets are `(A,B)`; the existing query constructor emits `target_refs=[A,B]`; E default roles therefore produce requested `P(B|A)`, not reversed `P(A|B)`. | Direction is carried by existing query/JOINT order, not by relabeling facts or E roles. | Preserve exact order. | D + E |
| **R12-2. Requests are explicit operation IDs, not first-pair/measure defaults.** `execute_requested_two_target_joints` requires a nonempty unique caller list of plan operation IDs and returns one explicit OK/typed-refusal entry per ID. Unknown, non-F2, ineligible, weighted or unbound requests refuse rather than falling back. | No arbitrary `next(pair)` or `measure_plans[0]` selection. Measure is derived from exact requested RAW operation/current SAMPLE mapping. | Preserve batch request matrix. | D |
| **R12-3. Exact asymmetric numerical repro passes.** For `B|A`: A=0 denom 6 → B0=6/B1=0; A=1 denom 6 → B0=2/B1=4. For reverse `A|B`: B=0 denom 8 → A0=6/A1=2; B=1 denom 4 → A0=0/A1=4. | E cold profile rows match the requested direction exactly. Changed source cell changes the real joint/profile; restore returns exact original profile. | G focused semantic closure. | D + E + G |
| **R12-4. Identity chain is explicit.** Transport keeps requested conditional operation ID → supporting joint operation/fact/query refs → E profile. Both identities remain visible; no alias of unconditioned joint to conditional estimand and no silent condition-value drop. | 1-target/3+/weighted/non-compatible facts remain retained/typed refusals. | Preserve request matrix. | D + E |

## 2. TEST / EXACT MATRIX

```text
PYTHONDONTWRITEBYTECODE=1 /tmp/rawlsing-oct28-p1r1/venv/bin/python -B \
  -m pytest -q rawlsing_next/tests/test_pre553_original35_execution.py::test_existing_joint_engine_exact_requested_conditional_direction \
  rawlsing_next/tests/test_pre553_original35_execution.py::test_governed_facts_queries_become_exact_cold_e_envelopes \
  -p no:cacheprovider --tb=short
2 passed in 3.07s
```

Requested matrix:
- `F2(B <- A)` → JOINT targets `[A,B]` → E profile A0: `{B0:6,B1:0}` denom 6; A1: `{B0:2,B1:4}` denom 6.
- `F2(A <- B)` → JOINT targets `[B,A]` → E profile B0: `{A0:6,A1:2}` denom 8; B1: `{A0:0,A1:4}` denom 4.
- Changed sourcefree cell B0→1 changes the first profile to `{B0:5,B1:1}`; restore exact.
- Unknown operation ID → typed `REQUESTED_OPERATION_NOT_IN_PLAN`; missing permission/replay still fail closed.

## 3. LIMITS

- Sourcefree engineering connection only; not original35/native/S3/science, population estimate or actor/person inference.
- Actual original run remains blocked by A coordinate and C/D scale; no 650s retry.
- Full35 plan accounting unchanged; requested pair subset proof only.
- No A/C/E/kernel/grammar/guide/controller/protected edit, no fabricated joint or role/arity relabeling.

## 4. PROGRAMMA_DELTA

```text
PROGRAMMA_DELTA — Universal35 D r12 F2 direction
- Identity: codex/pyat-universal35-d-20261106-r1@70d0f0fe45e0b383879ae625526cee6af03f2572; input e4f336972.
- Function: explicit requested F2 operation ID -> conditioner-first/target-second JOINT ScientificOperation -> existing C11/I03 fact/query -> exact E conditional profile and conditioner-value rows.
- Evidence: asymmetric P(B|A) 6/0 and 2/4; reverse P(A|B) 6/2 and 0/4; changed cell changes profile; restore exact; invalid request typed refusal.
- Limits: controlled sourcefree only; original data/native/science NOT_RUN.
```

## 5. BOUNDARY

Author evidence only; no fabricated permission/fact/query, no marginal assembly, no protected merge or self-review. G focused semantic closure requested.
