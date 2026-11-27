# FIELD FORGE EXTERNAL ESTATE RETURN — R1
**Commission:** FF-EXT-SURVEY-R1 · **Prepared SHA:** `92bf8876ef47abee0c05776f0afb2540914c0e10` · **Branch:** `agent/field-forge-external-source-integration-20261124-r1` · **Survey date:** 2026-11-24.
**Status:** local actual-file reconnaissance complete. No acquisition, normalization, harmonization, conversion, merge, production adapter, architectural decision, or source mutation. No raw respondent or firm rows exported.

## Scope and result
The actual `source_files` estate was inventoried and the fourteen selected families ES01–ES14 were inspected at native file/table/object grain. The estate contains **556 physical files / 4,275,874,328 bytes** plus **1,470 archive members** in the inventory; selected-family findings are in `TABLES.tsv`, `VARIABLES.tsv`, `VALUE_CODES.tsv`, `COVERAGE.tsv`, `COVERAGE_SUMMARY.tsv`, `DIMENSION_MAP.tsv`, and `ROSTER_COVERAGE_MATRIX.tsv`. Reserve material is in `FILE_MANIFEST.tsv` with `RESERVE_NOT_PROFILED`; original35/MICS are not exported.

The existing `COUNTRY_ROSTER_35_WAVES` contains **147 ISO-3 countries** from 41 local survey files. The original roster and its declared rules were reused, not re-invented. The source map's Asian W6 and AB9 status remains partially ambiguous; W6 is represented by nine separate country files and AB9 is present only as reserve source custody, not a selected external family.

## ES01 — EPR Core
- **Actual release/files:** `EPR_DATASET_FAMILY/{2021,2023_beta}/core/EPR-2021.csv` / `EPR-2023.csv`; 4,339 and 4,537 rows; 11 columns.
- **Measures/grain:** politically relevant group-period, inclusive `from`/`to` years. `size` = group share of country population; `status` = executive access category; `umbrella`; `reg_aut`; group/state ids. Not an all-ethnicity census and not individual belief/power.
- **Coverage:** 181 state names each; **140/147** roster matches; 1946–2021 / 1946–2023; 12,797/13,390 selected-dimension valid group-period counts.
- **Evidence:** Core codebook, CSV header, actual rows; 2021 and 2023 beta kept separate.
- **Blockers:** 2023 beta codebook and TEK Atlas are 404; do not infer 2023 coding changes from 2021 codebook. 2021 vs 2023 beta must be compared explicitly before choice.

## ES02 — GeoEPR
- **Actual release/files:** `GeoEPR-2021.geojson` (1,685 features), `GeoEPR-2023.geojson` (1,684), plus CSV/TXT/SQL/shapefile archives.
- **Measures/grain:** group settlement-period feature; `type`, `sqkm`, geometry. GeoJSON uses longitude/latitude WGS84 but has no explicit CRS member; shapefile `.prj` present in archive.
- **Coverage:** 152 state names each; **123/147** roster matches; 1946–2021 / 1946–2023. Geometry types counted (MultiPolygon and null geometry); no overlay or density was computed.
- **Evidence:** GeoJSON feature properties and geometry types; shapefile member list.
- **Blockers:** no geometry engine available, so polygon validity/overlap is **UNCHECKED**. Geometry is not population, local dominance, or density.

## ES03 — EPR-ED
- **Actual release/files:** `ED-2021.csv` and `ED-2023.csv`; 871 rows x 20 columns each. The two CSV files are byte-identical (SHA-256 `850b5aff…f65bed4`).
- **Measures/grain:** country-group categorical religion/language/phenotype composition and recorded shares; no year field.
- **Coverage:** 157 gwids; **128/147** roster matches; 9 selected share variables; 7,835 valid, 4 missing. Zero shares are preserved as valid zeros.
- **Evidence:** ED CSV header and codebook.
- **Blockers:** ED group identity is not an individual identity and not interchangeable with EPR/TEK links; 2023 beta did not change ED content.

## ES04 — EPR-TEK
- **Actual release/files:** `TEK-2021.csv` (643 rows) and `TEK-2023.csv` (642), 5 columns.
- **Measures/grain:** TEK-group to country-group nominal kin link; `tekid`, `gwid`, `gwgroupid`, `groupname`; no year field in table.
- **Coverage:** 160 state names each; **129/147** roster matches; 1,929/1,926 selected-field valid values (three fields split in COVERAGE).
- **Evidence:** TEK CSV and 2021 Atlas.
- **Blockers:** 2023 TEK codebook/Atlas 404. Kin link is not migration, money flow, alliance, contact, solidarity, or causal pressure.

## ES05 — RAS3
- **Actual release/files:** `RELIGION_AND_STATE/data/RAS3_COMPLETE_ARDA.sav`; 183 rows x 5,569 columns (wide country array; year encoded in variable names).
- **Measures/grain:** country-level expert-coded state religion policy: official religion (`SAX`), official support (`SBX`), restrictions on religious parties/public observance (`NX01X`, `MX01X`), religious marriage/divorce (`LX01X`), funding (`VFUNDINGX`), office oaths (`VOFFICE01X`), 1990–2014.
- **Coverage:** 35 selected variables; **142/147** roster matches; 6,146 valid / 259 missing at country-variable grain.
- **Evidence:** SAV variable labels, value labels, codebook, online codebook snapshot.
- **Blockers:** no explicit license text located. Expert codes are not law text, enforcement, or private belief; coverage endpoint and coding revisions must remain explicit.

## ES06 — RASM3
- **Actual release/files:** `RASM3_COMPLETE_ARDA.sav`; 771 minority rows x 2,154 columns.
- **Measures/grain:** country-minority discrimination/action codes, 1990–2014. Selected: `MMX01X` (public observance), `MMX02X` (private observance), `WZSOCDIS01X` (societal economic discrimination), `WZMIN2MAJ01X` (minority action), `WZGENERALX` (general societal relations).
- **Coverage:** 20 selected variables; **142/147** roster matches; 14,798 valid / 622 missing at country-variable grain.
- **Evidence:** SAV labels/codebook.
- **Blockers:** minority coverage is not a universal religious census; no name-only crosswalk or imputation to omitted groups; no explicit license.

## ES07 — RAS Constitutions v1.02
- **Actual release/files:** `RAS_Constitutions_2022_v1.02.sav`; 176 rows x 5,383 columns; 1990–2022 encoded in variable names.
- **Measures/grain:** constitutional clause presence: `coff` status, `coffestab` establishment, `csras01x` SRAS interference, `creldis01x` discrimination ban, `cfree01x` protection of religious freedom, `claws01x` religious law subordination.
- **Coverage:** 18 selected variables; **140/147** roster matches; 2,628 valid / 540 missing.
- **Evidence:** SAV labels/codebook.
- **Blockers:** provision alone is not operative sanction or practical access; enactment/effective dates are not separate fields in this array; no explicit license.

## ES08 — Women, Business and the Law
- **Actual release/files:** WBL 1.0 historical `WBL1-0-1971-2024.dta` (10,260 x 56); WBL 2026 3-pillar `WBL26-3Pillar-Scores-Published.dta` (190 x 266); separate 2026 LF/SF/EP DTAs; 2024 legal/supportive/EO DTAs; 2024/2026 Excel releases; NFIS, disability, historical/current reforms; reproducibility packages.
- **Measures/grain:** economy-year or economy cross-section; legal question responses, topic scores, pillar indices; separate legal, supportive, enforcement-perception products. WBL 1.0 internal years 1970–2023 (report years 1971–2024); WBL 2026 ReportYear 2026; WBL 2024 is 2.0.
- **Coverage:** **143/147** roster matches; WBL 1.0 190 economies x 54 years; WBL 2026 legal/supportive 190, EP 178; WBL 2024 legal/supportive 190, EO 164. All ten topics retained.
- **Evidence:** DTA/Excel headers, variable labels, sheets, WBL 2024 report, 2026 handbook, 2025 topic handbooks.
- **Blockers:** composite index is not a provision; legal scope/exceptions and actual enforcement are separate. No separate 2024-dated English 2.0 methodology handbook found; 2025 handbooks and 2024 full report are the official release-adjacent documentation. Expert respondent records are reserve and were not profiled.

## ES09 — ILOSTAT
- **Actual release/files:** 93 selected annual RDS files under `ILOSTAT/indicator/`; catalogs and dictionaries under `ILOSTAT/catalog` and `ILOSTAT/dictionaries`; bulk guidelines.
- **Measures/grain:** long reference-area x time x indicator x sex tables. Selected subjects: labour force, employment, status/occupation/activity, informal, unemployment/underutilisation, NEET, earnings, hours, working poverty, social protection, industrial relations, child labour, parental leave proxy.
- **Coverage:** **147/147** roster matches at reference-area grain; 323 distinct reference areas including aggregates; 1946–2027; 24,301,559 selected-dimension valid observations and 1,843,914 missing. `obs_status` exists in 83/93 files; `classif1` in 76; `classif2` in 17; notes in subsets.
- **Evidence:** all 93 RDS loaded; TOC/dictionaries; per-file schema and coverage.
- **Blockers:** no dedicated maternity-protection indicator; `EES_XPLV_SEX_RT_A` (parental leave) is proxy only. Observed, 19th-ICLS and modelled series are separate indicator IDs. RDS schema is not uniform. Do not infer individual control, employment relation, or household jointness.

## ES10 — JOIN
- **Actual release/files:** `GLOBAL_JOBS_INDICATORS_JOIN/data/join_database_w_definitions.xlsx`; 14,628 rows x 103 columns (Sheet1), definitions in Sheet2.
- **Measures/grain:** country-survey-subsample row; national survey estimates by sex/age/education/urban-rural and other subsamples; survey lineage and quality flags retained.
- **Coverage:** 168 ISO-3 countries; **132/147** roster matches; 1970–2021; 1,790 distinct survey source filenames; 18 selected indicators; 226,667 valid / 36,637 missing.
- **Evidence:** actual workbook structure, header, Sheet2 definitions, source/quality columns.
- **Blockers:** same indicator name is not equal meaning across surveys; no automatic averaging or duplicate evidence; missing years are not zeros. JOIN and ILOSTAT are separate survey-derived estimands.

## ES11 — WID
- **Actual release/files:** `WORLD_INEQUALITY_DATABASE/archive/wid_all_data.zip`; 819,884,358 bytes; SHA-256 `c107eb45…c7691e`; 696 members = 347 data + 347 metadata + `WID_countries.csv` + README; `unzip -t` clean; uncompressed 6,410,482,419 bytes. No permanent extraction.
- **Measures/grain:** country/region-year by variable, percentile, age, population unit; selected pre-tax national income top 10%/top 1%, net personal wealth top 10%/top 1%, average income/wealth, labor/capital top shares, top-1% threshold.
- **Coverage:** 263 source codes with selected data; **147/147** roster matches; 1800–2025; 97,982 valid selected observations. Metadata carries source, method, unit and average quality per series.
- **Evidence:** archive data and metadata streamed directly from ZIP; WID README, codes dictionary, DINA 2025.
- **Blockers:** license ambiguous in public pages; treat as non-commercial/attribution pending confirmation. Do not equate top percentile with ruling class, or mix units/PPP/age/definitions. Historical and subnational/regional codes are not current sovereign states.

## ES12 — Global Findex
- **Actual release/files:** `Global Findex/GlobalFindexDatabase2025.dta`; 8,577 rows x 438 columns; plus 2011/2014/2017/2021/2025 methodology, questionnaire, glossary and report documents.
- **Measures/grain:** country-wave-published-subgroup row; percentages and levels. `group`/`group2` axes include all, gender, age, education, labour force, income, urbanicity; 2011, 2014, 2017, 2021, 2022 (2021 round), 2024.
- **Coverage:** 174 country codes; **142/147** roster matches; 14 selected indicators; 68,736 valid / 51,342 missing published-margin cells.
- **Evidence:** DTA rows/group axes, glossary, questionnaires, methodology.
- **Blockers:** published subgroup margins only; no pseudo-joint reconstruction or individual assignment. Microdata not acquired. Five-wave aggregate is present; 2022 is part of the 2021 round.

## ES13 — Enterprise Surveys
- **Actual release/files:** selected aggregate indicator databases inside `Enterprise/` outer ZIPs: global methodology (292,314 x 293 DTA), not-global methodology (40,110 x 297), informal sector (64,211 x 99), plus indicator-description PDFs. Raw/Political Connections/Productivity/Standardized/WBES 2002–2005 archives are reserve.
- **Measures/grain:** establishment-level indicator rows; firm size, ownership, exporter, sector, employment composition, finance, infrastructure, regulatory constraints, performance. Global, historical non-global and informal-city universes are distinct.
- **Coverage:** global 181 source geos, **141/147** roster, 2006–2026; non-global 19 geos, **15/147**, 2002–2019; informal 21 geos, **16/147**, city-level. Selected-dimension counts only; no raw firm rows exported.
- **Evidence:** DTA metadata and country-year/city counts; inner member lists.
- **Blockers:** firm is not worker; city-only informal sample does not support national inference. Enterprise license terms were not separately captured. Raw firm microdata remained unprofiled.

## ES14 — V-Dem v16
- **Actual release/files:** `V_DEM/data/vdem.RData` object `vdem` (28,092 x 4,618); `codebook.RData` object `codebook` (781 x 14); v16 codebook and methodology PDFs; exact tag V16 commit `f4dd26922e658442524dfd954bf14f7ebe622d5d`.
- **Measures/grain:** country-year expert-coded latent/ordinal indicators. Selected: CSO repression/entry/consultation/participation, civil-society indices, freedom of association and assembly, freedom of expression/alternative information, media self-censorship, freedom of religion, religious-organization repression, labor rights, torture, political killings, trade-union engagement.
- **Coverage:** 202 country_text_id units; **144/147** roster matches; 1789–2025; 17 selected indicators; 408,630 valid / 68,934 missing. Uncertainty fields (`_codelow`, `_codehigh`, `_sd`) retained in VARIABLES.
- **Evidence:** actual RData and codebook objects; v16 release statement; methodology Part III.
- **Blockers:** expert-coded estimates are not legal text, observed enforcement, or individual experience. No generic democracy score as ground truth; no automatic repression rule; v16 absolute scores are not comparable to other versions.

## Reserve / not deeply profiled
`FILE_MANIFEST.tsv` records reserve custody: original35 respondent files and archive members; EPR ACD2EPR/ER/AG; RAS RMAR and SOR; WBL expert respondent products; Enterprise raw/other databases; MICS archive. These were inventoried for presence/format/schema only. The original35 and MICS files were not exported and no respondent rows were published.

## Cross-cutting findings
- The actual estate is richer than the source-map user-reported hints: Enterprise selected aggregates, WID complete archive, all 93 ILOSTAT files, Findex aggregate, V-Dem full+others, and the full RAS/WBL/JOIN sets are present.
- Main friction points are **rights/licensing ambiguity (RAS, WID, Enterprise)**, **missing 2023 EPR documentation**, **non-uniform ILOSTAT schemas**, **composite-vs-provision WBL semantics**, **historical/non-sovereign geographies (EPR, WID, V-Dem, ILOSTAT)**, and **firm/worker and subgroup/joint inference boundaries**.
- Source overlap is substantial by country label but not by estimand: JOIN/ILOSTAT both describe labour, yet survey instruments and definitions differ; EPR/ED/TEK/RAS/V-Dem all encode group/institutional conditions but at different units and evidence types. No source was equated to another.
