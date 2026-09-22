#!/usr/bin/env bash
set -euo pipefail

PREMAIN_PARENT="d474f8e3c9630c4bcbb10d6e8359b71ba5b3060d"
FIABC_PARENT="91723d443f56acb05af63acc0d3a34fb9a97e3f4"
MAIN_PARENT="25830fe7462bb9e29bc4087e6ae14f3f84cec377"
CODE_HEAD="aa15525750085f4e223d579010688660a9ae1b6b"

die() { printf 'RAWLSING_RECONCILED_FIABC_SOURCE_FREE_BLOCKED: %s\n' "$*" >&2; exit 2; }

for ref in "$PREMAIN_PARENT" "$FIABC_PARENT" "$MAIN_PARENT" "$CODE_HEAD"; do
  git merge-base --is-ancestor "$ref" HEAD || die "required cumulative ancestor $ref is absent"
done
[[ -z "$(git status --porcelain)" ]] || die "working tree is not clean"

unexpected="$(git diff --name-only "$FIABC_PARENT"..HEAD -- rawlsing_next | \
  grep -Ev '^(rawlsing_next/rabochii_return_beacon\.py|rawlsing_next/rabochii_return_beacon_actionable\.py|rawlsing_next/rabochii_return_beacon_sweep\.py|rawlsing_next/tests/test_rabochii_return_beacon\.py|rawlsing_next/tests/test_rabochii_return_beacon_actionable\.py|rawlsing_next/tests/test_rabochii_return_beacon_sweep\.py)$' || true)"
[[ -z "$unexpected" ]] || die "FIABC runtime/test drift after reconciliation: $unexpected"

[[ "$(git rev-parse HEAD:.github/workflows/rabochii-return-beacon.yml)" == "$(git rev-parse "$MAIN_PARENT":.github/workflows/rabochii-return-beacon.yml)" ]] \
  || die "Return Beacon workflow is not exact inherited main state"

python - <<'PY'
from pathlib import Path
p=Path(".github/workflows/rabochii-return-beacon.yml").read_text()
assert "workflow_dispatch:" in p
assert "\n  schedule:" not in p
assert "\n  push:" not in p
print("RETURN_BEACON_MANUAL_ONLY_PASS")
PY

python - <<'PY'
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
 "rawlsing_next.pre553_independent_parity_oracle",
)
for name in required: importlib.import_module(name)
print("RAWLSING_RECONCILED_FIABC_IMPORTS_OK",sys.version)
PY

python -m py_compile \
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
 rawlsing_next/pre553_independent_parity_oracle.py

python -m pytest -q \
 tests/test_fiabc_final_measurement_telemetry_closure.py \
 tests/test_fiabc_terminal_completeness.py \
 rawlsing_next/tests/test_fiabc_final_progress_driver.py \
 rawlsing_next/tests/test_fiabc_final_oracle_freeze_producers.py \
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

python - <<'PY'
import json
from pathlib import Path
from rawlsing_next import ee_p2x_darwin_stage_backend as backend
from rawlsing_next import fiabc_telemetry_semantics as telemetry
from rawlsing_next import fiabc_terminal_completeness as completeness
from rawlsing_next import pre553_independent_parity_oracle as oracle
from rawlsing_next.fiabc_live_terminal_control import WVS7_SUCCESSOR_DISCOVERY_AUTHORITY,WVS7_SUCCESSOR_LOCK2,WVS7_SUCCESSOR_LOCK2_REPLAY
tm=set(telemetry.METRIC_DEFINITIONS); bm=set(backend.METRICS); cm=set(completeness.FROZEN_DISPOSITIVE_METRICS)
assert len(tm)==35
assert bm==tm==cm
pkg=json.loads(Path("rawlsing_next/runtime/ee_p2x/02_WVS7_P2F2_RUNTIME_PACKAGE.json").read_text())
assert oracle.WVS7_LOCK2_IDENTITY==pkg["lock2"]==WVS7_SUCCESSOR_LOCK2
assert oracle.WVS7_DISCOVERY_AUTHORITY==pkg["discovery_authority_hash"]==WVS7_SUCCESSOR_DISCOVERY_AUTHORITY
assert oracle.WVS7_LOCK2_REPLAY==WVS7_SUCCESSOR_LOCK2_REPLAY
assert hasattr(backend,"_current_failure_authority")
assert hasattr(backend,"_current_manifest_cell_order")
print("RAWLSING_RECONCILED_FIABC_STATIC_CROSS_LANE_ASSERTIONS_PASS")
PY

echo "RAWLSING_CANONICAL_REINTEGRATION_SOURCE_FREE_QUALIFICATION_GREEN__READY_FOR_PRE_CANDIDATE_FREEZE"
