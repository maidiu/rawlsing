#!/usr/bin/env bash
set -euo pipefail

PREMAIN_PARENT="d474f8e3c9630c4bcbb10d6e8359b71ba5b3060d"
FIABC_PARENT="91723d443f56acb05af63acc0d3a34fb9a97e3f4"
MAIN_PARENT="25830fe7462bb9e29bc4087e6ae14f3f84cec377"
CODE_HEAD="28b29ac728dc816eaf4ccd1e0d7a021d20bd935e"

die() { printf 'RAWLSING_RECONCILED_FIABC_SOURCE_FREE_BLOCKED: %s\n' "$*" >&2; exit 2; }

if command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="$(command -v python3)"
elif command -v python >/dev/null 2>&1; then
  PYTHON_BIN="$(command -v python)"
else
  die "Python 3 interpreter not found (tried python3, python)"
fi
"$PYTHON_BIN" -c 'import sys; raise SystemExit(0 if sys.version_info.major == 3 else 2)' \
  || die "selected interpreter is not Python 3: $PYTHON_BIN"
readonly PYTHON_BIN

assert_blob() {
  local path="$1" expected="$2" label="$3" actual
  actual="$(git rev-parse "HEAD:$path")" || die "$label is absent from HEAD"
  [[ "$actual" == "$expected" ]] || die "$label blob drift: $actual"
}

assert_blob rawlsing_next/_pre553_query_eval.py f808dfcd2008cc71e9203de3cadf1abe14223974 "LiTS I05 evaluator"
assert_blob rawlsing_next/_pre553_query_predicate.py 8590bacf464b2c61f319f581820a3af76ed1e60c "LiTS F02 predicate interpreter"
assert_blob rawlsing_next/fiabc_final_oracle_freeze_producers.py 59070006706dcbe6a2ee0a2649e1ecd211f6d7eb "candidate-neutral oracle producer"
assert_blob rawlsing_next/fiabc_lits_i_d03_risk_set_authority.py 65e87a45339a2c29443c7c619d2687dbd5b90056 "LiTS D03 risk-set authority"
assert_blob rawlsing_next/fiabc_lits_i_f02_event_representation_authority.py 0ee29ee14f21ec48c431e215ef5c6ca08dfad869 "LiTS F02 event representation authority"
assert_blob rawlsing_next/fiabc_lits_i_i03_operation_authority.py 072fd760a649a1706e4acc988d2de46f678cbc61 "LiTS I03 operation authority"
assert_blob rawlsing_next/fiabc_lits_i_representation_authority.py 94a833a7d8946bf3bd43296d9fe1e2239a3aa4b9 "LiTS physical representation authority"
assert_blob rawlsing_next/fiabc_live_terminal_control.py 95739544dceea60298a6e90a87a9062b4fed6df1 "live terminal control"
assert_blob rawlsing_next/pre553_discovery_exact.py ee0544115feb9d76c8c68b9dd773302c8fa8bb48 "exact discovery interpreter"
assert_blob rawlsing_next/pre553_empirical_authority.py ca65a7fd4d52f0c44447434559b1d09412e7aa39 "runtime authority resolver"
assert_blob rawlsing_next/pre553_empirical_query.py 149e7a7d78f1d16c696cc5b75f561c2c2929e93e "empirical query evaluator"
assert_blob rawlsing_next/pre553_independent_parity_oracle.py 04555c145bf499e6c4c5d0f72e612baefa7319fa "independent parity oracle"
assert_blob rawlsing_next/pre553_runtime_authority.py 9030b0f20f3d71482425b8acb864abc182adc4b0 "runtime successor authority set"
assert_blob rawlsing_next/runtime/ee_p2x/01_LITS_CURRENT_RUNTIME_MATERIALIZER.py e4c2c8057e495a3a9a2fc1d7cb0896496d434ac1 "active LiTS runtime materializer"
assert_blob rawlsing_next/runtime/ee_p2x/03_LITS_RUNTIME_AUTHORITY_OVERLAY_BINDING.json 661c8f64d95fcf4be5236b1ff19c96485cb10b8b "LiTS runtime authority overlay binding"
assert_blob rawlsing_next/tests/test_fiabc_final_oracle_freeze_producers.py 0bbb151e6e7faeca683be94ed963f4c2a7fa3c82 "oracle producer hostile tests"
assert_blob rawlsing_next/tests/test_fiabc_final_preflight_fanin.py 02c6dad5912fd7283cc1fc5b889cde62b9818101 "preflight fan-in tests"
assert_blob rawlsing_next/tests/test_fiabc_lits_i_i03_operation_authority.py de296b63c3e6e9c59665a5f848e0807f3dc3c562 "I03 D03 F02 authority hostile tests"
assert_blob rawlsing_next/tests/test_fiabc_lits_i_representation_authority.py 33380bfd35b9d2cbb87a94266cb5e88862850e87 "LiTS representation hostile tests"
assert_blob rawlsing_next/tests/test_fiabc_t5_live_terminal_control.py 392bc4aef4b4449896a0bc8ad7828a47a3587978 "WVS and terminal control hostile tests"
assert_blob rawlsing_next/tests/test_fiabc_w3_i04_runtime_packaging_rebind.py 5de1f37e16ed1a0d3f6b09460926a1fb921864ff "runtime overlay packaging tests"
assert_blob rawlsing_next/tests/test_pre553_discovery_exact.py b53039aeb95e012993c5233a7575c1dad5a14929 "exact discovery hostile tests"

expected_runtime_files="$(cat <<'EOF'
rawlsing_next/_pre553_query_eval.py
rawlsing_next/_pre553_query_predicate.py
rawlsing_next/fiabc_final_oracle_freeze_producers.py
rawlsing_next/fiabc_lits_i_d03_risk_set_authority.py
rawlsing_next/fiabc_lits_i_f02_event_representation_authority.py
rawlsing_next/fiabc_lits_i_i03_operation_authority.py
rawlsing_next/fiabc_lits_i_representation_authority.py
rawlsing_next/fiabc_live_terminal_control.py
rawlsing_next/pre553_discovery_exact.py
rawlsing_next/pre553_empirical_authority.py
rawlsing_next/pre553_empirical_query.py
rawlsing_next/pre553_independent_parity_oracle.py
rawlsing_next/pre553_runtime_authority.py
rawlsing_next/rabochii_return_beacon.py
rawlsing_next/rabochii_return_beacon_actionable.py
rawlsing_next/rabochii_return_beacon_sweep.py
rawlsing_next/runtime/ee_p2x/01_LITS_CURRENT_RUNTIME_MATERIALIZER.py
rawlsing_next/runtime/ee_p2x/03_LITS_RUNTIME_AUTHORITY_OVERLAY_BINDING.json
rawlsing_next/tests/test_fiabc_final_oracle_freeze_producers.py
rawlsing_next/tests/test_fiabc_final_preflight_fanin.py
rawlsing_next/tests/test_fiabc_lits_i_i03_operation_authority.py
rawlsing_next/tests/test_fiabc_lits_i_representation_authority.py
rawlsing_next/tests/test_fiabc_t5_live_terminal_control.py
rawlsing_next/tests/test_fiabc_w3_i04_runtime_packaging_rebind.py
rawlsing_next/tests/test_pre553_discovery_exact.py
rawlsing_next/tests/test_rabochii_return_beacon.py
rawlsing_next/tests/test_rabochii_return_beacon_actionable.py
rawlsing_next/tests/test_rabochii_return_beacon_sweep.py
EOF
)"
actual_runtime_files="$(git diff --name-only "$FIABC_PARENT"..HEAD -- rawlsing_next | LC_ALL=C sort)"
expected_runtime_files="$(printf '%s\n' "$expected_runtime_files" | LC_ALL=C sort)"
[[ "$actual_runtime_files" == "$expected_runtime_files" ]] \
  || die "FIABC runtime/test scope drift: expected=[$expected_runtime_files] actual=[$actual_runtime_files]"

for ref in "$PREMAIN_PARENT" "$FIABC_PARENT" "$MAIN_PARENT" "$CODE_HEAD"; do
  git merge-base --is-ancestor "$ref" HEAD || die "required cumulative ancestor $ref is absent"
done
[[ -z "$(git status --porcelain)" ]] || die "working tree is not clean"

[[ "$(git rev-parse HEAD:.github/workflows/rabochii-return-beacon.yml)" == "$(git rev-parse "$MAIN_PARENT":.github/workflows/rabochii-return-beacon.yml)" ]] \
  || die "Return Beacon workflow is not exact inherited main state"

"$PYTHON_BIN" - <<'PY'
from pathlib import Path
p=Path(".github/workflows/rabochii-return-beacon.yml").read_text()
assert "workflow_dispatch:" in p
assert "\n  schedule:" not in p
assert "\n  push:" not in p
print("RETURN_BEACON_MANUAL_ONLY_PASS")
PY

"$PYTHON_BIN" - <<'PY'
import importlib, sys
required=(
 "pytest","pandas",
 "rawlsing_next.ee_p2x_darwin_court_driver",
 "rawlsing_next.ee_p2x_darwin_stage_backend",
 "rawlsing_next.ee_p2x_process_isolated_backend",
 "rawlsing_next.fiabc_live_accounting_binding",
 "rawlsing_next.fiabc_telemetry_semantics",
 "rawlsing_next.fiabc_live_terminal_control",
 "rawlsing_next.fiabc_terminal_completeness",
 "rawlsing_next.fiabc_succession_preflight",
 "rawlsing_next.fiabc_succession_producer",
 "rawlsing_next.fiabc_final_oracle_freeze_producers",
 "rawlsing_next.fiabc_lits_i_i03_operation_authority",
 "rawlsing_next.fiabc_lits_i_d03_risk_set_authority",
 "rawlsing_next.fiabc_lits_i_f02_event_representation_authority",
 "rawlsing_next.fiabc_lits_i_representation_authority",
 "rawlsing_next.pre553_independent_parity_oracle",
 "rawlsing_next.pre553_runtime_authority",
)
for name in required: importlib.import_module(name)
print("RAWLSING_RECONCILED_FIABC_IMPORTS_OK",sys.version)
PY

"$PYTHON_BIN" -m py_compile \
 rawlsing_next/ee_p2x_darwin_court_driver.py \
 rawlsing_next/ee_p2x_darwin_stage_backend.py \
 rawlsing_next/ee_p2x_process_isolated_backend.py \
 rawlsing_next/ee_p2x_candidate_process_envelope.py \
 rawlsing_next/fiabc_live_accounting_binding.py \
 rawlsing_next/fiabc_telemetry_semantics.py \
 rawlsing_next/fiabc_live_terminal_control.py \
 rawlsing_next/fiabc_terminal_completeness.py \
 rawlsing_next/fiabc_succession_preflight.py \
 rawlsing_next/fiabc_succession_producer.py \
 rawlsing_next/fiabc_final_oracle_freeze_producers.py \
 rawlsing_next/fiabc_lits_i_i03_operation_authority.py \
 rawlsing_next/fiabc_lits_i_d03_risk_set_authority.py \
 rawlsing_next/fiabc_lits_i_f02_event_representation_authority.py \
 rawlsing_next/fiabc_lits_i_representation_authority.py \
 rawlsing_next/pre553_runtime_authority.py \
 rawlsing_next/_pre553_query_predicate.py \
 rawlsing_next/_pre553_query_eval.py \
 rawlsing_next/pre553_empirical_authority.py \
 rawlsing_next/pre553_empirical_query.py \
 rawlsing_next/pre553_discovery_exact.py \
 rawlsing_next/pre553_independent_parity_oracle.py

"$PYTHON_BIN" -m pytest -q \
 tests/test_fiabc_final_measurement_telemetry_closure.py \
 tests/test_fiabc_terminal_completeness.py \
 rawlsing_next/tests/test_fiabc_final_progress_driver.py \
 rawlsing_next/tests/test_fiabc_final_oracle_freeze_producers.py \
 rawlsing_next/tests/test_fiabc_lits_i_representation_authority.py \
 rawlsing_next/tests/test_fiabc_lits_i_i03_operation_authority.py \
 rawlsing_next/tests/test_fiabc_w3_i04_runtime_packaging_rebind.py \
 rawlsing_next/tests/test_pre553_discovery_exact.py \
 rawlsing_next/tests/test_fiabc_succession_producer.py \
 rawlsing_next/tests/test_fiabc_final_preflight_fanin.py \
 rawlsing_next/tests/test_fiabc_t2_six_cell_execution_binding.py \
 rawlsing_next/tests/test_fiabc_t3_oracle_process_envelope.py \
 rawlsing_next/tests/test_fiabc_t4_live_accounting.py \
 rawlsing_next/tests/test_fiabc_t5_live_terminal_control.py \
 rawlsing_next/tests/test_fiabc_p2_terminal_verifier.py \
 rawlsing_next/tests/test_fiabc_succession_preflight.py \
 rawlsing_next/tests/test_pre553_independent_parity_oracle.py \
 tests/test_ee_p2x_darwin_court_driver.py

"$PYTHON_BIN" - <<'PY'
import json
from pathlib import Path
from rawlsing_next import ee_p2x_darwin_stage_backend as backend
from rawlsing_next import fiabc_telemetry_semantics as telemetry
from rawlsing_next import fiabc_terminal_completeness as completeness
from rawlsing_next import pre553_independent_parity_oracle as oracle
from rawlsing_next.fiabc_lits_i_f02_event_representation_authority import AUTHORITY_CONTENT_HASH as LITS_F02_REPRESENTATION_AUTHORITY
from rawlsing_next.fiabc_lits_i_representation_authority import REPRESENTATION_AUTHORITY_REF,TARGET_VARIABLES,LEGACY_FACADE_BLOB
from rawlsing_next.fiabc_live_terminal_control import WVS7_SUCCESSOR_DISCOVERY_AUTHORITY,WVS7_SUCCESSOR_LOCK2,WVS7_SUCCESSOR_LOCK2_REPLAY
tm=set(telemetry.METRIC_DEFINITIONS); bm=set(backend.METRICS); cm=set(completeness.FROZEN_DISPOSITIVE_METRICS)
assert len(tm)==35
assert bm==tm==cm
pkg=json.loads(Path("rawlsing_next/runtime/ee_p2x/02_WVS7_P2F2_RUNTIME_PACKAGE.json").read_text())
overlay=json.loads(Path("rawlsing_next/runtime/ee_p2x/03_LITS_RUNTIME_AUTHORITY_OVERLAY_BINDING.json").read_text())
wvs_oracle=json.loads(Path("WORKER_RETURNS/FIABC-LM2-R1M-LOCK2-SUCCESSOR-R16-ORACLE/07_FRESH_WVS_ORACLE.json").read_text())
assert oracle.WVS7_LOCK2_IDENTITY==pkg["lock2"]==WVS7_SUCCESSOR_LOCK2
assert oracle.WVS7_DISCOVERY_AUTHORITY==pkg["discovery_authority_hash"]==WVS7_SUCCESSOR_DISCOVERY_AUTHORITY
assert oracle.WVS7_LOCK2_REPLAY_IDENTITY==WVS7_SUCCESSOR_LOCK2_REPLAY
assert overlay["adopted_source_specific_authorities"]["lits_f02_event_representation_successor"]==LITS_F02_REPRESENTATION_AUTHORITY
assert wvs_oracle["expected_learned_product"]["coverage"]["typed_terminal_counts"]=={"COVERAGE_LIMITED":46}
assert overlay["wvs7_preservation"]["frozen_typed_terminal_counts"]=={"COVERAGE_LIMITED":46}
assert REPRESENTATION_AUTHORITY_REF.authority_content_hash=="9fce3b606413c2a5d3e9a05eda967067d191fbb31ff869d445d962bdf321393d"
assert dict(TARGET_VARIABLES)=={"q301_2":194,"q301_7":199}
assert LEGACY_FACADE_BLOB=="7c509c2098d0030f253344eb3f682471378812a8"
assert hasattr(backend,"_current_failure_authority")
assert hasattr(backend,"_current_manifest_cell_order")
print("RAWLSING_RECONCILED_FIABC_STATIC_CROSS_LANE_ASSERTIONS_PASS")
PY

echo "RAWLSING_CANONICAL_REINTEGRATION_SOURCE_FREE_QUALIFICATION_GREEN__READY_FOR_PRE_CANDIDATE_FREEZE"
