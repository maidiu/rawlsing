#!/usr/bin/env bash
set -euo pipefail

# This script contains only existing validators/CLIs. It deliberately contains
# no invented command for the missing LiTS oracle, WVS-standardization, T3
# freeze, or current-head I07 producers.
#
# It can become executable end-to-end only after the blockers in
# 05_BLOCKERS_IF_ANY.md are repaired and this launch pack is regenerated at
# the exact repaired head.

: "${LITS_PATH:?set LITS_PATH to the exact canonical LITS-2006-data.dta}"
: "${WVS_PATH:?set WVS_PATH to the exact canonical WVS Wave 7.sav}"
: "${WORK_ROOT:?set WORK_ROOT to a new isolated court working root}"
: "${LITS_ORACLE:?set LITS_ORACLE to the standard frozen LiTS oracle document}"
: "${WVS_ORACLE:?set WVS_ORACLE to the standard frozen successor WVS oracle document}"
: "${FROZEN_UPSTREAM_RECEIPT:?set FROZEN_UPSTREAM_RECEIPT to the final T3 two-source freeze receipt}"
: "${SUCCESSION_MANIFEST:?set SUCCESSION_MANIFEST to the current-head frozen I07 succession manifest}"
: "${LIFECYCLE_CONTEXT:?set LIFECYCLE_CONTEXT to the governed P10 lifecycle/failure-scope context}"

[[ -z "$(git status --porcelain)" ]] || { echo "dirty worktree" >&2; exit 2; }

# Lock1 runtime gate. This imports no survey data.
python - <<'PY'
from rawlsing_next.ee_p2x_darwin_court_driver import observe_host, verify_runtime_gate
host = observe_host()
verify_runtime_gate(host)
print("FIABC_LOCK1_RUNTIME_PASS", host)
PY

# Exact source identity only. No semantic decode, no candidate execution.
python - "$LITS_PATH" "$WVS_PATH" <<'PY'
import hashlib
import sys
from pathlib import Path

expected = {
    "LITS_I": "7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09",
    "WVS7": "2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d",
}
for source, raw in zip(("LITS_I", "WVS7"), sys.argv[1:]):
    path = Path(raw)
    if not path.is_file():
        raise SystemExit(f"{source} file missing: {path}")
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(8 * 1024 * 1024), b""):
            h.update(block)
    got = h.hexdigest()
    if got != expected[source]:
        raise SystemExit(f"{source} SHA mismatch: {got}")
    print(f"FIABC_SOURCE_SHA_PASS {source} {got}")
PY

# Isolated court root. Do not reuse a prior measured root.
if [[ -e "$WORK_ROOT/ee_p2x_stage_ledger.json" || -e "$WORK_ROOT/cells" ]]; then
  echo "WORK_ROOT already contains court/candidate state; choose a fresh root" >&2
  exit 2
fi
mkdir -p "$WORK_ROOT/court"

# Existing source-free LiTS frontier proof: 50 candidates / 77 roles only.
# This is deliberately NOT represented as the missing exact current LiTS oracle.
python WORKER_RETURNS/FIABC-HQ-FINAL-PREFLIGHT-FANIN/lits_oracle_source_free_probe.py   > "$WORK_ROOT/court/lits_source_free_frontier_probe.log"

# Revalidate the accepted R1M WVS wrapper as an accepted candidate-neutral input.
python - <<'PY'
import json
from pathlib import Path
from rawlsing_next.pre553_empirical_objects import canonicalize, semantic_hash

p = Path("WORKER_RETURNS/FIABC-LM2-R1M-LOCK2-SUCCESSOR-R16-ORACLE/07_FRESH_WVS_ORACLE.json")
doc = json.loads(p.read_text())
body = {k: v for k, v in doc.items() if k not in {"oracle_identity_sha256", "freeze_receipt"}}
got = semantic_hash(canonicalize(body))
assert got == doc["oracle_identity_sha256"] == "3694b8bd0b5468433a1a83bd469337c7e36e552c3a9a5fef65fff88df8fce800"
assert doc["candidate_outputs_seen"] == 0
assert doc["candidate_processes_started"] == 0
assert doc["candidate_owned_roots_consulted"] == []
print("FIABC_ACCEPTED_R1M_WVS_ORACLE_INPUT_PASS", got)
PY

# These are consumers, not producers. They will fail if the missing pre-candidate
# glue has not generated standard oracle documents and the T3 freeze receipt.
python - "$LITS_ORACLE" "$WVS_ORACLE" "$FROZEN_UPSTREAM_RECEIPT" "$WORK_ROOT" <<'PY'
import json
import sys
from pathlib import Path

from rawlsing_next.pre553_independent_parity_oracle import verify_frozen_oracle
from rawlsing_next.ee_p2x_candidate_process_envelope import load_frozen_upstream_receipt
from rawlsing_next.fiabc_live_terminal_control import load_frozen_source_oracle

lits, wvs, freeze, work = map(Path, sys.argv[1:])
for source, path in (("LITS_I", lits), ("WVS7", wvs)):
    doc = json.loads(path.read_text())
    ident = verify_frozen_oracle(doc)
    assert doc["source"] == source
    print("FIABC_STANDARD_ORACLE_PASS", source, ident)

doc, freeze_sha = load_frozen_upstream_receipt(freeze)
assert doc["candidate_outputs_seen"] == 0
assert doc["candidate_owned_roots_consulted"] == []
for source in ("LITS_I", "WVS7"):
    oracle, _, _ = load_frozen_source_oracle(
        freeze_path=freeze, source=source, work_root=work
    )
    print("FIABC_T3_FROZEN_ORACLE_BINDING_PASS", source, oracle["oracle_identity_sha256"])
print("FIABC_T3_FREEZE_PASS", freeze_sha)
PY

# Existing I07 evaluator: the missing glue must have produced these exact inputs.
python -m rawlsing_next.fiabc_succession_preflight   --manifest "$SUCCESSION_MANIFEST"   --lifecycle-context "$LIFECYCLE_CONTEXT"   --repo-root "$PWD"   --output "$WORK_ROOT/court/i07_direct_preflight.json"

# Existing current driver preflight. This starts no A/B/C candidate process.
python rawlsing_next/ee_p2x_darwin_court_driver.py   --preflight   --continuation-map WORKER_RETURNS/FIABC-T2/01_SIX_CELL_EXECUTION_MANIFEST.json   --current-court-contract WORKER_RETURNS/FIABC-T5/04_CURRENT_SIX_CELL_COURT_CONTRACT.json   --succession-manifest "$SUCCESSION_MANIFEST"   --succession-lifecycle-context "$LIFECYCLE_CONTEXT"   --work-root "$WORK_ROOT"   --repo-root "$PWD"   --lits-path "$LITS_PATH"   --wvs-path "$WVS_PATH"

test -f "$WORK_ROOT/court/fiabc_t5_succession_preflight.json"
echo "FIABC_PRE_CANDIDATE_LOCAL_PREFLIGHT_GREEN__STOP_BEFORE_CANDIDATE_EXECUTION"
