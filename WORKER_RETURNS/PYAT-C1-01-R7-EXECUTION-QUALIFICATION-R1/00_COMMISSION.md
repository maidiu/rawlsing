# PYAT C1-01 — R7 EXACT-PATCH SOURCE-FREE EXECUTION QUALIFICATION — R1

Status: ISSUED__USER_MEDIATED_CODEX_LAUNCH_REQUIRED

Role: Codex exact-patch source-free execution qualifier.

Branch:
`agent/codex-pyat-hq136-c1-01-r7-execution-r1`

Exact R7 return head to qualify:
`0da3c9c13ffd91cf50ab93f6280949eb960792c0`

R7 implementation tip recorded by worker:
`f7d72915fe6ac6b7dc2dc583fff462f748c3556d`

R7 commission:
`7ea809f3b4433d24c027eb0ad3e98b0a6d3fb607`

This is execution-only.

Do not modify production code, tests, packets, workflows or court specs.

## Important prior capability finding

The previous C1 execution lane:
`a92f977e9ce4615326b09ad9e3407b3b02684788`

already established that its isolated cloud shell had Python/pytest but could not materialize an exact GitHub worktree because GitHub network transport was unavailable.

Do not spend the job rediscovering that same limitation.

A valid qualification requires an exact executable checkout of the commissioned R7 head (or an exact checkout whose code/test blobs are proved identical to that head) plus authoritative worktree provenance.

If the available environment cannot obtain that exact worktree, return `BLOCKED_EXECUTION_CAPABILITY` promptly.

If the user explicitly authorizes use of their Mac in this worker conversation, you may use that exact repository checkout as the execution surface, provided you:

- verify the exact Git commit/worktree before execution;
- do not open/materialize raw survey files;
- use an isolated source-free Python environment;
- record clean/dirty status before and after.

Do not use the user's Mac without explicit authorization in that worker conversation.

## Exact command

Run:

`python -m pytest -q rawlsing_next/tests/test_pre553_analytical_composition.py rawlsing_next/tests/test_pre553_empirical_query.py rawlsing_next/tests/test_source_backed_positioned_subject_possibility.py`

Do not alter tests to make the command pass.

## Required provenance

Record:

- exact tested Git head;
- exact code blob for `rawlsing_next/pre553_analytical_composition.py` expected:
  `26f3380cb83cbbcedc87c74aaf603b0492c8ce8f`
- exact test blob expected:
  `db6b876f15d145cfc48cc6d944e48da4460842d3`
- clean/dirty status before and after;
- OS/platform;
- Python version;
- pytest version;
- relevant installed dependency versions;
- exact command;
- exit code;
- passed/failed/error/skipped counts;
- collection errors if any.

If the exact returned head contains documentary commits after the implementation tip, that is fine; prove that the executed production/test blobs exactly equal the two expected blobs above.

## Absolute prohibitions

Do not access or materialize raw survey files.
Do not run Candidate A/B/C.
Do not run measured P2X.
Do not run real-source C11.
Do not edit implementation/tests to repair a failure.
Do not begin C1-02.

If tests fail, preserve the failure exactly.

## Return terrain

Write only:

`WORKER_RETURNS/PYAT-C1-01-R7-EXECUTION-QUALIFICATION-R1/**`

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

`C1_01_R7_EXECUTION_QUALIFICATION_RETURNED__HQ_ADJUDICATION_REQUIRED`
