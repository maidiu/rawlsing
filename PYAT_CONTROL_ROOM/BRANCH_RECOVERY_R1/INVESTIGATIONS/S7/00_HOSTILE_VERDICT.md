# PYAT 845 S7 — INDEPENDENT HOSTILE WHOLE-ESTATE VERDICT

**Return branch:** `review/pyat-845-s7-independent-full-recovery-acceptance-20261030-r1`  
**Startup:** `750548ddbb9b4392a16ce93097b856f349e16182`  
**Final S7 SHA:** reported externally after push; a commit cannot contain its own hash.  
**Role:** fresh independent hostile reviewer. Not S1–S6 author, H1 author, original reviewer, source/scientific issuer, or own reviewer.  
**Worktree:** `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-845-s7-independent-full-recovery-acceptance-20261030-r1`  
**Device/harness/model:** mainMac; OpenCode 1.18.34 agent `build`; `opencode-go/deepseek-v4.1-flash`, variant `max`.  
**Independent session:** `ses_e700ee99affet8V64XRG9BwxGt`, title `PYAT 845 S7 independent whole-estate hostile court`, directory is this worktree. This is not S1/H1 session `ses_e7285576bffeqo0lE8N0HYK6gc`; the OpenCode DB shows that claimed H1 session is titled `Retained GT2 → N10E analytical consumer (H03)` with directory `/Users/matthewsmith`. H1's session-independence claim therefore fails, although S7 independently reproduced its material test results.

## 1. Exact inputs and current PRE-MAIN

| Item | Exact value |
|---|---|
| S6 return | `2c5cf86beb12b7dbeda5532614784737ad30d89d` |
| H1 return | `815edc1bd74094522afb8c9dad1742ecb77ec800` |
| PE/V2K repair return | `9647d851a2d9b6e93e6711eec7a65325fb83aaa1` |
| S1 corrected | `6a658ad347ad0a714f40cbce04b5cd6d1f5b5ab5` |
| S2 corrected | `3042fca8a2165e07871d408118e1741686020cdc` |
| S3 corrected | `ebdb51a5c79209b2e552cfce648f7847b19386c2` |
| S4 corrected | `d93e8c2441dfa394e56fc1f5bcf43a0b4388adcb` |
| S5 corrected | `32dac59b3741dcc54f507321c7826e65174af372` |
| Evidence law | `f50651a2bb0758e9fe6d6a2852441dcc782344be` |
| PRE-MAIN at dispatch and recheck | `87755f02ec5c37499b09e80db6fbdcc9316a6b15` |
| S6/H1 checked PRE-MAIN | `5fc1d43e3d5412194d1f1eaa30ff448f84635e99` |
| `rawlsing_next` tree at all three cuts | `1d88d3fbb1d18dadfda946d9cd7f309d84afa479` |

`87755f02` is unchanged from dispatch. Its difference from `5fc1d43e` is three audit/workflow files only. There is **no `rawlsing_next` production delta** between the S6/H1 cut and the S7 cut.

## 2. Custody verdict — PASS

- **845/845 branch names** are present exactly once across S1–S5. There are **838 distinct roster tips** because seven tip pairs are shared by two branch names. All roster tip objects exist.
- Remote recheck: **844/845 roster tips match the current origin branch head**. One frozen roster tip has moved: `proposal/pyat-stranded-branch-recovery-20261028-r1`, roster `3b5ff992a8579d35285c63c98efa1b7dccfb6d96`, current origin `becf0bfb04705b8fe0927dd56e7290e1dcd180a8` (one docs commit later). The frozen tip remains valid and is recorded; this is a delta, not a missing branch.
- **3,135/3,135 function rows**, each ID unique, exactly once, with per-shard counts `1279 + 218 + 398 + 897 + 343`. Corrected row order matches each original row index in all five shards.
- Ordered-ID custody hashes:
  - S1 `b3393f7ba5fc452f4225d46f9bbec870478466c562be82ac848463260214185d`
  - S2 `a2395017983425c16634dd9900eefe148b66775cfd1a3e8a50c0c6f15405075d`
  - S3 `8976b390e86127faf76c4323ac9c6659291c51056af1c451995e7642de4b4fd4`
  - S4 `2c99213df5bcc2064ce3e18ab8bc6a8a582f0137deee931c6c82717a8b5b5958`
  - S5 `76dfba2e30b4d7fc421622eec0c641481f1d9169f48fb5733e2ddc84d3b82a33`
  - Combined `5917b3bd58bb56f101d0daa35a0259761234a58a6c4bf9adaf6f0586d3593a68`
- GitHub Actions run **41162150215** (`cdcb4d39e7e1815c387558115ae9a2715cd10367`) is green and independently checks the S6 one-to-one membership. S7 rechecked the same invariant from the five corrected returns.
- Full branch-by-branch custody is in `845_BRANCH_ACCOUNTING.json`.

## 3. S6 group verdict — membership PASS, behavioral equivalence FAIL

`CROSS_SHARD_FUNCTION_GROUPS.jsonl` has **1,881 groups**: **1,879 row-derived groups + 2 external zero-member priority cases**. All 3,135 member IDs occur exactly once. Group `member_count`, shard sums, label sums and disposition sums are internally consistent for all 1,879 row groups. This is a genuine custody result.

It is **not** behavioral equivalence:

- **328 groups** contain more than one historical blob.
- **173 groups** contain more than one distinct AST body for the same path+symbol. The largest variants are `compare_temporal_anchors` (7 AST variants / 8 rows, F7-P07), `EvidenceResolver` (8/8, R61-R08), `evaluate_learned_world_consumer` (6/7), and `materialize_native_preimages` (5/6, R61-R03).
- **93 groups** have no historical blob at all.
- Grouping is exact **path + qualified symbol**, not behavioral identity or consumer identity. The group record does not prove that variants are interchangeable, nor that a current same-name implementation has the same behavior.
- **Six boundary defects** were found by AST/actual-qualname audit:
  - Five `SourceRelationResolver` groups merge outer-class and nested `_make_sealed_source_relation_owner.SourceRelationResolver` methods because S4 truncated nested qualnames: `FAM_b8e8a1c5bac3370d` (`__init__`), `FAM_1427a684892de839` (`require`), `FAM_214c6eaf1fe2a42d` (`_validate_positive`), `FAM_6813a575a7ce67c0` (`decide`), `FAM_c0d48f7daa8cc28d` (`resolve_exact`). The bodies differ; defect/merit conflation is possible.
  - One nested function is split across two groups: `PhysicalSourceIncidence.iter_batches.emit` appears in `FAM_bd6118ca46930519` (S4 row `4f7cd7ccb7a06b3d6a4f75f19c65dd16d6911445`) and `S6FAM-23dd9c27fe2a7c60` (S5 row `rawlsing_next/pre553_physical_decoder.py::PhysicalSourceIncidence.iter_batches.emit`).
- S6's own receiver map records **1,824 groups with `NO_REAL_RECEIVER_YET`**, **56 groups with `TEXT_REFERENCE_ONLY__NOT_EXECUTED`**, and **1 group with `NO_REAL_RECEIVER_YET__E03_EXACT_NOT_WHOLE_SERVICE`**. No executed callgraph was produced.

**Verdict:** `S6_MEMBERSHIP_PASS__BEHAVIORAL_EQUIVALENCE_UNPROVEN__SIX_BOUNDARY_DEFECTS`.

## 4. H1 challenge verdict — material results reproduce, two claims need correction

H1's `H1_S1_S5_GRADE_CHALLENGES.jsonl` has exactly **2,146** rows with the claimed verdict distribution. S7 independently reproduced the aggregate original-label counts: **89 SUPERSEDED_BETTER**, **555 HELD**, **713 adaptation**, **187 INVALID/TRASH**, **119 READY**.

### 4.1 S1's 150 `CURRENT_PRODUCTION_ACCEPTED_AT_NAMED_SCOPE` — REVISE CONFIRMED

- All **150/150** are `EXACT_AST_SAME_PATH` at `87755f02`; code presence is real.
- All **150/150** have `positive_oracle=NOT_TESTED`, `receipts=[]`, and no row-level E3 execution.
- **27** rows are in source modules outside the four current test modules: `_pre553_query_common` 12, `physical_decoder` 7, `source_native_preimage_adapter` 5, `empirical_query` 2, `analytical_composition` 1.
- S7 reran the four current universal modules at `87755f02`: **105 passed, exit 0**. That is module coverage, not row-level acceptance.
- **Verdict:** `ENGINEERING_REVISE__CURRENT_CODE_EXACT__ROW_LEVEL_E3_UNPROVEN`. Full 150 IDs are in `845_BRANCH_ACCOUNTING.json`.

### 4.2 S4's 325 `RENAMED_EQUIVALENT_PROVEN` — RED CONFIRMED, with a field nuance

- All **325/325** rows carry `CURRENT_FUNCTIONAL_PRESENCE=RENAMED_EQUIVALENT_PROVEN` but `ADOPTION=HISTORICAL_ACCEPTANCE_ONLY`.
- S7 independently compared original occurrence AST bodies to current `87755f02`: **325/325 exact body matches**. The body-exactness claim is true.
- All 325 have `evidence_strength=E1_EXACT_CURRENT_BODY_PRESENCE`, `positive_oracle=NOT_TESTED`, `fault_negative_oracle=NOT_TESTED`, `receipts=[]`, and empty consumer arrays. **323/325** original paths are under `WORKER_RETURNS`.
- H1's “first_consumer is empty” is substantively correct, but the field is present as `{non_test: [], test: []}` rather than absent.
- **Verdict:** `ENGINEERING_RED__RENAMED_BODY_EXACT__BEHAVIORAL_EQUIVALENCE_UNPROVEN`. It is not a current production claim, but it is also not behavioral equivalence proof.

### 4.3 Other H1 claims

- **S5 119 READY:** all are current-untested; RED confirmed.
- **S3 negative receipts:** all reproduced (below).
- **S3/S4 custody:** S3 398/398 direct attributes match; S4 897/897 original path is in the original occurrence paths. S3/S4 still lack `original_row_sha256`; S1/S2/S5 hashes verify.
- **H1's 28 specific defects:** not exactly reproducible as stated. S7 finds S3 5 + S4 11 + S5 13 + S2 1 = **30** specific defect rows. The claimed 28 subset reproduces as **27** (S3 5 + S4 11 + S5 11); the two S5 native Stage A/B rows and S2 `F0215` are additional. All named negatives remain preserved; no H1 defect is discarded.
- **H1 session independence:** FAIL. The claimed session is a different H03 session. S7 is fresh and independently reran the material receipts.

## 5. Reproduced test receipts

| Court | Exact tip | Command (worktree-root cwd) | Actual result | Exit |
|---|---|---|---|---|
| S3 seam | `ed34944e253b78714a28d72b8ca2a6521ce15930` | `PYTHONPATH=. python3 -m pytest rawlsing_next/tests/test_r3_s02_seam_witness.py -q` | **26 passed, 1 failed**; `test_s00c_change_source_owned_synthetic_numeric_values_changes_result: KeyError exact_probabilities` | 1 |
| S3 selected-world | `ed34944e…` | `PYTHONPATH=. python3 -m pytest rawlsing_next/tests/test_pre553_selected_world_progressive_contract.py -q` | **24 passed** | 0 |
| S3 E03 | `ed34944e…` | `PYTHONPATH=. python3 -m pytest rawlsing_next/tests/test_pre553_n9_n10w_progressive_candidate.py -q` | **18 passed** | 0 |
| S3 PE strict original | `e61a26ce24f023a53d6b116bb9eca2fb7b6f8e65` | `HQ297_EXACT_PE_ROOT=$PWD PYTHONPATH=. python3 -m pytest rawlsing_next/tests/test_hq297_k9k10_sc0_pe_independent.py -q` | **4 passed, 9 failed** | 1 |
| S3 V2K original | `694fb45085cd5e4891949921a44edb77c3f603f2` | `PV_RETURN=<tip>/WORKER_RETURNS/PYAT-R3-POSTASTRA-PV-V2K-INDEPENDENT-COURT-R1 PYTHONPATH=. python3 -m pytest rawlsing_next/tests/test_hq295_v2k_original_identity_successor.py rawlsing_next/tests/test_postastra_pv_v2k_independent.py -q` | **2 collection errors**; missing `pre553_original_workload_contract_v2_candidate` | 2 |
| Current universal | `87755f02ec5c37499b09e80db6fbdcc9316a6b15` | `PYTHONPATH=. python3 -m pytest rawlsing_next/tests/test_universal_grammar.py rawlsing_next/tests/test_universal_workload.py rawlsing_next/tests/test_universal_source_byte_custody.py rawlsing_next/tests/test_universal_source_projection.py -q` | **105 passed** | 0 |
| PE repaired candidate competence | `9647d851a2d9b6e93e6711eec7a65325fb83aaa1` | `PYTHONPATH=. python3 -m pytest WORKER_RETURNS/PYAT-R3-PE-V2K-SCOPED-RECOVERY/tests/test_pe_reversed_issuer_repair.py -q` | **2 passed** | 0 |
| V2K dependency severance at exact repair tree | `9647d851…` | `PYTHONPATH=. python3 -m pytest WORKER_RETURNS/PYAT-R3-PE-V2K-SCOPED-RECOVERY/tests/test_v2k_dependency_severance.py -q` | **1 passed, 1 failed**; V2K module itself is absent at the exact branch | 1 |

The PE 9 failures are exactly: `test_strict_reverse_scoped_issuer_forgery_must_refuse`, `test_strict_selected_world_nary_F2_AH_strata_roundtrip`, `test_strict_generated_runtime_fact_echo_not_source_promotion`, `test_strict_two_distinct_world_refresh_receipts`, `test_strict_four_clocks_historical_knowledge`, `test_strict_negative_status_algebra_and_source_risk`, `test_strict_values_read_not_only_hash_or_inferred_label`, `test_strict_nonparent_apprenticeship_world_effect`, `test_strict_parent_scenario_remains_input_only`.

**NOT_RUN:** F7/P07 HQ232/HQ236/HQ240 replay; R61-R09 D1/D4/D7 replay; P41 19 tests + 3 witnesses; C3 55-test court; V2K 63/24/50 suites requiring externally restored dependencies; repaired PE strict 5/8; native source/U/E; executed current production consumers/whole-service. All are `NOT_RUN`, not inferred green.

## 6. Reconstructed provenance for consequential families

S6 left 664/1,879 introducing tips null. S7 reconstructed exact blob-introducing commits independently. Representative results:

| Family | Exact introduced blob | Introducing commit (date) | Current at 87755f02 | Branch containment |
|---|---|---|---|---|
| R61-R08 binder | `3ca860e409f1d063da4cd03dd1691a89c67333f6` | `80bb8c18241ebcd7ddbe559b76c6b39a72025b89` (2026-10-23 19:20:39 -0400) | absent | 2/845 |
| R61-R03 universal workload | `8e7fe00a3ed008361d9f3c501e7782b2de3a636e` | `5ba003e6ce0c42b690e7128fb6b7e08f409f5576` (2026-10-24 02:22:13 -0400) | exact | 72/845 |
| R61-R03 issued workload | `31e84f49d624f5524906e9e7839d2873106f8249` | `aaaccb6437092e8e0581059c000943f000d93670` (2026-10-19 16:51:18 -0400) | exact | 1/845 |
| R61-R03 native binding | `dac73e484f8619088f5c6701b2b6991c07540f3b` | `54a2c427c94767b29653426f7cfb55db9cf22aac` (2026-10-24 00:30:14 -0400) | exact | 75/845 |
| R61-R03 preimage adapter | `a6299c1a6e8b26bd055ced1f49e5b757f20ccd8c` | `453a951307bbf9112f576907f48f88524247261f` (2026-10-22 02:21:08 -0400) | exact | 2/845 |
| Current decoder / R56 custody | `8732e34d0ea3f4cfffd7d33ee00f258dbc2d65dd` | `31a39c50cb5e8487968ab7b00386912fc5f1d6ca` (2026-10-22 04:32:29 -0400) | exact | 106/845 |
| Current R5 codec | `72f8f3c03ed065e86fea4e76bb17f8e06c2bf540` | `99489f9930d6bd8ffead45245395f9b306d2673e` (2026-08-21 17:36:27 -0400) | exact | 0/845 (pre-roster mainline) |
| C3 decoder candidate | `d3d828c171ea9fdd0e90563aff6ef705f5aae2cf` | `901e3e77f905847d3ef8d86b458280d8fe422dd0` (2026-09-29 16:37:15 -0400) | different current | 3/845 |
| R9 final runtime | broker `090d978b…`, session `ac1390b8…`, binding `0e11af22…` | `dfdf5659fd78e9bc996b07383349094059a5553d` (2026-10-04 15:06:53 -0400) | absent | 2/845 |
| F7/P07 sealed owners | `d9fb2c48…` / `8053d30d…` | `d5e6d6baa67ddf25a9864be6bb2564b535e0868f` (2026-10-07 14:52:06 -0400) / `c86ae335eaf70e82b5764c46754b16ca7e1587ce` (2026-10-07 18:48:28 -0400) | temporal absent; resolver present/test-only | 19/845 and 16/845 |
| PE candidate | `58484f4c3d9aae148d4116dcf00420c432aefcbd` | `b497f85713847cecc169d4d71c7629655d562dc0` (2026-10-14 10:39:56 -0400) | present, no static consumer | 3/845 |
| P41 service | `7d428106c79bcc56973f7c0044fc273a2b354554` | `24f80eeb31684d704e5c82b7ae880acdf01a933a` (2026-10-19 03:18:48 -0400) | absent (E03 exact only) | 1/845 |
| Selected-world seam | seam / contract | `208bca30471710d48124a6b69ba467f240d8834b` (2026-10-12 22:35:02 -0400) / `c98e888166a941a06ad694411911bc58f9c4639b` (2026-10-12 15:15:53 -0400) | absent | historical tips |
| R157 config | factory family | earliest `dbbb623b059f84640ffa7f7ad5eb097ba13ac02e` (2026-10-26 22:47:42 -0400) | absent | historical branch |

The R5 codec blob is inherited mainline code and is **not** carried by any of the 845 frozen branches. That is a current-code fact, not a recovery claim.

## 7. Exact current receivers / UNKNOWN

| Family | Exact current receiver or UNKNOWN |
|---|---|
| Physical decoder / R5 | Static imports at `fiabc_lm2_r1e_common_c11.py:24/30`, `pre553_physical_c11_bridge.py:10`, `pre553_source_backed_c11_facade.py:35/38`, `fiabc_lits_i_representation_authority.py:20/21`, `fiabc_lm2_r1j_wvs7_representation_authority.py:22`, `pre553_route_b_production.py:53`; executed consumer NOT_RUN |
| R61-R03 candidate library | `pre553_native_workload_binding.py` imports `pre553_issued_workload`; `pre553_universal_workload` imports native binding; only `tests/test_universal_workload.py` imports universal_workload; **NO_PRODUCTION_ENTRYPOINT_FOUND** |
| E03 / P41 | E03 exact `84d40414…` is imported only by `tests/test_pre553_n9_n10w_progressive_candidate.py:15`; no production import; P41 service absent |
| Source relations / F7 | `pre553_source_relations.py` is imported only by `tests/test_pre553_source_relations.py:13` and referenced as a string in `fiabc_succession_producer.py:59`; no production import |
| PE | No static current receiver found; PE tests only at historical tips |
| Sources equivalence / local universe | Tests only; no production import |
| R61-R08, R9, selected-world, V2K, R157 factory, G01 | Path absent; **UNKNOWN / no current receiver** |

## 8. Courts

| Court | Verdict |
|---|---|
| **ENGINEERING** | `CUSTODY_PASS__S6_MEMBERSHIP_PASS__S6_BEHAVIORAL_EQUIVALENCE_FAIL__H1_S1_REVISE__H1_S4_RED__S3_NEGATIVES_REPRODUCED__PE_REPAIR_PARTIAL__PRODUCTION_NOT_READY` |
| **SCIENTIFIC** | `HOLD__NO_SOURCE_NATIVE_READ__NO_CAN_ADP_SCI__NO_ORIGINAL_SURVEY_RESPONSE__NO_SCIENCE_ISSUANCE__SOURCEFREE_ONLY` |
| **AUTHORITY** | `HOLD__NO_ADOPTION__NO_MERGE__NO_MODEL_WORLD_ACTOR_N11_N12_GRANT__NO_SOROK_ACTOR__NO_SELF_ADOPTION` |
| **PRODUCTION** | `NOT_READY__1824_GROUPS_NO_REAL_RECEIVER__56_TEXT_ONLY__1_E03_EXACT_NOT_WHOLE_SERVICE__SIX_GROUP_BOUNDARY_DEFECTS` |

## 9. Actionable priorities

1. **Repair S6 family boundaries and re-key dispositions.** Split the five nested/outer `SourceRelationResolver` groups and join the two `iter_batches.emit` groups. Do not use group IDs as behavioral units until this is fixed.
2. **Make production-readiness evidence row-level.** For the S1 150, run current-receiver positive and fault-negative per row, especially the 27 outside the four universal test modules. For the S4 325, run ABI/consumer/fault-negative equivalence, not body-identity.
3. **Port C3 G01/D01/D02 + R5 carrier into the current decoder/r5 while preserving PR526 `_SourceSnapshot` custody; rerun the 55-test C3 court on the current receiver.**
4. **Integrate R9 broker/session/binding as sourcefree modules; reconcile the decoder route with PR526 custody; run the 20/15/34/R7 courts.**
5. **Diff and test the 118 KB R61-R08 binder against current provider/C1/J42/P41; run sourcefree positive and fault-negative; route to independent owner review.**
6. **Port P41 service onto current E03/C1/N10E/M4/M5; run 19 tests + 3 severance witnesses; keep N9/N10W/N11 holds.**
7. **Repair F7/P07 owner custody and TCB; rerun HQ232/HQ236 negatives and F7 49/159; do not promote the sealed owner.**
8. **Repair the selected-world seam `KeyError` and rerun 27 tests with zero failures; only then integrate the selected-world contract with a current P41/C1/N9 consumer.**
9. **PE/V2K:** decide the remaining 8 PE SC0 value-bearing gaps; make V2K exact dependency or a new current ABI adapter self-contained. Preserve `_auth` repair as sourcefree candidate only.
10. **R61-R09:** build a parent-owned observation and loaded-byte channel; rerun D1/D4/D7 plus a real C11 positive.
11. **R157:** map 35 configurations to current source-local-universe/source-equivalence owners; actual U/E_pre execution only under a separate competent grant.

No source, scientific, model, world, actor, N11/N12, Sorok, production or merge authority was granted or self-issued. No production code was changed. S7 does not adopt S6, H1, PE/V2K, or any candidate.
