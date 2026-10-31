# Integration non-adoption and rollback

**Candidate:** `PYAT_PE_SC0_OWNER_BOUND_SOURCEFREE_SUCCESSOR@1.0.0`

**Exact source cuts:** startup
`d0342290b257f85c3e8931f9962e0aecabc84ed3`; current PRE-MAIN
`8e44ca9c751049d65e6def47600b5c073ee04b29`; PRE-MAIN and startup
`rawlsing_next` tree `1d88d3fbb1d18dadfda946d9cd7f309d84afa479`; original PE
`e61a26ce24f023a53d6b116bb9eca2fb7b6f8e65` (blob `58484f4c...`); overlay
`9c030bf4c239d2e14f2b5a8a02ff7b44906cd0c7` (blob `1e4c0e63...`); hostile
review `33b5363a20d44cfb42b3d1e86fdb9615710adb23`.

**Implementation blobs:** `owner_bound_successor.py`
`08f0bea429a8f35223db8acf757ef7b714805603`; `sourcefree_world.py`
`264c6092b5a151960779d0e610f2d964474da920`; `n10e_adapter.py`
`3c9f34fd4f629ccebd8e9efeb485f3a2d7c1c2c5`; `first_consumer.py`
`145977129dcacad6f8a7ec3d2888783a6ed0652c`; `fixtures.py`
`6f3233945aadcf92730a7e77ad301e1a07c52414`; tests
`5a3558f7e60b1afc70210ef5cb1c69fd459049b1` and
`37ad5b63ed2be6fa6b87ee4e93483e51de5b2865`.

**Session:** OpenCode `1.18.34`, agent `build`,
`opencode-go/deepseek-v4.1-flash`, variant `max`, session
`ses_e6f557010ffeVc8ejV937G5Ii9`, PID `28096`.

## Non-adoption

This candidate is **not**:

- merged into PRE-MAIN;
- installed into production source;
- imported by a production entrypoint;
- registered as an N9/world/source/model/actor issuer;
- an N11/N12 permission;
- a replacement for the original PE strict court;
- a claim that the published overlay is repaired in place.

The predecessor overlay must not be installed. Its `sitecustomize.py` is an
auto-injection hazard. The successor deliberately contains no `sitecustomize.py`
and no `install()`-style monkeypatch.

The P41/E04L branch-local service and the #536 P41/R08 dispatch branch were
inspected only. GitHub issue 536 is OPEN; its dispatch branch tip equals its base
`750548ddbb9b4392a16ce93097b856f349e16182` and no worker return existed to
inspect. No existing worker worktree was modified.

## Integration blockers

1. No competent N9/world/source owner grant for selected-world values,
   sanctions, clocks, revision/digest or source promotion.
2. No production receiver that adopts `PYAT_PE_SC0_OWNER_BOUND_RECEIPT@1`.
3. No model-use, actor/person, N11/N12 or production permission.
4. No independent post-return review at the exact pushed SHA.
5. P41/E04L richer products are not reconciled into this minimum envelope; they
   remain separate branch-local apparatuses.
6. The original strict court remains 4 passed / 9 failed at its exact pinned
   tree; the successor does not silently rewrite or xfail it.

## Rollback

Because this candidate writes only under
`WORKER_RETURNS/PYAT-PE-SC0-OWNER-BOUND-SUCCESSOR/`, rollback is file-scoped:

```bash
# from the repository root, after confirming no other return depends on it
rm -rf WORKER_RETURNS/PYAT-PE-SC0-OWNER-BOUND-SUCCESSOR
```

No production file, PRE-MAIN ref, original return, P41/E04L branch or #536 worker
work is touched by that removal. The candidate is not imported by production, so
there is no production runtime rollback beyond deleting the isolated return
directory.

If a future adopter installs the contract, the adopter must also remove its own
integration binding and any production issuer registration; those are outside
this candidate and were not created here.

## Verification commands

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/PYAT-PE-SC0-OWNER-BOUND-SUCCESSOR/SOURCEFREE_CANDIDATE_AND_VERSIONED_API/tests
# 33 passed, exit 0

CAND=/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-pe-sc0-owner-bound-secure-successor-20261031-r1/WORKER_RETURNS/PYAT-PE-SC0-OWNER-BOUND-SUCCESSOR/SOURCEFREE_CANDIDATE_AND_VERSIONED_API
PYTHONPATH="$CAND" python3 -m pytest -q -p no:cacheprovider "$CAND/tests"
# 33 passed at current PRE-MAIN 8e44ca9, exit 0
```

Original/overlay/hostile receipts are in
`SOURCEFREE_CANDIDATE_AND_VERSIONED_API/evidence/`; the exact commands and
counts are in `00_RETURN.md`, `ALL_TWELVE_HOSTILE_TESTS_WITH_EXITS.md` and
`SOURCEFREE_CANDIDATE_AND_VERSIONED_API/evidence/TEST_SUMMARY.json`.

## Environment and custody

- No paid external source operation, original survey, actor run or model-use
  call was made.
- Tests used the local source-free N10E/C1 fixture.
- Fresh temporary detached worktrees at exact tips were used for the original,
  overlay and current PRE-MAIN checks. They are outside the workspace and were
  not merged.
- The candidate's evidence logs are test artifacts, not source evidence.

## Explicit NOT_RUN / UNKNOWN

- Production integration, deployment, merge or adopter binding: **NOT_RUN**.
- P41/E04L and #536 worker suites: **NOT_RUN**.
- Independent post-return review: **NOT_RUN**.
- Original source/actor/N9/model/N11/N12/Sorok operations: **NOT_RUN**.
- MAX beyond process argv `--variant max`: **UNKNOWN**.

## Verdicts

**ENGINEERING:** `ACCEPT_AT_TEST_ONLY_SOURCEFREE_SCOPE__ISOLATED__NO_PRODUCTION_IMPORT__NO_MERGE`.

**SCIENTIFIC:** `HOLD__SYNTHETIC_C1_N10E_ARITHMETIC_ONLY__NO_ORIGINAL_SOURCE_OR_WORLD_MEANING`.

**AUTHORITY:** `HOLD__TEST_ONLY_SOURCEFREE_GRANT_ONLY__NO_COMPETENT_SOURCE_N9_WORLD_MODEL_ACTOR_OR_PRODUCTION_AUTHORITY`.
