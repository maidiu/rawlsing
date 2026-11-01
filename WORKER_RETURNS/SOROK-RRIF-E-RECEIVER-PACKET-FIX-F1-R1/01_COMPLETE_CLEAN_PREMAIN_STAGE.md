# Complete clean PRE-MAIN receiving stage

## Cut verification

- Canonical PRE-MAIN: `8e44ca9c751049d65e6def47600b5c073ee04b29`.
- F1 dispatch: `d7df4da4f159313b31981796b9f1ebcd91bfd8be`.
- Immutable full candidate: `8d9585296ff264b947559f4a78f49f73ca45e53a`,
  path `WORKER_RETURNS/SOROK-RRIF-FINAL-E-REPAIR-AND-FIRST-CONSUMER-R1/candidate/rrif_r2`,
  tree `5394e33ec81766a4ee891b0d58007f24ac1d1303`.
- Independent review: `1198691534c050c19c7c874454b54f99011006c4`.
- At start and end, live PRE-MAIN remained `8e44ca9c…`; no PRE-MAIN write/merge.

## Clean stage

A disposable detached worktree was created at PRE-MAIN `8e44ca9c…`.
`SOROK_PRODUCT_CONTROL_ROOM/RRIF` was **ABSENT**.

### Old additive-only packet: expected STOP

```sh
sh old_candidate/receiving_packet/apply.sh /tmp/rrif-e-clean-f1 old_candidate
# exit 2
# RRIF_E_BASE_R2_MISSING: install exact R2 candidate first
# destination after command: RRIF_ABSENT
```

### Exact R2 base

Installed from `598d9e9eaba5143950c63317705fd09104fbf463` via Git archive:

```text
files:                            459
vendor SOURCE_MANIFEST rows:      444
SOURCE_MANIFEST SHA-256:          7cfcb4679e36b522e83cc7120dbc166ce61dd220099c2aca8f5c9ddb5252c126
```

`verify_r2_base.py` PASS: expected 459, actual 459, vendor 444, zero errors.

### Corrected packet apply

```sh
sh candidate/receiving_packet/apply.sh /tmp/rrif-e-clean-f1
# exit 0
# RRIF_E_PACKET_APPLIED_NOT_MERGED
```

Actual final stage:

```text
regular files:                    640
preimage entries:                 639 (self excluded)
rrif_r3_extension files:          174
first_consumer_cli.py:            present
SOURCE_MANIFEST SHA-256:          7cfcb467...
verify_packet.py:                 PASS, unlisted=[]
```

The candidate tree is installed from the immutable Git commit, not copied from the author's worktree. The new preimage includes `first_consumer_cli.py` and all 174 extension files and rejects any unlisted file.

## Suites on the clean stage

All commands used `PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0`,
`PYTHONPATH="<stage>:<stage>/rrif_r3_extension:<premain>"`, isolated pytest
cache, and the real stage path.

| Suite | Result |
|---|---|
| 20 R2 tests (`tests/test_join.py`, `tests/test_rrif_r2_c12.py`) | **20 passed** |
| 9 R3 extension tests (`rrif_r3_extension/tests/test_rrif_r3_extension.py`) | **9 passed** |
| 6 RRIF-E tests (`tests/test_rrif_e_repair.py`) | **6 passed** |
| First consumer (`first_consumer_cli.py`) | **exit 0** |

JUnit and text receipts: `junit/r2.xml`, `junit/r3.xml`, `junit/e.xml`,
`junit/r2.txt`, `junit/r3.txt`, `junit/e.txt`.

### First consumer

Status:

`PASS_PARTIAL_SAME_ROOT_C9_C12__C9_ACTOR_OWNER_HELD__CP_A5_SEPARATE_ROOT`

Observed:

- help accepted, wait clock 40, cold return scene open;
- C12 repaired root/fork green; upstream defect reproduced RED;
- coordinated custody BOTH_GREEN on intact, guard RED on tamper;
- C9 actor `C9_SOURCE_MISSING` (`no such table: actor_meta`);
- C9/C12 `INCOMPATIBLE_WITHOUT_OWNER_MIGRATION…`;
- CP-A5 separate root PASS, market/ask `UNKNOWN`;
- `OWNER_ANCHOR_REQUIRED`; `native_person=false`.

## Exact stage hashes

- R2 `SOURCE_MANIFEST.json`: `7cfcb4679e36b522e83cc7120dbc166ce61dd220099c2aca8f5c9ddb5252c126`
- Full candidate tree: `5394e33ec81766a4ee891b0d58007f24ac1d1303`
- New source preimage: `886f56b7788258fcbb3b9be665770c5af3fc7fdd13537a26227cc351c5bad092`
- First consumer receipt: `64a9c1714c5eab0ae8c0fedab897fabb172aca1889c04a8fa567143e8df723d3`

## Receiving status

`SOURCEFREE_TEST_ONLY_READY_FOR_OWNER_RECEIVING`. The clean stage is a necessary
prerequisite for owner/PRE-MAIN consideration, not proof of a live PRE-MAIN
caller, native science, C9 actor, C11 weld, human A5 or production adoption.
