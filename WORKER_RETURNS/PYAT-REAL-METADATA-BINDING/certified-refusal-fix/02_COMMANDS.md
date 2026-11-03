# Exact commands

Run root:
`/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-pdev01-gap007`

```sh
R=/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-pdev01-gap007
OUT="$R/WORKER_RETURNS/PYAT-REAL-METADATA-BINDING/certified-refusal-fix"
TMP=$(mktemp -d "${TMPDIR:-/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T}/pyat-certified.XXXXXX")

git -C "$R" archive 6949efbc3bb17d1ee2b00c9c0935f921a6a93fd8 rawlsing_next \
  | tar -x -C "$TMP"
git -C "$R" archive agent/pyat-pre553-r157-integration \
  rawlsing_next/source_configuration \
  rawlsing_next/pre553_source_read_admission.py \
  source_pre553_validation/SRC04 \
  | tar -x -C "$TMP"

mkdir -p "$TMP/prior"
git -C "$R" show 5f6e03493:campaign_d1_src04_tally/evidence/TALLY_PRODUCT.json \
  > "$TMP/prior/TALLY_PRODUCT.json"

REVIEW=/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-pdev01-gap007-review
git -C "$REVIEW" show ad205744c:WORKER_RETURNS/PYAT-REAL-METADATA-INDEPENDENT-REVIEW/decline-code-recheck/evidence/CORRECTION_ALLOWLIST.csv \
  > "$TMP/prior/CORRECTION_ALLOWLIST.csv"
git -C "$REVIEW" show ad205744c:WORKER_RETURNS/PYAT-REAL-METADATA-INDEPENDENT-REVIEW/decline-code-recheck/evidence/TYPED_UNKNOWN.csv \
  > "$TMP/prior/TYPED_UNKNOWN.csv"

PYTHONPATH="$TMP" PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
  python3 -B "$OUT/certified_refusal_fix.py" \
  --package-root "$TMP" \
  --source-config "$TMP/rawlsing_next/source_configuration/data/SRC04/source.config.json" \
  --allowlist "$TMP/prior/CORRECTION_ALLOWLIST.csv" \
  --typed-unknown "$TMP/prior/TYPED_UNKNOWN.csv" \
  --option-authority "/Users/matthewsmith/Desktop/Rawlsing/data/ddm_build_copy/reports/arab_barometer_response_option_authority.csv" \
  --tally-product "$TMP/prior/TALLY_PRODUCT.json" \
  --routing-receipt "$R/WORKER_RETURNS/PYAT-REAL-METADATA-BINDING/routing/01_ROUTING_RECEIPT.json" \
  --output "$OUT/01_CERTIFIED_RECEIPT.json" \
  --overlay "$OUT/02_CERTIFIED_OVERLAY.json"

PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
  python3 -B -m pytest "$OUT/test_certified_fix.py" \
  -q -o addopts='' -p no:cacheprovider \
  --junitxml="$OUT/logs/test_certified_fix_junit.xml"
```

Observed: **5 passed**.

Only metadata, the accepted aggregate tally and the exact per-item allowlist are
read. The SRC04 SAV path is not opened.
