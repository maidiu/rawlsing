# Clean PRE-MAIN stage and first consumer

## Fresh cut

- PRE-MAIN branch: `integration/pre-main-reconciliation-r1`.
- Exact cut: `8e44ca9c751049d65e6def47600b5c073ee04b29`.
- Fresh disposable worktree: `/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/rrif-e-f2-premain`.
- The worktree was detached at PRE-MAIN; `SOROK_PRODUCT_CONTROL_ROOM/RRIF` was absent before staging.
- The R2 base came from Git commit `598d9e9e...`, not from an author candidate copy.
- The full candidate came from immutable commit `8d958529...` through F1 `apply.sh`.
- No PRE-MAIN write, merge, reset, rebase or checkout of another worker occurred.

## Stage and packet

```sh
git -C "$PREMAIN" archive --format=tar 598d9e9eaba5143950c63317705fd09104fbf463 \
  SOROK_PRODUCT_CONTROL_ROOM/RRIF/CODE_CANDIDATE/RRIF_R2 | tar -x -C "$PREMAIN"

python3 "$PACKET/verify_r2_base.py" --dest "$R2" --repo "$PREMAIN"
# exit 0; ok=true; expected 459; actual 459; vars 444

sh "$PACKET/apply.sh" "$PREMAIN"
# exit 0; RRIF_E_PACKET_APPLIED_NOT_MERGED

python3 "$PACKET/verify_packet.py" --root "$R2"
# exit 0; listed 639; actual 640; unlisted [];
# r3_extension_files 174; source_manifest_sha256 7cfcb467...
```

Observed stage:

```text
regular files:                    640
self-excluded preimage entries:   639
rrif_r3_extension files:          174
first_consumer_cli.py:            present
SOURCE_MANIFEST SHA-256:          7cfcb4679e36b522e83cc7120dbc166ce61dd220099c2aca8f5c9ddb5252c126
```

## Suites

Each suite was a separate process with the real stage paths:

```sh
PYTHONPATH="$R2:$R2/rrif_r3_extension:$PREMAIN" \
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
python3 -m pytest -o addopts='' -q -p no:cacheprovider <suite>
```

| Suite | Result | JUnit |
|---|---|---|
| 20 R2: `tests/test_join.py`, `tests/test_rrif_r2_c12.py` | **20 passed** | `junit/r2.xml` |
| 9 R3: `rrif_r3_extension/tests/test_rrif_r3_extension.py` | **9 passed** | `junit/r3.xml` |
| 6 E: `tests/test_rrif_e_repair.py` | **6 passed** | `junit/e.xml` |

All JUnit files report zero failures and zero errors. No old RED was silently relabeled.

## First consumer

```sh
PYTHONPATH="$R2:$R2/rrif_r3_extension:$PREMAIN" \
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
python3 "$R2/first_consumer_cli.py" --root /tmp/f2_stage_consumer
```

Observed exit 0:

`PASS_PARTIAL_SAME_ROOT_C9_C12__C9_ACTOR_OWNER_HELD__CP_A5_SEPARATE_ROOT`

Receipt SHA-256: `7086918178930b899a73cb9216bdb58e5e60ffc5ad68077c9a69b7ab8633b485`.

The receipt preserves:

```text
C9 actor:              C9_SOURCE_MISSING
C9/C12:                INCOMPATIBLE_WITHOUT_OWNER_MIGRATION...
CP-A5:                 RETAIN_TOOL, separate root, market/ask UNKNOWN
external anchor:       OWNER_ANCHOR_REQUIRED
native C8/C9/C12:      false
native CP-A5:          false
native person:         false
owner adoption:        false
```

The receipt is sourcefree TEST_ONLY and proves no live PRE-MAIN caller.

## Rollback and sibling safety

After the 640-file stage, a sibling sentinel was created at `SOROK_PRODUCT_CONTROL_ROOM/RRIF/F2_SIBLING_SENTINEL` with SHA-256 `d4383fc33176254b2abac7cb3c14bcaae5701681537db3d69adf740b1feb1b9c`.

```sh
sh "$PACKET/rollback.sh" "$PREMAIN"
# exit 0
# RRIF_E_ROLLBACK_RESTORED_EXACT_R2
```

Observed:

```text
regular files after rollback:     459
SOURCE_MANIFEST SHA-256:          7cfcb467...
sibling sentinel:                 unchanged
verify_r2_base.py after rollback: exit 0, expected 459, actual 459
```

`rollback.sh` did not use `git clean`, reset, checkout, force, branch deletion or a foreign worktree. The sentinel was removed after the check.

## Cut readback

Live PRE-MAIN was `8e44ca9c751049d65e6def47600b5c073ee04b29` at the start and after the stage. The F2 branch remains based on F1 `1973d28e...`; the candidate `8d958529...` was not modified.
