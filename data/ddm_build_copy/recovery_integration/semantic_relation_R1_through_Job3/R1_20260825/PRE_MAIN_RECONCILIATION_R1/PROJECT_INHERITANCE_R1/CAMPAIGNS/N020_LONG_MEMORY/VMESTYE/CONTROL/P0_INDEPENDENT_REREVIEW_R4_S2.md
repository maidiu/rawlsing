# VMESTYE ZL-P0R R4 — independent receiving of corrected ZL-01 and clean S2 return
Date: 2026-11-08 (America/New_York); source records carry 2026-11-09 UTC.
Formal verdict: **REVISE**. ZL-01 source-key correction **PASS at S0–S1**, S2 execution logs materially improved and clean negatives independently read, but S2 receipt and validator assertions retain three concrete defects. **NO `ACCEPT_P0_SCHEMA_AND_ESTATE`, NO P1 ZL-02–ZL-14 release, NO protected merge.**
Prior R1 REVISE, R2 HOLD, and R3 REVISE are independent immutable historical events; R4 appended only.

## Immutable reviewer subjects
- Protected `integration/pre-main-reconciliation-r1@2162d85db5e6822707e5cdff7aac2656ebef4761`: unchanged.
- ZL-00 PR #819 `11047708a6e4b4050da351f4b6cc35f03cb8269b`: draft/unmerged; prior schema/lease S0–S1 checks retained.
- Corrected ZL-01 PR #820 `353adc216a832a6c41ccc99f77cb3b53651af64e`: draft/unmerged.
- Corrected S2 worker PR #826 `83192fcc998c2cf57899a4fc388dd5343df542a4`: draft/unmerged.
- Reviewer PR #821 R3 prior head `caefb06bb73e1bc58033794184069337c6847e71`; R4 additive files on same isolated reviewer branch.
- Historical D05 source `b7dd1bce667651c88ddd71c17c065f2b33ec38ec::data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/LONG_MEMORY_CURRENT_ZERO_LOSS_DELTA_R1/D05_MAINTENANCE_LIFECYCLE/AUTHORITY_MAINTENANCE_FUNCTION_LEDGER.csv#blob=bf77b70f1858697ce663f2eeec2e91e25aa6ac94`.
- Actual reviewer surface: ChatGPT authenticated GitHub connector, S0–S1 source/log examination plus read-only raw-source SHA256 parsing. **No mainMac S2 re-execution by this reviewer.** Worker reports `mainMac.lan`, Python 3.11.3, `opencode-go/deepseek-v4.1-flash`, effort not exposed and independent runner credential attestation not claimed. No S3/native/science/actor rights.

## Positive ZL-01 source-key receiving — PASS S0–S1
Direct full blob read of `CONTROL/P0_RETURN_AND_BRANCH_CENSUS.tsv` Git blob `65c1bbe4a602341c5caacca2d58dced31a23f382`:
- **6,125** source identities ×25 fields, every retained-negative/status nonempty and zero repeated five-field source identity.
- Diff against exact prior 6,120-row census blob `ace431dde03fde7aa124c351d2549b6e9b2b587b`: all old 6,120 source identities preserved; exactly `ZL01-006121..006125` / `D05-F07..F11` added. Only pre-existing D05-F06 changed `source_read_depth` and `negative_status` to explicit malformed CSV field-semantic hold; no other prior row changed.
- D05 grouped now **29**, D05 maintenance file **11**, D02–D07 per-file total **369**; all 23 per-file anti-join selectors and total 110 anti-join checks match claimed input/output counts, no duplicates. 111 coverage receipts source/output digests and counts internally match. This is documentary source identity, not independently rehashed 111 receipt digests by this reviewer.
- Exact 11 D05 raw physical source records at original ordinals 2–12 independently checked against new `CONTROL/P0_D05_RAW_SOURCE_QUALIFICATION.tsv` blob `55d15d59f2c2ad060f715296523daca2f1b49d82`: **11/11 SHA256 hashes match original bytes including newline**, each source identity/ordinal/commit/blob/path/census ID resolves.
- F06 row 7 and F11 row 12 retain `STRICT_CSV_REJECTS_QUOTING__RAW_PHYSICAL_KEY_ONLY__FIELD_SEMANTICS_HOLD`; independent strict CSV per-line parse fails for those two, while other nine have eight fields. Sidecar and census do not promote unqualified field meanings to current functional evidence. Twenty-three estate `semantically_reconciled`, `authority_application_proved`, `first_consumer_proved` remain zero; preserved holds are a *positive no-false-promotion finding*, not an S2 `HOLD` on source-key equality.
- ZL-01 seam predicate receipt 82 rows unchanged (blob `576b466b5edb5527daaf2d70978573a9942ff2a1`); original 26 `IF` predicates remain scoped. Source/cut positions unchanged.

## S2 execution evidence — positive but not fully coherent
Worker PR #826 `WORKER_RETURNS/PROGRAMMA-VMESTYE-P0-S2-QUALIFIED-VALIDATOR-20261109-R1/` files read at exact new worker HEAD:
- Historical bootstrap log exit `0`, protected 18 `NOT_DISPATCHED`, nine `NOT_RUN`, `BOOTSTRAP_SOURCE_PIN_AND_SHAPE_OK__FUNCTIONAL_ZERO_LOSS_UNPROVED`.
- New `logs/P0_S2_BASELINE_RESULT.json` blob `e1031aa9c0bfb7a86b481ff51c882cacd2ffecfc`: **49 PASS, zero FAIL, zero HOLD**. All old D05 no-drop failures absent; stdout coherent, stderr empty, new `P0_S2_EXECUTION_RECEIPT.tsv` reports baseline exit `0`.
- Eight fresh mutant logs all contain their specific expected error IDs and nonzero exit; crucially none inherit the old baseline's `A_SOURCE_KEYS:D05_SOURCE_PACKAGE` failure. Five unit tests reported pass. Review did not rerun them.
- Updated assembly manifest: 18 exact candidate files (9 from ZL-00, 9 from corrected ZL-01), no path overlap; independently read several blob hashes and confirmed their listed candidate-source blob IDs. Full local assembly was not reproduced in this GitHub reader.

## Blocking R4 discrepancies — S2 worker must correct
1. **R4-D01 — contradictory baseline exit evidence:** `P0_S2_EXECUTION_RECEIPT.tsv` blob `01ffbbd518b35e10283f425afec26603a557af11` says clean baseline `exit_code=0` while committed `logs/P0_S2_BASELINE_EXIT.txt` at identical PR826 HEAD still reads **`1`**. The return and implementation narrative both claim `0`. No versioned label identifies the `1` as a historical failed baseline; as named it is a contradictory primary executable receipt. Re-execute/recapture authoritative clean baseline, or append an explicitly labeled and source-hashed erratum preserving provenance, so exit receipt, stdout/stderr, JSON, and implementation readback agree. Do not silently overwrite the old evidence without documenting the historical run.
2. **R4-D02 — stale 364 bypasses positive selector court:** `validation/validate_vmestye_p0_s2.py` at Git blob `a9f921502e38a1eb288042aa51b7cd4da780a6fc`, lines **648–649**, still uses `if ok and total == 364:` before recording `C_D02_D07_SELECTORS` PASS. On corrected total **369**, that named positive assertion is *silently omitted* from the 49-result JSON (confirmed absent). Other source-key and per-file checks make 369 equality plausible, but the explicit promised selector receipt must not disappear based on stale expected count. Replace literal with source-derived/versioned correct condition, emit an explicit PASS or FAIL/HOLD for that assertion, and add a unit or negative fixture that catches this omission.
3. **R4-D03 — raw-line hash validator checks syntax, not source digest:** same validator lines **563–565** checks `raw_physical_line_sha256` against a `sha256:[0-9a-f]{64}` regular expression, but does not compare it to SHA256 of the immutable Git source raw physical line. I independently recomputed all 11 source hashes and found them correct, so there is no current-source discrepancy; the *executable integrity claim* is weaker than the field identity requirement. Bind the SHA to actual `commit+path+physical record ordinal` bytes, reject mismatched digest, and test a plausible but wrong 64-hex digest. This should be additive to the original eight negatives, not a substitute.

All three are narrowly repairable on S2 worker PR #826 without reopening the successful ZL-01 source-key correction, unless repair uncovers new substantive source disagreement.

## Decision and handoff
**REVISE S2; ZL-01 identity PASS_S0_S1; P0 NOT ACCEPTED.** This review is not the same as an authorized independent mainMac S2 run; its conclusions concern received source objects, submitted logs, and script logic. The preservation of F06/F11 historical field-semantic HOLD is correct and not permission for functional/scientific application.

Owner: **PR #826 S2 validator worker**. Provide new immutable HEAD with coherent baseline exit evidence; source-derived 369-selector result always emitted; genuine raw-line SHA256 comparison and a tampered-digest control; repeat clean baseline + eight required mutations and unit checks on pinned corrected ZL-01 `353adc216a832a6c41ccc99f77cb3b53651af64e`. Then same independent #799 ZL-P0R reviewer re-receives. No need to redispatch ZL-01 for already verified source-key correction.

Only after an independent `ACCEPT_P0_SCHEMA_AND_ESTATE` can VMESTYE/Omega HQ adjudicate Phase 0 closure and potential P1 release; this reviewer does not self-release or merge. `ZL-02..14` remain CLOSED, no protected write, original35/native/S3, scientific, actor or first-consumer/current functional zero-loss promotion.
