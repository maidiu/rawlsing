# LAUNCH IN: OpenCode — Space Bunny Free
# ROLE: PYAT R2 — LiTS FF02-D2M LOCAL RETAINED-CHECKPOINT EXPORT — R1
# REPOSITORY: maidiu/rawlsing

Branch:
`agent/opencode-pyat-hq174-lits-d2m-local-checkpoint-export-r1`

Exact branch base:
`6d23470ba406e1edc7efad1163a7cde87b9ef230`

This is the exact local-surface successor to the blocked FF02-D2 return.

Read first:

- `WORKER_COMMISSIONS/PYAT-R2-LITS-FF02-D2-R1/00_COMMISSION.md`
- `WORKER_RETURNS/PYAT-R2-LITS-FF02-D2-R1/00_RETURN.md @ 6d23470ba406e1edc7efad1163a7cde87b9ef230`

The previous D2 worker stopped correctly because its execution surface could not see the retained checkpoint bytes.

HQ now designates the governed local custody path as the execution surface for this exact checkpoint-only extraction.

## Exact retained checkpoint

Path:

`/Users/matthewsmith/Desktop/Rawlsing/LOCAL_CUSTODY/PREMAIN-FIABC-LITS-FINAL-SUCCESS-DURABLE-CUSTODY-R1/payload/PREMAIN-FIABC-LITS-FINAL-CANONICAL-CLOSURE-SOURCE-RETRY-R1/court/oracle_producers/LITS_I/current_i05_materialization_checkpoint_v3.json`

Expected byte size:

`3404445161`

Required document SHA-256:

`2704fd3fadc9c898a512183aaf5eebf0ca48d78c47e75a19d47e17281eaa5726`

Required checkpoint identity:

`3fab15f37db629f0ee24189620c65eff944d8a36c4b4509abb6b8bb2ea69c33f`

Required canonical closure:

`f264dd8f83a0794716583d1ea8445947cc9470b99475e5d51fc2383e7196f415`

## Mission

Execute the original FF02-D2 extraction law on the actual retained checkpoint.

Before any semantic dereference:

1. verify the exact path exists;
2. record observed file size;
3. compute SHA-256 by streaming the file;
4. require exact equality to the governed SHA above.

If any of these fail, stop with the original block terminal.

Only after exact hash verification may you read the minimal retained material needed from:

`/material/canonical_empirical_object_closure`

including:
- `public_object_preimages`
- `preimage_fragments`
- exact already-retained binding material needed for the commissioned rows.

## Required exports

Produce:

1. exactly 50 candidate_hash → DiscoveryResultReceipt.ref rows, including each receipt's:
   - authority_snapshot_refs
   - dependency_refs
   - winning_predicate_ref
   - source_release_refs
   - replay ref

2. exactly 24 AuthoritySnapshot exact refs with exact underlying AuthorityRef triples;

3. per-object exact authority_snapshot_refs for:
   - 60 EmpiricalFact
   - 63 EmpiricalQuerySpec
   - 35 EmpiricalPredicate
   - 50 DiscoveryResultReceipt

4. exact P2 memberwise logical bindings:
   - preferably the retained 50 cross_schema_logical_candidate_bindings rows including all 18 P2 mappings;
   - otherwise only exact retained predicate preimages sufficient to reproduce the already-qualified mapping source-free.

5. closure of B001/B002/B003 with exact retained evidence.

## Hard prohibitions

Do not:
- open/read/hash/stat raw LiTS source data;
- invoke any source decoder;
- run I03 or I05;
- run Candidate A/B/C;
- run P2X;
- infer semantics from values, counts, labels or frequencies;
- reconstruct missing semantics from Git/oracle artifacts;
- mutate production code;
- touch PRE-V3→V3.

This lane reads exactly one retained checkpoint payload and nothing else outside normal repo/control artifacts.

## Return directory

Write only:

`WORKER_RETURNS/PYAT-R2-LITS-FF02-D2M-LOCAL-R1/**`

Required:

- `00_RETURN.md`
- `01_CANDIDATE_RECEIPT_BINDINGS.tsv`
- `02_AUTHORITY_SNAPSHOT_CLOSURE.tsv`
- `03_PER_OBJECT_AUTHORITY_BINDINGS.tsv`
- `04_P2_LOGICAL_BINDINGS.tsv`
- `05_CHECKPOINT_EXPORT_VERIFICATION.json`
- `06_B001_B002_B003_CLOSURE.tsv`
- `07_FINAL_DISPOSITION.json`

PASS only if:
- exact path found;
- observed size exact;
- SHA exact;
- 50/50 receipt bindings;
- 24/24 snapshot closure;
- all required per-object bindings exact;
- P2 memberwise bindings exact and non-inferred;
- B001/B002/B003 closed;
- zero raw-source access.

Allowed:

- `PASS_D2M_LOCAL_CHECKPOINT_EXPORT__B001_B002_B003_CLOSED__INDEPENDENT_REVIEW_REQUIRED`
- `D2M_LOCAL_CHECKPOINT_NOT_FOUND_OR_HASH_MISMATCH__HQ_ADJUDICATION_REQUIRED`
- `D2M_RETAINED_PREIMAGE_CONTENT_GAP__HQ_ADJUDICATION_REQUIRED`

No self-adoption.

Terminal:
`D2M_LOCAL_CHECKPOINT_EXPORT_RETURNED__HQ_ADJUDICATION_REQUIRED`
