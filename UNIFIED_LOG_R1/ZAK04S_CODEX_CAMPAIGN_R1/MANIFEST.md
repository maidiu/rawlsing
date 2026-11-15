# MANIFEST — ZAK04S_CODEX_CAMPAIGN_R1

**Return root:** `UNIFIED_LOG_R1/ZAK04S_CODEX_CAMPAIGN_R1/`
**Status:** one bounded documentary checkpoint, S0/S1 static source only, plus the ZAK1057 round2 exact documentary correction (derivative branch; original return `ba20eeeea2243edd71febe0af0bc184d1cfeef1e` preserved immutable).
**Model/session:** `opencode-go/deepseek-v4.1-flash#max`, session `ses_e22bd21eeffeH5GWvx2XBKwSEw`.
**Source cuts:** protected `6a5c12f04323d74001f9632063ec907f4fc4468e`; historical `1f1c72f883d0d7a6d11d7df8bad75c37d06c3ffa`; predecessor `1428c2e92bce1a49efd87378cb23df936d646dc5`; consumer `016870e86913e6f7a811a51db6aba2d741bcfe58`; PDEV01 `aa18b6b8547c954d844bb0dcf94f70e2e14f15b0`.

## Files

| File | Records | Purpose |
|---|---:|---|
| `00_RETURN.md` | 1 | Commission answer, five grades, findings, holds, terminal sentence |
| `HUMAN_STORY.md` | 1 | Readable narrative and case pointer |
| `SCOPE_CONTRACT.md` | 1 | Two-axis scope, assignment sentence, boundaries |
| `FINDINGS.tsv` | 1 | One seam/T record (cross-reference, not a new canonical T) |
| `OPERATION_TRACES.tsv` | 7 | Producer B, predecessor A, F6P, I07 guard, WP2 port, retracted false lookup, protected N9 read |
| `AUTHORITY_USE.tsv` | 4 | Permission-only guard, test-only consumer, test port, producer ceiling |
| `EVIDENCE.tsv` | 24 | Exact commit/blob/path/line evidence rows, including corrected enumeration |
| `COVERAGE.tsv` | 10 | 6 inspected, 4 NOT_INSPECTED cells |
| `UNJOINS.tsv` | 9 | Numeric reader, schema mismatch, guard vs producer, variant rule, bounded absence, unsearched eras, authority, name collision, N9 source vs F6 consumption |
| `MECHANISM_RECONCILIATION.tsv` | 7 | Old mechanism to current operation comparisons, including N9 synthetic non-reader |
| `SOURCE_SEARCH_LOG.tsv` | 15 | Positive, negative, corrected full-enumeration and N9 reads |
| `REVERSE_CONSUMERS.tsv` | 5 | F6P, I07, WP2, protected N9, protected HEAD reverse traces |
| `DATA_SHAPES.tsv` | 12 | In/out shapes for B, A, F6P, guard, WP2, protected N9 |
| `SOURCE_STRATUM_QUEUE.md` | 6 tracts | Finite queue with DONE/HELD/QUEUED states |
| `CASES/ZAK04S_F6M_F6P_CURRENT_RECEIVER.md` | 1 | Standalone required T case |
| `CHANGED_FILES.txt` | 1 | Actual published file list |

## ZAK1057 round2 correction

- **Authority for correction:** independent review `9666515a5a2e349a3ab93635e4f0de40f91d6d36:UNIFIED_LOG_R1/ZAK1057_ROUND2_INDEPENDENT_REVIEW/CASES/ZAK1057-REVIEW-04-F6-MISSING-SHARE.md` and HQ source-confirmed erratum `2780d148d695f339f49b4dddbdf70648776e588d:WORKER_COMMISSIONS/ZAKONCHILOS_CODEX_HQ_RECON_CAMPAIGN_R1/HQ_ACTIVATION_20261114/ROUND2/04_ROUND1_EXACT_ERRATUM.{json,md}`.
- **Corrected claim:** the predecessor adds the whole target-stratum share to `uncovered` only when **no source is eligible** (`if not denom: uncovered += share`). When some planned sources are ineligible but at least one is eligible, it renormalizes weights onto survivors, assigns no uncovered mass to the excluded present source, and may emit a complete distribution; F6P's excluded-source-with-zero-uncovered `FALSE_FULL_COVERAGE` check is the relevant downstream risk. The repaired candidate computes `denom` over all planned sources, retains proportional `missing_share`, and adds it to `uncovered`; for partial ineligibility the predecessor has zero uncovered mass while the repaired candidate has positive uncovered mass.
- **Files corrected:** `00_RETURN.md` (§1, §2.2), `CASES/ZAK04S_F6M_F6P_CURRENT_RECEIVER.md` (§3, §7, §10), `HUMAN_STORY.md`, `DATA_SHAPES.tsv` (`ZAK04S:SHAPE:R1:B_IN`, `ZAK04S:SHAPE:R1:A_IN`), `OPERATION_TRACES.tsv` (`ZAK04S:OP:R1:BEFORE_A`, plus the repaired `BEFORE_B` negative wording), `MECHANISM_RECONCILIATION.tsv` (`ZAK04S:MECH:R1:001`), `UNJOINS.tsv` (`ZAK04S:UNJOIN:R1:004`), `EVIDENCE.tsv` (`ZAK04S:EV:R1:005`), plus this manifest, `MANIFEST_SHA256.tsv`, and `HQ_RECEIVING_NOTE.md`.
- **Preserved:** repaired-F6M output, F6P static-reader/refusal findings, I07 permission-guard distinctness, protected N9 synthetic-candidate scope, world-serving alternative, and the bounded `NOT_PROVED` current F6 receiver status.
- **Ceiling:** this is author-side documentary correction, not independent acceptance. The original lane04 `REVISE` verdict remains recorded pending receiving; no product code, runtime, science, source/actor authority or protected branch is touched.

## Integrity statement

- All TSV files are UTF-8 with literal header rows and no embedded tabs in fields.
- Evidence IDs are unique within this return and do not overwrite prior `ZAK04:*` or `R5:*` IDs.
- No code, test, script, CI or production file was modified. No execution of Rawlsing scientific functions occurred.
- `NOT_FOUND` rows are bounded to the declared symbol/path scope at the named commit. They are not global absence claims. The earlier empty N9 wildcard result is retracted and retained only as historical counterevidence (EV020).
- The protected N9 source is present; its F6 numeric consumption is `NOT_PROVED`, not absent. The F6P static reader is not a selected N9 reader. The I07 guard is not a numeric producer. The PDEV01 WP2 port is branch-test-only.

## Known unfinished cells

1. ZAK00 owner matrix `e725ec39...` read via `git show`; ZAK-04 jurisdiction and no-zero-loss/no-native limits recorded in EV024. Earlier file-path denial corrected, not a source gap.
2. R35 F6C full A/A0/B comparative and substitution receipt: HELD.
3. Pre-Vozhd/Vozhd/Verkhovod/Dva/Trii/Chetiri/Long Memory: NOT_INSPECTED.
4. Current SOROK P3/P5/P6 F6 receiver: NOT_INSPECTED.
5. Protected N9 file read; deeper N9/N10W producer input contract and alternate symbols: NOT_TRACED.
6. Independent reviewer: NOT_ASSIGNED.

## HQ receiving supplement

HQ_RECEIVING_NOTE.md records exact source-search retraction, count normalization and scope ceilings. MANIFEST_SHA256.tsv hashes the current documentary payload and excludes itself. Both are documentary-only intake additions.
