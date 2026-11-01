# RRIF-E — minimal receiving patch and rollback

## Target

- Current PRE-MAIN read cut: `8e44ca9c751049d65e6def47600b5c073ee04b29`.
- Target path: `SOROK_PRODUCT_CONTROL_ROOM/RRIF/CODE_CANDIDATE/RRIF_R2`.
- No PRE-MAIN branch, PR, ruleset or production database was modified.

## What is minimal

The packet is additive over the exact RRIF-R2 candidate:

- R2 base commit `598d9e9eaba5143950c63317705fd09104fbf463`;
- exact 444-file vendor manifest, SHA-256
  `7cfcb4679e36b522e83cc7120dbc166ce61dd220099c2aca8f5c9ddb5252c126`;
- additive patch `candidate/receiving_packet/RRIF_E_ADDITIVE.patch` with only:
  - repaired C12 verifier,
  - honest self-exclusion/source audit,
  - coordinated custody report,
  - exact C9/C12 compatibility,
  - same-root first consumer and CLI,
  - repair tests and the corrected original C12 test,
  - repaired candidate preimage.

The patch does **not** contain a blanket transplant of eight Gate01 branches,
the 444 vendor files, a C9 actor migration, a CP-A5 actor relabel, or an external
key/anchor.

## Apply (owner action only)

```sh
cd <premain-worktree>
patch -p1 -d SOROK_PRODUCT_CONTROL_ROOM/RRIF/CODE_CANDIDATE/RRIF_R2 \
  < <candidate>/receiving_packet/RRIF_E_ADDITIVE.patch
```

Or use `candidate/receiving_packet/apply.sh` with the R2 base already installed.
The apply script refuses if the base is missing.

Run:

```sh
PYTHONPATH="$R2:$R2/rrif_r3_extension:$REPO" \
python3 -m pytest -o addopts='' -q -p no:cacheprovider \
  "$R2/tests/test_join.py" "$R2/tests/test_rrif_r2_c12.py" \
  "$R2/tests/test_rrif_e_repair.py"

PYTHONPATH="$R2:$R2/rrif_r3_extension:$REPO" \
python3 "$R2/first_consumer_cli.py" --root /tmp/rrif-e-receipt
```

Expected: 26 passed; first-consumer status
`PASS_PARTIAL_SAME_ROOT_C9_C12__C9_ACTOR_OWNER_HELD__CP_A5_SEPARATE_ROOT`;
C9/C12 edge
`INCOMPATIBLE_WITHOUT_OWNER_MIGRATION__ROOT_COLD_READ_ONLY_UNDER_OWNER_ANCHOR_HOLD__FORK_LEGACY_ROOT_UNVERIFIED`.

The patch was tested in a clean R2 base copy at matching repository depth:
`patch -p1` applied with exit 0 and **26 passed** (see
`candidate/receiving_packet/PATCH_APPLY_TEST.md`).

## Dependencies

- R2 vendor closure 444 exact files, source commits R31J/R31E.
- Local Python 3.11+, pytest, SQLite.
- No network, provider, native source or production database.

## Independent review questions

1. Is the exact R2 vendor closure accepted as a prerequisite without rewriting
   its bytes or source manifest?
2. Is the repaired C12 verifier accepted only as self-consistency, not external
   owner custody?
3. Does the C9/C12 incompatibility remain owner-held, or does a competent owner
   issue a migration and new actor/root contract?
4. Is CP-A5 accepted as a separate-root sourcefree consumer without a synthetic
   same-root weld?
5. Is the external C12 owner anchor/issuer identified before any authenticity or
   completeness claim?

## Rollback

```sh
git -C <premain-worktree> checkout -- SOROK_PRODUCT_CONTROL_ROOM/RRIF/CODE_CANDIDATE/RRIF_R2
git -C <premain-worktree> clean -fd SOROK_PRODUCT_CONTROL_ROOM/RRIF/CODE_CANDIDATE/RRIF_R2
```

No force push, self-merge, production adoption or owner authorization is
performed by this worker. The candidate branch remains unmerged until a
competent owner and independent reviewer act.
