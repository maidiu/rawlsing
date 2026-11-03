# F6 final independent recheck — 22d671 vs 23edffb32

**Candidate:** `22d6712090970597e0c161b9f12eaece84bda5c5`
**Prior review:** `23edffb32141c133c8b45b723bb23f092928115c`
**Snapshot:** exact `git archive` from sibling `pyat-pdev01-f6`, `WORKER_RETURNS/PDEV01-F6-COMPARISON` only
**Scope:** `WORKER_RETURNS/PDEV01-F6-INDEPENDENT-REVIEW/final-recheck/`

## Scoped verdict

**`ACCEPT_ENGINEERING_CORRECTION__SCIENCE_AUTHORITY_HOLD_UNCHANGED`**

The corrections required by review `23edffb32` are present and independently
reproduce from the exact candidate snapshot. This is an engineering correction
acceptance only; it is not F6M/F6P scientific adoption, source permission,
transport/model-use grant, production installation, or an N9/N11/N12 wake.

## Corrections verified

1. **Raw boundary exception is a plain `KeyError`**
   - `type`: `KeyError`
   - `args`: `("native_bundle",)`
   - `str`: `"'native_bundle'"`
   - F6P supplies neither `native_bundle` nor `native_conditional_consumer`.

2. **Diagnostic ownership**
   - Authored label:
     `COMPARISON_LOCAL_BOUNDARY_SHAPE_DIFFERENCE__NOT_EMITTED_BY_F6P_OR_WP2`
   - Present in the comparison harness; absent from both F6P consumer and WP2
     source.
   - No typed receiver exception is claimed.

3. **No unexecuted receiver effects**
   - `wp2_receiver_executed=false`
   - `observed_effect=null`
   - `f6m_to_e04_join_claimed=false`
   - The old `NO_NONPARENT_OPTIONS_READ` / `NO_F6M_E04_JOIN` strings are absent
     from the candidate comparison files.

4. **Historical F6C outputs are exact**
   - Embedded files match the pinned `c1ebe091f` outputs byte-for-byte, not just
     by manifest declaration.
   - `A`: `3df50e9801326e43925150611de5d6fa2a89f4b7ee38bce093c96139e6a68561`
     (9,204,043 bytes)
   - `A0`: `0bb40d883c4f0aab1b07218b8cb32e618e7560a57b796e643f3c53060423d110`
     (9,203,068 bytes)
   - `B`: `01e0bce46799320da8f9c61f1edae04dc081574542fc0b78ff3d5277a767b720`
     (9,210,880 bytes)
   - Git blobs `1357a834…`, `e246e768…`, `b4d82136…` match the manifest.
   - The copied substitution receipt remains correctly marked as not
     self-contained.

5. **Checkout-root hash limit**
   - Candidate W1: `20f1d417843920e7913149db0cd9083dae9cc1db0d5031393a6bb1c297a915f9`
   - Prior-review W1: `2fbe5cff7445483fc7ad266c0b62599351cad66aae9dbc9c764ad08afa4db1cc`
   - Fresh snapshot W1: `5194fa883b305687e2653ad208798eb8e329bd8ead6a6d5165a653a91de6089a`
   - Semantics are equal; the difference is the absolute
     `source_product.module_file` embedded in F6P `output_hash`. Only
     same-checkout seed0/seed1 identity is claimed.

## Tests actually rerun

Focused correction tests only, on the exact disposable snapshot:

- `test_review_corrections.py`, `PYTHONHASHSEED=0`: **4 passed**
- `test_review_corrections.py`, `PYTHONHASHSEED=1`: **4 passed**

No unrelated F6P author/publication/reviewer suites were rerun. Prior review
`23edffb32` supplies those prior results.

## Reused prior review

The prior review evidence established the semantic bounds/uncovered mass/point
refusal and historical F6C receiver invariance. This recheck reused that
evidence and only re-verified the corrections and exact snapshot behavior.

## Holds

- Candidate F6M/F6P artifacts remain sourcefree TEST_ONLY.
- No original SAV/DTA, original respondents, source rights, population,
  transport, model-use, route probability or selection weight is created.
- No production edit, WP2 adapter, compiler replacement, CI, merge or
  downstream wake.
- Candidate worktree was read-only; the disposable snapshot is separate.
- The existing exact-tree scan file still labels the earlier production tree
  `aa18b6b85`; commit `22d671` changed only the F6 comparison return, so the
  production-tree conclusion is unchanged. No production claim is extended.

**Independent acceptance of the F6 science/authority remains held.**
