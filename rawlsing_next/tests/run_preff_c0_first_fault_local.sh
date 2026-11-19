#!/usr/bin/env bash
# PRE-FIELD-FORGE FIRST-FAULT SOURCEFREE COURTS.
# One integration line, no original survey reads or test-backend bakeoffs.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
: "${EXPECTED_PREFF_C0_HEAD:?Pin exact candidate SHA}"
HEAD_SHA="$(git rev-parse HEAD)"
if [[ "$HEAD_SHA" != "$EXPECTED_PREFF_C0_HEAD" ]]; then
  echo "HOLD_STALE_PREFF_C0_HEAD: $HEAD_SHA" >&2; exit 23
fi
if [[ -n "$(git status --porcelain --untracked-files=no)" ]]; then
  echo "HOLD_TRACKED_TREE_DIRTY" >&2; exit 24
fi
COURT="${PREFF_COURT:-C0_ALL_SMALL}"
OUT="${PREFF_PROOF_DIR:-$PWD/.pyat-preff-c0-proof/$COURT}"
mkdir -p "$OUT"
printf '%s\n' "$HEAD_SHA" > "$OUT/exact_head.txt"
printf '%s\n' "$COURT" > "$OUT/court.txt"
date -u '+%Y-%m-%dT%H:%M:%SZ' > "$OUT/start_utc.txt"
case "$COURT" in
  C0_PHYSICAL)
    tests=(rawlsing_next/tests/test_preff_c0_raw_preservation.py
           rawlsing_next/tests/test_pyat960_s1e_source_i02.py)
    ;;
  C1_PREDICATE_I05)
    tests=(rawlsing_next/tests/test_preff_c0_interpretation_seams.py
           rawlsing_next/tests/test_pre553_discovery_exact.py)
    ;;
  C1_SAVED_BATCH)
    tests=(rawlsing_next/tests/test_anvil_prepared_saved_batch_cut1.py
           rawlsing_next/tests/test_anvil_prepared_saved_postconsumer_join.py)
    ;;
  C3_DHIKR_FF01)
    tests=(rawlsing_next/tests/test_preff_c0_dhikr_first_consumer.py
           rawlsing_next/tests/test_pyat1009_ff01_i05_role_ingress.py
           rawlsing_next/tests/test_pre553_s04_i05_reception.py)
    ;;
  C0_ALL_SMALL)
    tests=(rawlsing_next/tests/test_preff_c0_raw_preservation.py
           rawlsing_next/tests/test_preff_c0_interpretation_seams.py
           rawlsing_next/tests/test_preff_c0_dhikr_first_consumer.py
           rawlsing_next/tests/test_pyat960_s1e_source_i02.py
           rawlsing_next/tests/test_pre553_discovery_exact.py
           rawlsing_next/tests/test_anvil_prepared_saved_batch_cut1.py
           rawlsing_next/tests/test_anvil_prepared_saved_postconsumer_join.py
           rawlsing_next/tests/test_pre553_s04_i05_reception.py)
    ;;
  *)
    echo "UNKNOWN_FIRST_FAULT_COURT: $COURT" >&2; exit 2
    ;;
esac
set +e
PYTHONDONTWRITEBYTECODE=1 "${PYTHON:-python3}" -B -m pytest \
  -q -o addopts='' -p no:cacheprovider \
  "${tests[@]}" --junitxml="$OUT/junit.xml" 2>&1 | tee "$OUT/pytest.log"
CODE=${PIPESTATUS[0]}
set -e
printf '%s\n' "$CODE" > "$OUT/exitcode"
date -u '+%Y-%m-%dT%H:%M:%SZ' > "$OUT/end_utc.txt"
echo "PREFF_C0_${COURT}_EXIT_${CODE}; exact_head=$HEAD_SHA; proof=$OUT"
echo "AUTHOR SOURCEFREE ONLY — NOT ORIGINAL SOURCE, G5 OR PROTECTED CAS"
exit "$CODE"
