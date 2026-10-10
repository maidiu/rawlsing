# HQ280 B1 — hostile no-drop court: execution-status register

**All four cases: UNEXECUTED.** These are the expected assertions in a staged runnable Python test; no test-run receipt or local Codex PASS exists here. Do not promote expected results to observed evidence.

| Case | Fixture and already-implemented owner calls | Expected verdict once executed | Observed |
|---|---|---|---|
| P01 | Independently frozen A+B and W01–W06 → source-backed C11 → Route B/I03/I05 → independently reconciled exact batch units → real C1 W03 consumer | Synthetic positive complete; A 3/3/2, B 4/4, B1/A1 3/3, A1/B1 3/4, B1/A2 0/2 measured zero; two I05 candidates; exact consumer `EXACT_SUPPORTED` | **UNEXECUTED** |
| N01 | A+B physical stream and original oracle, **A-only selected** C11/catalog/I03/I05/batch with a legitimate local `VALID_EMPTY` I05 receipt | Local selected scope may complete; source-original B and W02–W06 MUST be reported omitted/unexecuted; W03 consumer not satisfied; global FAIL | **UNEXECUTED** |
| N02 | Exact expected query jobs J1/J2/J3, submitted immutable batch J1/J3, existing I03 callback | Batch reports local 2/2 complete; expected-minus-submitted = exact J2; global FAIL | **UNEXECUTED** |
| N03 | Outcome perturb and physical cell reversal; pre-outcome work and discovery grammar held frozen | Work-class/original oracle keys and I05 candidate frontier stable; measured values may change; unchanged physical source permutation yields same C11 release | **UNEXECUTED** |

## Why this is a decisive omission witness

`project_c11_candidate_from_physical_cells` explicitly skips cells whose physical slot is not in a caller's governed projected slots. That is valid locally. N01 intentionally keeps A and B in physical cells but submits only A as a complete caller-declared projection and only A-derived jobs; hence no hidden B query is smuggled into the local engine to cause an ordinary fail-closed query error. The *separate immutable instrument/operation register* supplies the extra information capable of falsifying global closure.

`BatchManifest` hashes the units actually submitted. N02 independently freezes three exact `BatchUnitSpec` references and withholds the middle unit only from the selected manifest. Local `FULL_MANIFEST_COVERAGE` and global missing work are simultaneously true; there is no batch-engine defect inferred from this.

`VALID_EMPTY`, an observed B=1 zero cell with positive A=2 denominator, a missing scheduled operation, source-intrinsic inapplicability, and an authority hold remain distinct. The positive synthetic oracle grants the expected operations **only at this test-local source-free grain**, so N01 cannot reclassify omitted B as a scientific hold or genuine inapplicability.

## Local owner tests already available

- `test_pre553_source_backed_c11_facade.py`: physical slot, eligibility, explicit response topology and replay.
- `test_pre553_route_b_production.py`: selected C11→I03/I05 object closure.
- `test_pre553_empirical_query.py`: observed zero, null vs missing, source indexed same-respondent joints and reversed conditioning.
- `test_pre553_discovery_exact.py`: minority, ordered candidate enumeration, XOR, Cartesian and joint parity.
- `test_pre553_batch_runner.py`: local manifest completion, provenance, deterministic scheduling and deferred units.
- `test_pre553_recursive_handoff.py` and `test_pre553_analytical_composition_higher_order.py`: recursive ancestry and actual C1 higher-order consumer.
- `test_pre553_empirical_possibility_provider.py`: independent producer-derived forward/reverse consumer slices.

No need to duplicate full recursive or four-variable XOR scenarios in this minimum two-item scalar test.

## Execute and adjudicate

In a governed local checkout of the exact pushed branch:

```bash
python -m pytest -q rawlsing_next/tests/test_pre553_original_workload_nodrop_integration.py
```

Return actual per-test outcomes, Python environment, traceback and changed test-blob hash if fixture adjustment is needed. A failing test does **not** by itself establish a PRE-MAIN production defect; first differentiate synthetic fixture/API inconsistency from violation of an accepted owner contract. No production or authority changes permitted under B1.

No survey SAV/DTA was executed; no source-science permission, all-35 occupancy or self-adoption claimed.

`HQ280_B1_NODROP_TEST_CANDIDATE_RETURNED_FOR_HQ_REVIEW__NO_SELF_ADOPTION`
