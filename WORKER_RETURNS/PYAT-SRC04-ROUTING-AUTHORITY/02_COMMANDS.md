# Exact commands

Run root:
`/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-pdev01-gap007`

```sh
R=/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-pdev01-gap007
OUT="$R/WORKER_RETURNS/PYAT-SRC04-ROUTING-AUTHORITY"
TMP=$(mktemp -d "${TMPDIR:-/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T}/pyat-routing-authority.XXXXXX")

git -C "$R" archive 6949efbc3bb17d1ee2b00c9c0935f921a6a93fd8 rawlsing_next \
  | tar -x -C "$TMP"
git -C "$R" archive agent/pyat-pre553-r157-integration \
  rawlsing_next/source_configuration \
  rawlsing_next/pre553_source_read_admission.py \
  source_pre553_validation/SRC04 \
  | tar -x -C "$TMP"

PYTHONPATH="$TMP" PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
  python3 -B "$OUT/routing_authority.py" \
  --package-root "$TMP" \
  --source-config "$TMP/rawlsing_next/source_configuration/data/SRC04/source.config.json" \
  --certified-receipt "$R/WORKER_RETURNS/PYAT-REAL-METADATA-BINDING/certified-refusal-fix/01_CERTIFIED_RECEIPT.json" \
  --codebook "/Users/matthewsmith/Desktop/Rawlsing/data/FINAL CODEBOOKS/FINAL FINAL CODEBOOKS/Arab Barometer Wave 1 codebook.csv" \
  --exceptions "$TMP/source_pre553_validation/SRC04/EXCEPTIONS.json" \
  --output "$OUT/01_ROUTING_AUTHORITY_RECEIPT.json"

PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
  python3 -B -m pytest "$OUT/test_routing_authority.py" \
  -q -o addopts='' -p no:cacheprovider \
  --junitxml="$OUT/logs/test_routing_authority_junit.xml"
```

Observed: **5 passed**.

Only metadata, the accepted aggregate overlay receipt, codebook and source
exception ledger are read. The SRC04 SAV path is not opened.
