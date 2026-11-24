#!/bin/sh
# Run all four source-identical saved C11 arms. No original-data ingestion.
set -eu
HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
REPO=$(CDPATH= cd -- "$HERE/../.." && pwd)
PY=${PYAT_BENCH_PYTHON:-python3}
if ! "$PY" -c 'import pyarrow, psutil' >/dev/null 2>&1; then
  echo "Missing pyarrow/psutil in $PY. Activate the existing Rawlsing Python environment." >&2
  exit 3
fi
CONFIG=${PYAT_BENCH_CONFIG:-$HERE/bundle.json}
if [ ! -f "$CONFIG" ] && [ -f "$HERE/bundle.example.json" ] && [ -z "${PYAT_BENCH_CONFIG:-}" ]; then
  CONFIG="$HERE/bundle.example.json"
fi
if [ ! -f "$CONFIG" ]; then
  echo "Missing bundle.json and bundled default. Provide PYAT_BENCH_CONFIG with exact source/authority paths." >&2
  exit 3
fi
cd "$REPO"
exec "$PY" -u -m tools.pyat_c11_four_store.runner --config "$CONFIG" "$@"
