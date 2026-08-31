# M6 Response-Map and QUC Blocker

## Scope

This note records the bounded Phase-D M6 canary state. It is diagnostic evidence, not a new authority source and not a production completion claim.

## What V550 is using

V550 requires response-option authority to translate raw respondent values into governed response semantics. The canonical parent surface is the installed global map:

`data/ddm_build/reports/V550_response_option_map.csv`

The observed local parent has 357,324 data rows, 357,325 total lines, 71 columns, and SHA-256:

`971abaeaa334ab7025f7619d88da196567ac0f5314ecf5f97e745f82601eaaab`

Temporary per-scope Parquet files were derived mechanically from that parent for the canary. They are execution caches, not replacement authority. A durable implementation must record the parent hash, scope, row count, partition hash, and compiler version, and must fail closed when the parent hash changes.

## Observed execution

Afrobarometer R1 Lesotho completed the V550 process successfully. It did not prove the full nine-family chain: its later V551 surface had zero governed atom rows and its V551J lane was not certified.

Arab Barometer I Yemen failed inside V550 before shared-substrate completion:

```text
shared respondent substrate QUC enrichment incomplete for country=YE:
unjoined_rows=1434 vars=['Q2571', 'Q2572']
```

The `LY` versus `YE` country-label issue is not the reported failure here. The run passed `--country YE`; the failure is an unmatched QUC-to-bridge enrichment for the two variables above.

## Interpretation

This is not evidence that the global response-option map is absent or that all manual authority is missing. It is a separate contract boundary: response semantics may be available while the question relation is not completely enriched into the bridge surface required by the shared respondent substrate.

The correct next investigation is row-level reconciliation for `Q2571` and `Q2572`: source/wave/country identifiers, QUC keys, bridge keys, and the governing structural/semantic authority rows. Do not suppress the error, fabricate bridge rows, or substitute a different response map.

## Explicit boundary

The M6 canary was incomplete and was stopped after preserving the exact failure. No V552 or V552J run was authorized or performed by this diagnostic. No respondent Parquet or database extract belongs in GitHub.
