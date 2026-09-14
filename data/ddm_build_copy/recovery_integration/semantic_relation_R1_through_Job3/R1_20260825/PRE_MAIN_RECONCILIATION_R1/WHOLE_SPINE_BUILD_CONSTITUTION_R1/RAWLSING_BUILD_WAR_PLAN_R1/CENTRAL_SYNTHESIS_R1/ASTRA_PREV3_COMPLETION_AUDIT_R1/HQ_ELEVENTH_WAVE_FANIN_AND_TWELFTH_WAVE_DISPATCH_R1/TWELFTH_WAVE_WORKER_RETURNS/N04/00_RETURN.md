# N04 — governed bounded-court execution-surface recovery — governed return

Status: `BLOCKED__GITHUB_HOSTED_RUNNER_NOT_ALLOCATED`

Exact grain:
`RABOCHII_GOVERNED_BOUNDED_COURT_EXECUTION_SURFACE_RECOVERY_R1_ONLY`

Branch:
`agent/rabochii-prev3-w12-n04-governed-court-surface-recovery-r1`

Commission tip:
`b0bd8321addda0aff5298d5d61b2c69863b46003`

## Holding

No repo-content defect was found that is competent to explain or repair the zero-step governed-court failures.

The governed workflow used by the frozen M04 failures is byte-identical at Git blob `a974469aa1d83514d896e3de591d7618310ca493` to the workflow that successfully ran L01 only a few hours earlier. Control run `34806672726`, job `103859784864`, received GitHub-hosted runner `1000001019`, executed the protocol and bounded court, and concluded `success`.

The frozen M04 runs `34817399347` / job `103890925367` and `34817464330` / job `103891130623` both show `ubuntu-latest`, `runner_id: 0`, empty runner name, and zero workflow steps. An unrelated same-period main-branch `Rawlsing Worker Return Beacon` run, `34817473049` / job `103891159112`, independently shows the same `ubuntu-latest`, `runner_id: 0`, zero-step failure.

N04 then created an infrastructure-only neutral smoke fixture, without changing any production semantics or candidate tests:

- neutral fixture candidate commit: `745a080ed705938428b4688f23f6d3c6440fd000`;
- test: `rawlsing_next/tests/test_rabochii_governed_court_surface_smoke_n04.py`;
- test Git blob: `a28be7e15757c162e7eb7c64f198aac3dc768a86`;
- court spec: `.rabochii/court_spec.json`;
- court-spec Git blob: `1f7662580de38e12ddbc3ecd8afd6747e55da4f0`;
- evidence execution commit: `8c0e4e56299b7fcce716cdbabfb446149234731d`;
- probe PR: `#374`, draft, closed unmerged;
- neutral workflow run: `34819866310`, run number `424`;
- neutral job: `103898721968`.

The neutral smoke reproduced the same execution-surface failure: `failure`, `ubuntu-latest`, `runner_id: 0`, empty runner identity, zero steps, no job log blob, and zero receipt artifacts. Therefore the smoke test itself never executed and no lawful court receipt could be emitted.

Because the failure occurs before runner allocation and reproduces on a neutral infrastructure-only fixture while the exact same governed workflow blob has a recent successful control, a repository-content repair is not competent. The remaining defect is outside this commission's repository mutation authority: the GitHub-hosted runner allocation/execution entitlement surface must become available again before N04 can produce PASS.

## Smallest exact blocker

`N04_BLOCK__UBUNTU_LATEST_RUNNER_NOT_ALLOCATED__ZERO_STEP__NO_REPO_CONTENT_REPAIR_COMPETENT`

Blocker class:
`BLOCKED_EXECUTION_CAPABILITY`

Machine-readable blocker receipt:
`TWELFTH_WAVE_WORKER_RETURNS/N04/01_EXECUTION_SURFACE_BLOCKER_RECEIPT.json`

## PASS law

N04 does **not** issue PASS. The required neutral smoke court did not receive a runner, did not execute protocol steps, did not execute its bounded smoke test, and did not emit a valid court receipt.

The successor gate therefore remains closed. N04 has not qualified M02, M04, or M05, and has not run C09.

## Boundaries preserved

- repo-local production semantic repair: `NONE`;
- PRE-V3 ontology change: `NONE`;
- M02 qualification: `NOT_RUN`;
- M04 qualification: `NOT_RUN`;
- M05 qualification: `NOT_RUN`;
- C09 rerun: `NOT_RUN`;
- MAIN mutation: `NONE`;
- PRE-MAIN mutation: `NONE`;
- OBL063 revival: `NONE`;
- PRE-V3 scope: `OBJECTIVE_WORLD_ONLY`.

## Successor gate

After GitHub-hosted `ubuntu-latest` runner allocation is restored, rerun the already-frozen N04 neutral smoke court first. Only an actual run with runner allocation, protocol-step execution, the neutral bounded test, and a valid uploaded court receipt can convert N04 to PASS and wake M02 qualification, M04 OP014 qualification, and M05 qualification in parallel.

Terminal:
`N04_BLOCK__GOVERNED_COURT_SURFACE_NOT_REPO_REPAIRABLE__RUNNER_ALLOCATION_ZERO_STEP`
