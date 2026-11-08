# C18 — independent exact-head review of PR #774 / issue #772 Q86 identity guard

**Review:** issue #777 authorized next sourcefree court from C16 per-issue actions; independent nonauthor review of the existing Q86 identity guard.
**PR:** #774, `R8: bind frozen Field Forge Q86 producer to exact source identity`, **OPEN**, `reviews=[]` at intake.
**Exact PR head/sourcecut:** `9c776b358c5f5a31f2ff2d35460d5350c0dc2bc8`.
**PR base:** `integration/pre-main-reconciliation-r1@7a5429ffbc48efd25e28c912da80c822e66bc182`.
**R7 comparison base:** `392de04e86202a2a80361a91808ef06fd34c1cc8` (PR #770; separately open, no reviews, not accepted).
**Reviewer:** existing qualified C5 reviewer reused; not an author of PR #774, the Q86 guard, issue #772 implementation, C14/fan-in, or any implementation under review. Prior C5/C15 review relationship is disclosed; this is the required nonauthor guard review, not author self-review.
**Session/model:** `ses_e47b17f8fffedazgQeSGbql4HH`; actual model `deepseek-v4.1-flash`, provider `opencode-go`, variant `max` (from `actual-model.json`); no model/provider/account/region/effort change.
**Verdict:** **`ACCEPT_SCOPED` for the isolated identity guard at `9c776b`**, with an explicit downstream-closure boundary and a proof-artifact reporting note. **Combined R7+Q86 chain remains HELD** because PR #770 is open/unreviewed. No merge, no CI waiver, no production reachability, no generic FF currentness/semantics, no native/S3/science/actor authority.

## 1. Exact source diff and scope

The PR base is protected `7a5429ff`; the exact head is `9c776b35`. The source change is **18 added lines** in `rawlsing_next/field_forge_conditional_support.py`:

- `_frozen_q86_source_identity()` at lines 125–128 resolves the existing `wave1_r5_q86_c11_projection.question_ref("Q86B"/"Q86A")`.
- `_validate_frozen_q86_source_identity()` at lines 131–139 requires exact `ExactRef` equality.
- The guard is called at line 516, after the existing fact/query closure and query component/role-order validation, and **before** profile construction at lines 518+.

No C→D bridge, D→M4, M1/M4/M5/N9, permission/ceiling, relation-family/version, or generic FF source change is present. The test changes only replace invented `urn:test:gt12c:Q86A/B` refs with the exact source refs and add identity/negative witnesses. The R7-relative diff is the same guard and tests, not an R7 code import.

Exact source hashes:

```text
ed2dbd2fff1d9f8ebab2c5c74b41af2444490f6645aa702fcdd03767bc1bd538  rawlsing_next/field_forge_conditional_support.py
3c6639109338eed4d84dccd203732f5238c72e240d2a4339f68e17cca88bc8bf  rawlsing_next/tests/test_field_forge_conditional_support.py
8ca3d3610285010d64c4870a54376def7829a4b73e4f6dc762f0ee02a59b9258  rawlsing_next/tests/test_gt12_closure_b_c_to_d_bridge.py
93cdd81a56ce1075757c6259358c20f83f599679ac1e4f1df2ccb5f1043deb5b  rawlsing_next/tests/test_gt12_e2b_actual_object_consumer_harness.py
```

The exact Q86 source refs are:

```text
Q86B  QUESTION_IMPLEMENTATION  question_impl.phase0.2fb3a62609dad4c1306d  2fb3a62609dad4c1306d8cfa14f997eab4d6e65ada56083279386a202544a506
Q86A  QUESTION_IMPLEMENTATION  question_impl.phase0.67f036c0efb7fb98ff4a  67f036c0efb7fb98ff4a93dc811bf59cfc095608eda374f6534b006a62241bd3
```

## 2. Retained positive — verified from the committed sourcefree transport

The review created one disposable sparse detached worktree at the authorized path from shared objects at `9c776b`, containing `rawlsing_next` plus the committed sourcefree GT2 transport and the Q86 return evidence; no respondent/SAV/DTA/DB or original source directory was included. The transport is the existing sourcefree hashed-ref package, not original respondent rows.

`probes/independent_probe.py` called the unchanged pinned producer with the retained `EmpiricalQuerySpec`/`EmpiricalFact` from `load_current_gt2_query_fact_from_committed_transport()`:

```text
typed_state=SUPPORTED
condition_rows=6
conditioner_ref=Q86B exact QUESTION_IMPLEMENTATION 2fb3a626...
target_ref=Q86A exact QUESTION_IMPLEMENTATION 67f036c0...
relation_ref=urn:rawlsing:field-forge:conditional-support:sha256:1ffdfe536adc01d35709521145b9c8057f589c20983f507d5ed6197c4ad27d19
count_profile_hash=49bf14eb4a2b7fbf8e79ea4c72d10f4027819381564f582242ef6e24fc14fb59
C→D admission=ADMITTED
reason=EXACT_GT2_RELATION_ADMITTED_FOR_STRUCTURAL_MEDIATION_INPUT
target_use_permissions=[STRUCTURAL_MEDIATION_INPUT]
```

This independently confirms the PR's claimed retained relation/count-profile hashes and that the retained Q86 refs still reach the same positive C→D admission. The synthetic closure-B fixture used by `06_R8_PROOF_RUNNER.py` has a different relation hash (`e9b9eb5d…`) and count-profile hash (`2c8fb38c…`); that is a different fixture, not the retained product. The submitted `R8_PROOF_TRACE.json` does not show the retained `1ffdfe/49bf14` positive; C18's probe supplies that missing independent evidence. The author should add the retained positive/receipt to the proof trace (reporting note, not a code defect).

## 3. Identity negatives — refused before profile minting

The unchanged pinned code and tests produce:

| Negative | Observed |
|---|---|
| Unlike Q99B→Q99A pair | `FieldForgeConditionalSupportError`; no profile returned |
| Forged Q86 object-id with wrong exact kind (`QUESTION`) | `FieldForgeConditionalSupportError`; no profile returned |
| Wrong Q86A identity/content hash at same object-id | `FieldForgeConditionalSupportError`; no profile returned |
| Swapped Q86 roles/order | `FieldForgeConditionalSupportError`; no profile returned |

These are the intended identity failures: exact-ref equality includes kind, object-id and content-hash; the guard does not parse a substring or trust a label. The guard runs after `_query_component_material` (which independently checks `query.target_refs == (conditioner_ref, target_ref)` and exact component refs/order), so a caller cannot pass Q86 argument refs with a Q99 query/fact and mint a mislabeled profile.

## 4. Downstream closure negatives — exact boundary

The existing bridge/admission owner still closes the rest of the frozen chain. Observed:

| Negative | Observed boundary |
|---|---|
| Wrong risk set | profile can be built with exact Q86 refs; `GT12CToDBridgeError: frozen risk-set exact identity mismatch`; no C→D admission |
| Wrong source family | `OUT_OF_SCOPE` / `SOURCE_FAMILY_OR_WAVE_MISMATCH`; no target-use permission |
| Wrong source wave | `OUT_OF_SCOPE` / `SOURCE_FAMILY_OR_WAVE_MISMATCH`; no target-use permission |
| Wrong source artifact | `INTEGRITY_FAILURE` / `SOURCE_ARTIFACT_IDENTITY_MISMATCH`; no target-use permission |
| Missing/narrow relation permission | `DENIED` / `TARGET_USE_NOT_PERMITTED_BY_RELATION`; no target-use permission |
| Nonpositive upstream fact (`OBSERVED_ZERO`) | relation remains `OBSERVED_ZERO`; admission `UNRESOLVED` / `UPSTREAM_RELATION_OBSERVED_ZERO`; no positive profile/admission |
| Cold restore (synthetic closure-B baseline) | exact baseline relation ref restored; `ADMITTED` |

**Boundary:** identity negatives refuse **before profile minting**. Wrong risk/source/artifact/missing permission can mint a `SUPPORTED` profile object and are refused at the existing **C→D admission** boundary. This is the declared narrow scope of the identity guard and preserves the existing bridge as the risk/source/permission owner. It meets the requirement “no positive C→D admission,” but it does **not** satisfy a literal “no positive profile object” reading for those downstream negatives. If HQ requires producer-level refusal for risk/source/permission, that is a separate owner/scope decision and must not be added to this identity guard by the reviewer.

## 5. Tests and inherited failures

Independent focused runs in the pinned disposable worktree (unchanged code, Python 3.11.3, `python3 -P`, no env install):

```text
42 passed in 0.50s
  test_field_forge_conditional_support.py
  test_gt12_closure_b_c_to_d_bridge.py
  test_gt12_e2b_actual_object_consumer_harness.py

40 passed in 111.04s
  test_pre553_gt2_structural_positive_realization_court.py
```

The author's broader 140/58/41/29 test claims were not rerun (full-matrix prohibition); they remain author evidence. The first pytest invocation from the review checkout imported the review checkout's unguarded `rawlsing_next` and showed two failures; that is a harness path-shadowing error, preserved as `focused_pytest_shadowed_import_ERROR.log`, not a PR failure. The pinned `python3 -P` rerun is the valid result.

Inherited failures are preserved, not attributed to the guard:

- PR #774 CI: `canonical-tree` PASS; `governed-court` FAIL on the three inherited protected-base packaging tests; `3 failed, 144 passed in 50.44s` (author/CI record; not a changed-guard failure). No false CI green.
- GT34/A2 group: author-recorded `1 failed, 12 passed, 3 errors` identically on the untouched R7 base and R8 branch; exact names in `07_R7_GATE_AND_INHERITED_FAILURES.md`. Not rerun here due the full-matrix prohibition.
- The changed guard tests and retained structural court pass independently.

## 6. Sixteen-chain cross-check and generic-FF boundary

The existing `02_INDEXED_16_CHAIN_CROSSCHECK.tsv` has exactly 16 rows `Q86-S01`–`Q86-S16`; no new census was performed. Key stage answer is consistent with the actual protected code:

- `Q86-S16` PRE553 I03/I05 generic empirical query: `PROVED_CURRENT`; no Q86 literal/default in `pre553_empirical_query.py`.
- `Q86-S01` frozen FF Q86 producer: `BOUNDED_CANARY_ONLY`; guard now rejects unlike pairs before profile.
- `Q86-S02`–`S06`, `S08`, `S11`: bounded source-specific canaries / receiver seams, not generic FF.
- `Q86-S07`, `S09`, `S10`: no selected non-test receiver proved.
- `Q86-S12`: P1 constructor `TEST_ONLY_UNMERGED`.
- `Q86-S13`: GF1 generic pair candidate `TEST_ONLY_UNMERGED` PR #691; protected path absent.
- `Q86-S14`: retained Q86 context `TEST_ONLY_UNMERGED`.
- `Q86-S15`: R2 architecture `UNKNOWN` at runtime.

No generic Field Forge relation producer is proved to run alongside Q86 at a current protected stage. The generic empirical path is current at PRE553 I03/I05, then stops at the unmerged/test-only GF1 candidate. This does not close A9/A10; the 16-chain is not exhaustive and no generic FF currentness/semantics is claimed.

## 7. R7 separation and combined-chain status

R7 PR #770 at `392de04e` is **OPEN**, `reviews=[]`, `governed-court` FAIL (inherited packaging tests), `canonical-tree` PASS. Its independent acceptance is pending and is **not** a dependency of this isolated guard review: PR #774 is based on protected `7a5429`, and the guard diff is independent. However, combined T01/T02/T03 + Q86 guard acceptance remains **HELD** until R7 and the guard both receive governed review; this review does not accept the combined chain, does not merge, and does not waive CI.

## 8. Terminal disposition and next action

**Guard disposition:** `ACCEPT_SCOPED` at `9c776b358c5f5a31f2ff2d35460d5350c0dc2bc8` for the isolated Q86 exact-source-identity guard: exact refs, retained positive `1ffdfe/49bf14`, identity negatives, sourcefree tests, retained structural court, no generic/production overclaim.

**Boundary/limits:** downstream risk/source/artifact/permission negatives are admission-level; wrong risk/source/artifact/missing permission can create a `SUPPORTED` profile before C→D refusal. Do not call this producer-level closure. If HQ requires that stronger property, a separate owner-correct decision/repair is required; do not widen this guard by review fiat.

**Next authorized action:** HQ/PR owner may record the retained positive in the proof trace and adjudicate the isolated guard at the scoped disposition. Do not merge until R7 and combined-chain gates are separately accepted; no production, native/S3, science, actor, generic FF, or CI-waiver claim. If a selected current non-test Q86 operation is later demanded, that is a separate demand/issuer question; this guard does not prove it.

**No action from this review:** no code/runtime/test/HQ/peer/protected write; no new worker; no merge; no CI waiver; no goal-complete claim.

## 9. Evidence and limits

- Exact PR/base/head and remote readback: `logs/pr774_metadata.json`, `logs/source_identity.txt`.
- Findings: `FINDINGS.jsonl` (exact copy also at `01_FINDINGS.jsonl`).
- Source hashes and 16-chain evidence: `logs/source_identity.txt`.
- Proof runner: `probes/06_R8_PROOF_RUNNER.py`, `logs/proof_runner_pinned.stdout.json`, `probes/R8_PROOF_TRACE.json`.
- Independent retained/negative probe: `probes/independent_probe.py`, `probes/independent_probe.json`, `logs/independent_probe.stdout.json`.
- Focused tests: `logs/focused_pytest_pinned.log`, `logs/retained_structural_court.log`; path-shadowed harness error retained separately.
- Actual model: `logs/actual-model.json`.

No original respondent/SAV/DTA/DB/source-byte read, native/S3/science/actor effect, environment install, production/existing-test/HQ/peer/protected write, new issuer, new worker, recurring polling, full matrix, redundant census, merge, CI waiver, or goal-complete claim. The disposable sparse worktree was removed after evidence/source-hash retention; existing worktrees were not touched. Quota `UNKNOWN`.

**Final:** `ACCEPT_SCOPED` for the isolated Q86 identity guard; downstream closure boundary recorded; retained hash independently verified; combined R7+Q86 chain still held; no merge/production/native acceptance.
