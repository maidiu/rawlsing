#!/bin/bash
# Historical command record. Requires the full corrected snapshot; see
# ../snapshot/README.md and re-extract target 06e88 before rerunning.
set -u
ROOT="/Users/matthewsmith/Desktop/ANVIL_ARCHITECTURE_EXECUTION_20261117/INDEPENDENT_C/WORKER_RETURNS/ANVIL_ARCHITECTURE_C_20261117/R2_RECHECK"
SNAP="$ROOT/snapshot/WORKER_RETURNS/ANVIL_ARCHITECTURE_20261117"
GUARD="$SNAP/GUARDS/v2_supplementary_guard.py"
ACC="/Users/matthewsmith/Desktop/ANVIL_ARCHITECTURE_EXECUTION_20261117/ACCEPTED_INSTRUMENT/ANVIL_R7/tools/r7_integrated.py"
ZIP="/Users/matthewsmith/Desktop/ANVIL_R7_INTEGRATED_WORKFLOW_FIX_20261117.zip"
run() {
  name="$1"; dec="$2"; add="$3"; cw="$4"
  out="$ROOT/RUNS/negative_${name}.txt"
  PYTHONDONTWRITEBYTECODE=1 python3 "$GUARD" --decision "$dec" --addendum "$add" --crosswalk "$cw" \
    --evidence-root "$SNAP" --source-root "$SNAP/SOURCE_118" --repo /Users/matthewsmith/s2b-work/rawlsing --zip "$ZIP" > "$out" 2>&1
  code=$?
  status=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1])).get("status"))' "$out" 2>/dev/null || echo UNPARSEABLE)
  echo -e "${name}\t${code}\t${status}"
}
D="$SNAP/S2_S3/FINAL_DECISION.json"; A="$SNAP/S1/FRAME_V2_ADDENDUM.json"; C="$SNAP/S2_S3/FINAL_OBLIGATION_CROSSWALK.tsv"
N="$ROOT/WITNESS/negatives"
run v2_empty "$N/v2_empty_decision.json" "$N/v2_empty_addendum.json" "$N/v2_empty_crosswalk.tsv"
run stale_pending "$N/stale_pending_decision.json" "$A" "$C"
run stale_sc_estate "$N/stale_sc_estate_decision.json" "$A" "$C"
run unconditional_index "$N/unconditional_index_decision.json" "$A" "$C"
run unconditional_onecert "$N/unconditional_onecert_decision.json" "$A" "$C"
run stale_effect "$N/stale_effect_decision.json" "$A" "$C"
