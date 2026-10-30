# BP4R candidate overlay and replay order

This directory carries the bounded sourcefree BP4R repair candidate. It is not
adopted and does not modify PRE-MAIN or any original branch.

## Exact base and prior cuts

| Part | Exact cut | Blob / role |
|---|---|---|
| BP2P4J base | `5b3e6577400ea1d88971ae6b48e41a118b8059ae` | `WORKER_RETURNS/SOROK-20261020-BP2P4J-ACTUAL-JOINED-ALPHA-R1` |
| F2 preimage candidate | `0636d257f588f8874e65b2cb183d1d47c7f53327` | `candidate/bp2p4/c12_verify.py` blob `c1699c8da5e944ed079708e272c3af50d5a30a44`; focused test blob `ebe1e8287f9b8485b6c862b66b6c2a9dafcf59aa` |
| BP4 guard candidate | `790f793ea85c8aba914970b7d9c3c25f81bf8a01` | `03_...md` Part B; `bp2p4/c12_guard.py` blob `a6a8de75ad92967e9fde354d76adce8b9572217e`; test blob `8ca11491af25b98825c88f1355e391ce82659ab7` |
| C9-R3 actual consumer | `1e99681f58086f2784834df1186cfba71a2c50b9` | `SOROK_PRODUCT_CONTROL_ROOM/V3_COURTS/SYN02/POST_R2_REVIEW/R3/C9_SQL/c9_actor_r3.py` blob `67f34f699220ec1407e7e8f0d58ed328e88a36af` |
| C12 repaired source | `68b058656254234f0af02df2a592aa6f8c6a8bd2` | `WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1` |

## Apply order

1. Check out the BP2P4J base at `5b3e657…`.
2. Overlay the exact F2 `bp2p4/c12_verify.py` and focused test (needed for the
   combined F2+guard suites).
3. Overlay the exact author guard `bp2p4/c12_guard.py` and `tests/test_c12_guard.py`.
4. Apply `patches/01_c12_guard_episode_origin_and_version.patch`.
5. Apply `patches/02_c9_actual_consumer_writer_version.patch` to the C9-R3
   `c9_actor_r3.py` under its exact source path.
6. Copy `tests/test_bp4r_candidate.py` into the BP2P4J `tests/` directory.
7. Run with `BP4R_C9_DIR` set to the patched C9-R3 directory.

The full patched guard and C9 consumer files are included for byte-exact
comparison. The two `.patch` files apply with `patch -p1` from the repository
root and were verified to reproduce those full files exactly.

## What changed

- Episode body `branch_id` is treated as the immutable origin. The SQL
  `branch_id` column is the current storage location. Copied child rows keep the
  parent body and hash; origin is resolved from fork prefix counts. Local child
  rows must have the child as origin. No hashed body is rewritten.
- `check_c9_mirror_handshake`/`two_store_readiness` reject unsupported writer
  schemas instead of accepting two matching `@2` strings.
- The actual C9 `c12_fork_guard` reads `meta.schema` and rejects unsupported
  schema, SQLite user_version and application_id before returning FORK_READY.

## Not changed

- No original BP4/C12 store, C9 actor transaction, C12 anchor payload, global
  writer chronology, C9 old-count test, source data or PRE-MAIN control.
- No key, signer, trust root, native C12 receiver or adoption.
