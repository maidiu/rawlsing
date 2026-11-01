#!/bin/sh
set -eu
HERE=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
export PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0
export M35_JOIN_E_RETURN="$HERE/deps/join_e"
export PYTHONPATH="$HERE:$HERE/deps/m35:$HERE/deps/join_e"
exec python3 -m pytest -q "$HERE/tests/test_p1.py" "$@"
