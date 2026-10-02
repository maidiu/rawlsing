# LAUNCH IN: OpenCode — Space Bunny Free
# ROLE: PYAT R2 — LiTS D2R EPHEMERAL-ORIGIN RECOVERY + EXACT PREIMAGE EXPORT — R1
# REPOSITORY: maidiu/rawlsing

Branch:
`agent/opencode-pyat-hq175-lits-d2r-ephemeral-recovery-export-r1`

Exact base:
`55e334ba419cb88cc7e491a8e0c74a2d9fe1f498`

This is the custody-recovery successor to D2M.

Read exactly:

- `WORKER_RETURNS/PYAT-R2-LITS-FF02-D2M-LOCAL-R1/00_RETURN.md`
- `WORKER_RETURNS/PREMAIN-FIABC-LITS-FINAL-SUCCESS-DURABLE-CUSTODY-R1/custody_manifest.json`
- `WORKER_RETURNS/PREMAIN-FIABC-LITS-FINAL-SUCCESS-DURABLE-CUSTODY-R1/ephemeral_copy_verification.json`

Do not redo semantic archaeology.

## Governing custody fact

The durable-custody verification records a byte-identical copy from this exact original tree:

`/private/tmp/fiabc-lits-final-canonical-closure-source-retry-r1/WORKER_RETURNS/PREMAIN-FIABC-LITS-FINAL-CANONICAL-CLOSURE-SOURCE-RETRY-R1`

to the now-missing persistent tree:

`/Users/matthewsmith/Desktop/Rawlsing/LOCAL_CUSTODY/PREMAIN-FIABC-LITS-FINAL-SUCCESS-DURABLE-CUSTODY-R1/payload/PREMAIN-FIABC-LITS-FINAL-CANONICAL-CLOSURE-SOURCE-RETRY-R1`

The original copy-verification receipt states:

- 35 regular files
- 36 directories
- total regular-file bytes `3405790125`
- all regular files byte-identical between original and persistent copy
- checkpoint bytes `3404445161`
- checkpoint SHA-256 `2704fd3fadc9c898a512183aaf5eebf0ca48d78c47e75a19d47e17281eaa5726`

Exact checkpoint relative path:

`court/oracle_producers/LITS_I/current_i05_materialization_checkpoint_v3.json`

## Mission

Attempt recovery **only from the already-retained ephemeral origin recorded by the accepted custody manifest**.

This is not a raw-source recovery task.

No LiTS DTA/source file may be searched, opened, hashed, statted, decoded or inspected.

## PHASE 0 — exact origin-path gate

Check only the exact governed original tree first:

`/private/tmp/fiabc-lits-final-canonical-closure-source-retry-r1/WORKER_RETURNS/PREMAIN-FIABC-LITS-FINAL-CANONICAL-CLOSURE-SOURCE-RETRY-R1`

and exact checkpoint:

`/private/tmp/fiabc-lits-final-canonical-closure-source-retry-r1/WORKER_RETURNS/PREMAIN-FIABC-LITS-FINAL-CANONICAL-CLOSURE-SOURCE-RETRY-R1/court/oracle_producers/LITS_I/current_i05_materialization_checkpoint_v3.json`

If absent, you may enumerate only:

- `/private/tmp/fiabc-lits-final-canonical-closure-source-retry-r1`
- its immediate descendants needed to determine whether the exact return tree was renamed or nested one level differently;
- `/private/tmp` names matching exactly `*fiabc-lits-final-canonical-closure-source-retry-r1*`.

Do not perform another broad filesystem search.

If no exact retained origin is recoverable:
return
`D2R_EPHEMERAL_ORIGIN_ABSENT__HQ_CUSTODY_RECOVERY_REQUIRED`.

## PHASE 1 — checkpoint identity gate

If the exact checkpoint is present:

1. record observed byte size;
2. require `3404445161`;
3. stream SHA-256;
4. require exact:
   `2704fd3fadc9c898a512183aaf5eebf0ca48d78c47e75a19d47e17281eaa5726`.

Do not open semantic content before the exact hash passes.

If size/hash mismatches:
`D2R_EPHEMERAL_CHECKPOINT_IDENTITY_MISMATCH__HQ_ADJUDICATION_REQUIRED`.

## PHASE 2 — recover durable custody

After checkpoint identity passes, recreate the governed durable custody root:

`/Users/matthewsmith/Desktop/Rawlsing/LOCAL_CUSTODY/PREMAIN-FIABC-LITS-FINAL-SUCCESS-DURABLE-CUSTODY-R1/`

Copy the exact retained return tree from the governed ephemeral origin to:

`payload/PREMAIN-FIABC-LITS-FINAL-CANONICAL-CLOSURE-SOURCE-RETRY-R1`

Use a copy method that preserves bytes and does not transform content.

Then verify against the Git-banked `ephemeral_copy_verification.json` / `file_hash_manifest.json`:

- exact regular-file count;
- exact total bytes;
- exact checkpoint size/hash;
- all listed file hashes where practical;
- at minimum every `required_artifacts` entry from `ephemeral_copy_verification.json`.

Do not overwrite an unexpected pre-existing payload silently; if conflicting content appears, stop.

## PHASE 3 — execute D2M export from restored checkpoint

Once the persistent copy is restored and independently verified, execute the exact original D2M semantic extraction law against the restored checkpoint.

Read only what is required from:

`/material/canonical_empirical_object_closure`

including:
- `public_object_preimages`
- `preimage_fragments`
- exact retained binding material needed for the commissioned rows.

Export:

1. 50 candidate_hash → DiscoveryResultReceipt.ref rows with:
   - authority_snapshot_refs
   - dependency_refs
   - winning_predicate_ref
   - source_release_refs
   - replay ref

2. 24 AuthoritySnapshot exact refs with exact AuthorityRef triples;

3. per-object authority_snapshot_refs for:
   - 60 EmpiricalFact
   - 63 EmpiricalQuerySpec
   - 35 EmpiricalPredicate
   - 50 DiscoveryResultReceipt

4. exact P2 memberwise logical bindings:
   - 50 cross_schema_logical_candidate_bindings rows including all 18 P2 mappings; or
   - exact retained predicate preimages sufficient to reproduce the already-qualified mapping source-free.

5. explicit B001/B002/B003 closure evidence.

No reconstruction from counts, labels, frequencies or Git oracle summaries.

## Hard prohibitions

Do not:

- search for or inspect raw LiTS source data;
- open/hash/stat/decode the LiTS DTA;
- invoke source decoder;
- rerun I03/I05;
- run Candidate A/B/C;
- run P2X;
- infer semantics from values/counts/labels/frequencies;
- mutate production code;
- touch PRE-V3→V3.

The only large payload authorized is the exact retained checkpoint identified by governed SHA-256.

## Return

Write only:

`WORKER_RETURNS/PYAT-R2-LITS-D2R-EPHEMERAL-RECOVERY-R1/**`

Required:

- `00_RETURN.md`
- `01_ORIGIN_RECOVERY_RECEIPT.json`
- `02_DURABLE_CUSTODY_RESTORE_RECEIPT.json`
- `03_CANDIDATE_RECEIPT_BINDINGS.tsv`
- `04_AUTHORITY_SNAPSHOT_CLOSURE.tsv`
- `05_PER_OBJECT_AUTHORITY_BINDINGS.tsv`
- `06_P2_LOGICAL_BINDINGS.tsv`
- `07_B001_B002_B003_CLOSURE.tsv`
- `08_FINAL_DISPOSITION.json`

Allowed:

- `PASS_D2R_EPHEMERAL_RECOVERY_AND_PREIMAGE_EXPORT__B001_B002_B003_CLOSED__INDEPENDENT_REVIEW_REQUIRED`
- `D2R_EPHEMERAL_ORIGIN_ABSENT__HQ_CUSTODY_RECOVERY_REQUIRED`
- `D2R_EPHEMERAL_CHECKPOINT_IDENTITY_MISMATCH__HQ_ADJUDICATION_REQUIRED`
- `D2R_DURABLE_RESTORE_CONFLICT__HQ_ADJUDICATION_REQUIRED`
- `D2R_RETAINED_PREIMAGE_CONTENT_GAP__HQ_ADJUDICATION_REQUIRED`

No self-adoption.

Terminal:
`D2R_EPHEMERAL_RECOVERY_RETURNED__HQ_ADJUDICATION_REQUIRED`
