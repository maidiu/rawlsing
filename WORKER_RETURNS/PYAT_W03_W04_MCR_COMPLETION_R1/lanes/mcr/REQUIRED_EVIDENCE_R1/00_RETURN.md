# Required MCR evidence preparation R1

**Status:** `DELIVERED_PENDING_RECEIVING`
**Branch:** `agent/pyat-w03-w04-required-evidence-preparation-r1`
**Initial/execution cut:** `1c428d59dc53cb76a19c1502a74cfd3bba00a899`
**Scope:** prepare the exact twelve frozen top-level output documents and their declared evidence where the required court was actually run. This is not whole-MCR, economic, or final receiving acceptance.

## What was executed

- One canonical sourcefree selection (94 sourcefree tests plus 5 verifier tests): **99 passed in 41.63s**. Per-ID JUnit files are filtered extractions of this same run, not reruns.
- Existing proof-integrity gate `changed` from frozen `46b7325637e68f78ccc7487d4b1abc7009c5ac0b` to cut `1c428d59dc53cb76a19c1502a74cfd3bba00a899`: **MECHANICAL_PROOF_GATE_PASS_NOT_SCIENTIFIC_ADOPTION**, **2 witness contracts**, each baseline PASS and mutation RED.
- Existing verifier self-test: **PASS_SELF_TEST**, 32 negative mutations rejected.
- Launch-wrapper validation: **PASS_FORMAT_ONLY_NOT_AUTHORITY_OR_LAUNCH**, 12 obligations.
- Frozen commission/TSV/wrapper bytes were not edited: commission SHA-256 `ddc6273adcc9aeb1b7e75c7d82897dde929adffea152e7f57dc5254fa32f0166`; TSV SHA-256 `5de8d68207de353926bd2d42095a8c8c44a36b06ac4038a7c9b16a1b6173428e`; wrapper SHA-256 `c25dbb96259971a8f623179dd1435bcdc2d684edb2b02a4970565bbb0c5c25e7`.

## Artifact readiness

- Twelve exact output documents are present at the frozen top-level paths.
- Evidence is present for `W03-PREVIOUS-CAPITAL` and the tested engineering/persistence/boundary obligations (01, 04-09, 11, 12).
- Evidence is **intentionally absent/not run** for `W03-COLD-HIGHWATER`, `W03-SELECTED-CELLS-CANON`, and `W34-RESOURCE-ECONOMY` (02, 03, 10). Their output documents state `INCOMPLETE_NOT_RUN` and name the missing 100000-row raw receipts.
- No `proof_02`, `proof_03`, or `proof_10` PASS placeholder was created.
- No `delivered_ids.txt`, SHA-bound external `MCR_COMPLETION_EVIDENCE` block, final `--verify-return`, or independent same-SHA receiving block was manufactured.

## Unresolved exact obligations

1. `W03-COLD-HIGHWATER` — `proof_02_cold_rss.json` absent; 100000-row cold matrix not run/authorized.
2. `W03-SELECTED-CELLS-CANON` — `proof_03_cost_comparison.json` absent; 100000-row cells-and-hash matrix not run/authorized.
3. `W34-RESOURCE-ECONOMY` — `proof_10_resource_matrix.json` absent; final 100000-row full matrix not run/authorized; R4 8-row protocol is not final.
4. `W34-REPRODUCIBLE-RETURN` — local selected tests and proof gate passed, but independent same-SHA code/economic receiving and final external MCR evidence are pending.
5. GitHub Actions CI was not dispatched in this lane; local sourcefree execution is recorded, not CI acceptance.

## Evidence paths

- Canonical log/JUnit: `lanes/mcr/REQUIRED_EVIDENCE_R1/logs/selected_99.log`, `.../selected_99_junit.xml`.
- Proof gate: `lanes/mcr/REQUIRED_EVIDENCE_R1/logs/proof_gate_full_frozen_to_1c428d.json` and `.stderr`.
- Checker/wrapper: `.../logs/checker_self_test.log`, `.../logs/wrapper_validate.log`.
- Execution cut: `.../logs/execution_cut.txt`.

## Limits

Source/test/workflow/MCR code remained read-only; all writes are evidence/docs at the declared twelve paths and this receipt root. No source/respondent/SAV/DTA/DB/native/science/actor/protected-merge or 100k/full-matrix operation occurred. No model/provider/account/effort/region/install/subworker change. Final same-immutable-SHA 12-ID, both independent receivers, and external MCR requirements remain mandatory.
