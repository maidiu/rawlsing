# A — restore dropped accepted correction regressions — R5 return

**Job:** `PROGRAMMA-PYAT-UNIVERSAL35-SOURCE-MAPPING-20261106-R1`
**Branch:** `codex/pyat-universal35-src15-coordinate-20261106-r1`
**Continues:** `bc84799edbeaefd7785e178a0aaacc94f76260fe`
**F producer review:** `dcb2ff81c88aa08788a06acb62676e90f7674185` (PASS_SCOPED)
**Status:** `AUTHOR_TESTED__ACCEPTED_REGRESSIONS_RESTORED__PRODUCTION_UNCHANGED`

## Finding

The SRC15 coordinate patch replaced the accepted `cf44c5df` correction test
module (11 tests) with a 5-test module. That dropped accepted negative/regression
coverage required by the user goal.

## Action — test-only repair

Restored the complete accepted `cf44c5df` correction test module and merged the
unique SRC15 coordinate tests into it:

- 11 original accepted test functions restored with no assertion-count reduction.
- 2 unique SRC15 tests retained:
  `test_src15_coordinate_missing_range_and_observed_age_codes_are_bound`,
  `test_src15_coordinate_rules_are_exposed_to_current_owner`.
- Total: **13 tests**.
- No production file changed: coordinate correction, source-config registry,
  factory, ABI, provenance and SRC31/remaining state are unchanged.
- No new confidence-only test added.

## Receipt

```sh
python3 -m pytest -q -o addopts= -p no:cacheprovider \
  rawlsing_next/tests/test_source_configuration_corrections.py
```

Observed: **13 passed in 27.28s**.

`evidence_test_restore.json` compares AST test names/assertion counts:

- old accepted tests: 11
- new tests: 13
- missing old tests: 0
- weakened assertion counts: 0

`evidence_correction_tests.txt` is the exact module-only pytest receipt.
`evidence_changed_paths.txt` records the test-only/return diff.

## Preserved limits

- Production coordinate/sourceconfig/registry/factory/ABI unchanged.
- SRC31 and remaining accepted correction state unchanged.
- F producer review remains valid on the unchanged production patch.
- Full C11/native/all35 remains NOT_RUN; no source/native/science/actor authority.
- No provider/server/config/permission/protected changes.

## PROGRAMMA_DELTA

- **Identity:** same branch; production `bc84799…` unchanged; test module restored
  from accepted `cf44c5df…` plus SRC15 additions.
- **Function:** test-only regression restoration.
- **Input → output:** accepted 11-test module + 2 SRC15 tests → 13-test module.
- **Root/schema/clock/permission:** no change.
- **Actual first consumer:** NONE_VERIFIED; test-only repair.
- **Evidence:** `evidence_test_restore.json`,
  `evidence_correction_tests.txt`, `evidence_changed_paths.txt`.
- **Next action:** routine author receipt accepted; no new hostile court required.
