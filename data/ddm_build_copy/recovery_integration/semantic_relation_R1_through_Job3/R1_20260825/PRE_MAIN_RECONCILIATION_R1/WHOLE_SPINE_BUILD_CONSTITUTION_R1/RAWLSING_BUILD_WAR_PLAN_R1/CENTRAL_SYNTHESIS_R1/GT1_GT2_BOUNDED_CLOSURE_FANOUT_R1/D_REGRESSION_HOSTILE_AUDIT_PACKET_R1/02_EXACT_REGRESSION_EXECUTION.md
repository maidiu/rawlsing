# GT12 CLOSURE — EXACT INTEGRATED REGRESSION EXECUTION R1

## Purpose

This is the execution contract for the centrally integrated GT1/GT2 closure candidate after selected Closure A/B/C returns are composed.

It is not runnable proof on this D branch and it is not an adoption action.

## Candidate preconditions

Before test execution, central MUST establish:

1. `HEAD` is the exact candidate SHA named in the execution receipt.
2. Candidate is a descendant of common base `42c4a1ed753071026a5186e8c1770b6359a9e48c`.
3. Working tree is clean before execution.
4. Selected Closure A/B/C commit SHAs are recorded.
5. D's packet is present as evidence only; this branch does not replace central fan-in ancestry.
6. No PRE-MAIN or `main` ref was moved by the closure workers.
7. The integrated diff contains no unauthorized semantic widening hidden behind test changes.

The pre-run scope inspection must fail closed if the candidate unexpectedly:

- reopens FIELD FORGE R2 ontology;
- widens current I04/P06 to consume FIELD FORGE relations;
- changes the existing empirical M1 basis/signature semantics to absorb the new relation basis;
- fabricates V553, V555 or V556 as a compatibility shortcut;
- introduces positive V3 transition authority;
- selects a physical architecture or unrelated source/transport/weight authority.

A green pytest run does not cure an out-of-scope diff.

## Exact test selection

### Fixed mandatory file list

Run exactly these fixed paths:

```text
rawlsing_next/tests/test_wave1_r5_q86_c11_projection.py
rawlsing_next/tests/test_wave1_gt12_i03_positive_facts.py
rawlsing_next/tests/test_field_forge_conditional_support.py
rawlsing_next/tests/test_wave1_ff_prev3_relation_admission.py
rawlsing_next/tests/test_m1_admitted_field_forge_relation_v554_ingress.py
rawlsing_next/tests/test_wave1_gt1_gt2_positive_prev3_integration.py
rawlsing_next/tests/test_pre553_source_backed_c11_facade.py
rawlsing_next/tests/test_pre553_empirical_query.py
rawlsing_next/tests/test_pre553_replay_audit.py
rawlsing_next/tests/test_pre553_structural_admission.py
rawlsing_next/tests/test_m1_temporal_v554_admission_dedup.py
rawlsing_next/tests/test_m4_v557_v558_publication_repository.py
rawlsing_next/tests/test_psepf_zero_positive_guard.py
rawlsing_next/tests/test_wsc002r_a_typed_negative_conservation.py
rawlsing_next/tests/test_wsc002r_b_v3_authoritative_guard_binding.py
rawlsing_next/tests/test_wsc_gt0_prev3_bridge.py
rawlsing_next/tests/test_wsc_gt0_end_to_end_integrated.py
rawlsing_next/tests/test_whole_machine_integration.py
```

### Deterministic closure-delta additions

Central MUST append every `rawlsing_next/tests/test_*.py` file changed or added by the selected Closure A/B/C commits relative to the common base, deduplicating any file already in the fixed list.

This is not a wildcard test run. Central first resolves the exact changed paths from the selected commit diffs and records the resulting literal path list in the execution receipt.

### Conditional M5

Append:

`rawlsing_next/tests/test_m5_runtime_rsc_peer_prior.py`

iff the final integrated GT2 acceptance path actually traverses/materializes M5.

### Conditional shared canonical-object authority

Append:

`rawlsing_next/tests/test_pre553_empirical_objects_authority.py`

iff a selected Closure commit modifies `rawlsing_next/pre553_empirical_objects.py` or `rawlsing_next/pre553_empirical_authority.py`.

### Other shared-module repair rule

If a selected Closure commit changes another pre-existing shared semantic/runtime module not already directly covered above, central must add the closest existing direct contract test for that module. If no direct test exists, fail closed and add a bounded nonauthoritative regression test before proceeding; do not substitute a broad unrelated suite.

## Environment law

Use the inherited W1G repository-root execution contract.

Evidenced baseline:

- CPython `3.11.x`;
- repository root as CWD;
- `python -m pytest`;
- no added `PYTHONPATH`;
- ambient pytest plugin autoload disabled;
- deterministic hash seed;
- bytecode writes disabled.

The real execution receipt must record exact Python, platform, pytest, and activated optional dependency versions.

If Closure A's genuine carrier-scale tests need `pandas`, `pyarrow`, `pyreadstat`, `duckdb`, or another optional package, record only the packages actually activated. Do not install a broad dependency bundle by assumption.

## Canonical command shape

Resolve the exact literal path list first, then run from repository root:

```sh
export RAWLSING_EXPECTED_HEAD='<EXACT_INTEGRATED_CANDIDATE_SHA>'
export PYTEST_DISABLE_PLUGIN_AUTOLOAD=1
export PYTHONHASHSEED=0
export PYTHONDONTWRITEBYTECODE=1

test "$(git rev-parse HEAD)" = "$RAWLSING_EXPECTED_HEAD"
test -z "$(git status --porcelain=v1)"

python -c 'import pathlib, platform, sys, pytest, rawlsing_next; p=pathlib.Path(next(iter(rawlsing_next.__path__))).resolve(); root=pathlib.Path.cwd().resolve(); assert root == pathlib.Path.cwd().resolve(); assert root in p.parents or p == root; assert sys.version_info[:2] == (3,11); print("python_executable="+sys.executable); print("python_version="+platform.python_version()); print("platform="+platform.platform()); print("pytest_version="+pytest.__version__); print("rawlsing_next_path="+str(p))'
python -m pip freeze --all

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
  <EXACT_CLOSURE_DELTA_TEST_PATHS> \
  <CONDITIONAL_M5_OR_SHARED_OBJECT_PATHS> \
  --junitxml=/tmp/rawlsing-gt12-closure-pytest.xml

test -z "$(git status --porcelain=v1)"
```

The two placeholder groups MUST be resolved to literal paths or removed before invocation. Do not pass angle-bracket tokens to pytest.

## Genuine execution evidence

Regression tests alone do not replace Closure A's real governed-data proof.

Before the hostile audit, central must also possess the selected Closure A machine-readable/markdown execution receipt proving on the exact integrated code or information-equivalent exact code identity:

- exact 19,210-member governed risk-set C11 release;
- GT1 current I03 `SUPPORTED`, denominator `19,210`;
- deterministic GT1 replay;
- GT2 current I03 `SUPPORTED`, denominator `19,210`;
- deterministic GT2 replay;
- exact fact/query/risk-set/authority/replay refs/hashes.

If central re-executes that genuine data-bearing path after fan-in, record that execution separately from pytest counts.

## Required integrated semantic assertions

The regression run must include passing tests that establish all of the following on the integrated candidate:

- Q86B remains CONDITIONER; Q86A remains TARGET;
- C relation semantic owner remains the actual FIELD FORGE owner;
- D owns only the admission decision;
- target use remains exactly `STRUCTURAL_MEDIATION_INPUT`;
- admitted permission is no wider than relation permission;
- relation/admission/M1 exact refs and authority versions/hashes survive typed bridges;
- relation-specific M1 contract remains `M1_ADMITTED_FIELD_FORGE_RELATION_V554_INGRESS@1.0.0`;
- basis remains `ADMITTED_FIELD_FORGE_RELATION`;
- signature remains `V554-SIG-004-NONTEMPORAL-ADMITTED-RELATION-EXACT`;
- existing empirical M1 SIG-001/002/003 path remains unchanged;
- no V553 object is fabricated;
- no V555/V556 object is required or produced;
- actual M4 V557/V558 exact resolution succeeds;
- actual authoritative V3 guard yields `DENY_ZERO_EFFECT` with zero actor-state, ledger, cursor, RNG and scheduler changes.

## Failure discipline

If collection/import fails, classify first as `IMPORT_OR_ENVIRONMENT` vs `TEST_FAILURE` and run only the smallest diagnostic needed to identify the missing dependency/path.

If a focused test fails:

- preserve the exact candidate SHA and failing node/path;
- do not broaden to the full repository corpus as a substitute;
- do not delete or weaken the failing assertion to get a green count;
- do not use a passing inherited test to erase a failing new seam test;
- return the smallest concrete blocker/defect to central.

If a real governed-data execution fails while fixture regressions pass, the closure gate is still failed.

## Execution receipt minimum

Record:

1. exact candidate SHA and selected Closure A/B/C SHAs;
2. exact literal test path list;
3. pre/post clean-tree output;
4. Python executable/version/platform;
5. pytest version;
6. exact activated optional dependency versions;
7. pytest terminal counts and exit code;
8. elapsed time;
9. JUnit XML path + SHA-256 if emitted;
10. genuine GT1/GT2 execution receipt identity;
11. whether M5 was traversed;
12. exact smallest failure if any.

Only after this execution gate passes may central invoke `03_BOUNDED_HOSTILE_AUDIT_HANDOFF.md`.

`REGRESSION_PASS != HOSTILE_AUDIT_PASS != GT1_GT2_ADOPTION`.
