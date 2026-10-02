# LAUNCH IN: OpenCode — Space Bunny Free — OTHER MACHINE
# ROLE: PYAT R2 — LiTS D2X OTHER-MACHINE RETAINED-CHECKPOINT EXACT PREIMAGE EXPORT — R1
# REPOSITORY: maidiu/rawlsing

Branch:
`agent/opencode-pyat-hq176-lits-d2x-other-machine-checkpoint-export-r1`

Exact branch base:
`55e334ba419cb88cc7e491a8e0c74a2d9fe1f498`

This is the successor to the blocked D2/D2M custody lanes.

The user has now established that the governed retained checkpoint was stored on **another machine**.

Your job is to run the exact checkpoint-only export on that machine.

Do **not** reopen LiTS raw source data.
Do **not** rerun I03/I05.
Do **not** run Candidate A/B/C.
Do **not** run P2X.
Do **not** reconstruct semantic rows from Git summaries.
Do **not** mutate production code.

## Read first

From the repo, read:

- `WORKER_COMMISSIONS/PYAT-R2-LITS-FF02-D2-R1/00_COMMISSION.md`
- `WORKER_RETURNS/PYAT-R2-LITS-FF02-D2-R1/00_RETURN.md @ 6d23470ba406e1edc7efad1163a7cde87b9ef230`
- `WORKER_RETURNS/PYAT-R2-LITS-FF02-D2M-LOCAL-R1/00_RETURN.md @ 55e334ba419cb88cc7e491a8e0c74a2d9fe1f498`
- `WORKER_RETURNS/PREMAIN-FIABC-LITS-FINAL-SUCCESS-DURABLE-CUSTODY-R1/custody_manifest.json`

Do not redo FF02-A/B/C/D/E reasoning.

## Exact retained artifact to locate

Filename:

`current_i05_materialization_checkpoint_v3.json`

Required byte size:

`3404445161`

Required document SHA-256:

`2704fd3fadc9c898a512183aaf5eebf0ca48d78c47e75a19d47e17281eaa5726`

Required checkpoint identity:

`3fab15f37db629f0ee24189620c65eff944d8a36c4b4509abb6b8bb2ea69c33f`

Required canonical closure:

`f264dd8f83a0794716583d1ea8445947cc9470b99475e5d51fc2383e7196f415`

Historical governed persistent relative location under the Rawlsing repo root:

`LOCAL_CUSTODY/PREMAIN-FIABC-LITS-FINAL-SUCCESS-DURABLE-CUSTODY-R1/payload/PREMAIN-FIABC-LITS-FINAL-CANONICAL-CLOSURE-SOURCE-RETRY-R1/court/oracle_producers/LITS_I/current_i05_materialization_checkpoint_v3.json`

The absolute repo root on this other machine may differ. Resolve it from the checkout you are running in; do not assume the old machine's absolute `/Users/matthewsmith/Desktop/Rawlsing` prefix.

## PHASE 0 — machine/repo/custody lock

1. Record:
   - hostname;
   - OS/version;
   - architecture;
   - exact repository root;
   - checked-out branch;
   - HEAD.
2. Verify HEAD is exactly the commissioned branch tip or a descendant containing only this commission/return work.
3. Resolve the expected checkpoint path by joining the current repo root to the governed relative path above.
4. If that exact path exists, use it.
5. If it does not, perform only a **targeted checkpoint search** on this machine:
   - search for the exact filename `current_i05_materialization_checkpoint_v3.json`;
   - search for directories named `LOCAL_CUSTODY`;
   - search for directories matching `*PREMAIN-FIABC-LITS-FINAL-SUCCESS-DURABLE-CUSTODY-R1*`;
   - restrict searches to likely Rawlsing/project storage locations on this machine.
6. Do not perform a broad size-based filesystem sweep.
7. Do not stat/hash/open unrelated large files.
8. Once one candidate checkpoint is located, stop searching and enter the exact identity gate.

If no candidate checkpoint can be located:
`D2X_OTHER_MACHINE_CHECKPOINT_NOT_FOUND__HQ_ADJUDICATION_REQUIRED`

## PHASE 1 — exact checkpoint identity gate

Before any semantic dereference:

1. record the observed absolute checkpoint path;
2. record observed byte size;
3. require exactly `3404445161`;
4. stream-compute SHA-256;
5. require exact equality to:
   `2704fd3fadc9c898a512183aaf5eebf0ca48d78c47e75a19d47e17281eaa5726`.

If size or SHA mismatches, STOP:

`D2X_OTHER_MACHINE_CHECKPOINT_IDENTITY_MISMATCH__HQ_ADJUDICATION_REQUIRED`

Do not inspect the body of a mismatched file.

## PHASE 2 — exact retained semantic projection only

After the exact hash passes, read only the minimum required retained checkpoint material from:

`/material/canonical_empirical_object_closure`

including:

- `public_object_preimages`
- `preimage_fragments`
- exact already-retained binding material needed to project the commissioned rows.

Do not inspect unrelated checkpoint content.

## Required exports

### 1. Candidate → receipt bindings

Exactly 50 rows:

`candidate_hash -> DiscoveryResultReceipt.ref`

For each receipt export:

- `authority_snapshot_refs`
- `dependency_refs`
- `winning_predicate_ref`
- `source_release_refs`
- replay ref

### 2. Full AuthoritySnapshot closure

Exactly 24 retained `AuthoritySnapshot` exact refs with exact underlying `AuthorityRef` triples.

### 3. Per-object authority bindings

Export exact `authority_snapshot_refs` for:

- 60 `EmpiricalFact`
- 63 `EmpiricalQuerySpec`
- 35 `EmpiricalPredicate`
- 50 `DiscoveryResultReceipt`

No family-level substitution.

### 4. P2 memberwise logical bindings

Export either:

- the already-retained 50 `cross_schema_logical_candidate_bindings` rows, including all 18 P2 memberwise mappings;

or, only if those rows are not directly retained:

- the exact retained predicate preimages necessary to reproduce the already-qualified P2 memberwise logical mapping source-free.

Do not reconstruct P2 from values, counts, frequencies, labels, or nearest matching.

### 5. B001/B002/B003 closure

Return exact closure evidence for:

- `B001` — candidate -> DiscoveryResultReceipt exact refs;
- `B002` — 24 AuthoritySnapshot closure + per-object authority bindings;
- `B003` — exact memberwise P2 logical bindings / retained predicate preimages.

## PHASE 3 — checkpoint custody receipt

Record:

- actual machine/hostname;
- actual absolute checkpoint path;
- observed size;
- observed SHA-256;
- governed expected size/hash;
- checkpoint identity;
- canonical closure identity;
- whether the historical relative `LOCAL_CUSTODY/.../current_i05_materialization_checkpoint_v3.json` layout is preserved on this machine;
- whether this machine is now the authoritative reachable custody surface for this payload.

Do **not** copy the 3.4 GB checkpoint into Git.

Do **not** move it to the other machine unless separately commissioned.

The small extracted TSV/JSON return artifacts should be committed and pushed normally.

## Hard prohibitions

Zero:

- raw LiTS DTA/source reads;
- raw source hashing/statting;
- source decoder;
- I03/I05;
- Candidate A/B/C;
- measured P2X;
- semantic inference from observed source values;
- Git-oracle substitution for retained preimages;
- production mutation;
- PRE-V3 admission;
- PRE-V3→V3 work.

The only large payload authorized for read/hash is the exact retained checkpoint after it is located.

## Return directory

Write only:

`WORKER_RETURNS/PYAT-R2-LITS-D2X-OTHER-MACHINE-R1/**`

Required:

- `00_RETURN.md`
- `01_MACHINE_AND_CUSTODY_RECEIPT.json`
- `02_CANDIDATE_RECEIPT_BINDINGS.tsv`
- `03_AUTHORITY_SNAPSHOT_CLOSURE.tsv`
- `04_PER_OBJECT_AUTHORITY_BINDINGS.tsv`
- `05_P2_LOGICAL_BINDINGS.tsv`
- `06_B001_B002_B003_CLOSURE.tsv`
- `07_CHECKPOINT_EXPORT_VERIFICATION.json`
- `08_FINAL_DISPOSITION.json`

## PASS criteria

PASS only if all are true:

- exact checkpoint located;
- size = 3404445161;
- SHA-256 exact;
- checkpoint identity exact;
- canonical closure identity exact;
- 50/50 candidate→receipt rows;
- 24/24 AuthoritySnapshot exact refs;
- all required per-object authority bindings exact;
- P2 memberwise mapping exact and non-inferred;
- B001/B002/B003 all closed;
- zero prohibited execution.

Allowed dispositions:

- `PASS_D2X_OTHER_MACHINE_CHECKPOINT_EXPORT__B001_B002_B003_CLOSED__INDEPENDENT_REVIEW_REQUIRED`
- `D2X_OTHER_MACHINE_CHECKPOINT_NOT_FOUND__HQ_ADJUDICATION_REQUIRED`
- `D2X_OTHER_MACHINE_CHECKPOINT_IDENTITY_MISMATCH__HQ_ADJUDICATION_REQUIRED`
- `D2X_RETAINED_PREIMAGE_CONTENT_GAP__HQ_ADJUDICATION_REQUIRED`

No self-adoption.

Terminal:

`D2X_OTHER_MACHINE_CHECKPOINT_EXPORT_RETURNED__HQ_ADJUDICATION_REQUIRED`
