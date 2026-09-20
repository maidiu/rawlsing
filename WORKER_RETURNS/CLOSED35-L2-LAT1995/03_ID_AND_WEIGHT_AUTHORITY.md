# Latinobarómetro 1995 — ID and Weight Authority

## 1. Governing boundary

This file records only what producer documentation authorizes for `enc` and `wt`.

It does not infer semantics from the inherited SAV's value distribution and does not open/process raw source bytes.

## 2. Interview identifier — `enc`

Producer codebook v20190707, page 1:

- `pais` — `Country`
- `enc` — `Number interview`
- `enc` documented range: `0-99999` / `1-99999` as rendered by the codebook.

Source:
https://www.latinobarometro.org/documents/LAT-1995/latinobarometro-1995-codebook-v20190707.pdf

### Authority recovered

The producer authorizes the semantic label **Number interview**.

### Authority not recovered

The codebook does not say that `enc` is:
- globally unique across the eight-country aggregate;
- unique within each country;
- unique within interviewer, region, or fieldwork batch;
- stable across releases;
- stable across waves;
- a person identifier;
- a longitudinal key.

The existence of a separate `pais` field does not by itself authorize the composite `pais + enc` as injective.

### Binding realization law

| Question | Holding |
|---|---|
| Preserve `enc` exactly as a source-native carrier? | YES |
| Treat `enc` as respondent replay identity? | NO |
| Deduplicate rows sharing `enc`? | NO |
| Synthesize a unique identifier from `enc`? | NO |
| Assume `pais + enc` is unique? | NO |
| Replay identity | `SOURCE_SHA256 + ROW_ORDINAL` |
| Uniqueness scope | `UNKNOWN` |

This is consistent with inherited EC07: native ID collision/noninjectivity never licenses row collapse.

## 3. Weight — `wt`

Producer codebook v20190707, page 27:

- `wt` — **Weighting**
- `0` — `ERROR: No weight`
- `1` — `No weighting`
- `0.1-10` — `weighted`
- `10-99` — `WARNING: high`
- `99-9999` — `ERROR: TOO HIGH!`

The Spanish producer codebook likewise labels `wt` as **Ponderación**.

Sources:
- https://www.latinobarometro.org/documents/LAT-1995/latinobarometro-1995-codebook-v20190707.pdf
- https://www.latinobarometro.org/documents/LAT-1995/latinobarometro-1995-libro-de-codigos-v20190707.pdf

### Current producer platform behavior

The current Latinobarómetro ODA FAQ says:
- ODA statistics use the **sample weight provided for each selected sample** by default;
- if a selected sample has no weight, the result is unweighted;
- ODA percentages are calculated over weighted valid responses;
- the displayed base `N` is the weighted count of valid cases after filters/sample selection.

Source:
https://latinobarometro.org/oda-faq

This is meaningful producer authority for **current ODA behavior**.

It is not sufficient to convert `wt` into a complete 1995 raw-file estimator contract.

## 4. Exact 1995 WT authority matrix

| Property | Status | Basis |
|---|---|---|
| Field is a weighting variable | **CLOSED / YES** | 1995 producer codebook |
| Preserve raw `wt` values | **YES** | source-native preservation + codebook |
| `1` denotes "No weighting" | **YES** | 1995 producer codebook |
| Generic weighted-value range 0.1-10 documented | **YES** | 1995 producer codebook |
| Intended population / estimand | **UNKNOWN** | not recovered |
| Strictly within-country weight | **UNKNOWN** | current ODA says "sample weight" but 1995 codebook does not define domain |
| Cross-country aggregate weight | **UNKNOWN** | not recovered |
| Normalization target (mean 1 / sum N / population total / other) | **UNKNOWN** | not recovered |
| Calibration/raking margins | **UNKNOWN** | not recovered |
| Construction formula | **UNKNOWN** | not recovered |
| Variance/design interpretation | **UNKNOWN** | not recovered |
| External raw-file default estimator | **NOT AUTHORIZED** | ODA default is platform-specific; no 1995 raw-file estimator instruction recovered |
| Use WT to explain 1200 vs 1080 | **NOT AUTHORIZED** | no producer linkage recovered |
| Recompute/renormalize WT | **NOT AUTHORIZED** | no rule recovered |
| Replace missing/invalid WT by 1 | **NOT AUTHORIZED** | EC12 fail-closed law |

## 5. Brazil discrepancy interaction

The producer's current ODA definition of a displayed base `N` as a **weighted valid-case count** cannot be retroactively imported into the 1995 press report to explain its table bases.

Reasons:
1. the 1995 press report predates the current ODA surface;
2. the report does not say its printed `N=1200` is a weighted base;
3. the technical annex says `Muestra (N Casos)=1080`;
4. no 1995 producer note links `wt` to the 120-case difference.

Therefore:

`WT_PRESENT + CURRENT_ODA_WEIGHTING_DEFAULT != DOCUMENTED_1995_1200_VS_1080_EXPLANATION`

## 6. Source-specific realization consequence

A source-specific implementation may safely preserve:
- exact canonical source identity;
- row ordinals;
- `pais`;
- noninjective `enc`;
- `wt` as a source-native weighting carrier;
- the explicit unresolved Brazil provenance contradiction.

But this worker does **not** authorize:
- deduplication by interview number;
- default weighted external analysis;
- cross-country weighting;
- normalization of `wt`;
- deriving fielded/valid case status from weight values;
- dropping any Brazil rows.

Because exact 1995 weight domain/normalization remains unknown, this court returns PARTIAL.
