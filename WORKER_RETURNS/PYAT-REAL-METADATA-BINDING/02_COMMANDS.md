# Exact commands

Run root:
`/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-pdev01-gap007`

The R157 package is read from a disposable archive; only the worker return is
written.

```sh
R=/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-pdev01-gap007
OUT="$R/WORKER_RETURNS/PYAT-REAL-METADATA-BINDING"
TMP=$(mktemp -d "${TMPDIR:-/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T}/pyat-real-metadata.XXXXXX")

git -C "$R" archive 6949efbc3bb17d1ee2b00c9c0935f921a6a93fd8 rawlsing_next \
  | tar -x -C "$TMP"
git -C "$R" archive agent/pyat-pre553-r157-integration \
  rawlsing_next/source_configuration \
  rawlsing_next/pre553_source_read_admission.py \
  source_pre553_validation/SRC04 \
  | tar -x -C "$TMP"

PYTHONPATH="$TMP" PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
  python3 -B "$OUT/bind_real_metadata.py" \
  --package-root "$TMP" \
  --source-config "$TMP/rawlsing_next/source_configuration/data/SRC04/source.config.json" \
  --crosswalk "$TMP/rawlsing_next/source_configuration/data/SRC04/crosswalk.json" \
  --fixture-config "$TMP/source_pre553_validation/SRC04/fixture.config.json" \
  --fixture "$TMP/source_pre553_validation/SRC04/fixture.json" \
  --codebook "/Users/matthewsmith/Desktop/Rawlsing/data/FINAL CODEBOOKS/FINAL FINAL CODEBOOKS/Arab Barometer Wave 1 codebook.csv" \
  --directionality "/Users/matthewsmith/Desktop/Rawlsing/data/ddm_build_copy/directionality_authority/arab_barometer_I_directionality_authority.csv" \
  --option-authority "/Users/matthewsmith/Desktop/Rawlsing/data/ddm_build_copy/reports/arab_barometer_response_option_authority.csv" \
  --validation-results "$TMP/source_pre553_validation/SRC04/VALIDATION_RESULTS.json" \
  --metadata-origin "agent/pyat-pre553-r157-integration@056849e23" \
  --form-route-owner "ARAB lane / P3 integration owner named in the SRC04 exception ledger" \
  --r03-policy-owner "R03 GrammarPolicy/direction owner" \
  --output "$OUT/01_REDACTED_RECEIPT.json"

PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
  python3 -B -m pytest "$OUT/test_metadata_binding.py" \
  -q -o addopts='' -p no:cacheprovider \
  --junitxml="$OUT/test_metadata_binding_junit.xml"
```

Observed: **4 passed**.

No `Arab Barometer Wave 1.sav` path is opened. The only native release built by
the harness is the declared nonrespondent `fixture.json` through the existing C11
factory.
