# Commands, JUnit and source hashes

**Tested PRE-MAIN:** `8e44ca9c751049d65e6def47600b5c073ee04b29`.
**Dispatch:** `d7df4da4f159313b31981796b9f1ebcd91bfd8be`.
**Full candidate:** `8d9585296ff264b947559f4a78f49f73ca45e53a` / tree `5394e33e…`.
**R2 base:** `598d9e9eaba5143950c63317705fd09104fbf463`.

## Commands

```sh
# clean PRE-MAIN-derived worktree; RRIF absent
sh old_candidate/receiving_packet/apply.sh /tmp/rrif-e-clean-f1 old_candidate
# exit 2; RRIF_E_BASE_R2_MISSING; no RRIF

git -C /tmp/rrif-e-clean-f1 archive --format=tar 598d9e9eaba5143950c63317705fd09104fbf463 \
  SOROK_PRODUCT_CONTROL_ROOM/RRIF/CODE_CANDIDATE/RRIF_R2 | tar -x -C /tmp/rrif-e-clean-f1
# 459 files; SOURCE_MANIFEST SHA 7cfcb467…

sh candidate/receiving_packet/verify_r2_base.py \
  --dest /tmp/rrif-e-clean-f1/SOROK_PRODUCT_CONTROL_ROOM/RRIF/CODE_CANDIDATE/RRIF_R2 \
  --repo /tmp/rrif-e-clean-f1
# PASS; expected=459 actual=459 vars=444

sh candidate/receiving_packet/apply.sh /tmp/rrif-e-clean-f1
# RRIF_E_PACKET_APPLIED_NOT_MERGED; 640 files

python3 candidate/receiving_packet/verify_packet.py --root <stage>
# PASS; listed=639 actual=640 unlisted=[] extension=174
```

## JUnit/test results

All with `PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0`, isolated pytest cache and `PYTHONPATH="<stage>:<stage>/rrif_r3_extension:<premain>"`.

| JUnit | Tests | Result |
|---|---:|---|
| `junit/r2.xml` | 20 | 20 passed |
| `junit/r3.xml` | 9 | 9 passed |
| `junit/e.xml` | 6 | 6 passed |
| first consumer | 1 process | exit 0; expected PARTIAL status |

## First consumer

```sh
python3 <stage>/first_consumer_cli.py --root /tmp/rrif-e-consumer-f1b
# exit 0
# PASS_PARTIAL_SAME_ROOT_C9_C12__C9_ACTOR_OWNER_HELD__CP_A5_SEPARATE_ROOT
# OWNER_ANCHOR_REQUIRED; native_person=false
```

## Negative receipts

- `receipts/old_additive_stop.txt`: old patch STOP exit 2, no RRIF.
- `receipts/badbase_stop.txt`: lookalike base STOP exit 3, 459 unchanged.
- `receipts/missing_extension.json`: verifier exit 1, `MISSING_FILES`.
- `receipts/extra_unlisted.json`: verifier exit 1, unlisted extra.
- `receipts/rollback.txt`: restoration exit 0, 459 files, manifest hash exact.

## Hashes

```text
R2 SOURCE_MANIFEST.json
7cfcb4679e36b522e83cc7120dbc166ce61dd220099c2aca8f5c9ddb5252c126

full candidate tree
5394e33ec81766a4ee891b0d58007f24ac1d1303

new source preimage
886f56b7788258fcbb3b9be665770c5af3fc7fdd13537a26227cc351c5bad092

first consumer receipt
64a9c1714c5eab0ae8c0fedab897fabb172aca1889c04a8fa567143e8df723d3
```

Machine copies: `SOURCE_HASHES.json`; `junit/*.xml`; `junit/*.txt`.

## Final state

No live PRE-MAIN, main, Pyat, PROGRAMMA or source-owner branch was modified.
The clean stage is sourcefree TEST_ONLY and remains pending owner receiving
decision. Final remote SHA is reported in the terminal push readback.
