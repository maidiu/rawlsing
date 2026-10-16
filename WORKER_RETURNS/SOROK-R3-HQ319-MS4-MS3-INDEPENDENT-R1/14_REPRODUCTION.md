# Reproduction

Use real Git/Python/pytest in a separate sparse worktree on this review branch, with source objects available in the repository store. All commands below run from the repository root. `R=WORKER_RETURNS/SOROK-R3-HQ319-MS4-MS3-INDEPENDENT-R1`. No original survey or model/actor environment is used.

1. `PYTHONDONTWRITEBYTECODE=1 python3 "$R/repro/stage.py"` reconstructs target377, MS2 and MS1 packets. It refuses to overwrite an existing staged runtime. Only ignored staging below this return is written. Every source byte is checked against Git.
2. `python3 "$R/repro/install.py" old`; then `python3 "$R/repro/run.py" old original120 ms2_51 p3b`; `python3 "$R/repro/run.py" ms4_on_old hostile`; `python3 "$R/repro/run.py" followup_on_old followup`.
3. `python3 "$R/repro/install.py" ms3`; then `python3 "$R/repro/run.py" ms3 original120 ms2_51 p3b author47 selector12`; `python3 "$R/repro/run.py" ms4_on_ms3 hostile`; `python3 "$R/repro/run.py" followup_on_ms3 followup`.
4. `PYTHONDONTWRITEBYTECODE=1 python3 "$R/repro/audit.py"`; `PYTHONDONTWRITEBYTECODE=1 python3 "$R/repro/causal_audit.py"` verify byte custody/imports/frozen tests, aggregate real JUnit, and check causal invariants.

The subprocess runner sets `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`, `PYTHONDONTWRITEBYTECODE=1`, disables conftest/cache and runs pytest `-vv --tb=short --import-mode=importlib`. Each court retains all stdout/stderr, real JUnit, actual imported module paths/digests, exact command, timing and child exit code. The outer orchestration returns0 after saving results; it does not imply the child tests passed. Consult `execution.json` and JUnit. The audit asserts expected scientific/historical failures rather than treating all0 as success.

Expected outputs are the table in00_RETURN. The original85 must still yield ten literal REDs on MS3; do not edit its assertions to obtain green. The separately frozen follow-up20 must pass. P3b must remain a real FAIL with DEFER=None-effect on both sides. Original120 retains two missing-law-map failures. No test is skipped/xfail-rewritten and no native code is patched.

Portable evidence normalizes only the absolute worktree prefix and any JUnit hostname to nonidentifying aliases. Raw outputs are retained locally in ignored `staging/raw_evidence`; raw and normalized digests plus transformations are recorded in11_EVIDENCE_PORTABILITY.json. All test text, failure content, counts, timing and source identities remain. Files copied from earlier returns are not represented as new execution:07_TARGET_ALL_JUNIT_AUDIT explicitly labels them by target Git SHA; fresh evidence is under this return's own evidence directory.

Preregistration chronology:6bc2aa28ee444ffbb270ca00fdf1ae776bd284ae initial; ed1c6954c5d2637d433883db740ba5e9e3fcd83f static pre-run correction; ca0ff2a84db13e0ccb2d8aabefe7b46c6bd608a1 follow-up after original85. Frozen file SHA-256 checks execute before the relevant pytest collection. The original85 is identical across old/MS3 runs.
