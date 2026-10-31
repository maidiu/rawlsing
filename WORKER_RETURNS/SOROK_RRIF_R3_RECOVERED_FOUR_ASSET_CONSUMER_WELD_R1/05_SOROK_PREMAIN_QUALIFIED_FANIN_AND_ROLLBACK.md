# Sorok/PREMAIN qualified fan-in and rollback

## Minimal adoption candidate

The only proposed fan-in is the additive subpackage:

```text
SOROK_PRODUCT_CONTROL_ROOM/RRIF/CODE_CANDIDATE/RRIF_R2/rrif_r3_extension/
```

It contains:

- `cp_a5_consumer.py` — actual CP-A5 sourcefree life/encounter consumer;
- `cp_a5_runtime/` — exact 168-file CP-A5 runtime closure;
- `c9c12_consumer.py` — actual C9C12-R2 C12 reader over R2;
- `c9c12_reader.py`, `c12_guard.py` — copied C9C12-R2 candidate;
- `tests/test_rrif_r3_extension.py` — 9 actual consumer/fault tests.

R2 `joined/`, `vendor/j`, `vendor/e`, `SOURCE_MANIFEST.json`, and existing R2
tests were not changed. No manifest was regenerated. No production root, PREMAIN
file, Pyat file, Programma file, original owner branch, or source/actor record
was edited.

## Trusted source versions for review

| Source | Exact cut | Use |
|---|---|---|
| R2 sourcefree baseline | `598d9e9eaba5143950c63317705fd09104fbf463` | unchanged receiver/root and 20-test baseline |
| C9C12-R2 | `c78404724052496fdec8608c8b0e833c0f7c4ecc` | C12 guarded read; C9 actor reader |
| CP-A5-R2 | `913765328e4fab12b150ea01421ed6b445158184` | actual encounter consumer |
| B-F1CR-R2 | `bf3273c294c704ad7c631559b9866d351bb4f103` | reconstructed targetless C10; held |
| V3CORE-R1 | `b5cb3f917402b992d7cbe933af0b378d2b37cbfd` | material-only adapter; held |
| RRIF R1 | `c1765e0a7606a89c2fc9554721e44f85b99e8253` | mission/owner context |
| RRIF mandate | `fa832d1fd54b44eebf4f0c09ed4eb2f8ce378abd` | constitutional scope |
| RRIF adjudication | `b07b2233a63600a9da55d64aca3821d802d12636` | three-return decision |

## Qualified fan-in decision

**No automatic fan-in.** The extension is a review candidate, not an owner
adoption. The receiving review must at minimum cover:

1. CP-A5 `EncounterReader` access boundary and the exact `BP2_ORIGIN_INVARIANT_MISMATCH`
   at R2 same-root.
2. C9C12 C12 root read, legacy `first_session` HOLD, missing C9 `actor_meta`,
   and `OWNER_ANCHOR_REQUIRED`.
3. B-F1CR reconstruction identity versus the missing original `bf7e625e...`.
4. V3CORE material-only boundary and the 16 held annual steps.
5. No PREMAIN/Pyat/Programma/source owner change.

Required reviewers/owners: a separate I3 sourcefree reviewer; original C9R/BP4/
C12 owner; CP-A5 owner; B/C10 owner; V3 material owner; Sorok/PREMAIN receiver.
The author is not the reviewer and does not adopt its own candidate.

## Rollback

This return is reversible without touching the R2 baseline:

```bash
# Before merge: drop the extension directory and return artifacts.
rm -rf SOROK_PRODUCT_CONTROL_ROOM/RRIF/CODE_CANDIDATE/RRIF_R2/rrif_r3_extension
rm -rf WORKER_RETURNS/SOROK_RRIF_R3_RECOVERED_FOUR_ASSET_CONSUMER_WELD_R1

# After a local commit: revert the additive commit.
git revert --no-edit <rrif-r3-commit>
```

Rollback properties:

- R2 20-test source and files are unchanged, so the R2 baseline remains exactly
  `598d9e9e...`.
- No production or owner SQLite was written; the extension roots live under
  temporary/test paths.
- CP-A5 runtime is a copied sourcefree closure, not a reference to an owner DB.
- C9C12 files are copied candidate files; deleting the extension restores the
  base tree.
- Historical C9 14/1, BP4R 7/2, B3 ghost, F1CI3, G17I/CAN3/OC5E/M04 REDs are
  preserved and are not “fixed” by this return.

## Held grants

Not granted by this return:

- native C9/C12, C9/C12 production writer/anchor, external C12 custodian;
- native actor/person, human A5, B motive, private V3 mental state;
- original F1CR source, R5-to-original identity, B/C10 adoption;
- Pyat N11/N12/C11, Programma, CAN008/011/ADP/SCI05;
- PREMAIN merge, owner adoption, or self-review.
