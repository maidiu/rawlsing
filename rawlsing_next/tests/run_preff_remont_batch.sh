#!/usr/bin/env bash
# PYAT -> REMONT growing sourcefree first-fault execution queue.
# Pure execution/proof collection: no source waves, git writes, or owner promotion.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
: "${EXPECTED_PREFF_C0_HEAD:?Pin exact 40-hex candidate commit SHA before launching}"
HEAD_SHA="$(git rev-parse HEAD)"
if [[ "$HEAD_SHA" != "$EXPECTED_PREFF_C0_HEAD" ]]; then
  echo "HOLD_STALE_REMONT_QUEUE_HEAD: $HEAD_SHA; required $EXPECTED_PREFF_C0_HEAD" >&2
  exit 23
fi
if [[ -n "$(git status --porcelain --untracked-files=no)" ]]; then
  echo "HOLD_TRACKED_TREE_DIRTY__DO_NOT_TEST_UNPINNED_CODE" >&2
  exit 24
fi

# Append new QIDs here and to REMONT_EXECUTION_QUEUE.md, never repurpose an ID.
if (( $# )); then
  cases=("$@")
else
  cases=(RMT-Q001 RMT-Q002 RMT-Q003 RMT-Q004 RMT-Q007)
fi
OUT="${REMONT_PROOF_ROOT:-$PWD/.pyat-preff-remont-proof/$HEAD_SHA}"
mkdir -p "$OUT"
printf '%s\n' "$HEAD_SHA" > "$OUT/exact_head.txt"
date -u '+%Y-%m-%dT%H:%M:%SZ' > "$OUT/start_utc.txt"
printf '%s\n' "case_id,exitcode,report_directory" > "$OUT/index.csv"
failed=0
for id in "${cases[@]}"; do
  tests=()
  case "$id" in
    RMT-Q001)
      tests=(rawlsing_next/tests/test_preff_c3_dhikr_comparative.py)
      ;;
    RMT-Q002)
      tests=(rawlsing_next/tests/test_preff_c0_dhikr_first_consumer.py
             rawlsing_next/tests/test_pyat1009_ff01_i05_role_ingress.py
             rawlsing_next/tests/test_pre553_s04_i05_reception.py)
      ;;
    RMT-Q003)
      tests=(rawlsing_next/tests/test_preff_c4_ff_v3_empirical_handoff.py)
      ;;
    RMT-Q004)
      tests=(rawlsing_next/tests/test_pre553_empirical_objects_authority.py
             rawlsing_next/tests/test_pre553_s04_first_consumer.py
             rawlsing_next/tests/test_pyat1009_ff01_s04_consumer.py
             rawlsing_next/tests/test_pyat1009_ff01_generic_ingress.py
             rawlsing_next/tests/test_pyat1009_ff01_observed_research.py
             rawlsing_next/tests/test_pyat1009_ff01_cold_direct_estate.py)
      ;;
    RMT-Q005)
      ;;
    RMT-Q007) # C5 material sourcefree context navigation and real I05 role
      tests=(rawlsing_next/tests/test_preff_c5_continuing_contextual_prev3.py)
      ;;
    *)
      echo "INVALID_OR_UNCOMMISSIONED_REMONT_CASE: $id" >&2
      exit 2
      ;;
  esac
  dir="$OUT/$id"
  mkdir -p "$dir"
  printf '%s\n' "$id" > "$dir/case_id.txt"
  printf '%s\n' "$HEAD_SHA" > "$dir/exact_head.txt"
  date -u '+%Y-%m-%dT%H:%M:%SZ' > "$dir/start_utc.txt"
  echo "REMONT_EXECUTING $id at $HEAD_SHA"
  set +e
  if [[ "$id" == RMT-Q005 ]]; then
    EXPECTED_PREFF_C0_HEAD="$HEAD_SHA" \
    PREFF_COURT=C0_ALL_SMALL \
    PREFF_PROOF_DIR="$dir/broad_c0" \
    bash rawlsing_next/tests/run_preff_c0_first_fault_local.sh \
      2>&1 | tee "$dir/runner.log"
  else
    PYTHONDONTWRITEBYTECODE=1 "${PYTHON:-python3}" -B -m pytest \
      -q -o addopts='' -p no:cacheprovider "${tests[@]}" \
      --junitxml="$dir/junit.xml" 2>&1 | tee "$dir/pytest.log"
  fi
  code=${PIPESTATUS[0]}
  set -e
  date -u '+%Y-%m-%dT%H:%M:%SZ' > "$dir/end_utc.txt"
  printf '%s\n' "$code" > "$dir/exitcode.txt"
  printf '%s,%s,%s\n' "$id" "$code" "$dir" >> "$OUT/index.csv"
  if [[ "$code" -ne 0 ]]; then failed=$((failed+1)); fi
  echo "REMONT_RESULT $id exit=$code proof=$dir"
done
date -u '+%Y-%m-%dT%H:%M:%SZ' > "$OUT/end_utc.txt"
printf '%s\n' "$failed" > "$OUT/failed_cases.txt"
echo "REMONT_QUEUE completed=${#cases[@]} failed=$failed exact_head=$HEAD_SHA proof=$OUT"
echo "SOURCEFREE AUTHOR/WORKER EXECUTION ONLY; NOT INDEPENDENT G5, ORIGINAL SCIENCE, V3 ACTOR, PROTECTED CAS"
if [[ "$failed" -gt 0 ]]; then exit 1; fi
exit 0
