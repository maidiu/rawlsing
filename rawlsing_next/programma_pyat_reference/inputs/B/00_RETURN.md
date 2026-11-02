# PROGRAMMA PYAT PREP W1-B — current and pending code realization return

**Status:** `CURRENT_PREMAIN_CODE_CROSSWALK__TARGETED_SOURCEFREE_TESTS_PASS__NO_NATIVE_OR_OWNER_ADOPTION`
**Whole scope:** `PARTIAL__193_OF_214_PREMAIN_TEST_FILES_UNSAMPLED`
**Role:** independent current/PREMAIN/pending implementation and consumer forensic
investigator; not Pyat HQ, code author or own reviewer.

## Identity and currentness

| Item | Exact value |
|---|---|
| Assigned branch | `research/programma-pyat-w1-b-current-code-realization-20261101-r1` |
| Exact startup SHA in launch | `acbe2326c8f52dfe8bfa200e87c5c07a62a5c93a` |
| Observed remote branch head | `4c1513eaf33c8af333b82ccaeace8452c41e3380` |
| Difference | R2 environment/model routing commission only; no prior W1-B return found |
| Canonical PRE-MAIN at launch | `9809203fd915a84bae056a67210e9213879840db` |
| Live PRE-MAIN recheck | same `9809203...`; no changed head observed |
| Current main | `25830fe7462bb9e29bc4087e6ae14f3f84cec377` |
| R157 pending cut | `d81bc2c67baf933461ae6cfca468f24779cc7e44` |
| PROGRAMMA P1 pending cut | `d1278613e9e1a5d986ccce15782a697f19cbd722` |

The branch advanced only to the R2 launch/routing document. No existing W1-B
return or integration was found; this work is not a duplicate of another return.

## Model/harness observed

- Harness: OpenCode local S2 worktree, Python 3.11, Git/PyTest/subprocess.
- Model observed from the session runtime: `opencode-go/deepseek-v4.1-flash`.
- Effort requested: MAX. The harness did not expose independent effort telemetry;
  no model/provider/account change was made.
- No other agent, reviewer, controller or paid model call was launched.

## Method and search scope

- Verified the assigned branch and live PRE-MAIN; created an isolated sparse
  worktree at the observed R2 branch head.
- Read the shared W1 common contract, PROGRAMMA PYAT constitution, Astra
  PYAT atlas PROGRAM/DEPENDENCY_DAG/FUNCTIONS/IMPLEMENTATION_MAP/ACCEPTANCE,
  F1–F8 gates, N0–N13 dossiers, Whole-Machine G/S/P/Q/L/F/T/W/A register and
  RRIF finite closeout.
- Parsed all **350 PRE-MAIN `rawlsing_next/*.py` files** with a Python AST import
  graph; distinguished module importers, symbol call sites and test-only
  consumers. Direct-read selected implementation/test files; did not read every
  line of every module.
- Ran **526 targeted sourcefree tests in 21 PRE-MAIN test files, all PASS**:
  route_b 11, batch 16, C11 ingest 16, source façade 10, I03 32, I05 14,
  parity 20, Field Forge 11, M1 27, M2 28, M1 FF ingress 14, M2 release 28,
  B5 39, I4 30, learned adjudication 27, N10E 43, N9/N10W candidate 18,
  positioned possibility 13, analytical composition 13, analytical state-route 92,
  source relations 24.
- **193 of 214 PRE-MAIN test files were not sampled.** Main tests were **NOT_RUN**;
  main rows are source-read only. No original source/respondent/native execution.

### Test receipt matrix (command exit 0 for every row)

Command prefix used in the isolated PRE-MAIN worktree:

```sh
python3 -m pytest -o addopts= -q -p no:cacheprovider <file...>
```

| Test file | Collected/executed | Result |
|---|---:|---|
| `test_pre553_route_b_production.py` | 11 | PASS |
| `test_pre553_batch_runner.py` | 16 | PASS |
| `test_pre553_c11_repository_ingest.py` | 16 | PASS |
| `test_pre553_source_backed_c11_facade.py` | 10 | PASS |
| `test_pre553_empirical_query.py` | 32 | PASS |
| `test_pre553_discovery_exact.py` | 14 | PASS |
| `test_pre553_independent_parity_oracle.py` | 20 | PASS |
| `test_field_forge_conditional_support.py` | 11 | PASS |
| `test_m1_temporal_v554_admission_dedup.py` | 27 | PASS |
| `test_m2_v555_atomic_route.py` | 28 | PASS |
| `test_m1_admitted_field_forge_relation_v554_ingress.py` | 14 | PASS |
| `test_pre553_learned_product_release.py` | 28 | PASS |
| `test_pre553_learned_product_lifecycle.py` | 39 | PASS |
| `test_pre553_learned_world_composition.py` | 30 | PASS |
| `test_pre553_learned_empirical_adjudication.py` | 27 | PASS |
| `test_pre553_empirical_possibility_provider.py` | 43 | PASS |
| `test_pre553_n9_n10w_progressive_candidate.py` | 18 | PASS |
| `test_source_backed_positioned_subject_possibility.py` | 13 | PASS |
| `test_pre553_analytical_composition.py` | 13 | PASS |
| `test_pre553_analytical_state_and_route.py` | 92 | PASS |
| `test_pre553_source_relations.py` | 24 | PASS |

## Current realization summary

| Requirement | Best current code | Exact PRE-MAIN blob | First consumer | Status |
|---|---|---|---|---|
| F1 C11 ingest | `pre553_c11_ingest.validate_c11_source_release` | `37cd35fa...` | façade line 603 | CURRENT_SOURCEFREE |
| F1 C11 façade | `pre553_source_backed_c11_facade.build_source_backed_c11_repository` | `8a761119...` | Route B | CURRENT_SOURCEFREE |
| F1 D01/D02 | `pre553_physical_decoder.decode_sav/decode_dta` | `4b89c459...` | physical→C11 facade | C3/E4FR reviewed |
| F1 I03 | `pre553_empirical_query.execute_empirical_query` | `03facecf...` | façade line 659 | CURRENT_SOURCEFREE |
| F1 I05 | `pre553_discovery_exact.execute_exact_bounded_discovery` | `905f24d1...` | carrier line 456 | CURRENT_SOURCEFREE |
| P07 Batch | `pre553_batch_runner.BatchExecutionRunner` | `2d291600...` | issued workload line 331 | CURRENT_SOURCEFREE |
| P06 Route B | `pre553_route_b_production.execute_route_b_production` | `2385cd32...` | issued workload line 300 | CURRENT_SOURCEFREE |
| F2–F4 analytical | `pre553_analytical_composition.compose_positioned_subject_possibility` | `604c8d59...` | N10E provider line 574 | CURRENT_SOURCEFREE |
| F2–F4 state-route | `pre553_analytical_state_and_route.build_state_route_result` | `3a5e3db8...` | tests only | TEST_ONLY |
| F2–F4 possibility | `source_backed_positioned_subject_possibility.evaluate_positioned_subject_possibility` | `62e5eced...` | analytical composition | CURRENT_SOURCEFREE |
| F5 Field Forge | `field_forge_conditional_support.produce_exact_conditional_support_profile` | `a70decb2...` | GT12 bridge (test only) | TEST/BRIDGE ONLY |
| F5 FF M1 ingress | `m1_admitted_field_forge_relation_v554_ingress.evaluate_m1_admitted_field_forge_relation_v554` | `0aeacd9e...` | GT12 D→M4 (test only) | TEST/BRIDGE ONLY |
| M1 temporal | `m1_temporal_v554_admission_dedup.evaluate_m1_temporal_v554_admission_dedup` | `e8bd6376...` | reservoir harness/tests | TEST/HARNESS ONLY |
| M2 atomic | `m2_v555_atomic_route.evaluate_m2_v555_atomic_route` | `deef8a60...` | reservoir harness/tests | TEST/HARNESS ONLY |
| M2 release | `pre553_learned_product_release.constitute_release/resolve_release_exact` | `1cb76923...` | B5 lifecycle | PR #605/E6 |
| B5 lifecycle | `pre553_learned_product_lifecycle.LearnedProductLifecycleExecutor` | `dadf2362...` | I4 composition | PR #605/E6 |
| I4 learned world | `pre553_learned_world_composition.compose_learned_world` | `4a8e27a2...` | tests only | TEST_ONLY |
| N10E provider | `pre553_empirical_possibility_provider.provide_empirical_possibility_slice` | `23167aa2...` | progressive candidate line 327 | CANDIDATE CONSUMER |
| N9/N10W | candidate only; module says not implemented | `84d40414...` | tests only | NO N9/N10W CODE |
| N11/N12 | atlas dossier only | `f4f600a9...` / `ac83e3ad...` | none | NO CODE |
| F6 source relations | `pre553_source_relations.SourceRelationResolver` | `5b67e3f9...` | tests only | TEST_ONLY |
| F7 temporal | temporal gate/as-of pieces only | `e8bd6376...` / `dadf2362...` | tests only | NO N8E/N8S PRODUCER |
| R157 configs | 119 paths at `d81bc2c...` | `41e5afbf...` | none at PRE-MAIN | PENDING/UNINTEGRATED |
| P1 constructor | `programma_pyat_original35_constructor.construct_original35_epre` | `c8352c5a...` at `d1278613...` | BatchManifest | PENDING/AUTHOR TESTED |

## Merged/reviewed evidence actually reused

- **C3 PR #602** merged at `0075c15fdfb1ca7dea3c5cb54ace3652e0201441`;
  E4FR independently accepted `7cd2206fd976606d3816589e2fce03c03c827f39`;
  45 PASS and selected 194 PASS/1 SKIP. Physical SHA/encoding declaration is not
  source-use authority.
- **B5/M2 PR #605** merged at `fe3f5b4714b11015813537407f7eb4bbb6bc2c10`;
  E6 independently tested `b0f7675bf4f434bc8964c9b3ebc8392bb33d56fb`;
  175 sourcefree modern tests PASS. M2 `LOCAL_UNAUTHENTICATED` remains its ceiling.
- **R157** P6 accepted preparation at `d81bc2c...`; integration `1924499...`;
  119 paths, **0/119 current same-path at PRE-MAIN**, 19 RRIF-C code paths absent.
- **PROGRAMMA P1** at `d1278613...` is author-tested only; 18 constructor + 16
  batch tests reported, not independently reviewed, absent from PRE-MAIN.

## Exact consumer traversals

1. Physical decoder → C11 façade/ingest → Route B → issued workload → Batch → I03/I05.
   Reverse reaches the decoder. Missing: real source pack, production consumer.
2. C11 → I03/I05 → analytical composition → N10E provider → N9/N10W candidate.
   Reverse reaches C11. Missing: N9/N10W, selected world, production consumer.
3. I03 joint fact → Field Forge → GT12 C→D bridge → M1/M2 → M4/M5 publication.
   Reverse reaches Field Forge. Missing: non-test consumer for Field Forge/bridge.
4. F6 source relations and F7 temporal pieces → N9/N10W → N11/N12 dossiers.
   Reverse stops at missing N9/N10W and N8E/N8S. Missing: composed fields,
   comparable-wave producer, whole-world acceptance and wake decision.

Detailed source/ref/blob paths and `MISSING` stops are in
`EXACT_CONSUMER_TRAVERSALS.md`.

## Key gaps

- No production caller for M1/M2, I4, Field Forge, F6 source relations or
  analytical state-route; they are test/harness/bridge-only at this cut.
- N9/N10W/N11/N12 have no executable code; N10W requires N9 + N10E.
- F7 has no N8E comparable-wave or N8S structural-temporal producer.
- N10E provider terminates in a test-only progressive candidate.
- R157 configuration preparation is not integrated and is not U/E_pre.
- P1 constructor is not integrated, not independently reviewed and has no real
  source pack or C11/I03/I05 receiver.
- Main is an older baseline lacking Route B, analytical composition, learned
  release/lifecycle/world, N10E provider and P1/R157.

## Three verdicts

**ENGINEERING — current sourcefree realization is substantial but consumer-limited.**
C11/I03/I05/Route B/Batch, M2 release/B5, N10E provider and possibility primitives
exist and 526 targeted tests pass. M1/M2/Field Forge/I4/F6/analytical state-route
lack a production caller. This is author-executed sourcefree evidence, not
independent acceptance of this return.

**SCIENTIFIC — no new empirical or native claim.** The code preserves exact
source identities, negative states and non-pooling guards, but no original source
product, F1–F8 measured world, N11 acceptance or N12 wake decision is issued.

**AUTHORITY — no adoption or source right.** C3 and B5/M2 are at their exact
merged/reviewed sourcefree scopes. R157/P1 remain pending/unintegrated. No
original source, native N11/N12, actor/Sorok, production or PRE-MAIN write is
claimed.

## Next integrator step

Recheck live PRE-MAIN, then bind one exact authorized original35 source pack to
the existing C11/I03/I05 → Route B/Batch chain and produce one measured product
with its first consumer. Do not add another synthetic manifest, and do not promote
R157/P1 or the test-only M1/M2/Field Forge/I4/F6 paths before their named consumers
and owners exist.

## Final identity

Implementation return commit and final remote SHA are reported by the terminal
push readback; a file cannot contain the SHA of the commit that contains it.
