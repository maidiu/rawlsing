# EE-P2R6N — EXACT POSITIVE R6A PRODUCTION RUNTIME PROOF

Repository:

`maidiu/rawlsing`

## Execution surface

**BROWSER**

## Library access

**NO**

Do not access Library files, LiTS/WVS carriers, source bytes, empirical outcomes, or performance measurements.

Exact branch:

`agent/rabochii-prev3-ee-p2r6n-positive-r6a-proof-r1`

Exact base:

`d3fcef89db39dedbf7502c56a4928d3e79737a2b`

Before doing anything else, resolve live canonical HQ through:

`HQ_HANDOFF/LATEST.json`

and verify its immutable checkpoint packet.

At commission time the sealed checkpoint is:

`20260918T1933-0400`

with immutable handoff:

`38946e55ec24aeb7b284570a5f88325201ae9b08`

Controlling decision:

`HQD-2026-09-18-064`

Read prospectively:

`HQ_HANDOFF/EE_P2R6M_SNAPSHOT_ADOPTION_20260918.md`

## Mission

Perform the exact positive production-runtime proof that EE-P2R6J could not lawfully execute before the durable validated C11 snapshot existed.

Do not redesign or recompute the binding.

Do not activate or adopt it.

Do not perform A/B qualification.

Do not execute BE1 or P2X.

The only substantive question is:

> Does the exact adopted production R6A runtime accept the already-banked corrected binding preimage `a5f36...` against the exact publicly rehydrated adopted R6L C11 repository and return the exact adopted runtime release?

## Exact banked corrected binding

Use byte-for-byte:

`WORKER_RETURNS/EE-P2R6J/04_PROPOSED_ACTIVE_RUNTIME_BINDING_RECORD.json`

Git blob:

`4ac8cd48aac62600e648ff9692488796c51c826f`

Binding hash:

`a5f36a81843fe2ebab0b5cccb369ce76035f842b93e602613b8b9f3a81103308`

Binding object ID:

`urn:rawlsing:prev3:p2r6j:release-realization-binding:sha256:a5f36a81843fe2ebab0b5cccb369ce76035f842b93e602613b8b9f3a81103308`

The record is qualification-only in this commission even though its internal typed state is `ACTIVE_POSITIVE`.

Repository/HQ active binding count remains zero until a later explicit HQ adoption.

Do not change one byte of its `identity_material`.

Do not derive a replacement binding hash.

## Exact adopted snapshot transport

Logical snapshot:

`validated_c11_candidate_snapshot.json`

Logical byte length:

`1447731437`

Logical SHA-256:

`ca1e62ca14586bcd23392fc56d0af5f95c12d833bf994ef5a0ea09577ca1569b`

Deterministic compressed stream:

- gzip level `9`
- mtime `0`
- byte length `116229878`
- SHA-256 `42bff5e6ffc9dd76283b74525f47a5ec99c91ca44d9b5a7537fd13b820ef8e04`

Transport chunks:

1. `WORKER_RETURNS/EE-P2R6M/RUN_OUTPUT/validated_c11_candidate_snapshot.json.gz.part0000`
   - bytes `50331648`
   - SHA-256 `9743cb7de71d470b305c91d3a9c55fd615d2d1544c3ae82bb33cf0e4f4d2ccb2`
   - Git blob `aa93259b3ab62722febc8b99c8c61c69e27be3db`

2. `WORKER_RETURNS/EE-P2R6M/RUN_OUTPUT/validated_c11_candidate_snapshot.json.gz.part0001`
   - bytes `50331648`
   - SHA-256 `0a5b16e20bb16b3b1537ea9b8e15e308f9daa3656c7c6a2fa299a4b3bb9da6f3`
   - Git blob `1944d8955118a2510188cbc78412afdc86481270`

3. `WORKER_RETURNS/EE-P2R6M/RUN_OUTPUT/validated_c11_candidate_snapshot.json.gz.part0002`
   - bytes `15566582`
   - SHA-256 `84071bd29a466bbf4f8cfe0fe681749610e18f88fedcb1cd2573a7031b0b1869`
   - Git blob `603c69ca19b2cae2d736b0f41907ec8a94983b9c`

Reconstruct only by concatenating the three chunks in ascending index, verifying the compressed identity, then gunzip once.

No semantic partitioning exists.

## Exact rehydrator

Use the adopted R6K rehydrator byte-for-byte:

`WORKER_RETURNS/EE-P2R6K/04_SNAPSHOT_REHYDRATOR.py`

Git blob:

`02d731e43b30a85ba2df39dd5b62211c51352981`

The lawful reconstruction path remains:

`SERIALIZED_CANONICAL_CANDIDATE_BODIES`
→ `C11SourceReleaseCandidate`
→ `validate_c11_source_release`
→ genuine `C11LogicalRelease`
→ `C11Repository`
→ `resolve_release_exact`

Do not use private validation-seal shortcuts.

## Exact adopted release

Runtime release ref:

- kind: `C11LogicalRelease`
- object_id: `LITS1-I02-F02-SUCCESSOR-7cac43e2ca5b31cb-bf305bf3f169d669`
- content_hash:
  `192926fabd9c9c3d40e43b1d7705ca2bcfe7f8d06e286be26d4b886d436df43f`

Exact repository snapshot identity:

`[{"content_hash":"192926fabd9c9c3d40e43b1d7705ca2bcfe7f8d06e286be26d4b886d436df43f","kind":"C11LogicalRelease","object_id":"LITS1-I02-F02-SUCCESSOR-7cac43e2ca5b31cb-bf305bf3f169d669"}]`

ReplayManifest:

`30c168fbdf8425b23cbf2a2b2d2c9ab56f3438851f52e3562510089f1d381a08`

Candidate projection:

`23912633a23318d22bad0da08027867031320331d8d436d944e9c0b21eb086eb`

## Exact production R6A runtime

Use the production module directly:

`rawlsing_next/pre553_runtime_authority.py`

Git blob:

`2ddc591f2572983d18f8f3e8f81a33b80b3bca7b`

Do not copy or weaken the runtime implementation.

The decisive call is:

`Pre553RuntimeAuthoritySet.require_realized_release(frozen_scope, repository=exact_rehydrated_repository, runtime_release_ref=exact_runtime_release_ref)`

The returned `C11LogicalRelease.release_ref` must equal the exact adopted R6L runtime release ref above.

## Exact authority construction

Instantiate `Pre553RuntimeAuthoritySet` from exact adopted R4A/R5A authority records.

The already-qualified R6A fixture-loading law is available in:

`rawlsing_next/tests/test_ee_p2r6a_runtime.py`

Use the same exact production authority records, not fixture semantic substitutes.

Exact adopted authority hashes:

- respondent binding: `3ef0317887f6910838636d3816237a81d5a56b38e07595c8cc1f7c5e7f1fae74`
- mixed grammar: `0d7cfaac1d63cd438d29b109b590cb828805bd113fc37759a6f6f4c88d3c8f55`
- derived predicate: `225e4b80390500451834ea784d955465eb9f145a4cd1f798dace51f3a6d3baa4`
- R4A aggregate/successor: `b87c387f9d222c83106c8d47d369af44f5c5368b274fd85e7a08b12c20d49cae`
- realization relation authority: `9da19997168612891f59012e69674bac59fbee417d9b30b003171f3074168bf5`
- concrete binding schema: `a1da1ea78dce423ea3520726d0477b058057482d67964056743e08389d9045a0`
- R4A release precondition successor clause: `d8e3d9a19fa36599e8cd6b1bc8e82092c425fd9119be478f7ba79335d05a1b3e`
- R5A aggregate: `d9aa476c493810651baefa8bad23990d9dd80812a48670ad2052353f0e7d52a2`

Use exact adopted R4A authority JSON and exact:

- `WORKER_RETURNS/EE-P2R5A/02_RELEASE_REALIZATION_RELATION_AUTHORITY.json`
- `WORKER_RETURNS/EE-P2R5A/03_CONCRETE_REALIZATION_BINDING_SCHEMA.json`
- `WORKER_RETURNS/EE-P2R5A/04_R4A_RELEASE_PRECONDITION_SUCCESSOR_CLAUSE.json`

No latest/fuzzy/default authority lookup.

## Frozen scope

Use exact frozen F02 scope:

- kind: `C11LogicalRelease`
- object_id: `LITS1-F02-C11-7cac43e2ca5b31cb-bf305bf3f169d669`
- content_hash:
  `bf305bf3f169d66954be4f39cc602880fddea6083b5bee9c0212938355cd5297`

## Current binding-registry boundary

The repository/HQ registry still has zero active positive bindings.

Current controlling registry snapshot remains:

`HQ_HANDOFF/BINDING_REGISTRY_SNAPSHOTS/20260918T1820-0400.json`

content hash:

`209cca7eb759c8fc2df265a0673d180f699381b164e80b88acfa5199438e2b56`

uniqueness key:

`659a8929df10b31da4c82eaf5a6b8bd74234b6f21430422beff186cab804fc16`

Before qualification, confirm live HQ has not adopted a later binding for this exact key.

The `a5f36...` record is injected only into the in-memory R6A authority set for qualification.

Do not write an active registry snapshot.

## Required proof

PASS requires all of the following:

1. all three transport chunk Git blobs and SHA-256 identities match;
2. concatenated gzip size/SHA match;
3. decompressed canonical snapshot size/SHA match;
4. public rehydrator PASS;
5. exact one-release repository snapshot identity;
6. exact R6L runtime release resolves;
7. production R6A module blob exact;
8. banked active-record blob exact;
9. binding hash remains exactly `a5f36...`;
10. exact R4A/R5A authority records are loaded;
11. `require_realized_release` returns exactly the adopted runtime release;
12. returned release source SHA satisfies exact relation authority;
13. candidate projection, replay ref and M01-M18 coverage all match the binding evidence;
14. zero binding still fails closed;
15. two active positive bindings still fail closed;
16. quarantined R6I `fd4177e...` still fails production binding validation;
17. mutated source identity fails;
18. mutated runtime release ref fails;
19. mutated replay ref fails;
20. incomplete M01-M18 coverage fails;
21. no source/Library access;
22. no activation/adoption or downstream A/B/P2X execution.

## Resource behavior

The snapshot is large. Use deterministic temporary reconstruction and delete transient uncompressed bytes after qualification.

Do not commit the 1.44 GB uncompressed snapshot or the 116 MB reconstructed gzip.

Use the already-committed chunks as the only durable snapshot transport.

If the Browser qualification environment cannot complete the exact public rehydration because of a proved infrastructure resource ceiling, return a governed BLOCK naming that ceiling.

Do not replace exact rehydration with receipts or a fake repository.

## Required outputs

Write only under:

`WORKER_RETURNS/EE-P2R6N/`

At minimum:

1. `00_RETURN.md`
2. `01_SNAPSHOT_RECONSTRUCTION_RECEIPT.json`
3. `02_R6A_POSITIVE_PROOF_DRIVER.py`
4. `03_R6A_PRODUCTION_RUNTIME_PROOF.json`
5. `04_BROWSER_QUALIFICATION_RECEIPT.json`

No large reconstructed snapshot output is committed.

## PASS terminal

`EE_P2R6N_PASS__BANKED_A5F36_BINDING_ACCEPTED_BY_EXACT_PRODUCTION_R6A_AGAINST_PUBLICLY_REHYDRATED_ADOPTED_R6L_RELEASE__INACTIVE_PENDING_HQ_ADOPTION`

PASS wakes HQ corrected-binding adjudication only.

## BLOCK terminal

`EE_P2R6N_BLOCK__<EXACT_FIRST_SNAPSHOT_RECONSTRUCTION_REHYDRATION_AUTHORITY_OR_PRODUCTION_RUNTIME_FAILURE>`

## Hard forbidden

- no Library/carrier/source access;
- no binding preimage recomputation or mutation;
- no binding activation/adoption;
- no alternate/fake repository;
- no private validation seal;
- no R6A weakening;
- no A/B qualification;
- no BE1;
- no P2X;
- no Candidate-C repair;
- no D02/F02 workload mutation;
- no Lock1/Lock2 mutation;
- no MAIN or semantic PRE-MAIN mutation;
- no rebase;
- no replacement branch.

Run governed Browser qualification.

Commit and push the exact branch.

Report PASS/BLOCK, final tip, reconstructed snapshot identities, exact returned release ref, banked binding hash, production runtime proof disposition, qualification run/job/artifact identities, and wake.

Return to HQ.
