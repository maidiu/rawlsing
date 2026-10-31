#!/usr/bin/env bash
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
RETURN=$(cd "$HERE/.." && pwd)
cd "$RETURN"
PYTHONPATH=sourcefree_adapter:../.. PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
  python3 -m pytest -q -p no:cacheprovider tests/test_selected_world_repair.py
PYTHONPATH=sourcefree_adapter:../.. PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
  python3 -m pytest -q -p no:cacheprovider tests/test_p41_current_service.py
