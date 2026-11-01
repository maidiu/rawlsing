# Clean PRE-MAIN stage and first consumer

## Cut and worktree

- PRE-MAIN cut: `8e44ca9c751049d65e6def47600b5c073ee04b29`.
- Exclusive detached worktree: `/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/rrif-e-f1-premain`.
- F1 packet: `1973d28ed4ba4c9e58c9d96fbe358445dddc929c`, `WORKER_RETURNS/SOROK-RRIF-E-RECEIVER-PACKET-FIX-F1-R1/candidate`.
- Full candidate: `8d9585296ff264b947559f4a78f49f73ca45e53a`, tree `5394e33ec81766a4ee891b0d58007f24ac1d1303`, 640 regular files.
- R2 base: `598d9e9eaba5143950c63317705fd09104fbf463`, 459 regular files, 444 vendor rows, manifest SHA-256 `7cfcb4679e36b522e83cc7120dbc166ce61dd220099c2aca8f5c9ddb5252c126`.
- Live PRE-MAIN remained `8e44ca9c…` at start and end; no PRE-MAIN write, merge or rebase.

`SOROK_PRODUCT_CONTROL_ROOM/RRIF` was absent in the fresh cut before staging.

## Absent base

```sh
sh apply.sh "$PREMAIN"
# exit 2
# RRIF_E_BASE_R2_MISSING: install exact R2 candidate first
# destination absent afterward
```

## Exact R2 base

```sh
git -C "$PREMAIN" archive 598d9e9eaba5143950c63317705fd09104fbf463 \
  SOROK_PRODUCT_CONTROL_ROOM/RRIF/CODE_CANDIDATE/RRIF_R2 | tar -x -C "$PREMAIN"
```

```text
regular files:                    459
vendor rows:                      444
SOURCE_MANIFEST SHA-256:          7cfcb4679e36b522e83cc7120dbc166ce61dd220099c2aca8f5c9ddb5252c126
verify_r2_base.py:                PASS, expected=459 actual=459
```

## F1 apply

```sh
sh apply.sh "$PREMAIN"
# exit 0
# RRIF_E_PACKET_APPLIED_NOT_MERGED
```

Observed final stage:

```text
regular files:                    640
preimage entries:                 639 (self excluded)
rrif_r3_extension files:          174
first_consumer_cli.py:            present
verify_packet.py:                 PASS, unlisted=[]
R2 SOURCE_MANIFEST SHA-256:       7cfcb4679e36b522e83cc7120dbc166ce61dd220099c2aca8f5c9ddb5252c126
```

The candidate came from the immutable Git commit through `apply.sh`; it was not copied from the author worktree.

## Tests on the clean stage

Each suite ran in its own process with the real stage path:

```sh
PYTHONPATH="$STAGE:$STAGE/rrif_r3_extension:$PREMAIN" \
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
python3 -m pytest -o addopts='' -q -p no:cacheprovider <suite>
```

| Suite | Result |
|---|---|
| 20 R2: `tests/test_join.py`, `tests/test_rrif_r2_c12.py` | **20 passed** |
| 9 R3: `rrif_r3_extension/tests/test_rrif_r3_extension.py` | **9 passed** |
| 6 E: `tests/test_rrif_e_repair.py` | **6 passed** |

The E suite includes the C12 tamper/restore and source-preimage checks. No baseline RED was relabeled green.

## First consumer

```sh
PYTHONPATH="$STAGE:$STAGE/rrif_r3_extension:$PREMAIN" \
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
python3 "$STAGE/first_consumer_cli.py" --root /tmp/f1_stage_consumer_final
# exit 0
```

Status:

`PASS_PARTIAL_SAME_ROOT_C9_C12__C9_ACTOR_OWNER_HELD__CP_A5_SEPARATE_ROOT`

The receipt records:

- cold verification true;
- fork/cold branch `alt`;
- repaired root and `alt` C12 chains true;
- upstream known defect reproduced RED;
- C9 actor `C9_SOURCE_MISSING`, `no such table: actor_meta`;
- C9/C12 `INCOMPATIBLE_WITHOUT_OWNER_MIGRATION__ROOT_COLD_READ_ONLY_UNDER_OWNER_ANCHOR_HOLD__FORK_LEGACY_ROOT_UNVERIFIED`;
- CP-A5 `RETAIN_TOOL`, market/ask `UNKNOWN`, separate root;
- `OWNER_ANCHOR_REQUIRED`; native C8/C9/C12, native CP-A5, native person and owner adoption all false.

Consumer receipt SHA-256: `98ad04d915f5c90c70ba223bbf16ba1d73aee90bc7181864708705c674a06ccb`.

## Post-test state

`rollback.sh` restored the isolated stage to exact R2:

```text
RRIF_E_ROLLBACK_RESTORED_EXACT_R2
regular files:                    459
SOURCE_MANIFEST SHA-256:          7cfcb4679e36b522e83cc7120dbc166ce61dd220099c2aca8f5c9ddb5252c126
```

No live PRE-MAIN caller is proved. This stage is a sourcefree TEST_ONLY receiving fixture, not production code.

## Stage result

The clean stage proves D1, D2 and D5 are repaired and confirms D4 restoration. It does not cure the D3 pre-write base fail-open: `apply.sh` accepted a non-vendor-tampered R2 base and proceeded. The stage tests are green because the full candidate overwrites that ordinary-tree tamper; the base authentication claim is still false.
