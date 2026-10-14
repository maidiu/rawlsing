#!/bin/sh
set -eu
# Use a fresh reviewer checkout/return copy. The runtime remains host-local.
python3 WORKER_RETURNS/SOROK-R3-HQ299-RC0-SC0-PE-INDEPENDENT-R1/repro/stage.py
python3 WORKER_RETURNS/SOROK-R3-HQ299-RC0-SC0-PE-INDEPENDENT-R1/repro/run.py smoke
python3 WORKER_RETURNS/SOROK-R3-HQ299-RC0-SC0-PE-INDEPENDENT-R1/repro/run_required.py
python3 WORKER_RETURNS/SOROK-R3-HQ299-RC0-SC0-PE-INDEPENDENT-R1/repro/run.py independent
python3 WORKER_RETURNS/SOROK-R3-HQ299-RC0-SC0-PE-INDEPENDENT-R1/repro/build_results.py
python3 WORKER_RETURNS/SOROK-R3-HQ299-RC0-SC0-PE-INDEPENDENT-R1/repro/run_probe.py connection_probe
python3 WORKER_RETURNS/SOROK-R3-HQ299-RC0-SC0-PE-INDEPENDENT-R1/repro/run_probe.py facade_probe
python3 WORKER_RETURNS/SOROK-R3-HQ299-RC0-SC0-PE-INDEPENDENT-R1/repro/run_probe.py probe_environment
# Read *_execution.json for actual pytest exit codes; REDs intentionally remain RED.
