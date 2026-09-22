#!/usr/bin/env bash
set -euo pipefail
CODE_HEAD="aa15525750085f4e223d579010688660a9ae1b6b"
EXPECTED_BRANCH="agent/rabochii-prev3-ee-p2x-final-abc-equal-work-execution-r1"

: "${LITS_PATH:?set LITS_PATH}"
: "${WVS_PATH:?set WVS_PATH}"
: "${WORK_ROOT:?set WORK_ROOT}"

git merge-base --is-ancestor "$CODE_HEAD" HEAD || { echo "qualified code head $CODE_HEAD is not an ancestor of HEAD" >&2; exit 2; }
if git diff --name-only "$CODE_HEAD"..HEAD | grep -Ev '^WORKER_RETURNS/FIABC-FINAL-LAUNCH-FANIN-R1/' | grep -q .; then
  echo "non-launch-pack code changed after qualified code head $CODE_HEAD" >&2; exit 2
fi
[[ "$(git branch --show-current)" == "$EXPECTED_BRANCH" ]] || { echo "wrong branch" >&2; exit 2; }
[[ -z "$(git status --porcelain)" ]] || { echo "dirty worktree" >&2; exit 2; }

FROZEN_UPSTREAM_RECEIPT="$WORK_ROOT/court/t3/frozen-upstream.json"
SUCCESSION_PREFLIGHT_RECEIPT="$WORK_ROOT/court/fiabc_t5_succession_preflight.json"

test -f "$FROZEN_UPSTREAM_RECEIPT"
test -f "$SUCCESSION_PREFLIGHT_RECEIPT"

python rawlsing_next/ee_p2x_darwin_court_driver.py \
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
