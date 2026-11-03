# Exact commands

Run root:
`/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-pdev01-gap007`

```sh
R=/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-pdev01-gap007
OUT="$R/WORKER_RETURNS/PYAT-REAL-METADATA-BINDING/decline-code-fix"
TMP=$(mktemp -d "${TMPDIR:-/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T}/pyat-decline.XXXXXX")

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

PYTHONPATH="$TMP" PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
  python3 -B "$OUT/decline_code_fix.py" \
  --package-root "$TMP" \
  --source-config "$TMP/rawlsing_next/source_configuration/data/SRC04/source.config.json" \
  --option-authority "/Users/matthewsmith/Desktop/Rawlsing/data/ddm_build_copy/reports/arab_barometer_response_option_authority.csv" \
  --tally-product "$TMP/prior/TALLY_PRODUCT.json" \
  --routing-receipt "$R/WORKER_RETURNS/PYAT-REAL-METADATA-BINDING/routing/01_ROUTING_RECEIPT.json" \
  --output "$OUT/01_CORRECTION_RECEIPT.json" \
  --overlay "$OUT/02_Q101_CODE99_OVERLAY.json"

PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
  python3 -B -m pytest "$OUT/test_decline_fix.py" \
  -q -o addopts='' -p no:cacheprovider \
  --junitxml="$OUT/logs/test_decline_fix_junit.xml"
```

Observed: **5 passed**.

The commands read only metadata and retained aggregate counts. The SRC04 SAV
path is not opened.
