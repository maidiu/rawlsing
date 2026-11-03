# PDEV01 — same-lineage N10W qualification

**Status:** `CANDIDATE__TEST_ONLY__INDEPENDENT_REVIEW_REQUIRED`  
**Engineering:** `PASS_SCOPED_SAME_LINEAGE_J42_W41_E41_P41`  
**D2P3-as-N9:** `HOLD__NO_W41_E41_BINDING` — D2P3 is not relabeled  
**Source science:** `HOLD`  
**Authority:** `HOLD`

Resume base: `c75b464ab4dbba15c6a89db42aaf5d101ba13d55`  
Branch: `agent/pyat-pdev01-n10w-join-r1`  
Owned root: `WORKER_RETURNS/PDEV01-N10W-JOIN/same-lineage/`

## Actual same-lineage positive

The actual existing J42 lineage is used unchanged:

- N9: `W41_READONLY_SOURCE_QUALIFIED_WORLD@1`
- N10E: `E41_N10E_EMPIRICAL_POSSIBILITY_SLICE_PROVIDER_EXT@1.1.0`
- N10W receiver: `P41_GENERIC_POSSIBILITY_SERVICE@1`
- Source rows: `4320b3a505478c274fc756ce0e025e36685e0742e940072aae80ce11286e4c02`
- N9 clock: `TEST_CURRENT`, valid/published/test-now `2027-09-01`
- N9 currentness: `CURRENT_TEST_ONLY_SELECTION`
- Joined contract: `J42_JOINED_E41_W41_P41_PREV3_CONSUMER@1`
- Positive state: `SELECTED_VIEW_FROM_ACTUAL_JOINED_CONSUMER`
- Positive view hash: `062c4c5fc59c5618582d43f9e4c917ab97a32ecfd7249d5bfba2824fe0767287`
- 84/84 actual views positive; 84/84 cold view hashes equal
- Cold receipts byte-equal: `c54b215bb03bba391571b4c51357831b14f256b7c4c6eec98d85dd9bda30eebf`

## D2P3 boundary

Accepted D2P3 candidate `cfe7dc6111afcb8eda26eb9a54f6cad43b6d1584` / review `830a9656cb65f00337d5bcd0f7373dbef11d50df` is reused only as its accepted sourcefree field-reader evidence:

- Reader state: `TWO_VALUES_READ_TEST_ONLY`
- Producer refs:
  - `D2P_TESTONLY_FIELD:2b00177b2685b4a2171bfc27ec77a17f7e59b603bf4bd1e0fc10dc8575908f40`
  - `D2P_TESTONLY_FIELD:de36df435bd086fe265af2c3207e0ce4b4e14b66a2c8a148829bf027567c0587`
- Source families: `GH_GSS_PHC_2021`, `GH_NCA_LICENSEE_REPORTS_2021Q4`

D2P3 has no W41 N9 provider, no E41 N10E receipt, and no J42 source-row binding. The first missing binding is therefore explicit: D2P3 field refs are not W41/E41 and are **not fed** to the N10W receiver. It is not relabeled.

## Mismatch, refusal, restore

- R05 source rows `a585bd130c1a935cdef7723095483ccf228da633f58b9110c8ca21a189595b54` against the J42 W41/E41 lineage → `JOINED_SOURCE_ROWS_MISMATCH`
- R05 provider substitution → `JOINED_PROVIDER_IDENTITY_MISMATCH`
- Restored J42 lineage → positive view hash `062c4c5fc59c5618582d43f9e4c917ab97a32ecfd7249d5bfba2824fe0767287`

No incompatible R05/W41 identity was relabeled.

## Exact command

```sh
cd /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-pdev01-n10w-join
PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH="WORKER_RETURNS/PDEV01-N10W-JOIN/repair:$PWD" \
python3 WORKER_RETURNS/PDEV01-N10W-JOIN/same-lineage/run_same_lineage.py
```

## Evidence and pins

- `SAME_LINEAGE_WITNESS.json`
- `RUN.stdout` / `RUN.stderr`
- J42 commit: `f53cb0d2bce52640268c844c398bbd8007d28edc`
- J42 guard source: `WORKER_RETURNS/PDEV01-N10W-JOIN/repair/guarded_receiver.py`
- J42 receipts: `c54b215bb03bba391571b4c51357831b14f256b7c4c6eec98d85dd9bda30eebf`
- W41 artifact SHA-256: `09a92d6c00e867a44712b225cadd352b7d41a2038384de26de34f5c10a9185e7`
- D2P3 trace SHA-256: `dfee8bcc7f1f0202e2b9ffee7d3cbe70e1c361d45b4727356393ae14c6c457f3`

## Limits

TEST_ONLY sourcefree W41/E41/P41 and synthetic E04 values only. D2P3 is a GSS/NCA field reader, not N9. No original data, source access, production edits, adoption, merge, CI, N11/N12, actor/Sorok, or authority expansion.

**Next:** distinct nonauthor review of the same-lineage positive, D2P3 boundary, mismatch refusal, and restore. The author does not self-accept.
