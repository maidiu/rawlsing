#!/usr/bin/env bash
set -u
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
OUT="$ROOT/evidence/full-vertical-execution-combined"
mkdir -p "$OUT/logs" "$OUT/metrics"
printf 'index\tname\tstatus\texit\tseconds\n' > "$OUT/case_results.tsv"
index=0
while IFS= read -r name; do
  [ -z "$name" ] && continue
  index=$((index + 1))
  id=$(printf '%02d' "$index")
  log="$OUT/logs/${id}_${name}.json"
  start=$(date +%s)
  if [ "$name" = "test_11_resource_receipts_are_actual_measurements" ]; then
    python3 "$ROOT/run_p3_vertical_slice.py" --test "$name" --timeout 600 \
      --metrics-path "evidence/full-vertical-execution-combined/metrics/resource.json" > "$log"
  else
    python3 "$ROOT/run_p3_vertical_slice.py" --test "$name" --timeout 600 > "$log"
  fi
  rc=$?
  end=$(date +%s)
  status=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1])).get("status","UNKNOWN"))' "$log" 2>/dev/null || printf 'UNREADABLE')
  printf '%s\t%s\t%s\t%s\t%s\n' "$id" "$name" "$status" "$rc" "$((end - start))" >> "$OUT/case_results.tsv"
  printf '%s %s %ss\n' "$id" "$status" "$((end - start))"
done <<'CASES'
test_primary_actual_formation_read_later_and_no_mediator_control
test_a_two_histories_change_later_move_without_demographic_labels
test_b_actual_material_opportunity_changes_without_psych_mutation
test_c_two_standpoints_same_history_without_mutation
test_d_incompatible_mediators_coexist_and_activate_without_resolution
test_e_stability_event_reveals_without_new_record
test_f_four_actual_compression_forms_bind_without_fabricated_history
test_g_actor_and_user_views_are_narrower_than_objective_state
test_h_wrong_root_actor_branch_time_source_rule_version_refuse_before_effects
test_h_cross_root_binding_is_refused_not_migrated
test_h_cold_reopen_idempotent_replay_and_source_restore
test_h_real_process_crash_after_base_before_psych_commit
test_11_resource_receipts_are_actual_measurements
CASES
python3 - "$ROOT" "$OUT" <<'PY'
import hashlib
import json
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
out = Path(sys.argv[2])
rows = []
for line in (out / "case_results.tsv").read_text(encoding="utf-8").splitlines()[1:]:
    index, name, status, code, seconds = line.split("\t")
    rows.append({
        "index": int(index),
        "name": name,
        "status": status,
        "exit": int(code),
        "seconds": int(seconds),
    })
files = [
    "run_p3_vertical_slice.py",
    "tests/p3_fixture_support.py",
    "tests/test_p3_vertical_slice.py",
    "p3/state_store.py",
    "p3/p3_owner.py",
    "p3/compression.py",
]
summary = {
    "schema": "SOROK_P3_COMBINED_MATRIX@1",
    "commit": subprocess.check_output(
        ["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip(),
    "cases": rows,
    "passed": sum(1 for row in rows if row["status"] == "PASS"),
    "failed": sum(1 for row in rows if row["status"] != "PASS"),
    "source_sha256": {
        path: hashlib.sha256((root / path).read_bytes()).hexdigest()
        for path in files
    },
    "resource_metrics": str(out / "metrics" / "resource.json"),
}
(out / "matrix_summary.json").write_text(
    json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps(summary, indent=2, sort_keys=True))
PY
