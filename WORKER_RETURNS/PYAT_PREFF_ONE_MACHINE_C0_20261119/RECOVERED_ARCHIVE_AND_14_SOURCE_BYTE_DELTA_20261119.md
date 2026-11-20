# REMONT — actual recovered ZIP/codebook/raw-source bytes, beyond historical recovery (2026-11-19)

**Status:** `SOURCE_BYTES_VERIFIED_BUT_SOURCE_ISSUANCE_AND_CURRENT_SELECTION_HELD`. This is **an additive evidence correction**, not a new programme or source-admission grant. Historical original artifact retrieval ledger already exists with **190 records**: [ORIGINAL_ARTIFACT_RETRIEVAL_LIST.json](ORIGINAL_ARTIFACT_RETRIEVAL_LIST.json) and [human ledger](ORIGINAL_ARTIFACT_RETRIEVAL_LIST.md). Preserve it: its 35 original sources and 70 source-audit locations are broader than this newly verified bytes-only supplement.

## Materialized original archives, hashes and meaning

| Source | Actual byte size | SHA-256 independently calculated | Actual Library locator | Physical evidence |
|---|---:|---|---|---|
| `question_structure_register.csv` **C** | 26,582,238 | `9139c1ab77bf47a872f63ccae7784f3631f03a3e02a936b4ac41e75580c45219` | `/Rawlsing/Evidence/question_structure_register_9139c1ab77bf47a8_18792x69.csv` | 18,792 rows, 69 columns, 562 historical manual-review rows, 35 source-family/wave pairs; recovered original, not a selected current source issuer |
| `complete_36wave_final.zip` | 388,583,537 | `dacbc0ccaed13a15cc09785f9360a67f6fe8d1efb95d3064a2f32d5f103fd589` | `/complete_36wave_final.zip`, `file_000000009ad8822fab6efcc81c540dbc` | 4,907 ZIP entries, 4,382 files, 5,342,956,797 bytes uncompressed, V550 derived shard artifacts; **zero original .sav/.dta, zero QSR, zero FQRA/R14 original/manual response authorities.** Historical Asian Barometer W6 derivative shards **not admitted in CLOSED_35** |
| `FINAL FINAL CODEBOOKS.zip` | 3,876,304 | `476da5b6d9b1375a7a190ec1001f0a0e5102e86bcff862c7fdf05a7991c882db` | `/Rawlsing/FINAL FINAL CODEBOOKS.zip`, `file_0000000023c48212b8f5cdc0eaa6d156` | 99 ZIP entries incl. macOS companion files; **48 actual codebook CSVs**, all independently member-SHA-256 verified: **35 closed-wave codebooks + 13 excluded Asian Barometer W6 main/country codebooks**, no original SAV/DTA |

## Fourteen frozen original source byte matches actually verified

These **actual native Library files**, sometimes under producer filenames rather than frozen normalized names, were materialized and their SHA-256 independently compared with the [frozen 35-source byte inventory](https://github.com/maidiu/rawlsing/blob/5d387a9a8c72c68e6ef87a671d6d486bfd1fc43e/data/ddm_build_copy/vozhd_trii/20260820_pre553_empirical_compiler_activation/SUBSTRATE_RECONSTRUCTION/SOURCE_BYTE_INVENTORY.csv). **14/14 matches**, without asserting oldMac originals were modified or original source rights granted:

- Afrobarometer R1: `/Rawlsing/merged_r1_data(1).sav` (`Afro Barometer Round 1.sav` original).
- Arab Barometer I/II: `/ABI_English.sav`, `/ABII_English.sav` (the second also exists under another name in Library; the verified one is ABII_English).
- Asian Barometer W1: `/Rawlsing/Wave1_20170906.sav`.
- GSS: `/GSS1972.sav`, `/GSS1973.sav`, `/Rawlsing/GSS1984.sav`, `/Rawlsing/GSS1993.sav`, `/Rawlsing/GSS2010.sav`.
- Latinobarómetro 1995/2011/2024: `/Rawlsing/Latinobarometro 1995.sav`, `/Rawlsing/Latinobarometro 2011.sav`, `/Rawlsing/Latinobarometro 2024.sav`.
- South Asia W1: `/Rawlsing/SDSA 2005.sav`.
- WVS W1: `/Rawlsing/WV1_Data_spss_v20200208(1).sav`.

**Other 21 frozen sources**: SHA256 and exact byte sizes preserved in frozen 35-source inventory. Not retrieved/rehash-verified this operation, and not thereby deemed missing. Historical candidate location `~/Desktop/Rawlsing/data/Data/<original_frozen_basename>`, plus already-preserved source handoffs.

## Truly primary semantic bytes also directly verified this operation

- `R14_ACCEPTED_SOURCE_OBJECT_INDEX_R4.csv`: 106,233 B, SHA256 `174de5af9c3bf0fc1929bac87fa8e62ace95b2aeab39c1ff6d718a14ad8194f2` (native Library `file_000000003090822f8e337f4679fc8ef3`).
- `R14_SOURCE_NATIVE_CANDIDATE_INTEGRITY_AUDIT_R3.csv`: 352,871 B, `fa1d4d91692b7e5349657d0e3becd3ee248d8d4a76ceec1dd5238d34843a7fa0` (`file_000000008ee881f7b169181a30dc6311`).
- `WVS Wave 7 (2017) Questionnaire.pdf`: 885,723 B, `5b6b06cb79681c0f5013fcfb93720951a033674b657985944bfcabc9f6a2735b` (`file_00000000da80722f98a132205b69d244`).
- `WVS Wave 7 (2017) Codebook.pdf`: 3,542,402 B, `d13c892099ac6a4681acdad344b81f99d086a5694be94cf5e7a578a62bf02ad3` (`file_00000000e41c722f8d67a0fc93343951`).
- `question_relation_registry_35wave_active_v1.csv`: 1,119,028 B, `a91239a5e630c554d2c397f739a60f1313ea8ab7377780ee3c64f4969e49267b` (`file_000000002ee881fba3c96ce1bf2f3a04`).

## Durable full-list location and hashes

A self-contained, sorted **119-record actual-byte and high-priority-authority inventory** complements, but does **not replace**, the existing broader 190-record historical retrieval manifest. Every record supplies file name, precise byte size or explicit unavailable value, date **and date-type**, SHA256 **and grade**, direct Library/GitHub/oldMac locator and honest owner/state note. All are banked in native ChatGPT Library:

`/Rawlsing/Evidence/REMONT_2026.11.19_FULL_INVENTORY/`

- `REMONT_exact_file_inventory.csv` — 75,981 B / SHA256 `77fbe3628542d43f3cc53a35a7e4908f947e05697173cde0bbefbfd0edcd4f2c`.
- `REMONT_exact_file_inventory.json` — 117,576 B / SHA256 `6a6b404cc79f7b2fee87cac2260ae5340431451c983c1d3790222419b0a60d24`.
- `REMONT_recovery_guide.md` — 16,031 B / SHA256 `dd7daff0cdf96e76a23d28e285e4e087a2e1150375ca5b1b814fe90b926138bf`.
- `FINAL_FINAL_CODEBOOKS_members.csv` — 7,187 B / SHA256 `e8308a67e727ddf99db98917473850d79ac0ad1e72573bb1a4e0af67e14681f4`; **48 individually computed SHA-256 digests**, member timestamps, sizes.
- `complete_36wave_final_contents.csv` — 986,676 B / SHA256 `70ea3091590ce29d575a51afe26997d11d1add32a28787f4d6d4b9f6d650f740`; **all 4,907 archive entries**, exact ZIP member lengths, member dates, CRC32 clearly distinguished from SHA256.
- `REMONT_Exact_Recovery_Inventory_2026-11-19.zip` — 123,316 B / SHA256 `6e439744d321a652d3f0fd3020b8914a341691caf05bbec978d2afe33283b2d9`; packages those five inventories.

The two original uploaded archives themselves **remain stored separately** at root and `/Rawlsing/`; these inventory records don't duplicate or move them. The known historical source-qualified missing link remains **an approved source-specific WVS7 FQRA/R14→C11 response object/occurrence-index/routing authority**, separately Z06 current selection and real U43→I03/Batch/S04 consumer invalidation. A historical frozen file is not a new source grant. **No tests, independent reviewer, leases, scientific-source permission, or protected receiving happened in this recovery tranche.**

## Cold machine instructions

Read both lists (190 historical paths + 119 actual-byte checks) before doing more archaeology. Prefer `SOURCE_BYTES_VERIFIED` over inferred completeness; don't drop 70 source-audit paths from the historical list. QSR version C, R14, WVS7 documentary and 14 original source files **need no user resupply**. Never treat 36-wave derived artifacts or Asian W6 as an accepted source/semantic corpus for CLOSED_35.

**Disposition:** `ACTUAL_ARCHIVE_AND_SOURCE_BYTES_RECOVERED__SOURCE_INSTANCE_C11_ISSUANCE_OPEN__HQ_CURRENTNESS_HOLD`.
