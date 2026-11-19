#!/usr/bin/env bash
# Test sourcefree full-stack I03→S04/FF01 additive code on Codex ANVIL 00eb C11.
# This is a nonmutating sourcefree experiment, not a merge or original-source grant.
# bash rawlsing_next/tests/check_pyat_s04_cold_against_codex.sh 00ebc4a162e27a310b89c9a54e251fe063c7ee60 <CODE_SHA>
set -euo pipefail
ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"
C11_REF="${1:-00ebc4a162e27a310b89c9a54e251fe063c7ee60}"
CODE_REF="${2:-HEAD}"
OUT="${PYAT_1097_ANVIL_COMPAT_PROOF_DIR:-$ROOT/.pyat1097-anvil-00eb-proof}"
mkdir -p "$OUT"
for wanted in "$C11_REF" "$CODE_REF"; do
  if ! git cat-file -e "$wanted^{commit}" 2>/dev/null; then
    echo "HOLD_UNRESOLVED_EXACT_CODEX_OR_S04_HEAD: $wanted" >&2
    exit 12
  fi
done
C11="$(git rev-parse "$C11_REF^{commit}")"
CODE="$(git rev-parse "$CODE_REF^{commit}")"
printf '%s\n' "$C11" > "$OUT/exact_codex_c11_head.txt"
printf '%s\n' "$CODE" > "$OUT/exact_additive_s04_code_head.txt"
printf 'Native Codex C11 HEAD: %s\nAdditive S04 code HEAD: %s\n' "$C11" "$CODE"
# Frozen review candidates: all are NEW to Codex's original-witness branch.
# None may silently overwrite a native C11 source decoder/query/physical owner.
files=(
  rawlsing_next/field_forge_generic_empirical_ingress.py
  rawlsing_next/field_forge_i05_role_ingress.py
  rawlsing_next/field_forge_n10e_crossread.py
  rawlsing_next/field_forge_observed_research.py
  rawlsing_next/pre553_s04_observed_research.py
  rawlsing_next/pre553_s04_i05_reception.py
  rawlsing_next/pre553_s04_ff01_consumer.py
  rawlsing_next/pre553_s04_cold_custody.py
  rawlsing_next/pre553_s04_research_batch.py
  rawlsing_next/pre553_s04_first_consumer.py
  rawlsing_next/pre553_distinct_cold_i03_batch.py
  rawlsing_next/pre553_distinct_cold_s04_batch.py
  rawlsing_next/pre553_s04_general_joint_algebra.py
  rawlsing_next/pre553_s04_dynamic_research.py
  rawlsing_next/pre553_interpretation_qualification.py
  rawlsing_next/tests/test_pre553_interpretation_qualification.py
  rawlsing_next/tests/test_pre553_interpretation_native_replay.py
  rawlsing_next/tests/test_pre553_s04_observed_research.py
  rawlsing_next/tests/test_pre553_s04_i05_reception.py
  rawlsing_next/tests/test_pre553_s04_ff01_read_conservation.py
  rawlsing_next/tests/test_pyat1009_ff01_generic_ingress.py
  rawlsing_next/tests/test_pyat1009_ff01_observed_research.py
  rawlsing_next/tests/test_pyat1009_ff01_i05_role_ingress.py
  rawlsing_next/tests/test_pyat1009_ff01_n10e_crossread.py
  rawlsing_next/tests/test_pyat1009_ff01_cold_direct_estate.py
  rawlsing_next/tests/test_pyat1009_ff01_s04_consumer.py
  rawlsing_next/tests/test_pre553_s04_cold_custody.py
  rawlsing_next/tests/test_pre553_s04_research_batch.py
  rawlsing_next/tests/test_pre553_s04_first_consumer.py
  rawlsing_next/tests/test_pyat1097_held_integrity_and_i05.py
  rawlsing_next/tests/test_pre553_distinct_cold_i03_batch.py
  rawlsing_next/tests/test_pre553_distinct_cold_s04_batch.py
  rawlsing_next/tests/test_pre553_s04_general_joint_algebra.py
  rawlsing_next/tests/test_pre553_s04_dynamic_research.py
  rawlsing_next/tests/test_pyat1155_hostile_supported_risk.py
  rawlsing_next/tests/run_pyat1097_fullstack_review_local.sh
)
# The author/sourcefree runner is allowed to grow. A new test which
# only exists at CODE and is absent from the frozen Codex native tree
# MUST be overlaid, otherwise this compatibility court would RED due to
# a missing test rather than testing actual native-C11 compatibility.
runner_tests="$(git show "$CODE:rawlsing_next/tests/run_pyat1097_fullstack_review_local.sh" | awk '
  /^tests=\($/ { in_tests=1; next }
  in_tests && /^\)/ { exit }
  in_tests && /^[[:space:]]+rawlsing_next\/tests\// {
    gsub(/^[[:space:]]+|[[:space:]]+$/, "", $0); print
  }
')"
if [[ -z "$runner_tests" ]]; then
  echo "HOLD_NO_EXECUTABLE_TEST_SELECTION_AT_CODE_HEAD" >&2
  exit 16
fi
while IFS= read -r test_file; do
  if git cat-file -e "$C11:$test_file" 2>/dev/null; then
    continue
  fi
  found=0
  for file in "${files[@]}"; do
    if [[ "$file" == "$test_file" ]]; then
      found=1
      break
    fi
  done
  if [[ "$found" != 1 ]]; then
    echo "HOLD_RUNNER_TEST_MISSING_FROM_ADDITIVE_OVERLAY: $test_file" >&2
    exit 17
  fi
done <<< "$runner_tests"

for file in "${files[@]}"; do
  if git cat-file -e "$C11:$file" 2>/dev/null; then
    echo "HOLD_SOURCE_OVERLAP_WITH_CODEX_NATIVE: $file" >&2
    exit 13
  fi
  if ! git cat-file -e "$CODE:$file" 2>/dev/null; then
    echo "HOLD_ADDITIVE_CODE_PATH_MISSING_AT_EXACT_HEAD: $file" >&2
    exit 14
  fi
done
git diff --name-status "$C11" "$CODE" -- \
  rawlsing_next/_pre553_query_common.py \
  rawlsing_next/_pre553_query_eval.py \
  rawlsing_next/pre553_direct_estate_i03.py \
  rawlsing_next/pre553_c11_repository.py \
  rawlsing_next/pre553_c11_ingest.py \
  rawlsing_next/pre553_source_direct_parquet_estate.py \
  | tee "$OUT/differing_native_c11_paths.txt"
TEMP="$(mktemp -d "${TMPDIR:-/tmp}/pyat-s04-cold-codex-XXXXXX")"
WT="$TEMP/codex"
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
  # Compare all overlay bytes back against their pinned source without relying
  # on Git tracked status (the overlay files are intentionally untracked).
  if ! git show "$CODE:$file" | cmp -s - "$WT/$file"; then
    echo "HOLD_OVERLAY_BYTES_DO_NOT_MATCH_FROZEN_CANDIDATE: $file" >&2
    exit 15
  fi
done
printf '%s\n' "EXACT_ADDITIVE_OVERLAY_BYTES_MATCH_CODE_SHA" > "$OUT/overlay_grade.txt"
echo "Codex native files unchanged. Code added only in previously absent paths."
set +e
(
  cd "$WT"
  EXPECTED_PYAT_1097_REVIEW_HEAD="$C11" \
  PYAT_1097_REVIEW_PROOF_DIR="$OUT/execution" \
  PYTHON="${PYTHON:-python3}" \
    bash rawlsing_next/tests/run_pyat1097_fullstack_review_local.sh
)
result=$?
set -e
printf '%s\n' "$result" > "$OUT/overlay_exitcode"
if [[ "$result" -ne 0 ]]; then
  echo "CODEX_S04_SOURCEFREE_OVERLAY_RED=$result"
  exit "$result"
fi
echo "CODEX_S04_SOURCEFREE_OVERLAY_GREEN — NO SRC16 ANALYSIS LICENSE; NOT NATIVE ORIGINAL SOURCE OR SCIENCE/G5 ACCEPTANCE"
echo "Evidence: $OUT"
