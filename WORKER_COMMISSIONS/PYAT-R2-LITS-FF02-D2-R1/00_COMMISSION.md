# PYAT R2 — LiTS FF02-D2 retained-checkpoint exact preimage export — R1

Repository: `maidiu/rawlsing`

Branch:
`agent/rabochii-pyat-r2-lits-ff02-d2-checkpoint-preimage-export-r1`

Exact parent HQ join:
`72aa6124c21bbedba586c738665284bddb3c8d25`

Agent type:
`LOCAL RETAINED-CHECKPOINT EXECUTION / METADATA EXTRACTION ONLY`

This is the retry of FF02-D after D proved a custody/location blocker on an execution surface that did not contain the retained checkpoint.

## Read first

1. `PYAT_R2_LITS_FF02_DE_FANIN_R1/00_HQ_JOIN.md`
2. `PYAT_R2_LITS_FF02_DE_FANIN_R1/01_D2_EXECUTION_HANDOFF.md`
3. `WORKER_RETURNS/PYAT-R2-LITS-FF02-D-R1/00_RETURN.md`
4. `WORKER_RETURNS/PYAT-R2-LITS-FF02-C-R1/09_EXACT_BLOCKER_INVENTORY.tsv`

Do not redo FF02-A, B, C, D or E reasoning.

## Mission

Locate the already-retained exact checkpoint file:

`current_i05_materialization_checkpoint_v3.json`

on the execution surface where the successful LiTS canonical materialization/checkpoint was retained.

Before reading its semantic body, compute its SHA-256.

Required exact document SHA-256:

`2704fd3fadc9c898a512183aaf5eebf0ca48d78c47e75a19d47e17281eaa5726`

Required checkpoint identity:

`3fab15f37db629f0ee24189620c65eff944d8a36c4b4509abb6b8bb2ea69c33f`

Required canonical closure:

`f264dd8f83a0794716583d1ea8445947cc9470b99475e5d51fc2383e7196f415`

If the file is not found or the document SHA does not match exactly, STOP with the block terminal below.

If it matches, read only what is required from:

`/material/canonical_empirical_object_closure`

including:

- `public_object_preimages`
- `preimage_fragments`

and any already-retained exact binding material needed to project the commissioned documentary rows.

## Required outputs

Produce and bank:

### 1. Candidate → receipt bindings

Exactly 50 rows:

`candidate_hash -> DiscoveryResultReceipt.ref`

For each receipt also export:

- `authority_snapshot_refs`
- `dependency_refs`
- `winning_predicate_ref`
- `source_release_refs`
- replay ref

### 2. Full AuthoritySnapshot closure

Exactly 24 retained AuthoritySnapshot exact refs, with the exact underlying AuthorityRef triples carried by their preimages.

### 3. Per-object authority bindings

Export exact `authority_snapshot_refs` for the retained:

- 60 `EmpiricalFact`
- 63 `EmpiricalQuerySpec`
- 35 `EmpiricalPredicate`
- 50 `DiscoveryResultReceipt`

No family-level substitution.

### 4. P2 memberwise logical bindings

Export either:

- the already-qualified 50 `cross_schema_logical_candidate_bindings` rows, including all 18 P2 memberwise mappings;

or, if those rows are not directly retained,

- the exact retained predicate preimages necessary to reproduce the already-qualified P2 memberwise logical mapping source-free.

Do not reconstruct P2 by counts, frequencies, labels or nearest matching.

### 5. Verification receipt

Prove:

- observed checkpoint path;
- observed byte size;
- observed SHA-256 == governed SHA-256;
- checkpoint identity == governed identity;
- canonical closure identity == governed closure;
- every exported row is an exact projection of retained checkpoint material;
- zero reconstructed semantic rows;
- no source, decoder, I03/I05 or candidate execution was used.

## Hard prohibitions

DO NOT:

- open/materialize/read raw LiTS source bytes;
- invoke a source decoder;
- rerun I03;
- rerun I05;
- run Candidate A/B/C;
- run P2X;
- infer semantics from values, labels, counts or frequencies;
- use D04/FF01 as current truth;
- substitute the Git oracle for missing exact checkpoint preimages;
- mutate production code;
- mint Field Forge semantic authority;
- create or current-select relation objects;
- perform PRE-V3 admission;
- touch PRE-V3→V3.

This lane is extraction only.

## Return directory

Own only:

`WORKER_RETURNS/PYAT-R2-LITS-FF02-D2-R1/`

Required files:

- `00_RETURN.md`
- `01_CANDIDATE_RECEIPT_BINDINGS.tsv`
- `02_AUTHORITY_SNAPSHOT_CLOSURE.tsv`
- `03_PER_OBJECT_AUTHORITY_BINDINGS.tsv`
- `04_P2_LOGICAL_BINDINGS.tsv`
- `05_CHECKPOINT_EXPORT_VERIFICATION.json`
- `06_B001_B002_B003_CLOSURE.tsv`

## Pass criteria

PASS only if all are true:

- exact checkpoint file found;
- SHA-256 exact match;
- 50/50 candidate→receipt rows;
- 24/24 AuthoritySnapshot exact preimages;
- all required per-object authority bindings exact;
- P2 memberwise mapping exact and non-inferred;
- B001/B002/B003 all closed;
- zero prohibited execution.

Pass terminal:

`PYAT_R2_LITS_FF02_D2_PASS__CHECKPOINT_ONLY_EXACT_PREIMAGE_EXPORT_COMPLETE__B001_B002_B003_CLOSED__NO_SOURCE_REOPEN`

Block terminal:

`PYAT_R2_LITS_FF02_D2_BLOCKED__EXACT_RETAINED_CHECKPOINT_NOT_FOUND_OR_HASH_MISMATCH__NO_SUBSTITUTION`
