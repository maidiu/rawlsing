# PYAT R2 / FF02-D — checkpoint-only final-preimage export — R1

## Terminal

`PYAT_R2_LITS_FF02_D_BLOCKED__EXACT_CHECKPOINT_CUSTODY_OR_PREIMAGE_EXPORT_FAILURE__NO_SUBSTITUTION`

## Exact worker identity

- repository: `maidiu/rawlsing`
- branch: `agent/rabochii-pyat-r2-lits-ff02-d-checkpoint-preimage-export-r1`
- commission commit: `67c595a7b77c3ae01f3961318e6c8ae32f66f229`
- exact parent fan-in: `d43de2ec39fa0a5159674a98933c6a5b050a1788`
- governed checkpoint identity: `3fab15f37db629f0ee24189620c65eff944d8a36c4b4509abb6b8bb2ea69c33f`
- governed checkpoint document SHA-256: `2704fd3fadc9c898a512183aaf5eebf0ca48d78c47e75a19d47e17281eaa5726`
- governed canonical closure: `f264dd8f83a0794716583d1ea8445947cc9470b99475e5d51fc2383e7196f415`
- governed frozen oracle: `e5d66db4b6f8339672b0f4828b72a8df68b5525bf71ecfda899d0531d618a98a`
- return HEAD: reported externally after commit; cannot self-embed its own SHA.

## Holding

The commission's required failure law triggered **before any checkpoint dereference**.

The exact retained file:

`current_i05_materialization_checkpoint_v3.json`

was not present on the worker's accessible local filesystem surface, was not exposed as a current conversation/Project file, and was not discoverable as a standalone authorized Library file by exact filename or governed checkpoint identity.

The Git-visible repository contains the custody receipts and the commission/fan-in evidence proving that the checkpoint exists on the authorized retained execution surface, but it does not contain the 3.4GB checkpoint body itself. FF02-C already proved that the Git-visible oracle/control plane is insufficient for the required candidate→receipt pairing, full 24-snapshot enumeration, per-object authority bindings, and memberwise P2 logical bindings.

Therefore this worker does **not** substitute:
- the unordered DiscoveryResultReceipt ref pool in the oracle;
- historical D04/FF01 material;
- counts/labels/frequencies;
- reconstructed pairings;
- raw LiTS source;
- a new I03/I05 execution.

No requested preimage row is emitted as if checkpoint-derived.

## Custody probes performed

1. worker branch identity resolved exactly to commission commit `67c595a7b77c3ae01f3961318e6c8ae32f66f229`;
2. commission parent verified as `d43de2ec39fa0a5159674a98933c6a5b050a1788`;
3. bounded local filesystem search for the exact checkpoint filename and checkpoint/i05-materialization names returned no checkpoint file;
4. current conversation/Project file surface contains no checkpoint artifact;
5. bounded Library search for the exact checkpoint filename / governed checkpoint identity returned no exact checkpoint artifact;
6. Git evidence was consulted only to confirm the known custody boundary and missing-preimage specification.

Because the file itself was not located, its governed document SHA-256 could not be freshly recomputed by this worker. This is a **custody/location blocker**, not a hash mismatch.

## Required export disposition

| required export | disposition |
|---|---|
| 50 candidate_hash → DiscoveryResultReceipt.ref bindings | BLOCKED — exact checkpoint unavailable |
| receipt authority/dependency/winning-predicate/source-release/replay refs | BLOCKED — exact checkpoint unavailable |
| all 24 AuthoritySnapshot refs + AuthorityRef triples | BLOCKED — exact checkpoint unavailable |
| per-object authority_snapshot_refs for 60 facts / 63 queries / 35 predicates / 50 receipts | BLOCKED — exact checkpoint unavailable |
| 50 cross-schema logical bindings or exact P2 predicate preimages | BLOCKED — exact checkpoint unavailable |
| checkpoint-only content/replay verification | BLOCKED at initial file-custody step |

The four TSV export files are intentionally header-only. Filling them from Git/oracle inference would violate the commission.

## Prohibition audit

- raw LiTS source opened/materialized/read: **NO**
- decoder invoked: **NO**
- I03 run: **NO**
- I05 run: **NO**
- Candidate A/B/C run or state used: **NO**
- P2X run: **NO**
- semantic inference performed: **NO**
- production code mutated: **NO**
- Field Forge authority minted: **NO**
- positive structural relation created: **NO**
- historical D04/FF01 substituted as current truth: **NO**

## Smallest lawful next action

Run this exact commission on an execution surface that has the already-retained checkpoint file locally available. Before extraction, recompute SHA-256 over that file and require exact equality with:

`2704fd3fadc9c898a512183aaf5eebf0ca48d78c47e75a19d47e17281eaa5726`.

If it matches, read only:

`#/material/canonical_empirical_object_closure/{public_object_preimages,preimage_fragments}`

and project the six commissioned documentary artifacts. No source reopen or empirical rerun is required.

## Terminal

`PYAT_R2_LITS_FF02_D_BLOCKED__EXACT_CHECKPOINT_CUSTODY_OR_PREIMAGE_EXPORT_FAILURE__NO_SUBSTITUTION`
