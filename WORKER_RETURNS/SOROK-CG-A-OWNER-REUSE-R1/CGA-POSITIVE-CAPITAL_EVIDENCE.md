# CGA-POSITIVE-CAPITAL evidence

## Exact sourcepack and historical blobs

```text
sourcepack09  c3cdc7c1e151cf3ece8159f7cc384b2359212e6c  64746865b0d02c2246f82cd4947ad96cb22802b073f9f1abd6595ce799ae8613
B1            c0f4588c158b40c8903b4aae2f292eae5238b8a0:bfirst.py = 94ffc52847e4c8ae760212d1bc8543594ba793fa
B1 sha256     478b989730f49a5def41a367b6f53e4aae9c80961f7f466fe669c7dbd92201a3
B3A           16f15a125ba54cdf17f5d41be2d851bbcd2240d7:integration.py = d3a324bb93c17fdaf12670dd153aeb138d9c426a
B3A sha256    6b0187c5dfa0a48928f78fb0c3979de6c35e49aa770c9d10f644f57eaed6a679
HQ300         189da3b54307d8731132c9a7f7baf578fee8bc96:positive_chain.py = b4db0cc1c26992a2ca9714e827075fd73e1a18f2
HQ300 sha256  11bc2a6d7622eef0cbd0dfcf31b984f03dfb0f1cdb8eea90e5eab06e3be0bd95
M01           02187a14e75ff30dd953d3c7185d689b80e62304:00_RETURN.md = b4f3ee8db327c7fdc5670a6fd17478465d5dc512
M01 sha256    19b12d88ef4d8df73ae55692fb5067ae074815b678cebe426acd7bb580365f61
C9RI          e7f4dbd472d885c71650da0fdbd0b713c6af74b6:vendor/c9r/candidate/pipeline.py = cb0350909dedd9f7159dce145ba216b211a8185c
C9RI sha256   b5da655ca03cdc9dc6dad11b88dfadd22101836cffc7993f530e6148ded0695c
BP2P4J        5b3e6577400ea1d88971ae6b48e41a118b8059ae:bp2p4/product.py = 8f7177a6b4e3ae0cae6316a13cf57adf363e0460
BP2P4J sha256 55c99dffb8cc7ab64e9fba4e15a353b41a984466a22e2cecf36f793a749a0a0f
```

The B1 vendored runtime path in the P3 tree also hashes to `478b9897...`:

```text
WORKER_RETURNS/SOROK-P3-E1-DEVELOPMENTAL-ABI-RECONNAISSANCE-R1/probe/vendor/B1/bfirst.py
git blob 94ffc52847e4c8ae760212d1bc8543594ba793fa
sha256  478b989730f49a5def41a367b6f53e4aae9c80961f7f466fe669c7dbd92201a3
```

## Current caller proof

`p3/test_rules.py` (`00b1006f...`) declares `B1_SHA256 = "478b9897..."` and loads the B1 module through `importlib` inside `_mode_for` (`test_rules.py:79-93`). `evaluate_event` uses `_mode_for` only in the `FORMATION` phase (`test_rules.py:167-190`) and returns a `readset` containing the B1 SHA-256 (`test_rules.py:224-230`). `production_guard()` always returns `DENY_ZERO_EFFECT` (`test_rules.py:50-53`).

`tests/test_rules.py` executed:

```text
test_recovered_b1_predicate_is_actor_local_and_preserves_opposed_parents PASS
test_later_response_requires_the_exact_prior_record_and_separate_activation_reader PASS
test_absent_actor_access_cannot_be_replaced_with_a_user_view_or_prose PASS
test_material_denial_is_not_repaired_by_a_mediator_or_native_claim PASS
test_wrong_version_and_exact_source_severance_refuse_and_restore PASS
```

`evidence/p3_store_rules.log` records 57 passed in 0.63 s (store + rules). The source-severance test writes extra bytes to a copied B1, gets `B1_SOURCE_SEVERED`, restores exact bytes, and then gets the expected `joint_check` record.

## Selected target path

The cold-later test (`WORKER_RETURNS/SOROK-CG-A-OWNER-REUSE-R1/tests/test_cold_later_recruit.py`) executed:

```text
bootstrap -> 3 realized events -> 2 formation records in PsycheStore
close owner -> reopen exact P2/P3 root and sidecar
advance -> later recruit response streams exactly the 2 formation record hashes
readset intersects the 2 formation hashes
terminal -> finish -> store head count remains 2
```

Command:

```bash
python3 -B -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-CG-A-OWNER-REUSE-R1/tests/test_cold_later_recruit.py
```

Observed: `1 passed in 247.70s`.

## Non-promotion evidence

- B3A has a different package/schema and no current P3 caller (`grep` for `from b3`/`integration` in P3 returns none).
- HQ300 uses `ChainEventLedger`, `AdmittedEvent`, `OwnerPrestate`, `CandidateRegistryFixture`; it is not a `DevelopmentOwner`.
- M01 has no code module in its exact tree (return/evidence only).
- C9RI vendor uses `vendor/c9r/candidate/*` and its own pipeline; no import into P3.
- V3 exact archive is absent; prior `SOROK-DEVELOPMENTAL-RECURSION-REUSE-R1` records the mismatch/HOLD.
