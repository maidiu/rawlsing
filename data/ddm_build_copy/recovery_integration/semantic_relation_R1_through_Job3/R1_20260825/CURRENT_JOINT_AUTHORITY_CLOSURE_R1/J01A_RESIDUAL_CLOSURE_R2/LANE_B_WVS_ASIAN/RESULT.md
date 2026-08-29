# J01-A R2 LANE B — WVS / ASIAN BAROMETER CURRENT-ONLY RETURN

Status: `BLOCKED__NO_SUCCESS_TOKEN`

Jurisdiction executed only for WVS W1/W4/W7 and Asian Barometer W1/W4/W5. No sibling R2 branch or historical J carrier was admitted.

## Terminal finding

This lane cannot lawfully emit a certified R2 source-structure universe, candidate universe, or exact R1 lineage. The hard blocker is not a negative substantive finding; it is loss of the exact frozen R1 carrier payload named by the command. The command-authorized Library aliases now resolve to different bytes than the frozen R1 manifest.

Frozen source carrier required by the command:
- SHA-256 `47913a300402b65e4fd92197220ced0195b6b50704679e3cc088d15604d4b7ad`
- 253,503 bytes
- 299 rows

Current payload behind that Library alias during this court:
- SHA-256 `de4a097b1059be2c398ed0eef5876f308a37e38c0fc315d936b42213d1ba8ba7`
- 394,454 bytes
- 439 parsed data rows

Frozen J-candidate carrier required by the command:
- SHA-256 `3fe61d274c4b0d78c9b1ba142709125831a4c7d8e3418e0a69fc257879b743f9`
- 216,925 bytes
- 257 rows

Current Library path is 288,879 bytes; the materialized payload checked during this court hashes to `329840cc555b791c1cebca8328a317009d5ce201c4b60e72edec1900923ac550` with 328 parsed data rows.

The original manifest-bound file IDs could not be materialized from the current Library surface. Because shared R2 authority requires every R1 lane row to be accounted for exactly once, reading the mutated alias as if it were the frozen baseline would consume uncommanded later content and violate sibling blindness. Therefore it was rejected.

## WVS W1 crosswalk result

`SAFE_NATIVE_TO_CURRENT_MEMBER_CROSSWALK = UNRESOLVED`

Positive current evidence demonstrates why same-number mapping is forbidden:
- native `WVS Wave 1 (1981) Questionnaire.pdf` SHA `199bb069...` has `V111` as the leisure-time relaxing-versus-active item;
- current `WVS Wave 1 (1981) Codebook.pdf` SHA `80ceb7ef...` has `V111` as `Future changes: Less emphasis on money and material possessions`;
- current WVS deep catalog SHA `cc538e72...` binds current W1 `V111` to `question_impl.phase0.678c69fb141c9abed7a7` with that future-changes meaning.

The current official WVS longitudinal documentation explicitly lists `WVS Time Series List of Variables and equivalences 1981 2022 v3.1 (Excel)`. That is the correct class of current authority for W1 identity, but the actual workbook/mapping payload was not recoverable through the governed Library/web surface in this run. No positional, ordinal, same-number, label-only, or neighboring-wave substitution was used.

## Asian Barometer recovery result

W1 current locator recovery succeeded at the file-identity level: the governed locator ledger names `CoreQs-May25rev.doc`, `Wave1_codebook_20170327.txt`, and `Wave1_20170906.sav`; the current official Asian Barometer site also confirms the First Wave core questionnaire is downloadable. Exact W1 questionnaire/codebook bytes were not materialized, so no hash-bound W1 source structure was certified.

W4 native source recovery is strong: `ABS4_Core_Questionnaire.pdf`, SHA `5be5ed726287f83c6bf723ae563e434f7d17f623e630b31b6ba1b92d2cdcbba0`, was rendered and text-extracted over all 44 pages. Numerous explicit respondent-facing multi-member/ranking blocks are directly present.

W5 current native source existence was recovered more strongly than R1: the official current `CoreQ_W5.pdf` is directly reachable as a 44-page PDF, and the governed locator ledger names `CoreQ_W5_R1.pdf`, `ABS5_Core_Questionnaire_20190805.pdf`, and `20230505_W5_merge_15_codebook.pdf`. The binary could not be locally materialized for SHA binding, so deterministic source-hash identity was not certified.

No exact current `Rawlsing_P2_Asian_Barometer_*Deep_Question_Node_Catalog*.csv` was recovered by exact-title/locator-ledger search. Absence is not inferred; exact current member binding therefore remains open for W1/W4/W5.

## Carrier decision

The two required R2 carrier CSVs are emitted as schema-only placeholders with **zero certified data rows**. Zero is not asserted as the lane universe count. `COUNTS_R2.json` marks both certified counts `null`; `VALIDATION_R2.json` marks carrier and lineage validation false. This avoids turning an input-integrity failure into a fake substantive answer.

## Required next authority

To resume this lane without violating the command, SUB-VOZHD must restore or provide the exact frozen R1 carrier payloads bound by `CARRIER_MANIFEST.json` (or an independently authenticated byte-identical copy), and provide/recover the actual current WVS equivalence workbook plus the exact current Asian deep catalog if available.

Success token **not emitted**.
