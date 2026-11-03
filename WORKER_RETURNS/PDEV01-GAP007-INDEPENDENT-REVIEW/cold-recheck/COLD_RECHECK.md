# GAP-007 focused cold recheck — 023534c vs 6a305

## Verdict

**REVISE** — core cold replay passes; the actual repair return still claims the
prior release ref and one optional tamper guard was not implemented.

## Candidate and snapshot

- Candidate: `023534c7f3f7fc5411ed52676490a1a0f70cd864`
- Previous candidate: `6a305523074898dda9c75e3e24fb6ea6fa2eeb40`
- Snapshot: exact `git archive` of candidate `WORKER_RETURNS/PDEV01-GAP007`
  from sibling `pyat-pdev01-gap007`, extracted to a disposable temp directory.
- Frozen source: `frozen/source.sav`, SHA
  `5009f3c9272dcbfb15a48b17cfff51f9afa67e60d6a2c1364c9aa07bc6732e4f`.

## Cold replay result

Two fresh processes produced byte-identical JSON:

- Source SHA: `5009f3c9272dcbfb15a48b17cfff51f9afa67e60d6a2c1364c9aa07bc6732e4f`
- Release ref: `64cf774b408686394c8caf9969f442b518e365d04c924bafefb6204239c9bf03`
- Manifest ref: `6fd0f47cde582407a6afb6f21d3fb5c7d001cc14b03f688f34cce87770eef8ab`
- I05 compilation ref: `78568e5e47b086d9f537a6359b8e729ab2d8e42305981075d21aa613e0b31dc9`
- 210 query refs equal across runs.
- Committed `actual_trace.json` equals both fresh runs.

Preserved core:
- 210 executed / `COMPLETED`
- 210 `SUPPORTED` facts
- 630 typed refusals: CONDITIONAL 210, JOINT 210, HETEROGENEITY 105,
  RECURSIVE_BRANCH 105
- 840 total and 840 distinct original operation refs
- I05 remains a separate capability call: 16 receipts, 30 facts, 16 candidates,
  not part of the P1 840 accounting
- Single synthetic `C11LogicalRelease` is reused across all 35 roster/wave
  entries and all 210 bound units (TEST_ONLY scope).

The prior cold-replay nondeterminism is fixed by the frozen SAV.

## Remaining defects

### 1. Actual repair return release ref is stale

`00_RETURN.md` says release
`383716e4c9d233df69ef8cd508f7ffa5053d7a7355e7135a170eb1c2b337d9c1`,
but the actual trace and both cold runs use
`64cf774b408686394c8caf9969f442b518e365d04c924bafefb6204239c9bf03`.

Smallest repair: update the return text to the actual frozen-source release ref.
No code change.

### 2. Tamper refusal is not implemented in the runtime

`replay_repair.py` only checks that `frozen/source.sav` exists. A tampered file
was accepted and produced source SHA `1b9f1f05…` and release ref `7b432f34…`.
`test_06` does check the frozen SHA and fails on the tampered fixture. The task
conditioned tamper refusal on “if implemented”; it is recorded here, not used as
the primary verdict basis.

## Commands

```sh
git -C /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-pdev01-gap007 \
  archive 023534c7f3f7fc5411ed52676490a1a0f70cd864 WORKER_RETURNS/PDEV01-GAP007 \
  | tar -x -C <snapshot>

PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 PYTHONPATH=<snapshot>:<sibling> \
  python3 <snapshot>/WORKER_RETURNS/PDEV01-GAP007/repair/replay_repair.py > run1.json
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 PYTHONPATH=<snapshot>:<sibling> \
  python3 <snapshot>/WORKER_RETURNS/PDEV01-GAP007/repair/replay_repair.py > run2.json

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=<sibling> \
  python3 -m pytest <sibling>/WORKER_RETURNS/PDEV01-GAP007/repair/test_repair.py -q -o addopts=''
```

Candidate tests: **7 passed** (48.60s). No candidate writes; TEST_ONLY; no source
rights, original data, merge, CI or wake.
