# RRIF-E minimal receiving packet

This packet is an additive repair over the exact RRIF-R2 candidate. It is not a
PRE-MAIN merge and does not install the 444-file vendor closure by itself.

## Prerequisite

Install the exact R2 candidate at `base_candidate_commit`
`598d9e9eaba5143950c63317705fd09104fbf463` under
`SOROK_PRODUCT_CONTROL_ROOM/RRIF/CODE_CANDIDATE/RRIF_R2`.

Verify `SOURCE_MANIFEST.json` has SHA-256
`7cfcb4679e36b522e83cc7120dbc166ce61dd220099c2aca8f5c9ddb5252c126`
and exactly 444 rows. Do not replace vendor bytes.

## Apply

```sh
cd <premain-worktree>
patch -p1 -d SOROK_PRODUCT_CONTROL_ROOM/RRIF/CODE_CANDIDATE/RRIF_R2 \
  < <candidate>/receiving_packet/RRIF_E_ADDITIVE.patch
python3 SOROK_PRODUCT_CONTROL_ROOM/RRIF/CODE_CANDIDATE/RRIF_R2/first_consumer_cli.py \
  --root /tmp/rrif-e-receipt
```

Expected first-consumer status:
`PASS_PARTIAL_SAME_ROOT_C9_C12__C9_ACTOR_OWNER_HELD__CP_A5_SEPARATE_ROOT`.

Expected C9/C12 edge:
`INCOMPATIBLE_WITHOUT_OWNER_MIGRATION__ROOT_COLD_READ_ONLY_UNDER_OWNER_ANCHOR_HOLD__FORK_LEGACY_ROOT_UNVERIFIED`.

## Review questions

1. Is the exact 444-file R2 vendor closure accepted as the base?
2. Is the repaired C12 verifier accepted as self-consistency only, not external custody?
3. Does the C9/C12 incompatibility remain owner-held or does the owner issue a lawful migration?
4. Does the owner accept the separate-root CP-A5 consumer without a same-root actor weld?

## Rollback

```sh
git -C <premain-worktree> checkout -- SOROK_PRODUCT_CONTROL_ROOM/RRIF/CODE_CANDIDATE/RRIF_R2
git -C <premain-worktree> clean -fd SOROK_PRODUCT_CONTROL_ROOM/RRIF/CODE_CANDIDATE/RRIF_R2
```

No PREMAIN commit, force push, native grant or owner adoption is performed.
