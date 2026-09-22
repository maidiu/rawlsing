#!/usr/bin/env bash
set -euo pipefail

PREMAIN_PARENT="d474f8e3c9630c4bcbb10d6e8359b71ba5b3060d"
FIABC_PARENT="91723d443f56acb05af63acc0d3a34fb9a97e3f4"
MAIN_PARENT="25830fe7462bb9e29bc4087e6ae14f3f84cec377"
CODE_HEAD="f6914345c9856acefba9879ff325c12ab6040b5c"

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

TERMINAL_ORACLE_BLOB="6cf8d8bf8ac2d6421cd733a72a444687e241e659"
TERMINAL_PRODUCER_BLOB="6c93b3a25e671af714ddb39ef6b335410cf4d0e7"
LITS_REPRESENTATION_AUTHORITY_BLOB="94a833a7d8946bf3bd43296d9fe1e2239a3aa4b9"
LITS_REPRESENTATION_TEST_BLOB="35cbae0328b3aa695ed4ece3c979a3742f1a527d"
DISCOVERY_EXACT_BLOB="ee0544115feb9d76c8c68b9dd773302c8fa8bb48"
DISCOVERY_EXACT_TEST_BLOB="b53039aeb95e012993c5233a7575c1dad5a14929"
LIVE_TERMINAL_CONTROL_BLOB="3530ab1a576f2e84980ba81a53a20f75404ef2aa"
LIVE_TERMINAL_CONTROL_TEST_BLOB="eb3db5ac86c7b01f01586c4bf0ee9a4f156b09a0"
TERMINAL_PREFLIGHT_TEST_BLOB="02c6dad5912fd7283cc1fc5b889cde62b9818101"
[[ "$(git rev-parse HEAD:rawlsing_next/pre553_independent_parity_oracle.py)" == "$TERMINAL_ORACLE_BLOB" ]] \
  || die "terminal-readiness LiTS oracle owner drift"
[[ "$(git rev-parse HEAD:rawlsing_next/fiabc_final_oracle_freeze_producers.py)" == "$TERMINAL_PRODUCER_BLOB" ]] \
  || die "terminal-readiness oracle producer drift"
[[ "$(git rev-parse HEAD:rawlsing_next/fiabc_lits_i_representation_authority.py)" == "$LITS_REPRESENTATION_AUTHORITY_BLOB" ]] \
  || die "LiTS-I representation authority drift"
[[ "$(git rev-parse HEAD:rawlsing_next/tests/test_fiabc_lits_i_representation_authority.py)" == "$LITS_REPRESENTATION_TEST_BLOB" ]] \
  || die "LiTS-I representation hostile test drift"
[[ "$(git rev-parse HEAD:rawlsing_next/pre553_discovery_exact.py)" == "$DISCOVERY_EXACT_BLOB" ]] \
  || die "exact discovery validation interpreter drift"
[[ "$(git rev-parse HEAD:rawlsing_next/tests/test_pre553_discovery_exact.py)" == "$DISCOVERY_EXACT_TEST_BLOB" ]] \
  || die "exact discovery validation hostile test drift"
[[ "$(git rev-parse HEAD:rawlsing_next/fiabc_live_terminal_control.py)" == "$LIVE_TERMINAL_CONTROL_BLOB" ]] \
  || die "live terminal constituent I03 control drift"
[[ "$(git rev-parse HEAD:rawlsing_next/tests/test_fiabc_t5_live_terminal_control.py)" == "$LIVE_TERMINAL_CONTROL_TEST_BLOB" ]] \
  || die "live terminal constituent I03 hostile test drift"
[[ "$(git rev-parse HEAD:rawlsing_next/tests/test_fiabc_final_preflight_fanin.py)" == "$TERMINAL_PREFLIGHT_TEST_BLOB" ]] \
  || die "terminal-readiness preflight qualification test drift"

for ref in "$PREMAIN_PARENT" "$FIABC_PARENT" "$MAIN_PARENT" "$CODE_HEAD"; do
  git merge-base --is-ancestor "$ref" HEAD || die "required cumulative ancestor $ref is absent"
done
[[ -z "$(git status --porcelain)" ]] || die "working tree is not clean"

unexpected="$(git diff --name-only "$FIABC_PARENT"..HEAD -- rawlsing_next | \
  grep -Ev '^(rawlsing_next/pre553_independent_parity_oracle\.py|rawlsing_next/pre553_discovery_exact\.py|rawlsing_next/fiabc_final_oracle_freeze_producers\.py|rawlsing_next/fiabc_lits_i_representation_authority\.py|rawlsing_next/fiabc_live_terminal_control\.py|rawlsing_next/tests/test_pre553_discovery_exact\.py|rawlsing_next/tests/test_fiabc_lits_i_representation_authority\.py|rawlsing_next/tests/test_fiabc_t5_live_terminal_control\.py|rawlsing_next/tests/test_fiabc_final_preflight_fanin\.py|rawlsing_next/rabochii_return_beacon\.py|rawlsing_next/rabochii_return_beacon_actionable\.py|rawlsing_next/rabochii_return_beacon_sweep\.py|rawlsing_next/tests/test_rabochii_return_beacon\.py|rawlsing_next/tests/test_rabochii_return_beacon_actionable\.py|rawlsing_next/tests/test_rabochii_return_beacon_sweep\.py)$' || true)"
[[ -z "$unexpected" ]] || die "FIABC runtime/test drift after reconciliation: $unexpected"

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
 "rawlsing_next.fiabc_lits_i_representation_authority",
 "rawlsing_next.pre553_independent_parity_oracle",
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
 rawlsing_next/fiabc_lits_i_representation_authority.py \
 rawlsing_next/pre553_discovery_exact.py \
 rawlsing_next/pre553_independent_parity_oracle.py

"$PYTHON_BIN" -m pytest -q \
 tests/test_fiabc_final_measurement_telemetry_closure.py \
 tests/test_fiabc_terminal_completeness.py \
 rawlsing_next/tests/test_fiabc_final_progress_driver.py \
 rawlsing_next/tests/test_fiabc_final_oracle_freeze_producers.py \
 rawlsing_next/tests/test_fiabc_lits_i_representation_authority.py \
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
from rawlsing_next.fiabc_lits_i_representation_authority import REPRESENTATION_AUTHORITY_REF,TARGET_VARIABLES,LEGACY_FACADE_BLOB
from rawlsing_next.fiabc_live_terminal_control import WVS7_SUCCESSOR_DISCOVERY_AUTHORITY,WVS7_SUCCESSOR_LOCK2,WVS7_SUCCESSOR_LOCK2_REPLAY
tm=set(telemetry.METRIC_DEFINITIONS); bm=set(backend.METRICS); cm=set(completeness.FROZEN_DISPOSITIVE_METRICS)
assert len(tm)==35
assert bm==tm==cm
pkg=json.loads(Path("rawlsing_next/runtime/ee_p2x/02_WVS7_P2F2_RUNTIME_PACKAGE.json").read_text())
assert oracle.WVS7_LOCK2_IDENTITY==pkg["lock2"]==WVS7_SUCCESSOR_LOCK2
assert oracle.WVS7_DISCOVERY_AUTHORITY==pkg["discovery_authority_hash"]==WVS7_SUCCESSOR_DISCOVERY_AUTHORITY
assert oracle.WVS7_LOCK2_REPLAY_IDENTITY==WVS7_SUCCESSOR_LOCK2_REPLAY
assert REPRESENTATION_AUTHORITY_REF.authority_content_hash=="9fce3b606413c2a5d3e9a05eda967067d191fbb31ff869d445d962bdf321393d"
assert dict(TARGET_VARIABLES)=={"q301_2":194,"q301_7":199}
assert LEGACY_FACADE_BLOB=="7c509c2098d0030f253344eb3f682471378812a8"
assert hasattr(backend,"_current_failure_authority")
assert hasattr(backend,"_current_manifest_cell_order")
print("RAWLSING_RECONCILED_FIABC_STATIC_CROSS_LANE_ASSERTIONS_PASS")
PY

echo "RAWLSING_CANONICAL_REINTEGRATION_SOURCE_FREE_QUALIFICATION_GREEN__READY_FOR_PRE_CANDIDATE_FREEZE"
