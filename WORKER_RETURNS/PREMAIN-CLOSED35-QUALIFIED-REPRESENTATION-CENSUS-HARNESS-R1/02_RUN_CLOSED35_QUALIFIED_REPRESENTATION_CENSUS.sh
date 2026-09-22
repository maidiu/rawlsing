#!/bin/bash
set -euo pipefail

if [[ $# -ne 2 ]]; then
  echo "usage: $0 <source-path-manifest.json> <work-output-root>" >&2
  exit 2
fi

MANIFEST="$1"
OUTPUT_ROOT="$2"
EXPECTED_BRANCH="agent/rabochii-premain-closed35-qualified-representation-census-harness-r1"
QUALIFIED_CODE_HEAD="__SOURCE_FREE_QUALIFIED_CODE_HEAD__"

if [[ "$QUALIFIED_CODE_HEAD" == __SOURCE_FREE_QUALIFIED_CODE_HEAD__ ]]; then
  echo "CLOSED35_REP_CENSUS BLOCKED: harness source-free qualification head not rebound" >&2
  exit 88
fi

REPO_ROOT="$(git rev-parse --show-toplevel)"
CURRENT_BRANCH="$(git -C "$REPO_ROOT" branch --show-current)"
if [[ "$CURRENT_BRANCH" != "$EXPECTED_BRANCH" ]]; then
  echo "CLOSED35_REP_CENSUS BLOCKED: wrong branch $CURRENT_BRANCH" >&2
  exit 89
fi

if [[ "$(uname -s)" != "Darwin" ]]; then
  echo "CLOSED35_REP_CENSUS BLOCKED: Darwin required" >&2
  exit 90
fi
if [[ "$(uname -m)" != "x86_64" ]]; then
  echo "CLOSED35_REP_CENSUS BLOCKED: x86_64 required" >&2
  exit 91
fi

PYTHON_BIN="${PYTHON_BIN:-python3}"
"$PYTHON_BIN" - <<'PY'
import importlib.metadata
import platform
import sys
expected = {
    "cpython": "3.11.3",
    "pyreadstat": "1.3.6",
    "pyarrow": "25.0.1",
}
observed = {
    "cpython": platform.python_version(),
    "pyreadstat": importlib.metadata.version("pyreadstat"),
    "pyarrow": importlib.metadata.version("pyarrow"),
}
if observed != expected:
    raise SystemExit(f"CLOSED35_REP_CENSUS BLOCKED: runtime {observed!r} != {expected!r}")
PY

exec "$PYTHON_BIN" -m rawlsing_next.closed35_representation_census_harness \
  --repo-root "$REPO_ROOT" \
  --manifest "$MANIFEST" \
  --output-root "$OUTPUT_ROOT" \
  --qualified-code-head "$QUALIFIED_CODE_HEAD"
