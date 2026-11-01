#!/bin/sh
set -eu
HERE=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
export PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0
exec python3 "$HERE/p1_hostile.py" "$@"
