# CLOSED35-L2-AFR9 — Afrobarometer Round 9 Documentary Authority Closure

Repository: `maidiu/rawlsing`

Base: `agent/vozhd-premain-fiabc-s35-fanin-r1@770d95c1a604ea1f47ac2971b923673c14c42984`

Worker branch: `agent/rabochii-closed35-l2-afrobarometer-r9-authority-r1`

Canonical source: `Afro Barometer Round 9.sav`

Canonical SHA-256: `3afcecd08d2f4b531a926d455a943084d9f71c1276b4f3a58e77a9162e6879d8`

Terminal:

`CLOSED35_L2_AFROBAROMETER_R9_DOCUMENTARY_AUTHORITY_PARTIAL__EXACT_UNKNOWN_SET_RETURNED`

## Holding

Round 9 documentary authority is materially improved but not completely closed.

The official Round 9 producer record closes the source-semantic meaning of the previously blocked Q78F declaration, the Q118 response structure and 9996 terminator, Q47C code 94, and the old/new within-country weight succession. It does **not** close three exact-release identity/routing questions and one exact raw-carrier role question strongly enough to authorize a fully semantic source-specific realization.

No source execution, raw-carrier opening, measured P2X, or numeric role inference was performed.

## Governing inheritance

This return consumes the S35 HQ and Authority71/72 holdings without modifying them:

- exact source identity is the canonical SHA above;
- accepted physical truth includes an unexercised Q78F user-missing declaration `-1`, eleven physical Q118 slots, ordinary stored `9996`, and four physically distinct old/new weight carriers;
- physical order, labels, missing declarations, and carrier identity survive even when semantic authority is absent;
- weight names/distributions are not role authority;
- source documentation may close semantics but may not erase contradictory exact-source physical facts.

## Producer-authority findings

### 1. Q78F = -1

**Semantic meaning: CLOSED.**

Official Round 9 country codebooks identify Q78F as the item asking about the economic and political influence of the European Union/EU on the respondent's country. The Ghana Round 9 codebook, for example, defines Q78F as `Influence of the EU on Ghana`, codes the substantive scale 1–5, and explicitly gives `-1 = Missing`. The Sudan Round 9 codebook documents the same question family with country-local coding.

The Round 9 Survey Manual independently defines `-1` as the standard missing-data code.

**Applicability/routing: PARTIAL.**

Q78F is demonstrably an actual Round 9 administered item in multiple official country releases (including Ghana, Sudan, São Tomé and Príncipe, and Eswatini). Q78F itself is not documented as conditional on Q78D/Q78E in the Ghana/Sudan codebooks; Q78E, by contrast, carries an explicit Q78D gate.

However, the merged 39-country Round 9 codebook used by Authority71 omits Q78F, and no official Round 9 master routing matrix recovered in this court enumerates the exact set of merged countries for which Q78F is applicable. Therefore:

`Q78F_MEANING = CLOSED`

`Q78F_-1 = MISSING`

`Q78F_EXACT_MERGED_COUNTRY_APPLICABILITY_SET = UNKNOWN`

No adjacency-based inference from Q78A–E is authorized.

### 2. Q118 topology

**Question structure: CLOSED AS MULTIPLE RESPONSE, NOT RANKED.**

The Round 9 Survey Manual explicitly identifies Q118-type items as multiple-response questions and instructs use of `9996 = no further reply` when there is no further response.

Official Round 9 country codebooks define the slots as repeated spoken-language fields — `first`, `second`, `third`, etc. — and repeatedly state that the interviewer was instructed to **tick all that apply**. This is a repeated/multiple-response serialization, not a preference ranking.

The slots therefore preserve:

- slot identity;
- slot ordinal/storage position;
- multiplicity;
- country-specific language dictionaries;
- ordinary terminator/special codes independently of physical missingness.

They must not be flattened or deduplicated.

**9996: CLOSED at Q118 scope.**

For Q118, `9996` means `No further reply` / `No further response`. It is an ordinary stored special-response value, not SPSS system missing and not the Q78F user-missing declaration.

The Survey Manual's generic Round 9 special-code law distinguishes:

- `96/996/9996` = no further answer for multiple-response questions;
- `94/994/9994` = not asked in country;
- `-1` = missing data.

**Slots 1–10: DOCUMENTED.**

The merged Round 9 codebook documents Q118 through `Q118_10` and then `Q118OTHER`. Country codebooks show that the number of realized language slots varies with country-local language topology.

**Slot 11: UNKNOWN AT EXACT ROUND-9 DOCUMENTARY GRAIN.**

The accepted canonical SAV contains `Q118_11` as an eleventh physical slot. No exact Round 9 official codebook, questionnaire, release note, or data dictionary recovered by this court documents `Q118_11`. Exact public searches for `Q118_11` / eleventh-slot labels returned no Round 9 producer hit.

Earlier Afrobarometer rounds contain analogous eleventh spoken-language slots, but cross-round continuity is not admissible as exact Round 9 authority.

Therefore:

`Q118_1..Q118_10 = DOCUMENTED_MULTI_RESPONSE_SLOTS`

`Q118_11 = PHYSICAL_SLOT_PRESERVE_OPAQUE__EXACT_R9_SEMANTIC_BINDING_UNKNOWN`

The physical ordinal of a slot must not be interpreted as respondent preference, priority, or rank.

### 3. Q47C = 94

**Meaning: CLOSED.**

The Round 9 Survey Manual explicitly defines the 94-family as:

`94 / 994 / 9994 = Not Asked in Country`.

This resolves the exact semantic class of the accepted ordinary Q47C raw code `94`.

Country instruments independently prove actual Q47C country-routing use. The official Angola Round 9 questionnaire marks Q47C `NOT ASKED IN ANGOLA` and supplies Angola-specific replacement questions; other Round 9 country codebooks likewise document country-local Q47C substitutions.

Therefore, at this field/code scope:

`Q47C=94 => NOT_ASKED_IN_COUNTRY`

This remains an ordinary stored semantic special code. It must not be converted to physical missing merely because it is a non-substantive applicability state.

No claim is made that code 94 has identical semantics outside the producer's Round 9 special-code regime or that every variable exercises it.

### 4. Weight roles and succession

The producer documents an actual Round 9 weight succession.

The Round 9 Survey Manual states that Afrobarometer expanded its weighting calculation to account for household size through `ADULT_CT`; the **new** weight is labeled `withinwt_hh` and is the weight that **must be used for analysis**, while the previous weight is retained and relabeled `withinwt_ea`.

Thus the conceptual within-country succession is closed:

`OLD EA-LEVEL WITHIN-COUNTRY WEIGHT = withinwt_ea`

`NEW HH-LEVEL WITHIN-COUNTRY WEIGHT = withinwt_hh`

`ROUND 9 ANALYTICAL SUCCESSOR = withinwt_hh`

The sampling/weight documentation further distinguishes use:

- within-country weights are for national descriptive estimates;
- `COMBINWT`-class weights equalize country sample contribution for merged multi-country descriptive estimates;
- the Round 9 Survey Manual cautions against activating WITHINWT/COMBINWT for inferential relationship analysis.

Later official Afrobarometer codebooks make the family design explicit as four logical weights: `withinwt_ea`, `withinwt_hh`, `combinwt_ea`, and `combinwt_hh`. This later-round evidence is corroborative family continuity only; it is **not** admitted as an exact Round 9 raw-name alias map.

### 5. Exact raw weight-carrier bindings

The exact canonical SAV physically exposes `WITHINWT`, `V397_A`, `COMBINWT`, and `V399_A` as distinct carriers in accepted Authority71 evidence.

Public exact-release producer documentation recovered here establishes the logical old/new weight roles and succession, but does not name the short raw carriers `V397_A` or `V399_A`.

Accordingly:

- `WITHINWT`: producer legacy protocol plus Round 9 succession law establishes the old within-country EA-level role sufficiently for role-level realization.
- `COMBINWT`: producer protocol establishes the combined cross-country descriptive role, but the exact old/new EA-vs-HH variant represented by the canonical short carrier must not be inferred beyond documented/raw-native metadata.
- `V397_A`: accepted source-native label points toward the new HH-level within-country weight, but no official public Round 9 alias binding `V397_A -> withinwt_hh` was recovered. **UNKNOWN exact alias.**
- `V399_A`: no official public Round 9 alias/role binding was recovered. It must not be silently treated as `combinwt_hh`. **UNKNOWN exact alias and exact role.**

Numeric inspection is explicitly inadmissible and was not used.

## Exact UNKNOWN set

The remaining documentary unknown set is exactly:

1. `Q78F_EXACT_MERGED_COUNTRY_APPLICABILITY_SET`
2. `Q118_11_EXACT_ROUND9_PRODUCER_BINDING`
3. `V397_A_EXACT_ROUND9_ALIAS_BINDING`
4. `V399_A_EXACT_ROUND9_ALIAS_AND_ROLE_BINDING`

Q47C=94 is no longer in the unknown set.

Q118's multiple-response character and 9996 meaning are no longer in the unknown set.

The old-EA/new-HH within-country succession is no longer in the unknown set.

## Admission consequence

A later source-specific realization may lawfully:

- bind Q78F to EU influence and `-1` to Missing;
- preserve Q78F applicability as UNKNOWN outside exact country authority until a merged routing map is supplied;
- realize Q118_1..Q118_10 as ordered storage slots of one multiple-response spoken-language surface;
- preserve Q118_11 as an opaque eleventh physical slot without invented semantics;
- bind Q118 `9996` to No further reply while keeping it physically ordinary;
- bind Q47C `94` to Not Asked in Country while keeping it physically ordinary;
- encode the producer's old-EA/new-HH weight succession at the logical-role layer;
- refuse to select `V397_A` or `V399_A` semantically until exact producer alias authority is supplied.

A later realization may **not**:

- delete Q78F's unexercised declaration;
- infer Q78F country applicability from missingness or adjacency;
- infer Q118_11 from Q118_10, Q118OTHER, or earlier rounds;
- interpret Q118 slot position as preference/rank;
- collapse 9996 into physical missing;
- infer weight roles from numeric distributions;
- bind V397_A/V399_A from source labels alone when exact producer alias authority is the governing burden.

## Public producer sources admitted

- Afrobarometer, *Round 9 Survey Manual*, July 2022: https://www.afrobarometer.org/wp-content/uploads/2022/07/AB_R9.-Survey-Manual_eng_FINAL_20jul22.pdf
- Afrobarometer, *Merged Round 9 codebook — 39 countries*: https://www.afrobarometer.org/survey-resource/merged-round-9-codebook-39-countries-2023/
- Afrobarometer, Ghana Round 9 codebook: https://www.afrobarometer.org/wp-content/uploads/2024/05/GHA_R9.Codebook_21May24.final_.pdf
- Afrobarometer, Sudan Round 9 codebook: https://www.afrobarometer.org/wp-content/uploads/2024/05/SUD_R9.Codebook_13May24.final_.pdf
- Afrobarometer, Angola Round 9 questionnaire: https://www.afrobarometer.org/wp-content/uploads/2023/06/ANG_R9.-Indigenised-questionnaire_13Feb22_final.docx.pdf
- Afrobarometer, Angola Round 9 codebook: https://www.afrobarometer.org/wp-content/uploads/2024/10/ANG_R9.Codebook_28Jun24.final_.pdf
- Afrobarometer, Nigeria Round 9 codebook: https://www.afrobarometer.org/wp-content/uploads/2024/05/NIG_R9.Codebook_15May24.final_.pdf
- Afrobarometer, Zambia Round 9 codebook: https://www.afrobarometer.org/wp-content/uploads/2024/06/ZAM_R9.Codebook_4Jun24.final_.pdf
- Afrobarometer, Seychelles Round 9 codebook: https://www.afrobarometer.org/wp-content/uploads/2024/07/SEY_R9.Codebook_13Jun24.final_.pdf
- Afrobarometer sampling/weighting guidance: https://www.afrobarometer.org/surveys-and-methods/sampling/
- Afrobarometer, *Weights Protocol*: https://www.afrobarometer.org/wp-content/uploads/2022/04/Afrobarometer_Weights_Protocol.pdf

## Proof boundary

This is a documentary-authority return only.

No local raw survey carrier was opened.

No source execution was performed.

No measured P2X was run.

No source certification is claimed beyond the exact semantic bindings explicitly closed above.
