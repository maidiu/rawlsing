# PYAT R2 — LiTS FF02-D checkpoint-only final-preimage export — R1

Repository: `maidiu/rawlsing`

Branch: `agent/rabochii-pyat-r2-lits-ff02-d-checkpoint-preimage-export-r1`

Exact parent fan-in:
`d43de2ec39fa0a5159674a98933c6a5b050a1788`

Agent type:
`LOCAL CHECKPOINT-CAPABLE EXECUTION / METADATA EXTRACTION ONLY`

This is **not** a raw-source lane and **not** an empirical rerun.

## Governing evidence

Read first:

- `PYAT_R2_LITS_FF02_FANIN_R1/00_HQ_JOIN.md`
- `PYAT_R2_LITS_FF02_FANIN_R1/01_CROSS_EXAMINATION.md`
- `PYAT_R2_LITS_FF02_FANIN_R1/02_NEXT_PROGRAM.md`

Then consume the exact worker returns:

- FF02-A: commit `8ecf148a3548ea94e9fd525e917ca2c098794294`
- FF02-B: commit `a6e7a02132abe1bfc85f803292218cfa7ba525c0`
- FF02-C: commit `9567284ea1e97c5bf5d587523ec92be01138683f`

FF02-C controls the missing-preimage specification.

## Exact retained identities

- canonical closure:
  `f264dd8f83a0794716583d1ea8445947cc9470b99475e5d51fc2383e7196f415`
- checkpoint identity:
  `3fab15f37db629f0ee24189620c65eff944d8a36c4b4509abb6b8bb2ea69c33f`
- checkpoint document SHA-256:
  `2704fd3fadc9c898a512183aaf5eebf0ca48d78c47e75a19d47e17281eaa5726`
- frozen oracle:
  `e5d66db4b6f8339672b0f4828b72a8df68b5525bf71ecfda899d0531d618a98a`

The retained checkpoint slice required is:
`current_i05_materialization_checkpoint_v3.json#/material/canonical_empirical_object_closure`
including `public_object_preimages` and `preimage_fragments`.

## Mission

Export and bank the exact missing documentary preimages required to close FF02-C blockers B001–B003.

Produce:

1. all 50 `candidate_hash -> DiscoveryResultReceipt.ref` bindings;
2. for each retained DiscoveryResultReceipt:
   - `authority_snapshot_refs`;
   - `dependency_refs`;
   - `winning_predicate_ref`;
   - `source_release_refs`;
   - exact replay ref;
3. all 24 retained AuthoritySnapshot exact refs and their underlying AuthorityRef triples;
4. per-object `authority_snapshot_refs` for:
   - 60 EmpiricalFact;
   - 63 EmpiricalQuerySpec;
   - 35 EmpiricalPredicate;
   - 50 DiscoveryResultReceipt;
5. either:
   - all 50 already-qualified `cross_schema_logical_candidate_bindings` rows,
   - or exact retained predicate preimages sufficient to reproduce the memberwise P2 mapping source-free;
6. exact content/replay verification proving every exported row is a projection of the retained checkpoint and not a reconstruction from counts, labels, historical compact products or source inference.

## Hard prohibitions

- DO NOT open or materialize raw LiTS source.
- DO NOT decode source.
- DO NOT run I03.
- DO NOT run I05.
- DO NOT run Candidate A/B/C.
- DO NOT run P2X.
- DO NOT infer semantics from values, labels or frequencies.
- DO NOT mutate production code.
- DO NOT mint Field Forge relation authority.
- DO NOT create positive structural relations.
- DO NOT use historical D04/FF01 as current source of truth.

## Required failure law

If the exact retained checkpoint cannot be located or its document SHA-256 does not equal the governed hash, stop with an exact custody/location blocker.

Do not substitute any older checkpoint, compact oracle, raw source, or reconstructed equivalent.

## Return

Own only:

`WORKER_RETURNS/PYAT-R2-LITS-FF02-D-R1/`

Minimum files:

- `00_RETURN.md`
- `01_CANDIDATE_RECEIPT_BINDINGS.tsv`
- `02_AUTHORITY_SNAPSHOT_CLOSURE.tsv`
- `03_PER_OBJECT_AUTHORITY_BINDINGS.tsv`
- `04_P2_LOGICAL_BINDINGS.tsv`
- `05_CHECKPOINT_EXPORT_VERIFICATION.json`
- `06_BLOCKER_DISPOSITION.tsv`

Success terminal:

`PYAT_R2_LITS_FF02_D_PASS__CHECKPOINT_ONLY_EXACT_PREIMAGE_EXPORT_COMPLETE__B001_B002_B003_CLOSED__NO_SOURCE_REOPEN`

Block terminal:

`PYAT_R2_LITS_FF02_D_BLOCKED__EXACT_CHECKPOINT_CUSTODY_OR_PREIMAGE_EXPORT_FAILURE__NO_SUBSTITUTION`
