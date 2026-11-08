# C7 — commands and independently checked evidence

**Surface/method:** authenticated GitHub connector for immutable `fetch_file(ref=SHA)`, `fetch_blob`, `fetch_commit`, remote branch readback, and local read-only `git ls-remote` attempt. Independent data parsing and SHA-256 were computed over the exact returned UTF-8 contents in a JS isolate. No code/test/data probe executed; no respondent/SAV/DTA/DB touched. SHA-256 implementation self-test `abc` → `ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad` passed.

## Reproducible read-only checks / results

- `github_fetch_commit(ad4fe3c9cd67eed5bc79644bb399a7090846a8fe)` → 12 fan-in files 00–10 + CHECKPOINT. `github_fetch_commit(483f2a156d2156eeed22f31efc23a05b9335219d)` → only 09 and CHECKPOINT changed. Prepared branch readback of both blobs equals prepared cut: 09 `f9e3d64b15c8f2d1ac46f937f1815ca9bf22b7b0`, CHECKPOINT `3f8a6828888a9c86ba15683f956ecc17e15e47b3`.
- Fetch 00–10/CHECKPOINT at **content ref** `ad4fe3c9c`, not a later branch. JSON parse 51 newline-delimited `03` objects and compare ID sets to 51 `02 CASE` and 51 `05` rows: 51 unique each, symmetric differences empty; `case_family` 1/2/10/2/7/29. `forward_walk`, `reverse_walk`, `exact_hold`, `frozen_taxonomy_verdict` all nonempty. A–J values nonempty except I on 10 C6 records.
- TSV parse with delimiter `\t`: `01` 93 data rows, 23 columns, zero width failures; types 29 FUNCTION/58 RELEASE/6 DENOMINATOR. `02` 149 rows, 12 columns, zero width failures; 51 CASE/26 FF_REGISTER/16 FF_DEPENDENCY/15 POST_FF_REGISTER/11 POST_FF_SEAM/30 748_CURRENT_OWNER. `05` 51 rows, 10 columns, zero width failures. `08` 42 rows, 11 columns, zero width failures.
- Fetch P1 source import: 154 JSONL rows partition 26 FF +16 FF dependency +15 post-FF +11 seams +29 F1 +30 #748 +27 B5. Identity set comparison to `02`: all 26/16/15/11/30 source IDs present, no extras (normalizing `native_identity_fields`). Fetch P1 historical estate by Git blob `93a15c5d8ac46b5cc389c70031c45d4a41fd837b` because path fetch returned empty for the 3.43 MB blob: 1608 valid JSONL rows, partition 58/27/27/228/581/687. This was Git blob read, not local file/source execution.
- Fetch corrected C1–C6 author cases at their exact 09 cuts (1/2/10/2/7/29 = 51), independent `00_REVIEW.md`/`01_FINDINGS.jsonl`/`02_COMMANDS_AND_EVIDENCE.md` at exact review cuts, and correction files (C1/C2/C4/C6 `06`; C3/C5 `07`). Compare C1/C5 original A–J and forward/reverse exactly to fan-in: zero field differences. C3 A–J verbatim; 29 C6 `grade` and F1 counts match fan-in `01`.
- C6 29 author case `f1_callsite_count_228` values sum 228; 58 C6 release rows vs fan-in 58 release rows: SHA, selected bytes, row rules and exact gap fields all agree except fan-in's 16 explicit `NO_SELECTED_SHA` placeholders for source blank unresolved releases. C6 runtime status 58/58 `NOT_RUN__NO_ORIGINAL_RESPONDENT_OR_SOURCE_BYTE_EXECUTION`. `01` states 42 selected-state and 16 unresolved; 38 single-file/row SHA plus four member-set `SET:` digests.
- `03` C6 field I: count = 29; 19 populated with A02 historical acceptance/hold statuses, 10 empty: F13/F14/F15/F16/F18/F21/F26/F27/F28/F29; no I contains `NOT_RUN`. This is not inferred from prose.
- `07` contains A01–A17 once each, all preserved open and none called CLOSED. `CHECKPOINT.goal_complete=false`, `stage=HQ_FANIN_DRAFT_COMPLETE_INDEPENDENT_REVIEW_PENDING`; 0 `SEVERED_PROVED` and 0 `QUALIFIED_EQUIVALENT_PROVED` in tax counts.
- Protected `7a5429ffbc48efd25e28c912da80c822e66bc182` static source range fetch: `pre553_source_backed_c11_facade.py:440-555` contains `project_c11_candidate_from_physical_cells`; `pre553_j_role_certification.py:1005-1035` contains `build_j_validator_registry`; `wave1_r5_q86_c11_projection.py:320-348` contains `GT12-A-R5-Q86-SOURCE-SEMANTICS`. `rawlsing_next/source_configuration/factory.py` 404 at protected ref, consistent with C5 producer/receiving seam (not proof of missing C11 function). These are sampled exact static ranges, not exhaustive verification.
- Local read-only command attempted: `git ls-remote https://github.com/maidiu/rawlsing.git refs/heads/agent/pyat-hq-pre-forge-to-prev3-authority-severance-functional-adequacy-20261107-r1` → failed `fatal: could not read Username for 'https://github.com': No such device or address`. This does **not** count as successful direct `ls-remote`. Authenticated connector branch lookup, immutable branch ref file fetch and later compare/readback are the available verification substitute; final return should disclose this method exception.

## SHA-256 of exact content-head fan-in files (independent UTF-8 digest)

| File | SHA-256 |
|---|---|
| `00_EXECUTIVE_REAL_OPERATIONS_AND_VERDICT.md` | `68133725ea79f3f92e0818cc6dc4c13296f3c147bd0e699b01325c8cca066823` |
| `01_LEGACY_SELECTED_AUTHORITY_USE_AND_INCOMPLETE_CALLEE_COVERAGE.tsv` | `a9f8c9d9af9f73bd48982eeb9556f03d89e183414ed164588f930278e3f8a84d` |
| `02_CURRENT_IMPLEMENTATIONS_PRE_FORGE_VS_WHOLE_PREV3.tsv` | `253bf4453b84ab769bb62672e8c805652cef7803dd6ba07ea4723a00578e9849` |
| `03_BIDIRECTIONAL_FUNCTION_AUTHORITY_CASES.jsonl` | `8f8b3919ef149a8836cd5f25bc0d6c2e777f5a1339d8611f7f2231c50a43b3d1` |
| `04_PROVED_EQUIVALENCES_AND_NO_BUILD_DECISIONS.md` | `b56c997a59a38fd4d326ba21c213be5966cb319ea0522c483379015ce0815ead` |
| `05_SEVERED_OR_INCOMPLETE_MINIMAL_OWNER_REPAIRS.tsv` | `c0e840650069a1dbf29f17af64785262331cef7b052204de4a760d5ec0ba282d` |
| `06_REAL_LOCAL_TEST_COMMANDS_OUTPUT_HASHES_AND_MUTATIONS.md` | `5be23983c960ba74952789cac2999ee6ccb78d0498157f2d2416956da7446c4c` |
| `07_SECONDARY_AGENDA_NON_DROP_AND_WORKER_COLLISION.md` | `ffe887b7c69824cf3ba98e21b54ea4473a1a33e8a7fc60cc7d198a2932e7e1c2` |
| `08_COVERAGE_DENOMINATORS_COLD_HANDOFF.tsv` | `bc8698ba2c40e6ae8a74be180cc97b28e7614dd24b170d5fc7ec25d0d6df15d5` |
| `09_INDEPENDENT_REVIEW_REQUEST_AND_EXACT_HEAD.md` | `ca169f65990166d0b0eba41c25065be06563715afd0014a4628f19206b7c2733` |
| `10_HQ_PRIORITY_AND_NEXT_WORK.md` | `a641ed474e64ad36e747a51165ed58c5e81c2136ccaa6a99efd2f69a4e43ddf9` |
| `CHECKPOINT.json` | `90ffdf55fe33b030e46d01db56880bf00bb7c34f8b2231f5ccb708d3814de621` |

These are content-head digests, not prepared metadata head digests for 09/CHECKPOINT. Git blob SHAs from file readbacks are recorded separately. No claim of local filesystem execution, repo tests or S3 is made.

## Adjudication rule

Treat C7-001–005 as reporting/schema corrections requiring HQ owner adjudication. Preserve the source-court positives and negative/NOT_RUN limits. No successful direct shell `ls-remote` or new test execution is claimed. Return branch write constrained to `C7_HQ_FANIN_INDEPENDENT_REVIEW/` only.
