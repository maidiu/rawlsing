#!/usr/bin/env bash
# C7 actual Sorok R4 two-checkout sourcefree first-consumer court.
# Does not fetch, write protected sources or process original surveys.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
: "${EXPECTED_PREFF_C0_HEAD:?Pin exact C7 code HEAD}"
: "${EXPECTED_C7_R4_HEAD:?Pin independent R4 source HEAD}"
HEAD="$(git rev-parse HEAD)"
if [[ "$HEAD" != "$EXPECTED_PREFF_C0_HEAD" ]]; then
  echo "HOLD_C7_C6_HEAD_CHANGED: $HEAD" >&2; exit 23
fi
if [[ -n "$(git status --porcelain --untracked-files=no)" ]]; then
  echo "HOLD_C7_DIRTY_SOURCE_TREE" >&2; exit 24
fi
R4_FIXED=7bff10db7adb7b17bcf035a27561ea59e9a3b2be
if [[ "$EXPECTED_C7_R4_HEAD" != "$R4_FIXED" ]]; then
  echo "HOLD_C7_R4_SOURCE_VERSION_NOT_AUDITED: $EXPECTED_C7_R4_HEAD" >&2
  exit 25
fi
if ! git cat-file -e "$R4_FIXED^{commit}" 2>/dev/null; then
  echo "HOLD_C7_R4_GIT_COMMIT_NOT_FETCHED: fetch origin pull/1174/head first" >&2
  exit 26
fi
OUT="${PREFF_PROOF_DIR:-$PWD/.pyat-preff-c7-proof/$HEAD}"
mkdir -p "$OUT"
printf '%s\n' "$HEAD" > "$OUT/pyat_c7_head.txt"
printf '%s\n' "$R4_FIXED" > "$OUT/sorok_r4_source_head.txt"
tmp="$(mktemp -d "${TMPDIR:-/tmp}/pyat-c7-r4.XXXXXXXX")"
trap 'rm -rf "$tmp"' EXIT
git archive "$R4_FIXED" \
  SEAM/ORACLE/UM_SOROK_ORGANISM_R4_LIVED_GENESIS/um_sorok_organism/ |
  tar -xf - -C "$tmp"
PKG="$tmp/SEAM/ORACLE/UM_SOROK_ORGANISM_R4_LIVED_GENESIS/um_sorok_organism"
if [[ ! -f "$PKG/runtime.py" ]]; then
  echo "HOLD_C7_R4_SOURCE_PACKAGE_ARCHIVE_MISSING" >&2
  exit 27
fi
printf '%s\n' "$PKG" > "$OUT/temporary_r4_package_path.txt"
date -u '+%Y-%m-%dT%H:%M:%SZ' > "$OUT/start_utc.txt"
set +e
PYAT_C7_R4_PACKAGE_DIR="$PKG" PYTHONDONTWRITEBYTECODE=1 \
"${PYTHON:-python3}" -B -m pytest \
  -q -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_preff_c7_actual_r4_world_bridge.py \
  --junitxml="$OUT/junit.xml" 2>&1 | tee "$OUT/pytest.log"
STATUS=${PIPESTATUS[0]}
set -e
printf '%s\n' "$STATUS" > "$OUT/exitcode.txt"
date -u '+%Y-%m-%dT%H:%M:%SZ' > "$OUT/end_utc.txt"
echo "C7_REAL_R4_SOURCEFREE_EXIT_$STATUS C7=$HEAD R4=$R4_FIXED PROOF=$OUT"
echo "RESEARCH ACTOR WORLD ONLY. NOT PROTECTED SOROK, ORIGINAL SURVEY, G5 OR NATIVE PERSON"
exit "$STATUS"
