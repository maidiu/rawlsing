# CLOSED35-L2-LAT1995 — Latinobarómetro 1995 Brazil Sample / Release Provenance Documentary Authority Closure

Repository: `maidiu/rawlsing`

Base: `agent/vozhd-premain-fiabc-s35-fanin-r1@770d95c1a604ea1f47ac2971b923673c14c42984`

Branch: `agent/rabochii-closed35-l2-latinobarometro1995-authority-r1`

Canonical source (inherited, unchanged):

- filename: `Latinobarometro 1995.sav`
- SHA-256: `4b7fc6da17dfddafd6a835717e8dc06981208eb4120fa33bdd16e12ae95926f7`
- format: SAV
- inherited replay identity: `SOURCE_SHA256 + ROW_ORDINAL`

Research boundary: GitHub/browser/public documentary research only. No local raw SAV bytes were opened. No source processing or measured P2X was run.

## Holding

The documentary court closes an important fact but **does not recover the missing causal provenance** for the Brazil 120-row discrepancy.

The strongest producer evidence is internally contradictory:

1. Corporación Latinobarómetro's current 1995 study page calls the publication the **final release `v1995.1`** and offers the aggregated SPSS SAV package together with the 1995 report, codebook, and technical records.
2. The producer's own 1995 press report repeatedly prints **Brazil `N=1200`** in substantive tables.
3. The **same report's technical annex** prints **Brazil `Muestra (N Casos)=1080`**.
4. The report introduction says **9,077 interviews** were conducted in total.
5. No producer erratum, correction note, version note, exclusion rule, validation rule, or weighting note was recovered that explains why Brazil is 1200 in the report tables but 1080 in the technical sheet.

Therefore the 1200 count is **not an undocumented anomaly unique to the inherited raw carrier**. It is a producer-published 1995 analytical/base count. But the documentary record recovered here does not authorize any claim that:
- 120 rows were invalid, excluded, or later added;
- 1080 is a weighted/valid/completed subset;
- 1200 and 1080 belong to different release versions;
- the technical sheet is simply erroneous;
- the canonical raw release should be trimmed to 1080.

The lawful documentary holding is:

`CANONICAL RAW RELEASE AUTHENTIC__BRAZIL_120_ROW_PROVENANCE STILL UNKNOWN`

"Authentic" here is bounded: exact byte identity remains the already-accepted S35 canonical-root fact; public producer documentation independently establishes a final 1995 producer release and producer-recognized Brazil `N=1200`, but does not publish a checksum that independently re-hashes the inherited SAV.

A more exact contradiction label is:

`PRODUCER_DOCUMENTARY_CONTRADICTION_ESTABLISHED__BRAZIL_1200_TABLE_BASE_VS_1080_TECHNICAL_SAMPLE__CAUSAL_PROVENANCE_UNKNOWN`

## Brazil 1200 vs 1080

### What is established

The 1995 report identifies the first Latinobarómetro measurement as May-June 1995 in eight countries and states that Corporación Latinobarómetro was responsible for production and interpretation of the data.

Its substantive tables repeatedly list countries in the order:

`Argentina | Brasil | Chile | México | Paraguay | Perú | Uruguay | Venezuela`

and repeatedly assign:

`N = 1200 | 1200 | 1240 | 1204 | 587 | 1226 | ... | 1200`.

The technical annex then labels Brazil:

`Brasil | CBPA, MORI | ... | Junio | 1080 | 2.8% | 33%`.

This contradiction occurs **inside one producer document**.

The introductory total of `9077` does not reconcile with the technical-annex country Ns as printed. The annex Ns sum to `8949`. Some report tables use Uruguay `1212`, while others use `1220`; the table pattern with Brazil `1200` and Uruguay `1220` sums to `9077`. This arithmetic is documentary cross-checking only; it does not authorize a repair or a causal explanation.

### What remains unknown

No producer-authoritative documentation recovered in this court identifies:
- a 120-case Brazil exclusion population;
- a validity/editing rule yielding 1080;
- a release migration from 1080 to 1200 or vice versa;
- a weighting transformation that changes Brazil's case count from 1080 to 1200;
- a documented erratum to the 1995 technical sheet;
- a documented erratum to the 1200 table bases;
- an exact historical version genealogy explaining the conflict.

The discrepancy must remain explicit.

## Interview identifiers

The producer codebook documents:
- `pais` — Country;
- `enc` — **Number interview**.

The codebook does **not** state that `enc` is globally unique, country-unique, longitudinally stable, or a respondent identity key.

Therefore:
- noninjective `enc` values are preserved;
- no deduplication is authorized;
- no synthetic uniqueness repair is authorized;
- `enc` may be retained as a source-native interview-number carrier only;
- replay identity remains `SOURCE_SHA256 + ROW_ORDINAL`.

## WT

The producer's 1995 codebook documents:

`wt — Weighting`

with the code/range annotations:
- `0` — ERROR: No weight
- `1` — No weighting
- `0.1-10` — weighted
- `10-99` — WARNING: high
- `99-9999` — ERROR: TOO HIGH

The current producer ODA FAQ states that the ODA applies the sample weight supplied for each selected sample by default and describes table bases as weighted counts of valid cases.

That current platform behavior is useful **platform-level authority**, but it does not supply the missing 1995 source-specific facts:
- exact population/estimand of `WT`;
- whether it is strictly within-country, cross-country, or compositional;
- normalization target;
- construction/calibration margins;
- whether raw-file external analysis must apply it by default;
- whether it explains the 1200/1080 documentary contradiction.

Accordingly:
- `WT` is authoritatively a weighting field;
- its raw/source-native values must be preserved;
- no default external estimator is authorized here;
- no normalization or recomputation is authorized;
- weighted realization remains fail-closed pending exact 1995 weight authority.

## Release-page anomaly

The current 1995 landing page text mechanically says the wave comprises "18 countries/territories", while that same page's country list, the 1995 codebook, and the 1995 report identify the actual 1995 wave as eight countries. This appears to be a current landing-page/template inconsistency and is not used to redefine the 1995 source scope.

## Admission consequence

The inherited canonical source identity is not altered.

This documentary court is sufficient to:
- retain the exact canonical root;
- preserve all Brazil 1200 rows;
- preserve noninjective interview numbers;
- retain `WT` without selecting or normalizing it;
- bind the 1200/1080 conflict as an explicit unresolved release-provenance fact.

It is **not** sufficient to authorize full source-specific weighted realization, because both the causal Brazil provenance and the exact `WT` analytical domain remain unknown.

## Sources

Producer-primary:
- 1995 release page: https://www.latinobarometro.org/latinobarometro-1995
- 1995 press report: https://www.latinobarometro.org/documents/LAT-1995/informe-latinobarometro-1995.pdf
- 1995 technical records (English): https://www.latinobarometro.org/documents/LAT-1995/latinobarometro-1995-eng.pdf
- 1995 codebook v20190707: https://www.latinobarometro.org/documents/LAT-1995/latinobarometro-1995-codebook-v20190707.pdf
- ODA FAQ: https://latinobarometro.org/oda-faq
- Corporación Latinobarómetro, About Us: https://www.latinobarometro.org/about-us

Distribution/archive corroboration:
- JD Survey historical documentation catalog: https://www.jdsurvey.net/jds/jdsurveyAnalisis.jsp?ESID=428&ES_COL=135&Idioma=I&SeccionCol=10

Inherited S35 authority:
- `WORKER_RETURNS/FIABC-HQ-S35-FANIN/00_RETURN.md`
- `WORKER_RETURNS/FIABC-HQ-S35-FANIN/01_GAP_LEDGER.csv`
- `WORKER_RETURNS/FIABC-S35-1/01_CLOSED35_CANONICAL_SOURCE_ROOTS.csv`
- `WORKER_RETURNS/FIABC-S35-3/01_SOURCE_EDGE_CLASS_MANIFEST.csv`
- `WORKER_RETURNS/FIABC-S35-3/02_SOURCE_TO_EDGE_CLASS_MATRIX.csv`

## Terminal

`CLOSED35_L2_LATINOBAROMETRO1995_DOCUMENTARY_AUTHORITY_PARTIAL__BRAZIL_OR_WEIGHT_UNKNOWN_SET_RETURNED`
