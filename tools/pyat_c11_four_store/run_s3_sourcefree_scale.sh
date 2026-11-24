#!/bin/sh
# Constructs only isolated, disposable, explicitly synthetic physical data.
set -eu
HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
REPO=$(CDPATH= cd -- "$HERE/../.." && pwd)
PY=${PYAT_BENCH_PYTHON:-python3}
if ! "$PY" -c 'import psutil' >/dev/null 2>&1; then
  echo "PYAT_BENCH_PYTHON must provide the existing psutil environment" >&2
  exit 3
fi
cd "$REPO"
exec "$PY" -u -m tools.pyat_c11_four_store.sourcefree_s3_scale "$@"
