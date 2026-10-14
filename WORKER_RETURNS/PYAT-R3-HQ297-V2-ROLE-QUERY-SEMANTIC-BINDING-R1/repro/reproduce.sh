#!/bin/sh
set -eu
# Run in a fresh assigned checkout to preserve these saved execution artifacts.
python3 WORKER_RETURNS/PYAT-R3-HQ297-V2-ROLE-QUERY-SEMANTIC-BINDING-R1/repro/execute.py red
python3 WORKER_RETURNS/PYAT-R3-HQ297-V2-ROLE-QUERY-SEMANTIC-BINDING-R1/repro/execute.py green
python3 WORKER_RETURNS/PYAT-R3-HQ297-V2-ROLE-QUERY-SEMANTIC-BINDING-R1/repro/execute.py regressions
python3 WORKER_RETURNS/PYAT-R3-HQ297-V2-ROLE-QUERY-SEMANTIC-BINDING-R1/repro/cold_replay.py
