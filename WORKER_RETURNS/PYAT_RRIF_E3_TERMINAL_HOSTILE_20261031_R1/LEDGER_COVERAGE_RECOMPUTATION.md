# RRIF-E3 ledger coverage recomputation

Pinned sources: HQ ce84f0596121ffa707cb751f99364bf580ef1c63; D1 3f6fc7b7c7ee49dc502537b2b50314eb18159905; D2 7f592959e6631d9ed7c3cb7defbe1a11ea7ed2ec; D3 a897ad3d6105d6ce24d0821be1fe2a8fdea2f553; D4 57e22a5c04adca78184df9099616ab65415411f6; D5 7a241a80ec327c9e49b33659fd3630a27aaf4ede; RRIF-C b75addf621c3a6c1a3b196bd92a810fad77ae3ae; RRIF-V bec050449f0b38606718e4e9691caa1721fcd94f; PRE-MAIN 8e44ca9c751049d65e6def47600b5c073ee04b29.

| Unit | Count | Evidence grade |
|---|---:|---|
| HQ 30-case JSONL | 30 unique | Direct S1 parse |
| D1–D5 | 5 × 6 = 30 unique | Direct S1 parse, set and exact disposition equality |
| RRIF-C lineages | 34 unique | Direct S1 parse, 30 subset and four remainder |
| Frozen branch names/tips | 845 / 838 | RRIF-C validator report, not new recensus |
| Code-branch rows | 321 | RRIF-C validator report |
| Code-introducing/inherited review | 155 / 166 | RRIF-C validator report |
| Original variants/families | 3135 / 1885 | Preserved original ledger; no invented branch authorship |

The four previously accounted C lineages are LIN-C1_03A_STATE_ROUTE, LIN-C1_03R_REPLAY_LIFECYCLE, LIN-C1_03_JOIN, LIN-V2K_ORIGINAL_IDENTITY. They include the C1-03 integration/test grouping. Each of the 30 JSONL lines provides original source SHA and line-precise locator, original worker negative and current source/consumer classification, HQ named owner/wake, and adversarial E3 challenge.

## R157 denominator bridge not proved

RRIF-V: **34** code deltas on final-review branch, **4 exact / 6 modified / 24 absent**. RRIF-C lineage row: **19** union introduced paths, **0 exact / 2 modified / 17 absent**. D2: **19 absent**, no `source_configuration` directory or `pre553_source_read_admission.py`. RRIF-C ACCOUNTED_FOR_CODE_BRANCHES.jsonl recomputation: five R157 code-introducing branch rows with introduced-blob counts **5+15+5+2+5 = 32**, across **19 distinct paths**. The 34,32,19 may count different branch comparison vs lineage-introduction vs unique path identities; **the exact crosswalk was not furnished**. This is a finite R157 historical defect, not reason to recount 845 branches. Require an explicit 34→32→19 per-path table, mark tests/fixtures/overlap and resolve two falsely modified paths. Never call original35 config scientifically retired merely because no current external importer.

## Reproduction recipe (S1)

Fetch the HQ 30-line JSONL at its pinned SHA; fetch D1–D5 six-line JSONLs at exact return SHAs; parse as JSONL; assert five groups of six, each ID unique, exact HQ/worker proposal pair equality; fetch C 34-line JSONL, assert uniqueness and 30 subset; compare retained four. Read RRIF-C denominator JSON and RRIF-V counts as reports only. No S3/source-native or local pytest executed by E3.
