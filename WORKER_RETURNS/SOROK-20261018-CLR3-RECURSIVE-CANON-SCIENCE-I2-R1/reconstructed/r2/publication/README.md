# Published CLR2 archival closure

`00_PUBLICATION_RETURN.md` supplies publication authority/status. Original R1/R2 reports and evidence remain unchanged. Start with the portable verifier from the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 WORKER_RETURNS/SOROK_CONTINGENT_LIVES_CAUSAL_COURT_R2_REASSESSMENT/publication/verify_publication.py --smoke
```

It validates frozen bytes and prior receipts and reproduces the three baseline outputs. It does not run all courts.

To rerun the unchanged courts in a fresh checkout, install/use Python 3.11+ and pytest, and run these commands separately from the indicated directories. The publication worker verified the old receipts and ran only the smoke; the commands below are reproduction instructions, not claims of additional runs.

From `WORKER_RETURNS/SOROK_CONTINGENT_LIVES_CAUSAL_COURT_R1/inherited/causal_experiment/`:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -v -p no:cacheprovider test_world_intersection.py
```

Expected: 24 PASS, exit 0.

From `WORKER_RETURNS/SOROK_CONTINGENT_LIVES_CAUSAL_COURT_R1/`:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -v -p no:cacheprovider test_controls.py
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -v -p no:cacheprovider test_falsifiers.py
```

Expected respectively: 23 PASS/exit 0 and 6 RED/exit 1. Run each command even though the second is intentionally RED.

From `WORKER_RETURNS/SOROK_CONTINGENT_LIVES_CAUSAL_COURT_R2_REASSESSMENT/`:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -v -p no:cacheprovider test_adjudication.py
```

Expected: 18 PASS/exit 0, confirming audit observations rather than repairs to the six old assertions. To save fresh JUnit, append `--junitxml=...` with a new path outside the frozen trees; do not overwrite prior receipts.

The archival R2 runner additionally requires the old unpublished Git commit for custody checks. Use the verifier/direct commands above in a fresh clone. The existing R1 runner writes old evidence in place, so it is not the archival publication entry point.

The 66-source-file manifest proves copied artifact identity. This directory's SHA256SUMS covers new publication records (excluding itself and its referring manifest). No old numerical rule, test expectation, frozen inventory or reassessment was altered.
