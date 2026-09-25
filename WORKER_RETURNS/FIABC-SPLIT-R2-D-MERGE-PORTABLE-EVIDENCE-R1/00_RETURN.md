# FIABC SPLIT R2 — Worker D return

Terminal:

`PASS__SPLIT_R2_D_MERGE_PORTABLE_EVIDENCE__READY_FOR_FANIN`

## Provenance

- Repository: `maidiu/rawlsing`
- Exact common base: `e1b82095c83dd15a64b409dba0e4ae7d4f4460c6`
- Worker commission commit: `5019995462f7ae8ffccdd45c2a6932823e4ffd8e`
- Worker D implementation/test head: `d0b8c289428ace3df0d71581ee7f5afaeb42c057`
- Protected execution head, unchanged: `3d8f2ad62600b6777dcb23a28404a067502e77a0`
- Dedicated fan-in branch: `agent/vozhd-fiabc-split-r2-fanin-r1`

This lane remained source-free and candidate-free. No LiTS/WVS raw source was opened, hashed, decoded, or inferred from. No Candidate A/B/C process was launched. No measured P2X was run. Protected execution and prior measured roots were not mutated.

## What Worker D implemented

### 1. Non-circular qualified-control binding

Added:

`HQ_HANDOFF/launchers/FIABC_SOURCE_LOCAL_SPLIT_EVIDENCE.py`

It provides a post-qualification external control binding that binds:

- exact qualified implementation commit;
- exact qualified control branch;
- exact protected execution head;
- exact SHA-256 of launcher, source-local driver, merge verifier, and evidence helper;
- clean control checkout;
- current checkout bytes matching the qualified bytes even when an evidence/docs-only tip is later checked out.

Wrong branch, dirty checkout, missing qualified commit, missing bound file, and any bound-file hash drift fail closed.

The receipt is intentionally external to the qualified implementation commit, avoiding an impossible self-referential commit-hash requirement.

### 2. Pre-run repo-live baseline and post-terminal portable closure

The helper adds a pre-run exact-HEAD inventory of:

`WORKER_RETURNS/EE-P2X/LOCAL_COURT`

The inventory distinguishes tracked HEAD baseline bytes from later live mutations.

After the measured source-local terminal exists, the portable closure independently binds and verifies:

- canonical selected-source SHA;
- exact protected execution head;
- exact current manifest Git blob identity;
- exact source-local terminal and its self identity;
- exact stage ledger and hash;
- every selected-source stage receipt and hash;
- no foreign-source ledger stage;
- no RUNNING stage;
- candidate terminal addresses/dispositions;
- blocker and candidate-failure inventories against the ledger;
- every work-root output artifact hash;
- every repo-local ledger artifact hash;
- pre/post repo-live evidence delta;
- all changed repo-live evidence attributable to the selected-source ledger;
- portable copies of every repo-local ledger artifact under the external WORK_ROOT;
- qualified control binding;
- runtime/host fingerprint;
- no S17, no six-cell completion, no measured synthesis, no P2 authorization;
- no copied raw survey bytes.

Any repo-live mutation outside the selected-source ledger attribution is rejected rather than silently packaged.

### 3. Nonzero measured-driver orchestration failure receipt

The helper provides a fail-closed receipt for any nonzero measured-driver exit. It records:

- source and canonical source SHA identity;
- protected execution head;
- qualified control identity;
- runtime when available;
- measured-driver exit code;
- whether any candidate ledger entry exists;
- last terminal/partial source stage;
- ledger/progress hashes when present;
- source terminal presence/absence;
- exact `PRESERVE_WORK_ROOT`;
- explicit no-automatic-retry law;
- explicit classification as orchestration/control failure rather than inferred candidate-local failure.

### 4. Merge hardened from summary-trust to evidence verification

Replaced the former terminal-summary merge with a verifier that independently re-opens and validates, for both LiTS-I and WVS7:

- terminal self identity and exact canonical source SHA;
- exact protected execution and manifest identity;
- A/B/C inventory;
- source-local/no-S17/no-synthesis flags;
- stage ledger;
- all stage receipt paths and hashes;
- absence of foreign-source stages and RUNNING stages;
- completeness versus explicit common-court incomplete inventory;
- candidate terminal/disposition coherence;
- blocker/failure coherence;
- portable repo-live evidence copies and hashes;
- qualified control binding;
- same-hardware/governed-runtime law;
- macOS mismatch as separately recorded, not collapsed into hardware/runtime;
- permanent prohibition on absolute cross-source physical comparison.

Merge still does **not** recreate governed S17 and does not authorize P2 synthesis or architecture selection.

### 5. Explicit control compatibility law / WVS RUN5 framework

Default new-court law is one exact qualified split-control implementation for both halves.

A legacy WVS half is never silently grandfathered. The helper emits only a HOLD framework listing the required findings. Merge accepts a control exception only with an explicit compatibility receipt proving candidate-execution semantic equivalence, portable reverification, and explicit physical-metric admissibility adjudication, scoped to `WVS7_LEGACY_RUN5_ONLY`.

### 6. Protected-backend repo-live write audit

Forensic inspection of protected `rawlsing_next/ee_p2x_darwin_stage_backend.py` at `3d8f2ad...` found the mutable `LOCAL_COURT` writers at the cell/failure, learned, persistence, and deletion paths. Those writes are surfaced as backend `output_artifacts`, so requiring post-run live mutations to be ledger-attributable is compatible with the protected backend rather than an invented relocation or new evidence channel.

## Source-free hostile qualification

Checked in:

`rawlsing_next/tests/test_fiabc_split_r2_d_merge_portable_evidence.py`

Isolated source-free execution result:

- 9 tests run
- 9 PASS
- exit code 0
- raw source opens: 0
- raw source hash passes: 0
- decoder calls: 0
- candidate launches: 0
- candidate outputs: 0
- measured execution: false

The tests cover exact 51-stage-per-source inventory, foreign-source rejection, RUNNING-stage rejection, receipt hash tamper, canonical source drift, control hash drift, dirty checkout, wrong control branch, nonzero orchestration receipt semantics, same-qualified-control default law, explicit legacy WVS compatibility, macOS-separate treatment, hardware/runtime mismatch rejection, and permanent cross-source physical-comparison prohibition.

## Fan-in wiring contract

Worker D deliberately did not rewrite Worker B's owned shell.

Fan-in must wire the Worker D helper into the integrated launcher at these boundaries:

1. **after protected checkout/runtime/control gates, before measured source-block entry:** emit repo-live baseline;
2. **on nonzero measured-driver exit:** emit orchestration-failure receipt before returning the nonzero exit;
3. **after source-local terminal exists and measured timing is over:** emit portable evidence closure;
4. **after integrated source-free qualification:** seal the immutable qualified-control binding against the exact qualified implementation head, then bank it in an evidence/docs-only commit;
5. **merge:** invoke hardened merge with the control root and, only when HQ has explicitly adjudicated legacy WVS conservation, the compatibility receipt.

The launcher may run from a later evidence/docs-only tip only if its current launcher/driver/merge/helper bytes exactly match the immutable qualified binding. The source terminal records the observed checkout head; the closure separately binds the qualified implementation identity.

No Worker D change touches the protected execution branch or canonical six-cell launcher.

`PASS__SPLIT_R2_D_MERGE_PORTABLE_EVIDENCE__READY_FOR_FANIN`
