# PRE-MAIN real base + patch receiving stage

## Clean PRE-MAIN

Detached worktree created from the exact live `integration/pre-main-reconciliation-r1`
head:

```text
8e44ca9c751049d65e6def47600b5c073ee04b29
```

Before staging:

```text
SOROK_PRODUCT_CONTROL_ROOM/RRIF/CODE_CANDIDATE/RRIF_R2
= ABSENT
```

## 1. Additive patch alone — actual STOP

```sh
sh candidate/receiving_packet/apply.sh <clean-premain> candidate
```

Actual:

```text
exit 2
stderr: RRIF_E_BASE_R2_MISSING: install exact R2 candidate first
destination after command: ABSENT
```

This correctly refuses to apply the patch without the R2 base. The author's
26/26 R2-copy rehearsal is not a clean PRE-MAIN integration test.

## 2. Exact R2 base staging

The exact precondition was extracted from
`598d9e9eaba5143950c63317705fd09104fbf463`:

```text
R2 files:                         459
vendor SOURCE_MANIFEST rows:     444
SOURCE_MANIFEST SHA-256:          7cfcb4679e36b522e83cc7120dbc166ce61dd220099c2aca8f5c9ddb5252c126
```

## 3. Patch application

```sh
sh candidate/receiving_packet/apply.sh <clean-premain> candidate
```

Actual:

```text
RRIF_E_ADDITIVE_APPLIED_NOT_MERGED
patch exit 0
staged files after patch: 466
```

Files patched:

```text
joined/c12_verify_repair.py
joined/source_identity.py
joined/c12_custody.py
joined/c9c12_compat.py
joined/first_consumer.py
first_consumer_cli.py
tests/test_rrif_e_repair.py
tests/test_rrif_r2_c12.py
RRIF_R2_CANDIDATE_SOURCE_PREIMAGE.json
```

## 4. Actual receiving tests

### R2-only subset

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="<staged>:<clean-premain>" \
python3 -m pytest -q tests/test_join.py tests/test_rrif_r2_c12.py
```

Actual:

```text
20 passed in 14.72s
```

### RRIF-E repair tests

```sh
PYTHONPATH="<staged>:<clean-premain>" python3 -m pytest -q tests/test_rrif_e_repair.py
```

Actual:

```text
collection error
ModuleNotFoundError: No module named 'c12_guard'
```

The staged tree has no `rrif_r3_extension/c12_guard.py`; the patch did not add it.

### R3 extension tests

```text
ERROR: file or directory not found:
<staged>/rrif_r3_extension/tests/test_rrif_r3_extension.py
```

The candidate's 174-file `rrif_r3_extension` closure is missing from the
receiving patch.

### First consumer

```sh
PYTHONPATH="<staged>:<staged>/rrif_r3_extension:<clean-premain>" \
python3 <staged>/first_consumer_cli.py --root /tmp/rrif_e_stage_consumer
```

Actual:

```text
exit 1
joined/c12_custody.py: from c12_guard import GuardedC12Store, verify_store
ModuleNotFoundError: No module named 'c12_guard'
```

## 5. Source-preimage mismatch after staging

```text
RRIF_R2_CANDIDATE_SOURCE_PREIMAGE.json:
schema RRIF_R2_CANDIDATE_SOURCE_PREIMAGE@2
listed files: 638
staged files: 466
first_consumer_cli.py listed: false
rrif_r3_extension present in stage: false
```

The candidate 638-entry preimage describes the full 640-file candidate (minus
self) but not the 466-file receiving stage. The omitted `first_consumer_cli.py`
is an additional M1 hole even in the full candidate.

## 6. Base-identity and rollback defects

`apply.sh` checks only `joined/session.py`; it does not verify the exact
`SOURCE_MANIFEST.json` hash/444 rows before patching. We verified the base
manually, but the script itself would patch a lookalike base.

`APPLY.md` recommends:

```sh
git checkout -- <candidate path>
git clean -fd <candidate path>
```

`git clean -fd` can remove unrelated untracked files in an active checkout. This
rollback is not safe as written. The receiving rehearsal used a detached
temporary worktree; no live PRE-MAIN or other worker tree was cleaned,
reset, or mutated.

## 7. Exact receiving state

The current patch is **not ready for PRE-MAIN**. The stage is real, but the E
consumer and R3 tests cannot import without the omitted extension. The owner
must use the repair in `04_NARROW_RESIDUALS_AND_READY_TO_CLOSE.md` before any
bounded transfer.
