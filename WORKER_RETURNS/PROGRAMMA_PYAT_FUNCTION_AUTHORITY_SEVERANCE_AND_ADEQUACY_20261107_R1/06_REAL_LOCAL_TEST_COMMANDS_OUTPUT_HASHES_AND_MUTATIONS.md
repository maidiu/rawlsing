# 06 — Real local test commands, output hashes and mutations (reused receipts; no rerun)

**Rule:** this fan-in did **not** execute tests, probes, source code, source configuration or original data. The commands, exits, counts, hashes and mutation classes below are **reused from the accepted C1–C6 receipts** at the exact author/review cuts. Where a lane did not run a test or a mutation, it is recorded as `NOT_RUN`. No new test, probe, code patch, source-byte read or source_configuration execution was performed in this lease.

## Exact cuts

| Lane | Author/correction cut | Review cut | Evidence root |
|---|---|---|---|
| C1 | `79c4f33c51e7d0146e06e12cac6ea903c79cb7b0` | `753ff5dc95fb218f84ebf1697a91a2d392367f2c` | `pyat777-source-consumer/.../C1_SOURCE_CONSUMER` |
| C2 | `b132fa4a02b31ba539b33f24ad022846bb81acb8` | `638f75e7b661057954f7dbd3b58739b83ec2e8e1` | `pyat777-joint-consumer/.../C2_JOINT_CONSUMER` |
| C3 | `3fd285d671d51c8576fd2b962bc34eda1a714ece` | `aa122437b1fe224f4c6ea2ee31ed2f7de6af7323` | `pyat777-ff-postff-consumer/.../C3_FF_POSTFF_CONSUMER` |
| C4 | `950ff275527a2963253336cbb05924a6c2943cd8` | `0def1171f8f9d2681b64ebe287adb7d209c896c7` | `pyat777-joint-consumer/.../C4_J_ROLE_FIRST_CONSUMER` |
| C5 | `451f8d1e094800d523589cdd4db5159a338db836` | `ea9ff9e54e2bc7c9a56a1398d172e87a8f109f03` | `pyat777-source-consumer/.../C5_SOURCE_ESTATE_PRODUCER_CONSUMER` |
| C6 | `0d548b033a0a20c9738fa4a3412ba5acd01217c5` | `333ade4e4c003595630d7f53eaeece85902d6759` | `pyat777-joint-consumer/.../C6_HISTORICAL_SELECTED_USE` |

Protected source observation for C1–C5: `7a5429ffbc48efd25e28c912da80c822e66bc182`. Historical source for C6: `9ba4764bef551b1ce498e5772d60b73d69337d4b`. C6 R4 ledger: `0c5b385d858033306c6221bcd344b2f69616ff29`; R1 exact readset: `5296ede23c667a6ab044dfb92a15e29205c6fd11`; F1 cut: `6f8da13c2734ba1b5e83ff0de6c0ab1aefe3cf95`.

## C1 — Q86 R5 source-semantic first consumer

Environment: `mainMac.lan`, Darwin 22.3.0 x86_64, Python 3.11.3, `PYTHONDONTWRITEBYTECODE=1`, `PYTHONHASHSEED=0`, `-p no:cacheprovider`, `TMPDIR`/basetemp under the C1 lease. Model actual: `opencode-go/deepseek-v4.1-flash`; separate effort telemetry not exposed; commission target DeepSeek V4.1 Flash MAX.

### C1-1 — Inherited focused 97-test suite (PASS)

```sh
cd /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat777-source-consumer
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 TMPDIR=<C1>/tmp PYTHONPATH="$PWD" \
python3 -B -m pytest -q -p no:cacheprovider --basetemp=<C1>/tmp/pytest-97 \
  rawlsing_next/tests/test_pre553_c11_repository_ingest.py \
  rawlsing_next/tests/test_pre553_source_backed_c11_facade.py \
  rawlsing_next/tests/test_pre553_empirical_query.py \
  rawlsing_next/tests/test_field_forge_conditional_support.py \
  rawlsing_next/tests/test_gt12_closure_b_c_to_d_bridge.py \
  rawlsing_next/tests/test_gt12_e2b_actual_object_consumer_harness.py
```

Result: exit `0`; `97 passed in 3.02s`. Log SHA-256: `1b2cbb19e5ac4a0f00a25fdd1f147a6b04878208947eb70aac6a866f14868809`.

### C1-2 — Direct Q86 sourcefree/canary tests (PASS)

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 TMPDIR=<C1>/tmp PYTHONPATH="$PWD" \
python3 -B -m pytest -q -p no:cacheprovider --basetemp=<C1>/tmp/pytest-q86 \
  rawlsing_next/tests/test_wave1_gt12_i03_positive_facts.py
```

Result: exit `0`; `8 passed in 0.32s`. Log SHA-256: `cf3877f5a0006b0cfe5842a91c99c70d59a6ac6d7e439551f7f664fc7cfe8886`.

### C1-3 — R7 T01 named falsifier rerun (RED + restoration PASS)

```sh
git show 392de04e86202a2a80361a91808ef06fd34c1cc8:WORKER_RETURNS/PROGRAMMA-PYAT-WHOLE-PIPELINE-AUTHORITY-AUDIT-20261107-R1/R7_SOURCEFREE_FIRST_CONSUMER_TESTS/08_EXECUTION_RUNNER.py > <C1>/probes/r7_t01_runner.py
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 TMPDIR=<C1>/tmp PYTHONPATH="$PWD" \
python3 -B <C1>/probes/r7_t01_runner.py
```

Result: exit `0`. Wrong-kind, wrong-operation and wrong-scope ALLOW authorities each reach `SUPPORTED 2/2`; DENY is `UNAVAILABLE 0/0`; cold restore matches baseline. Runner SHA-256 `21f695335e73839475e4321222fbf9ed28ae7d4889c903644c6d6c026a6ee4d4`; trace `54114666a2442a3a844184dd53acdb51d62120e455e940d0f94f1fa478ca20ef`; mutation ledger `2342ec75ba97a652c08d5f3e984dcb7ab6a82107547e76c3ab06e248cba620c0`. Scope: generic C11/I03 falsifier, **not** Q86 selected-original proof.

### C1-4 — Q86 selected-authority/source-semantic probe (PASS, SOURCEFREE_COMPARE_ONLY)

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 TMPDIR=<C1>/tmp \
python3 -B <C1>/probes/q86_source_semantics_probe.py
```

Result: exit `0`. AR-0033 present, 15,498,257 bytes, SHA-256 `305cb215485bc95ebecee395e578c52739311bc2fc15faed27318bd922f47332`. Q86A/Q86B 6 rows each; `context_only`, `recommended_computation=none`; contract hashes `198f189a...`/`01ceeb78...`; substantive `curated_packet`, special `curated_special`. Probe SHA-256 `1484506c8a794ff987e357d01171c86adb4caf4785725cf2fbebb55acec86412`; output `1b3ed2379bbdd6c4425b91053b83d2416f21537fd19c7964f8258460e4ccd77c`; raw log `6e2499141fed1a02f003a6bf37edbc21dbf83a595cc17ed0d33ab030c7a0a87a`. `PROVENANCE_RED`: selected AR-0033 Q86 contract hash not bound; current candidate substitute `UNPROVED`; **not** proved severance. `RESTORATION_PASS`: synthetic baseline `SUPPORTED 3/3`.

### C1-5 — Q86 exact negative/restoration probe (PASS)

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 TMPDIR=<C1>/tmp PYTHONPATH="$PWD" \
python3 -B <C1>/probes/q86_negative_probe.py
```

Result: exit `0`; baseline `SUPPORTED 3/3`; typed refusal for wrong source SHA, wrong QIMPL, wrong source-structure/wave grain, wrong common risk-set count, wrong target-use operation, widened GT1 permission ceiling; restoration `true`; baseline `SUPPORTED 3/3`. Probe SHA-256 `403fd84765052308bd98c01f4a1031722bb3740c825195ff24686feafb6fb38f`; output/log `b0f013381ef6ae167403a5cc508c5dd84018f0371e1bfd34d6ab237140aae294`. Selected Q86 version/shadow/withdrawal/cold restore at the actual selected row: `NOT_RUN`.

### C1-6 — Case builder / anti-join

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 TMPDIR=<C1>/tmp PYTHONPATH="$PWD" \
python3 -B <C1>/probes/build_case_outputs.py
```

Result: exit `0`; 212 register rows preserved, 17 matched, 195 unmatched; one case `C1-Q86-R5-RAW-001`. Builder SHA-256 `8f684884c68ecefae8972d9588466c46789d1e8137e77baff5bbb5477ae3c1ae`; `01_CASES` `1a494391d0e1cf817efde6aad5878d3fc1dec12969e58af805ebdeb6d883a767`; `02_CASES` `861dbea0b415c9bb634fafd4c85cad6fb6505e6f0be4cd3ba268e74aeb6772b3`; `04_MINIMAL_OWNER_ACTIONS` `44153bcc716838490cab290654ee43d62af529b070801c68c9a8023ae3debcfc`; `05_REGISTER_ANTIJOIN` `2f7975d2463bc83601ddce8e6700c64f2e99520e5a35ee667a03267f264b48b4`; corrected build log `0c02bc0b3899d257ef58a109d594bd9c4bca3403e093ff2b85589629329ec3be`.

C1 source hashes: `wave1_gt12_i03_positive_facts.py` `ab14f87d...`; `pre553_c11_ingest.py` `0c56a0f6...`; `_pre553_query_common.py` `969fb4c3...`; `_pre553_query_eval.py` `9c7613a5...`; `pre553_source_backed_c11_facade.py` `7788feb5...`; `pre553_empirical_query.py` `7cd7fd4f...`; `field_forge_conditional_support.py` `ec9558c6...`; `gt12_c_to_d_relation_bridge.py` `3360a935...`; `test_wave1_gt12_i03_positive_facts.py` `79d99a1c...`.

## C2 — O11 exact joint sourcefree composition

All commands from `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat777-joint-consumer` with `PYTHONDONTWRITEBYTECODE=1`, `TMPDIR` under `C2_JOINT_CONSUMER/tmp`.

### C2-1 — Sourcefree probe

```sh
cd /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat777-joint-consumer
PYTHONDONTWRITEBYTECODE=1 TMPDIR="$PWD/WORKER_RETURNS/PROGRAMMA_PYAT_FUNCTION_AUTHORITY_SEVERANCE_AND_ADEQUACY_20261107_R1/C2_JOINT_CONSUMER/tmp" \
python3 WORKER_RETURNS/PROGRAMMA_PYAT_FUNCTION_AUTHORITY_SEVERANCE_AND_ADEQUACY_20261107_R1/C2_JOINT_CONSUMER/probes/probe_joint.py \
> WORKER_RETURNS/.../C2_JOINT_CONSUMER/logs/probe_joint.json 2> .../logs/probe_joint.err
```

Result: exit `0`; stderr empty. Fixture `E03_PROGRESSIVE_ABC_Y_58`, 58 synthetic nonrespondent rows, `real_subject=False`. Provider `EXACT_SUPPORTED_SLICE_PRODUCED` (actual invocation log), composition `SUPPORTED`, consumer `EXACT_SUPPORTED`; denominators `32/16/8`; fractions `9/16`, `5/8`, `3/4`. Negatives: wrong conditioner order and false pairing `ConditionValueRelationMismatch` (asserted); wrong source universe `PositionedSubjectPossibilityError` (observed); missing registry `EmpiricalQueryExecutionError` (observed). Same-process deterministic rebuild matches; cross-process persisted restore/serialization/cache cold start `NOT_RUN`. Old-version/shadow/revocation `NOT_RUN__NO_SELECTED_J_ISSUER_OR_VERSION`.

Probe SHA-256 `83a9724fc2d705a51afa36c6443fe853c2cbef9546a91dda28c25f00e587372f`; probe JSON `d061fa82fbce20c695c2e3a0a3ddaf17bd225729e466e2b536c364bc0d77e16b`; pytest log `9749135c41084e8173dbba868a950d160ec3c5551a45ff1fb5468ed9bb740241`.

### C2-2 — Named sourcefree tests (PASS)

```sh
PYTHONDONTWRITEBYTECODE=1 TMPDIR=... python3 -m pytest -q -p no:cacheprovider \
  --basetemp=.../tmp/pytest \
  rawlsing_next/tests/test_pre553_n9_n10w_progressive_candidate.py::test_full_progressive_chain_matches_hand_derived_oracle \
  rawlsing_next/tests/test_pre553_n9_n10w_progressive_candidate.py::test_unordered_conditioner_list_is_refused \
  rawlsing_next/tests/test_pre553_n9_n10w_progressive_candidate.py::test_false_pairing_value_is_refused \
  rawlsing_next/tests/test_pre553_n9_n10w_progressive_candidate.py::test_progressive_declares_no_rights_and_no_real_current
```

Result: `4 passed in 1.55s`. Independent review also ran 3 extra focused checks (`05_EXTRA_FOCUSED_TESTS.log`, 3 passed) and reproduced the probe byte-identically (`09_PROBE_DIFF.txt`). Source hashes: provider `99d71605...`, composition `2358cd26...`, consumer `9c041cb1...`, candidate/fixture `78f85aea...`.

## C3 — Field Forge / post-FF sourcefree court

### C3-1 — Primary selected court (21 passed)

```sh
OUT='WORKER_RETURNS/PROGRAMMA_PYAT_FUNCTION_AUTHORITY_SEVERANCE_AND_ADEQUACY_20261107_R1/C3_FF_POSTFF_CONSUMER'
TMPDIR="$OUT/tmp" PYTHONDONTWRITEBYTECODE=1 PYTEST_ADDOPTS='-p no:cacheprovider' \
python3 -m pytest -q \
  rawlsing_next/tests/test_gt12_closure_b_c_to_d_bridge.py::test_actual_c_relation_admits_without_reownership_and_is_lossless \
  rawlsing_next/tests/test_gt12_closure_b_c_to_d_bridge.py::test_c_observed_zero_blocker_cannot_be_laundered_to_admitted \
  rawlsing_next/tests/test_wave1_ff_prev3_relation_admission.py::test_positive_gt2_admission_is_exact_and_narrow \
  rawlsing_next/tests/test_wave1_ff_prev3_relation_admission.py::test_observed_zero_is_nonpositive_even_without_blocker_refs \
  rawlsing_next/tests/test_gt12_d_to_m4_typed_bridge.py::test_positive_relation_m1_derives_adopted_context_and_reaches_v558 \
  rawlsing_next/tests/test_gt12_d_to_m4_typed_bridge.py::test_typed_negative_or_nonpositive_input_cannot_translate_even_with_refs_stripped \
  rawlsing_next/tests/test_l01_evidence_world_consumer.py::test_signed_r08_evidence_reaches_actual_nonparent_numbers_and_world_routes \
  rawlsing_next/tests/test_l01_evidence_world_consumer.py::test_actual_request_mutation_refuses_and_restores \
  --basetemp="$OUT/tmp/pytest"
```

Result: `21 passed in 3.31s`, exit `0`.

### C3-2 — Additional negative/replay/authority tests (10 passed)

```sh
OUT='WORKER_RETURNS/PROGRAMMA_PYAT_FUNCTION_AUTHORITY_SEVERANCE_AND_ADEQUACY_20261107_R1/C3_FF_POSTFF_CONSUMER'
TMPDIR="$OUT/tmp" PYTHONDONTWRITEBYTECODE=1 PYTEST_ADDOPTS='-p no:cacheprovider' \
python3 -m pytest -q \
  rawlsing_next/tests/test_wave1_ff_prev3_relation_admission.py::test_deterministic_receipt_and_historical_replay \
  rawlsing_next/tests/test_wave1_ff_prev3_relation_admission.py::test_source_artifact_hash_tamper_is_integrity_failure \
  rawlsing_next/tests/test_gt12_closure_b_c_to_d_bridge.py::test_ref_hash_rule_source_and_risk_tamper_fail_closed \
  rawlsing_next/tests/test_gt12_d_to_m4_typed_bridge.py::test_wrong_source_dependency_risk_set_or_participant_order_cannot_reuse_authority \
  rawlsing_next/tests/test_gt12_d_to_m4_typed_bridge.py::test_actual_pre553_ref_authority_material_survives_d_to_e_losslessly \
  rawlsing_next/tests/test_l01_evidence_world_consumer.py::test_current_p41_receipt_owner_closes_historical_r53_failures \
  --basetemp="$OUT/tmp/pytest_neg"
```

Result: `10 passed in 2.04s`, exit `0`. **Total 31 passed, 0 failed.** Independent review corroborated 11/11 source blob/hash matches and a minimal two-node edge replay (10 tests); the full 31-test suite was not repeated.

C3 source identities (protected `7a5429`): `field_forge_conditional_support.py` `a70decb2...`; `wave1_ff_prev3_relation_admission.py` `c5fb675f...`; `gt12_c_to_d_relation_bridge.py` `ea04ec07...`; `gt12_d_to_m4_typed_bridge.py` `ca3d6b8d...`; `m1_admitted_field_forge_relation_v554_ingress.py` `0aeacd9e...`; `pre553_evidence_world_consumer.py` `75ff3b9a...`; `pre553_universal_world_binding.py` `fdda8b2f...`; `pre553_n9_n10w_progressive_candidate.py` `84d40414...`; `m4_v557_v558_publication_repository.py` `8ec5c8e1...`; `m5_runtime_rsc_peer_prior.py` `18735bdb...`; `m6_actor_safe_expression.py` `74d9701c...`. `git diff 7a5429..HEAD -- rawlsing_next` empty.

Mutation classes: Q86 exact role/order/source family/wave/artifact/risk/permission/context scope; zero/nonpositive/blocker/typed negative; source/risk/role tamper; deterministic replay; no laundering of observed zero; sourcefree R08/E41 source/permission/edition/clock/risk/zero-support mutation/restore; P41 R53 closure. **No production severance RED/restoration claim**; no selected non-test generic FF consumer.

## C4 — O14 J role/component mechanism

```sh
PYTHONDONTWRITEBYTECODE=1 TMPDIR=... python3 -m pytest -q -p no:cacheprovider \
  --basetemp=.../tmp/pytest2 \
  rawlsing_next/tests/test_pre553_j_role_certification.py::test_h08_two_relation_components_certify_without_historical_executor \
  rawlsing_next/tests/test_pre553_j_role_certification.py::test_h10_negative_role_authority_blocks_before_relation_promotion \
  rawlsing_next/tests/test_pre553_j_role_certification.py::test_h11_changed_role_authority_blocks_and_changes_binding_identity \
  rawlsing_next/tests/test_pre553_j_role_certification.py::test_h12_missing_successor_mapping_remains_unresolved_no_target_fallback \
  rawlsing_next/tests/test_pre553_j_role_certification.py::test_h14_component_set_order_mismatch_is_integrity_failure \
  rawlsing_next/tests/test_pre553_j_role_certification.py::test_h15_serialized_role_vector_replay_mismatch_is_integrity_failure \
  rawlsing_next/tests/test_pre553_j_role_certification.py::test_exact_current_selection_authority_mismatch_rejected_by_registration
```

Result: `7 passed in 2.23s` (independent review `7 passed in 2.69s`). Positive h08; negatives h10/h11/h12/h14/h15/selection-authority mismatch. Source hashes: `pre553_j_role_certification.py` `838e123c...`; `pre553_component_authority_vector.py` `9cbe0200...`; `pre553_learned_empirical_adjudication.py` `40ce648e...`; historical six `9ba` pins match. `NONE_FOUND_IN_STATIC_SOURCE` for non-test invocation/call-through; exact `build_j_validator_registry` → `M1ValidatorRegistry` exists. Selected original J release/row, historical first-reader execution, old-version/shadow/revocation: `NOT_RUN__NO_SELECTED_J_RELEASE`.

## C5 — Shared source-estate producer/consumer

C5 did **not** run a new test; it reused P6 evidence. P6 commands (reused, not rerun):

```sh
PYTHONPATH=. python3 .r61/r157-p6/audit_coverage.py
# -> physical_slots=18413; items=18276; unique=18276; unmatched=26

PYTHONPATH=. python3 -u .r61/r157-p6/native_replay.py
# -> 35 sources; 35 release hashes match index; 0 construction mismatches

PYTHONPATH=. python3 -m pytest \
  rawlsing_next/tests/test_source_configuration_library.py \
  rawlsing_next/tests/test_source_configuration_p3.py \
  rawlsing_next/tests/test_source_configuration_foundation.py \
  -q -o addopts=''
# -> 34 passed in 148.50s

PYTHONPATH=<candidate> python3 -m rawlsing_next.source_configuration.cli \
  --index <temp>/index.json build-index --sqlite <temp>/index.sqlite
# -> available=35; JSON sha256 = be69b414f0c03ffc70e0888137c4bde5a8114a3890011f7e1a40ebdbf83770f6
```

C5 hashes: `P6_REVIEW.md` `92853315...`; `SOURCE_LIBRARY_INDEX.json` `be69b414...`; `SOURCE_ROSTER.json` `a0201dbd...`; `factory.py` `3848b5ee...`; `library.py` `a12f4441...`; `reader.py` `e22b05f7...`; `schema.py` `0b30669b...`; `READINESS_MATRIX.json` `6271929f...`. Current C11 owners: `pre553_source_backed_c11_facade.py` `7788feb5...`; `pre553_c11_ingest.py` `0c56a0f6...`; `pre553_source_local_universe_admission.py` `377b4d76...`; `pre553_empirical_query.py` `7cd7fd4f...`; `pre553_source_native_preimage_adapter.py` `e99dd211...`; `pre553_c11_integrity.py` `3963face...`. Protected/base `rawlsing_next/source_configuration`: 0 paths. C5 outputs: `01_CASES` `08b680f3...`; `02_CASES` `d7207e84...`; `04_MINIMAL_OWNER_ACTIONS` `8e37f046...`; `05_REGISTER_ANTIJOIN` `8c5208d9...`; `06_ALL35_SOURCE_DISPOSITIONS` `2c405095...`; build log `436c6fc1...`; reporting validation `22669ca1...`. 35/35 fixture releases; 18,413 slots; 18,276 items; 18,250 joins; 26 unmatched; 1,653 held slots; 24 `NOT_RUN` + 11 `FIXTURE_ONLY`; original execution `NOT_RUN`.

## C6 — Historical selected-use closure

C6 ran **no test suite**; it ran deterministic read/join/build checks only. Exact commands:

```sh
cd /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat777-joint-consumer
git -C /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat777-joint-consumer rev-parse HEAD
git -C /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat777-joint-consumer \
  show 0c5b385d:WORKER_RETURNS/PROGRAMMA-PYAT-AUTHORITY-RECLOSURE-20261106-R1/MAINMAC_COMPOUND_RECLOSURE/R4_HISTORICAL_VERSION/01_ALL_58_HISTORICAL_RELEASE_LEDGER.tsv
git -C /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat777-joint-consumer \
  show 6f8da13c2734ba1b5e83ff0de6c0ab1aefe3cf95:WORKER_RETURNS/PROGRAMMA-PYAT-AUTHORITY-RECLOSURE-20261106-R1/F1_BROWSER_FUNCTION_CROSSWALK/02_LEGACY_FUNCTION_AND_AUTHORITY_MATRIX.csv
git -C /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat777-joint-consumer \
  show 6f8da13c2734ba1b5e83ff0de6c0ab1aefe3cf95:WORKER_RETURNS/PROGRAMMA-PYAT-AUTHORITY-RECLOSURE-20261106-R1/F1_BROWSER_FUNCTION_CROSSWALK/01_LEGACY_AUTHORITY_CALLSITES.csv
git -C /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat777-joint-consumer \
  show 5296ede23c667a6ab044dfb92a15e29205c6fd11:WORKER_RETURNS/PROGRAMMA-PYAT-AUTHORITY-RECLOSURE-20261106-R1/MAINMAC_COMPOUND_RECLOSURE/R1_ORIGINAL_CALL_RECLOSURE/01_R1_ORIGINAL_CALLSITES.tsv
python3 WORKER_RETURNS/PROGRAMMA_PYAT_FUNCTION_AUTHORITY_SEVERANCE_AND_ADEQUACY_20261107_R1/C6_HISTORICAL_SELECTED_USE/scripts/build_c6_selected_use.py
```

Retained denominators asserted before writing: `F1_29=29`, `F1_228=228`, `R1_581=581`, `JOINED_687=687`, `RELEASE_58=58`.

Source/retained hashes: `P1_SOURCE_REGISTER_ROWS.jsonl` `3d01719c...`; `P1_HISTORICAL_ESTATE_AND_CALLSITE_ROWS.jsonl` `33c1b0d1...`; R4 58-row ledger `8fbe5288...`; F1 matrix `103a4018...`; F1 callsites `0f622426...`; R1 exact callsites `4906bef5...`.

Final C6 output hashes (correction cut `0d548b03`): `01_HISTORICAL_SELECTED_USE_CASES.jsonl` `252449d0...`; `02_LEGACY_AUTHORITY_CALLSITE_COVERAGE.tsv` `214b19f4...`; `03_AUTHORITY_RELEASE_USAGE.tsv` `74d3fe19...`; `04_UNPROVED_SELECTIONS_AND_MINIMUM_EVIDENCE.tsv` `77087d57...`; builder `0e51144b...`; `06_REPORTING_CORRECTIONS.md` `8883853e...`. The reviewed author cut `a34c1bf` had `9ed1839a...` / `5d5a41dd...` / `7c6a2905...` / `6f076ec3...`; the review verified those and the corrections changed only reporting/grades.

C6 counts: 29 functions; 58 releases; 42 selected-state / 16 unresolved; 38 single-file/row SHA + 4 `SET:` digests; 15 functions with selected state; 8 static F1 edge; 7 selected-only; 10 no callsite; 3 neither; 228 F1 callsites; 581 R1 rows (180 linked + 401 outside; all `RUNTIME_EXECUTED=NO`); 687 joined rows (680 linked + 7 outside F30; one F30 tool-reader row, not six-stage); 50 gaps. **No pytest log is claimed; no actual historical invocation was observed.**

## Mutation ledger (reused, not rerun)

| Lane | Mutation classes | Result |
|---|---|---|
| C1 Q86 | wrong source SHA; wrong QIMPL; wrong source-structure/wave grain; wrong common risk-set count; wrong target-use operation; widened GT1 permission ceiling; generic T01 wrong-kind/operation/scope | 6/6 typed refusals + restoration `true`; T01 ALLOW `SUPPORTED 2/2` RED; baseline `SUPPORTED 3/3` restored |
| C2 O11 | wrong conditioner order; false pairing; wrong source universe; missing authority registry; same-process rebuild | two asserted typed refusals; two observed typed refusals; rebuild matches; persisted restore `NOT_RUN` |
| C3 Q86/P41 | observed zero; nonpositive/blocker; source/risk/role tamper; replay; permission closure; R08/E41 source/edition/permission/clock/risk/zero-support | 31/31 pass; typed refusals; restore; no production severance claim |
| C4 O14 | h10 negative role; h11 changed role authority; h12 missing successor mapping; h14 component-set/order; h15 serialized replay; selection-authority mismatch | 7/7 pass; exact registry dispatch; no selected J release |
| C5 R157 | fixture/nonrespondent; 26 unmatched; 1,653 held slots; 11 fixture-only + 24 NOT_RUN | 35/35 fixture releases; 34 focused tests; original execution `NOT_RUN` |
| C6 historical | none executed; selected/static/unresolved/negative evidence accounting | no test suite; no invocation; `NOT_RUN` |

## Explicit NOT_RUN (do not convert to green)

- Original respondent / SAV / DTA / DB read: `NOT_RUN`.
- Native S3 / original35 issuance / science / actor: `NOT_RUN`.
- Actual historical six-stage invocation or run manifest for the 29/58: `NOT_RUN`.
- Selected Q86 version/shadow/withdrawal/cold restore at the actual selected row: `NOT_RUN`.
- Cross-process persisted restore/serialization/cache cold start: `NOT_RUN`.
- C2/C4 old-version/shadow/revocation: `NOT_RUN__NO_SELECTED_J_ISSUER_OR_VERSION` / `NOT_RUN__NO_SELECTED_J_RELEASE`.
- C5 original source execution / source_configuration execution: `NOT_RUN`.
- C6 pytest or native execution: `NOT_RUN`; no pytest log claimed.
- Any new test, new probe, code patch, production/existing-test/HQ/peer/protected write: `NOT_RUN` by this lease.
- CI waiver: **none fabricated.** FIABC 144 pass / 3 fail and R09 provenance remain as previously recorded.

## C9–C13 — reused real local receipts (no rerun by this fan-in)

The C14 combined return did **not** execute any test, probe, replay or source code. The following are reused from the exact C9–C13 returns and independent reviews at their stated cuts. They are S0/S1 documentary plus reused S2 sourcefree/test-time evidence.

### C9 — workload-plan/query-target-use → I03 first consumer

- **Author:** `396bfee9cca0275d040597828848ede4a7da80a7`; P1 boundary author `d540cfcc44359f8f78aceccf8afb247c4a7ad80d`; C9R correction `02a13a5e01880835434b30d9a3587147f9dab0de`; independent review `05a750ad6bcab8124c1f5d86b8867181fa4ee92c` reviewed target `d540cfcc` and returned `REVISE_SCOPED`; C9R-01/C9R-02 were reconciled in `02a13a5e`, which received HQ scoped acceptance after correction with **no independent re-review**. Do not present `05a750ad` as the review of `02a13a5e`.
- **Sourcefree API witness:** `compile_universal_workload:143` → `build_test_only_workload:299` → `execute_universal_workload:229` → `execute_test_only_workload:423` → `admit:219` → `execute_issued_workload:280` → `CarrierNeutralResearchExecutor.execute_i03:430` → `execute_empirical_query:685`.
- **Observed:** 4/4 compiled/executed operations; 4 SUPPORTED RAW facts; 4 receipts; no-drop 4/4; authority `B49-TEST-ONLY-QUERY-AUTH`; scope `TEST_ONLY_SOURCEFREE`; `target_use_permission_ids=[]`; denominators 3/3, 3/3, 4/4, 2/2.
- **Negative/restore:** wrong source SHA → 0/4 executed, 4 failed, no-drop false; wrong host/purpose → typed `WorkloadAdmissionError: SOURCE_HOST_PURPOSE_MISMATCH`; restoration fact refs match positive.
- **P1 boundary:** 840 ATLAS candidate operations/units admitted by current `BatchManifest`; direct `BatchExecutionRunner(manifest=..., repository=C11Repository())` refused at synthetic `C11LogicalRelease release25` — **expected as-built negative, not missing engine**. Existing PDEV01-GAP007 at `d3d6e48791623478fd1d838c7e95a72b77b5cd74` already binds 210 DIST operations to 210 current I03 queries/predicates and 210 Batch units: 210/210 COMPLETED, 210 SUPPORTED; 630 non-DIST typed `P1_OPERATION_KIND_HAS_NO_EXACT_CURRENT_I03_BINDING`; I05 16 receipts/30 facts/16 candidates; receipt SHA-256 `bba0de8231ea50b46c1f5d5f73c434d64af2d9bcd9c5ef610876e7955b1256ab`.
- **Limits:** sourcefree/test-only; no actual shared35 selected input, original35 execution, native/S3/science/actor effect, or production acceptance; 840 synthetic ATLAS operations are not original35; 630 typed refusals are not 630 missing capabilities.

### C10 — Q3/F03 historical first-consumer replay

- **Author:** `fdda847507936f5e2cd32cf8c57326f0f65200d6`; trace SHA-256 `53c2b4ed0ae775682f4ae7b7cd477868d6dc9dadd4d70bf802ce45670cb97184`; independent review `ac8f10220dfbc489cd2d261d1d66e228f2bc2424` (`REVISE_SCOPED`; C10R-01/02/03).
- **Pins:** AR-0005 `0f7fa1c0...` 47,874,248 bytes/18,518 rows; AR-0006 `a91239a5...` 1,119,028 bytes/700 rows; historical module `2fb0851d...` 38,858 bytes; historical source `9ba4764bef551b1ce498e5772d60b73d69337d4b`.
- **Observed:** full audit 18,518 rows; 35 active waves; 9 positive family witnesses with hashes; explicit block/ambiguous/missing-row/limited-registry/missing-file/cold-restore negatives; AR-0006 20-row residual.
- **Limits:** test-time replay only; **original historical run `NOT_OBSERVED`**; downstream V550 bridge/V551 atoms `NOT_RUN`; nine rows are not all35; current selection/equivalence `UNPROVED`; no positive severance finding.

### C11 — Q3/F08 historical first-consumer replay

- **Author:** `76392135cea16afc0ff07da97843837bd33fc9b7`; independent review `b939c51a21359efc556c3f58860789e247b011aa` (`REVISE_SCOPED`; C11R-01 Q4 wording corrected by HQ).
- **Pins:** AR-0047 `866eb3ab...` 11,059 bytes/35 rows; AR-0048 `29e7706b...` 1,702 bytes/7 rows; AR-0049 `15f7b561...` 26,582,348 bytes/18,792 rows; AR-0050 `3612c6b4...` 3,487 bytes/8 question types; QUC module `254542f9...` 115,511 bytes; historical source `9ba4764...`.
- **Observed:** selected GSS/1973/`uswar` row; `manual_override_used=true`; `semantic_role=RELATION_EVIDENCE`; `review_required=true`; `allowed_as_v551_relation_evidence=false`; contract hash `6c94c7a8...`; positive output `1c78a386...`; missing override/duplicate/missing register/missing itinerary negatives; restore equals positive.
- **Limits:** one selected nonrespondent authority row; test-time replay only; **original historical run `NOT_RUN`**; AR-0050 is register-builder metadata only, not QUC runtime effect; one row does not prove all35; current QUC succession `UNPROVED`.

### C12/C13 — functional-responsibility maps

- **C12 F08:** `71c40ba0325cb841c5ea3f45522b1ce72d5deff8`; `RESPONSIBILITY_MAP.jsonl` SHA-256 `5067649bbd16a2c95426ae88e112c56da2667029071b53cfc0a48bb8991675a1`; 6 rows; five QUC obligations compared; no QUC-equivalent producer→selector→consumer; current selection `UNPROVED`; no repair/new reader.
- **C13 F03:** `87390f002c3d122b958031087a77f7f7575931fc`; `RESPONSIBILITY_MAP.jsonl` SHA-256 `66e7ee95f2d6d02a27d08b238319d0a9ba460129cf8b65bae7cfb34ef4db9ed2`; 5 rows; generic C11/authority/query and bounded WVS7 routing pin present; full F03 selected operation/adapter `UNPROVED`; `F03=UNPROVED_CURRENT_SELECTION`; no new engine/adapter.

### C9–C13 explicit NOT_RUN

- Original historical run for C10/C11: `NOT_OBSERVED` / `NOT_RUN`.
- Actual selected shared35 source/wave + C11 release + I03 query/predicate: `NOT_RUN__UNPROVED_SELECTION`.
- Actual selected current F03 operation: `NONE_PROVED`.
- Actual selected current QUC operation: `NONE_PROVED`.
- Original issuer / native / S3 / science / actor: `NOT_RUN`.
- No new test, replay, probe, source read, source_configuration execution, production patch, protected/peer/HQ write, or worker dispatch in C14.
