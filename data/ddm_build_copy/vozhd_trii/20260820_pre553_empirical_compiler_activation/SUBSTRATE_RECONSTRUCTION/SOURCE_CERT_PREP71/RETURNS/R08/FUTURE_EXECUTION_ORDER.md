# SOURCE CERT PREP71 — R08 SOUTH ASIA — FUTURE EXECUTION ORDER

Status: `PREPARATION_ONLY__NON_DISPOSITIVE__DO_NOT_CERTIFY`

This is a proposed later source-certification court order. It does not certify either source.

## Shared preflight

1. Pin the future court authority and exact source snapshot before decode.
2. Materialize governed Library `surveys.zip` only; require size `158180333` and SHA-256 `f68d2b33ec0eeb973699963e4c7122d624b99a541b40277e4daed8b87dc9d05f`.
3. Extract only the South Asia member under court.
4. Verify exact member SHA before decode; abort on mismatch.
5. Use the governed SPSS SAV path with user-missing preservation and no South-Asia-specific compatibility encoding override. Preserve raw values, system missing, variable-local user-missing declarations, labels/dictionaries, variable ordinals, row ordinals, and UTF-8 metadata.
6. Never infer semantic state from numeric code, label text, country mask, or observed missingness.

## South Asia Wave 1

Exact source: `surveys/South Asia Wave 1.sav`  
SHA-256: `de7b51f9abf455b072555a84c5592e3ac46bb32c4f9f61bc055160f7d871e571`  
Accepted physical shape: `8442 × 68`; system-missing `6387`; user-missing `14608`.

Execution order:

1. **Source SHA gate** — exact hash above or stop.
2. **Decoder/config gate** — preserve SPSS user-missing declarations and UTF-8 source metadata.
3. **Hostile physical fixtures** — execute W1 fixtures F01–F10.
4. **Mandatory paired missingness proof** — `c12` row 4 code `8` / `No opinion` must remain `FORMAT_USER_MISSING_VALUE`; `b7` row 18 code `8` / `No opinion` must remain `OBSERVED_STORAGE_VALUE`. Any global code-8 classification fails immediately.
5. **Identity gate** — retain `(source_snapshot,row_ordinal)` as replay identity. No native W1 respondent ID is authorized by this packet.
6. **Routing gate** — preserve `c10ai` system-missing and user-missing states exactly; do not convert its country mask into routing semantics without source-native routing authority.
7. **Metadata/topology gate** — preserve the measured negative facts `weight_index=0`, no evident design candidate, and no explicit SPSS MR-set metadata. These facts do not authorize an unweighted estimand or absence of questionnaire topology.
8. **Documentary semantic gate** — before certifying respondent identity, c10ai routing, per-variable semantic response states, weights/design, or complete questionnaire topology, obtain exact W1 questionnaire/codebook/dataset-note/methodology authority. Unresolved items stay `UNKNOWN`.
9. **Carrier/C11 equivalence gate** — prove every source-side physical distinction and every documentary claim actually authorized above survives exact carrier/C11 representation.
10. **Negative/fail-closed fixtures** — reject global numeric missing rules, inferred native IDs, numeric country pooling, inferred unweighted design, and routing inferred only from missingness.
11. **Future disposition gate** — this preparation packet proposes `PACKET_READY__COMPOUND_HOSTILE_COURT_REQUIRED`; only the later authorized court may certify or block.

## South Asia Wave 2

Exact source: `surveys/South Asia Wave 2.sav`  
SHA-256: `6a5329ea16f4546188167edd691e0e6adbeae0737a015470aa26df0e01206f22`  
Accepted physical shape: `10617 × 73`; system-missing `16263`; user-missing `0`.

Execution order:

1. **Source SHA gate** — exact hash above or stop.
2. **Decoder/config gate** — preserve all semantic-like codes as ordinary storage where the SAV declares no user-missing values; require UTF-8 round-trip including U+2019/U+2013 labels.
3. **Identity hostile gate** — execute duplicate `resno` rows 54 and 90 plus Pakistan `resno` system-missing row 6427. `resno` must not replace `(source_snapshot,row_ordinal)` as universal replay identity.
4. **Country-coordinate gate** — preserve exact `ccode` dictionary `1 Bangladesh, 2 India, 3 Maldives, 4 Nepal, 5 Pakistan, 6 Sri Lanka`, including code 3 with zero realized rows. Never reuse W1 numeric country meanings.
5. **Routing gate** — execute GBC27 Nepal system-missing and paired GBC32 Nepal missing/present fixtures. The official Set A rule `Q32 if answered Q31` authorizes the printed generic condition only; it does not explain the merged-file country-specific mask.
6. **Repeated/ranked topology gate** — execute GBC31a/b/c ordered-slot fixture. Preserve First/Second/Third identity and source ordinals independently; no scalar `(respondent,question)` collapse.
7. **Semantic-code physical gate** — execute ordinary code-8 and ordinary `-1` fixtures. Documentary DK/NA wording may enrich semantic state only where explicitly authorized and may never rewrite physical state.
8. **Metadata gate** — execute Unicode, weight/design-negative, and MR-negative fixtures. Absence of SPSS MR metadata does not erase ranked/repeated questionnaire topology.
9. **Documentary semantic gate** — bind official Lokniti Questionnaire Set A only to claims it explicitly prints (Country Code field, `Resp. as in voter list` field, Q31 ranks/codes, Q32 condition/codes). Obtain exact dataset notes/codebook/country-form/methodology before authorizing SAV `resno`, ordinary `-1`, country masks, weights/design, open-ended code dictionaries, or complete merged-release scope.
10. **Carrier/C11 equivalence gate** — require exact preservation of physical state plus only passed documentary-semantic assertions.
11. **Negative/fail-closed fixtures** — reject `resno` as universal ID, W1 country-code reuse, global semantic-code rules, generic missing normalization, inferred unweighted design, or item equivalence from label similarity.
12. **Future disposition gate** — this preparation packet proposes `PACKET_READY__COMPOUND_HOSTILE_COURT_REQUIRED`; only the later authorized court may certify or block.

## Cross-wave fail-closed law

The future court must preserve, before any harmonization: zero exact/casefolded variable-name overlap; `v1 → ccode` coordinate drift; shifted country code meanings; W1 user-missing declarations versus W2 none; recurrent response-code state drift; W2 ordinary unlabeled `-1`; W2 ranked Q31 structure; routing masks; and source-specific labels/dictionaries. Family lineage is not item/value equivalence authority.
