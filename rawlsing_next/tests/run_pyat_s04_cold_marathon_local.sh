#!/usr/bin/env bash
# Exact HEAD, sourcefree S04 cold-preimage custody + batch + inherited consumers.
# EXPECTED_PYAT_S04_COLD_HEAD=<sha> bash rawlsing_next/tests/run_pyat_s04_cold_marathon_local.sh
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd -P)"
cd "$ROOT"
: "${EXPECTED_PYAT_S04_COLD_HEAD:?Supply exact reviewed 40-character commit}"
HEAD="$(git rev-parse HEAD)"
if [[ "$HEAD" != "$EXPECTED_PYAT_S04_COLD_HEAD" ]]; then
  echo "REFUSED_STALE_HEAD: $HEAD != $EXPECTED_PYAT_S04_COLD_HEAD" >&2
  exit 23
fi
if [[ -n "$(git status --porcelain --untracked-files=no)" ]]; then
  echo "REFUSED_DIRTY_TRACKED_SOURCE; use a fresh detached test worktree" >&2
  exit 24
fi
PYTHON="${PYTHON:-python3}"
OUT="${PYAT_S04_COLD_PROOF_DIR:-$ROOT/.pyat-s04-cold-proof}"
mkdir -p "$OUT"
printf '%s\n' "$HEAD" > "$OUT/exact_head.txt"
git status --short > "$OUT/untracked_and_dirty_paths.txt"
"$PYTHON" --version > "$OUT/python_version.txt" 2>&1
date -u '+%Y-%m-%dT%H:%M:%SZ' > "$OUT/start_utc.txt"
printf 'Exact code HEAD: %s\n' "$HEAD"
echo "SOURCEFREE only; no original survey or new scientific estimand."
"$PYTHON" -B -m compileall -q \
  rawlsing_next/pre553_s04_cold_custody.py \
  rawlsing_next/pre553_s04_research_batch.py \
  rawlsing_next/pre553_s04_first_consumer.py \
  rawlsing_next/tests/test_pre553_s04_cold_custody.py \
  rawlsing_next/tests/test_pre553_s04_research_batch.py \
  rawlsing_next/tests/test_pre553_s04_first_consumer.py
tests=(
  rawlsing_next/tests/test_pre553_s04_cold_custody.py
  rawlsing_next/tests/test_pre553_s04_research_batch.py
  rawlsing_next/tests/test_pre553_s04_first_consumer.py
)
if [[ "${PYAT_S04_COLD_NEW_ONLY:-0}" != "1" ]]; then
  tests+=(
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
fi
set +e
PYTHONPATH="$ROOT" "$PYTHON" -B -m pytest -q \
  -o addopts='' -p no:cacheprovider "${tests[@]}" \
  --junitxml="$OUT/junit.xml" 2>&1 | tee "$OUT/pytest.log"
code=${PIPESTATUS[0]}
set -e
printf '%s\n' "$code" > "$OUT/exitcode"
date -u '+%Y-%m-%dT%H:%M:%SZ' > "$OUT/end_utc.txt"
echo "S04_COLD_SOURCEFREE_EXIT=$code; logs=$OUT"
echo "Even PASS is author suite only; independent G5/source rights/science held."
exit "$code"
