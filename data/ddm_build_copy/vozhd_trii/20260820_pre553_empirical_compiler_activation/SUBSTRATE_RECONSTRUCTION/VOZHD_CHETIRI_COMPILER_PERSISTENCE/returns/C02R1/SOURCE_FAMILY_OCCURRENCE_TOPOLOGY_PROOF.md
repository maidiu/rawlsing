# VC4 C02-R1 — SOURCE-FAMILY OCCURRENCE/TOPOLOGY PROOF

Status: `INCOMPLETE_BY_EXACT_SOURCE_UNAVAILABILITY`
Disposition: `C02R1_BLOCK__EXACT_SOURCE_UNAVAILABLE`

## Proof burden

For every identity-bearing C11 M04/M05 occurrence/topology fact across the current exact 35-source corpus, C02-R1 must establish one of two things:

1. an exact FD from immutable source evidence + frozen decoder semantics + existing governed variable/question/topology/routing authority, including reconstruction, complete scope, exhaustive exception law, integrity binding, and ExactRef/C11 replay closure; or
2. the smallest exact additional governed material required where the fact is not so determined.

The court may not infer either answer from storage layout, implementation shape, majority behavior, or an unknown exception set.

## Complete governed corpus

- SAV sources: 31
- DTA sources: 4
- total: 35

Family counts:

- Afro Barometer: 3 source(s)
- Arab Barometer: 4 source(s)
- Asian Barometer: 3 source(s)
- EVS: 5 source(s)
- GSS: 8 source(s)
- Latinobarometro: 3 source(s)
- LiTS: 4 source(s)
- South Asia: 2 source(s)
- WVS: 3 source(s)

The checked-in inventory binds expected bytes and SHA-256 for every member. Those expected hashes are reproduced in the source registry below; no row is presented as an execution-time source-hash receipt.

## Existing accepted physical evidence

Accepted SR03 established a 35-source physical census and physically declared native SAV multiple-response metadata, including 18 MR sets across:

- `Asian Barometer Wave 5.sav`
- `EVS 2008.sav`
- `EVS 2017.sav`

That is relevant physical evidence that multiplicity/topology metadata exists in the governed corpus. It does **not** prove the semantic occurrence FD required here. SR03 itself does not authorize `source cell = semantic occurrence`, and C02/C06 expressly left the U5/M04/M05 seam open.

## Frozen generic law

Across SAV/DTA, the source constitution and decoder contract preserve source row/variable identity and physical format distinctions. Authority 56 binds:

`EVENT_GRAIN_UNLESS_EXACT_FD_CERTIFICATE`

and rejects carrier/source-cell position as a standalone semantic occurrence certificate.

Candidate determinants for the required facts are enumerated in the 525-row matrix. Candidate determinants are not certificates.

## Required-fact registry for the 525-row matrix

`M04_M05_FD_CERTIFICATE_MATRIX.csv` is normalized as 35 source indices × 15 fact codes. Source identity/hash metadata is defined in the source table below; field semantic ownership/determinants/authority are defined here.

| code | required fact | M | semantic owner | smallest candidate determinant set | governing authority |
|---|---|---|---|---|---|
| F01 | `source_release_identity` | M04 | source/release authority | immutable source snapshot identity + governed release manifest | 09_SOURCE_NATIVE_CONSTITUTION.md; 52_POST_R4...; SOURCE_BYTE_INVENTORY.csv |
| F02 | `source_row_respondent_replay_coordinate` | M04 | source replay owner | exact source snapshot identity + deterministic decoder row ordinal | 09_SOURCE_NATIVE_CONSTITUTION.md; 52_POST_R4... |
| F03 | `native_variable_identity` | M04/M05 | source-native metadata owner | exact source snapshot + frozen decoder variable ordinal/name + instrument release | 09_SOURCE_NATIVE_CONSTITUTION.md; 10_FORMAT_DECODER_CONTRACT.md |
| F04 | `canonical_question_identity` | M04/M05 | question binding authority | native variable identity + exact governed question binding/version | 52_POST_R4...; pre553_c11_integrity.py QuestionVariableBinding |
| F05 | `component_identity` | M05 | question/topology authority | native variable/question identity + exact component/subitem binding + topology authority | 52_POST_R4...; pre553_c11_integrity.py QuestionVariableBinding |
| F06 | `event_group_id` | M04/M05 | C11 occurrence/topology owner | respondent replay coordinate + question binding + exact occurrence grouping law/material | 56_POST_R4... EVENT_GRAIN_UNLESS_EXACT_FD_CERTIFICATE; accepted C06 U5 |
| F07 | `response_event_id_or_deterministic_index` | M04 | C11 occurrence owner | respondent replay coordinate + native variable/question + exact occurrence/index law/material | 56_POST_R4...; accepted C02 M04; accepted C06 U5 |
| F08 | `semantic_occurrence_slot_identity` | M04/M05 | C11 occurrence/topology owner | event group + component/slot/selection/rank/order determinants + exact topology authority/material | 09_SOURCE_NATIVE_CONSTITUTION.md; 56_POST_R4...; accepted C02/C06 |
| F09 | `multiplicity` | M05 | topology authority | question/component binding + source-native multiplicity metadata + exact topology authority/material | 09_SOURCE_NATIVE_CONSTITUTION.md; 10_FORMAT_DECODER_CONTRACT.md; 56_POST_R4... |
| F10 | `rank_order` | M05 | topology authority | occurrence/slot identity + source-native rank/order evidence + exact topology authority/material | 09_SOURCE_NATIVE_CONSTITUTION.md; 56_POST_R4... |
| F11 | `repeated_event_identity` | M04/M05 | occurrence/topology authority | respondent/question identity + repeated-event discriminator + exact topology law/material | 09_SOURCE_NATIVE_CONSTITUTION.md; 56_POST_R4... |
| F12 | `multiple_response_component_selection_identity` | M05 | topology authority | MR-set/component metadata + respondent/question + selection occurrence + exact topology law/material | 10_FORMAT_DECODER_CONTRACT.md; SR03 accepted physical census; 56_POST_R4... |
| F13 | `topology_identity` | M05 | topology authority | question/component binding + native topology declarations + event-specific topology determinants | 09_SOURCE_NATIVE_CONSTITUTION.md; 10_FORMAT_DECODER_CONTRACT.md; 56_POST_R4... |
| F14 | `occurrence_keys_in_c11_identity_content_hash_exactref` | M04/M05/M18 | C11 identity/replay owner | all semantic occurrence/topology determinants entering canonical semantic projection | 52_POST_R4... M18; 56_POST_R4...; pre553_c11_integrity.py ExactRef/replay law |
| F15 | `routing_applicability_altering_occurrence_existence` | M04/M05/M07 | routing/topology authority | respondent/question/source scope + exact routing/applicability rule/fact + occurrence law | 52_POST_R4... M07; 56_POST_R4... |

Matrix status vocabulary:

- `access=P`: `NOT_PROBED_AFTER_TERMINAL_COMPLETE_SCOPE_STOP`.
- `access=U`: `UNAVAILABLE_AT_EXECUTION__BLOCKING` (only source index 34, WVS7).
- `fd=A`: `NOT_ADJUDICATED__COURT_STOPPED_ON_REQUIRED_SOURCE_UNAVAILABLE`.
- `fd=B`: `UNRESOLVED_BLOCKING__EXACT_SOURCE_UNAVAILABLE`.
- `det=C`: `CANDIDATE_DETERMINANT_SET_ONLY__NOT_CERTIFIED`; resolve the exact candidate set from the fact registry above.
- `recon=X`: reconstruction function `NOT_EXECUTED / NOT_CERTIFIED`.
- `exc=X`: exhaustive exception law `NOT_ESTABLISHED`.
- `integrity=E`: expected inventory SHA is bound in the source registry below, but no execution-time raw SHA/read occurred.
- `replay=U5`: ExactRef/C11 occurrence replay closure `NOT_CERTIFIED__C06_U5_OPEN`.
- `minmat=N`: exact minimum additional occurrence/topology material `NOT_ADJUDICATED`.

Every matrix row resolves `(source_index, fact_code)` through the source registry and fact registry in this proof; no code means “unknown by implication.”

## Complete-scope execution result

The proof court could not enter raw-source execution because one mandatory source was unavailable:

`WVS Wave 7.sav`
expected SHA: `2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d`

Its explicitly authorized transport `WVS Wave 7.sav.zip` was also unavailable on accessible source surfaces.

The governing C02-R1 law says:

`If exact sources are unavailable, BLOCK rather than infer.`

Accordingly, no source-specific occurrence/topology metadata or values were opened for any source after the complete-scope gate failed. Other inventory members are not labeled unavailable; they are simply unprobed in this court after the terminal witness.

## Source-by-source proof state

| # | source | family | format | expected SHA-256 | C02-R1 source state |
|---:|---|---|---|---|---|
| 1 | `Afro Barometer Round 1.sav` | Afro Barometer | sav | `6c9869a7cc7321cc74efb708835e21c8b65286a25c76deac45aba84d75697ee2` | `NOT_PROBED_AFTER_COMPLETE_SCOPE_STOP` |
| 2 | `Afro Barometer Round 5.sav` | Afro Barometer | sav | `c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651` | `NOT_PROBED_AFTER_COMPLETE_SCOPE_STOP` |
| 3 | `Afro Barometer Round 9.sav` | Afro Barometer | sav | `3afcecd08d2f4b531a926d455a943084d9f71c1276b4f3a58e77a9162e6879d8` | `NOT_PROBED_AFTER_COMPLETE_SCOPE_STOP` |
| 4 | `Arab Barometer Wave 1.sav` | Arab Barometer | sav | `2a48ba4b2f23d022a2dfe4b8a0cc685febbd82579b5434f9ecd96ed4c1243d18` | `NOT_PROBED_AFTER_COMPLETE_SCOPE_STOP` |
| 5 | `Arab Barometer Wave 2.sav` | Arab Barometer | sav | `6529841b97bd56463490d810ad24ceaa4866066d12e4651a7081682d413606a1` | `NOT_PROBED_AFTER_COMPLETE_SCOPE_STOP` |
| 6 | `Arab Barometer Wave 5.sav` | Arab Barometer | sav | `6a5cbad637ce1546833a1d4812ba6d1e8d75f85b5b199b0cf3ec5cf456068dbc` | `NOT_PROBED_AFTER_COMPLETE_SCOPE_STOP` |
| 7 | `Arab Barometer Wave 8.sav` | Arab Barometer | sav | `a5e83a953f03dd890e076a51da473051f1cfd1ca2e8ab93c2172eeb2517af998` | `NOT_PROBED_AFTER_COMPLETE_SCOPE_STOP` |
| 8 | `Asian Barometer Wave 1.sav` | Asian Barometer | sav | `ac0b8bc1ddb2fa6b952417e35b6379ce6a2cf8596776a43282ba44f48e0ae1a2` | `NOT_PROBED_AFTER_COMPLETE_SCOPE_STOP` |
| 9 | `Asian Barometer Wave 4.sav` | Asian Barometer | sav | `4d914817509d0e5f3adde49707df148f696992055937f085080a016002a39200` | `NOT_PROBED_AFTER_COMPLETE_SCOPE_STOP` |
| 10 | `Asian Barometer Wave 5.sav` | Asian Barometer | sav | `2576e428ff8de3c8d93a418c9120a1c2955ab7b1f35961d8c18fa562bc4b5e63` | `NOT_PROBED_AFTER_COMPLETE_SCOPE_STOP` |
| 11 | `EVS 1981.sav` | EVS | sav | `5b703173845c086382fd93252f1cbc91dfef74007755459adfc73785389172f2` | `NOT_PROBED_AFTER_COMPLETE_SCOPE_STOP` |
| 12 | `EVS 1990.sav` | EVS | sav | `66252a92c59bf6759b79a6b35b2be658b98a433373212a70c8ec94755d3e02ec` | `NOT_PROBED_AFTER_COMPLETE_SCOPE_STOP` |
| 13 | `EVS 1999.sav` | EVS | sav | `6058644a9308aad574b95fa0afd1b026fedea289c6c95aca043aefb41ae0ab8a` | `NOT_PROBED_AFTER_COMPLETE_SCOPE_STOP` |
| 14 | `EVS 2008.sav` | EVS | sav | `5469e3b39cbbb6d7230ff9894426cc75fe074541d284633235df4af3442ac379` | `NOT_PROBED_AFTER_COMPLETE_SCOPE_STOP` |
| 15 | `EVS 2017.sav` | EVS | sav | `95096c2474b81ef12004726e4ed5b0919b1ea7bb672baff676ae40fb1b629bd2` | `NOT_PROBED_AFTER_COMPLETE_SCOPE_STOP` |
| 16 | `GSS1972.sav` | GSS | sav | `e368fc0f1d141b201900185c919c48ab1de1c4c7815bccf83a6e4fb224293204` | `NOT_PROBED_AFTER_COMPLETE_SCOPE_STOP` |
| 17 | `GSS1973.sav` | GSS | sav | `59e65801dc26818bbcf15f9ed985cf8f1faafa65a3eb59e2d3180a7b13a5c1c2` | `NOT_PROBED_AFTER_COMPLETE_SCOPE_STOP` |
| 18 | `GSS1984.sav` | GSS | sav | `1da2df0c0e0692817081a46856deeaa6c78891101e53cf0139a971de16f7ac18` | `NOT_PROBED_AFTER_COMPLETE_SCOPE_STOP` |
| 19 | `GSS1993.sav` | GSS | sav | `7fc409cc07172f9a556bf88c5df8d2ea5e539b2a6ff37348711eeb21b4355ae8` | `NOT_PROBED_AFTER_COMPLETE_SCOPE_STOP` |
| 20 | `GSS2002.sav` | GSS | sav | `8ece381105237a1800051eec3617dad9dd05bf137e34fa833653464a58222be1` | `NOT_PROBED_AFTER_COMPLETE_SCOPE_STOP` |
| 21 | `GSS2010.sav` | GSS | sav | `c229aff7430c12f246678f385e0776b089681ae9830bac88423e0964ac34ee05` | `NOT_PROBED_AFTER_COMPLETE_SCOPE_STOP` |
| 22 | `GSS2016.sav` | GSS | sav | `a053bdc5661eb2c1dd9a2d3a5d054601c66955a178fb266be9cef1023aea9b07` | `NOT_PROBED_AFTER_COMPLETE_SCOPE_STOP` |
| 23 | `GSS2024.sav` | GSS | sav | `27166a481ba6e240aca68293464a2b1fd9a9171a3ddba89a038038a32b8d1eef` | `NOT_PROBED_AFTER_COMPLETE_SCOPE_STOP` |
| 24 | `Latinobarometro 1995.sav` | Latinobarometro | sav | `4b7fc6da17dfddafd6a835717e8dc06981208eb4120fa33bdd16e12ae95926f7` | `NOT_PROBED_AFTER_COMPLETE_SCOPE_STOP` |
| 25 | `Latinobarometro 2011.sav` | Latinobarometro | sav | `a44e89e08e564e4e175199eeeabfa6163f32f4ba0a19a6c3f5b4752de6cca22e` | `NOT_PROBED_AFTER_COMPLETE_SCOPE_STOP` |
| 26 | `Latinobarometro 2024.sav` | Latinobarometro | sav | `ff5cef18c87969026e7f993d09f10c38a547bf81d5d398784fb59b960b7b0a40` | `NOT_PROBED_AFTER_COMPLETE_SCOPE_STOP` |
| 27 | `LiTS_II.dta` | LiTS | dta | `c43d0e1821c51398817d7dfdfad2c0a4a5bb0d492f6a58096670e623bb6130e9` | `NOT_PROBED_AFTER_COMPLETE_SCOPE_STOP` |
| 28 | `LiTS_III.dta` | LiTS | dta | `368ae5d07a44975a2f0a9ce3b1e564988a966b2632e28075c56a24d60065bcc8` | `NOT_PROBED_AFTER_COMPLETE_SCOPE_STOP` |
| 29 | `LiTS_IV.dta` | LiTS | dta | `14e1032755c4f42d8d3dc61647097ccd7605ba281551e53953c76d22a223cd1c` | `NOT_PROBED_AFTER_COMPLETE_SCOPE_STOP` |
| 30 | `South Asia Wave 1.sav` | South Asia | sav | `de7b51f9abf455b072555a84c5592e3ac46bb32c4f9f61bc055160f7d871e571` | `NOT_PROBED_AFTER_COMPLETE_SCOPE_STOP` |
| 31 | `South Asia Wave 2.sav` | South Asia | sav | `6a5329ea16f4546188167edd691e0e6adbeae0737a015470aa26df0e01206f22` | `NOT_PROBED_AFTER_COMPLETE_SCOPE_STOP` |
| 32 | `WVS Wave 1.sav` | WVS | sav | `051bf450568f44181559a5b2bfbe58b4f05b58bc806643d0c63353c937ff0824` | `NOT_PROBED_AFTER_COMPLETE_SCOPE_STOP` |
| 33 | `WVS Wave 4.sav` | WVS | sav | `c6757ed187655c8b9af88ae4c23c00f066696a641af2f316b4343272ea1d4a0a` | `NOT_PROBED_AFTER_COMPLETE_SCOPE_STOP` |
| 34 | `WVS Wave 7.sav` | WVS | sav | `2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d` | `UNAVAILABLE_AT_EXECUTION__BLOCKING` |
| 35 | `LiTS_I.dta` | LiTS | dta | `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09` | `NOT_PROBED_AFTER_COMPLETE_SCOPE_STOP` |

## Exact conclusion

C02-R1 cannot certify:

- a complete source-backed FD;
- a complete named non-derivable exception/material set;
- a sparse exception set;
- or irreducible full-event persistence.

The smallest exact non-derivable material is therefore **not adjudicated** here.

The only lawful finding is the execution-evidence block:

`CLOSED35_REQUIRED_SOURCE_WVS7_UNAVAILABLE_AT_COURT_EXECUTION`

A future rerun with every exact source available must begin again at the source gate, hash-verify before each read, then settle the determinant/exception domain without using this block as evidence for either architecture.
