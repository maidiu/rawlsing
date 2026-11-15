# Sorok P6 PR #779 exact-two documentary repair — implementation return

**Grade:** `DOCUMENTARY_REPAIR_CANDIDATE__SOURCE_READBACK_ONLY__INDEPENDENT_REVIEW_PENDING`
**Original P6 PR #779 head:** `69987ef2741e6f90daede0e9e397aae0ac8e6b0b`
**Protected PRE-MAIN source observed:** `7a5429ffbc48efd25e28c912da80c822e66bc182`
**Repair branch:** `repair/sorok-p6-exact-canonical-and-transcript-redaction-20261108-r1`
**Scope:** no P6 runtime, P5 runtime, world owner, S46, model science, user-profile authority, or protected PRE-MAIN modification.

## Defect 1 — canonical currentness top heading

The unmodified canonical verifier expects the first line of `SOROK_PRODUCT_CONTROL_ROOM/CURRENT_PROGRESS.md` to name `revision39` when its paired JSON is revision 39. The submitted P6 head moved a P6 joined candidate heading to line 1, so three later historical-receiving assertions cascaded RED. The repair restores the original exact R39 first-line heading and places the P6 candidate notice immediately below it. The paired JSON stays revision 39; R37/R38/R39 historical evidence remains. Verified by direct GitHub readback that line 1 now begins `# Sorok current progress revision39`. **Canonical CI must be rerun; local native/shell verifier was NOT_RUN here.**

## Defect 2 — published private paths

Removed personal absolute Mac workspace and ephemeral demo paths from five tracked evidence artifacts:

- `WORKER_RETURNS/SOROK-P6-JOINED-VERIFICATION-20261107-R1/joined_demo/TRANSCRIPT.md`, Git blob `bff4a176bf47911586daf71961f734d18f5367c0` → `1396dbe56f541d451399a0398f83814587a3a59b`.
- `WORKER_RETURNS/SOROK-P6-JOINED-VERIFICATION-20261107-R1/joined_demo/actual_run.jsonl`, blob `fdf6dc66cd9ca1feff4b0b580ab73eeb523987e1` → `4afeef9717b6fcae04483ad01437dd8b43da5ab6`.
- `WORKER_RETURNS/SOROK-P6-COLD-DEMO-20261107-R1/TRANSCRIPT.md`, blob `71e503d12fb8d7b768f7d577ab137d989ff261bb` → `00a9e0f3877e4e18e79c62df8269932e5519f59b`.
- `WORKER_RETURNS/SOROK-P6-COLD-DEMO-20261107-R1/actual_run.jsonl`, blob `3d4a41395020f418069bf4f2b536d3fa60ee56f8` → `3afb0a164b3dc9be325789096d19ea7669e8ffc9`.
- `WORKER_RETURNS/SOROK-P6-JOINED-VERIFICATION-20261107-R1/joined_demo_run.log`, blob `11d64b5c3b3e9bea6d49fc3254dfc623488caafb` → `408b1ba4deed7464f74381805a47a9bd14e94ace`.

The receipt `WORKER_RETURNS/SOROK-P6-JOINED-VERIFICATION-20261107-R1/joined_demo_receipt.json` now separately records raw preimage bytes and SHA-256, and current sanitized bytes and SHA-256. Independently computed original hashes matched the published prior review exactly:

| Evidence | Original raw SHA-256 | Published sanitized SHA-256 |
|---|---|---|
| joined transcript | `88f703c76edc5b5d0da0560390b6f755f5017651c6b9fc92747c58a79fa25885` | `e15343c25ee20bfaa7617acd75a5a0437e091c00e93b1bf391bf7236f14861f4` |
| joined JSONL | `a8ce2e3e4cc2ccda393f062635bc6be077e0fd1d58145659c13bfdc094689756` | `f1588dcb943e63d86a8316c9965fb1b914934b1204b2cbc4d2759e42b6d1d65e` |
| joined house history | `03cf9da0bcf2396ba362b67aa2f10dff2d0f673a0619a0c861b515d9b54fee3f` | unchanged |

Both original and sanitized `actual_run.jsonl` files parse to 13 lines, every exit remains zero, and **all non-command JSON fields are structurally identical** in old vs redacted files, including result, receipt, timing, label and sequencing. Only absolute paths in command arrays changed. No rerun of the 13 commands is asserted.

The remaining `/private/tmp/...` references in independently returned pytest proof markdown identify a temporary Python executable rather than a private home/workspace. They are not altered to avoid rewriting independently reviewed test invocations.

## Exact independent receiving requirements

1. Readback the exact repair HEAD and confirm first-line R39/paired JSON 39 and historical R37/R38/R39 conservation.
2. Verify **unaltered** `PROGRAMMA canonical tree integrity` CI PASS on repair PR.
3. Audit all tracked relevant P6 raw transcript paths, including log; confirm no personal home/workspace locator.
4. Recompute the current published SHA-256 and original preimage SHA-256; confirm byte counts in updated receipt, exact redaction and semantic invariance of both 13-record JSONL sequences. The historical original run bytes are intentionally different.
5. Verify P6 and P5 runtime files are exactly unchanged from independently reviewed candidate, and P6 `PASS_SCOPED` evidence remains valid at its original grade.
6. Keep governed FIABC/LiTS `144 PASS / 3 inherited FAIL` separate from any canonical check outcome. Do not claim global CI green.
7. Return `ACCEPT_SCOPED` or `REVISE` with exact SHA and discrepancies. This repairer is **not** its own independent reviewer.
8. After acceptance, integrate this repair into the **existing P6 PR #779 branch** without rebuilding P6. Merge P5 #775 first into protected PRE-MAIN only on its own qualified receiving; then reconcile P6’s paired progress against the newly protected P5 receiving. Do not silently overwrite it.

**Protected merge:** NOT_PERFORMED. **Native science/human/production grants:** HELD. **T4/S46 Mechanism I:** completely separate; neither fixed nor invalidated by this repair.
