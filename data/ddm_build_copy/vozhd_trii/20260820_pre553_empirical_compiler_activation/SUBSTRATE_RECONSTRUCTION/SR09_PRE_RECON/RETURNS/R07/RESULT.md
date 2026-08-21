# SR09-PRE R07 — LiTS Adversarial Raw-Source Reconnaissance

Status: `AUTHORIZED__NON_DISPOSITIVE__HIGH_PRIORITY`  
Worker: `R07`  
Family: `LITS_I_II_III_IV`  
Starting HEAD: `491a2394e323c904128ca425ef9e793e33ca0d5d`

## Holding

All four assigned LiTS source snapshots were obtained only from the frozen ChatGPT Library transports, hash-verified before probing, and hash-verified again after probing. No raw bytes were modified. No `DATABASE_URL` or legacy PostgreSQL source truth was used.

This reconnaissance does **not** certify any LiTS release. All four require source-specific hostile fixtures and documentary authority. No new physical DTA class was found beyond the frozen DTA contract. LiTS IV did expose a new **source-specific reader behavior within the existing `FORMAT_READER_COMPATIBILITY` class**: pandas 2.2.3 fails on the exact snapshot when `convert_missing=True` and automatic Stata date conversion are combined; `convert_dates=False` completes raw-state classification without altering bytes.

## Source identity

| source | rows | vars | SHA-256 |
|---|---:|---:|---|
| LiTS I | 29,002 | 1,198 | `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09` |
| LiTS II | 38,864 | 627 | `c43d0e1821c51398817d7dfdfad2c0a4a5bb0d492f6a58096670e623bb6130e9` |
| LiTS III | 51,206 | 1,290 | `368ae5d07a44975a2f0a9ce3b1e564988a966b2632e28075c56a24d60065bcc8` |
| LiTS IV | 37,478 | 1,319 | `14e1032755c4f42d8d3dc61647097ccd7605ba281551e53953c76d22a223cd1c` |

## Measured source facts

### 1. Respondent identity changes by release

- **LiTS I:** `id` is injective on all 29,002 rows. `serial` alone has only 1,114 distinct values, while `(country, serial)` is injective. This is measurement, not authority to define identity from that composite.
- **LiTS II:** `SerialID` is injective on all 38,864 rows. `(country, psu, hh)` is **not** injective: 38,861 distinct tuples, three duplicate-excess rows.
- **LiTS III:** `ID` is injective on all 51,206 rows, but `hhid` is system-missing on 28,625 rows. Among present rows, `(country, hhid)` still has 3,038 duplicate-excess rows.
- **LiTS IV:** string `hhid` is present and injective on all 37,478 rows.

No cross-release identity correspondence is inferred.

### 2. Country/scope representation is not stable

- **I:** numeric `country` plus string `countryname`; 29 observed pairings.
- **II:** numeric `country`, padded string `country_`, string `countryname`, `country0`, `Region1`, and `Region2`; 35 observed country values, while the `country` value-label dictionary contains 194 entries.
- **III:** `country` is directly stored as a string with 34 observed values; no LiTS-I/II numeric mapping was imported.
- **IV:** numeric `country` has 37 observed values and a 37-entry compatibility-decoded label dictionary.

A direct hostile example: LiTS II row 0 has `country=2` paired in-file with decoded `Albania`; LiTS IV row 0 has `country=1` with decoded `Albania`. Decoded text remains authority-limited, but the physical code instability is enough to prohibit code transfer.

### 3. Stata missingness was independently scanned

Every numeric variable in each release was scanned across every source row. This was a **full numeric-domain scan**, not an all-cell rescan of every string field.

| source | numeric vars scanned | vars with system missing | system-missing cells | extended `.a`–`.z` |
|---|---:|---:|---:|---:|
| I | 1,197 | 1,145 | 24,983,759 | 0 |
| II | 622 | 2 | 3,118 | 0 |
| III | 1,235 | 1,178 | 41,915,435 | 0 |
| IV | 1,279 | 888 | 28,377,791 | 0 |

LiTS II is especially hostile to family-wide assumptions: only `age5564` and `age65` carry Stata system missing, 1,559 rows each. LiTS III and IV have radically denser system-missing incidence.

No extended Stata missing values were observed in any of the four releases.

### 4. Ordinary semantic-looking codes are not physical missing

Representative exact measurements:

- I `q201=98` at row 6,286 carries compatibility-decoded “don't know”; `q301_1=6` at row 22 carries “not applicable”. Both are ordinary values.
- II `q203_t1=-99` at row 25 and `q224a_t1=-98` at row 11 are ordinary values under compatibility-decoded refusal/N/A labels.
- III `q112_1=-99` at row 1,694 is ordinary even though the same variable also contains 38,220 Stata system-missing cells. `q203=-98` at row 1,963 is ordinary.
- IV `q1032=-99` at row 418, `q208=-98` at row 480, and `visit1outcome=814` at row 132 are ordinary values under compatibility-decoded refusal/N/A/soft-refusal labels.

These remain `SEMANTIC_CODE_CANDIDATE` evidence only. No label text was promoted into C11 semantics.

### 5. Weight/design surfaces drift materially

- I: `weight_0`, `weight_1`, `weight_2`; each has 29,000 ordinary values + 2 system missings.
- II: `weight`, `XCweight`; neither has system missing; `psu` also remains a raw design candidate.
- III: `weight_population`, `weight_sample`, `weight_one`; all fully ordinary; `PSU_number` remains separate.
- IV: `weight`, `weight_pop`, `weight_trt`, `weight_pop_trt`. The first two each have 89 system-missing rows; the top-up pair each have 36,369 system-missing rows. At row 33,351 base `weight` is system missing while `weight_trt` is ordinary `0.8103665009995247`.

No primary/default weight, estimand, normalization rule, or lawful combination is inferred.

### 6. Routing/module/topology representation changes form

- I: twelve household-member slot families are explicit (`q101_1..12`, `q102_1..12`, `q103_1..12`); `q105_12` is physically present but system-missing for every row.
- II: repeated household slots continue; ordered `q305_1`/`q305_2` priority fields are distinct, and the source contains a random-selection carrier named `select`.
- III: **308 `PR*` variables and 308 `SR*` variables** expose separate primary/secondary respondent module surfaces, alongside five visit/outcome blocks.
- IV: **134 explicit `*_skip` variables**, ten visit blocks (40 visit variables), twenty household-name slots, twenty `q103` slots, and ordered `sections_order1/2` fields are physically represented.

Raw missingness is not used to infer eligibility. The explicit carriers are preserved as evidence; questionnaire semantics remain an authority gap.

### 7. Schema/name continuity is actively dangerous

Pairwise exact-name overlap is low and usually unstable:

| pair | exact-name overlap | storage-type drift | format drift | decoded-label drift |
|---|---:|---:|---:|---:|
| I–II | 65 | 64 | 64 | 65 |
| I–III | 68 | 68 | 64 | 68 |
| I–IV | 40 | 40 | 40 | 40 |
| II–III | 77 | 77 | 77 | 77 |
| II–IV | 85 | 85 | 85 | 85 |
| III–IV | 78 | 15 | 78 | 75 |

This is not cosmetic drift. Same names such as `q201`, `q203`, `q204`, and household-member fields are repeatedly reused for different storage types and decoded question labels. Name-only harmonization would rewrite source history.

### 8. Encoding/text authority remains open

The governing rule remains unchanged for **all four** snapshots:

`latin1 = COMPATIBILITY_EXECUTION_ONLY__NOT_SOURCE_TEXT_ENCODING_AUTHORITY`

This worker did not infer intended encoding and did not repair label text. The frozen pyreadstat compatibility path was not re-executed because `pyreadstat` is unavailable in this runtime; the accepted SR03 result remains the baseline for that governed execution path.

As an independent structural reader, pandas 2.2.3 reports:

- I format 113: `latin-1`
- II format 115: `latin-1`
- III format 118: `utf-8`
- IV format 118: `utf-8`

That cross-reader difference is **not** an encoding ruling. It strengthens the requirement that reader compatibility provenance and source-text authority remain separate.

## Reconnaissance dispositions

Each source carries:

- `KNOWN_HAZARD_CLASS__SOURCE_SPECIFIC_FIXTURE_REQUIRED`
- `DOCUMENTARY_AUTHORITY_GAP`

No source is certified. No new DTA physical hazard class is asserted.

## Required later authority

Later certification needs release-specific authority for respondent identity, country/scope coding and crosswalks, weight/design semantics, routing/module semantics, source-text encoding, and cross-release semantic equivalence.

Token:

`PRE553_SR09PRE_R07_LITS_RECON_COMPLETE`
