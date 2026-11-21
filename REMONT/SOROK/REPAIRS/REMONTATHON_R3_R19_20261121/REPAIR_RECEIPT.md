# REMONT R19 — P004 atomic selected-project course / R17 P018 provenance

**Parent:** R18 [#1241](https://github.com/maidiu/rawlsing/pull/1241) `a4a495bbb456bd211b4fbdbd29478c0f0052603f`.
**Current P018 reuse:** R17 [#1230](https://github.com/maidiu/rawlsing/pull/1230) descendant `28bf7fc48264d433ecf172bd0846744a3476222e`, exact `storage.py` blob `75087ed57c3a39d82b9ded5ebf8123f949e54c21` and `test_r17_source_preflight.py` blob `b25f93b2fd81fa814bfeee9be843d7279cf0b31b`.

## Actual first fault
R18 `record_activity_afterlife` preflighted selected means/existence but checked duplicate event occurrence *inside* the append loop. With valid selected project A (fresh) then B (already history event E), A's operational history was changed before B raised `DUPLICATE_ACTIVITY_EVENT_FOR_PROJECT`; the rejected operation left an inconsistent partial historical trace.

## Actual isolated test-first court
A self-contained copy of the frozen R18 function (same source function body, substituting module imports and the GRADE constant) ran eight targeted tests under **Python 3.13.5**. Before the patch: **5 PASS, 3 FAIL** normal and -O. After moving every selected project duplicate preflight before the append loop: **8 PASS** normal, **8 PASS** -O, **8 pytest PASS**. Cases cover duplicate in second versus first selected project, retained preexisting actor history, legacy multi-project assertions, incompatible selected means, valid multi-project activity, legacy single basis, and a projectless attempt.

These tests were **not** run against a complete Git checkout. No full inherited (296+) suite, Python 3.11, integration demo, cold SQLite replay, or independent acceptance is claimed for this R19 tree. The new exact-tree test file is `tests/test_remontathon_r19_atomic_history.py`; run that first, then the inherited R17/R18/whole-organism courts.

## Repair
The old per-project duplicate history check was replaced with a single preflight over all selected matching project courses, before any `operational_history` or `activity_history` mutation. R18's selected means/existence preflight remains unchanged, and legacy direct helper provenance remains explicitly graded. This is atomicity of this specific sourcefree function only, not a distributed database atomicity proof.

## Source custody and limits
- R18 selected means source was originally `activity.py` blob `9af345b8cea9282988aab52cfe22badd56633d7e`.
- R19 patched `activity.py` blob `a9d32efece356c0c398d7cf93dc1bfd8c932a22f`.
- Reused R17 source `storage.py` blob `75087ed57c3a39d82b9ded5ebf8123f949e54c21`; newer P018 typo/unsafe-envelope handling is now inherited at this new source candidate.
- Reused R17 test blob `b25f93b2fd81fa814bfeee9be843d7279cf0b31b`.
- R18 73 P, T0, E6 unchanged. P004 remains PARTIAL. Original protected PRE-MAIN and SOROK PROGRAMMA/CURRENT_PROGRESS remain untouched; receiving requires separately competent owner.

## Required local exact-tree commands
From `SEAM/ORACLE/UM_SOROK_ORGANISM_R3`, under Python 3.11:

```sh
python3.11 -m unittest -v tests.test_remontathon_r19_atomic_history tests.test_remontathon_r18_p004_selected_means tests.test_r17_source_preflight
python3.11 -O -m unittest -v tests.test_remontathon_r19_atomic_history tests.test_remontathon_r18_p004_selected_means tests.test_r17_source_preflight
python3.11 -m unittest discover -s tests -q
python3.11 -O -m unittest discover -s tests -q
python3.11 -m pytest -q
python3.11 -m um_sorok_organism demo
```
Record exact HEAD, test exits, cold reopen/event hash, SHA256 and independent hostile review. No producer/native authority assumed.
