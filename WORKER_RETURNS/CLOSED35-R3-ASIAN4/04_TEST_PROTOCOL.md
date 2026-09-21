# CLOSED35-R3-ASIAN4 — Synthetic Test Protocol

Status:

`TESTS_AUTHORED__NOT_EXECUTED`

GitHub/browser tooling only. No raw survey carrier was opened. No Python test runner was executed. No real-source processing, Candidate A/B/C execution, I05, whole-source physical equivalence or measured P2X occurred.

Synthetic tests are authored in:

`rawlsing_next/tests/test_closed35_r3_asian4_realization.py`

## Required rejection court

1. **Source SHA drift**
   - Admit the canonical source SHA under `SAV_NATIVE_GOVERNED`.
   - Mutate the SHA and require fail-closed.

2. **Native ID replay invention**
   - Construct two synthetic rows with identical native `country` and `idnumber` but different row ordinals.
   - Require distinct replay keys.
   - Reject `idnumber` or `country+idnumber` as hard replay authority.

3. **Ordinary -1 coerced into physical missing**
   - Project a synthetic Wave-4 `-1` as `OBSERVED_STORAGE_VALUE`.
   - Attempt `SYSTEM_MISSING` classification.
   - Require rejection.

4. **Global -1 semantic invention**
   - Preserve variable-local `BOUNDED_UNKNOWN`.
   - Attempt to assign one global meaning such as `NOT_APPLICABLE`.
   - Require rejection.

5. **Merged/instrument geography collapse**
   - Require merged carrier `country` and instrument carrier `SE1` to remain distinct.
   - Require the accepted 3–8 drift witness to remain nonidentical.
   - Attempt automatic harmonization.
   - Require rejection.

6. **Ranked q20/q21/q22 topology**
   - Preserve exact order and multiplicity.
   - Reorder or flatten.
   - Require rejection.

7. **Ranked q99/q99a/q99b topology**
   - Preserve exact order.
   - Preserve documentary first / optional second / optional third role authority.
   - Reorder or flatten.
   - Require rejection.

8. **q172 documented scope**
   - Admit only `ASEAN_COUNTRIES_ONLY` as the recovered documentary scope.
   - Attempt `ALL_COUNTRIES`.
   - Require rejection.

9. **Routing inferred from missingness/country storage**
   - Resolve q172 with different synthetic `country` values and different `-1`/observed states.
   - Require the same bounded exact-risk-set state.
   - Physical incidence must not decide routing.

10. **w / w_cross aliasing**
    - Preserve both distinct carriers.
    - Attempt semantic aliasing.
    - Require rejection.

11. **Default weight invention**
    - Preserve both carriers with role/estimand `BOUNDED_UNKNOWN`.
    - Attempt default selection.
    - Require rejection.

12. **Cross-wave semantic leakage**
    - Admit Wave 4.
    - Attempt to import Wave 5 or Wave 1 semantic authority.
    - Require rejection.

13. **Candidate-specific semantic divergence**
    - Bind A/B/C to one source-specific realization identity.
    - Mutate C's realization identity.
    - Require rejection.

14. **S35 edge binding**
    - Require exact tuple:
      `EC01,EC05,EC09,EC10,EC12,EC13`.
    - Require EC14 absent for Wave 4.

15. **R35 hook boundary**
    - Require I01 physical metadata.
    - Require I02 derivative parentage for non-direct raw carriers.
    - Require I03 source-scope/expectation/candidate/whole-source-receipt schemas.
    - Require `semantic_authority=false`.

## Acceptance boundary

A future executed synthetic court may establish only that the implementation obeys these source-independent invariants.

Even a future synthetic PASS would not establish:

- real canonical SAV execution;
- source decode equivalence;
- whole-source physical equivalence;
- Candidate A/B/C physical parity;
- I05;
- exact q172 merged-source risk set;
- weight/design estimands;
- merged/instrument geography reconciliation;
- measured P2X;
- source certification.
