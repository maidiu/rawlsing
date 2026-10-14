#!/bin/sh
set -eu
repo_root=$(git rev-parse --show-toplevel)
runtime_root=$(mktemp -d /tmp/hq295-v2k-runtime.XXXXXX)
result_root=$(mktemp -d /tmp/hq295-v2k-results.XXXXXX)
git archive 3f91dc22d2eb863bc1d2facccfd33e6c05349503 rawlsing_next WORKER_RETURNS/PYAT-HQ282-P01-V2-DURABLE-CONSUMER-INTEGRATION-R1 | tar -x -C "$runtime_root"
cp "$repo_root/rawlsing_next/pre553_original_identity_v2k_successor_candidate.py" "$runtime_root/rawlsing_next/"
export PYTHONPATH="$runtime_root"
cd "$runtime_root"
python3 -m pytest -q "$repo_root/rawlsing_next/tests/test_hq295_v2k_original_identity_successor.py" --import-mode=importlib --junitxml="$result_root/successor.xml"
python3 -m pytest -q rawlsing_next/tests/test_pre553_v2_durable_consumer_integration_candidate.py rawlsing_next/tests/test_pre553_original_workload_v2_mutation_hostiles_candidate.py rawlsing_next/tests/test_pre553_route_b_production.py rawlsing_next/tests/test_pre553_empirical_query.py rawlsing_next/tests/test_pre553_discovery_exact.py --junitxml="$result_root/owners.xml"
python3 "$repo_root/WORKER_RETURNS/PYAT-R3-HQ295-V2K-ORIGINAL-IDENTITY-SUCCESSOR-R1/repro/emit_successor.py" "$repo_root" "$result_root/ledger" "$result_root" first
python3 "$repo_root/WORKER_RETURNS/PYAT-R3-HQ295-V2K-ORIGINAL-IDENTITY-SUCCESSOR-R1/repro/emit_successor.py" "$repo_root" "$result_root/ledger" "$result_root" replay
