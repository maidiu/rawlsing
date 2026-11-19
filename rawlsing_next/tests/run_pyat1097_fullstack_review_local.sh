#!/usr/bin/env bash
# Independent sourcefree whole-stack hostile regression, exact HEAD only.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd -P)"
cd "$ROOT"
: "${EXPECTED_PYAT_1097_REVIEW_HEAD:?Supply exact 40-character review commit}"
SHA="$(git rev-parse HEAD)"
if [[ "$SHA" != "$EXPECTED_PYAT_1097_REVIEW_HEAD" ]]; then
  echo "HOLD_WRONG_REVIEW_HEAD: $SHA != $EXPECTED_PYAT_1097_REVIEW_HEAD" >&2
  exit 23
fi
if [[ -n "$(git status --porcelain --untracked-files=no)" ]]; then
  echo "HOLD_DIRTY_TRACKED_TREE: exact-head sourcefree proof requires clean checkout" >&2
  exit 24
fi
PYTHON="${PYTHON:-python3}"
"$PYTHON" - <<'PY'
from importlib.util import find_spec
required = ("pytest", "pyarrow", "duckdb", "pandas", "pyreadstat")
missing = [x for x in required if find_spec(x) is None]
if missing:
    raise SystemExit("HOLD_MISSING_SOURCEFREE_DEPENDENCIES: " + ", ".join(missing))
PY
OUT="${PYAT_1097_REVIEW_PROOF_DIR:-$ROOT/.pyat1097-review-proof}"
mkdir -p "$OUT"
printf '%s\n' "$SHA" > "$OUT/exact_head.txt"
"$PYTHON" --version > "$OUT/python_version.txt" 2>&1
date -u '+%Y-%m-%dT%H:%M:%SZ' > "$OUT/start_utc.txt"
"$PYTHON" -B -m compileall -q \
  rawlsing_next/field_forge_generic_empirical_ingress.py \
  rawlsing_next/field_forge_i05_role_ingress.py \
  rawlsing_next/pre553_s04_observed_research.py \
  rawlsing_next/pre553_distinct_cold_i03_batch.py \
  rawlsing_next/pre553_distinct_cold_s04_batch.py \
  rawlsing_next/pre553_s04_general_joint_algebra.py \
  rawlsing_next/pre553_s04_dynamic_research.py \
  rawlsing_next/tests/test_pyat1097_held_integrity_and_i05.py \
  rawlsing_next/tests/test_pre553_distinct_cold_i03_batch.py \
  rawlsing_next/tests/test_pre553_distinct_cold_s04_batch.py \
  rawlsing_next/tests/test_pre553_s04_general_joint_algebra.py \
  rawlsing_next/tests/test_pre553_s04_dynamic_research.py
tests=(
 rawlsing_next/tests/test_pre553_s04_general_joint_algebra.py
 rawlsing_next/tests/test_pre553_s04_dynamic_research.py
 rawlsing_next/tests/test_pyat1097_held_integrity_and_i05.py
 rawlsing_next/tests/test_pre553_distinct_cold_i03_batch.py
 rawlsing_next/tests/test_pre553_s04_cold_custody.py
 rawlsing_next/tests/test_pre553_s04_research_batch.py
 rawlsing_next/tests/test_pre553_s04_first_consumer.py
 rawlsing_next/tests/test_pyat1009_ff01_s04_consumer.py
 rawlsing_next/tests/test_pre553_s04_observed_research.py
 rawlsing_next/tests/test_pre553_s04_i05_reception.py
 rawlsing_next/tests/test_pre553_s04_ff01_read_conservation.py
 rawlsing_next/tests/test_pyat1009_ff01_generic_ingress.py
 rawlsing_next/tests/test_pyat1009_ff01_observed_research.py
 rawlsing_next/tests/test_pyat1009_ff01_i05_role_ingress.py
 rawlsing_next/tests/test_pyat1009_ff01_n10e_crossread.py
 rawlsing_next/tests/test_pyat1009_ff01_cold_direct_estate.py
 rawlsing_next/tests/test_pre553_direct_estate_i03.py
 rawlsing_next/tests/test_pre553_empirical_query.py
 rawlsing_next/tests/test_pre553_discovery_exact.py
 rawlsing_next/tests/test_pre553_empirical_possibility_provider.py
 rawlsing_next/tests/test_field_forge_conditional_support.py
)
set +e
PYTHONPATH="$ROOT" "$PYTHON" -B -m pytest -q  -o addopts='' -p no:cacheprovider -rs  "${tests[@]}" --junitxml="$OUT/junit.xml" 2>&1 | tee "$OUT/pytest.log"
RESULT=${PIPESTATUS[0]}
set -e
printf '%s\n' "$RESULT" > "$OUT/exitcode"
date -u '+%Y-%m-%dT%H:%M:%SZ' > "$OUT/end_utc.txt"
if [[ "$RESULT" -ne 0 ]]; then
  echo "PYAT1097_SOURCEFREE_RED_EXIT=$RESULT; proof=$OUT"
  exit "$RESULT"
fi
"$PYTHON" - "$OUT/junit.xml" <<'PY'
import sys
from xml.etree import ElementTree as E
r=E.parse(sys.argv[1]).getroot()
suites=[r] if r.tag=="testsuite" else r.findall(".//testsuite")
n=sum(int(s.get("tests","0")) for s in suites)
fail=sum(int(s.get("failures","0"))+int(s.get("errors","0")) for s in suites)
skipped=sum(int(s.get("skipped","0")) for s in suites)
print("PYAT1097_REPORTED",n,"FAILED_OR_ERROR",fail,"SKIPPED",skipped)
if not n or fail or skipped:
    raise SystemExit("HOLD_NOT_FULLY_EXECUTED_SOURCEFREE_COURT")
PY
echo "PYAT1097_EXACT_HEAD_SOURCEFREE_TEST_EXIT_0; proof=$OUT"
echo "No independent G5, 100k/high-width physical pass, original source or scientific rank inferred."
