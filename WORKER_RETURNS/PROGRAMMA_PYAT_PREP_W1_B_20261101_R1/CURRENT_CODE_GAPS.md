# CURRENT_CODE_GAPS — present/PREMAIN/pending Pyat realization

**Scope:** current `main` at `25830fe7462bb9e29bc4087e6ae14f3f84cec377`;
live PRE-MAIN at `9809203fd915a84bae056a67210e9213879840db`; pending
`R157@d81bc2c67baf933461ae6cfca468f24779cc7e44` and
`PROGRAMMA_P1@d1278613e9e1a5d986ccce15782a697f19cbd722`.

**Method:** authenticated Git tree/source read; Python AST import graph over all
350 PRE-MAIN `rawlsing_next/*.py` files; direct reads of selected owners/tests;
526 targeted sourcefree tests run in 21 files, all PASS. This is not whole-repo
exhaustiveness; 193 of 214 PRE-MAIN test files were unsampled. See
`CURRENT_REALIZATION.jsonl` for exact path/symbol/ref/blob rows.

## 1. Strong current sourcefree realization exists

| Requirement | Best current implementation | Exact PRE-MAIN blob | Observed consumer | Test receipt |
|---|---|---|---|---|
| C11 ingest | `pre553_c11_ingest.validate_c11_source_release` | `37cd35fa2e3420a3eea272a2902e96ab9ba38aba` | `pre553_source_backed_c11_facade` line 603 | 16 PASS |
| C11 facade | `pre553_source_backed_c11_facade.build_source_backed_c11_repository` | `8a761119e4a8d68eb291fc4edfadb52e027f8284` | Route B / issued workload | 10 PASS |
| D01/D02 decoder | `pre553_physical_decoder.decode_sav/decode_dta` + `pre553_r5_codec` | `4b89c4598f324834de064c1200c63698a20e3c5c` | physical → C11 facade | 45 PASS / selected 194 PASS / 1 SKIP (C3/E4FR) |
| I03 query | `pre553_empirical_query.execute_empirical_query` | `03facecf70890bfd13b80418620d274cbcd69d02` | facade line 659; analytical composition line 1038 | 32 PASS |
| I05 discovery | `pre553_discovery_exact.execute_exact_bounded_discovery` | `905f24d114419dbdd93879ad2bee5b59dd2f23af` | carrier execution line 456; recursive handoff line 528 | 14 + 20 PASS |
| Batch | `pre553_batch_runner.BatchExecutionRunner` | `2d291600b9a10c56d9c6f6de7f7d619f6c52e829` | issued workload line 331; native binding line 1074 | 16 PASS |
| Route B | `pre553_route_b_production.execute_route_b_production` | `2385cd327dced3c5b887b59085aa0d21b04d78c3` | issued workload line 300 | 11 PASS |
| Analytical composition | `pre553_analytical_composition.compose_positioned_subject_possibility` | `604c8d591d4cc2b646e9b149cdb233fc9d69cf6b` | N10E provider line 574 | 13 PASS |
| Possibility service | `source_backed_positioned_subject_possibility.evaluate_positioned_subject_possibility` | `62e5eced47b64512f47b004e3e13a6ef3fe21de7` | analytical composition | 13 PASS |
| M2 release | `pre553_learned_product_release.constitute_release/resolve_release_exact` | `1cb7692399aad8fb272c8c9ce956719527829007` | B5 lifecycle | 28 PASS; PR #605/E6 |
| B5 lifecycle | `pre553_learned_product_lifecycle.LearnedProductLifecycleExecutor` | `dadf2362f3195c28ebaf97655e28cdba72c04fb3` | I4 composition | 39 PASS; PR #605/E6 |
| N10E provider | `pre553_empirical_possibility_provider.provide_empirical_possibility_slice` | `23167aa25291fb148b1e3cf210ac33fe7769b783` | progressive candidate line 327 | 43 PASS |

## 2. Critical consumer gaps

### G1 — M1/M2 have no production caller
`m1_temporal_v554_admission_dedup.evaluate_m1_temporal_v554_admission_dedup` and
`m2_v555_atomic_route.evaluate_m2_v555_atomic_route` are present and pass 27/28
tests, but the only non-definition call sites are `tests/pre553_reservoir_harness.py`
and test files. No current Route B, analytical, I4 or world-serving module calls
the exact evaluators. **Status: TEST/HARNESS ONLY.**

### G2 — Field Forge and GT12 C→D bridge have no production caller
`field_forge_conditional_support.produce_exact_conditional_support_profile`
(`a70decb...`) is imported by `gt12_c_to_d_relation_bridge`, but that bridge is
imported only by `tests/test_gt12_e2b_actual_object_consumer_harness.py`.
`m1_admitted_field_forge_relation_v554_ingress` is consumed by
`gt12_d_to_m4_typed_bridge`/`m4_m1_evaluation_binding`, whose own callers are
tests. **Status: TEST/BRIDGE ONLY; no F5 positive objective consumer proved.**

### G3 — I4 learned-world composition is test-only
`pre553_learned_world_composition.compose_learned_world`
(`4a8e27a2...`) imports M1/M2/B5, but no non-test module imports I4. Its 30 tests
pass. **Status: TEST ONLY; no production I4 consumer.**

### G4 — N10E provider terminates in a test-only candidate
`provide_empirical_possibility_slice` is called by
`pre553_n9_n10w_progressive_candidate.run_single_conditioner_step` line 327.
That candidate is imported only by tests. The module explicitly states N9 and
N10W are not implemented. **Status: SOURCEFREE CANDIDATE ONLY.**

### G5 — N9/N10W/N11/N12 have no code
N9 and N10W are dossier/acceptance targets; N10W requires N9 + N10E. N11/N12 are
`PROPOSED_NOT_COMMISSIONED` atlas dossiers. No current executable acceptance
manifest or `prev3_v3_wake_decision.md` implementation was found.
**Status: NO_CODE / DOCUMENT_ONLY.**

### G6 — F6 multi-field composition is guard-only
`pre553_source_relations.SourceRelationResolver` / composite guards
(`5b67e3f9...`) pass 24 tests, but no non-test module imports
`pre553_source_relations`. F6 requires two eligible field contributions and an
actual composed world consumer; neither is proved. **Status: PARTIAL GUARD ONLY.**

### G7 — F7 has no comparable-wave/temporal producer
PRE-MAIN has temporal gating (`m1_temporal`) and as-of currentness
(`LearnedProductLifecycleExecutor.resolve_current_as_of`), but no N8E
comparable-wave empirical movement producer and no N8S structural temporal
pressure producer. The 27 M1 tests do not exercise cross-wave comparison.
**Status: PARTIAL PIECES / NO N8E/N8S CODE.**

### G8 — Analytical state-route owner is test-only
`pre553_analytical_state_and_route.build_state_route_result` has 92 tests and
preserves noncomparable/unknown states, but no non-test importer.
**Status: TEST ONLY.**

## 3. Pending/unintegrated candidates

### R157 — 119 historical source-configuration paths
Final-review tree `d81bc2c...` has 119 exact source-configuration/read-admission
paths; **0/119** are same-path present at PRE-MAIN; 19 are the RRIF-C introduced
code-path subset. P6 accepted the preparation at
`d81bc2c...`; integration `1924499...` remains historical preparation, not U/E_pre.
**First current PRE-MAIN consumer: NONE PROVED.** Do not transplant.

### PROGRAMMA P1 — sourcefree original35 constructor
Branch `d1278613...` adds `programma_pyat_original35_constructor.py` blob
`c8352c5a...`, 18 constructor tests + 16 batch tests (author-reported), producing
synthetic 35-wave/840-operation plans and typed HOLD/ABSTAIN. It is absent from
PRE-MAIN. First sourcefree receiver is `BatchManifest`/`BatchExecutionRunner`.
**No independent review; no source pack; no C11/I03/I05 execution; no U/E_pre
issuance.**

## 4. Main vs PRE-MAIN ABI/diff candidates

- Main `pre553_c11_ingest.py` blob `332d3d09...` differs from PRE-MAIN
  `37cd35fa...`; main `pre553_empirical_query.py` blob `d81e4ebe...` differs from
  PRE-MAIN `03facecf...`.
- Main `pre553_batch_runner.py` and `m1_temporal`/`m2_v555` binaries are same-path
  but main lacks Route B, issued workload/native binding, analytical composition,
  learned release/lifecycle/world, N10E provider and P1 constructor.
- PRE-MAIN `pre553_route_b_production.py`, `pre553_analytical_composition.py`,
  `pre553_analytical_state_and_route.py`, `field_forge_conditional_support.py`,
  `pre553_learned_product_release.py`, `pre553_learned_product_lifecycle.py`,
  `pre553_learned_world_composition.py`, `pre553_empirical_possibility_provider.py`
  and `pre553_n9_n10w_progressive_candidate.py` are absent from main.
- H125 atlas blobs are not uniformly current PRE-MAIN blobs. Treat H125 as a
  source-graded plan/identity reference, not a current binary manifest.

## 5. Test coverage and unsampled remainder

Executed 526 tests in 21 PRE-MAIN files, all PASS:

`route_b 11`, `batch 16`, `c11 ingest 16`, `source facade 10`, `I03 32`,
`I05 14`, `parity 20`, `field forge 11`, `M1 27`, `M2 28`, `M1 FF ingress 14`,
`M2 release 28`, `B5 39`, `I4 30`, `learned adjudication 27`, `N10E 43`,
`N9/N10W 18`, `possibility 13`, `analytical composition 13`, `state-route 92`,
`source relations 24`.

PRE-MAIN has 214 test files; **193 were not sampled**. Main tests were **NOT_RUN**;
main rows are source-read only. No native/original source execution.

## 6. Recheck / exact next integrator step

Recheck live PRE-MAIN before any fan-in; current observed head is
`9809203fd915a84bae056a67210e9213879840db`. The next integrator should:

1. Keep C3 and B5/M2 at their exact merged/reviewed scopes.
2. Bind one exact original35 source pack to C11/I03/I05 and prove the first
   measured product through the existing Route B/Batch chain, rather than adding
   another synthetic manifest.
3. Wire M1/M2/B5/I4 and Field Forge to a real current consumer before calling F3,
   F5, F6 or N9 mature.
4. Keep N9/N10W/N11/N12 and R157/P1 as absent/pending until their named owners
   produce code and acceptance evidence.
