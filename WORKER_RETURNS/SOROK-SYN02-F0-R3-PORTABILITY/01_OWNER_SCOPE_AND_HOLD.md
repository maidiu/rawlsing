# SYN02-F0-R3 — owner scope and source-edit hold

## Current execution override — 2026-10-28

The user explicitly superseded the earlier procedural approval requirement: "only stop for genuine decisions that actually have consequences and implications, trade-offs, need unpacking and theoretical charting-out" and "if ... there is an obvious right answer ... do not waste time on it". This authorizes the already-tested correctness/security repair here; the historical source-edit hold below no longer blocks this patch. Exact patch SHA256 `40b98b7b6f08016ffe69e4c7054bc7277944a5d06931c9dfa29864f9c80ffea9` was checked and applied to the unchanged source on existing R3 branch at `f645c9227d7fd1bc1908bdce0f03667c9161980d`. The four enumerated source/manifest paths alone changed, plus this current record and execution receipts. The pre-existing 141-file trust inventory remains hash-identical.

Root inspected the source patch independently of its OpenCode author and executed the prescribed deterministic regressions: **86 passed from repository root and 86 passed from `/tmp`**. Actual results are recorded in `02_TEST_RECEIPTS.md` and `03_APPLIED_REGRESSION_RECEIPT.json`. This grants no scientific law, real provider/account call, irreversible world event, Pyat/native-person acceptance or production deployment. The sections below describe the prior held state and its original reasoning.

**Status:** `NO_R3_SOURCE_OWNER_SCOPE_FOUND__SOURCE_EDITS_HELD__ISOLATED_PATCH_AND_TESTS_READY__NO_SOURCE_EDIT__NO_NATIVE_GRANT`.

## 1. What was checked

The F0-R2 owner-scope record at `WORKER_RETURNS/SOROK-SYN02-F0-R2-PORTABILITY/01_OWNER_SCOPE.md` says:

- the user selected **“Approve enumerated R2 source scope”**;
- the approval is for the **R2** source paths and R2 tranche only;
- it is “not a standing source-owner grant,” “not a retroactive F0 approval,” and “not a native/production grant”;
- the original F0 alternate branch and its extra-file delivery remain separate/unadopted;
- a distinct reviewer must accept before integration.

The R2 record’s approved paths are the S48/S51/S52 source paths, but its date, branch, startup, commission and text are specifically the F0-R2 tranche. It does not name F0-R3, the R3 branch, the R3 commission, the R3 startup, or the R3 patch/tests.

The R3 commission itself says:

> “Actual S48/S51/S52 source edits require verified prospective owners' scope approval; if absent write only isolated R3 tests/repair plans and HOLD existing-source edits.”

I searched the checked-out worktree and the exact startup history for an R3-specific owner approval. No such record was found. The user launch is a dispatch, not a witnessed original-owner scope signature. Therefore:

- **No actual S48/S51/S52 source file was edited.**
- **No test file, manifest, or evidence script inside the source packages was edited.**
- The proposed code changes are held as an isolated patch in `patches/F0-R3-source-custody.patch`.
- The external trust file and acceptance tests are isolated under this R3 return.
- A **competent S48/S51/S52 source owner** must prospectively approve the exact R3 scope before the patch is applied to the accepted source.

This is not a rejection of the R3 repair; it is the required authority hold.

## 2. Preserved boundaries

- Historical F0 alternate branch `agent/sorok-syn02-f0-portable-sourcefree-build-r1` remains at `c821b488b3a9a3f0fa01b1981989cc17af637dc1`; it is not adopted.
- R2 branch `agent/sorok-syn02-f0-r2-source-custody-repair-r1` remains at `60797302652e7d7877443f6e9d0becde5afb8382`; it is the source-edit baseline.
- R3 branch is `agent/sorok-syn02-f0-r3-source-custody-repair-r1` at its sealed startup; no source branch merge, force-push or reset occurred.
- No production, C9/C12, CAN/ADP/SCI05/Pyat, source-survey, provider-account or native C11/C12/A5 file was changed.
- No paid CLI/provider or account entitlement was tested.
- C12 fork perception-loss remains an independent inherited RED; this R3 patch does not repair it.

## 3. What the owner must approve

If the owner elects to apply the isolated patch, the prospective scope must name:

- exact startup `60797302652e7d7877443f6e9d0becde5afb8382`;
- R3 branch `agent/sorok-syn02-f0-r3-source-custody-repair-r1`;
- the four patched source/manifest paths in `patches/F0-R3-source-custody.patch`;
- the new `external_source_trust.json` and R3 tests under this folder;
- no provider/account/native/production authority.

After approval, a separate implementer/owner should:

1. Apply `git apply --check` then `git apply` the patch to a clean R2 source checkout.
2. Copy `external_source_trust.json` to the R3 path used by the patched binding.
3. Run the commands in `02_TEST_RECEIPTS.md` from repository root and `/tmp`.
4. Run the R3 tests against the patched copy; no real provider.
5. Send the resulting source and tests to a distinct independent reviewer.

No self-adoption, no native grant.

## 4. Actual status

- Source-edit disposition: **HOLD**.
- Patch disposition: **READY_FOR_OWNER_APPLICATION / NOT_APPLIED**.
- Test disposition: **R3 tests RED on unpatched R2, GREEN on isolated patched copy**.
- Science disposition: **NO_CHANGE**.
- Authority disposition: **NO_NATIVE / OWNER SCOPE HELD**.
