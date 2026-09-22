#!/usr/bin/env bash
set -euo pipefail

CODE_HEAD="aa15525750085f4e223d579010688660a9ae1b6b"
EXPECTED_BRANCH="agent/rabochii-prev3-ee-p2x-final-abc-equal-work-execution-r1"

: "${LITS_PATH:?set LITS_PATH to exact canonical LITS-2006-data.dta}"
: "${WVS_PATH:?set WVS_PATH to exact canonical WVS Wave 7.sav}"
: "${WORK_ROOT:?set WORK_ROOT to a fresh isolated court root}"

git merge-base --is-ancestor "$CODE_HEAD" HEAD || { echo "qualified code head $CODE_HEAD is not an ancestor of HEAD" >&2; exit 2; }
if git diff --name-only "$CODE_HEAD"..HEAD | grep -Ev '^WORKER_RETURNS/FIABC-FINAL-LAUNCH-FANIN-R1/' | grep -q .; then
  echo "non-launch-pack code changed after qualified code head $CODE_HEAD" >&2; exit 2
fi
[[ "$(git branch --show-current)" == "$EXPECTED_BRANCH" ]] || { echo "wrong branch" >&2; exit 2; }
[[ -z "$(git status --porcelain)" ]] || { echo "dirty worktree" >&2; exit 2; }

python - <<'PY'
from rawlsing_next.ee_p2x_darwin_court_driver import observe_host, verify_runtime_gate
host=observe_host()
verify_runtime_gate(host)
print("FIABC_LOCK1_RUNTIME_PASS", host)
PY

python - "$LITS_PATH" "$WVS_PATH" <<'PY'
import hashlib, sys
from pathlib import Path
expected={
"LITS_I":"7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09",
"WVS7":"2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d",
}
for source,raw in zip(("LITS_I","WVS7"),sys.argv[1:]):
    path=Path(raw)
    if not path.is_file(): raise SystemExit(f"{source} missing: {path}")
    h=hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(8*1024*1024), b""): h.update(block)
    got=h.hexdigest()
    if got != expected[source]: raise SystemExit(f"{source} SHA mismatch: {got}")
    print("FIABC_SOURCE_SHA_PASS",source,got)
PY

if [[ -e "$WORK_ROOT/ee_p2x_stage_ledger.json" || -e "$WORK_ROOT/cells" ]]; then
  echo "WORK_ROOT already contains court/candidate state; choose a fresh root" >&2
  exit 2
fi
mkdir -p "$WORK_ROOT/court/oracles" "$WORK_ROOT/court/t3"

python -m rawlsing_next.fiabc_final_oracle_freeze_producers standardize-wvs \
  --r1m WORKER_RETURNS/FIABC-LM2-R1M-LOCK2-SUCCESSOR-R16-ORACLE/07_FRESH_WVS_ORACLE.json \
  --output "$WORK_ROOT/court/oracles/WVS7.standard.json" \
  --freeze-sequence 30

python -m rawlsing_next.fiabc_final_oracle_freeze_producers produce-lits \
  --repo-root "$PWD" \
  --source "$LITS_PATH" \
  --work-root "$WORK_ROOT" \
  --output "$WORK_ROOT/court/oracles/LITS_I.standard.json" \
  --freeze-sequence 30

python -m rawlsing_next.fiabc_final_oracle_freeze_producers freeze-t3 \
  --lits-oracle "$WORK_ROOT/court/oracles/LITS_I.standard.json" \
  --wvs-oracle "$WORK_ROOT/court/oracles/WVS7.standard.json" \
  --work-root "$WORK_ROOT" \
  --output "$WORK_ROOT/court/t3/frozen-upstream.json"

HEAD="$(git rev-parse --verify HEAD^{commit})"
SUCCESSION_MANIFEST="$WORK_ROOT/court/fiabc_i07_current_head_succession_manifest.json"
LIFECYCLE_CONTEXT="$WORK_ROOT/court/fiabc_p10_lifecycle_context.json"
SUCCESSION_PRODUCER_RECEIPT="$WORK_ROOT/court/fiabc_i07_p10_producer_receipt.json"

python -m rawlsing_next.fiabc_succession_producer \
  --repo-root "$PWD" \
  --expected-head "$HEAD" \
  --manifest-output "$SUCCESSION_MANIFEST" \
  --lifecycle-output "$LIFECYCLE_CONTEXT" \
  --receipt-output "$SUCCESSION_PRODUCER_RECEIPT"

python -m rawlsing_next.fiabc_succession_preflight \
  --manifest "$SUCCESSION_MANIFEST" \
  --lifecycle-context "$LIFECYCLE_CONTEXT" \
  --repo-root "$PWD" \
  --output "$WORK_ROOT/court/fiabc_i07_direct_preflight.json"

python rawlsing_next/ee_p2x_darwin_court_driver.py \
  --preflight \
  --continuation-map WORKER_RETURNS/FIABC-T2/01_SIX_CELL_EXECUTION_MANIFEST.json \
  --current-court-contract WORKER_RETURNS/FIABC-T5/04_CURRENT_SIX_CELL_COURT_CONTRACT.json \
  --succession-manifest "$SUCCESSION_MANIFEST" \
  --succession-lifecycle-context "$LIFECYCLE_CONTEXT" \
  --work-root "$WORK_ROOT" \
  --repo-root "$PWD" \
  --lits-path "$LITS_PATH" \
  --wvs-path "$WVS_PATH"

test -f "$WORK_ROOT/court/fiabc_t5_succession_preflight.json"
echo "FIABC_PRE_CANDIDATE_PREFLIGHT_GREEN__STOP_BEFORE_CANDIDATES"
echo "FROZEN_UPSTREAM_RECEIPT=$WORK_ROOT/court/t3/frozen-upstream.json"
