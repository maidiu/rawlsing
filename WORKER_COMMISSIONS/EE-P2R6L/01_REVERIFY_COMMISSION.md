# EE-P2R6L-R2 — EXISTING R6L OUTPUT NO-CARRIER RE-VERIFICATION AND SEAL

Repository: `maidiu/rawlsing`

## Execution surface

**LOCAL-MACHINE CODEX**

## Maximum model intelligence required

**LUNA**

This is a verification-and-sealing task only. No empirical execution, investigation, repair, or semantic judgment is authorized.

## Library access

**NO**

Do not open, hash, inspect, enumerate, or otherwise access `LITS-2006-data.dta` or any other carrier.

## Exact branch

`agent/rabochii-prev3-ee-p2r6l-lits-i02-successor-release-local-execution-r1`

This is the continuation of the existing R6L local worktree containing the four already-generated, uncommitted JSON outputs under:

`WORKER_RETURNS/EE-P2R6L/RUN_OUTPUT/`

Do not create a replacement branch.

Do not rebase.

## Authority precondition

Before doing anything else:

1. resolve live `HQ_HANDOFF/LATEST.json`;
2. verify the immutable checkpoint packet;
3. confirm HQ decision `HQD-2026-09-18-051` is adopted;
4. confirm that R6R repair head `20a53b10503ed5caf803fd875bd735286986449b` is adopted;
5. confirm the local branch is authorized for **verification-only / Library NO** continuation.

If those conditions are not present in live HQ, STOP without touching the existing outputs.

## Prior lawful local execution

The earlier exact R6L carrier/driver execution already occurred and obeyed first-failure law.

It stopped at:

`EE_P2R6L_BLOCK__F02_SOURCE_SCAN_ROOTS_COUNTS_MISMATCH`

HQ subsequently proved that failure was caused by the old verifier's truncated `EXPECTED_SCAN` schema, not by demonstrated source-replay divergence.

The existing four output files were produced before that verifier failure and must be preserved byte-for-byte:

- `successor_release_receipt.json`
- `successor_release_replay_manifest.json`
- `successor_release_m01_m18.json`
- `successor_release_extension_scan.json`

## Adopted repaired verifier

Use only:

`WORKER_RETURNS/EE-P2R6L/SUPPORT/02_REPAIRED_SUCCESSOR_RELEASE_VERIFIER.py`

Required Git blob SHA-1:

`e7752c558c7fb407852ef7377f45eca775d3b86b`

This file is an exact copy of the adopted R6R repaired verifier.

Original source driver blob, for provenance only:

`b819fdff50470a71f1c570aa8021e28b361fa986`

### Critical prohibition

**DO NOT EXECUTE THE SOURCE DRIVER AGAIN.**

Do not reopen the carrier.

Do not regenerate any of the four existing JSON outputs.

Do not edit any of the four outputs before or after verification.

## Mission

Reverify the already-existing output set using the adopted repaired verifier.

If and only if that verifier passes, hash and seal the exact existing files and create the governed R6L PASS return.

## Step 0 — fast-forward only

Because this branch has been advanced remotely only to add this successor commission and the adopted repaired verifier support file, bring the local branch to the exact current remote commission tip by a **fast-forward only** operation.

Preserve all four existing uncommitted output JSON files.

Do not use reset --hard, clean, checkout paths, stash-drop, or any operation that can discard them.

If Git reports an untracked-file conflict involving those four outputs, STOP and preserve them. Do not overwrite or move them without explicit HQ repair authority.

## Step 1 — pre-verification integrity

Confirm all four required files already exist.

Do not rewrite them.

Record SHA-256 of all four **before** running the repaired verifier.

This is file-integrity bookkeeping only; it does not authorize empirical interpretation.

## Step 2 — repaired verifier only

Run exactly in substance:

`python WORKER_RETURNS/EE-P2R6L/SUPPORT/02_REPAIRED_SUCCESSOR_RELEASE_VERIFIER.py --receipt WORKER_RETURNS/EE-P2R6L/RUN_OUTPUT/successor_release_receipt.json`

The verifier discovers and checks the three sibling sidecars from the receipt directory under the preserved R5B contract.

No source path argument is permitted.

No carrier may be opened.

### On failure

STOP at the exact first failing check.

Do not:

- edit the outputs;
- patch the verifier;
- rerun the source driver;
- reopen the carrier;
- substitute a different sidecar;
- weaken a check.

Return the exact new blocker with command, exit status, stderr, pre-verification hashes, and failing check.

## Step 3 — post-verification immutability

If verifier exits 0:

1. SHA-256 hash the same four existing JSON files again.
2. Require every post-verification hash to equal its pre-verification hash.
3. Extract the exact I02-minted runtime release ref only from the verified existing receipt.
4. Do not infer or issue a ReleaseRealizationBinding.

Any byte change before/after verification is a BLOCK.

## Step 4 — governed return

Create:

`WORKER_RETURNS/EE-P2R6L/00_RETURN.md`

and:

`WORKER_RETURNS/EE-P2R6L/01_LOCAL_EXECUTION_RECEIPT.json`

The receipt must bind at minimum:

- prior carrier/driver execution status: `COMPLETED_BEFORE_R6R_REPAIR__NOT_RERUN`;
- prior first-failure terminal;
- original driver Git blob SHA-1:
  `b819fdff50470a71f1c570aa8021e28b361fa986`;
- adopted repaired verifier Git blob SHA-1:
  `e7752c558c7fb407852ef7377f45eca775d3b86b`;
- exact repaired-verifier command;
- verifier exit status;
- pre-verification SHA-256 for each of the four existing outputs;
- post-verification SHA-256 for each output;
- equality of pre/post hashes;
- exact I02-minted runtime release ref from verified receipt;
- exact accepted-I02 disposition from verified receipt;
- confirmation `LIBRARY_ACCESS_DURING_R2 = NONE`;
- confirmation `SOURCE_DRIVER_RERUN = FALSE`;
- confirmation `OUTPUT_REGENERATION = FALSE`;
- confirmation `REALIZATION_BINDING_ISSUED = FALSE`;
- confirmation `P2X_EXECUTED = FALSE`;
- confirmation `BE1_EXECUTED = FALSE`.

Preserve any original local runtime/environment metadata already available from the prior run or generated receipt. Do not invent missing historical environment facts.

## Step 5 — commit

Commit only:

- the four already-existing output JSON files;
- `WORKER_RETURNS/EE-P2R6L/00_RETURN.md`;
- `WORKER_RETURNS/EE-P2R6L/01_LOCAL_EXECUTION_RECEIPT.json`.

The repaired support verifier and this commission are already committed by HQ.

Do not commit source carrier bytes, caches, environments, logs unrelated to the governed receipt, or other repository changes.

Push the exact branch.

## PASS terminal

`EE_P2R6L_PASS__ACCEPTED_I02_SUCCESSOR_RELEASE_MINTED_AND_VERIFIED__READY_FOR_CONCRETE_REALIZATION_BINDING_ISSUANCE`

PASS wakes:

`HQ_CONCRETE_REALIZATION_BINDING_ISSUANCE_USING_ADOPTED_R6R_REFRESHED_R6B_CHAIN`

## BLOCK terminal

`EE_P2R6L_R2_BLOCK__<EXACT_FIRST_REVERIFICATION_OR_SEAL_FAILURE>`

A BLOCK does not authorize carrier access or driver rerun.

## Hard forbidden

- no Library access;
- no carrier access;
- no source driver execution;
- no regeneration or mutation of existing output JSONs;
- no verifier patch;
- no realization binding issuance;
- no P2X or BE1;
- no Candidate-C repair;
- no selector remint;
- no D02/F02 workload mutation;
- no Lock1/Lock2 mutation;
- no MAIN or semantic PRE-MAIN mutation;
- no rebase;
- no replacement branch.

Return PASS/BLOCK, final branch tip, exact runtime release ref if PASS, the four SHA-256 values, repaired-verifier disposition, and confirmation that the source/carrier was not reopened.
