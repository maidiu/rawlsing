# Reproduce the candidate court

Use the authenticated shared Git object store and an isolated worktree of the assigned branch, Python/pytest and all pinned commits. Run from repository root; all writes stay in this return. A fresh reconstruction refuses an existing `runtime/`; explicitly preserve/move any existing runtime rather than treating it as disposable. The delivered run used a live-verified warm M04 static closure, copied into this own return without mutable process-state continuity.

```sh
python3 WORKER_RETURNS/SOROK-R3-HQ315-M05-M04-PROVENANCE-ANCESTRY-REPAIR-R1/review/stage.py
python3 WORKER_RETURNS/SOROK-R3-HQ315-M05-M04-PROVENANCE-ANCESTRY-REPAIR-R1/review/run_phase.py before
python3 WORKER_RETURNS/SOROK-R3-HQ315-M05-M04-PROVENANCE-ANCESTRY-REPAIR-R1/repro/run_historical.py
cp -R WORKER_RETURNS/SOROK-R3-HQ315-M05-M04-PROVENANCE-ANCESTRY-REPAIR-R1/evidence/historical_nine WORKER_RETURNS/SOROK-R3-HQ315-M05-M04-PROVENANCE-ANCESTRY-REPAIR-R1/evidence/before/
python3 WORKER_RETURNS/SOROK-R3-HQ315-M05-M04-PROVENANCE-ANCESTRY-REPAIR-R1/repro/install_candidate.py
python3 WORKER_RETURNS/SOROK-R3-HQ315-M05-M04-PROVENANCE-ANCESTRY-REPAIR-R1/review/run_phase.py after
python3 WORKER_RETURNS/SOROK-R3-HQ315-M05-M04-PROVENANCE-ANCESTRY-REPAIR-R1/review/run_author.py
python3 WORKER_RETURNS/SOROK-R3-HQ315-M05-M04-PROVENANCE-ANCESTRY-REPAIR-R1/repro/run_historical.py
cp -R WORKER_RETURNS/SOROK-R3-HQ315-M05-M04-PROVENANCE-ANCESTRY-REPAIR-R1/evidence/historical_nine WORKER_RETURNS/SOROK-R3-HQ315-M05-M04-PROVENANCE-ANCESTRY-REPAIR-R1/evidence/after/
python3 WORKER_RETURNS/SOROK-R3-HQ315-M05-M04-PROVENANCE-ANCESTRY-REPAIR-R1/review/audit.py
```

Before running the audit after a fresh reconstruction, retain each historical invocation under `evidence/before/historical_nine` and `evidence/after/historical_nine`, as in the delivered packet. The original wrappers write their single latest root historical directory. Phase runner snapshots original413, independent100, original74 and unchanged M04 51 into phase directories, preserving before-results when after-execution overwrites original harness output locations. The original M04 child exits1 with ten failures before repair; the phase runner validates and records that exact child exit. After repair all638 exit0. The historical child exits1 with nine literal failures; its wrapper validates that identity/count without calling them passes. New author48 exit0. `AUDIT_OK` means evidence consistency, not independent acceptance.

The copied M03 `repro/` scripts are exact historical harness bytes. Do not invoke their `repro/audit.py` as M05's acceptance auditor; it describes M03's source/seal and expected M02 baseline. M05's `review/audit.py` verifies this court. The generated Git wrapper adds `--full-tree` only for nested `ls-tree` staging, leaving scientific source/tests untouched.

Two baseline source files are retained under ignored `runtime/m03_original`; M03 original blobs are 3eb2d02aee8dc840e7cac1f99230d7c69adc2f58 and2434bda6f4b00e6ea5881291f5422227e8045e74. The explicit installer overlays the two candidate files at the actual original M01 import location. No accepted owner monkeypatch is used. The complete patch is `candidate/M03_TO_M05.patch`; `candidate/M01_TO_M03.patch` is inherited historical source, not the new repair.

`03_AUTHOR_FREEZE.json` records actual pre-execution file digests. The original local freeze15a25d19… preceded implementation and first author execution. Its published portable counterpart b13db905… was made afterward to redact machine path/hostname metadata from baseline evidence, with identical tests, predictions, source and outcomes. That later counterpart is not claimed prospectively created. The privacy-custody receipt documents the mapping. Final portable metadata preserves assertions/results; raw metadata remains only in ignored local storage. The generated `toolbin/` and runtime markers are host-local.

Actual runtime is Python3.11.3/pytest9.1.1. All ordinary tests construct fresh synthetic owner instances. Recorded reconstruction calls are isolated verification calls, not additional native commits on the live Cell. M06 must independently inspect the new reconstruction/terminal-state logic and scientific limitations; no helper or acceptance reviewer is auto-launched here.
