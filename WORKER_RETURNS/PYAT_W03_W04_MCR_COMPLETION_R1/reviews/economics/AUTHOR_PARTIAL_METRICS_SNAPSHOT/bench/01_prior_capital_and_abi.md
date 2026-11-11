# Bench lane — W03-PREVIOUS-CAPITAL / ABI pin

**Lane:** `pyat-w03-w04-mcr-bench-r1`, existing OpenCode DeepSeek V4.1 Flash MAX.
**Worktree:** `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-w03-w04-mcr-bench-r1`
**Branch:** `agent/pyat-w03-w04-mcr-bench-r1`
**Startup anchor observed:** `a5f21266a91b9b00041a1fbdc6a31d5bc0949fe4` — this anchor contains only the commission/contract files; it deletes the source tree.
**Source anchor used to restore the exact frozen source without semantic change:** `1b0c8dc4c4c6350aa77f70fea9470f5b18aa21dc` (`Restore full pinned source plus exact three MCR contract files`).
**Frozen PR895 source head:** `46b7325637e68f78ccc7487d4b1abc7009c5ac0b`; remote `refs/pull/895/head` readback remains exactly `46b73256`.
**Contract source:** `5a891a311c70f4cb8c09864008b33405362f7c7c`.
**Protected base:** `4f3413fc5c37b589be3412f826bf8f68ee617d4a`.

## Exact source/restore proof

```text
git diff --stat 46b73256..1b0c8dc4 -- rawlsing_next
(empty)
```

Only the three MCR contract files differ between `46b73256` and `1b0c8dc4`; all source blobs remain the frozen PR895 source. The bench implementation adds only the benchmark module, its new test, and its workflow changes.

## Reviewed prior capital retained

| Path | Blob | Status |
|---|---|---|
| `rawlsing_next/_pre553_c11_execution_view.py` | `986f327aa18053edc61bd837cdded02bbf8388d9` | reviewed compact production blob; retained |
| `rawlsing_next/tests/test_pre553_c11_execution_view.py` | `8e8effa58579af0c3326ecd4af7e159947abe4ec` | reviewed paired test blob; retained |
| `rawlsing_next/pre553_source_backed_c11_facade.py` | `7c967b8227a2843971c7cd9f61f3deaa423af866` | frozen PR895 source; unchanged |
| prior review | `9999c0afac5d7d7eb72ad0df602da4b232a49565` | `ACCEPT_FOCUSED_COMPRESSED_BODY_DELTA`; read, not reaccepted |

The reviewed compact body remains the hot selector path; the benchmark does not change it, create a second C11 engine, or reintroduce the P1R1 mutable-reference defect. Protected base `4f3413` has the older execution-view/test blobs (`de561330...` / `ac59e38b...`) and is used only as the explicit protected baseline.

## ABI used by the benchmark

- `ExactPhysicalCellStream` → `project_c11_candidate_from_physical_cells` → `validate_c11_source_release` → `_compact_public_objects` (existing private compact boundary) → `C11Repository` → `CarrierNeutralResearchExecutor.execute_i03/execute_i05`.
- `ParquetC11Carrier.persist/reopen` for the full cold/warm/delete/rebuild matrix.
- Existing `_fixture` sourcefree physical-cell/projection data is reused and extended to narrow/wide/repeat row profiles; no alternative statistical oracle or source-native performance number is invented.
- No production facade/ingest/repository/execution-view/carrier edit.

## Unresolved ABI note

The compact body boundary still has no public separation between object construction and canonical closure hashing. The benchmark records those two stages as `COMBINED_WITH_OBJECTCONSTRUCTION_AT_PUBLIC_CANDIDATE_BOUNDARY` rather than inventing separate measurements. This is a measurement boundary, not a claim of a missing function.
