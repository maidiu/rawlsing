#!/usr/bin/env bash
# Exact-head sourcefree economics, separate processes per variant.
# Not original source/native 100k proof, avoids within-process RSS comparison.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd -P)"
cd "$ROOT"
: "${EXPECTED_PYAT_1097_REVIEW_HEAD:?Must pin exact reviewed git commit}"
HEAD="$(git rev-parse HEAD)"
if [[ "$HEAD" != "$EXPECTED_PYAT_1097_REVIEW_HEAD" ]]; then
  echo "HOLD_WRONG_CODE_HEAD: $HEAD" >&2
  exit 23
fi
if [[ -n "$(git status --porcelain --untracked-files=no)" ]]; then
  echo "HOLD_DIRTY_TRACKED_CODE" >&2
  exit 24
fi
PYTHON="${PYTHON:-python3}"
OUT="${PYAT_1097_ECON_PROOF_DIR:-$ROOT/.pyat1097-sourcefree-economics}"
mkdir -p "$OUT"
if [[ -e "$OUT/report.json" || -e "$OUT/legacy_1.json" ]]; then
  echo "HOLD_PROOF_DIR_ALREADY_OWNS_ECON_RECEIPTS: use a fresh output directory" >&2
  exit 25
fi
printf '%s\n' "$HEAD" > "$OUT/exact_head.txt"
for size in 1 10 100; do
  for mode in legacy shared; do
    "$PYTHON" -B rawlsing_next/tests/measure_pyat1097_distinct_saved_economics.py \
      --size "$size" --mode "$mode" --out "$OUT/${mode}_${size}.json"
  done
done
"$PYTHON" - "$OUT" <<'PY'
import json, pathlib, sys
root = pathlib.Path(sys.argv[1])
rows=[]
for size in (1,10,100):
    original=json.loads((root / f"legacy_{size}.json").read_text())
    shared=json.loads((root / f"shared_{size}.json").read_text())
    assert original["contract"] == shared["contract"]
    assert original["source_release_ref"] == shared["source_release_ref"]
    assert original["all_original_queries"] == shared["all_original_queries"], (
        f"REVISE_NATIVE_I03_S04_PARITY_FOR_SIZE_{size}"
    )
    assert original["native_index_preparations"] == size
    assert shared["native_index_preparations"] == 1
    row={
        "distinct_sourcefree_questions": size,
        "identical_fact_S04_and_risk_ref": True,
        "baseline_wall_seconds": original["elapsed_ns_excluding_fixture_construction"]/1e9,
        "shared_wall_seconds": shared["elapsed_ns_excluding_fixture_construction"]/1e9,
        "observed_ratio_legacy_over_shared": (
            original["elapsed_ns_excluding_fixture_construction"]/
            shared["elapsed_ns_excluding_fixture_construction"]
        ),
        "baseline_process_peak_rss_bytes": original["peak_whole_process_rss_bytes"],
        "shared_process_peak_rss_bytes": shared["peak_whole_process_rss_bytes"],
        "rss_is_process_peak_not_query_delta": True,
        "baseline_index_preparations": size,
        "shared_index_preparations": 1,
    }
    rows.append(row)
report={
    "contract":"PYAT1097_DISTINCT_SOURCEFREE_COMPARISON@1",
    "exact_git_head":(root/"exact_head.txt").read_text().strip(),
    "source_scope":"ONLY_4_RESPONDENT_SOURCEFREE_DISTINCT_QUERIES_NO_NATIVE_SURVEY_RIGHTS",
    "narrative":"Observed values vary by host; no model-selected P0 speedup guarantee or original-source economic claim",
    "results":rows,
    "qualification":"INDEPENDENT_NONAUTHOR_REVIEW_AND_NATIVE_SCALE_REQUIRED",
}
(root/"report.json").write_text(json.dumps(report,indent=2,sort_keys=True)+"\n")
print(json.dumps(report,indent=2))
PY
echo "PYAT1097_SOURCEFREE_ECONOMICS_PARITY_GREEN, observed measurements at $OUT/report.json"
