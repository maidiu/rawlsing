# PYAT R2 — FF02-D2 exact execution handoff

Purpose: rerun the already-defined FF02-D metadata extraction on an execution surface that actually has the retained checkpoint file.

This is a custody completion, not a new semantic or empirical court.

## Required checkpoint

Filename:
`current_i05_materialization_checkpoint_v3.json`

Required document SHA-256:
`2704fd3fadc9c898a512183aaf5eebf0ca48d78c47e75a19d47e17281eaa5726`

Required checkpoint identity:
`3fab15f37db629f0ee24189620c65eff944d8a36c4b4509abb6b8bb2ea69c33f`

Required canonical closure:
`f264dd8f83a0794716583d1ea8445947cc9470b99475e5d51fc2383e7196f415`

Read only the retained canonical empirical object closure needed to project the commissioned metadata.

## Required outputs

- exact 50 candidate_hash -> DiscoveryResultReceipt.ref bindings;
- complete receipt authority/dependency/winning-predicate/source-release/replay refs;
- all 24 AuthoritySnapshot exact refs + AuthorityRef triples;
- per-object authority_snapshot_refs for retained facts, queries, predicates and receipts;
- exact P2 logical bindings or exact retained predicate preimages sufficient for the already-qualified memberwise mapping;
- checkpoint-only identity/replay verification.

## Hard stop

If the exact checkpoint is not found or its SHA-256 does not match, stop. Do not substitute:
- raw LiTS source;
- another checkpoint;
- Git oracle pools;
- D04/FF01;
- count/label/frequency reconstruction;
- I03/I05 rerun.

The desired terminal is:

`PYAT_R2_LITS_FF02_D2_PASS__CHECKPOINT_ONLY_EXACT_PREIMAGE_EXPORT_COMPLETE__B001_B002_B003_CLOSED__NO_SOURCE_REOPEN`
