# SOURCE CERT PREP71 — R03 FUTURE EXECUTION ORDER

Status: `NON_DISPOSITIVE_PACKET__DO_NOT_CERTIFY_HERE`

This file orders the later source-equivalence courts. It does not execute or close them.

## Asian Barometer Wave 1

1. **Source identity gate** — require SHA-256 `ac0b8bc1ddb2fa6b952417e35b6379ce6a2cf8596776a43282ba44f48e0ae1a2` and byte size `3451655`; fail closed on mismatch.
2. **Decoder/config gate** — SAV native path, source-reported `BIG-5`, no compatibility override, preserve raw values, value labels, variable labels, SPSS system missing, SPSS user-missing declarations/values, storage/display metadata, and row ordinal. **A UTF-8 family default is a failure.**
3. **Hostile physical fixtures** — replay `W1_Q001_USERMISS_98`, `W1_Q0181_SYSTEM_MISSING`, and the source-wide typed-missing totals without converting either state to row absence.
4. **Metadata/topology fixtures** — replay `W1_ENCODING_BIG5`, country/level3 coordinates, all nine weight candidates, and q097 first/second/third slot order.
5. **Documentary semantic assertions** — bind exact W1 questionnaire/codebook authority for user-missing semantics, country-specific routing, and weights/design. Until obtained, labels are evidence but not semantic closure.
6. **Exact carrier/C11 equivalence assertions** — every source row remains replayable by `(source SHA, row ordinal)`; each tested raw cell retains physical state + raw value + source metadata separately from semantic interpretation.
7. **Negative/fail-closed fixtures** — reject UTF-8 substitution; reject global idnumber uniqueness; reject dropped user-missing cells; reject inferred routing from system missingness; reject any default weight.
8. **Future disposition gate** — only the later authorized source court may issue a certification-level disposition.

## Asian Barometer Wave 4

1. **Source identity gate** — require SHA-256 `4d914817509d0e5f3adde49707df148f696992055937f085080a016002a39200` and byte size `7735596`.
2. **Decoder/config gate** — SAV native path, source-reported `UTF-8`, no compatibility override; preserve all ordinary values even when labels read `Missing`.
3. **Hostile physical fixtures** — replay q1 `-1` as `OBSERVED_STORAGE_VALUE`; verify zero physical system/user-missing cells.
4. **Metadata/topology fixtures** — replay W4 row identity, raw country + region coordinates, w/w_cross, q20/q21/q22, q99/q99a/q99b, and q172.
5. **Documentary semantic assertions** — source-native `ABS4_Core_Questionnaire.pdf` binds q99 slot labels, q172 wording/domain, and generic SE1 instrument country codes. Bind a merged-data codebook before reconciling the **different** SAV country dictionary or assigning `-1` semantics. Bind sampling/weight documentation before analytical weight assertions.
6. **Exact carrier/C11 equivalence assertions** — raw SAV geography remains source coordinate authority; questionnaire code lists remain documentary evidence and may not overwrite raw values.
7. **Negative/fail-closed fixtures** — reject inheritance of W1 BIG-5, W5 MR topology, W5 ID collisions, questionnaire-SE1 recoding of raw country, `-1 -> physical missing`, or a default weight.
8. **Future disposition gate** — later authorized source court only.

## Asian Barometer Wave 5

1. **Source identity gate** — require SHA-256 `2576e428ff8de3c8d93a418c9120a1c2955ab7b1f35961d8c18fa562bc4b5e63` and byte size `10688196`.
2. **Decoder/config gate** — SAV native path, source-reported `UTF-8`, no compatibility override; preserve ordinary sentinel codes and all native MR metadata exactly.
3. **Hostile physical fixtures** — replay IR11d `-1` as ordinary storage and the duplicate Hong Kong country+ID fixture.
4. **Native MR topology court** — require all three distinct sets exactly:
   - `IR3a`: dichotomy, counted value `1`, members `IR3a_1..IR3a_5`;
   - `Q112`: dichotomy, counted value `1`, members `SE15A..SE15M`;
   - `SE15`: dichotomy, counted value `1`, members `SE15A..SE15O`;
   - exact overlap: `Q112 ∩ SE15 = SE15A..SE15M`.
   The later court must prove that **both Q112 and SE15 survive as separately addressable native sets**. Member overlap is not deduplication authority.
5. **MR documentary guard** — `CoreQ_W5.pdf` documents SE15 A-O and IR3a as multiple-answer. It also documents questionnaire item 112 as an unrelated governance statement. Therefore the raw native MR set name `Q112` is preserved literally but **must not be semantically equated to questionnaire item 112** without a merged-data construction/codebook authority.
6. **Other metadata/topology fixtures** — raw country/region domain vs observed support, w, q106/q106a/q106b, India-only Q106c/d/e, and q186.
7. **Documentary semantic assertions** — bind W5 merged-data geography mapping, sampling/weight methodology, ordinary `-1` semantics, exact q186 risk set, fieldwork ID authority, and India country-team questionnaire/routing authority.
8. **Exact carrier/C11 equivalence assertions** — source SHA + row ordinal remains replay identity; duplicate native IDs do not collide; MR set identity/membership/order/count value survive; raw/core country-code disagreement survives as two explicit evidence layers.
9. **Negative/fail-closed fixtures** — reject MR-set deduplication by overlapping members; reject Q112-name semantic inference; reject `-1 -> physical missing`; reject country+ID as universal key; reject generic CoreQ country recoding of raw SAV; reject default weight; reject inferred India/ASEAN routing from missingness alone.
10. **Future disposition gate** — later authorized source court only.

Token: `PRE553_SOURCE_CERT_PREP71_R03_RETURNED`
