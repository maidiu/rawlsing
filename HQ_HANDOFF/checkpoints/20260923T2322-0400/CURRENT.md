# RAWLSING HQ CURRENT — FIABC DISPOSITIVE TERMINAL LAUNCHER READY

Status: `RAWLSING_FIABC_PRE_CANDIDATE_STOP_SEALED__DETERMINISTIC_TERMINAL_LAUNCHER_QUALIFIED__MEASURED_SIX_CELL_COURT_NEXT`

Checkpoint: `20260923T2322-0400`

## Governing decisions

- `HQD-2026-09-23-087` — adopt independently accepted LiTS/WVS7 T3 freeze, restore accepted lineage home to canonical PRE-MAIN, and authorize the protected six-cell execution substrate.
- `HQD-2026-09-23-088` — adopt the deterministic control-plane Terminal launcher.

## Frozen execution substrate

Protected branch:

`agent/rabochii-prev3-ee-p2x-final-abc-equal-work-execution-r1`

Exact execution HEAD:

`b53ff08921af263b9db4d1ad038f35fbc12b990a`

Do not advance or edit this branch for launcher packaging.

## Frozen answer key

- LiTS oracle identity: `e5d66db4b6f8339672b0f4828b72a8df68b5525bf71ecfda899d0531d618a98a`
- WVS7 live standard-oracle identity: `e546c15533ba138be9995095059ea3b70b64a6d7b5765e3789935cff7342ef00`
- T3 SHA-256: `7dfb62362b983b92dee2774d862a46c0c0ce3ca2c3bb48850e0f400346936908`
- PRE_CANDIDATE_STOP: `203fae32dc31ad6afe6dd2e85aed0ddf1a262d9a93efa6597a0c09173c64b384`

## Qualified deterministic launcher

Launcher:

`HQ_HANDOFF/launchers/RUN_DISPOSITIVE_FIABC_SIX_CELL.sh`

Launcher implementation commit:

`355a71cc27b8e95188a66d81eccc52abe2ee9d0a`

Launcher Git blob:

`fb79e4962fa4bc55dc94527d8834bf0c764b5471`

Qualification commit:

`9ab9d43a5d9218a69ae025214739a3470240cddd`

Qualification receipt:

`HQ_HANDOFF/launchers/FIABC_DISPOSITIVE_SIX_CELL_LAUNCHER_QUALIFICATION_20260923.json`

The launcher:
- requires exact branch and HEAD;
- requires exact CPython 3.11.3 / pyreadstat 1.3.6 / pyarrow 25.0.1 on Darwin x86_64;
- verifies exact LiTS/WVS source SHA-256 values;
- requires a fresh persistent work root outside the repository and temporary directories;
- copies and rehashes the already-frozen LiTS oracle, WVS oracle, and T3 receipt;
- verifies PRE_CANDIDATE_STOP invariants;
- does not invoke `produce-lits`;
- does not invoke `freeze-t3`;
- generates only current-head succession and lifecycle receipts;
- runs the fixed driver preflight;
- proves T3 is unchanged after preflight;
- invokes the fixed process-isolated driver `--run`;
- preserves the work root and logs;
- performs no Git mutation.

Syntax qualification and hostile static assertions passed. Qualification itself opened/hashed/decoded zero survey sources and started zero candidate processes.

## Next lawful action

From the canonical PRE-MAIN checkout, obtain the launcher above.

Run it against a clean worktree of the protected execution branch at exact head `b53ff089...`.

Required operator inputs:

- `FIABC_REPO_ROOT` — path to that exact protected execution checkout;
- `LITS_PATH` — exact canonical LiTS source;
- `WVS_PATH` — exact canonical WVS7 source;
- `WORK_ROOT` — fresh persistent court root outside the repo and temporary directories;
- optionally `PYTHON_BIN` if the exact qualified Python is not `python3`.

Then execute the launcher directly from Terminal.

Do not use Codex or another model to steer a healthy run.

If the launcher or driver stops, preserve the complete work root unchanged and adjudicate the emitted evidence before any retry/resume.

## Downstream gates

- P2 HQ synthesis: BLOCKED pending measured six-cell return.
- P3 hostile kill: BLOCKED pending P2 provisional favorite.
- final architecture selection: BLOCKED pending P3.
- FF02: downstream; not a prerequisite for FIABC.
