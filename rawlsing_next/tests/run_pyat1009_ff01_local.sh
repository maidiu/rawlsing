#!/usr/bin/env bash
# PYAT #1009 sourcefree author-candidate test runner.
# Usage: bash rawlsing_next/tests/run_pyat1009_ff01_local.sh
# This is NOT independent G5 or source/native/scientific certification.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd -P)"
cd "$ROOT"
PYTHON="${PYTHON:-python3}"
OUT="${PYAT1009_PROOF_DIR:-${ROOT}/.pyat1009-local-proof}"
mkdir -p "$OUT"
printf 'PYAT #1009 code HEAD: '; git rev-parse HEAD
printf 'Current branch: '; git branch --show-current || true
printf 'Dirty/unreviewed paths:\n'; git status --short || true
"$PYTHON" --version
"$PYTHON" - <<'PY'
import importlib.util
missing = [name for name in ("pytest", "pyarrow", "duckdb", "pandas", "pyreadstat")
           if importlib.util.find_spec(name) is None]
if missing:
    raise SystemExit("Missing: " + ", ".join(missing) +
                     "\nInstall with: python3 -m pip install pytest pandas pyreadstat pyarrow duckdb")
print("Sourcefree test dependencies importable")
PY
files=(
  rawlsing_next/tests/test_pyat1009_ff01_generic_ingress.py
  rawlsing_next/tests/test_pyat1009_ff01_observed_research.py
  rawlsing_next/tests/test_pyat1009_ff01_i05_role_ingress.py
  rawlsing_next/tests/test_pyat1009_ff01_n10e_crossread.py
  rawlsing_next/tests/test_pyat1009_ff01_cold_direct_estate.py
)
if [[ "${PYAT1009_NEW_ONLY:-0}" != "1" ]]; then
  files+=(
    rawlsing_next/tests/test_pre553_empirical_query.py
    rawlsing_next/tests/test_pre553_discovery_exact.py
    rawlsing_next/tests/test_pre553_empirical_possibility_provider.py
    rawlsing_next/tests/test_pre553_direct_estate_i03.py
    rawlsing_next/tests/test_field_forge_conditional_support.py
  )
fi
printf 'Executing %s test suites.\n' "${#files[@]}"
date -u '+Start UTC: %Y-%m-%dT%H:%M:%SZ'
set +e
PYTHONPATH="$ROOT" "$PYTHON" -B -m pytest \
  -q -o addopts='' -p no:cacheprovider \
  "${files[@]}" \
  --junitxml="${OUT}/pytest.xml" 2>&1 | tee "${OUT}/pytest.log"
rc=${PIPESTATUS[0]}
set -e
date -u '+End UTC: %Y-%m-%dT%H:%M:%SZ'
printf '%s\n' "$rc" > "${OUT}/pytest.exitcode"
git rev-parse HEAD > "${OUT}/git_head.txt"
printf 'Test exit code: %s\n' "$rc"
printf 'Proof log: %s\n' "${OUT}/pytest.log"
printf 'JUnit: %s\n' "${OUT}/pytest.xml"
printf 'AUTHOR LOCAL PROOF ONLY — NOT INDEPENDENT G5, NATIVE SURVEY, SCIENCE, OR PROTECTED RECEIVING.\n'
exit "$rc"
