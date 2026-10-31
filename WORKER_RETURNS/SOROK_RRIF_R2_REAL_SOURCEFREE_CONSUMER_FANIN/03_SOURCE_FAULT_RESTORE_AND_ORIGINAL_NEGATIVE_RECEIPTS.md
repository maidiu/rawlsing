# Source-fault, restore, C12 preimage and preserved negatives

## 1. Test command actually run

```sh
C="$PWD/SOROK_PRODUCT_CONTROL_ROOM/RRIF/CODE_CANDIDATE/RRIF_R2"
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$C:$PWD" \
python3 -m pytest -o addopts='' -q -p no:cacheprovider \
  SOROK_PRODUCT_CONTROL_ROOM/RRIF/CODE_CANDIDATE/RRIF_R2/tests/test_join.py \
  SOROK_PRODUCT_CONTROL_ROOM/RRIF/CODE_CANDIDATE/RRIF_R2/tests/test_rrif_r2_c12.py \
  --junitxml=WORKER_RETURNS/SOROK_RRIF_R2_REAL_SOURCEFREE_CONSUMER_FANIN/evidence/rrif_r2_junit.xml
```

Actual:

```text
.................... [100%]
20 passed in 28.60s
JUnit: tests=20 failures=0 errors=0 skipped=0
```

This executes the JOIN-E tests and the added C12 tamper/restore test against the
candidate source. It is sourcefree, not native.

## 2. C12 self-referential verifier repair and adverse test

The sourcefree C12 path uses `r26e.c12_integrity.QualifiedC12Store`, not the
raw `bp4.store.C12Store.verify`. The former recomputes the actual persisted
preimages and drops the post-hash `episode_id` from the episode body:

```text
episode:      digest(body without hash, without episode_id)
world_event:  digest(body without hash)
checkpoint:   digest(state without hash)
perception:   sequence integrity
```

Added test `test_c12_episode_preimage_tamper_is_detected_and_restores`:

1. Start `JoinedSession` with `perform=omit`.
2. Open the C12 SQLite file and select the first episode preimage.
3. Simulate a raw-database attacker by dropping the append-only trigger and
   modifying the body with `tampered_for_rrif_proof=true`.
4. `JoinedSession.open(state)` raises
   `BRANCH_C12_VERIFY_FAILED: ["episode:0:body_hash_mismatch"]`.
5. Restore the exact original body.
6. `JoinedSession.open(state)` succeeds and `c12_verify("root")` is `ok=true`.

Added test `test_independent_c12_verifier_rejects_forged_episode_hash`:

- modifies the episode body with a forged source claim;
- asserts `QualifiedC12Store.verify(branch)` `ok=false` with
  `body_hash_mismatch`;
- asserts the reconciliation-side `bp2p4.c12_verify.verify_branch_chain` also
  returns false.

This is the required independent recompute, not an author assertion and not a
trust-the-state check. The test also demonstrates a valid restoration after
the adverse mutation.

## 3. C9 target source fault/restore

Existing JOIN-E test `test_c9_target_consumer_severance_cold_red_restore`:

- starts a sourcefree JOIN product, closes it, and directly toggles/mutates the
  C9 `target_state` row;
- cold positive becomes RED (`C9`/`TARGET` error);
- the exact original target body is restored;
- cold positive returns GREEN and verifies.

This is C9 source severance/restore, not a native E2 claim. The C9 target
remains a TEST_ONLY row.

## 4. B source identity substitution and restore

Existing tests cover the two required B-source behaviors:

- `test_coordinated_sidecar_and_meta_source_substitution_rejected`: coordinated
  mutation of `bp2_join.json` and `session.json` to `REFUSE_TOOL`/foreign actors
  yields `J_PROVENANCE_MISMATCH`.
- `test_b_source_edge_help_observable_and_targetless_no_target`: observed
  `SHARE_TOOL` gives `HELP_ACCEPT` and tool retained; targetless `REFUSE_TOOL`
  gives `HELP_REFUSE`, no target and no fabricated E2; cold targetless reopen
  remains refused.

The `e2`/`omit` pair is a real source-sensitive behavior:

```text
omit -> tools_remaining=1 -> HELP_ACCEPT
e2   -> tools_remaining=0 -> HELP_REFUSE
```

No invented consent, no hidden B interior and no source mutation is accepted.

## 5. Preserved historical negatives

These are **not** erased by the new green:

| Historical negative | Preserved status |
|---|---|
| C9 R3B original-version court | `14 passed / 1 failed`; unchanged negative/fault witness |
| BP4R old writer-clock/anchor diagnostics | `7 passed / 2 failed`; preserved |
| B3/X3 original ghost/partial-write cases | historical RED; not rewritten |
| F1CI3 | three RED preserved |
| G17I | three RED; source/future/C9 fake inputs |
| CAN3 | nine RED preserved |
| OC5E | 49 RED preserved |
| M04 | ten original RED preserved |
| F1CR claimed patch | `SOURCE_NOT_FOUND`; reconstruction is not original |
| C9 old/new reader/writer cuts | compatibility constraint, not resolved by recency |

The candidate uses JOIN-E at `7bf2` and its R29P/R26E qualified C12 verifier.
It does not import C9C12-R2, CP-A5-R2, B-F1CR-R2 or V3CORE-R1 as native or
unqualified successors.

## 6. Negative tests actually executed

The 20-test run includes:

- foreign/wrong-root and relocated-root refusal;
- coordinated source/meta mutation refusal;
- missing/orphan product refusal;
- branch lineage tamper refusal;
- nested fork receipt isolation and rollback;
- targetless refusal and cold refusal;
- private-state/actor-ignorance surface separation;
- attention exclusion of actor decision;
- CLI closure/manifest/session verification;
- C12 episode tamper/restore and forged preimage rejection.

No test treats a branch name, author test count or source recovery count as a
native or human claim.
