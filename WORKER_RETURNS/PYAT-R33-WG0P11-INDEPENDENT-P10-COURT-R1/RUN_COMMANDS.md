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

## Completed P10 Phase B

Exact candidate head: `c9f876788dea5770563f0c1ac3354ec745cfa59c`.
The initial detached local-object clone was used for the first complete replay;
its evidence remains under `phase_b_p10/`. A further direct GitHub clone removes
reliance on locally accumulated Git objects. Its evidence is under
`phase_b_remote/`.

```sh
git clone --filter=blob:none --no-checkout https://github.com/maidiu/rawlsing.git /tmp/wg0p11-remote-filtered-p10
git -C /tmp/wg0p11-remote-filtered-p10 sparse-checkout init --cone
git -C /tmp/wg0p11-remote-filtered-p10 sparse-checkout set WORKER_RETURNS/PYAT-R33-WG0P10-PUBLICATION-REPAIR-R1
git -C /tmp/wg0p11-remote-filtered-p10 checkout --detach c9f876788dea5770563f0c1ac3354ec745cfa59c
```

The source filter avoids downloading unrelated historical file bodies; all
1,272 P10 artifact files are actually materialized and independently match the
immutable Git tree. There is no objects/info/alternates. The historical register
read by the published bootstrap is verified directly with `git show` at
`bec9a128922e4e431ce2ed862aa7802c902813ed` and compared byte-for-byte with the
already-staged frozen register. This reads Git history and never overlays a
candidate file. The exact command is recorded in
`phase_b_remote/historical_register_git_dependency.json`.

After materialization, every replay subprocess receives the following Git
configuration override so a missing object cannot be silently fetched:

```sh
export GIT_CONFIG_COUNT=1
export GIT_CONFIG_KEY_0=remote.origin.url
export GIT_CONFIG_VALUE_0=/nonexistent/WG0P11_GIT_NETWORK_DISABLED
export PYTHONDONTWRITEBYTECODE=1
export PYTEST_DISABLE_PLUGIN_AUTOLOAD=1
cd /tmp/wg0p11-remote-filtered-p10/WORKER_RETURNS/PYAT-R33-WG0P10-PUBLICATION-REPAIR-R1
python3 -B repro/wg0p8_publication.py verify
python3 -B repro/wg0p8_publication.py probe-import
python3 -B repro/wg0p10_regenerate_cold.py
python3 -B repro/wg0p8_publication.py run
```

From the WG0P11 write checkout, set WG0P11_ROOT to that P10 return and
WG0P11_EVIDENCE to the absolute `phase_b_remote` evidence directory. Execute the
unchanged `test_independent_publication.py` with pytest (`-c /dev/null -p
no:cacheprovider`) and JUnit, then `phase_b_hostiles.py` with its evidence under
`phase_b_remote/source_hostiles`. Run P10's published transport-9 test with a
fresh JUnit file. Exact child commands/cwd/exits/stdout/stderr are persisted.

The two original historical test selections also run unmodified under the
native bootstrap. Their required failures remain recorded separately from the
passing mandatory court. A final verifier and independent source rehash confirm
that the deliberate hostile stimuli were fully restored, and no candidate
Python source changed. No original test or expectation is modified.
