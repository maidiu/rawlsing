#!/usr/bin/env bash
set -euo pipefail

HERE=$(cd "$(dirname "$0")" && pwd)
RETURN=$(cd "$HERE/.." && pwd)
REPO_ROOT=${REPO_ROOT:-$(git -C "$RETURN" rev-parse --show-toplevel)}
SOURCE_COMMIT=e61a26ce24f023a53d6b116bb9eca2fb7b6f8e65
OUT="$HERE"
WORK=${WORK:-$(mktemp -d "${TMPDIR:-/tmp}/pe-sc0-court.XXXXXX")}
KEEP_WORK=${KEEP_WORK:-0}

cleanup() {
  if [ "$KEEP_WORK" != "1" ]; then
    rm -rf "$WORK"
  fi
}
trap cleanup EXIT

expect_blob() {
  local path=$1 expected=$2 actual
  actual=$(git -C "$REPO_ROOT" hash-object "$path")
  if [ "$actual" != "$expected" ]; then
    echo "BLOB_MISMATCH $path expected=$expected actual=$actual" >&2
    exit 3
  fi
}

git -C "$REPO_ROOT" archive "$SOURCE_COMMIT" rawlsing_next | tar -x -C "$WORK"

expect_blob "$WORK/rawlsing_next/pre553_postastra_pe_generic_world_possibility.py" 58484f4c3d9aae148d4116dcf00420c432aefcbd
expect_blob "$WORK/rawlsing_next/tests/test_hq297_k9k10_sc0_pe_independent.py" d2fe653dadf94893b0fdfd268f36683f8dfed9af
expect_blob "$WORK/rawlsing_next/tests/test_postastra_pe_generic_world_possibility.py" 92f59875583bf513c6fdbcd3ad7fe2b49e45e212
expect_blob "$WORK/rawlsing_next/tests/test_postastra_pe_fixture.py" c9674d5fe9d01621eda0fdb4a999391eba422d92

patch -p1 -d "$WORK" < "$RETURN/candidate/PE_TEST_FIXTURE_AUTHORITY.patch" >/dev/null
expect_blob "$WORK/rawlsing_next/tests/test_postastra_pe_fixture.py" 83984e7b3719f350cb735a9d80b0a83560576a47

cp "$RETURN/candidate/sc0_pe_overlay.py" "$RETURN/candidate/sitecustomize.py" "$WORK/"
cp -R "$RETURN/candidate/port" "$RETURN/candidate/oracles" "$WORK/"

export HQ297_EXACT_PE_ROOT="$WORK"
export PYTHONPATH="$WORK"
export PYTHONDONTWRITEBYTECODE=1
export PYTHONHASHSEED=0

cd "$WORK"
python3 -m pytest -q -p no:cacheprovider rawlsing_next/tests/test_postastra_pe_generic_world_possibility.py \
  --junitxml="$OUT/author_21.junit.xml" 2>&1 | tee "$OUT/author_21.log"
python3 -m pytest -q -p no:cacheprovider rawlsing_next/tests/test_hq297_k9k10_sc0_pe_independent.py \
  --junitxml="$OUT/strict_13.junit.xml" 2>&1 | tee "$OUT/strict_13.log"
python3 -m pytest -q -p no:cacheprovider "$RETURN/tests/test_pe_sc0_overlay_court.py" \
  --junitxml="$OUT/overlay_faults.junit.xml" 2>&1 | tee "$OUT/overlay_faults.log"

echo "COURT_TREE=$WORK" | tee "$OUT/court_tree.log"
echo "PE_BLOB=58484f4c3d9aae148d4116dcf00420c432aefcbd" | tee -a "$OUT/court_tree.log"
echo "FIXTURE_PATCHED_BLOB=83984e7b3719f350cb735a9d80b0a83560576a47" | tee -a "$OUT/court_tree.log"
