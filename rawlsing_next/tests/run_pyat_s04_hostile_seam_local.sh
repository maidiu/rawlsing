#!/usr/bin/env bash
# Exact-head S04->FF01 sourcefree hostile seam with inherited S04/FF/C11 suites.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd -P)"
cd "$ROOT"
: "${EXPECTED_S04_SEAM_HEAD:?Set exact 40-character reviewed Git SHA}"
HEAD="$(git rev-parse HEAD)"
if [[ "$HEAD" != "$EXPECTED_S04_SEAM_HEAD" ]]; then
  echo "REFUSED stale or wrong S04 seam HEAD: $HEAD expected $EXPECTED_S04_SEAM_HEAD" >&2
  exit 23
fi
if [[ -n "$(git status --porcelain --untracked-files=no)" ]]; then
  echo "REFUSED dirty tracked source; do not conflate local edits with exact-head proof" >&2
  exit 24
fi
OUT="${PYAT_S04_SEAM_PROOF_DIR:-$ROOT/.pyat-s04-independent-seam-proof}"
mkdir -p "$OUT"
echo "$HEAD" > "$OUT/exact_head.txt"
PYTHON="${PYTHON:-python3}"
"$PYTHON" -B -m compileall -q  rawlsing_next/pre553_s04_observed_research.py  rawlsing_next/pre553_s04_ff01_consumer.py  rawlsing_next/tests/test_pyat1009_ff01_s04_consumer.py
set +e
PYTHONPATH="$ROOT" "$PYTHON" -B -m pytest -q -o addopts='' -p no:cacheprovider  rawlsing_next/tests/test_pyat1009_ff01_s04_consumer.py  rawlsing_next/tests/test_pre553_s04_observed_research.py  rawlsing_next/tests/test_pre553_s04_i05_reception.py  rawlsing_next/tests/test_pre553_s04_ff01_read_conservation.py  rawlsing_next/tests/test_pyat1009_ff01_generic_ingress.py  rawlsing_next/tests/test_pyat1009_ff01_observed_research.py  rawlsing_next/tests/test_pyat1009_ff01_i05_role_ingress.py  rawlsing_next/tests/test_pyat1009_ff01_n10e_crossread.py  rawlsing_next/tests/test_pyat1009_ff01_cold_direct_estate.py  rawlsing_next/tests/test_pre553_direct_estate_i03.py  rawlsing_next/tests/test_pre553_empirical_query.py  rawlsing_next/tests/test_pre553_discovery_exact.py  rawlsing_next/tests/test_pre553_empirical_possibility_provider.py  rawlsing_next/tests/test_field_forge_conditional_support.py  --junitxml="$OUT/junit.xml" 2>&1 | tee "$OUT/pytest.log"
result=${PIPESTATUS[0]}
set -e
printf '%s\n' "$result" > "$OUT/exitcode"
echo "S04_SOURCEFREE_EXIT=$result; proof=$OUT"
echo "No original source or production/scientific/actor authority inferred."
exit "$result"
