# PYAT1002 — source metadata / custody census

This is a metadata and permission-proof census. It is not a source read,
a source-positive, a U/Epre operation, an I02 release, a first I03 fact, or
a scientific/authority acceptance. No SAV/DTA bytes were opened, decoded,
read or hashed by this commission.

## Exact source of truth

| Input | Exact reference used |
|---|---|
| R157 source library index | `source_pre553_validation/integration/SOURCE_LIBRARY_INDEX.json` @ `1924499ef52403a0f331b8aff9b7c7eff99bf1e2` |
| R157 source roster | `rawlsing_next/source_configuration/evidence/SOURCE_ROSTER.json` @ same cut |
| R157 readiness/permission field | `SOURCE_PRE553_PLAN/evidence/PER_SOURCE_READINESS.csv` @ same cut |
| R157 per-source gaps/routing | `SOURCE_PRE553_PLAN/evidence/PER_SOURCE_GAPS.json` @ same cut |
| R157 original configs | `rawlsing_next/source_configuration/data/SRCxx/*.config.json` @ same cut |
| Historical ledger | `WORKER_RETURNS/PYAT960_S1E_A_COUNTER/evidence/b_all35_ledger.json` |
| Local artifact presence | `stat` only under `RAWLSING_LOCAL_DATA_ROOT` (no open/hash) |

## Historical ledger (preserved, not science)

| Quantity | Exact value |
|---|---:|
| Sources | 35 |
| Original item identities | 18,276 |
| Physical slots | 18,413 |
| Exact relation matches | 18,250 |
| Unjoined implementation IDs | 26 |
| Unjoined: SRC01 | 3 |
| Unjoined: SRC24 | 18 |
| Unjoined: SRC26 | 5 |

Unjoined status: `PREPARATION_HELD__NOT_SCIENCE`. These identities are not
respondent counts, executable operation counts, denominator membership or
scientific compliance.

## Per-source census

| SRC | Family / wave | Artifact | Declared SHA-256 (prefix) | Bytes | Rows | Items / slots | Response slots | Weight slots | Present / size | Routing unresolved | Blocked response gaps | Unjoined |
|---|---|---|---|---:|---:|---:|---:|---:|---|---:|---:|---:|
| SRC01 | Afrobarometer / R1 | `Afro Barometer Round 1.sav` | `6c9869a7cc73…` | 4,492,565 | 21,531 | 144 / 144 | 129 | 5 | yes / match | 131 | 7 | 3 |
| SRC02 | Afrobarometer / R5 | `Afro Barometer Round 5.sav` | `c9200ba325bb…` | 49,689,458 | 51,587 | 348 / 348 | 249 | 2 | yes / match | 232 | 24 | 0 |
| SRC03 | Afrobarometer / R9 | `Afro Barometer Round 9.sav` | `3afcecd08d2f…` | 70,621,348 | 53,444 | 421 / 421 | 310 | 4 | yes / match | 294 | 51 | 0 |
| SRC04 | Arab Barometer / I | `Arab Barometer Wave 1.sav` | `2a48ba4b2f23…` | 1,531,099 | 7,337 | 181 / 181 | 178 | 0 | yes / match | 179 | 2 | 0 |
| SRC05 | Arab Barometer / II | `Arab Barometer Wave 2.sav` | `6529841b97bd…` | 7,192,678 | 12,782 | 468 / 468 | 448 | 0 | yes / match | 463 | 2 | 0 |
| SRC06 | Arab Barometer / V | `Arab Barometer Wave 5.sav` | `6a5cbad637ce…` | 11,637,259 | 27,850 | 359 / 359 | 337 | 0 | yes / match | 241 | 13 | 0 |
| SRC07 | Arab Barometer / VIII | `Arab Barometer Wave 8.sav` | `a5e83a953f03…` | 12,275,728 | 15,627 | 690 / 690 | 651 | 0 | yes / match | 554 | 30 | 0 |
| SRC08 | Asian Barometer / W1 | `Asian Barometer Wave 1.sav` | `ac0b8bc1ddb2…` | 3,451,655 | 12,217 | 217 / 217 | 187 | 9 | yes / match | 183 | 10 | 0 |
| SRC09 | Asian Barometer / W4 | `Asian Barometer Wave 4.sav` | `4d914817509d…` | 7,735,596 | 20,667 | 289 / 289 | 240 | 2 | yes / match | 180 | 3 | 0 |
| SRC10 | Asian Barometer / W5 | `Asian Barometer Wave 5.sav` | `2576e428ff8d…` | 10,688,196 | 26,951 | 308 / 308 | 204 | 1 | yes / match | 277 | 99 | 0 |
| SRC11 | EVS / 1981 | `EVS 1981.sav` | `5b703173845c…` | 11,815,613 | 19,378 | 370 / 370 | 331 | 1 | yes / match | 89 | 6 | 0 |
| SRC12 | EVS / 1990 | `EVS 1990.sav` | `66252a92c59b…` | 24,341,244 | 38,213 | 390 / 390 | 336 | 2 | yes / match | 203 | 8 | 0 |
| SRC13 | EVS / 1999 | `EVS 1999.sav` | `6058644a9308…` | 31,857,144 | 41,125 | 513 / 513 | 359 | 2 | yes / match | 435 | 7 | 0 |
| SRC14 | EVS / 2008 | `EVS 2008.sav` | `5469e3b39cbb…` | 63,832,833 | 66,280 | 477 / 477 | 384 | 2 | yes / match | 174 | 9 | 0 |
| SRC15 | EVS / 2017 | `EVS 2017.sav` | `95096c2474b8…` | 53,499,063 | 59,438 | 474 / 474 | 337 | 4 | yes / match | 362 | 13 | 0 |
| SRC16 | GSS / 1972 | `GSS1972.sav` | `e368fc0f1d14…` | 1,647,241 | 1,613 | 216 / 216 | 157 | 0 | yes / match | 107 | 10 | 0 |
| SRC17 | GSS / 1973 | `GSS1973.sav` | `59e65801dc26…` | 1,984,639 | 1,504 | 339 / 339 | 279 | 0 | yes / match | 221 | 10 | 0 |
| SRC18 | GSS / 1984 | `GSS1984.sav` | `1da2df0c0e06…` | 4,309,530 | 1,473 | 675 / 675 | 592 | 0 | yes / match | 417 | 10 | 0 |
| SRC19 | GSS / 1993 | `GSS1993.sav` | `7fc409cc0717…` | 5,506,397 | 1,606 | 752 / 752 | 694 | 0 | yes / match | 645 | 13 | 0 |
| SRC20 | GSS / 2002 | `GSS2002.sav` | `8ece38110523…` | 17,746,227 | 2,765 | 1,119 / 1,119 | 1,021 | 0 | yes / match | 1,076 | 17 | 0 |
| SRC21 | GSS / 2010 | `GSS2010.sav` | `c229aff7430c…` | 10,170,184 | 2,044 | 922 / 922 | 592 | 0 | yes / match | 622 | 19 | 0 |
| SRC22 | GSS / 2016 | `GSS2016.sav` | `a053bdc5661e…` | 16,989,724 | 2,867 | 1,018 / 1,018 | 924 | 0 | yes / match | 577 | 19 | 0 |
| SRC23 | GSS / 2024 | `GSS2024.sav` | `27166a481ba6…` | 20,922,610 | 3,986 | 980 / 980 | 879 | 0 | yes / match | 800 | 17 | 0 |
| SRC24 | Latinobarómetro / 1995 | `Latinobarometro 1995.sav` | `4b7fc6da17df…` | 2,224,483 | 9,069 | 203 / 203 | 183 | 0 | yes / match | 197 | 7 | 18 |
| SRC25 | Latinobarómetro / 2011 | `Latinobarometro 2011.sav` | `a44e89e08e56…` | 9,900,209 | 20,204 | 414 / 414 | 370 | 0 | yes / match | 379 | 25 | 0 |
| SRC26 | Latinobarómetro / 2024 | `Latinobarometro 2024.sav` | `ff5cef18c879…` | 7,886,834 | 19,214 | 195 / 332 | 275 | 0 | yes / match | 193 | 5 | 5 |
| SRC27 | LiTS / 2006 | `LiTS_I.dta` | `7cac43e2ca5b…` | 139,531,180 | 29,002 | 1,198 / 1,198 | 280 | 0 | yes / match | 0 | 918 | 0 |
| SRC28 | LiTS / II | `LiTS_II.dta` | `c43d0e1821c5…` | 199,716,969 | 38,864 | 627 / 627 | 542 | 0 | yes / match | 3 | 84 | 0 |
| SRC29 | LiTS / III | `LiTS_III.dta` | `368ae5d07a44…` | 170,487,994 | 51,206 | 1,290 / 1,290 | 1,165 | 0 | yes / match | 0 | 124 | 0 |
| SRC30 | LiTS / IV | `LiTS_IV.dta` | `14e1032755c4…` | 110,465,945 | 37,478 | 1,319 / 1,319 | 1,073 | 0 | yes / match | 0 | 245 | 0 |
| SRC31 | South Asia / W1 | `South Asia Wave 1.sav` | `de7b51f9abf4…` | 595,974 | 8,442 | 68 / 68 | 64 | 0 | yes / match | 66 | 3 | 0 |
| SRC32 | South Asia / W2 | `South Asia Wave 2.sav` | `6a5329ea16f4…` | 894,051 | 10,617 | 73 / 73 | 69 | 0 | yes / match | 70 | 3 | 0 |
| SRC33 | WVS / W1 | `WVS Wave 1.sav` | `051bf450568f…` | 6,358,941 | 13,586 | 188 / 188 | 143 | 0 | yes / match | 175 | 5 | 0 |
| SRC34 | WVS / W4 | `WVS Wave 4.sav` | `c6757ed18765…` | 41,997,221 | 60,045 | 418 / 418 | 354 | 0 | yes / match | 406 | 4 | 0 |
| SRC35 | WVS / W7 | `WVS Wave 7.sav` | `2bd2a20fc565…` | 185,163,494 | 97,220 | 613 / 613 | 390 | 0 | yes / match | 397 | 146 | 0 |

## Family counts

| Family | Sources |
|---|---:|
| Afrobarometer | 3 |
| Arab Barometer | 4 |
| Asian Barometer | 3 |
| EVS | 5 |
| GSS | 8 |
| Latinobarómetro | 3 |
| LiTS | 4 |
| South Asia | 2 |
| WVS | 3 |

## Field provenance and limits

- `declared_source_sha256`, byte size, row count and column count are the
  R157 `SOURCE_ROSTER.json` values; they match the 35 original config
  `identity` bindings for all rows.
- `counts` are the exact R157 source-index counts (original items, physical
  slots, questions, response slots, coordinate slots, routing rules and
  weight slots). They are not equivalent dimensions and are not collapsed.
- `edition_custody.status` is
  `PRESENT_SIZE_MATCHED_HISTORICAL_HASH_NOT_REHASHED`: the artifact is
  present at the exact local filename and its size matches the R157
  declared size. The historical SHA-256 is recorded; the current bytes were
  not re-hashed under the commission's no-rehash rule.
- `host_custody.host_authentication` is `NOT_ESTABLISHED`. A local file
  stat is not an authenticated host grant.
- `instrument_codebook.codebook_status` is `KNOWN_METADATA` for all 35;
  `semantic_authority_status` is
  `PREPARATION_ONLY_NOT_SOURCE_SCIENTIFIC_AUTHORITY`.
- `administration_routing_status` preserves the exact routing-state map.
  Every row retains either explicit `SOURCE_ROUTING_UNRESOLVED` states or
  blocked response-authority gaps; no routing is invented from physical
  missingness.
- `universe()` fields preserve the exact config values. Sample frames and
  sampling designs remain UNKNOWN/UNRESOLVED where the source config says so;
  no target population is invented.
- `response_weight_design.weight_design_status` never promotes a declared or
  held weight slot into design/estimand authority. Population, temporal and
  causal gates remain `NOT_RUN`/`NOT_AUTHORIZED`.
- `current_permission.decision` is `UNKNOWN_OWNER_DECISION` for all 35: the
  source identities and historical evidence are present, but no current
  competent permission proof was located.

