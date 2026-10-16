# Reproduce M06

Use the assigned branch in an isolated worktree of the existing authenticated Git store, with Python3.11.3 and pytest9.1.1. No dependency installation, model API or external source is required. All paths below are repository-relative. Preserve an existing `runtime/` before fresh reconstruction; staging refuses to overwrite it.

```sh
python3 WORKER_RETURNS/SOROK-R3-HQ316-M06-M05-OWNER-ANCESTRY-INDEPENDENT-R1/repro/stage.py
python3 WORKER_RETURNS/SOROK-R3-HQ316-M06-M05-OWNER-ANCESTRY-INDEPENDENT-R1/repro/run_baseline.py
python3 WORKER_RETURNS/SOROK-R3-HQ316-M06-M05-OWNER-ANCESTRY-INDEPENDENT-R1/repro/run_new.py
python3 WORKER_RETURNS/SOROK-R3-HQ316-M06-M05-OWNER-ANCESTRY-INDEPENDENT-R1/repro/package_audit.py
```

The original delivered run materialized M05's 37 non-evidence packet files from exact Git blobs in one source-staging command, then ran its unchanged `review/stage.py` and `repro/install_candidate.py`. `repro/stage.py` encapsulates those same operations for reproduction. The original scientific execution then invoked M05's unchanged `review/run_phase.py after`, `review/run_author.py` and `repro/run_historical.py` independently; `run_baseline.py` wraps the same invocations. It was not retroactively claimed as the original launcher. The four baseline child commands, exact pytest arguments, exit statuses, JUnit and stdout are retained under `evidence/baseline638`, `evidence/m05_author48` and `evidence/historical_nine`.

M05's unchanged stage creates a local Git wrapper adding `--full-tree` only for nested `ls-tree` reconstruction. It does not change scientific source or tests. All nested paths remain in this return's ignored runtime. It reconstructs from Git, not another chat's files. The M05 candidate installer overlays only the two commissioned source files at the inherited M01 import location.

`run_new.py` checks the actual test and preregistration bytes against prospective commit8f6d11c54f313665e9320d4d58af7b6d1825796e before invoking pytest in a fresh process. The child captures actual module files, source hashes and the EMPTY guard before/after. Its expected result is114 PASS. The original frozen file is unchanged; do not rewrite a failed assertion. The new source-body mutation controls run serially, restore exact bytes in `finally`, and never modify canonical repository code.

The baseline wrapper expects638 PASS and48 PASS. The historical Python wrapper exits0 only when its actual pytest child exits1 with exactly9 failures. Those are preserved failures, not successes. No complete historical585 run is claimed. The packaging auditor independently checks counts, every original case name/outcome, original test bytes, frozen source identities, actual imports and the36-arm native receipts. Audit corrections concern metadata lookup only and do not re-execute science.

Portable evidence replaces personal absolute paths and hostname metadata with tokens; assertions, expected/observed effects, synthetic owner data, source preimages and outcomes are unchanged. Exact absolute import paths were observed at runtime, while the published passport records paths relative to this return. The raw M05 execution metadata remains in the ignored runtime; path-redaction digests accompany the portable packet. No actual source survey data, credentials or personal host details are published.
