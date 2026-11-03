# Exact commands

Run root:
`/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-pdev01-gap007`

```sh
R=/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-pdev01-gap007
OUT="$R/WORKER_RETURNS/PYAT-REAL-METADATA-BINDING/routing"
TMP=$(mktemp -d "${TMPDIR:-/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T}/pyat-routing.XXXXXX")

git -C "$R" archive 6949efbc3bb17d1ee2b00c9c0935f921a6a93fd8 rawlsing_next \
  | tar -x -C "$TMP"
git -C "$R" archive agent/pyat-pre553-r157-integration \
  rawlsing_next/source_configuration \
  rawlsing_next/pre553_source_read_admission.py \
  source_pre553_validation/SRC04 \
  | tar -x -C "$TMP"

mkdir -p "$TMP/prior"
git -C "$R" show 4b1d407d54e4e7f035a10cbe252d4ca04652f4d7:campaign_a_src04/evidence/SLICE_SELECTION.json > "$TMP/prior/SLICE_SELECTION.json"
git -C "$R" show 4b1d407d54e4e7f035a10cbe252d4ca04652f4d7:campaign_a_src04/evidence/RELEASE_RECEIPT.json > "$TMP/prior/RELEASE_RECEIPT.json"
git -C "$R" show 5f6e03493:campaign_d1_src04_tally/evidence/TALLY_PRODUCT.json > "$TMP/prior/TALLY_PRODUCT.json"
git -C "$R" show 5f6e03493:campaign_d1_src04_tally/review/FOCUSED_RECHECK.json > "$TMP/prior/FOCUSED_RECHECK.json"

PYTHONPATH="$TMP" PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
  python3 -B "$OUT/trace_routing.py" \
  --package-root "$TMP" \
  --source-config "$TMP/rawlsing_next/source_configuration/data/SRC04/source.config.json" \
  --slice-selection "$TMP/prior/SLICE_SELECTION.json" \
  --release-receipt "$TMP/prior/RELEASE_RECEIPT.json" \
  --tally-product "$TMP/prior/TALLY_PRODUCT.json" \
  --focused-recheck "$TMP/prior/FOCUSED_RECHECK.json" \
  --option-authority "/Users/matthewsmith/Desktop/Rawlsing/data/ddm_build_copy/reports/arab_barometer_response_option_authority.csv" \
  --output "$OUT/01_ROUTING_RECEIPT.json"

PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
  python3 -B -m pytest "$OUT/test_routing.py" \
  -q -o addopts='' -p no:cacheprovider \
  --junitxml="$OUT/logs/test_routing_junit.xml"
```

Observed: **5 passed**.

The commands read only metadata and accepted aggregate receipts. The SRC04 SAV
path is not opened.
