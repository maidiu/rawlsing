# GAP-007 final focused recheck — d3d6e4879

## Verdict

**PASS_SCOPED**

The corrected candidate fixes the prior return/release mismatch and adds the
runtime frozen-fixture guard. Cold replay and the 210/630/840 accounting are
preserved.

## Candidate and prior review

- Candidate: `d3d6e48791623478fd1d838c7e95a72b77b5cd74`
- Previous independent review: `bff80e2a7`
- Exact disposable snapshot: `git archive d3d6e4879 WORKER_RETURNS/PDEV01-GAP007`
  from sibling `pyat-pdev01-gap007`
- Candidate read-only; only `final-recheck/**` written.
- TEST_ONLY/sourcefree; no original data, source rights, production, merge, CI
  or adoption.

## Verified

### Release reference reconciliation

- `00_RETURN.md` and the actual trace now use:
  `64cf774b408686394c8caf9969f442b518e365d04c924bafefb6204239c9bf03`
- The stale prior reference `383716e4…` is absent from the current repair
  report/receipt files.
- `actual_trace.json`, `01_ACTUAL_RECEIPT.json`, `cold_replay_1.json` and
  `cold_replay_2.json` are byte-identical:
  `bba0de8231ea50b46c1f5d5f73c434d64af2d9bcd9c5ef610876e7955b1256ab`

### Frozen fixture and tamper refusal

- Frozen `source.sav` SHA:
  `5009f3c9272dcbfb15a48b17cfff51f9afa67e60d6a2c1364c9aa07bc6732e4f`
- Two fresh processes produce exact identical JSON.
- Source SHA stable: `5009f3c9…`
- Release ref stable: `64cf774b…`
- All 210 query refs stable.
- BatchManifest ref stable: `6fd0f47c…`
- I05 compilation ref stable: `78568e5e…`
- A one-byte-changed frozen SAV passed with `--source` is refused:
  - exit `2`
  - empty stdout
  - stderr contains `FROZEN_SOURCE_SHA256_MISMATCH`, expected SHA and changed SHA

### Preserved operation accounting

- 210 DIST units executed; 210 Batch receipts `COMPLETED`; 210 `SUPPORTED`
  facts.
- 630 typed refusals: CONDITIONAL 210, JOINT 210, HETEROGENEITY 105,
  RECURSIVE_BRANCH 105.
- 840 total operations; 840 distinct original operation refs; no dropped or
  invented operations.
- I05 remains a separate sourcefree capability call: 16 receipts, 30 facts,
  16 candidates; no I05 operation in the P1 840 accounting.
- One synthetic C11 carrier is reused across all 35 roster/wave entries and all
  210 bound units (TEST_ONLY scope).

## Candidate tests

**9 passed** in 49.60s, including two fresh-process identity comparisons and the
runtime changed-fixture refusal.

## Exact commands

```sh
git -C /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-pdev01-gap007 \
  archive d3d6e4879 WORKER_RETURNS/PDEV01-GAP007 | tar -x -C <snapshot>

PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 PYTHONPATH=<snapshot>:<sibling> \
  python3 <snapshot>/WORKER_RETURNS/PDEV01-GAP007/repair/replay_repair.py > run1.json
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 PYTHONPATH=<snapshot>:<sibling> \
  python3 <snapshot>/WORKER_RETURNS/PDEV01-GAP007/repair/replay_repair.py > run2.json

python3 <snapshot>/WORKER_RETURNS/PDEV01-GAP007/repair/replay_repair.py \
  --source <temporary-one-byte-changed-copy>

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=<sibling> \
  python3 -m pytest <sibling>/WORKER_RETURNS/PDEV01-GAP007/repair/test_repair.py \
  -q -o addopts=''
```

## Limits

- Scoped to the exact synthetic, sourcefree candidate and TEST_ONLY fixture.
- No scientific, source-rights, population, production, merge, CI or wake claim.
