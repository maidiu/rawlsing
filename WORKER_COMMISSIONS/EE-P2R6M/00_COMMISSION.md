# EE-P2R6M — EXACT ADOPTED R6L VALIDATED C11 SNAPSHOT MATERIALIZATION

Repository:

`maidiu/rawlsing`

## Execution surface

**LOCAL-MACHINE CODEX**

## Maximum intelligence

**LUNA**

## Library access

**EXACT_ONLY**

Only the exact already-authorized LiTS-I carrier may be accessed.

Exact branch:

`agent/rabochii-prev3-ee-p2r6m-local-validated-c11-snapshot-materialization-r1`

Exact base:

`21948398ad84095b69a815e29e756ad9f6d139c4`

Before doing anything else, resolve live canonical HQ through:

`HQ_HANDOFF/LATEST.json`

and verify the immutable checkpoint packet.

At commission time the sealed checkpoint is:

`20260918T1909-0400`

with immutable handoff:

`71767a68c73aadb4d678f088202647dc56692f23`

Controlling decision:

`HQD-2026-09-18-062`

Read:

`HQ_HANDOFF/EE_P2R6K_ADOPTION_20260918.md`

and:

`WORKER_RETURNS/EE-P2R6K/05_LOCAL_EXECUTION_PACKET.json`

before execution.

## Mission

Perform exactly one local replay of the already-adopted R5B/R6L construction solely to emit the missing complete canonical validated-C11 snapshot.

This is not a new empirical study.

This is not a benchmark.

This is not P2X.

This is not permission to inspect arbitrary Library material.

This is one exact reconstruction/materialization of already-adopted authority.

## Authorized carrier

Only:

`LITS-2006-data.dta`

Exact SHA-256:

`7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`

Expected dimensions:

`29,002 × 1,198`

All other Library/carrier access is forbidden.

If the exact carrier cannot be resolved or its SHA differs, STOP.

## Exact programs

Use the exact adopted R6K programs:

- codec:
  `WORKER_RETURNS/EE-P2R6K/02_C11_VALIDATED_SNAPSHOT_CODEC.py`
  blob:
  `d4427366f15b98ab2acd40578f7ff59ee574b2d0`

- local materializer:
  `WORKER_RETURNS/EE-P2R6K/03_LOCAL_SNAPSHOT_MATERIALIZER.py`
  blob:
  `3decd4055f97f6b55996417d5ad7b84f86c806e0`

- rehydrator:
  `WORKER_RETURNS/EE-P2R6K/04_SNAPSHOT_REHYDRATOR.py`
  blob:
  `02d731e43b30a85ba2df39dd5b62211c51352981`

- adopted R5B driver:
  `WORKER_RETURNS/EE-P2R6K/SUPPORT/R5B/03_LOCAL_I02_SUCCESSOR_RELEASE_DRIVER.py`
  blob:
  `b819fdff50470a71f1c570aa8021e28b361fa986`

Verify all exact blobs before execution.

Do not patch any of these on failure.

## Exact invocation

Use an empty output directory.

Run exactly:

`python WORKER_RETURNS/EE-P2R6K/03_LOCAL_SNAPSHOT_MATERIALIZER.py --source <EXACT_LIBRARY_PATH>/LITS-2006-data.dta --output-dir <EMPTY_OUTPUT_DIR>`

Run count:

`ONE`

Do not perform a second source replay after a successful run.

## Hard stop identities

The materializer must reproduce all adopted R6L identities exactly.

Release ID:

`LITS1-I02-F02-SUCCESSOR-7cac43e2ca5b31cb-bf305bf3f169d669`

Semantic release hash:

`192926fabd9c9c3d40e43b1d7705ca2bcfe7f8d06e286be26d4b886d436df43f`

Source release manifest hash:

`0546be4fa3f55239ee5d208234000066bdc84d832e89bc91d646ee623ed96714`

Candidate projection hash:

`23912633a23318d22bad0da08027867031320331d8d436d944e9c0b21eb086eb`

ReplayManifest hash:

`30c168fbdf8425b23cbf2a2b2d2c9ab56f3438851f52e3562510089f1d381a08`

Historical replay-manifest JSON SHA-256:

`aa3b6026d4dbc3df8b142725704974eaef810e5dbf5b31d14b19c88cf8ecafd5`

Any mismatch is an immediate BLOCK.

Do not "repair" or normalize a mismatch.

## Required validation path

The emitted snapshot is acceptable only if exact rehydration proves:

`SERIALIZED_CANONICAL_CANDIDATE_BODIES`
→ `C11SourceReleaseCandidate`
→ `validate_c11_source_release`
→ genuine sealed `C11LogicalRelease`
→ `C11Repository`
→ `resolve_release_exact`

Private `_make_validated_release` or `_C11_VALIDATION_SEAL` use is forbidden.

## Required outputs

Write governed return material under:

`WORKER_RETURNS/EE-P2R6M/`

At minimum:

1. `00_RETURN.md`
2. `01_LOCAL_SNAPSHOT_MATERIALIZATION_RECEIPT.json`
3. `02_SNAPSHOT_TRANSPORT_MANIFEST.json`
4. `03_SNAPSHOT_REHYDRATION_RECEIPT.json`

Snapshot transport must follow exact R6K law.

One logical semantic snapshot:

`validated_c11_candidate_snapshot.json`

Deterministic gzip:

- compresslevel `9`
- `mtime=0`

If gzip size is at or below `94371840` bytes, commit one:

`validated_c11_candidate_snapshot.json.gz`

If gzip size exceeds `94371840` bytes, split only the compressed transport stream into fixed `50331648`-byte ordered chunks, with exact per-chunk hashes and reconstruction metadata.

Do not semantically partition the JSON snapshot.

Do not commit an individual Git blob above GitHub's limit.

The local receipt must bind:

- source SHA and dimensions;
- exact R6K program blobs;
- snapshot schema;
- canonical uncompressed snapshot byte length and SHA-256;
- compressed byte length and SHA-256;
- chunk set if used;
- all adopted R6L hard-stop identities;
- public rehydration PASS;
- repository exact-resolution PASS;
- exact one-release repository snapshot identity;
- confirmation that source replay count was one;
- confirmation that no forbidden downstream work occurred.

## Banked binding preimage boundary

The banked corrected binding preimage remains exactly:

`a5f36a81843fe2ebab0b5cccb369ce76035f842b93e602613b8b9f3a81103308`

Do not recompute it.

Do not activate it.

Do not run the R6A positive binding proof in this local commission.

## PASS terminal

`EE_P2R6M_PASS__ADOPTED_R6L_IDENTITIES_EXACT__VALIDATED_C11_SNAPSHOT_EMITTED_AND_PUBLICLY_REHYDRATED__READY_FOR_BROWSER_R6A_POSITIVE_PROOF`

PASS wakes HQ adjudication only.

## BLOCK terminal

`EE_P2R6M_BLOCK__<EXACT_FIRST_SOURCE_REPLAY_SNAPSHOT_TRANSPORT_OR_REHYDRATION_FAILURE>`

## Hard forbidden

- no access to any carrier except exact LiTS-I;
- no second successful source replay;
- no benchmark/performance measurement;
- no source-semantic exploration;
- no selector mutation/remint;
- no binding activation/adoption;
- no R6A positive binding proof;
- no A/B qualification;
- no BE1;
- no P2X;
- no Candidate-C repair;
- no D02/F02 workload mutation;
- no Lock1/Lock2 mutation;
- no MAIN or semantic PRE-MAIN mutation;
- no patching R6K code on failure;
- no rebase;
- no replacement branch.

Commit and push the governed return on this exact branch.

Report PASS/BLOCK, final tip, snapshot logical SHA/size, transport SHA/size and chunk disposition, rehydration disposition, exact repository snapshot identity, and wake.

Return to HQ.
