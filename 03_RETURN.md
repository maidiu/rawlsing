# U01 — T02 GENERIC R4 BATCH ADAPTER INDEPENDENT QUALIFICATION R1 — RETURN

Repository: `maidiu/rawlsing`

Worker branch: `agent/rabochii-prev3-w19-u01-t02-r4-batch-adapter-hostile-qualification-r1`

Commission tip: `1a0f07ef73066a9379c14c8e8d112cf0817ad6ae`

Exact grain: `SDTF_R4_GENERIC_BATCH_ADAPTER_INDEPENDENT_HOSTILE_QUALIFICATION_R1_ONLY`

Library: `NOT USED`

## Terminal

**BLOCK**

`U01_BLOCK__T02_PREDECESSOR_LINEAGE_IS_NOT_FAIL_CLOSED_WHEN_PRIOR_SNAPSHOT_IS_ABSENT_FROM_BATCH`

The exact T02 candidate cannot be independently qualified. The frozen S03 contract requires `predecessor_row_ref` to be null only for generation 0 and otherwise to be the **exact prior row ref**; it also states that different generations require exact predecessor lineage.

T02 does not enforce that law when the predecessor snapshot is not co-present in the same batch.

## Frozen identities checked

T02 producer return: `161b207f1efb6f8291c1dae3258bb710438f6b54`

Implementation: `rawlsing_next/sdtf_r4_generic_batch_adapter.py`

Implementation blob: `c1a495c7a23d4ebee086fd5410d9627f4aefb695`

Producer test: `rawlsing_next/tests/test_sdtf_r4_generic_batch_adapter.py`

Producer test blob: `7b4190601757fa69352d1a990c27242c67226cae`

Frozen S03 contract artifact blob: `0a2eb3da6d755f12197348a71cfa7d1dd97d7b4d`

Frozen S03 contract ref:

`SDTF_R4_GENERIC_BATCH_ENVELOPE_CONTRACT|SDTF_R4_GENERIC_BATCH_RULE_ENVELOPE_INTAKE_AND_CONSTRUCTOR_CONTRACT_R1@1.0.0|abc44b2b4ff04e164b5188e5929b0c10ca1b6e582b28207bb7e464ace698a83d`

The commissioned implementation/test blobs match the producer identities.

## Smallest exact blocker

`PREDECESSOR_CHAIN_INVALID_NOT_FAIL_CLOSED_FOR_UNPRESENTED_PRIOR_SNAPSHOT`

The candidate's `_validate_lineage(...)` does this for `generation > 0`:

1. reject a missing predecessor;
2. compute the expected prior-generation object id;
3. reject only if predecessor `kind` or `object_id` differs;
4. otherwise return success.

It does **not** validate `predecessor.content_hash` there.

Later, `adapt_generic_r4_batch(...)` compares the predecessor's full exact ref only if a row with that predecessor object id is present in the current batch. If the prior snapshot is absent, that comparison is skipped.

Therefore this counterexample is accepted by the lineage gate:

- successor generation: `1`;
- predecessor kind: `SDTF_R4_GENERIC_BATCH_CANDIDATE_ROW`;
- predecessor object id: the syntactically expected `namespace:id:g0`;
- predecessor content hash: any valid lowercase SHA-256 different from the actual g0 row hash;
- g0 row: omitted from the batch.

The successor's own row identity remains internally self-consistent because its forged predecessor ref is itself hashed into the successor identity. With otherwise projectable cells, no lineage failure is added and the row can continue toward the adopted R4 constructor. That is fail-open predecessor lineage, contrary to S03.

## Why the producer's lineage test does not close this

Producer test identity:

`test_predecessor_chain_error_is_row_local_and_fails_closed`

covers only `generation=1` with `predecessor=None`. It proves the missing-predecessor case, not the forged-hash/unpresented-prior case.

The producer's `14 passed` remains producer evidence only and cannot cure the missing independent lineage case.

## Independent blocker reproduction artifact

`02_REPRO_U01_T02_PREDECESSOR_LINEAGE_BLOCKER.py`

Test identity:

`u01_predecessor_hash_forgery_is_accepted_when_prior_snapshot_absent`

The reproduction script requires an actual checkout at producer tip, verifies both commissioned Git blob identities with `git rev-parse`, constructs the real g0 row using the committed producer fixture, replaces only the predecessor content hash, presents only the g1 successor, and asserts that `PREDECESSOR_CHAIN_INVALID` is absent. Exit 0 reproduces the blocker; a repaired implementation should cause the final assertion to fail and then undergo fresh qualification.

## Repository-interface execution evidence

No PASS/interface qualification is claimed.

This execution container did not have an actual repository checkout and could not obtain one over Git:

```text
git ls-remote https://github.com/maidiu/rawlsing.git refs/heads/agent/rabochii-prev3-w19-u01-t02-r4-batch-adapter-hostile-qualification-r1
fatal: unable to access 'https://github.com/maidiu/rawlsing.git/': Could not resolve host: github.com
```

The terminal implementation blocker is established before repository-interface qualification can succeed. After repair, the successor must run the committed producer suite plus the U01 reproduction/repair regression against the actual repository import graph. `INTERFACE_EQUIVALENT_FIXTURE_PASS != ACTUAL_REPOSITORY_INTERFACE_QUALIFICATION` remains enforced.

## Preserved boundaries

No R4/S03 redesign was performed. No concrete rule was minted. No `CURRENT_ACCEPTED` selection was made. No source semantics were adjudicated. No actor/entity fact was materialized. No topology was constructed. No V3/person state or OBL063 semantics were entered. Library was not used. MAIN and PRE-MAIN were not mutated.

## Successor gate

**BLOCK leaves generic R4 batch production use dormant.**

Successor needed: repair only the exact predecessor-lineage closure defect so an N>0 predecessor is proved as the exact prior snapshot (by co-present exact prior row identity or another separately frozen exact lineage-resolution surface), then perform fresh independent qualification with actual repository execution. No broader R4/S03 redesign is authorized by this return.
