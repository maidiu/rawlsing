#!/usr/bin/env bash
set -euo pipefail

if command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="$(command -v python3)"
elif command -v python >/dev/null 2>&1; then
  PYTHON_BIN="$(command -v python)"
else
  echo "FIABC_MEASURED_SIX_CELL_BLOCKED: Python 3 interpreter not found (tried python3, python)" >&2
  exit 2
fi
"$PYTHON_BIN" -c 'import sys; raise SystemExit(0 if sys.version_info.major == 3 else 2)' || {
  echo "FIABC_MEASURED_SIX_CELL_BLOCKED: selected interpreter is not Python 3: $PYTHON_BIN" >&2
  exit 2
}
readonly PYTHON_BIN
QUALIFIED_CODE_HEAD="6e2b817c80fc8745354e4a54103ba97a04c4437d"
QUALIFICATION_CLOSURE_HEAD="cbda295ec2e265709f1634b643e27abf704582d3"
EXPECTED_BRANCH="agent/rabochii-prev3-ee-p2x-final-abc-equal-work-execution-r1"

: "${LITS_PATH:?set LITS_PATH}"
: "${WVS_PATH:?set WVS_PATH}"
: "${WORK_ROOT:?set WORK_ROOT}"

git merge-base --is-ancestor "$QUALIFIED_CODE_HEAD" HEAD || { echo "green-qualified code head $QUALIFIED_CODE_HEAD is not an ancestor of HEAD" >&2; exit 2; }
git merge-base --is-ancestor "$QUALIFICATION_CLOSURE_HEAD" HEAD || { echo "qualification closure head $QUALIFICATION_CLOSURE_HEAD is not an ancestor of HEAD" >&2; exit 2; }
unexpected="$(
  git diff --name-only "$QUALIFIED_CODE_HEAD"..HEAD \
    | grep -Ev '^(WORKER_RETURNS/FIABC-CANONICAL-TERMINAL-READINESS-R1/|WORKER_RETURNS/FIABC-FINAL-LAUNCH-FANIN-R1/)' \
    || true
)"
if [[ -n "$unexpected" ]]; then
  echo "non-qualified code changed after green source-free head $QUALIFIED_CODE_HEAD:" >&2
  printf '%s\n' "$unexpected" >&2
  exit 2
fi
[[ "$(git branch --show-current)" == "$EXPECTED_BRANCH" ]] || { echo "wrong branch: expected $EXPECTED_BRANCH" >&2; exit 2; }
[[ -z "$(git status --porcelain)" ]] || { echo "dirty worktree" >&2; exit 2; }

FROZEN_UPSTREAM_RECEIPT="$WORK_ROOT/court/t3/frozen-upstream.json"
SUCCESSION_PREFLIGHT_RECEIPT="$WORK_ROOT/court/fiabc_t5_succession_preflight.json"

test -f "$FROZEN_UPSTREAM_RECEIPT"
test -f "$SUCCESSION_PREFLIGHT_RECEIPT"

"$PYTHON_BIN" rawlsing_next/ee_p2x_darwin_court_driver.py \
  --run \
  --continuation-map WORKER_RETURNS/FIABC-T2/01_SIX_CELL_EXECUTION_MANIFEST.json \
  --current-court-contract WORKER_RETURNS/FIABC-T5/04_CURRENT_SIX_CELL_COURT_CONTRACT.json \
  --succession-preflight-receipt "$SUCCESSION_PREFLIGHT_RECEIPT" \
  --frozen-upstream-receipt "$FROZEN_UPSTREAM_RECEIPT" \
  --backend-module rawlsing_next.ee_p2x_process_isolated_backend \
  --work-root "$WORK_ROOT" \
  --repo-root "$PWD" \
  --lits-path "$LITS_PATH" \
  --wvs-path "$WVS_PATH"
