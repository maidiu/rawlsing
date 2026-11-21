#!/bin/sh
set -eu
HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
REPO=$(CDPATH= cd -- "$HERE/../.." && pwd)
PY=${PYAT_BENCH_PYTHON:-python3}
if ! "$PY" -c 'import pyarrow, psutil' >/dev/null 2>&1; then
  echo "Missing pyarrow or psutil in $PY. Use the existing Rawlsing Python environment." >&2
  exit 3
fi
CONFIG=${PYAT_BENCH_CONFIG:-$HERE/bundle.json}
if [ ! -f "$CONFIG" ]; then
  echo "Missing $CONFIG. Copy bundle.example.json to bundle.json and specify exact authority/provider paths." >&2
  exit 3
fi
cd "$REPO"
exec "$PY" -u -m tools.pyat_c11_four_store.runner --config "$CONFIG" "$@"
