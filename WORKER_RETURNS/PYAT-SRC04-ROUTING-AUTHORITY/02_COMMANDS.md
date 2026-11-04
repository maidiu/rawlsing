# Exact commands

Run root:
`/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-pdev01-gap007`

```sh
R=/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-pdev01-gap007
OUT="$R/WORKER_RETURNS/PYAT-SRC04-ROUTING-AUTHORITY"
TMP=$(cat /tmp/pyat-src04-tmp-path.txt)

# Edition comparison: the supplied files are byte-identical.
shasum -a 256 \
  "/Users/matthewsmith/Desktop/Rawlsing/data/original codebook pdfs/Arab Bar W1 Questionnaire_ENG.pdf" \
  "/Users/matthewsmith/Desktop/Rawlsing/data/Arabbarometer/ABI_Questionnaire_ENG.pdf"

# Original questionnaire item citations, route scan, 14 authority join,
# and actual validation through the normal source-configuration schema owner.
PYTHONPATH="$TMP" PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
  python3 -B "$OUT/questionnaire_authority.py" \
  --package-root "$TMP" \
  --source-config "$TMP/rawlsing_next/source_configuration/data/SRC04/source.config.json" \
  --certified-receipt "$R/WORKER_RETURNS/PYAT-REAL-METADATA-BINDING/certified-refusal-fix/01_CERTIFIED_RECEIPT.json" \
  --codebook "/Users/matthewsmith/Desktop/Rawlsing/data/FINAL CODEBOOKS/FINAL FINAL CODEBOOKS/Arab Barometer Wave 1 codebook.csv" \
  --option-authority "/Users/matthewsmith/Desktop/Rawlsing/data/ddm_build_copy/reports/arab_barometer_response_option_authority.csv" \
  --exceptions "$TMP/source_pre553_validation/SRC04/EXCEPTIONS.json" \
  --edition-a "/Users/matthewsmith/Desktop/Rawlsing/data/original codebook pdfs/Arab Bar W1 Questionnaire_ENG.pdf" \
  --edition-b "/Users/matthewsmith/Desktop/Rawlsing/data/Arabbarometer/ABI_Questionnaire_ENG.pdf" \
  --output-dir "$OUT"

# 7 focused checks.
PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
  python3 -B -m pytest "$OUT/test_questionnaire_authority.py" \
  -q -o addopts='' -p no:cacheprovider \
  --junitxml="$OUT/logs/test_questionnaire_authority_junit.xml"

# The prior 5-check routing trace remains reproducible as well.
PYTHONPATH="$TMP" PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
  python3 -B "$OUT/routing_authority.py" \
  --package-root "$TMP" \
  --source-config "$TMP/rawlsing_next/source_configuration/data/SRC04/source.config.json" \
  --certified-receipt "$R/WORKER_RETURNS/PYAT-REAL-METADATA-BINDING/certified-refusal-fix/01_CERTIFIED_RECEIPT.json" \
  --codebook "/Users/matthewsmith/Desktop/Rawlsing/data/FINAL CODEBOOKS/FINAL FINAL CODEBOOKS/Arab Barometer Wave 1 codebook.csv" \
  --exceptions "$TMP/source_pre553_validation/SRC04/EXCEPTIONS.json" \
  --output "$OUT/01_ROUTING_AUTHORITY_RECEIPT.json"
```

Observed: **7 passed** in 0.04s.

Only questionnaire PDFs, metadata, the accepted aggregate receipt, codebook and
source authority are read. The SRC04 SAV path is not opened.
