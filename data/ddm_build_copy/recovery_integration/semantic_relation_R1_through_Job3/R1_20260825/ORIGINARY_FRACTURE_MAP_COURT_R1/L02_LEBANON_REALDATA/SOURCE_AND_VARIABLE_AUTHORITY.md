# L02 SOURCE AND VARIABLE AUTHORITY — ARAB BAROMETER WAVE VIII LEBANON Q873

Status: `SOURCE_BOUND__REAL_LIBRARY_DATA`

## Mandatory source objects

| Object | SHA-256 | Use |
|---|---|---|
| `ArabBarometer_WaveVIII_English_v3.sav` | `a5e83a953f03dd890e076a51da473051f1cfd1ca2e8ab93c2172eeb2517af998` | released respondent-level Wave VIII data |
| `ENG-Arab-Barometer-Wave-VIII-Questionnaire-RELEASE-FIN-NOV-2024-1.pdf` | `d72c3afc4529703376dc1133a3d984541c2ceebd1af6cb03a1562f6ce104c2fb` | instrument text, option/routing authority |
| `rawlsing chatlog DDM chatgpt(1).txt` | `b0ff181b0d1f6a591b005b829aafeb27b0740249332b49e08bd381800ab1745a` | originary exemplar and remembered claims to replicate/correct |

Library objects were read/materialized only and were not mutated.

## Exact empirical surface

Questionnaire Q873 asks whether people in the respondent's country face discrimination because of specified bases and is **SELECT ALL THAT APPLY**. Source options are:

1. socioeconomic class
2. region within country
3. skin color
4. race or ethnicity
5. nationality
6. religion
7. gender
8. tribe — routed only to countries 7, 8, 9
9. age
10. sexual orientation — routed only to countries 10 and 21
11. disability status
12. migration status
13. none of these — mutually exclusive with every other substantive option
98. don't know
99. refused

The released SAV encodes these as one 0/1 toggle per item: `Q873_1` … `Q873_13`, plus `Q873_98` and `Q873_99`. The SAV value labels explicitly bind `1` to selection of each named discrimination basis and `0` to the non-selected toggle state. Multi-select identity is therefore preserved as respondent-level vectors and exact response patterns; **`Q873_1=1` means SES selected, not SES only**.

## Country, weight, and denominator authority

- Lebanon is `COUNTRY=10` in the SAV's source value labels.
- Released analysis weight field: `WT`.
- The SAV header contains no active SPSS weight command (`weight_index=0`); this worker explicitly applies released field `WT` and also reports unweighted `n`.
- Released rows: `15,627`.
- Q873 SES toggle observed/nonmissing: `14,417` rows.
- The `1,210` structurally missing Q873 rows are exactly Kuwait (`COUNTRY=9`) in this release. They are **not** coded as Q873 non-selection.
- Source-routed substantive Wave-VIII Q873 denominator is:
  `Q873_1 nonmissing AND Q873_98 != 1 AND Q873_99 != 1`.
- Lebanon substantive denominator is the same rule plus `COUNTRY=10`: `n=2,339`, weighted `n=2,334.695584341760`.
- Lebanon has 62 Q873 don't-know rows and 2 refused rows outside the substantive denominator.
- `Q873_8` is structurally unavailable in Lebanon, as required by questionnaire routing; `Q873_10` is observed in Lebanon, also as required by routing.
- Zero violations of Q873 option-13 exclusivity are present in the Lebanon substantive data.

## Positional variables used

| Source variable | Source meaning / worker use |
|---|---|
| `Q1003` | highest education: 1 no formal, 2 elementary, 3 preparatory/basic, 4 secondary, 5 technical, 6 BA, 7 MA+ |
| `Q1012` | religion: Muslim, Christian, no religion, other |
| `Q1012A_MUSLIM` | source denomination among Muslims, including Sunni, Shia, Druze, etc. |
| `Q1012A_CHRISTIAN` | source denomination among Christians, including Maronite, Orthodox, Catholic, Armenian, etc. |
| `Q609` | religiosity |
| `Q1015` | monthly household income in local currency |
| `Q1016` | household financial situation / ability to cover expenses |
| `Q13` | urban / rural / camp |
| `Q1001` | age |
| `Q1002` | gender |
| `STRATUM`, `PSU` | released sampling identifiers, preserved as source metadata; not used to fabricate a variance estimator |

Three deterministic descriptive helper fields are derived by the analysis script:

- `DENOMINATION_COMBINED`: source-preserving union of Muslim and Christian denomination variables under `Q1012` routing.
- `COUNTRY_INCOME_RANK_QUINTILE`: country-local percentile quintile of source `Q1015`; used so local-currency income values are not compared numerically across countries.
- `AGE_BAND`: 18–29 / 30–44 / 45–59 / 60+.

These helper fields are **descriptive splitters only**, never actor beliefs, personalities, causes, or new source semantics.

## SAV read / replay method

`analyze_lebanon_fracture_map.py` verifies all three mandatory source hashes before analysis. Because no SPSS reader dependency is assumed, it reads this exact `$FL2` SAV release directly:

- layout code `2`
- case size `692`
- bytecode compression `1`
- case count `15,627`
- compression bias `100`
- data start byte `176,848`

The parser fails closed unless it decodes exactly 15,627 cases, ends on a complete case, and consumes the source file exactly to its byte size.

Repository replay then runs `normalize_and_shard_oracles.py`, which performs serialization only: CRLF/LF normalization to canonical LF and deterministic 50-row sharding of the 370-row response-pattern census. The required `RESPONSE_PATTERN_ORACLE.csv` is the manifest emitted by that step; the eight part files contain every monolithic data row in order.

## Weight, support, and uncertainty law

Every branch carries unweighted `n`, sum of `WT`, and Kish effective sample size. Binary selection uncertainty uses an approximate 95% Wald interval with Kish effective `n`. This is a **descriptive approximation, not a full complex-survey variance estimator**; no design-based precision claim beyond that approximation is made.

Originary stop-law thresholds recovered from the mandatory chatlog are frozen as:

- `n < 25` → `UNDERPOWERED_STOP_NO_SPLIT`
- `25 <= n < 50` → `EXPLORATORY_ONLY`
- `n >= 50` → `DESCRIPTIVE_ORACLE_SUPPORTED`

The last label records count support for this acceptance oracle; it does not convert descriptive association into causality.

## Determinicity method

`BRANCH_DETERMINICITY_ORACLE.csv` ranks source/derived positional splitters by weighted mutual information normalized by target entropy. Every row is explicitly limited to:

`DESCRIPTIVE_ASSOCIATION_ONLY__NOT_CAUSAL_NOT_PERSONA`

High-cardinality denomination associations in small subgroups are retained as descriptive signals with cell-support cautions rather than promoted to stable causal claims.
