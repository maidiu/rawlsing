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
  cases=(RMT-Q001 RMT-Q002 RMT-Q003 RMT-Q004 RMT-Q007 RMT-Q008 RMT-Q009 RMT-Q010 RMT-Q013 RMT-Q014 RMT-Q015 RMT-Q016 RMT-Q017 RMT-Q018 RMT-Q019 RMT-Q020)
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
    RMT-Q008) # REMONT P0 ABI parity and historical raw/held negative courts
      tests=(rawlsing_next/tests/test_preff_c1_typed_condition_uncertainty.py
             rawlsing_next/tests/test_preff_c0_raw_preservation.py)
      ;;
    RMT-Q009) # C5 contextual navigation full inherited sourcefree court
      ;;
    RMT-Q010) # C6 V3/SEAM pinned replay, world and pair negative court
      ;;
    RMT-Q013) # 17 PF025 target-absence vs legitimate-empty first-fault checks
      tests=(rawlsing_next/tests/test_preff_c1_target_absence.py)
      ;;
    RMT-Q014) # Exact asked/eligible RAW denominator and source-native nonanswers
      ;; # Reuse existing R03_ASKED_ELIGIBLE court below, never duplicate tests.
    RMT-Q015) # Source-coherent continuing S04/DHIKR adaptive budget and PRE-V3 context
      tests=(rawlsing_next/tests/test_pre553_s04_determinicity_cycle.py)
      ;;
    RMT-Q016) # PR #1207 country-issued source, R03 role, source registry, S04 budget
      tests=(rawlsing_next/tests/test_pre553_s04_country_refinement.py
             rawlsing_next/tests/test_pre553_s04_country_multinational_scope.py
             rawlsing_next/tests/test_pre553_s04_country_r03_v2_issuer.py
             rawlsing_next/tests/test_pre553_source_country_registry_adapter.py)
      ;;
    RMT-Q017) # Country-scoped noise and search-complexity admission
      tests=(rawlsing_next/tests/test_pre553_s04_support_noise_admission.py)
      ;;
    RMT-Q018) # Separately issued finite-frame F6 sharp partial identification
      tests=(rawlsing_next/tests/test_pre553_s04_partially_identified_repertoire.py)
      ;;
    RMT-Q019) # Existing HAQQ source-coherent forward/reverse/position inquiry
      tests=(rawlsing_next/tests/test_pre553_s04_position_repertoire_inquiry.py)
      ;;
    RMT-Q020) # Distinct F6 two-source issued population parameter intervals
      tests=(rawlsing_next/tests/test_pre553_s04_uncertain_repertoire.py
             rawlsing_next/tests/test_pre553_s04_position_repertoire_inquiry.py)
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
  if [[ "$id" == RMT-Q005 || "$id" == RMT-Q009 || "$id" == RMT-Q010 || "$id" == RMT-Q014 ]]; then
    # Reuse the existing exact-head first-fault courts, not duplicated suites.
    court=C0_ALL_SMALL
    case "$id" in
      RMT-Q009) court=C5_V3_CONTEXT ;;
      RMT-Q010) court=C6_V3_SEAM ;;
      RMT-Q014) court=R03_ASKED_ELIGIBLE ;;
    esac
    proof_subdir=court
    if [[ "$id" == RMT-Q005 ]]; then proof_subdir=broad_c0; fi
    EXPECTED_PREFF_C0_HEAD="$HEAD_SHA" \
    PREFF_COURT="$court" \
    PREFF_PROOF_DIR="$dir/$proof_subdir" \
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
