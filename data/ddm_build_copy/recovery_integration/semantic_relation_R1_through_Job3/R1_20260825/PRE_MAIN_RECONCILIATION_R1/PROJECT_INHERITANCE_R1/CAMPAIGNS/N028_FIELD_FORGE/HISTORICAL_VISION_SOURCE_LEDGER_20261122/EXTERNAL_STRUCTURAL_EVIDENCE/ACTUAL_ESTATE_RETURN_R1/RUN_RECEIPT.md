# RUN RECEIPT — FF-EXT-SURVEY-R1

## Inputs and exact source of the commission
- Prepared commit: `92bf8876ef47abee0c05776f0afb2540914c0e10`
- PR: `maidiu/rawlsing#1327`
- Branch: `agent/field-forge-external-source-integration-20261124-r1`
- Commission path inspected from the fetched prepared commit:
  `data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/PROJECT_INHERITANCE_R1/CAMPAIGNS/N028_FIELD_FORGE/HISTORICAL_VISION_SOURCE_LEDGER_20261122/EXTERNAL_STRUCTURAL_EVIDENCE/`
- Local actual estate: `/Users/matthewsmith/Desktop/Rawlsing/source_files`
- Local return bundle: `/Users/matthewsmith/Desktop/FIELD_FORGE_EXTERNAL_ESTATE_RETURN_R1`
- No network acquisition, dataset download, credential change, source mutation, or protected-branch write.

## Runtime and readers
- Python 3.11.3 on macOS 13.7.8, 16 GiB RAM.
- `pandas 3.0.6`, `pyreadstat 1.3.8`, `pyreadr 0.5.9`, `openpyxl 3.1.5`, `pycountry 26.2.16`, `country_converter 1.3.2`.
- No R binary. No PDF text extractor (`pypdf`, `pdftotext`, `pdfminer` unavailable). No geometry engine (`shapely`, `fiona`, `geopandas` unavailable).
- SAV/DTA read with pyreadstat; RDS/RData with pyreadr; XLSX with openpyxl; ZIP/CSV with stdlib `zipfile`, `csv`, `io`; GeoJSON with `json`.

## Commands actually run
```text
git fetch origin refs/heads/agent/field-forge-external-source-integration-20261124-r1
git fetch origin refs/pull/1327/head
python3 scripts/01_inventory.py          # all physical files + archive members
python3 scripts/02_epr.py                # ES01-ES04 + reserve schema
python3 scripts/03_wbl.py                # ES08
python3 scripts/04_join.py               # ES10
python3 scripts/05_findex.py             # ES12
python3 scripts/06_vdem.py               # ES14
python3 scripts/07_ilostat.py            # ES09
python3 scripts/08_wid.py                # ES11, direct ZIP streaming
python3 scripts/09_enterprise.py         # ES13 selected aggregates
python3 scripts/10_ras.py                # ES05-ES07 + reserve schema
python3 scripts/11_merge.py              # combined TSVs, summary, roster matrix
```
Additional read-only checks: `unzip -t` on `wid_all_data.zip` (clean); `zipfile.testzip()` in the inventory for each ZIP (no failures); `gzip -t` for all 93 ILOSTAT RDS files (no failures).

## Actual inventory
- Physical files under `source_files`, excluding `.DS_Store`: **556**.
- Physical bytes: **4,275,874,328**.
- `FILE_MANIFEST.tsv`: **2,026 rows** (556 physical + 1,470 archive members); **0** inventory failures.
- Status counts: 307 `INSPECTED`; 1,470 `INSPECTED_METADATA_ONLY`; 249 `RESERVE_NOT_PROFILED`.
- Selected-family source roles: 169 `selected_source`; 114 `documentation`; 24 `metadata`; 247 `reserve`; 2 archive rows.
- WID archive: 819,884,358 bytes; SHA-256 `c107eb456096d0dfc76c6e61977d545d7897d7f7fd3e8789af7db0de50c7691e`; 696 members; uncompressed 6,410,482,419 bytes; not extracted.
- Enterprise inner DTAs were written only to `/tmp` for metadata/count reads, not extracted into the source estate.

## Deliverable tables
| File | Rows | Bytes | SHA-256 prefix |
|---|---:|---:|---|
| `FILE_MANIFEST.tsv` | 2,026 | 456,725 | `586b3236db1bd88e` |
| `TABLES.tsv` | 146 | 68,648 | `6651e54a5f5b915e` |
| `VARIABLES.tsv` | 17,588 | 5,145,803 | `5b57d8be2ef1d7bd` |
| `VALUE_CODES.tsv` | 3,982 | 579,709 | `18170ef348cdb585` |
| `COVERAGE.tsv` | 111,669 | 22,292,861 | `cd9ae4ece87de58c` |
| `COVERAGE_SUMMARY.tsv` | 25 release-groups | 1,703 | `07eb61160cb51245` |
| `DIMENSION_MAP.tsv` | 29 | 21,069 | `d92c528e7fb248aa` |
| `ROSTER_COVERAGE_MATRIX.tsv` | 147 roster rows x 14 ES columns | 4,934 | `caf3cd0ea424c824` |

`TABLES.tsv` includes selected and reserve table/object rows. `VARIABLES.tsv` is a complete metadata census for the selected tables plus selected-dimension rows; RAS contributes the largest block (13,106 wide-array variables). `VALUE_CODES.tsv` contains code labels for named categorical/short domains; V-Dem has no native value labels and therefore no VALUE_CODES rows.

## Coverage summary reconciliation
`COVERAGE_SUMMARY.tsv` is generated from `COVERAGE.tsv`, one row per ES x source x release. Counts are source-native country/territory grain, not harmonized country-year coverage. A country counts as roster-matched only where the source-native code maps to an exact ISO-3 already in the local roster. Selected-dimension coverage is in `COVERAGE.tsv`; a `1` in `ROSTER_COVERAGE_MATRIX.tsv` means at least one selected-dimension observation for that ES and roster ISO-3.

## Failures, partials and exact blockers
- **PDF text extraction:** unavailable. PDFs were checked for presence and header; no claim of page-level codebook text extraction.
- **Geometry validity/overlays:** unavailable (no geometry engine). GeoEPR geometry types and null counts were measured; polygon validity and overlays are **UNCHECKED**.
- **R:** unavailable. RData/RDS were read with pyreadr, not R.
- **WID:** no permanent extraction. Data and metadata were streamed from the ZIP; per-country ZIP members were not separately downloaded or extracted.
- **ILOSTAT:** all 93 RDS files readable and gzip-valid. Schema varies by indicator: `obs_status` in 83/93, `classif1` in 76/93, `classif2` in 17/93, notes in subsets. No dedicated maternity-protection indicator.
- **EPR 2023:** six codebooks, TEK Atlas 2023 and GeoEPR-2023.xlsx return 404 in official custody; 2021 GeoEPR xlsx was never published. These are typed gaps, not inferred content.
- **RAS/WID licenses:** public-page license text absent/ambiguous as stated in `RIGHTS_AND_LIMITS.md`; no legal conclusion drawn.
- **Enterprise:** raw/other enterprise archives were not deeply profiled; selected aggregate indicator DBs were read for schema and counts only. No raw firm rows exported.
- **Original35/MICS:** reserve and not profiled/exported.

## Source mutation check
No script writes under `source_files`. All created files are under the return directory. No original file was deleted, renamed, converted, harmonized, merged, or permanently extracted.
