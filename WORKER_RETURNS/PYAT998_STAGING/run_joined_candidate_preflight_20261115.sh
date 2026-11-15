#!/usr/bin/env bash
# PYAT #998 read-only SOURCEFREE compatibility preflight; NOT integrated G5.
set -Eeuo pipefail
ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"
EXPECTED="integration/pyat998-r6-s2a-joined-staging-20261115-r1"
ACTUAL="$(git branch --show-current)"
if [[ "$ACTUAL" != "$EXPECTED" && "${ALLOW_DETACHED_PYAT998:-0}" != "1" ]]; then
  echo "REFUSE: wrong branch ($ACTUAL). Use $EXPECTED or explicit pinned detached checkout." >&2; exit 2
fi
if [[ -n "$(git status --porcelain)" ]]; then
  echo "REFUSE: dirty source tree; use a fresh independent worktree." >&2; exit 2
fi
PY="${PYTHON_BIN:-python3}"
LOGROOT="$(mktemp -d /tmp/pyat998-joined-preflight.XXXXXX)"
export PYTHONPATH="$ROOT${PYTHONPATH:+:$PYTHONPATH}"
printf "REF=%s\\nBRANCH=%s\\nLOGDIR=%s\\n" "$(git rev-parse HEAD)" "$ACTUAL" "$LOGROOT" | tee "$LOGROOT/cut.txt"

"$PY" - <<'PY' | tee "$LOGROOT/blob_custody.txt"
import json, pathlib, subprocess
root=pathlib.Path.cwd()
p=root/"WORKER_RETURNS/PYAT998_STAGING/r6_s2a_accepted_blob_supplement_20261115.json"
m=json.loads(p.read_text())
assert len(m["files"])==17
for row in m["files"]:
    f=root/row["path"]
    assert f.is_file(), f"Missing {f}"
    actual=subprocess.check_output(["git","hash-object",str(f)],text=True).strip()
    assert actual==row["source_blob"]==row["integration_blob"], f"Wrong accepted blob {row['path']}"
print("PASS 17/17 accepted #997 R6 and #999 S2-A blobs")
PY

"$PY" - <<'PY' | tee "$LOGROOT/environment.txt"
import sys,platform,pytest,pyarrow,pandas,pyreadstat
print("Python",sys.version,"OS",platform.platform())
for mod in (pytest,pyarrow,pandas,pyreadstat):
    print(mod.__name__,getattr(mod,"__version__","installed"))
PY

run_suite() {
  local label="$1"; shift
  echo "RUN $label" | tee -a "$LOGROOT/sequence.txt"
  "$PY" -B -m pytest -q -o addopts='' -p no:cacheprovider "$@" 2>&1 | tee "$LOGROOT/$label.log"
  echo "PASS $label" | tee -a "$LOGROOT/sequence.txt"
}
run_suite r6_saved_body_issuer \
  rawlsing_next/tests/test_pyat997_s1e_source_saved_body_bridge.py \
  rawlsing_next/tests/test_pyat997_s1e_saved_native_first_consumer.py \
  rawlsing_next/tests/test_pyat997_s1e_saved_source_bridge.py
run_suite s2a_truth_and_physical \
  rawlsing_next/tests/test_pre553_s2a_public_selector_h26.py \
  rawlsing_next/tests/test_pre553_source_direct_parquet_estate.py
run_suite native_learned_consumers \
  rawlsing_next/tests/test_pyat991_s2d_five_readers.py \
  rawlsing_next/tests/test_pyat919_s2e_a3_native_closure.py \
  rawlsing_next/tests/test_pyat960_s2g_durable_lifecycle.py
run_suite old_world_binding_red rawlsing_next/tests/test_universal_world_binding.py
echo "PREFLIGHT_ONLY: NO JOINED FIRST-CONSUMER G5; NO SOURCE/NATIVE SCIENCE; NO PROTECTED CAS" | tee "$LOGROOT/VERDICT.txt"
echo "Logs: $LOGROOT"
