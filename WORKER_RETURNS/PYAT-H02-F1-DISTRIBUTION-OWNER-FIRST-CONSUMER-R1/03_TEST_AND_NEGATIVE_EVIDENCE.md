# PYAT H02 — tests, negative evidence and direct consumer call

Observed FINDING: the retained GT2 lane is genuinely positive and the N10E analytical lane is executable only on its synthetic fixture; one pre-existing analytical test is RED. Causal INTERPRETATION: reuse the retained structural consumer; do not manufacture an analytical binding without owner authority. Proposed HQ ACTION: accept the retained positive at its grain and decide the analytical lane separately. Accountable OWNER: Pyat HQ and the original analytical/Field Forge owners.

## Environment and execution

Local macOS x86_64, Python 3.11.3, pytest 9.1.1, SQLite 3.40.1. All runs used `PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1`. Base and worker HEAD before the return commit: `299f41e97a43c67be9cc76a79fa49b48f4e12e54`. No source code was modified. Tests were inspected before execution; no arbitrary historical script was run.

## 1. Retained GT2 current-consumer court — PASS

```sh
python3 -m pytest rawlsing_next/tests/test_pre553_gt2_structural_positive_realization_court.py -q --junitxml=.../01_HQ222_GT2_COURT_40.xml
```

`40 passed` in 157.53s; failures 0, errors 0, skipped 0. JUnit SHA-256 `1079f32d1de3e7a781e3ebfa66d3aea5296c248acba7d0363a4ef0157eabeac3`.

Key executed witnesses: `test_retained_empirical_product_is_the_real_current_gt2_canary`; `test_complete_native_joint_domain_is_preserved_not_collapsed`; `test_minority_and_zero_geometry_survives_the_relation`; `test_current_authorized_v554_v558_consumer_consumes_the_real_product`; `test_v558_repository_preserves_exact_relation_lineage`; `test_source_materialization_is_never_opened`.

Hostile witnesses executed and passed: wrong Q86B/Q86A order; altered risk-set identity and row count; altered source family/wave/artifact; stale fact/query ref; incomplete joint domain; relation content-hash mismatch; permission widening; missing admission/relation authority; wrong target use; V554 equivalence mismatch; denied structural use; fabricated positive preparation; nonpositive upstream; causal/mechanism re-reading; actor injection; V3 actor promotion; V555 relation refusal. The V555 test returns `CONSTRUCTION_FAILURE__NOT_STRUCTURAL_NEGATIVE` with `M1 contract id mismatch`, and the adopted current lane forbids V555 as producer family.

## 2. N10E analytical producer/consumer — PASS on synthetic AT07

```sh
python3 -m pytest rawlsing_next/tests/test_pre553_empirical_possibility_provider.py -q --junitxml=.../02_N10E_PROVIDER_43.xml
```

`43 passed` in 18.68s; failures 0, errors 0, skipped 0. JUnit SHA-256 `1a7c8e9f74bef537a6e5e7cdc346a32baa643835a127505f4b8ed16b670ed78a`.

The frozen source-free oracle is a 100-row synthetic AT07 law: forward 54/60 = 9/10, reverse 54/62 = 27/31. The suite proves generated evidence identity, producer-derived geometry, direct consumer execution, deterministic replay, fresh-process replay and negatives for source/release mismatch, target-topology mismatch, foreign universe, non-supported/zero-support refusal, model source out of scope, precomputed-geometry exclusion and identity tamper. It does not consume the retained GT2 product.

## 3. Supporting analytical tests — 22 PASS, 1 pre-existing RED

```sh
python3 -m pytest rawlsing_next/tests/test_wave1_gt12_i03_positive_facts.py rawlsing_next/tests/test_wave1_gt12_a2_real_gt1.py rawlsing_next/tests/test_source_backed_positioned_subject_possibility.py -q --junitxml=.../03_ANALYTICAL_SUPPORT_23.xml
```

Result: `22 passed, 1 failed` in 0.65s. The failure output is preserved below; the supporting-run JUnit was not retained because it duplicates the failure trace already recorded here.

Failure: `test_wave1_gt12_a2_real_gt1.py::test_a2_claim_scoped_authorities_bind_actual_release_universe_and_replay` raises `GT12BI03BindingError: validated projection domain omits an observed exact source-native response state`. It reproduces alone at untouched `299f41e`, so it is not caused by this return. It is an analytical A2 fixture-route defect, not the retained GT2 consumer. No repair was attempted: the reused positive is unaffected and the single-repair budget was not spent on an unrelated lane.

## 4. Direct real-consumer call (not just pytest)

A one-off Python invocation (no new committed engine) performed:

1. `load_current_gt2_query_fact_from_committed_transport()` — no path argument; fixed committed transport.
2. `produce_exact_conditional_support_profile(...)` — retained-fact consumer and distribution producer; exact Q86B→Q86A order and `STRUCTURAL_MEDIATION_INPUT` ceiling.
3. `admit_gt12_c_relation` — first downstream consumer of the produced profile.
4. `run_current_r1c_e2b_actual_objects(query, fact)` twice — current V554/V557/V558 consumer.

Actual result: 6 conditioner rows × 6 target states = 36 joint cells; total support 19,210; 23 zero cells; real anchors `0|0=2112`, `0|1=4493`, `1|0=491`, `1|1=11232`, `DK|1=250`, `DK|DK=334`, `MISSING|1=9`, `MISSING|MISSING=6`. Relation object `urn:rawlsing:field-forge:conditional-support:sha256:1ffdfe53...`; admission `ADMITTED` for `STRUCTURAL_MEDIATION_INPUT`; M1 `ELIGIBLE`; V554 F1 `urn:rawlsing:v554:f1:sha256:3530f08f...`; V558 entry producer `V554`, allowed use `CONTEXT`, resolution `RESOLUTION_COMPLETE`; V3 `DENY_ZERO_EFFECT`. Replay equality held for relation hash, admission ref, F1 id and V558 resolution.

Raw receipt: `evidence/04_DIRECT_RETAINED_CONSUMER_RECEIPT.json`, SHA-256 `be18bfc7fc6623f0aba57ac9e1c8c8b21323b18914fc3edef49d00a8cd202279`.

## 5. Original-corpus non-use

The retained loader has no path/source parameter; `test_source_materialization_is_never_opened` passed. No SAV, respondent row, raw response value, original survey execution, source reopening or native semantic issuance occurred. The manifest records `sav=false`, `source_rows=false`, `raw_respondent_response_values=false`. The 19,210/36 geometry is genuinely consumed from the fixed committed transport, not re-derived from original respondents.

## 6. Files and limits

No implementation source was changed, so there is no new engine to review. The evidence JUnit/log files are under `evidence/`; tests and their oracles remain at their pinned PRE-MAIN blobs. The pre-existing A2 RED is preserved, not hidden. No self-review, adoption, PRE-MAIN mutation, merge or V555 relabel was performed.

DONE: 40/40 retained court, 43/43 analytical provider, direct retained consumer receipt, 22/23 supporting analytical with one preserved RED, original-corpus non-use. REMAINING: HQ decision on the analytical retained binding. CRITICAL BLOCKERS: analytical model/query authority and V555 relation authority. LARGEST PRODUCTIVE MOVE: owner supplies the analytical GT2 binding or confirms the structural lane. FLIGHT: local source-free tests only. DELTA: real retained consumption is proved; the synthetic analytical lane is not misrepresented as retained-source qualification.
