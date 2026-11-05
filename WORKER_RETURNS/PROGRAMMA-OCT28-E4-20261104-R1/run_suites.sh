#!/usr/bin/env bash
set -eu
root=$1
cut=$2
export PYTHONPATH=. PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 LC_ALL=C
cd "$root/$cut"
git rev-parse HEAD
# The sourcefree authority test reads these exact tracked documentary inputs.
git sparse-checkout add --no-cone /HQ_HANDOFF/DECISION_LEDGER.jsonl /WORKER_RETURNS/EE-P2R6O/SUPPORT/01_NODE4A_PREDICATE_INPUTS.py
git ls-files -s HQ_HANDOFF/DECISION_LEDGER.jsonl WORKER_RETURNS/EE-P2R6O/SUPPORT/01_NODE4A_PREDICATE_INPUTS.py
test -z "$(git status --porcelain --untracked-files=no)"
bash "$root/inputs/e3/related-suite-command.sh"
python3 -m pytest rawlsing_next/tests/test_universal_world_binding.py::test_same_source_r04_partial_resume_reaches_actual_p41 -q -o addopts= -p no:cacheprovider
