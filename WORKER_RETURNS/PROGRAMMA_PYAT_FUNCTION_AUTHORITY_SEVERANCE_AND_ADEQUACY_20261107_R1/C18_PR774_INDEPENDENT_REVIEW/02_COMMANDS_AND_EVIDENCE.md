# C18 — commands, hashes and evidence

**Review:** PR #774 / issue #772 Q86 source-identity guard.
**PR head:** `9c776b358c5f5a31f2ff2d35460d5350c0dc2bc8` (OPEN, `reviews=[]` at intake).
**PR base:** `7a5429ffbc48efd25e28c912da80c822e66bc182`.
**R7 comparison base:** `392de04e86202a2a80361a91808ef06fd34c1cc8` (PR #770; open, no reviews).
**Verdict:** `ACCEPT_SCOPED` for the isolated identity guard; combined R7+Q86 chain held.

All commands were read-only over HQ/PR/source/existing tests except writes under `C18_PR774_INDEPENDENT_REVIEW/` and the authorized disposable sparse worktree. No original respondent/SAV/DTA/DB/source-byte read, native/S3/science/actor effect, environment install, production/test/HQ/peer/protected write, new issuer, new worker, merge or CI waiver occurred.

## 1. Worktree/lease and exact PR identity

```sh
cd /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat777-c5-source35-independent-review
git branch --show-current
git rev-parse HEAD
git status --short
```

Result: branch `agent/pyat777-c5-source35-independent-review-20261107-r1`, HEAD `c4f68989788a0a0b27a3b65be610502cb4a824db`; only the C18 lease/output is untracked before commit.

```sh
gh pr view 774 --repo maidiu/rawlsing --json number,title,state,isDraft,headRefName,headRefOid,baseRefName,baseRefOid,reviews
git ls-remote origin refs/heads/fix/pyat-r8-frozen-ff-q86-source-identity-guard-20261107-r1
git ls-remote origin refs/heads/integration/pre-main-reconciliation-r1
git -C /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat777-authority-severance-hq rev-parse 7a5429ffbc48efd25e28c912da80c822e66bc182
```

Result:

```text
PR #774: OPEN, headRefOid=9c776b358c5f5a31f2ff2d35460d5350c0dc2bc8,
baseRefOid=7a5429ffbc48efd25e28c912da80c822e66bc182,
headRefName=fix/pyat-r8-frozen-ff-q86-source-identity-guard-20261107-r1,
reviews=[]
remote PR branch=9c776b358c5f5a31f2ff2d35460d5350c0dc2bc8
remote protected=7a5429ffbc48efd25e28c912da80c822e66bc182
local protected object=7a5429ffbc48efd25e28c912da80c822e66bc182
```

`logs/pr774_metadata.json` retains the JSON readback.

## 2. Exact source diff and hashes

```sh
git -C /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat777-authority-severance-hq diff \
  7a5429ffbc48efd25e28c912da80c822e66bc182..9c776b358c5f5a31f2ff2d35460d5350c0dc2bc8 \
  -- rawlsing_next/field_forge_conditional_support.py
```

Result: 18 added lines only —

- `_frozen_q86_source_identity()` lines 125–128;
- `_validate_frozen_q86_source_identity()` lines 131–139;
- one call at line 516, before profile construction.

The R7-relative diff (`392de04e..9c776b`) contains the same guard plus the added identity tests; no C→D/D→M4/M1/M4/M5/N9/permission/relation-family change.

Exact source/test hashes (`logs/source_identity.txt`):

```text
ed2dbd2fff1d9f8ebab2c5c74b41af2444490f6645aa702fcdd03767bc1bd538  rawlsing_next/field_forge_conditional_support.py
3c6639109338eed4d84dccd203732f5238c72e240d2a4339f68e17cca88bc8bf  rawlsing_next/tests/test_field_forge_conditional_support.py
8ca3d3610285010d64c4870a54376def7829a4b73e4f6dc762f0ee02a59b9258  rawlsing_next/tests/test_gt12_closure_b_c_to_d_bridge.py
93cdd81a56ce1075757c6259358c20f83f599679ac1e4f1df2ccb5f1043deb5b  rawlsing_next/tests/test_gt12_e2b_actual_object_consumer_harness.py
58e29ed60e5b222b89ec5e15583d3587e3824a7b2cbc580b08a6c22568f1a2f5  .../06_R8_PROOF_RUNNER.py
0e88ee8cad16309bacdb93d085e4f1fc5fbc59c10f46301258c95ab650696558  .../02_INDEXED_16_CHAIN_CROSSCHECK.tsv
```

## 3. Disposable sparse worktree and exact-source execution

One disposable detached sparse worktree was created from shared objects at the authorized path:

```text
/Users/matthewsmith/Desktop/Rawlsing_Controller/local-automation-state/pyat777-01a15c1e/pyat777-pr774-independent-guard-review-r1/pinned-source
```

It contained `rawlsing_next` plus the existing sourcefree GT2 transport under `data/ddm_build_copy/.../R4A_CURRENT_GT2_EXECUTION_CONSTRUCTOR_COMPLETE_EXTRACTION_R2` and the PR return evidence. The transport is the committed sourcefree hashed-ref package (`respondent_ref_hashes.bin` is a hash list), not original respondent/source rows. No SAV/DTA/DB or original-source directory was included. Python: 3.11.3. No environment install.

The first pytest attempt from the review checkout used `PYTHONPATH=<pinned>` but cwd shadowed it with the review checkout's unguarded `rawlsing_next`; two tests failed. That is preserved as `logs/focused_pytest_shadowed_import_ERROR.log` and is **not** a code failure. Re-running with `python3 -P` (safe path) imported the pinned code.

## 4. Focused tests and proof runner

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 PYTHONPATH="$PIN" \
python3 -P -B -m pytest \
  "$PIN/rawlsing_next/tests/test_field_forge_conditional_support.py" \
  "$PIN/rawlsing_next/tests/test_gt12_closure_b_c_to_d_bridge.py" \
  "$PIN/rawlsing_next/tests/test_gt12_e2b_actual_object_consumer_harness.py" \
  -q -p no:cacheprovider -p no:warnings
```

Result: `42 passed in 0.50s` (`logs/focused_pytest_pinned.log`).

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 PYTHONPATH="$PIN" \
python3 -P -B "$C18/probes/06_R8_PROOF_RUNNER.py"
```

Result: exit 0, `logs/proof_runner_pinned.stdout.json`; baseline synthetic closure-B relation hash `e9b9eb5d1904262a3be7689f5853c23cedef09e2bcb9256db7cb28072d207891`, count-profile `2c8fb38c06db7f63d0ee78d71bcc40c8889601f9f503a10c7d8fdbb63f44a520`; all identity negatives refused; wrong risk/source/artifact/permission/nonpositive behaved as expected; cold restore matched baseline.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 TMPDIR="$C18/tmp" PYTHONPATH="$PIN" \
python3 -P -B -m pytest "$PIN/rawlsing_next/tests/test_pre553_gt2_structural_positive_realization_court.py" \
  -q -p no:cacheprovider -p no:warnings
```

Result: `40 passed in 111.04s` (`logs/retained_structural_court.log`). This test loads the committed sourcefree GT2 transport and exercises the retained structural positive path.

## 5. Independent retained/negative probe

`probes/independent_probe.py` is an independently written probe using the unchanged pinned public producer/bridge and the committed sourcefree transport. Run:

```sh
PYTHONPATH="$PIN" python3 -P -B "$C18/probes/independent_probe.py"
```

Result (also `probes/independent_probe.json` / `logs/independent_probe.stdout.json`):

```text
retained relation_ref = 1ffdfe536adc01d35709521145b9c8057f589c20983f507d5ed6197c4ad27d19
retained count_profile_hash = 49bf14eb4a2b7fbf8e79ea4c72d10f4027819381564f582242ef6e24fc14fb59
retained typed_state = SUPPORTED, condition_rows = 6
C→D admission = ADMITTED / EXACT_GT2_RELATION_ADMITTED_FOR_STRUCTURAL_MEDIATION_INPUT
target_use_permissions = [STRUCTURAL_MEDIATION_INPUT]

unlike_Q99B_Q99A = refused FieldForgeConditionalSupportError
forged_Q86_object_id_wrong_kind = refused FieldForgeConditionalSupportError
forged_Q86_wrong_identity_hash = refused FieldForgeConditionalSupportError
swapped_Q86_roles = refused FieldForgeConditionalSupportError

wrong_risk = refused GT12CToDBridgeError (frozen risk-set exact identity mismatch)
wrong_source_family = OUT_OF_SCOPE / SOURCE_FAMILY_OR_WAVE_MISMATCH; no target use
wrong_source_wave = OUT_OF_SCOPE / SOURCE_FAMILY_OR_WAVE_MISMATCH; no target use
wrong_source_artifact = INTEGRITY_FAILURE / SOURCE_ARTIFACT_IDENTITY_MISMATCH; no target use
wrong_permission = DENIED / TARGET_USE_NOT_PERMITTED_BY_RELATION; no target use
nonpositive_observed_zero = UNRESOLVED / UPSTREAM_RELATION_OBSERVED_ZERO; no target use
cold_restore = exact synthetic closure-B baseline ref; ADMITTED
```

This independently confirms the PR's declared retained `1ffdfe/49bf14` hashes. The synthetic closure-B baseline (`e9b9…/2c8f…`) is a different fixture; the author's `R8_PROOF_TRACE.json` contains the synthetic baseline, not the retained positive. `C18-008` records the proof-artifact gap; the code/behavior is verified.

## 6. 16-chain cross-check

The existing `02_INDEXED_16_CHAIN_CROSSCHECK.tsv` has 16 rows `Q86-S01`–`Q86-S16`; no new census was run. Spot-checked against pinned code:

- `Q86-S16` PRE553 I03/I05 generic query: `PROVED_CURRENT`; `pre553_empirical_query.py` has no Q86 literal/default.
- `Q86-S13` GF1 generic pair candidate: `TEST_ONLY_UNMERGED`; protected `rawlsing_next/gf1_pair_support_consumer.py` is absent.
- `Q86-S01` guard lines 125–139,516; Q86-S02–S06/S08/S11 bounded canaries/seams; Q86-S07/S09/S10 no receiver; Q86-S12/S14 test-only/unmerged; Q86-S15 architecture/UNKNOWN.

This is not an exhaustive census; A9/A10 remain open. No generic Field Forge relation producer is proved to run alongside Q86 at a current protected stage.

## 7. CI, inherited failures and R7

```sh
gh pr checks 774 --repo maidiu/rawlsing
gh pr view 770 --repo maidiu/rawlsing --json number,state,isDraft,headRefOid,reviews,statusCheckRollup
```

Result:

```text
PR #774: governed-court FAIL (3 failed, 144 passed in 50.44s; inherited protected-base packaging tests);
         canonical-tree PASS; no changed-guard test failure reported.
PR #770: OPEN; reviews=[]; head 392de04e; governed-court FAIL; canonical-tree PASS.
GT34/A2 author-recorded: 1 failed, 12 passed, 3 errors identically on untouched R7 base;
         exact names in 07_R7_GATE_AND_INHERITED_FAILURES.md. Not rerun here (full-matrix prohibition).
```

No false CI green. The inherited 3 packaging failures and GT34/A2 failure/errors are separate from the changed guard. R7 acceptance is pending and not used as a dependency for the isolated guard; combined T01/T02/T03 + Q86 guard acceptance remains held.

## 8. Model and session

`logs/actual-model.json` records the actual turn:

```text
session=ses_e47b17f8fffedazgQeSGbql4HH
model.id=deepseek-v4.1-flash
providerID=opencode-go
variant=max
```

No model/provider/account/region/effort change was made. The `OPENCODE_SESSION_ID` environment matched the C18 session.

## 9. Cleanup and evidence retention

The disposable sparse worktree was cleaned after evidence/source-hash retention:

```text
pinned worktree removed; existing worktrees untouched
```

Evidence retained under `C18_PR774_INDEPENDENT_REVIEW/`: `00_REVIEW.md`, `FINDINGS.jsonl` (exact copy also at `01_FINDINGS.jsonl`), `02_COMMANDS_AND_EVIDENCE.md`, `probes/`, `logs/`.

## 10. Boundary

`ACCEPT_SCOPED` applies to the isolated exact-Q86-source-identity guard at `9c776b`. Identity negatives refuse before profile. Wrong risk/source/artifact/missing permission can create a `SUPPORTED` profile before the existing C→D bridge refuses; that is admission-level closure, not producer-level. It meets "no positive C→D admission" but not a literal "no positive profile object" reading for downstream closure. If HQ requires the latter, it is a separate owner/scope decision and must not be added to this identity guard by review fiat. The retained positive hash is independently verified; the author should add it to the proof trace. No merge, production/native/generic FF claim, or CI waiver is made.
