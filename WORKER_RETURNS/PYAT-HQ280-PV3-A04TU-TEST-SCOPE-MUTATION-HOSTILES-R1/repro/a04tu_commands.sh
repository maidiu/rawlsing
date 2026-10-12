#!/bin/sh
# PYAT HQ280 PV3 A04TU - exact reproduction commands.
# Run from the worktree root (/Users/matthewsmith/Desktop/Rawlsing_Worktrees/hq280-a04tu).
# The venv lives OUTSIDE the worktree; system Python is untouched.
set -eu
V=/Users/matthewsmith/Desktop/Rawlsing_Worktrees/.venv_a04tu
D=WORKER_RETURNS/PYAT-HQ280-PV3-A04TU-TEST-SCOPE-MUTATION-HOSTILES-R1/repro/logs
echo "venv freeze:"; "$V/bin/python" -m pip freeze
echo "HEAD:"; git rev-parse HEAD
export PYTHONDONTWRITEBYTECODE=1
"$V/bin/python" -m pytest rawlsing_next/tests/test_pre553_original_workload_v2_verifier_candidate.py -q | tee "$D/rerun_44.txt" | tail -2
"$V/bin/python" -m pytest rawlsing_next/tests/test_pre553_original_workload_v2_mutation_hostiles_candidate.py -q | tee "$D/rerun_29.txt" | tail -2
