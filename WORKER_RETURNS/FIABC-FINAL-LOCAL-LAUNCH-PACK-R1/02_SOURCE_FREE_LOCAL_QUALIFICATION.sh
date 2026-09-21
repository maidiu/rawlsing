#!/usr/bin/env bash
set -euo pipefail

EXPECTED_HEAD="858b3b52674044e020b85f8697c5f2c61ce15371"
EXPECTED_BRANCH="agent/rabochii-prev3-ee-p2x-final-abc-equal-work-execution-r1"

die() { printf 'FIABC_SOURCE_FREE_QUALIFICATION_BLOCKED: %s\n' "$*" >&2; exit 2; }

[[ "$(git rev-parse HEAD)" == "$EXPECTED_HEAD" ]] || die "HEAD is not exact audited integrated head $EXPECTED_HEAD"
[[ -z "$(git status --porcelain)" ]] || die "working tree is not clean"

# The active driver still enforces this historical execution-branch identity.
# A detached/integration branch checkout is not launch-equivalent.
[[ "$(git branch --show-current)" == "$EXPECTED_BRANCH" ]] || die   "driver requires existing P2X execution branch $EXPECTED_BRANCH to be fast-forwarded to the exact head"

python - <<'PY'
import importlib
import sys

required = (
    "pytest",
    "pandas",
    "rawlsing_next.ee_p2x_darwin_court_driver",
    "rawlsing_next.ee_p2x_darwin_stage_backend",
    "rawlsing_next.ee_p2x_process_isolated_backend",
    "rawlsing_next.fiabc_live_accounting_binding",
    "rawlsing_next.fiabc_telemetry_semantics",
    "rawlsing_next.fiabc_live_terminal_control",
    "rawlsing_next.fiabc_terminal_completeness",
    "rawlsing_next.fiabc_succession_preflight",
    "rawlsing_next.pre553_independent_parity_oracle",
)
for name in required:
    importlib.import_module(name)
print("FIABC_SOURCE_FREE_IMPORTS_OK", sys.version)
PY

python -m py_compile   rawlsing_next/ee_p2x_darwin_court_driver.py   rawlsing_next/ee_p2x_darwin_stage_backend.py   rawlsing_next/ee_p2x_process_isolated_backend.py   rawlsing_next/ee_p2x_candidate_process_envelope.py   rawlsing_next/fiabc_live_accounting_binding.py   rawlsing_next/fiabc_telemetry_semantics.py   rawlsing_next/fiabc_live_terminal_control.py   rawlsing_next/fiabc_terminal_completeness.py   rawlsing_next/fiabc_succession_preflight.py   rawlsing_next/pre553_independent_parity_oracle.py

python -m pytest -q   tests/test_fiabc_final_measurement_telemetry_closure.py   tests/test_fiabc_terminal_completeness.py   rawlsing_next/tests/test_fiabc_final_progress_driver.py   rawlsing_next/tests/test_fiabc_final_preflight_fanin.py   rawlsing_next/tests/test_fiabc_t2_six_cell_execution_binding.py   rawlsing_next/tests/test_fiabc_t3_oracle_process_envelope.py   rawlsing_next/tests/test_fiabc_t4_live_accounting.py   rawlsing_next/tests/test_fiabc_t5_live_terminal_control.py   rawlsing_next/tests/test_fiabc_p2_terminal_verifier.py   rawlsing_next/tests/test_fiabc_succession_preflight.py   tests/test_ee_p2x_darwin_court_driver.py

# Cross-lane hostile assertions the separately-authored tests currently do not
# prove against one another.
python - <<'PY'
import json
from pathlib import Path

from rawlsing_next import ee_p2x_darwin_stage_backend as backend
from rawlsing_next import fiabc_telemetry_semantics as telemetry
from rawlsing_next import fiabc_terminal_completeness as completeness
from rawlsing_next import pre553_independent_parity_oracle as oracle

errors = []

tm = set(telemetry.METRIC_DEFINITIONS)
bm = set(backend.METRICS)
cm = set(completeness.FROZEN_DISPOSITIVE_METRICS)
if len(tm) != 35 or bm != tm:
    errors.append(f"telemetry/backend registry drift: telemetry={len(tm)} backend={len(bm)}")
if cm != tm:
    errors.append(
        "S16/S17 completeness != telemetry registry; missing="
        + ",".join(sorted(tm - cm))
        + " extra=" + ",".join(sorted(cm - tm))
    )

pkg = json.loads(Path("rawlsing_next/runtime/ee_p2x/02_WVS7_P2F2_RUNTIME_PACKAGE.json").read_text())
if oracle.WVS7_LOCK2_IDENTITY != pkg["lock2"]:
    errors.append(
        f"WVS oracle Lock2 predecessor/successor split: oracle={oracle.WVS7_LOCK2_IDENTITY} runtime={pkg['lock2']}"
    )
if oracle.WVS7_DISCOVERY_AUTHORITY != pkg["discovery_authority_hash"]:
    errors.append(
        "WVS oracle DiscoveryAuthority predecessor/successor split: "
        f"oracle={oracle.WVS7_DISCOVERY_AUTHORITY} runtime={pkg['discovery_authority_hash']}"
    )

r1m = json.loads(Path(
    "WORKER_RETURNS/FIABC-LM2-R1M-LOCK2-SUCCESSOR-R16-ORACLE/07_FRESH_WVS_ORACLE.json"
).read_text())
if r1m.get("schema") != oracle.ORACLE_SCHEMA:
    errors.append(
        "accepted R1M WVS oracle is not the standard live T3/T5 oracle schema: "
        f"{r1m.get('schema')} != {oracle.ORACLE_SCHEMA}"
    )

legacy = json.loads(Path("WORKER_RETURNS/EE-P2X/09_LOCAL_COURT_FROZEN_EXPECTATIONS.json").read_text())
if legacy.get("lock2", {}).get("hash") != pkg["lock2"]:
    errors.append(
        "active backend failure serialization still consumes predecessor 09 expectations: "
        f"{legacy.get('lock2', {}).get('hash')} != {pkg['lock2']}"
    )

if errors:
    print("FIABC_INTEGRATED_HOSTILE_AUDIT_BLOCKED")
    for index, error in enumerate(errors, 1):
        print(f"{index}. {error}")
    raise SystemExit(3)

print("FIABC_SOURCE_FREE_QUALIFICATION_GREEN__FINAL_CLOSURE_AND_ACTIVE_SEAMS_PASS")
PY
