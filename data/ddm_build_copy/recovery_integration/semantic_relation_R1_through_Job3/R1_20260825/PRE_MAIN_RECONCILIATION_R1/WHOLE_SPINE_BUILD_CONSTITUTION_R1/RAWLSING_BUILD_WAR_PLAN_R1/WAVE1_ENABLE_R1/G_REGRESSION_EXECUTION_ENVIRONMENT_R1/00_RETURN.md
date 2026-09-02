# RAWLSING WAVE 1G — REPRODUCIBLE REGRESSION / EXECUTION ENVIRONMENT R1

Status:

`PASS__WAVE1G_REGRESSION_EXECUTION_ENVIRONMENT_READY`

## Identity

- repository: `maidiu/rawlsing`
- worker branch: `agent/rabochii-warplan-w1g-regression-execution-environment-r1`
- exact working ancestry: `d15f8973ddeff46dbaa15f352fe5d7e59e1fe1a3`
- immutable Wave 1 instruction/evidence ref: `3454b15ff7ef388f6e028f78fad4e229c9aa969f`
- GT0 hostile rereview semantic evidence: `19ea48a7f0742c721e28b4ac51e6c205d01f5497`
- repaired GT0 candidate referenced for execution-surface inspection only: `ed1482517e0eebe2228e838dc6a24b97db879fc9`
- no sibling Wave 1 Enable branch consumed
- no PRE-MAIN or `main` movement performed

## Ruling

The smallest reproducible Golden Thread regression surface is a thin **repository-root Python/pytest command contract plus environment fingerprint**, not a new CI, container, deployment, database, package-management or product architecture.

Current repository evidence does not justify adding a root `pyproject.toml`, `requirements*.txt`, `pytest.ini`, `tox.ini`, `noxfile.py`, container definition or CI workflow merely to run the Golden Thread suites.

The canonical source-transfer README explicitly says generated outputs, virtual environments and environment files are excluded and the receiving environment supplies runtime dependencies. Canonical PRE-MAIN also contains no root pytest/dependency/CI manifest.

A prior successful combined regression receipt records:

- runner: `ubuntu-latest`;
- Python: `3.11`;
- result: `157 passed, 0 failed, 0 errors, 0 skipped`;
- elapsed: `3.69s`.

That is current compatibility evidence for a Python 3.11 baseline. It is **not** evidence for a particular pytest/package version because those versions were not recorded.

## Implemented execution contract

Future Golden Thread fan-ins should execute from the repository root with:

- exact candidate SHA verified before execution;
- clean working tree before and after execution;
- CPython `3.11.x` as the evidenced baseline;
- `python -m pytest`, never a path-dependent standalone `pytest` executable;
- `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1` to remove ambient third-party plugin drift;
- `PYTHONHASHSEED=0` for deterministic hash-order conditions;
- `PYTHONDONTWRITEBYTECODE=1` so test execution does not dirty the checkout with bytecode;
- no added `PYTHONPATH` when executing from repository root;
- exact interpreter/platform/pytest/package fingerprints captured in the return receipt;
- exact test path list recorded verbatim;
- exact pytest terminal counts recorded;
- a JUnit XML emitted outside the repository when machine-readable counts are useful.

`rawlsing_next` has no package `__init__.py` at current PRE-MAIN. Its tests rely on repository-root import visibility as a namespace package. Therefore changing the working directory to `rawlsing_next/tests` or injecting an unrelated installed `rawlsing_next` must be treated as an execution-integrity failure.

## Dependency tiers

### CORE_SEMANTIC

The exact GT0 focused + inherited gate surface imports only:

- Python standard library;
- `rawlsing_next`;
- `pytest`.

No pandas, pyarrow, pyreadstat, DuckDB, database server, network service or respondent data is required for that exact gate.

### CLAIM_TRIGGERED_CARRIER

Broader current PRE553 tests demonstrate optional dependency requirements at specific file grains:

- `pandas` — source-backed facade / physical decoder fixtures;
- `pyarrow` — Parquet/R4 carrier tests;
- `pyreadstat` — SR06 physical decoder/carrier tests;
- `duckdb` — imported lazily by the direct DuckDB session when that execution path is actually invoked.

These packages are **not** baseline Golden Thread dependencies. A future fan-in adds only the packages directly imported or invoked by its exact selected test subset.

## Exact GT0 gate example

For the current GT0 execution gate, the file-grain suite is:

`rawlsing_next/tests/test_wsc_gt0_protocol.py`
`rawlsing_next/tests/test_wsc_gt0_prev3_bridge.py`
`rawlsing_next/tests/test_wsc_gt0_end_to_end_integrated.py`
`rawlsing_next/tests/test_wsc002r_a_typed_negative_conservation.py`
`rawlsing_next/tests/test_wsc002r_b_v3_authoritative_guard_binding.py`
`rawlsing_next/tests/test_wsc002r_c_m6_render_authoritative_binding.py`
`rawlsing_next/tests/test_pre553_structural_admission.py`
`rawlsing_next/tests/test_m1_temporal_v554_admission_dedup.py`
`rawlsing_next/tests/test_psepf_zero_positive_guard.py`
`rawlsing_next/tests/test_m6_actor_safe_expression.py`
`rawlsing_next/tests/test_render_bounded_expression.py`.

The first six are GT0/repair focused surfaces. The last five are the smallest directly named inherited contract files required by the execution gate.

## Canonical command shape

From the repository root in a real checkout:

```sh
export RAWLSING_EXPECTED_HEAD='<exact candidate SHA>'
export PYTEST_DISABLE_PLUGIN_AUTOLOAD=1
export PYTHONHASHSEED=0
export PYTHONDONTWRITEBYTECODE=1

test "$(git rev-parse HEAD)" = "$RAWLSING_EXPECTED_HEAD"
test -z "$(git status --porcelain=v1)"

python -c 'import platform, sys, pytest; print("python_executable="+sys.executable); print("python_version="+platform.python_version()); print("platform="+platform.platform()); print("pytest_version="+pytest.__version__)'
python -m pip freeze --all

python -m pytest -q <EXACT_FOCUSED_AND_INHERITED_PATHS> \
  --junitxml=/tmp/rawlsing-golden-thread-pytest.xml

test -z "$(git status --porcelain=v1)"
```

For the evidenced baseline, the execution controller must additionally verify `sys.version_info[:2] == (3, 11)` before asserting parity with the prior repository-native receipt.

## Receipt minimum

Every fan-in/execution return should report:

1. repository and exact candidate SHA;
2. exact command and test-path list;
3. pre/post `git status --porcelain=v1`;
4. Python executable + exact version;
5. platform identity;
6. pytest exact version;
7. activated optional dependency versions, if any;
8. pytest passed/failed/error/skipped/xfailed/xpassed/deselected counts as emitted;
9. exit code;
10. elapsed time from pytest output;
11. JUnit artifact path/hash if emitted;
12. smallest diagnostic command if the primary subset failed at import/collection time.

## Diagnostic discipline

If a focused run fails:

- first classify `IMPORT_OR_ENVIRONMENT` vs `TEST_FAILURE`;
- for import/environment failure, run only the smallest import/version diagnostic needed to name the missing package/module/path;
- do not broaden immediately to the whole test corpus;
- do not install broad optional dependency bundles unless the selected test paths prove they need them;
- do not use a passing broader suite to erase a failing focused test;
- preserve the exact candidate SHA and failing node/file identity.

## No infrastructure promotion

This lane does not select:

- GitHub Actions or any CI vendor;
- Docker/OCI or another container architecture;
- Conda/Poetry/uv/pip-tools as canonical package manager;
- web/app framework;
- database/backend;
- deployment platform;
- persistent runtime architecture.

If central fan-in later wants a durable CI job, it can wrap this exact command contract without changing its semantic/test-selection law.

Terminal:

`PASS__WAVE1G_REGRESSION_EXECUTION_ENVIRONMENT_READY`
