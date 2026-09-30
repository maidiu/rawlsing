# PYAT C1-01 — R6 SOURCE-FREE EXECUTION QUALIFICATION — R1

Status: ISSUED__USER_MEDIATED_CODEX_LAUNCH_REQUIRED

Role: Codex source-free execution-only worker.

Branch:
`agent/codex-pyat-hq133-c1-01-r6-execution-r1`

Exact patch under test:
`663379caa7c9b8a80bca889d8d5b59d0486ff901`

Do not modify implementation, tests, current C1 packet, workflows or court specs.

Your only job is to execute the exact returned R6 source-free test path on the exact patch and bank an honest qualification receipt.

## Exact command

Run:

`python -m pytest -q rawlsing_next/tests/test_pre553_analytical_composition.py rawlsing_next/tests/test_pre553_empirical_query.py rawlsing_next/tests/test_source_backed_positioned_subject_possibility.py`

If normal repository setup requires installation of project test dependencies, use an isolated disposable environment and record exactly what was installed.

Do not alter repository source/test content to make execution possible.

## Required provenance

Record:
- exact tested Git commit;
- clean/dirty worktree before and after;
- OS/platform;
- Python version;
- pytest version;
- relevant dependency versions;
- exact command;
- exit code;
- passed/failed/error/skipped counts;
- collection errors if any.

## Absolute prohibitions

Do not access or materialize raw survey sources.
Do not run Candidate A/B/C.
Do not run measured P2X.
Do not run real-source C11 materialization.
Do not edit production code or tests.
Do not use the user's Mac unless the user explicitly authorizes that in the actual worker conversation.

If the exact patch fails, preserve the failure exactly and return it. Do not repair in this lane.

## Return terrain

Write only:
`WORKER_RETURNS/PYAT-C1-01-R6-EXECUTION-QUALIFICATION-R1/**`

Required:
- `00_RETURN.md`
- `01_ENVIRONMENT.json`
- `02_EXECUTION_RECEIPT.json`
- `03_FINAL_DISPOSITION.json`

Allowed:
- `PASS_SOURCE_FREE_QUALIFICATION`
- `FAIL_SOURCE_FREE_QUALIFICATION`
- `BLOCKED_EXECUTION_CAPABILITY`

Terminal:
`C1_01_R6_EXECUTION_QUALIFICATION_RETURNED__HQ_ADJUDICATION_REQUIRED`
