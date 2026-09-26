#!/usr/bin/env bash
set -euo pipefail

CONTROL_ROOT="${CONTROL_ROOT:-$(git rev-parse --show-toplevel)}"
EXECUTION_ROOT="${EXECUTION_ROOT:-/private/tmp/fiabc-protected-16f5}"
RUNTIME_PYTHON="${RUNTIME_PYTHON:-/private/tmp/fiabc-lits-onepass-r1-runtime.kHpXQb/bin/python3.11}"
PACKET_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GUARD_ROOT="$PACKET_ROOT/source_free_guard"
TELEMETRY_DIR="$PACKET_ROOT/.zero-execution-processes"
OUTPUT="$PACKET_ROOT/HOSTILE_TEST_OUTPUT.txt"

[[ "$(git -C "$CONTROL_ROOT" branch --show-current)" == "agent/vozhd-fiabc-split-r2-fanin-r1" ]]
[[ "$(git -C "$CONTROL_ROOT" rev-parse HEAD)" == "ed8dabf015d1fd4b4ade9b55816a420b0bc1811e" ]]
[[ "$(git -C "$EXECUTION_ROOT" branch --show-current)" == "agent/rabochii-prev3-ee-p2x-final-abc-equal-work-execution-r1" ]]
[[ "$(git -C "$EXECUTION_ROOT" rev-parse HEAD)" == "16f5e7d5f691e908d85dc1dd26b8a59a29f668f4" ]]
[[ -z "$(git -C "$EXECUTION_ROOT" status --porcelain --untracked-files=all)" ]]
"$RUNTIME_PYTHON" -c 'import platform,sys; assert sys.version_info[:3] == (3,11,3); assert platform.system() == "Darwin"; assert platform.machine() == "x86_64"'

rm -rf "$TELEMETRY_DIR"
mkdir -p "$TELEMETRY_DIR"
: > "$OUTPUT"
export FIABC_ZERO_EXECUTION_TELEMETRY_DIR="$TELEMETRY_DIR"
export FIABC_SOURCE_SPLIT_EXECUTION_ROOT="$EXECUTION_ROOT"
export FIABC_REQUIRE_EXACT_DARWIN_RUNTIME=1
export PYTHONDONTWRITEBYTECODE=1

status=0
printf '%s\n' '=== FAN-IN SOURCE-FREE HOSTILE QUALIFICATION ===' | tee -a "$OUTPUT"
cd "$CONTROL_ROOT"
set +e
PYTHONPATH="$GUARD_ROOT:$CONTROL_ROOT" "$RUNTIME_PYTHON" -B -m pytest -vv -p no:cacheprovider \
  rawlsing_next/tests/test_fiabc_split_r2_a_progress_transition_parity.py \
  rawlsing_next/tests/test_fiabc_split_r2_b_workroot_gates.py \
  rawlsing_next/tests/test_fiabc_split_r2_d_merge_portable_evidence.py \
  rawlsing_next/tests/test_fiabc_split_r2_e_wvs_bytecode_prestate.py \
  rawlsing_next/tests/test_fiabc_source_local_split_qualification.py \
  rawlsing_next/tests/test_fiabc_t3_oracle_process_envelope.py \
  rawlsing_next/tests/test_fiabc_t4_live_accounting.py \
  rawlsing_next/tests/test_fiabc_t5_live_terminal_control.py \
  rawlsing_next/tests/test_fiabc_w3_i06a_process_isolation.py 2>&1 | tee -a "$OUTPUT"
fanin_status=${PIPESTATUS[0]}
set -e
if [[ "$fanin_status" -ne 0 ]]; then status="$fanin_status"; fi

printf '%s\n' '=== PROTECTED JOINED-SUCCESSOR SOURCE-FREE HOSTILE QUALIFICATION ===' | tee -a "$OUTPUT"
cd "$EXECUTION_ROOT"
set +e
PYTHONPATH="$GUARD_ROOT:$EXECUTION_ROOT" "$RUNTIME_PYTHON" -B -m pytest -vv -p no:cacheprovider \
  rawlsing_next/tests/test_fiabc_t5_joined_failure_semantics_repair.py \
  rawlsing_next/tests/test_fiabc_cache_neutral_joined_successor.py 2>&1 | tee -a "$OUTPUT"
joined_status=${PIPESTATUS[0]}
set -e
if [[ "$status" -eq 0 && "$joined_status" -ne 0 ]]; then status="$joined_status"; fi

# The hostile warm-pyc test deliberately creates this one untracked fixture.
WARMED_PYC="$EXECUTION_ROOT/rawlsing_next/__pycache__/fiabc_live_terminal_control.cpython-311.pyc"
if [[ -f "$WARMED_PYC" ]]; then
  rm -f "$WARMED_PYC"
  rmdir "$EXECUTION_ROOT/rawlsing_next/__pycache__" 2>/dev/null || true
fi

PYTHONPATH="$GUARD_ROOT:$CONTROL_ROOT" "$RUNTIME_PYTHON" -B -S \
  "$PACKET_ROOT/aggregate_source_access_telemetry.py" "$TELEMETRY_DIR" \
  "$PACKET_ROOT/source_access_telemetry.json"
rm -rf "$TELEMETRY_DIR"

[[ -z "$(git -C "$EXECUTION_ROOT" status --porcelain --untracked-files=all)" ]] || status=1
[[ -z "$(git -C "$CONTROL_ROOT" status --porcelain)" ]] || status=1
unexpected_untracked="$(git -C "$CONTROL_ROOT" ls-files --others --exclude-standard | sed '/^WORKER_RETURNS\/FIABC-SOURCE-SPLIT-R2-FANIN-R1\//d')"
[[ -z "$unexpected_untracked" ]] || status=1
exit "$status"
