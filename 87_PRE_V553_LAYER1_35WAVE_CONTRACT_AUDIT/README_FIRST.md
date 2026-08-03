# Rawlsing Layer-1 35-wave pre-V553 contract audit harness

## Purpose

This additive harness creates and executes **Layer 1** of the pre-V553 freeze audit:

- all 35 active waves;
- one representative country per wave;
- all respondents in that country;
- a deterministic, contract-covering set of 20–50 governed variables;
- the current fused route through V552J;
- nonrespondent-only artifact collection;
- privacy, field-inventory, and preliminary point-to-point preservation evidence.

It does not redesign V550J, V551J, V552, or V552J. It imports the current installed all-wave runner and uses its current compilers and semantic gates. The only execution change is replacing the historical fixed `20` question limit with the size of the generated governed filter.

## Governing inputs

The selector reads the cumulative handoff ZIP directly and requires:

1. `Rawlsing_J_Family_Active_35_Wave_Scope_*.csv`;
2. exactly nine source-local `Deep_Question_Node_Catalog_*.csv` files.

The currently preserved cumulative v35 handoff satisfies both requirements and covers exactly 18,276 active implementations over 35 waves.

Plan mode does not require a database or repository. Execute mode requires the exact current repository and live PostgreSQL environment.

## Plan-only use

```bash
python 87_PRE_V553_LAYER1_35WAVE_CONTRACT_AUDIT/code/run_layer1_35wave_contract_audit.py \
  --handoff-zip /path/to/Rawlsing_J_Family_Authority_Strategy_Handoff_v35_20260801.zip \
  --output-root /path/to/layer1_plan
```

Default selection is 20 minimum, 36 target, and 50 maximum variables per wave.

Plan outputs include:

- `AUDIT_SCOPE_MATRIX.csv`
- `AUDIT_VARIABLE_SELECTION.csv`
- `AUDIT_FAMILY_COVERAGE_MATRIX.csv`
- `AUDIT_MORPHOLOGY_COVERAGE_SUMMARY.json`
- one exact question filter per wave
- `LAYER1_RUN_PLAN.json`
- SHA-256 manifest

## Live execution

Run from the exact current Rawlsing repository:

```bash
python 87_PRE_V553_LAYER1_35WAVE_CONTRACT_AUDIT/code/run_layer1_35wave_contract_audit.py \
  --handoff-zip /path/to/Rawlsing_J_Family_Authority_Strategy_Handoff_v35_20260801.zip \
  --repo-root /path/to/current/Rawlsing/repository \
  --output-root /path/to/layer1_live_audit \
  --env-file /path/to/current/Rawlsing/repository/.env \
  --execute
```

For each live scope, the selector intersects the codebook/authority plan with the live structural and canonical registry rows. It also reads the current J-family registry and seeds a real multi-variable family when one is available.

The invoked route is:

```text
V550 one country extraction and shared substrate write
→ V550 base processing
→ V550J prepared_required + --forbid-database-access
→ V551
→ V551J
→ V552
→ V552J with applicable V552 structural artifacts
```

## Privacy boundary

The collector refuses to package:

- shared respondent-substrate Parquet or CSV;
- respondent membership/response tables;
- raw respondent output;
- Parquet files with obvious respondent/case identifier columns.

Text artifacts are credential-redacted before packaging. Every exclusion or unreadable Parquet schema is written to `PRIVACY_SCAN.csv`.

## Important limitations

- The preserved package contains the complete governed 35-wave catalog and response authority needed for selection. It does not necessarily contain every original raw questionnaire PDF or SAV codebook.
- Plan mode cannot prove live country availability or current J-family applicability. Execute mode performs the live registry intersection.
- `BASIC_POINT_TO_POINT_CONSERVATION_CHECKS.csv` is an initial machine check, not the final end-to-end conservation verdict. The full freeze audit must inspect all downstream consumers and value-level preservation.
- A scope that is legitimately blocked must remain blocked with an exact reason. The harness does not coerce all scopes to pass.

## Exit codes

- `0`: plan completed, or every executed scope passed and privacy scan is clean;
- `1`: execution completed with failed scopes or privacy findings;
- `2`: harness/configuration failure.
