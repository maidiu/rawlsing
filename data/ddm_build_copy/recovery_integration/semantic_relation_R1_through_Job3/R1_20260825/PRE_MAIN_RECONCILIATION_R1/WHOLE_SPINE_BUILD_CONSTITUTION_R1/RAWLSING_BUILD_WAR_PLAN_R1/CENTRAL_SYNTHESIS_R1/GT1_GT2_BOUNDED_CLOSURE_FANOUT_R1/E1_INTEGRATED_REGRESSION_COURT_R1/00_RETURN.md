# GT12 FINAL E1 — INTEGRATED REGRESSION COURT R1

## Terminal

`PASS__GT12_FINAL_E1_INTEGRATED_REGRESSION_COURT_GREEN`

## Exact candidate identity

Frozen integrated production candidate:

`820311811b3e4094aea7e0e665fd0a228520cd1a`

Exact court execution HEAD after the permitted, separately identified test-only fixture refresh:

`f1c7ea61a8583e0ca47efecbf6b86ed92569ddbb`

The delta from the frozen candidate to the court execution HEAD changes exactly two test files and **zero production modules**:

- `rawlsing_next/tests/test_pre553_replay_audit.py`
- `rawlsing_next/tests/test_gt12_d_to_m4_typed_bridge.py`

The production/runtime tree under test is therefore the frozen integrated candidate.

Selected closure tips recorded:

- A1: `2753d1abbcb702e9260f4ab60c528748fb28c7d2`
- A2: `eb625ef51a99d9661d90e9ac3e496b00f7e9032a`
- B: `a4c6e57d628c94cf1a6cda9e149371d230dacd62`
- C: `24eccabda8a15ad885ece71351b8464e68eebda3`
- D packet: `5ce9b13285f5ac42297e01a21e8dba4026c0a5ac`

## Environment fingerprint

- runner: GitHub-hosted Ubuntu 24.04.4 LTS
- Python executable: `/opt/hostedtoolcache/Python/3.11.16/x64/bin/python`
- CPython: `3.11.16`
- platform: `Linux-6.17.0-1022-azure-x86_64-with-glibc2.39`
- pytest: `9.1.1`
- pip: `26.2.1`
- setuptools: `79.0.1`
- optional dependency activated because the mandatory source-backed test imports it: `pandas==3.0.5`
- transitive activated numeric dependency: `numpy==2.4.6`
- `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`
- `PYTHONHASHSEED=0`
- `PYTHONDONTWRITEBYTECODE=1`
- no added `PYTHONPATH`
- repository root CWD

## Exact regression command

```sh
export RAWLSING_EXPECTED_HEAD='f1c7ea61a8583e0ca47efecbf6b86ed92569ddbb'
export PYTEST_DISABLE_PLUGIN_AUTOLOAD=1
export PYTHONHASHSEED=0
export PYTHONDONTWRITEBYTECODE=1

python -m pytest -q \
  rawlsing_next/tests/test_wave1_r5_q86_c11_projection.py \
  rawlsing_next/tests/test_wave1_gt12_i03_positive_facts.py \
  rawlsing_next/tests/test_field_forge_conditional_support.py \
  rawlsing_next/tests/test_wave1_ff_prev3_relation_admission.py \
  rawlsing_next/tests/test_m1_admitted_field_forge_relation_v554_ingress.py \
  rawlsing_next/tests/test_wave1_gt1_gt2_positive_prev3_integration.py \
  rawlsing_next/tests/test_pre553_source_backed_c11_facade.py \
  rawlsing_next/tests/test_pre553_empirical_query.py \
  rawlsing_next/tests/test_pre553_replay_audit.py \
  rawlsing_next/tests/test_pre553_structural_admission.py \
  rawlsing_next/tests/test_m1_temporal_v554_admission_dedup.py \
  rawlsing_next/tests/test_m4_v557_v558_publication_repository.py \
  rawlsing_next/tests/test_psepf_zero_positive_guard.py \
  rawlsing_next/tests/test_wsc002r_a_typed_negative_conservation.py \
  rawlsing_next/tests/test_wsc002r_b_v3_authoritative_guard_binding.py \
  rawlsing_next/tests/test_wsc_gt0_prev3_bridge.py \
  rawlsing_next/tests/test_wsc_gt0_end_to_end_integrated.py \
  rawlsing_next/tests/test_whole_machine_integration.py \
  rawlsing_next/tests/test_wave1_gt12_a2_real_gt1.py \
  rawlsing_next/tests/test_gt12_closure_b_c_to_d_bridge.py \
  rawlsing_next/tests/test_gt12_d_to_m4_typed_bridge.py \
  rawlsing_next/tests/test_m5_runtime_rsc_peer_prior.py \
  rawlsing_next/tests/test_pre553_c11_repository_ingest.py \ \
  --junitxml=/tmp/rawlsing-gt12-closure-pytest.xml
```

The 23 paths include the entire Closure-D fixed matrix, all A2/B/C closure-delta tests, conditional M5 because the integrated acceptance harness materializes M5, and the direct C11 ingest contract because Closure A changed shared ingest/integrity code.

## Final court result

GitHub Actions run: `33787185431`

Job: `100754681149`

Result:

- **354 passed**
- **0 failed**
- **0 collection errors**
- pytest exit code: **0**
- pytest summary time: **3.14 s**
- measured command time: **3.654702958 s**
- JUnit XML: `/tmp/rawlsing-gt12-closure-pytest.xml`
- JUnit SHA-256: `dd47adfaa074b14935c3b0886901749d57ee21bcc66991d24a149beb12261aaf`

Pre-run:

- HEAD = `f1c7ea61a8583e0ca47efecbf6b86ed92569ddbb`
- tree clean = **YES**

Post-run:

- HEAD = `f1c7ea61a8583e0ca47efecbf6b86ed92569ddbb`
- tree clean = **YES**

## Diagnostic failures and exact classification

### Environment correction

An earlier real checkout run, `33786678343`, stopped during collection because the mandatory source-backed C11 test imports pandas.

Blocker:

`ModuleNotFoundError: No module named 'pandas'`

Classification:

`IMPORT_OR_ENVIRONMENT`

Only pandas was added to the runner environment. No candidate or test assertion changed for this correction.

### Stale fixture/test assumptions

With pandas active, the frozen candidate itself produced:

`347 passed, 7 failed`

The seven failing node IDs were:

- `rawlsing_next/tests/test_pre553_replay_audit.py::test_replay_manifest_tamper_fails_against_pinned_identity`
- `rawlsing_next/tests/test_pre553_replay_audit.py::test_i02_validate_replay_accepts_only_exact_manifest`
- `rawlsing_next/tests/test_pre553_replay_audit.py::test_i02_validate_replay_rejects_semantic_projection_tamper`
- `rawlsing_next/tests/test_pre553_replay_audit.py::test_i02_validate_replay_rejects_source_content_tamper`
- `rawlsing_next/tests/test_pre553_replay_audit.py::test_i02_validate_replay_rejects_authority_set_tamper`
- `rawlsing_next/tests/test_pre553_replay_audit.py::test_i02_validate_replay_rejects_missing_replay_authority`
- `rawlsing_next/tests/test_gt12_d_to_m4_typed_bridge.py::test_actor_or_v3_authority_is_not_created_by_bridge_payload`

Classification:

`STALE_FIXTURE_TEST_ASSUMPTION`

The replay-audit fixtures still patched the obsolete materialized `_candidate_projection` helper even though the accepted A1 scale repair moved exact replay hashing to `_candidate_projection_semantic_hash`. The test-only refresh now patches the exact current helper to the same semantic hash oracle; source/hash/authority/replay assertions are unchanged.

The Closure-C negative test used `"V3_" not in repr(payload)`, which falsely matches lawful `PREV3_` identifiers. The refreshed assertion structurally rejects actual `V3_` / `ACTOR_` semantic fields and V3/actor authority namespaces, while retaining the exact M1 downstream-contract, no-new-V553, and focal-proposition assertions. This is more specific to the asserted prohibition and does not permit positive V3 authority.

No production semantic repair was made.

## Scope confirmations

E1 did **not**:

- rerun the real governed GT2 data execution;
- perform the final hostile audit;
- issue GT1/GT2 adoption;
- alter FIELD FORGE or PRE-V3 semantics;
- change any production module;
- acquire Library/source data;
- move PRE-MAIN;
- move `main`.

The temporary GitHub Actions execution scaffold is absent from the final branch tree.

## Terminal

`PASS__GT12_FINAL_E1_INTEGRATED_REGRESSION_COURT_GREEN`
