# MANIFEST — ZAK04S_CODEX_CAMPAIGN_R1

**Return root:** `UNIFIED_LOG_R1/ZAK04S_CODEX_CAMPAIGN_R1/`
**Status:** one bounded documentary checkpoint, S0/S1 static source only.
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
