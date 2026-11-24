#!/bin/sh
# Read-only existing-S3 source-authorized/native or physical-only economics.
set -eu
HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
REPO=$(CDPATH= cd -- "$HERE/../.." && pwd)
PY=${PYAT_BENCH_PYTHON:-python3}
if ! "$PY" -c 'import pyarrow, psutil' >/dev/null 2>&1; then
  echo "PYAT_BENCH_PYTHON must provide the existing pyarrow/psutil environment" >&2
  exit 3
fi
cd "$REPO"
exec "$PY" -u -m tools.pyat_c11_four_store.prepared_s3_runner "$@"
