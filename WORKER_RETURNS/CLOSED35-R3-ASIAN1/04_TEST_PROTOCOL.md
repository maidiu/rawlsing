# CLOSED35-R3-ASIAN1 — Synthetic Test Protocol

Status:

TESTS_AUTHORED__NOT_EXECUTED

Browser/GitHub tooling was used only. No raw survey carrier was opened and no Python test runner was executed.

Synthetic tests are authored in:

rawlsing_next/tests/test_closed35_r3_asian1_realization.py

## Required rejection court

1. Exact source and BIG-5 reader drift
   - Admit only the canonical SHA under SAV_SOURCE_DECLARED_BIG5.
   - Mutate the SHA and require fail-closed.
   - Replace BIG-5 with a generic/native/later-wave reader mode and require fail-closed.

2. Decoded BIG-5 text semantic promotion / normalization
   - Preserve a decoded text string exactly.
   - Attempt to treat readability as documentary semantic authority and require failure.
   - Attempt source-text normalization/harmonization without authority and require failure.

3. Native ID replay invention
   - Construct two synthetic rows sharing native country/idnumber with different row ordinals.
   - Require distinct replay keys.
   - Reject idnumber and country+idnumber as hard replay authority.

4. Typed-missing collapse
   - Preserve q001=98 as FORMAT_USER_MISSING_VALUE with stored value and declaration.
   - Preserve q018_1 as SYSTEM_MISSING without an invented stored value.
   - Attempt to collapse the two physical states and require failure.
   - Keep semantic response-state mapping BOUNDED_UNKNOWN.

5. Routing inferred from missingness or decoded labels
   - Resolve one variable under different synthetic missing/observed states and different readable labels.
   - Require identical BOUNDED_UNKNOWN routing state.
   - No physical incidence or label text may mint applicability.

6. Nine-weight collapse / default invention
   - Require exact distinct tuple w_jp,w_hk,w_kr,w_cn,w_mo,w_ph,w_tw,w_th,w_all.
   - Delete/alias one carrier and require failure.
   - Require role/estimand and default-use state to remain BOUNDED_UNKNOWN / unauthorized.
   - Default-selection call must fail.

7. q097 ranked-slot flattening
   - Require q097_1,q097_2,q097_3 at ranks 1,2,3 and packet ordinals 135,136,137.
   - Reorder, duplicate or flatten one slot and require failure.

8. Geography / cross-wave leakage
   - Preserve country and level3 as source-local carriers.
   - Require cross-wave recoding disabled.
   - Instrument reconciliation remains BOUNDED_UNKNOWN.
   - W4/W5 geography must not be imported.

9. Candidate-specific semantic divergence
   - A/B/C must carry one source-specific realization identity.
   - Mutate C's identity and require failure.

10. S35/R35 binding
    - Require exact edge tuple EC01,EC02,EC05,EC07,EC09,EC12,EC13,EC14.
    - Require R35 I01/I02/I03 hook metadata.
    - Require the hooks to grant no survey-semantic authority.

## Acceptance boundary

A future executed synthetic court may establish only that the implementation obeys the governed realization invariants.

It still cannot establish:

- raw-source execution;
- whole-source physical equivalence;
- A/B/C physical parity;
- I05;
- source certification;
- measured P2X.
