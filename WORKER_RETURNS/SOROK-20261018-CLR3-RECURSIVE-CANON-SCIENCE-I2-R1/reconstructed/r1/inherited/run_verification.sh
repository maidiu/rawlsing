#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
(cd "$ROOT/m2_patch" && python -m pytest -q test_m2.py test_m3_independent.py test_m3_unresolved.py test_source_preimages.py)
(cd "$ROOT/causal_experiment" && python -m pytest -q test_world_intersection.py)
(cd "$ROOT/causal_experiment" && python world_intersection.py)
