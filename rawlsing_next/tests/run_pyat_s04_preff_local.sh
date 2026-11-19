#!/usr/bin/env bash
# Author-sourcefree S04 pre-Field Forge first read. Not scientific G5.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd -P)"
cd "$ROOT"
PYTHON="${PYTHON:-python3}"
OUT="${PYAT_S04_PROOF_DIR:-$ROOT/.pyat-s04-local-proof}"
mkdir -p "$OUT"
printf 'Current SHA: '; git rev-parse HEAD
printf 'Dirty paths:\n'; git status --short
"$PYTHON" --version
files=(
  rawlsing_next/tests/test_pre553_s04_observed_research.py
  rawlsing_next/tests/test_pre553_s04_i05_reception.py
  rawlsing_next/tests/test_pre553_s04_ff01_read_conservation.py
  rawlsing_next/tests/test_pyat1009_ff01_generic_ingress.py
  rawlsing_next/tests/test_pyat1009_ff01_observed_research.py
  rawlsing_next/tests/test_pyat1009_ff01_i05_role_ingress.py
  rawlsing_next/tests/test_pyat1009_ff01_n10e_crossread.py
  rawlsing_next/tests/test_pyat1009_ff01_cold_direct_estate.py
)
if [[ "${PYAT_S04_FAST:-0}" != "1" ]]; then
  files+=(
    rawlsing_next/tests/test_pre553_empirical_query.py
    rawlsing_next/tests/test_pre553_discovery_exact.py
    rawlsing_next/tests/test_pre553_empirical_possibility_provider.py
    rawlsing_next/tests/test_pre553_direct_estate_i03.py
    rawlsing_next/tests/test_field_forge_conditional_support.py
  )
fi
echo "Running upstream S04, selected F1–F4/I05, and consumer seam sourcefree tests."
set +e
PYTHONPATH="$ROOT" "$PYTHON" -B -m pytest -q \
  -o addopts='' -p no:cacheprovider "${files[@]}" \
  --junitxml="$OUT/pytest.xml" 2>&1 | tee "$OUT/pytest.log"
code=${PIPESTATUS[0]}
set -e
printf '%s\n' "$code" > "$OUT/pytest.exitcode"
git rev-parse HEAD > "$OUT/git_head.txt"
echo "Test exit code: $code; proof: $OUT"
echo "AUTHOR SOURCEFREE TEST ONLY. NOT ORIGINAL-SOURCE/WEIGHTS/INDEPENDENT G5."
exit "$code"
