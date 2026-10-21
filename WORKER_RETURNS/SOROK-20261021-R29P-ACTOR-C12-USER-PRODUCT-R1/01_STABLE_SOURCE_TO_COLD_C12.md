# R29P stable source to cold C12 and A0/A2

## Actual chain

```text
R26V sourcefree A/B history
  -> R27P StableJoinedProducer.stage_world explicit life
  -> real BP2 C8 keyed occurrence / E1 / TEST_ONLY CAN008 A / separate CAN011 T+grant
  -> committed C9 target / independently performed E2
  -> R29PProduct seed and BP4 A0-A3 world
  -> R26E QualifiedC12Store read path
  -> persisted SQLite close / new-process reopen
  -> actor-limited M6 and A2 offscreen life
```

No upstream function is patched. `StableJoinedProducer` subclasses the base BP2 producer and overrides only `stage_world`, assigning an explicitly constructed `historical_life`. The test `test_no_global_builder_mutation_and_two_isolates` asserts `bp2_joined.producer.build_two_actor_life` is the original function before and after two products. Each isolate has its own root, key file, C9 database and C12 database.

## Exact source custody

| Layer | Source | Exact identity |
|---|---|---|
| Historical A/B producer | R27P copy of R26V | `candidate/historical_actor_producer.py`, blob `e84f6cfd34d8b7811d29bcd91f1c04593065beb3` |
| Stable owner injection | R27P | `candidate/stable_actor_binding.py`, blob `e06acc1792008ba1743d9edcbe929e9ec82e4061` |
| BP2/BP4 joined product | BP2P4J | 150-file manifest, commit `5b3e6577400ea1d88971ae6b48e41a118b8059ae` |
| C12 preimage repair | R26E | `r26e/c12_integrity.py`, blob `0c51c9d13f1065c41b16813f9827a21338e2d6cf` |
| N1 screen | N1 | `n1/n1_eligibility.py`, blob `03b7e092c87c7133313598ca024948ef030b70bb` |
| R29P product | this return | `r29p/product.py`, `r29p/runner.py`, `r29p/faults.py` |

`SOURCE_MANIFEST.json` records the exact 150 vendor hashes plus the six copied host files. `evidence/source_manifest_closure.json` verifies 150/150 vendor files and 6/6 extras.

## Qualified C12 preimages

R26E's qualified verifier is used for every product read. It verifies:

- episode rows with `hash` and post-hash `episode_id` excluded;
- world-event and checkpoint rows with only `hash` excluded;
- column hash equals body hash;
- contiguous sequence numbers;
- perception sequence numbers.

The pinned upstream `C12Store.verify` remains false on populated episodes because it hashes the body before removing its own `hash`; the test asserts that upstream defect while the qualified verifier returns `ok=true`.

## Persisted reopen and fork

`R29PProduct` persists the BP2 binding in `product/bp2_join.json` and adds the R26V variant. `R29PProduct.reopen` reads that binding, rebuilds the exact sourcefree life, re-assembles the verified BP2 artifacts from the recorded physical paths and opens the same SQLite database with `QualifiedC12Store`.

The cold test starts a new Python process, reopens the same persisted database through `R29PProduct.reopen`, verifies the populated chain and reads the same A0/A2 claims. It does not re-run the producer and does not create a new root.

`C12Store.fork` copies rows at or before the fork clock and preserves their hashes. The fork test writes a post-fork SAY only on `alt`; `root` and `alt` share the pre-fork rows and diverge afterward. Both branches cold reopen and verify.

## Sourcefree grade and limits

The actors are simulator histories, not observed humans. The rules, grants, E2, C8 key/anchor and C12 are `TEST_ONLY`. The product is not a native C12 person, not a C11 weld and not a human psychological finding. Raw SQLite deletion and a same-user witness/key compromise remain outside the C12 containment boundary.
