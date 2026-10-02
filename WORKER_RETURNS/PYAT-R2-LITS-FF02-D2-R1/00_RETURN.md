# PYAT R2 — LiTS FF02-D2 retained-checkpoint exact preimage export — R1

## Terminal

`PYAT_R2_LITS_FF02_D2_BLOCKED__EXACT_RETAINED_CHECKPOINT_NOT_FOUND_OR_HASH_MISMATCH__NO_SUBSTITUTION`

## Exact worker identity

- repository: `maidiu/rawlsing`
- branch: `agent/rabochii-pyat-r2-lits-ff02-d2-checkpoint-preimage-export-r1`
- commission tip: `59a6ed87fd7b91934164848a48a7a4ce86e95e4e`
- exact parent HQ join named by commission: `72aa6124c21bbedba586c738665284bddb3c8d25`
- governed checkpoint filename: `current_i05_materialization_checkpoint_v3.json`
- governed checkpoint identity: `3fab15f37db629f0ee24189620c65eff944d8a36c4b4509abb6b8bb2ea69c33f`
- governed checkpoint document SHA-256: `2704fd3fadc9c898a512183aaf5eebf0ca48d78c47e75a19d47e17281eaa5726`
- governed canonical closure: `f264dd8f83a0794716583d1ea8445947cc9470b99475e5d51fc2383e7196f415`

## Holding

The D2 commission's hard-stop law triggered at the checkpoint-custody step, before any semantic checkpoint dereference.

The exact retained checkpoint is documented by the governed durable-custody control plane, but its bytes are not exposed on this worker's execution surface. The custody manifest at governed repository state `bc207de1db6c1e48b81c7b27b2633ad1177077ff` records:

- checkpoint bytes: `3404445161`;
- checkpoint SHA-256: `2704fd3fadc9c898a512183aaf5eebf0ca48d78c47e75a19d47e17281eaa5726`;
- Git disposition: `PERSISTENT_LOCAL_HEAVYWEIGHT_PAYLOAD`;
- Git path: `null`;
- persistent path:
  `/Users/matthewsmith/Desktop/Rawlsing/LOCAL_CUSTODY/PREMAIN-FIABC-LITS-FINAL-SUCCESS-DURABLE-CUSTODY-R1/payload/PREMAIN-FIABC-LITS-FINAL-CANONICAL-CLOSURE-SOURCE-RETRY-R1/court/oracle_producers/LITS_I/current_i05_materialization_checkpoint_v3.json`.

That control-plane record proves where the retained payload was banked and that it was intentionally excluded from ordinary Git. It does **not** expose the checkpoint bytes to this worker and therefore cannot substitute for the commission's required fresh pre-read SHA-256 verification.

The exact checkpoint filename is absent from the current conversation/Project file surface, absent as an available Library file, absent from the current container filesystem probes, and absent as an ordinary Git blob. Consequently this worker cannot freshly compute the document SHA-256 or read `/material/canonical_empirical_object_closure`.

Per the commission: if the exact file is not found on the execution surface, stop. No Git-oracle, D04/FF01, count/frequency/label, or historical reconstruction is lawful.

## Read-first / governing evidence checked

- `PYAT_R2_LITS_FF02_DE_FANIN_R1/00_HQ_JOIN.md`
- `PYAT_R2_LITS_FF02_DE_FANIN_R1/01_D2_EXECUTION_HANDOFF.md`
- prior FF02-D return at `0d0c234efaa9e8985d82139cba2127d14e10baaa`
- FF02-C exact blocker inventory at `9567284ea1e97c5bf5d587523ec92be01138683f`
- durable-custody manifest:
  `WORKER_RETURNS/PREMAIN-FIABC-LITS-FINAL-SUCCESS-DURABLE-CUSTODY-R1/custody_manifest.json`
  at `bc207de1db6c1e48b81c7b27b2633ad1177077ff`

FF02-C's exact blockers remain open because D2 could not reach the checkpoint body:

- `B001`: 50 candidate -> DiscoveryResultReceipt exact-ref bindings;
- `B002`: full 24-snapshot closure and per-object authority bindings;
- `B003`: exact memberwise P2 logical bindings / required retained predicate preimages.

## Required export disposition

| required export | disposition |
|---|---|
| 50 candidate_hash -> DiscoveryResultReceipt.ref bindings | BLOCKED — checkpoint body unavailable on current execution surface |
| receipt authority/dependency/winning-predicate/source-release/replay refs | BLOCKED — checkpoint body unavailable |
| 24 AuthoritySnapshot refs + AuthorityRef triples | BLOCKED — checkpoint body unavailable |
| per-object authority_snapshot_refs for 60 facts / 63 queries / 35 predicates / 50 receipts | BLOCKED — checkpoint body unavailable |
| 50 cross-schema logical bindings or exact P2 predicate preimages | BLOCKED — checkpoint body unavailable |
| checkpoint-only content/replay verification | BLOCKED at exact file-location / fresh-hash gate |

The four export TSVs are intentionally header-only. Emitting semantic rows from the Git-banked oracle/control plane would violate the commission.

## Verification result

- exact checkpoint located on current execution surface: **NO**
- fresh observed checkpoint byte size: **NOT AVAILABLE**
- fresh observed checkpoint SHA-256: **NOT AVAILABLE**
- governed custody-record byte size: `3404445161`
- governed custody-record SHA-256: `2704fd3fadc9c898a512183aaf5eebf0ca48d78c47e75a19d47e17281eaa5726`
- checkpoint semantic body opened: **NO**
- canonical closure dereferenced: **NO**
- reconstructed semantic rows: **0**

This is an execution-surface custody/location block, not an observed hash mismatch.

## Prohibition audit

- raw LiTS source opened/materialized/read: **NO**
- source decoder invoked: **NO**
- I03 rerun: **NO**
- I05 rerun: **NO**
- Candidate A/B/C run: **NO**
- P2X run: **NO**
- semantics inferred from values/labels/counts/frequencies: **NO**
- D04/FF01 substituted as current truth: **NO**
- Git oracle substituted for missing checkpoint preimages: **NO**
- production code mutated: **NO**
- Field Forge semantic authority minted: **NO**
- relation objects created/current-selected: **NO**
- PRE-V3 admission performed: **NO**
- PRE-V3→V3 touched: **NO**

## Smallest lawful next action

Run this exact D2 commission on an execution surface that can directly read the already-retained checkpoint bytes at the governed durable-custody location (or on a surface to which that exact content-addressed checkpoint has been made available). First compute SHA-256 and require exact equality with the governed document hash; only then project the commissioned rows from `/material/canonical_empirical_object_closure`.

No LiTS source reopen, decoder, I03/I05 rerun, Candidate A/B/C execution, or semantic reconstruction is required or authorized.

## Terminal

`PYAT_R2_LITS_FF02_D2_BLOCKED__EXACT_RETAINED_CHECKPOINT_NOT_FOUND_OR_HASH_MISMATCH__NO_SUBSTITUTION`
