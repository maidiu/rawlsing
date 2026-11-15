#!/usr/bin/env bash
set -euo pipefail

IMPLEMENTATION_HEAD="ebb0da371f809a47bce68c6beb331208846573a9"
ACTUAL_HEAD="$(git rev-parse --verify HEAD^{commit})"
: "${QUAL_OUT:?set QUAL_OUT to a fresh persistent qualification output directory}"
PYTHON_BIN="${PYTHON_BIN:-python3}"

die() { printf 'FIABC_W3_I01_I02_QUAL_BLOCKED: %s\n' "$*" >&2; exit 2; }

git merge-base --is-ancestor "$IMPLEMENTATION_HEAD" "$ACTUAL_HEAD" || die "implementation head is not an ancestor of checkout"
unexpected="$(git diff --name-only "$IMPLEMENTATION_HEAD".."$ACTUAL_HEAD" | grep -Ev '^WORKER_RETURNS/PREMAIN-FIABC-W3-I01-I02-FANIN-R1/' || true)"
[[ -z "$unexpected" ]] || die "non-qualification files changed after implementation head: $unexpected"
[[ -z "$(git status --porcelain --untracked-files=all)" ]] || die "working tree is not clean"
[[ ! -e "$QUAL_OUT" ]] || die "QUAL_OUT already exists"

IMMUTABLE_EVIDENCE_COMMITS=(
  "0b96b8de9aac774566f872cf0630ebd4ddeb70e6"
  "76c73e5c15eb512fa0b3217bc9e313d2b54f9a2d"
  "0c0dd1f23bc59017552afdbd5af2021f051d48f7"
)
for commit in "${IMMUTABLE_EVIDENCE_COMMITS[@]}"; do
  if ! git cat-file -e "${commit}^{commit}" 2>/dev/null; then
    git fetch --no-tags origin "$commit"
  fi
  git cat-file -e "${commit}^{commit}" 2>/dev/null || die "immutable succession evidence commit unavailable: $commit"
done
echo "FIABC_W3_I01_I02_IMMUTABLE_EVIDENCE_FETCH_PASS ${IMMUTABLE_EVIDENCE_COMMITS[*]}"

"$PYTHON_BIN" -B - <<'PY'
import importlib.metadata, platform
expected = {
    "implementation":"CPython","python":"3.11.3",
    "pyreadstat":"1.3.6","pyarrow":"25.0.1",
    "system":"Darwin","machine":"x86_64",
}
observed = {
    "implementation":platform.python_implementation(),
    "python":platform.python_version(),
    "pyreadstat":importlib.metadata.version("pyreadstat"),
    "pyarrow":importlib.metadata.version("pyarrow"),
    "system":platform.system(),
    "machine":platform.machine(),
}
assert observed == expected, (expected, observed)
print("FIABC_W3_I01_I02_RUNTIME_PASS", observed)
PY

"$PYTHON_BIN" -B - <<'PY'
mods = (
    "rawlsing_next.pre553_diagnostics",
    "rawlsing_next.pre553_effective_n",
    "rawlsing_next.ee_p2x_darwin_court_driver",
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
for name in mods:
    __import__(name)
print("FIABC_W3_I01_I02_CURRENT_IMPORTS_PASS")
PY

[[ -z "$(git status --porcelain --untracked-files=all)" ]] || die "imports dirtied worktree"

PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 "$PYTHON_BIN" -m pytest -q -p no:cacheprovider   rawlsing_next/tests/test_pre553_diagnostics.py   rawlsing_next/tests/test_pre553_effective_n.py   tests/test_fiabc_final_measurement_telemetry_closure.py   tests/test_fiabc_terminal_completeness.py   rawlsing_next/tests/test_fiabc_final_progress_driver.py   rawlsing_next/tests/test_fiabc_final_oracle_freeze_producers.py   rawlsing_next/tests/test_fiabc_succession_producer.py   rawlsing_next/tests/test_fiabc_final_preflight_fanin.py   rawlsing_next/tests/test_fiabc_t2_six_cell_execution_binding.py   rawlsing_next/tests/test_fiabc_t3_oracle_process_envelope.py   rawlsing_next/tests/test_fiabc_t4_live_accounting.py   rawlsing_next/tests/test_fiabc_t5_live_terminal_control.py   rawlsing_next/tests/test_fiabc_p2_terminal_verifier.py   rawlsing_next/tests/test_fiabc_succession_preflight.py   rawlsing_next/tests/test_pre553_independent_parity_oracle.py   tests/test_ee_p2x_darwin_court_driver.py

[[ -z "$(git status --porcelain --untracked-files=all)" ]] || die "pytest dirtied worktree"

"$PYTHON_BIN" -B - <<'PY'
import json
from pathlib import Path
from rawlsing_next import ee_p2x_darwin_stage_backend as backend
from rawlsing_next import fiabc_telemetry_semantics as telemetry
from rawlsing_next import fiabc_terminal_completeness as completeness
from rawlsing_next import pre553_independent_parity_oracle as oracle
from rawlsing_next.fiabc_live_terminal_control import (
    WVS7_SUCCESSOR_DISCOVERY_AUTHORITY,
    WVS7_SUCCESSOR_LOCK2,
    WVS7_SUCCESSOR_LOCK2_REPLAY,
)

tm=set(telemetry.METRIC_DEFINITIONS)
bm=set(backend.METRICS)
cm=set(completeness.FROZEN_DISPOSITIVE_METRICS)
assert len(tm)==35, len(tm)
assert bm==tm
assert cm==tm

pkg=json.loads(Path("rawlsing_next/runtime/ee_p2x/02_WVS7_P2F2_RUNTIME_PACKAGE.json").read_text())
assert oracle.WVS7_LOCK2_IDENTITY == pkg["lock2"] == WVS7_SUCCESSOR_LOCK2
assert oracle.WVS7_DISCOVERY_AUTHORITY == pkg["discovery_authority_hash"] == WVS7_SUCCESSOR_DISCOVERY_AUTHORITY
assert oracle.WVS7_LOCK2_REPLAY_IDENTITY == WVS7_SUCCESSOR_LOCK2_REPLAY

assert hasattr(backend, "_current_failure_authority")
assert hasattr(backend, "_current_manifest_cell_order")
print("FIABC_W3_I01_I02_CURRENT_STATIC_ASSERTIONS_PASS")
PY

mkdir -p "$QUAL_OUT"

"$PYTHON_BIN" -B -m rawlsing_next.fiabc_succession_producer   --repo-root "$PWD"   --expected-head "$ACTUAL_HEAD"   --manifest-output "$QUAL_OUT/fiabc_i07_current_head_succession_manifest.json"   --lifecycle-output "$QUAL_OUT/fiabc_p10_lifecycle_context.json"   --receipt-output "$QUAL_OUT/fiabc_i07_p10_producer_receipt.json"

"$PYTHON_BIN" -B -m rawlsing_next.fiabc_succession_preflight   --manifest "$QUAL_OUT/fiabc_i07_current_head_succession_manifest.json"   --lifecycle-context "$QUAL_OUT/fiabc_p10_lifecycle_context.json"   --repo-root "$PWD"   --output "$QUAL_OUT/fiabc_i07_direct_preflight.json"

"$PYTHON_BIN" - "$QUAL_OUT/fiabc_i07_direct_preflight.json" <<'PY'
import json, sys
from pathlib import Path
doc=json.loads(Path(sys.argv[1]).read_text())
assert doc.get("status") == "PASS" or doc.get("passed") is True, doc
print("FIABC_W3_I01_I02_LIVE_SUCCESSION_PASS", doc.get("status"))
PY

[[ -z "$(git status --porcelain --untracked-files=all)" ]] || die "qualification dirtied worktree"

echo "PASS__FIABC_W3_I01_I02_FANIN_CURRENT_LAW_SOURCE_FREE_QUALIFIED"
echo "IMPLEMENTATION_HEAD=$IMPLEMENTATION_HEAD"
echo "QUALIFICATION_HEAD=$ACTUAL_HEAD"
echo "QUAL_OUT=$QUAL_OUT"
