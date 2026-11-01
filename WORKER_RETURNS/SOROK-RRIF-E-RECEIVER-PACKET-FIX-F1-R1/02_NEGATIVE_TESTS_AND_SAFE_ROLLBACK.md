# Negative tests and safe rollback

## 1. Old additive-only packet before R2

```sh
sh old/receiving_packet/apply.sh /tmp/rrif-e-clean-f1 old_candidate
# exit 2
# RRIF_E_BASE_R2_MISSING: install exact R2 candidate first
# RRIF absent afterward: TRUE
```

## 2. Lookalike R2 base

A fresh clean stage received the exact 459-file R2 base, then its
`SOURCE_MANIFEST.json` was altered by one byte.

```sh
sh candidate/receiving_packet/apply.sh /tmp/rrif-e-badbase
# exit 3
# RRIF_E_BASE_R2_IDENTITY_MISMATCH: STOP before write
# files in destination after: 459 (unchanged)
```

`verify_r2_base.py` is run before candidate extraction or any write. It checks:

- exact manifest SHA-256;
- exactly 444 vendor rows;
- every vendor file Git blob;
- exact 459-file R2 tree set (no missing or extra).

## 3. Missing R3 extension

A validated full candidate copy was created, then
`rrif_r3_extension/c12_guard.py` was removed.

```sh
python3 verify_packet.py --root /tmp/rrif-e-neg
# exit 1
# MISSING_FILES:rrif_r3_extension/c12_guard.py
# ACTUAL_FILE_COUNT_MISMATCH
# r3_extension_files: 173
```

## 4. Extra unlisted file

An unlisted file was added to a validated copy.

```sh
python3 verify_packet.py --root /tmp/rrif-e-extra
# exit 1
# ACTUAL_FILE_COUNT_MISMATCH
# unlisted=["UNLISTED_EXTRA.txt"]
# listed=639 actual=641
```

`verify_packet.py` checks actual final-tree equality, not just listed rows. The
candidate test additionally checks `actual - {preimage}` and the unlisted list.

## 5. Source-preimage identity

The corrected preimage pins:

- source candidate commit `8d958529…`;
- tree `5394e33e…`;
- 640 actual regular files;
- 639 listed non-self files;
- 174 extension files;
- `first_consumer_cli.py` present;
- source manifest SHA-256 `7cfcb467…`.

The old 638-entry preimage has been replaced by the 639-entry preimage in this
packet. It lists every non-self actual file.

## 6. Tested rollback

After full apply on `/tmp/rrif-e-clean-f1`:

```sh
sh candidate/receiving_packet/rollback.sh /tmp/rrif-e-clean-f1
# exit 0
# RRIF_E_ROLLBACK_RESTORED_EXACT_R2
# files: 459
# manifest SHA-256: 7cfcb4679e36b522e83cc7120dbc166ce61dd220099c2aca8f5c9ddb5252c126
```

Rollback:

- removes/replaces only
  `SOROK_PRODUCT_CONTROL_ROOM/RRIF/CODE_CANDIDATE/RRIF_R2`;
- re-extracts exact R2 from `598d9e9e…`;
- verifies 459 files, 444 rows, manifest hash and vendor blobs;
- does not run `git clean -fd`, reset, `checkout --`, branch deletion or force;
- does not touch sibling paths or other worktrees.

The full stage was reapplied after rollback for the final test evidence; no live
PRE-MAIN or another worker tree was used.

## Outcomes

| Negative | Expected/actual |
|---|---|
| old patch before R2 | STOP exit 2, no RRIF |
| lookalike base | STOP exit 3, 459 unchanged |
| missing extension | verifier exit 1 |
| extra unlisted | verifier exit 1 |
| source manifest identity | STOP before write |
| rollback | exact 459 R2 restored |
