# WAVE 1G — REPRODUCIBLE REGRESSION / EXECUTION FINDINGS R1

## 1. Scope

This lane answers one question only:

**What is the smallest repository-native execution surface future Golden Thread fan-ins need in order to run focused tests plus the smallest inherited regression subset in a real checkout and return exact environment/count evidence?**

It does not choose product/runtime architecture, physical persistence, containerization, CI vendor, database, deployment platform or package-management sovereignty.

## 2. Repository reality

At canonical PRE-MAIN `d15f8973ddeff46dbaa15f352fe5d7e59e1fe1a3`:

- root contains `README.md`, `data/`, `rawlsing_next/`, and `section85/`;
- no root `pyproject.toml`, `setup.cfg`, `setup.py`, `requirements*.txt`, `pytest.ini`, `tox.ini`, `noxfile.py`, Dockerfile or environment YAML is present;
- no `.github/workflows/` directory is present;
- `rawlsing_next/` has no `__init__.py`;
- current `rawlsing_next/tests/` contains 32 Python test files at PRE-MAIN;
- the README explicitly says the repository intentionally excludes virtual environments and environment files and expects runtime dependencies from the receiving environment.

Therefore a new global dependency/build/CI framework would be a new project choice, not mere recovery of current test law.

## 3. Prior successful execution evidence

The strongest explicit current receipt found is:

`WAVE3/W32_EXECUTABLE_RECONSTRUCTION/COMBINED_REGRESSION_RECEIPT.txt`

It records:

- repository-native run;
- `ubuntu-latest / Python 3.11`;
- `157 passed, 0 failed, 0 errors, 0 skipped in 3.69s`.

A separate W33 receipt records retained/fresh test passes but does not provide a stronger environment identity.

Neither receipt records the exact pytest version or a dependency lock. Consequently:

`PYTHON_3_11_SUCCESS_EVIDENCE != CANONICAL_PACKAGE_LOCK`.

The correct near-term response is to fingerprint exact versions in every execution receipt rather than invent a historical package lock.

## 4. GT0 execution-gate dependency result

The exact GT0 real-checkout gate names six focused WSC002/repair files and five directly implicated inherited contract files.

Static import inspection at repaired candidate `ed1482517e0eebe2228e838dc6a24b97db879fc9` shows those 11 test files use only:

- Python standard library modules;
- `pytest`;
- `rawlsing_next`.

The corresponding GT0/current authority modules use only standard library plus other `rawlsing_next` modules.

Therefore the GT0 execution gate does **not** require:

- pandas;
- pyarrow;
- pyreadstat;
- DuckDB;
- a database service;
- network access;
- source respondent data;
- a container;
- a CI service.

This is the cheapest useful baseline for future semantic-only Golden Thread fan-ins.

## 5. Broader dependency tiers

Broader PRE553 tests do contain claim-specific external dependencies:

- `test_pre553_source_backed_c11_facade.py` imports `pandas`;
- `test_pre553_sr06_decoder_carrier.py` imports `pandas` and `pyreadstat`;
- `test_pre553_r4_compaction.py` imports `pyarrow`;
- `pre553_duckdb_direct.py` imports `duckdb` lazily only when `VerifiedDuckDBSession` is instantiated.

This proves a dependency-tier design is more faithful than one global bundle.

### Tier A — CORE_SEMANTIC

Required:

- Python 3.11 baseline;
- pytest;
- repository checkout.

Use for GT0 and future semantic-only seams unless exact selected tests prove otherwise.

### Tier B — CLAIM_TRIGGERED_CARRIER

Add only exact packages required by selected empirical/carrier tests:

- pandas;
- pyarrow;
- pyreadstat;
- duckdb.

No package becomes globally required merely because one historical test surface uses it.

## 6. Repository-root import law

Because `rawlsing_next` is a namespace package in this checkout, repository root must be on Python's import search path.

The stable execution rule is:

`CWD = REPOSITORY_ROOT`

and:

`python -m pytest ...`.

Do not:

- run from inside `rawlsing_next/tests`;
- install a second unrelated `rawlsing_next` package and let it shadow checkout sources;
- add arbitrary `PYTHONPATH` entries;
- use a standalone `pytest` binary whose interpreter may differ from the recorded Python.

A receipt that cannot prove checkout-local imports is not sufficient for canonicalization.

## 7. Ambient pytest isolation

The repository has no project pytest plugin contract. Ambient user/global plugins can change collection, warnings, fixtures or execution behavior without appearing in Git.

Therefore the baseline sets:

`PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`.

Current exact GT0 tests do not use third-party plugin APIs, so this narrows environmental variability without removing a repository-declared requirement.

If a future test explicitly requires a plugin, that plugin becomes claim-triggered and must be named/versioned in the exact execution contract rather than silently autoloaded.

## 8. Determinism / clean-checkout controls

Baseline environment:

```sh
export PYTEST_DISABLE_PLUGIN_AUTOLOAD=1
export PYTHONHASHSEED=0
export PYTHONDONTWRITEBYTECODE=1
```

Precondition:

```sh
test "$(git rev-parse HEAD)" = "$RAWLSING_EXPECTED_HEAD"
test -z "$(git status --porcelain=v1)"
```

Postcondition:

```sh
test -z "$(git status --porcelain=v1)"
```

The pre/post status comparison prevents generated files or test side effects from being silently accepted as part of the candidate.

## 9. Environment fingerprint

Before the test command, record:

```sh
python -c 'import platform, sys, pytest; print("python_executable="+sys.executable); print("python_version="+platform.python_version()); print("platform="+platform.platform()); print("pytest_version="+pytest.__version__)'
python -m pip freeze --all
```

For the current compatibility baseline also require:

```sh
python -c 'import sys; assert sys.version_info[:2] == (3, 11), sys.version'
```

This is an execution compatibility contract, not a claim that only Python 3.11 can ever work.

## 10. Exact GT0 command instance

The current gate can be run in one pytest process from repository root:

```sh
python -m pytest -q \
  rawlsing_next/tests/test_wsc_gt0_protocol.py \
  rawlsing_next/tests/test_wsc_gt0_prev3_bridge.py \
  rawlsing_next/tests/test_wsc_gt0_end_to_end_integrated.py \
  rawlsing_next/tests/test_wsc002r_a_typed_negative_conservation.py \
  rawlsing_next/tests/test_wsc002r_b_v3_authoritative_guard_binding.py \
  rawlsing_next/tests/test_wsc002r_c_m6_render_authoritative_binding.py \
  rawlsing_next/tests/test_pre553_structural_admission.py \
  rawlsing_next/tests/test_m1_temporal_v554_admission_dedup.py \
  rawlsing_next/tests/test_psepf_zero_positive_guard.py \
  rawlsing_next/tests/test_m6_actor_safe_expression.py \
  rawlsing_next/tests/test_render_bounded_expression.py \
  --junitxml=/tmp/rawlsing-golden-thread-pytest.xml
```

This is file-grain exactness. Future gates may narrow to exact node IDs if the commissioning handoff specifies them; this lane does not invent node-level exclusions absent such authority.

## 11. Future fan-in selection rule

Every future Golden Thread fan-in should construct its suite from three sets:

`NEW_FOCUSED_TESTS`

plus:

`DIRECTLY_CHANGED_OR_BOUND_CONTRACT_TESTS`

plus:

`SMALLEST_INHERITED_SEAM_TESTS_NAMED_BY_THE_GATE`.

Do not automatically run all 32 current PRE-MAIN tests, and do not automatically skip inherited regressions.

A broader diagnostic is authorized only after a concrete failure such as:

- import/collection failure;
- signature/type drift that may affect an adjacent inherited module;
- shared fixture/helper failure;
- candidate-caused change to a common semantic primitive.

## 12. Receipt schema

A sufficient execution receipt is one immutable text/markdown/JSON object containing:

- `repository`;
- `candidate_sha`;
- `expected_sha`;
- `pre_git_status`;
- `post_git_status`;
- `cwd`;
- `python_executable`;
- `python_version`;
- `platform`;
- `pytest_version`;
- optional activated dependency versions;
- exact environment variables affecting pytest;
- exact ordered test paths/node IDs;
- exact command;
- exit code;
- passed/failed/error/skipped/xfailed/xpassed/deselected counts;
- elapsed time;
- JUnit path and SHA-256 when emitted;
- any smallest diagnostic command/result;
- final terminal.

No count should be inferred by counting `test_` functions statically because parametrization changes collected case counts.

## 13. Why no new runner/CI file was added

The four-file Wave 1 lane contract is already sufficient to reproduce the command surface.

Adding a repository-root runner, CI workflow, container or global dependency lock now would create one or more new project-level infrastructure choices without a starvation witness. It would also create a second location that could drift from gate-defined exact test paths.

Central fan-in may later wrap this contract in a thin script or CI job if repeated execution requires it. Such a wrapper must accept the exact candidate SHA and exact test list as inputs and must not become a semantic source of truth.

## 14. Integration handoff

For the Wave 1 central fan-in:

1. consume the selected empirical/structural test paths from lanes A-F after their fan-in;
2. classify each path as CORE_SEMANTIC or CLAIM_TRIGGERED_CARRIER;
3. add only activated optional packages;
4. execute from a clean repo-root checkout using Python 3.11 baseline and plugin autoload disabled;
5. report the exact environment and pytest counts;
6. if a new semantic boundary is accepted, preserve the exact focused + smallest inherited suite for its bounded hostile audit.

Terminal:

`PASS__WAVE1G_REGRESSION_EXECUTION_ENVIRONMENT_READY`
