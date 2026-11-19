#!/usr/bin/env bash
# Codex acc264 sourcefree joined native PYAT first-consumer qualification.
# ANVIL_JOINED_TREE=/private/exact/patched/runtime \
# EXPECTED_PYAT_INTERPRETATION_HEAD=<sha> \
# bash rawlsing_next/tests/check_pyat_interpretation_against_anvil_acc.sh
set -euo pipefail
ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"
: "${EXPECTED_PYAT_INTERPRETATION_HEAD:?Exact PYAT code SHA required}"
: "${ANVIL_JOINED_TREE:?Codex isolated joined sourcefree runtime required}"
CODE="$(git rev-parse HEAD)"
if [[ "$CODE" != "$EXPECTED_PYAT_INTERPRETATION_HEAD" ]]; then
  echo "HOLD_STALE_EXACT_PYAT_HEAD" >&2; exit 23
fi
if [[ -n "$(git status --porcelain --untracked-files=no)" ]]; then
  echo "HOLD_TRACKED_TREE_DIRTY" >&2; exit 24
fi
ANVIL="$(cd "$ANVIL_JOINED_TREE" && pwd -P)"
if [[ ! -d "$ANVIL/rawlsing_next" ]]; then
  echo "HOLD_ANVIL_JOINED_SOURCEFREE_RUNTIME_MISSING" >&2; exit 12
fi
OUT="${PYAT_ACC_INTERPRETATION_PROOF_DIR:-$ROOT/.pyat-acc-interpretation-proof}"
mkdir -p "$OUT"
printf '%s\n' "$CODE" > "$OUT/exact_pyat_head.txt"
printf '%s\n' "acc264c4bb2af06bd02578776a2831265ef2c432" > "$OUT/codex_return_head.txt"
# Exact corrected native product hashes, from acc264 JOINED_EVIDENCE.json.
native=(
  rawlsing_next/pre553_source_i02_handoff.py
  rawlsing_next/_pre553_query_predicate.py
  rawlsing_next/pre553_discovery_exact.py
  rawlsing_next/pre553_saved_workload_integration.py
)
hashes=(
  c32d62e93ce28354e90fafb3befab97b203bf589d3f05441d4661254bd555514
  7f22f515d541af33e7b529b0635092c69f2555b0ebb284141e3ffededfce7a3e
  4afe821016a77465cdbc7fa6f492fdc93dda6bf78347ad0c7f7c812a7f575830
  efa46bbdf8453674db6c686a65510c90d497893a1b6ec5651a11d76863d2e52f
)
for i in "${!native[@]}"; do
  file="$ANVIL/${native[$i]}"
  if [[ ! -f "$file" ]]; then
    echo "HOLD_JOINED_NATIVE_FILE_MISSING: $file" >&2; exit 13
  fi
  observed="$(shasum -a 256 "$file" | awk '{print $1}')"
  printf '%s %s\n' "$observed" "${native[$i]}" >> "$OUT/native_file_hashes.txt"
  if [[ "$observed" != "${hashes[$i]}" ]]; then
    echo "HOLD_ACC264_NATIVE_FILE_HASH_DRIFT: ${native[$i]}" >&2; exit 14
  fi
done
WORK="$(mktemp -d "${TMPDIR:-/tmp}/pyat-acc264-joined-XXXXXX")"
trap 'rm -rf "$WORK"' EXIT
# Only the sourcefree runtime package is copied, NOT any .sav/original data.
cp -a "$ANVIL/rawlsing_next" "$WORK/rawlsing_next"
# Exact additive PYAT feature and test files. Conflicting existing owner paths
# cause HOLD, never overwritten; the four native Codex files never appear here.
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
)
for file in "${files[@]}"; do
  if ! git cat-file -e "$CODE:$file" 2>/dev/null; then
    echo "HOLD_ADDITIVE_PYAT_PATH_NOT_AT_CODE_SHA: $file" >&2; exit 15
  fi
  mkdir -p "$WORK/$(dirname "$file")"
  if [[ -e "$WORK/$file" ]]; then
    if ! git show "$CODE:$file" | cmp -s - "$WORK/$file"; then
      echo "HOLD_OVERLAP_WITH_CODEX_JOINED_FILE: $file" >&2; exit 16
    fi
  else
    git show "$CODE:$file" > "$WORK/$file"
  fi
done
for i in "${!native[@]}"; do
  observed="$(shasum -a 256 "$WORK/${native[$i]}" | awk '{print $1}')"
  if [[ "$observed" != "${hashes[$i]}" ]]; then
    echo "HOLD_CODEX_NATIVE_BYTES_CHANGED: ${native[$i]}" >&2; exit 17
  fi
done
date -u '+%Y-%m-%dT%H:%M:%SZ' > "$OUT/start_utc.txt"
set +e
(
  cd "$WORK"
  PYTHONPATH="$WORK" "${PYTHON:-python3}" -B -m pytest -q \
    -o addopts='' -p no:cacheprovider \
    rawlsing_next/tests/test_pre553_interpretation_qualification.py \
    rawlsing_next/tests/test_pre553_interpretation_native_replay.py \
    rawlsing_next/tests/test_pre553_s04_observed_research.py \
    rawlsing_next/tests/test_pyat1097_held_integrity_and_i05.py \
    rawlsing_next/tests/test_pyat1009_ff01_generic_ingress.py \
    --junitxml="$OUT/junit.xml"
) 2>&1 | tee "$OUT/pytest.log"
RESULT=${PIPESTATUS[0]}
set -e
printf '%s\n' "$RESULT" > "$OUT/exitcode"
date -u '+%Y-%m-%dT%H:%M:%SZ' > "$OUT/end_utc.txt"
if [[ "$RESULT" -ne 0 ]]; then
  echo "ACC264_PYAT_JOINED_SOURCEFREE_RED=$RESULT"; exit "$RESULT"
fi
echo "ACC264_PYAT_JOINED_SOURCEFREE_GREEN__NOT_NATIVE_ORIGINAL_SOURCE_OR_G5"
echo "Proof: $OUT"
