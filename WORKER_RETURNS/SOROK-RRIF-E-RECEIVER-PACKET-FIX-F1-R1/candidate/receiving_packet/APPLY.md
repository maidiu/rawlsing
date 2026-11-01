# RRIF-E complete receiving packet (F1)

This packet installs the **complete immutable 640-file Final-E candidate** over the exact 459-file RRIF-R2 base. The full candidate is referenced at:

- commit `8d9585296ff264b947559f4a78f49f73ca45e53a`
- path `WORKER_RETURNS/SOROK-RRIF-FINAL-E-REPAIR-AND-FIRST-CONSUMER-R1/candidate/rrif_r2`
- tree `5394e33ec81766a4ee891b0d58007f24ac1d1303`

The candidate contains all 174 `rrif_r3_extension/` files and `first_consumer_cli.py`. The packet does not duplicate those 640 code files; the exact Git tree is the source of truth. The candidate commit must exist in the target repository object database.

## Prerequisite: exact R2 base

Install the exact R2 candidate from `598d9e9eaba5143950c63317705fd09104fbf463` at:

`SOROK_PRODUCT_CONTROL_ROOM/RRIF/CODE_CANDIDATE/RRIF_R2`

The installer verifies all 459 R2 files, the exact `SOURCE_MANIFEST.json` SHA-256 `7cfcb4679e36b522e83cc7120dbc166ce61dd220099c2aca8f5c9ddb5252c126`, 444 vendor rows and every vendored Git blob before writing. A lookalike/extra/missing base stops before patch.

## Apply (isolated worktree only)

```sh
sh candidate/receiving_packet/apply.sh <premain-worktree>
```

Expected success: `RRIF_E_PACKET_APPLIED_NOT_MERGED`.

After apply, expected installed state: 640 regular files, 639 preimage entries (self excluded), 174 extension files, `first_consumer_cli.py` included, exact source-manifest hash.

## Test (clean PRE-MAIN-derived stage)

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="<stage>:<stage>/rrif_r3_extension:<premain>" \
  python3 -m pytest -q <stage>/tests/test_join.py <stage>/tests/test_rrif_r2_c12.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="<stage>:<stage>/rrif_r3_extension:<premain>" \
  python3 -m pytest -q <stage>/rrif_r3_extension/tests/test_rrif_r3_extension.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="<stage>:<stage>/rrif_r3_extension:<premain>" \
  python3 -m pytest -q <stage>/tests/test_rrif_e_repair.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="<stage>:<stage>/rrif_r3_extension:<premain>" \
  python3 <stage>/first_consumer_cli.py --root <fresh-receipt-root>
```

Expected first consumer: `PASS_PARTIAL_SAME_ROOT_C9_C12__C9_ACTOR_OWNER_HELD__CP_A5_SEPARATE_ROOT`, `OWNER_ANCHOR_REQUIRED`, `native_person=false`.

## Rollback (isolated worktree)

```sh
sh candidate/receiving_packet/rollback.sh <premain-worktree>
```

This restores the exact 459-file R2 base from `598d9e9e…` and only replaces `SOROK_PRODUCT_CONTROL_ROOM/RRIF/CODE_CANDIDATE/RRIF_R2`. It does not use `git clean -fd`, `reset --hard`, `checkout --`, or touch any sibling path. Never run it in a shared active worktree.

## Limits

Sourcefree TEST_ONLY candidate. No PRE-MAIN merge, production adoption, CAN/ADP/SCI05/Pyat/human authority. The external owner anchor remains `OWNER_ANCHOR_REQUIRED`; native person is false.
