# Independent Phase A commands

Exact remote P8 fetched first; independent checkout:

```sh
git clone --no-hardlinks --no-checkout . /tmp/wg0p11-independent-p8
git -C /tmp/wg0p11-independent-p8 checkout --detach e1d82971f8c07147550ce53ef3c4bc52f349fed3
```

From the WG0P11 checkout, after first oracle/test commit was pushed:

```sh
export WG0P11_ROOT=/tmp/wg0p11-independent-p8/WORKER_RETURNS/PYAT-R31-WG0P8-PUBLICATION-CUSTODY-R1
export WG0P11_EVIDENCE="$PWD/WORKER_RETURNS/PYAT-R33-WG0P11-INDEPENDENT-P10-COURT-R1/03_ALL_ACTUAL_FROZEN_NATIVE_AND_COLD_JUNIT"
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -c /dev/null -q WORKER_RETURNS/PYAT-R33-WG0P11-INDEPENDENT-P10-COURT-R1/test_independent_publication.py --tb=short --junitxml="$WG0P11_EVIDENCE/phase_a_p8_D1_D5.xml"
```

Actual exit 1: 1 passed / 5 failed. Outer pytest emitted two harmless /dev cache
write warnings; future invocations can disable cacheprovider. No test was
changed or repeated to obtain a different result.

Every child command, working directory, exit, stdout and stderr is recorded in
its JSON receipt. Historical receipts record the exact native bootstrap commands
and selection for the five unconstructible controls and characterisation file.
These runs use candidate bootstrap_p6 and repro on PYTHONPATH,
WG0M_RUN=phase_b_P5, WG0L_PHASE_B_ADAPTER=phase_b_adapter_v1,
PYTHONDONTWRITEBYTECODE=1 and PYTEST_DISABLE_PLUGIN_AUTOLOAD=1.

P10 acceptance must first use the completed repair's own published runner, in a
fresh isolated exact-head clone. The independent test uses WG0P11_ROOT for that
return and optionally WG0P11_RUNNER for its published verifier script. It does
not repair directories, restore missing candidate files or rewrite cold paths.
