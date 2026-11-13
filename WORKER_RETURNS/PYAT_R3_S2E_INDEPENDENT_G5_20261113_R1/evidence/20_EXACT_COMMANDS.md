# Exact execution commands

All commands ran from a sparse worktree of the frozen repository root unless
noted. Python was a dedicated temp venv:

```sh
python3 -m venv /var/folders/.../s2e-g5-venv
s2e-g5-venv/bin/python -m pip install --disable-pip-version-check -q \
  pytest pandas pyreadstat pyarrow duckdb
```

Frozen worktree:

```sh
git worktree add --no-checkout --detach /var/folders/.../s2e-g5-code \
  81a764cc7eac960f0fd607d9c3fe62428905daa4
git -C /var/folders/.../s2e-g5-code sparse-checkout init --cone
git -C /var/folders/.../s2e-g5-code sparse-checkout set rawlsing_next .github
git -C /var/folders/.../s2e-g5-code checkout \
  81a764cc7eac960f0fd607d9c3fe62428905daa4
```

Frozen native/hostile/regression suite:

```sh
cd /var/folders/.../s2e-g5-code
PYTHONPATH=. /usr/bin/time -l /var/folders/.../s2e-g5-venv/bin/python \
  -B -m pytest -q -s -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_pyat919_s2e_a3_native_closure.py \
  rawlsing_next/tests/test_pyat919_s2e_b2_fate_counterexample.py \
  rawlsing_next/tests/test_pyat919_s2e_a_whole_native_batch.py \
  rawlsing_next/tests/test_pyat919_s2e_a_counterattack.py \
  rawlsing_next/tests/test_pyat919_s2e_a_conservation.py \
  rawlsing_next/tests/test_pre553_empirical_query.py \
  rawlsing_next/tests/test_pre553_discovery_exact.py \
  rawlsing_next/tests/test_universal_workload.py \
  rawlsing_next/tests/test_universal_workload_custody.py
```

Frozen core monitored suite (fast process-tree sampler):

```sh
PYTHONPATH=. /var/folders/.../s2e-g5-venv/bin/python \
  probes/run_tree_fast.py \
  /var/folders/.../s2e-g5-venv/bin/python -B -m pytest -q -s \
  -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_pyat919_s2e_a3_native_closure.py \
  rawlsing_next/tests/test_pyat919_s2e_b2_fate_counterexample.py \
  rawlsing_next/tests/test_pyat919_s2e_a_whole_native_batch.py \
  rawlsing_next/tests/test_pyat919_s2e_a_counterattack.py \
  rawlsing_next/tests/test_pyat919_s2e_a_conservation.py
```

S2-F preservation:

```sh
PYTHONPATH=. /usr/bin/time -l /var/folders/.../s2e-g5-venv/bin/python \
  -B -m pytest -q -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_pyat940_s2f_a_counter_provenance.py \
  rawlsing_next/tests/test_pyat940_s2f_b_negative_and_multisource.py \
  rawlsing_next/tests/test_pyat940_s2f_durable_closure.py \
  rawlsing_next/tests/test_pyat940_s2f_fresh_process.py
```

Test-only repair worktree and green suite:

```sh
git worktree add --no-checkout --detach /var/folders/.../s2e-g5-code-repaired \
  7b19a242ebc9edf85bf8303be33338f860eabf65
git -C /var/folders/.../s2e-g5-code-repaired sparse-checkout init --cone
git -C /var/folders/.../s2e-g5-code-repaired sparse-checkout set rawlsing_next .github
git -C /var/folders/.../s2e-g5-code-repaired checkout \
  7b19a242ebc9edf85bf8303be33338f860eabf65
cd /var/folders/.../s2e-g5-code-repaired
PYTHONPATH=. /var/folders/.../s2e-g5-venv/bin/python probes/run_tree_fast.py \
  /var/folders/.../s2e-g5-venv/bin/python -B -m pytest -q -s \
  -o addopts='' -p no:cacheprovider \
  <the same nine test files>
```

Independent frozen-code attacks and witness:

```sh
cd /var/folders/.../s2e-g5-code
PYTHONPATH=. /var/folders/.../s2e-g5-venv/bin/python -B -m pytest -q -s \
  -o addopts='' -p no:cacheprovider attacks/test_independent_b2_fate.py
PYTHONPATH=. /var/folders/.../s2e-g5-venv/bin/python -B -m pytest -q -s \
  -o addopts='' -p no:cacheprovider attacks/test_independent_a3_additive.py
PYTHONPATH=. /var/folders/.../s2e-g5-venv/bin/python -B -m pytest -q -s \
  -o addopts='' -p no:cacheprovider attacks/test_independent_a3_predicate.py
PYTHONPATH=. /var/folders/.../s2e-g5-venv/bin/python -B \
  probes/s2e_positive_witness.py
```

Additional F3/state coverage (inherited tests, frozen code):

```sh
PYTHONPATH=. /var/folders/.../s2e-g5-venv/bin/python -B -m pytest -q \
  -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_discovery_exact.py::test_simpson_reversal_is_detected_from_exact_pooled_and_stratified_facts \
  rawlsing_next/tests/test_pre553_discovery_exact.py::test_supported_non_top_minority_is_not_prevalence_pruned \
  rawlsing_next/tests/test_pre553_discovery_exact.py::test_recursive_subgroup_fork_preserves_exact_parent_ancestry \
  rawlsing_next/tests/test_pre553_discovery_exact.py::test_valid_empty_frontier_is_typed_and_complete \
  rawlsing_next/tests/test_pre553_discovery_exact.py::test_diagnostic_validation_cannot_become_canonical_empirical_truth
PYTHONPATH=. /var/folders/.../s2e-g5-venv/bin/python -B -m pytest -q \
  -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_analytical_composition_higher_order.py::test_at10_minority_and_counterpattern_branches_are_supported
PYTHONPATH=. /var/folders/.../s2e-g5-venv/bin/python -B -m pytest -q \
  -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_analytical_state_and_route.py -k at14
```
