# SOROK B3AS-I2 independent schema/readset repair court R1

Verdict: **ACCEPT_SCOPED** (see `00_RETURN.md`). Both unchanged B3A-I2 schema REDs close under the exact authored repair `16f15a125ba54cdf17f5d41be2d851bbcd2240d7`; all frozen, atomicity, B3, F2, E3, X3, inherited and sourcefree expectations are preserved unchanged.

## Layout

- `00_RETURN.md` — custody, execution, RED accounting, verdict.
- `02_REQUIREMENTS_AND_LIMITATIONS.md` — preserved limits and outstanding owner permissions.
- `preregistration_independent.json` — independent hostile-control predictions, frozen before execution.
- `test_independent_hostiles.py`, `independent_worker.py` — this reviewer's own controls and process worker (no candidate/frozen edits).
- `freeze_hashes.json` — pre-execution hashes and the logged reviewer-side fixture amendments.
- `environment_passport.json` — sanitized editor/model/OS/Python/SQLite passport.
- `evidence/results_summary.json` — machine-readable accounting.
- `evidence/junit/` — frozen JUnit for every court, pre- and post-repair.
- `evidence/independent/` — cold schema/row/SQL receipts for the independent controls.
- `evidence/independent_run1/` — preserved first-run outputs before fixture amendments.
- `evidence/inherited/` — inherited command exits and preserved historical negative logs.
- `evidence/cold_replay_audit.json`, `evidence/actual_imports.json` — cold replay and import hash verification.

## Reproduction

Runtimes are materialized from pinned Git blobs through the candidate's `materialize.py` (199 verified entries). Frozen courts are executed with `REVIEW_B3_ROOT` / `REVIEW_EVIDENCE` (B3A-I2 court) or `I2_CANDIDATE_ROOT` / `I2_EVIDENCE` (independent controls) pointing at a fresh materialized candidate. No author database or execution log is reused.

No semantic adoption. No next commission. Findings return to Sorok HQ.
