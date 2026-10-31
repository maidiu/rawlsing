#!/usr/bin/env bash
set -euo pipefail

HERE=$(cd "$(dirname "$0")" && pwd)
RETURN=$(cd "$HERE/.." && pwd)
REPO_ROOT=${REPO_ROOT:-$(git -C "$RETURN" rev-parse --show-toplevel)}
SOURCE_COMMIT=e61a26ce24f023a53d6b116bb9eca2fb7b6f8e65
OUT="$HERE"
WORK=${WORK:-$(mktemp -d "${TMPDIR:-/tmp}/pe-sc0-original.XXXXXX")}
KEEP_WORK=${KEEP_WORK:-0}

cleanup() {
  if [ "$KEEP_WORK" != "1" ]; then
    rm -rf "$WORK"
  fi
}
trap cleanup EXIT

git -C "$REPO_ROOT" archive "$SOURCE_COMMIT" rawlsing_next | tar -x -C "$WORK"
test "$(git -C "$REPO_ROOT" hash-object "$WORK/rawlsing_next/pre553_postastra_pe_generic_world_possibility.py")" = 58484f4c3d9aae148d4116dcf00420c432aefcbd
test "$(git -C "$REPO_ROOT" hash-object "$WORK/rawlsing_next/tests/test_postastra_pe_fixture.py")" = c9674d5fe9d01621eda0fdb4a999391eba422d92

export HQ297_EXACT_PE_ROOT="$WORK"
export PYTHONPATH="$WORK"
export PYTHONDONTWRITEBYTECODE=1
export PYTHONHASHSEED=0

cd "$WORK"
python3 -m pytest -q -p no:cacheprovider rawlsing_next/tests/test_postastra_pe_generic_world_possibility.py \
  --junitxml="$OUT/original_author_21.junit.xml" 2>&1 | tee "$OUT/original_author_21.log"
set +e
python3 -m pytest -q -p no:cacheprovider rawlsing_next/tests/test_hq297_k9k10_sc0_pe_independent.py \
  --junitxml="$OUT/original_strict_4_of_13.junit.xml" 2>&1 | tee "$OUT/original_strict_4_of_13.log"
status=${PIPESTATUS[0]}
set -e
if [ "$status" -ne 1 ]; then
  echo "ORIGINAL_STRICT_UNEXPECTED_EXIT=$status" >&2
  exit 4
fi
echo "ORIGINAL_STRICT_EXIT=1_EXPECTED_4_PASS_9_FAIL" | tee "$OUT/original_strict_exit.log"
