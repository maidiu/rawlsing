# PDEV-01 N10W same-lineage independent review — 883da8fff2

**Subject:** `883da8fff2bb10fe2181d0c0a7ddc84d34bb5a8c`  
**Review base:** `02b98ec3dd88e5e742ce459e54d233f547768145`  
**Scope:** TEST_ONLY sourcefree actual J42 W41/E41/P41; synthetic E04; D2P3 GSS/NCA field-reader boundary.  
**Write root:** `WORKER_RETURNS/PDEV01-N10W-JOIN-INDEPENDENT-SAME-LINEAGE/`

## Verdict

**Engineering: `PASS_SCOPED_SAME_LINEAGE_J42_W41_E41_P41`**  
**D2P3-as-N9: `HOLD__EXACT_MISSING_W41_E41_PRODUCER_BINDING`**  
**Science: `HOLD`**  
**Authority: `HOLD`**

No bypass or false lineage was found in the actual J42 same-lineage path. The
actual calls and identity controls replay. D2P3 is not relabeled, not fed to
N10W, and has no existing lawful W41/E41 binding.

## Actual J42 lineage

Using the independently built actual J42 receipts reused from review
`e79be4a3d`:

- Receipts SHA-256: `c54b215bb03bba391571b4c51357831b14f256b7c4c6eec98d85dd9bda30eebf`
- 84 / 84 views positive
- Cold receipts byte-equal; all 84 cold view hashes equal
- Positive view: `062c4c5fc59c5618582d43f9e4c917ab97a32ecfd7249d5bfba2824fe0767287`
- N9: `W41_READONLY_SOURCE_QUALIFIED_WORLD@1`
- N10E: `E41_N10E_EMPIRICAL_POSSIBILITY_SLICE_PROVIDER_EXT@1.1.0`
- N10W: `P41_GENERIC_POSSIBILITY_SERVICE@1`
- N9 clock: `TEST_CURRENT`, valid/published/test-now `2027-09-01`
- N9 currentness: `CURRENT_TEST_ONLY_SELECTION`
- Source rows: `4320b3a505478c274fc756ce0e025e36685e0742e940072aae80ce11286e4c02`

## Mismatch, provider refusal and restoration

| Control | Result |
|---|---|
| R05 source rows `a585bd13…` against J42 | `REFUSED / JOINED_SOURCE_ROWS_MISMATCH` |
| R05 provider substitution | `REFUSED / JOINED_PROVIDER_IDENTITY_MISMATCH` |
| restore J42 | `SELECTED_VIEW_FROM_ACTUAL_JOINED_CONSUMER`, same positive view hash |

No incompatible lineage was relabeled.

## First missing D2P3-to-N9 binding

D2P3 trace `cfe7dc6111afcb8eda26eb9a54f6cad43b6d1584` /
`WORKER_RETURNS/PYAT-USERDIRECT-20261014-R6-D2P3-PRODUCER-READER-LINEAGE-R1/new/producer_reader_trace.json`
SHA-256 `dfee8bcc7f1f0202e2b9ffee7d3cbe70e1c361d45b4727356393ae14c6c457f3`:

- Reader state: `TWO_VALUES_READ_TEST_ONLY`
- Producer refs: `D2P_TESTONLY_FIELD:2b00177b…`, `D2P_TESTONLY_FIELD:de36df43…`
- Source families: `GH_GSS_PHC_2021`, `GH_NCA_LICENSEE_REPORTS_2021Q4`
- No W41 N9 provider, no E41 N10E receipt, no J42 source rows
- D2P3 refs do not appear in the J42 receipt
- D2P3 is not fed to or mistaken for N10W

**Exact missing binding:** a W41 version-selected N9 world plus an E41 N10E
receipt plus exact J42 source-row/currentness binding for the D2P3 GSS/NCA
field refs. **No existing lawful construction path is present.** Building that
W41-style artifact is outside this review’s authority; the smallest path is a
new competent owner-issued artifact, not a relabel or adapter.

## Exact command

```sh
cd /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-pdev01-n10w-join-review
PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 python3 \
  WORKER_RETURNS/PDEV01-N10W-JOIN-INDEPENDENT-SAME-LINEAGE/run_same_lineage_review.py
```

Evidence: `evidence/same_lineage_review.json`, `evidence/ENVIRONMENT_PASSPORT.json`,
`logs/review.stdout.log`, `SOURCE_PINS.json`.

## Science and authority

Science `HOLD`: original empirical execution is ungranted. No test output is
passed as original; a separate original science owner acceptance would be
required. Authority `HOLD`: no source reads, native issuance, adoption, merge
or production edit. The environment passport is sanitized; quota is `UNKNOWN`.
