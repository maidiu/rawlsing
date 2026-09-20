# Latinobarómetro 1995 — Residual WT and ENC Authority

## 1. Scope

This pass asks only whether deeper archival evidence closes:
- `ENC` uniqueness scope;
- `WT` estimand/population domain;
- `WT` normalization;
- `WT` construction/calibration;
- external raw default weighted estimator.

It does not inspect raw values.

## 2. ENC

Inherited producer authority:
- variable `ENC`;
- label: **Number interview**.

### New evidence searched

Historical JDS/ASEP materials establish:
- annual individual microdata files;
- official questionnaires/technical records;
- country×wave sample selection in the archive;
- later harmonization/replacement of named geography/party coding.

None states that `ENC` is:
- unique over the aggregate wave;
- unique within country;
- unique within country×wave;
- explicitly nonunique by design;
- a person identifier;
- stable through the 2011/2013 file replacements;
- a cross-wave identifier.

Country×wave being a "sample" is not a uniqueness declaration.

### Frozen authority state

`ENC_UNIQUENESS_SCOPE = UNDOCUMENTED`

This is sharper than "administrative only": **administrative-only is itself not explicitly documented for ENC**.

Binding rules:
- retain `ENC` as source-native interview-number metadata;
- collisions remain lawful;
- no deduplication;
- no `PAIS+ENC` key promotion;
- no longitudinal linkage;
- replay identity remains `SOURCE_SHA256 + ROW_ORDINAL`.

## 3. WT — positive authority that survives

Inherited:
- `WT` is producer-labelled **Weighting / Ponderación**;
- the 1995 codebook documents weight/no-weight/range annotations.

Current producer ODA:
- by default, statistics use the **sample weight provided for each selected sample**;
- if no weight exists, results are unweighted;
- percentages are based on weighted valid responses.

Source:
https://latinobarometro.org/oda-faq

Current producer data architecture distinguishes:
- country-level samples/data;
- wave-level annual aggregate;
- longitudinal/time-series products.

Sources:
- https://latinobarometro.org/study-level
- https://www.latinobarometro.org/data

These current statements establish a producer practice at the **ODA platform surface**.

## 4. What they do not bind to 1995 raw WT

No recovered document says:

`1995 raw variable WT == the exact ODA supplied sample-weight object under a documented immutable mapping`

No recovered 1995 document defines:
- target population;
- estimand;
- country-only versus cross-country scope;
- normalization target;
- calibration variables;
- age/sex/education/geography margins;
- post-stratification/raking procedure;
- design/nonresponse correction;
- expansion-weight versus normalized-weight interpretation;
- variance-estimation role;
- combination rule across countries.

Historical JDS documentation inventory lists:
- 1995 questionnaire/technical record;
- 1995 codebook;
- later general methodological reports.

It does not expose a separate 1995 weighting construction note.

Source:
https://www.jdsurvey.net/jds/jdsurveyAnalisis.jsp?ESID=428&ES_COL=135&Idioma=I&SeccionCol=10

## 5. Exact residual matrix

| Authority question | Final state | Authorized action |
|---|---|---|
| Is `WT` a weighting field? | **CLOSED / YES** | preserve it |
| May current ODA apply a sample weight by default? | **CLOSED / YES, ODA SURFACE ONLY** | describe current platform behavior |
| 1995 target population / estimand | **IRREDUCIBLE DOCUMENTARY UNKNOWN** | none |
| 1995 country-local vs cross-country domain | **IRREDUCIBLE DOCUMENTARY UNKNOWN** | do not combine/assume |
| 1995 normalization | **IRREDUCIBLE DOCUMENTARY UNKNOWN** | do not renormalize |
| 1995 construction / calibration | **IRREDUCIBLE DOCUMENTARY UNKNOWN** | do not reconstruct |
| 1995 variance/design use | **IRREDUCIBLE DOCUMENTARY UNKNOWN** | no design inference |
| External raw-file default estimator | **NO 1995 PRODUCER AUTHORIZATION RECOVERED** | default must remain disabled/fail-closed |
| Use `WT` to explain Brazil 1200/1080 | **NOT AUTHORIZED** | preserve contradiction |
| Substitute `WT=1` when uncertain | **NOT AUTHORIZED** | fail closed |
| Infer semantics from numeric distribution | **FORBIDDEN** | not performed |

## 6. Why current ODA is insufficient for an external raw default

"ODA defaults to weighting" is an instruction about a producer-controlled analytical application.

An external raw-data runtime would need an additional binding:
1. exact raw variable → estimator weight;
2. exact sample/domain;
3. exact normalization/composition law;
4. exact missing/invalid-weight behavior;
5. cross-country combination rule if applicable.

Those bindings were not recovered for 1995.

Therefore the absence is operationally decisive:

`CURRENT_ODA_DEFAULT_WEIGHTING != AUTHORITY_FOR_EXTERNAL_1995_RAW_DEFAULT_ESTIMATOR`

## 7. Later historical-file replacement does not repair WT/ENC

JDS/ASEP documents replacement/harmonization of historical files for:
- Region;
- City;
- Political Party.

No recovered notice adds:
- `ENC` uniqueness rules;
- `WT` reconstruction;
- `WT` normalization;
- Brazil sampling corrections.

Thus:
- the replacement event is part of provenance;
- its documented scope cannot be expanded to unresolved variables.

## 8. Final residual set

Frozen:
- `ENC_UNIQUENESS_SCOPE = UNDOCUMENTED`
- `WT_ESTIMAND_AND_POPULATION_DOMAIN = IRREDUCIBLE_DOCUMENTARY_UNKNOWN`
- `WT_NORMALIZATION = IRREDUCIBLE_DOCUMENTARY_UNKNOWN`
- `WT_CONSTRUCTION_CALIBRATION = IRREDUCIBLE_DOCUMENTARY_UNKNOWN`
- `EXTERNAL_RAW_DEFAULT_WEIGHTED_ESTIMATOR = NO_1995_PRODUCER_AUTHORIZATION_RECOVERED__FAIL_CLOSED`

No concrete residual-specific producer archive lead remains.
