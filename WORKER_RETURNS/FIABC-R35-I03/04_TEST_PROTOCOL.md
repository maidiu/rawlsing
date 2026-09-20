# FIABC-R35-I03 — Test Protocol

## Exact test file

`rawlsing_next/tests/test_fiabc_r35_i03_physical_equivalence.py`

## Authored cases

1. direct-raw positive control produces the physical-only PASS receipt;
2. an EC01-only source is not forced to carry irrelevant MR/weight evidence;
3. wrong reader version fails despite equal source SHA and equal semantic observation;
4. compatibility execution promoted to semantic authority fails;
5. all-missing column loss fails;
6. display representation replacing raw magnitude fails;
7. raw-header/dictionary-stream mismatch normalized away fails;
8. MR topology flattening fails despite identical raw vectors;
9. weight candidates discarded/default-selected fail;
10. subset/cache dropping an expectation-declared source-native dimension fails;
11. equal semantic observation with unequal physical metadata fails;
12. non-raw derivative without parentage receipt fails;
13. derivative parentage terminating at wrong canonical ancestor fails;
14. verified derivative parentage can close to the same canonical expectation;
15. EC14 without real atomic composition fails.

## Qualification command

`python -m pytest -q rawlsing_next/tests/test_fiabc_r35_i03_physical_equivalence.py`

## Commission execution boundary

The command is specified but was not run by this browser/GitHub-only worker.

No raw survey carrier is needed by these tests; fixtures are synthetic physical-contract objects.

No measured P2X is authorized or required.

## Hostile-court acceptance

R35-Q01 should treat I03 PASS as valid only when all of these remain true:

- exact canonical source identity;
- exact reader/config identity;
- exact I01 physical metadata digest;
- complete source-declared physical dimension closure;
- valid I02 parentage for every derivative path;
- explicit nonimplication of semantic/certification PASS.
