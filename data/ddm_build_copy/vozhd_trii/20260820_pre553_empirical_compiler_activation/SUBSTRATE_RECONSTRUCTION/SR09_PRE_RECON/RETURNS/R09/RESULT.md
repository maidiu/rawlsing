# SR09-PRE R09 — WVS RAW-SOURCE RECONNAISSANCE RETURN

Status: `COMPLETE__NON_DISPOSITIVE_RECONNAISSANCE`

Token: `PRE553_SR09PRE_R09_WVS_RECON_COMPLETE`

## Input gate

Both frozen Library transports matched exactly. Only WVS Waves 1 and 4 were extracted from `surveys.zip`; only WVS Wave 7 was extracted from `WVS Wave 7.sav.zip`. All three extracted source hashes matched the R09 order before probing.

The accepted SR03 R3 package also matched its frozen checkout hash and supplied the already-accepted full physical manifests. Raw full traversals were then used only because identity injectivity, observed country support, exact row sentinels, and cell-vector equality cannot be recovered from aggregate manifest counts.

## WVS Wave 1 — measured facts

- 13,586 rows × 188 variables, UTF-8.
- Physical cells: 2139348 ordinary, 263028 SPSS user-missing, 151792 system-missing.
- `V3` (Original respondent number) is not globally injective: 2,677 distinct values. `(V2,V3)` is injective for all 13,586 rows.
- `S007` (Unified respondent number) is globally injective: 13,586/13,586. It is nevertheless retained as an attribute, not substituted for row-ordinal replay identity.
- Hostile metadata shape: `S007` raw values range from 320120001 through 8400122325 while the SAV reports original format `F2.0`. Storage is still numeric 8-byte. Raw magnitude and display/print metadata therefore cannot be collapsed.
- 10 observed country codes; `S025` carries 10 observed country-year states.
- 13 physically complete weight-like variables are present; no explicit PSU/stratum candidate is named in the SAV metadata.
- Ordered structures include `V106/V107` and `V203/V204`. `V204` observes 515 typed `-3` cells while `V107` observes none, demonstrating that even within W1 a numeric missing code is not a universal second-slot state.
- Eight derived variables are system-missing on every row. This is a typed physical fact, not permission to delete them.

Disposition: `KNOWN_HAZARD_CLASS__SOURCE_SPECIFIC_FIXTURE_REQUIRED`.

## WVS Wave 4 — measured facts

- 60,045 rows × 418 variables, UTF-8.
- Physical cells: 15615063 ordinary, 9284788 SPSS user-missing, 198959 system-missing.
- `V3` has 301 typed `-5` missing IDs. Excluding them leaves 59,744 rows but only 59,711 distinct `(V2,V3)` keys: 32 duplicate keys, 33 excess rows, max multiplicity 3. W4 has no `S007`.
- `V2` and `V2A` are separately named coordinates but are cell-for-cell identical on all 60,045 rows; each has 41 observed country codes. The label alone does not authorize collapsing or inventing a split-up semantics.
- Three columns (`ISL22`, `V160S`, `V160T`) are SPSS user-missing on every row; `I_TRUSTCOURTS` is system-missing on every row.
- `V218` contains ordinary, non-missing country-specific values whose labels look semantically absent: `1208=Refused` (5), `5904=Do not know` (26), `9309=I don't know/no answer` (56). These remain `OBSERVED_STORAGE_VALUE` pending source authority.
- `V220` and `Q223_LOCAL` have identical raw vectors on all rows but different English/local value-label dictionaries. Raw equality does not make metadata interchangeable.
- Ordered/repeated families include `V120–V125`, `V214/V215`, and party first/second-choice variables. `V221` observes 1,960 typed `-3` cells; the aims second-choice variables `V121/V123/V125` do not.
- Four weight-like variables are present; no explicit PSU/stratum candidate is named in SAV metadata.

Disposition: `KNOWN_HAZARD_CLASS__SOURCE_SPECIFIC_FIXTURE_REQUIRED`.

## WVS Wave 7 — hostile baseline replay

The frozen W7 oracle remains controlling evidence for its known hostile facts. The targeted raw traversal reproduced the identity/scope shape without importing W7 semantics into earlier waves:

- 97,220 rows × 613 variables, UTF-8.
- `D_INTERVIEW`: 96,221 distinct values; `858069901` occurs on 1,000 Uruguay rows.
- `S007`: 97,220/97,220 distinct.
- 66 observed `B_COUNTRY` values; `A_YEAR` spans 2017–2023.
- `I_PSU=-4` remains 31,137 typed user-missing cells.
- `Q152–Q157` retain the accepted first/second-slot counts; W7 second slots `Q153/Q155/Q157` observe `-3` states.
- `Q223`, `Q223_ABREV`, and `Q223_LOCAL` are raw-identical on all 97,220 rows while carrying separate label views.

Disposition: `KNOWN_HAZARD_CLASS__SOURCE_SPECIFIC_FIXTURE_REQUIRED` (reconnaissance only; no certification ruling).

## What actually transfers across WVS

A family fixture may share the **physical invariants**: row-ordinal replay identity; preservation of SPSS user/system missingness; raw-value/label-dictionary separation; ordered-slot identity; country/local scope retention; and no implicit weight default.

It may **not** share native-ID assumptions, numeric missing semantics, country-coordinate bindings, weight roles, or exact question-variable mappings. The identity contradiction alone forbids that: W1 has unique `S007` plus country-scoped `V3`; W4 lacks `S007` and has genuine country+`V3` collisions; W7 again has unique `S007` but a catastrophically noninjective `D_INTERVIEW`.

The first/second-choice topology is structurally reusable, but its code mapping is not. W4 aims second slots do not observe `-3`; W7 aims second slots do. W1 uses `-3` in `V204` but not `V107`. Same apparent topology, different physical code behavior.

## W1/W4 behavior beyond the frozen W7 hostile oracle

W1 and W4 do expose source-specific hostile shapes that the named W7 oracle does not itself exercise: W1's `S007` display-format/raw-magnitude contradiction; W1's eight all-system-missing variables; W4's three all-user-missing variables plus one all-system-missing variable; W4's within-country `V3` collisions; and W4's ordinary country-specific semantic-looking `V218` codes.

These do **not** require a new stable hazard taxonomy. They are covered by existing physical-missingness, identity, semantic-code-candidate, metadata, and raw-vs-display preservation laws. They do require W1/W4-specific hostile fixtures.

## Authority boundary

No label such as “Don't know,” “No answer,” “Not applicable,” “Not asked,” “Missing,” or “Refused” was promoted into a governed semantic state. Weight purpose, design variance, respondent-ID semantics, routing, country-local mappings, and cross-wave concept equivalence remain documentary authority gaps recorded in `AUTHORITY_GAPS.csv`.

No database was consulted. No production/runtime state was modified. No source was certified.
