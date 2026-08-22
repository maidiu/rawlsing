# SOURCE CERT PREP71 — R03 ASIAN BAROMETER PACKET RETURN

Status: `PREPARATION_COMPLETE__NON_DISPOSITIVE`  
Worker: `SOURCE-CERT-PREP71-R03`  
Branch: `agent/vozhd-trii-srcprep71-r03-asian`  
Exact starting HEAD: `0ac2a8c00ca5718f293e98f98be6685f67ea2445`

This return prepares later source-equivalence courts for Asian Barometer Waves 1, 4 and 5. It does **not** issue a source-certification verdict.

## Identity and transport gates

`surveys.zip` was materialized from ChatGPT Library file `file_0000000036e0822f963b9604cb2bad49` into worker-private scratch. The bundle is exactly `158180333` bytes with SHA-256 `f68d2b33ec0eeb973699963e4c7122d624b99a541b40277e4daed8b87dc9d05f`. Only the three assigned substantive members were extracted.

| source | bytes | SHA-256 | fixtures | packet disposition |
|---|---:|---|---:|---|
| W1 | 3451655 | `ac0b8bc1ddb2fa6b952417e35b6379ce6a2cf8596776a43282ba44f48e0ae1a2` | 9 | `PACKET_READY__COMPOUND_HOSTILE_COURT_REQUIRED` |
| W4 | 7735596 | `4d914817509d0e5f3adde49707df148f696992055937f085080a016002a39200` | 9 | `PACKET_READY__SOURCE_SPECIFIC_HOSTILE_COURT_REQUIRED` |
| W5 | 10688196 | `2576e428ff8de3c8d93a418c9120a1c2955ab7b1f35961d8c18fa562bc4b5e63` | 13 | `PACKET_READY__COMPOUND_HOSTILE_COURT_REQUIRED` |

Accepted SR03 physical-manifest hashes were independently recovered from the accepted checkout package: W1 `b607ce2dc5991a7320812b1d77362da3456aa6d80f9389cd9697ffba81377177`, W4 `06b55f0e53c67bb45a295edcee9507d87737cdabb6de4b539ed8747d1dab9694`, W5 `0a492240cbdf7d91b2e247fbddc556c4cf34214486235912f88b16fd79d7636f`. No full-cell source rescan was performed.

## W1 packet

W1 is an explicit encoding exception: `BIG-5`, not UTF-8. Its packet freezes 199 variables with SPSS missing ranges, 284,794 user-missing cells, 720,729 system-missing cells, q001 user-missing replay, q018_1 system-missing replay, country-scoped native identity, W1 geography, all nine weight candidates, and the q097 first/second/third topology. The later court must fail if a family UTF-8 default is applied.

Library/browser document search did not recover the exact W1 source-native questionnaire/codebook bytes. The official ABS site confirms the First Wave core questionnaire exists, but that listing is insufficient to close W1 response semantics, routing, or weight design. Those are named authority gaps, not reasons to reinterpret raw labels.

## W4 packet

W4 is independently prepared: UTF-8, zero SPSS user/system missing cells, ordinary `-1` values labeled `Missing`, country+id injectivity local to this release, 14-country + 84-region-code coordinates, `w` and `w_cross`, ordered q20/q21/q22 and q99/q99a/q99b, and q172 ASEAN-only routing text.

Library source-native `ABS4_Core_Questionnaire.pdf` explicitly identifies q99/q99a/q99b as first/second/third problem responses and q172 as “ASEAN countries only.” It also exposes a critical data-vs-instrument distinction: the questionnaire SE1 country-code order differs from the merged SAV raw country dictionary for codes 3–8. The packet therefore preserves both, with the raw SAV dictionary governing replay and the questionnaire remaining documentary evidence pending an explicit merged-data mapping authority.

## W5 packet

W5 is a compound hostile packet: UTF-8, zero physical missing cells, ordinary `-1` sentinels, two duplicate Hong Kong `(COUNTRY, IDnumber)` pairs, raw-vs-instrument geography drift, one weight candidate, general and India-only ranked problem modules, q186 ASEAN-only routing, and **three distinct native MR sets**.

The native MR topology is frozen exactly:

- `IR3a`: dichotomy, counted value `1`, members `IR3a_1..IR3a_5`;
- `Q112`: dichotomy, counted value `1`, members `SE15A..SE15M`;
- `SE15`: dichotomy, counted value `1`, members `SE15A..SE15O`;
- overlap: `Q112 ∩ SE15 = SE15A..SE15M`.

Distinct set identities are part of the source evidence. A later carrier/C11 court must prove both Q112 and SE15 survive separately; overlapping members are **not** authority to deduplicate sets.

The official W5 core questionnaire strengthens the guard rather than collapsing it: it documents SE15 as the A–O household-asset battery and separately documents questionnaire item 112 as an ethnic-equality/governance statement. Thus the **native SPSS MR-set name `Q112` cannot be semantically identified with questionnaire question 112 merely by string equality**. The packet preserves the set name literally and names a merged-data/codebook authority gap for its semantic alias.

The same core questionnaire marks q186 “ASEAN countries only,” but India-only Q106c/d/e are absent from the common instrument. ABS’s own release policy says country-specific variables require country-team authority, so the India module remains explicitly documentary-blocked for semantic/routing assertions.

## Family reuse boundary

Reusable across this family: raw-byte identity gate; source SHA + row ordinal replay identity; preservation of raw values, system/user-missing machinery, labels/dictionaries, every weight candidate, repeated-slot order, and native MR metadata when present.

Not reusable by assumption: encoding; missing-code semantics; native-ID uniqueness; country/region coordinates; weight roles; label/value-code dictionaries; variable ordinals; routing risk sets; or MR set topology. W1, W4 and W5 each have source-specific hostile fixtures for those dimensions.

## Named future-certification blockers

There are 15 explicit authority gaps. The principal blockers are: exact W1 questionnaire/codebook/routing/weight authority; W4 merged-data country-code reconciliation, ordinary `-1` semantics, exact q172 risk set, and weight methodology; W5 native-ID authority, merged country-code reconciliation, ordinary `-1` semantics, the Q112 MR-set semantic alias, India country-team module authority, exact q186 risk set, and weight methodology. None changes the frozen physical-carrier contract.

Frozen-contract contradiction found: **no**.  
User local source directory used: **no**.  
WVS70 touched: **no**.  
Full source scans performed: **no**.

Token: `PRE553_SOURCE_CERT_PREP71_R03_RETURNED`
