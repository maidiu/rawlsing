# CLOSED35-R2-ASIAN5 — Synthetic Test Protocol

Status:

`TESTS_AUTHORED__NOT_EXECUTED`

Browser/GitHub tooling was used only. No raw source carrier was opened and no Python test runner was executed.

Synthetic tests are authored in:

`rawlsing_next/tests/test_closed35_r2_asian5_realization.py`

## Required rejection court

1. **country+ID replay identity rejection**
   - Construct two synthetic rows with the same native country and ID but different row ordinals.
   - Require distinct replay keys.
   - Explicitly reject `COUNTRY+IDnumber` as replay authority.

2. **source SHA drift**
   - Admit the canonical SHA under `SAV_NATIVE_GOVERNED`.
   - Mutate the SHA and require fail-closed.

3. **MR topology preservation**
   - Require exactly `IR3a`, `Q112`, `SE15`.
   - Require exact members and counted value 1.
   - Require `Q112 ∩ SE15 = SE15A..SE15M`.

4. **MR flattening rejection**
   - Delete a set or member.
   - Require failure.

5. **Q112/SE15 alias rejection**
   - Assert alias because of overlap.
   - Require failure.

6. **questionnaire-Q112 name inference rejection**
   - Assert native MR `Q112` has questionnaire item 112 semantics by name.
   - Require failure.

7. **routing inferred from missingness rejection**
   - Resolve the India module with different synthetic missing/sentinel states and country values.
   - Require the same governed bounded-unknown routing projection.
   - Resolve q186 without converting storage evidence into an exact risk set.

8. **undocumented weight selection rejection**
   - Preserve `w` as a carrier.
   - Require estimand/default state `BOUNDED_UNKNOWN`.
   - Default-selection call must fail.

9. **geography fabrication rejection**
   - Require raw source-local coordinate authority.
   - Require merged-to-instrument reconciliation to remain `BOUNDED_UNKNOWN`.
   - Cross-wave recoding remains unauthorized.

10. **candidate semantic divergence rejection**
    - A/B/C must carry one source-specific realization identity.
    - Mutate C's realization identity and require failure.

11. **S35/R35 edge binding**
    - Require exact edge tuple `EC01,EC07,EC08,EC10,EC12,EC13,EC14`.
    - Require R35 I01/I02/I03 hook metadata.
    - Require no semantic authority from the R35 hooks.

## Acceptance boundary

A future executed synthetic court may establish only that the realization implementation obeys these source-independent invariants.

It still cannot establish:

- raw-source execution;
- whole-source physical equivalence;
- A/B/C physical parity;
- I05;
- source certification;
- measured P2X.
