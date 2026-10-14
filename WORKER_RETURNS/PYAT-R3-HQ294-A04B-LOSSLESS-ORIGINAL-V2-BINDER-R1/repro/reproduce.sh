#!/bin/sh
set -eu
repo_root=$(git rev-parse --show-toplevel)
runtime_root=$(mktemp -d /tmp/hq294-a04b-owner.XXXXXX)
result_root=$(mktemp -d /tmp/hq294-a04b-results.XXXXXX)
# Exact Git archive, no checkout changes and no original source reads.
git archive 3f91dc22d2eb863bc1d2facccfd33e6c05349503 rawlsing_next | tar -x -C "$runtime_root"
export PYTHONPATH="$runtime_root"
cd "$runtime_root"
python3 -m pytest -q "$repo_root/rawlsing_next/tests/test_hq294_a04b_identity_court.py" --import-mode=importlib --junitxml="$result_root/identity.xml"
python3 -m pytest -q rawlsing_next/tests/test_pre553_v2_durable_consumer_integration_candidate.py rawlsing_next/tests/test_pre553_original_workload_v2_mutation_hostiles_candidate.py rawlsing_next/tests/test_pre553_route_b_production.py rawlsing_next/tests/test_pre553_empirical_query.py rawlsing_next/tests/test_pre553_discovery_exact.py --junitxml="$result_root/owners.xml"
python3 "$repo_root/WORKER_RETURNS/PYAT-R3-HQ294-A04B-LOSSLESS-ORIGINAL-V2-BINDER-R1/repro/emit_cold.py" "$result_root/ledger" "$result_root" first
python3 "$repo_root/WORKER_RETURNS/PYAT-R3-HQ294-A04B-LOSSLESS-ORIGINAL-V2-BINDER-R1/repro/emit_cold.py" "$result_root/ledger" "$result_root" replay
