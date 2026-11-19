#!/usr/bin/env bash
# Sourcefree compatibility at a local Codex C11 HEAD. Never modifies owner worktrees.
# Usage from a Rawlsing checkout:
#   bash rawlsing_next/tests/check_pyat1009_against_c11_head.sh b3dd74916
set -euo pipefail
ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"
C11_REF="${1:-b3dd74916}"
CODE_REF="${PYAT1009_CANDIDATE_REF:-HEAD}"
ANVIL="68aa7cac7cce7057fefd458ef4a06bec2dede1b2"
BASE="aab22c22c9e282ff40f970cdedab7ddfb39ecd7a"
OUT="${PYAT1009_COMPAT_OUT:-$ROOT/.pyat1009-c11-compat-proof}"
mkdir -p "$OUT"
for ref in "$C11_REF" "$CODE_REF" "$ANVIL" "$BASE"; do
  if ! git cat-file -e "$ref^{commit}" 2>/dev/null; then
    echo "HOLD_LOCAL_COMMIT_NOT_FOUND: $ref"
    echo "Obtain exact full SHA and a locally available commit. No stale substitution."
    exit 12
  fi
done
C11="$(git rev-parse "$C11_REF^{commit}")"
CODE="$(git rev-parse "$CODE_REF^{commit}")"
printf '%s\n' "$C11" > "$OUT/c11_head.txt"
printf '%s\n' "$CODE" > "$OUT/code_head.txt"
echo "Exact C11: $C11"
echo "Exact code: $CODE"
if ! git merge-base --is-ancestor "$ANVIL" "$C11"; then
  echo "HOLD_ANCESTRY: C11 does not descend from accepted ANVIL sourcefree."
  exit 13
fi
if ! git merge-base --is-ancestor "$BASE" "$CODE"; then
  echo "HOLD_CODE_ANCESTRY: code is not based on frozen ANVIL candidate."
  exit 14
fi
files=(
  .github/workflows/pyat1009-generic-ff01-sourcefree.yml
  rawlsing_next/field_forge_generic_empirical_ingress.py
  rawlsing_next/field_forge_observed_research.py
  rawlsing_next/field_forge_i05_role_ingress.py
  rawlsing_next/field_forge_n10e_crossread.py
  rawlsing_next/tests/run_pyat1009_ff01_local.sh
  rawlsing_next/tests/check_pyat1009_against_c11_head.sh
  rawlsing_next/tests/test_pyat1009_ff01_generic_ingress.py
  rawlsing_next/tests/test_pyat1009_ff01_observed_research.py
  rawlsing_next/tests/test_pyat1009_ff01_i05_role_ingress.py
  rawlsing_next/tests/test_pyat1009_ff01_n10e_crossread.py
  rawlsing_next/tests/test_pyat1009_ff01_cold_direct_estate.py
)
for file in "${files[@]}"; do
  if git cat-file -e "$C11:$file" 2>/dev/null; then
    echo "HOLD_OVERLAP_WITH_C11: $file"
    exit 15
  fi
  if git cat-file -e "$BASE:$file" 2>/dev/null; then
    echo "HOLD_NOT_ADDITIVE_TO_BASE: $file"
    exit 16
  fi
  if ! git cat-file -e "$CODE:$file" 2>/dev/null; then
    echo "HOLD_MISSING_CANDIDATE_FILE: $file"
    exit 17
  fi
done
echo "Changed upstream contracts relative to this PR's ANVIL base:"
git diff --name-status "$BASE" "$C11" -- \
  rawlsing_next/pre553_source_direct_parquet_estate.py \
  rawlsing_next/pre553_direct_estate_i03.py \
  rawlsing_next/pre553_empirical_query.py \
  rawlsing_next/_pre553_query_eval.py \
  rawlsing_next/pre553_empirical_objects.py \
  rawlsing_next/pre553_c11_ingest.py \
  rawlsing_next/pre553_c11_repository.py \
  rawlsing_next/pre553_batch_runner.py \
  rawlsing_next/pre553_discovery_exact.py \
  rawlsing_next/pre553_analytical_composition.py \
  rawlsing_next/pre553_empirical_possibility_provider.py | tee "$OUT/changed_source_contract_paths.txt"

TEMP="$(mktemp -d "${TMPDIR:-/tmp}/pyat1009-compat-XXXXXX")"
WT="$TEMP/code"
cleanup() {
  if [[ -e "$WT/.git" ]]; then
    git -C "$ROOT" worktree remove --force "$WT" || true
  fi
  rm -rf "$TEMP"
}
trap cleanup EXIT
git worktree add --detach "$WT" "$C11"
for file in "${files[@]}"; do
  mkdir -p "$WT/$(dirname "$file")"
  git show "$CODE:$file" > "$WT/$file"
done
echo "Only candidate NEW files overlay exact C11 worktree. Existing C11 bytes unchanged."
mkdir -p "$OUT/execution"
set +e
(
 cd "$WT"
 PYAT1009_PROOF_DIR="$OUT/execution" \
 PYTHON="${PYTHON:-python3}" bash rawlsing_next/tests/run_pyat1009_ff01_local.sh
)
status=$?
set -e
printf '%s\n' "$status" > "$OUT/compat.exitcode"
if [[ "$status" -ne 0 ]]; then
  echo "COMPATIBILITY_NOT_PROVEN: exit $status"
  exit "$status"
fi
echo "LOCAL_SOURCEFREE_OVERLAY_PASSED — not independent G5, source-native or protected CAS."
echo "Evidence: $OUT"
