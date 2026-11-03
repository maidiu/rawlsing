# PDEV-01 N10W focused clock recheck — candidate c75b464ab4

**Candidate:** `c75b464ab4dbba15c6a89db42aaf5d101ba13d55`  
**Reused review evidence:** `e79be4a3d8cd2cbe57c4a25361acc5e4dd9a8e1c`  
**Scope:** TEST_ONLY sourcefree W41/E41/P41 and synthetic E04 only.  
**Write root:** `WORKER_RETURNS/PDEV01-N10W-INDEPENDENT-REVIEW/clock-recheck/`

## Verdict

**`PASS_SCOPED_CLOCK_RECHECK__TRUSTED_W41_CLOCK_SNAPSHOT_AND_VIEW_BOUND__84_POSITIVE_AND_COLD_PRESERVED`**

The c75b repair resolves the remaining caller-self-consistency gap at the
tested engineering scope:

- The W41 artifact is loaded by exact commit/path and verified by pinned
  SHA-256, not accepted from caller-provided fields.
- The exact W41 world is selected by the J42 view key.
- `n9_world.selection` and `j42_bindings.w41_clock` are both bound to that
  trusted world clock.
- `w41_snapshot_hash` and `w41_view_hash` are bound to the same trusted world.
- Changing both caller clocks to `2099-01-01` and rehashing P41 is **refused**
  with `JOINED_N9_SELECTION_MISMATCH`.
- Actual J42 remains **84/84 positive** with cold view hashes equal.

Science and authority remain **HOLD**: the evidence is TEST_ONLY sourcefree,
N9 currentness is `CURRENT_TEST_ONLY_SELECTION`, and no original source,
operative N9, N11/N12, production edit, merge or new trust authority is involved.

## Exact evidence

Actual J42 receipts reused from e79 (independent actual build; two byte-equal
receipts):

- SHA-256: `c54b215bb03bba391571b4c51357831b14f256b7c4c6eec98d85dd9bda30eebf`
- 84 views, all `SELECTED_VIEW_FROM_ACTUAL_JOINED_CONSUMER`
- cold 84 view hashes equal
- positive selected view: `062c4c5fc59c5618582d43f9e4c917ab97a32ecfd7249d5bfba2824fe0767287`
- N9/W41, N10E/E41, N10W/P41 families exact
- N10E 3 `EXACT_SUPPORTED`; N10W `EXACT_PROGRESSIVE_CHAIN` / 3 live consumptions

Trusted W41 artifact:

- `b0a68e4ff5d5e2ca62b080376fda6b5f5431a6c2:WORKER_RETURNS/PYAT-R41-W41-OBJECTIVE-WORLD-R1/current_historical_asof_world_consumer_receipts.json`
- SHA-256 `09a92d6c00e867a44712b225cadd352b7d41a2038384de26de34f5c10a9185e7`
- selected world `base/TEST_CURRENT/budget5`:
  - clock `TEST_CURRENT / 2027-09-01 / 2027-09-01 / 2027-09-01`
  - snapshot `239d6828e3470a34bef9127da69d39f188397fe05540211faef6a31de68f6ff9`
  - view `5fe218c6df01cf25cf6d32a26c3e9cadab01aaa977e50db6d56c66d811ca6386`

Boundary mutations with P41 rehash:

| Mutation | Result |
|---|---|
| both caller clocks `2099-01-01` | `REFUSED / JOINED_N9_SELECTION_MISMATCH` |
| selection only | `REFUSED / JOINED_N9_SELECTION_MISMATCH` |
| `j42_bindings.w41_clock` only | `REFUSED / JOINED_W41_CLOCK_BINDING_MISMATCH` |
| `w41_snapshot_hash` changed | `REFUSED / JOINED_W41_SNAPSHOT_MISMATCH` |
| `w41_view_hash` changed | `REFUSED / JOINED_W41_VIEW_MISMATCH` |
| stale P41 hash | `REFUSED / JOINED_RECEIPT_CONTENT_HASH_MISMATCH` |

The five prior provider/currentness mutation results and missing-parent/stale
controls are reused from e79 evidence; the c75b guard preserves those paths.

## Exact command

```sh
cd /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-pdev01-n10w-join-review
PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 python3 \
  WORKER_RETURNS/PDEV01-N10W-INDEPENDENT-REVIEW/clock-recheck/run_recheck.py
```

Evidence: `evidence/recheck_evidence.json`, `logs/recheck.stdout.log`,
`SOURCE_PINS.json`.

## Limits

No original data/source read, no production/source edit, no merge/CI, no new
trust authority, no N9/OC05 installation, no N11/N12 or scientific adoption.
Candidate remains readonly; only this clock-recheck root was written.
