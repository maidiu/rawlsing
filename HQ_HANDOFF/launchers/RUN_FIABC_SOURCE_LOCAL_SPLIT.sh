#!/usr/bin/env bash
set -euo pipefail

EXPECTED_EXECUTION_BRANCH="agent/rabochii-prev3-ee-p2x-final-abc-equal-work-execution-r1"
EXPECTED_EXECUTION_HEAD="3d8f2ad62600b6777dcb23a28404a067502e77a0"
EXPECTED_CONTROL_BRANCH="agent/vozhd-fiabc-source-split-alternate-runner-r1"

LITS_SOURCE_SHA256="7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09"
WVS_SOURCE_SHA256="2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d"

LITS_ORACLE_SHA256="cb1c6ae6f9ddef15d41897451ac9f60208d4615ea60ddbeaef8874ba1000e3f4"
WVS_ORACLE_SHA256="869e72112978949e349140b74ab1b4d4966923c9ccedef518e3db9b3f54f3194"
T3_SHA256="7dfb62362b983b92dee2774d862a46c0c0ce3ca2c3bb48850e0f400346936908"
STOP_IDENTITY_SHA256="203fae32dc31ad6afe6dd2e85aed0ddf1a262d9a93efa6597a0c09173c64b384"
LITS_ORACLE_IDENTITY_SHA256="e5d66db4b6f8339672b0f4828b72a8df68b5525bf71ecfda899d0531d618a98a"
WVS_ORACLE_IDENTITY_SHA256="e546c15533ba138be9995095059ea3b70b64a6d7b5765e3789935cff7342ef00"

ANSWER_KEY_ROOT="WORKER_RETURNS/PREMAIN-FIABC-LITS-INDEPENDENT-ACCEPTANCE-T3-FREEZE-R1"
LITS_ORACLE_REL="$ANSWER_KEY_ROOT/court/oracles/LITS_I.standard.json"
WVS_ORACLE_REL="$ANSWER_KEY_ROOT/court/oracles/WVS7.standard.json"
T3_REL="$ANSWER_KEY_ROOT/court/t3/frozen-upstream.json"
STOP_REL="$ANSWER_KEY_ROOT/PRE_CANDIDATE_STOP.json"
CONTINUATION_MAP="WORKER_RETURNS/FIABC-T2/01_SIX_CELL_EXECUTION_MANIFEST.json"
COURT_CONTRACT="WORKER_RETURNS/FIABC-T5/04_CURRENT_SIX_CELL_COURT_CONTRACT.json"
BACKEND_MODULE="rawlsing_next.ee_p2x_process_isolated_backend"

usage() {
  cat >&2 <<'EOF'
Usage:
  SOURCE=LITS_I SOURCE_PATH=/path/to/LiTS_I.dta \
  WORK_ROOT=/persistent/fresh/root FIABC_REPO_ROOT=/path/to/protected-checkout \
  PYTHON_BIN=/path/to/pinned/python \
  bash HQ_HANDOFF/launchers/RUN_FIABC_SOURCE_LOCAL_SPLIT.sh

or SOURCE=WVS7 with SOURCE_PATH pointing to the exact canonical WVS7 SAV.

This is an ALTERNATE source-local runner. It executes A->B->C for exactly one
source and never runs/claims six-cell S17 completion.
EOF
  exit 2
}

die() {
  printf 'FIABC_SOURCE_LOCAL_LAUNCH_BLOCKED: %s\n' "$*" >&2
  exit 2
}

: "${SOURCE:?set SOURCE to LITS_I or WVS7}"
: "${SOURCE_PATH:?set SOURCE_PATH to the selected exact canonical source}"
: "${WORK_ROOT:?set WORK_ROOT to a fresh persistent root outside temporary directories}"
: "${FIABC_REPO_ROOT:?set FIABC_REPO_ROOT to the protected execution checkout}"
PYTHON_BIN="${PYTHON_BIN:-python3}"

case "$SOURCE" in
  LITS_I) EXPECTED_SOURCE_SHA256="$LITS_SOURCE_SHA256" ;;
  WVS7) EXPECTED_SOURCE_SHA256="$WVS_SOURCE_SHA256" ;;
  *) usage ;;
esac

command -v "$PYTHON_BIN" >/dev/null 2>&1 || die "Python interpreter not found: $PYTHON_BIN"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_LOCAL_DRIVER="$SCRIPT_DIR/FIABC_SOURCE_LOCAL_SPLIT_DRIVER.py"
[[ -f "$SOURCE_LOCAL_DRIVER" ]] || die "source-local driver missing: $SOURCE_LOCAL_DRIVER"

CONTROL_ROOT="$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel 2>/dev/null)" || die "launcher must live in a Git checkout"
CONTROL_BRANCH="$(git -C "$CONTROL_ROOT" branch --show-current)"
CONTROL_HEAD="$(git -C "$CONTROL_ROOT" rev-parse --verify HEAD^{commit})"
[[ "$CONTROL_BRANCH" == "$EXPECTED_CONTROL_BRANCH" ]] || die "wrong control branch: $CONTROL_BRANCH"
[[ -z "$(git -C "$CONTROL_ROOT" status --porcelain --untracked-files=all)" ]] || die "control checkout is dirty"

LAUNCHER_SHA256="$(shasum -a 256 "${BASH_SOURCE[0]}" | awk '{print $1}')"
SOURCE_LOCAL_DRIVER_SHA256="$(shasum -a 256 "$SOURCE_LOCAL_DRIVER" | awk '{print $1}')"
export RAWLSING_FIABC_SPLIT_CONTROL_HEAD="$CONTROL_HEAD"
export RAWLSING_FIABC_SPLIT_RUNNER_SHA256="$LAUNCHER_SHA256"

FIABC_REPO_ROOT="$("$PYTHON_BIN" - "$FIABC_REPO_ROOT" <<'PY'
from pathlib import Path
import sys
print(Path(sys.argv[1]).resolve())
PY
)"
WORK_ROOT="$("$PYTHON_BIN" - "$WORK_ROOT" <<'PY'
from pathlib import Path
import sys
print(Path(sys.argv[1]).resolve())
PY
)"
SOURCE_PATH="$("$PYTHON_BIN" - "$SOURCE_PATH" <<'PY'
from pathlib import Path
import sys
print(Path(sys.argv[1]).resolve())
PY
)"

case "$WORK_ROOT" in
  /private/tmp|/private/tmp/*|/tmp|/tmp/*) die "WORK_ROOT must be persistent and outside temporary directories" ;;
esac

"$PYTHON_BIN" - "$FIABC_REPO_ROOT" "$WORK_ROOT" <<'PY'
from pathlib import Path
import sys
repo = Path(sys.argv[1]).resolve()
work = Path(sys.argv[2]).resolve()
try:
    work.relative_to(repo)
except ValueError:
    pass
else:
    raise SystemExit("FIABC_SOURCE_LOCAL_LAUNCH_BLOCKED: WORK_ROOT must be outside execution checkout")
PY

cd "$FIABC_REPO_ROOT"
[[ "$(git branch --show-current)" == "$EXPECTED_EXECUTION_BRANCH" ]] || die "wrong execution branch"
[[ "$(git rev-parse --verify HEAD^{commit})" == "$EXPECTED_EXECUTION_HEAD" ]] || die "wrong execution HEAD"
[[ -z "$(git status --porcelain --untracked-files=all)" ]] || die "protected execution checkout is dirty"

IMMUTABLE_SUCCESSION_EVIDENCE_COMMITS=(
  "0b96b8de9aac774566f872cf0630ebd4ddeb70e6"
  "76c73e5c15eb512fa0b3217bc9e313d2b54f9a2d"
  "0c0dd1f23bc59017552afdbd5af2021f051d48f7"
)
for commit in "${IMMUTABLE_SUCCESSION_EVIDENCE_COMMITS[@]}"; do
  if ! git cat-file -e "${commit}^{commit}" 2>/dev/null; then
    git fetch --no-tags origin "$commit"
  fi
  git cat-file -e "${commit}^{commit}" 2>/dev/null || die "immutable succession evidence unavailable: $commit"
done

for p in "$LITS_ORACLE_REL" "$WVS_ORACLE_REL" "$T3_REL" "$STOP_REL" "$CONTINUATION_MAP" "$COURT_CONTRACT"; do
  [[ -f "$p" ]] || die "required governed file missing: $p"
done
[[ -f "$SOURCE_PATH" ]] || die "selected source missing: $SOURCE_PATH"

"$PYTHON_BIN" - <<'PY'
import importlib.metadata
import platform
expected = {
    "implementation": "CPython",
    "python": "3.11.3",
    "pyreadstat": "1.3.6",
    "pyarrow": "25.0.1",
    "pandas": "2.3.1",
    "numpy": "2.3.2",
    "system": "Darwin",
    "machine": "x86_64",
}
observed = {
    "implementation": platform.python_implementation(),
    "python": platform.python_version(),
    "pyreadstat": importlib.metadata.version("pyreadstat"),
    "pyarrow": importlib.metadata.version("pyarrow"),
    "pandas": importlib.metadata.version("pandas"),
    "numpy": importlib.metadata.version("numpy"),
    "system": platform.system(),
    "machine": platform.machine(),
}
if observed != expected:
    raise SystemExit(f"FIABC_SOURCE_LOCAL_LAUNCH_BLOCKED: runtime mismatch: expected={expected!r} observed={observed!r}")
print("FIABC_SOURCE_LOCAL_RUNTIME_GATE_PASS", observed)
PY

"$PYTHON_BIN" - "$SOURCE" "$SOURCE_PATH" "$EXPECTED_SOURCE_SHA256" <<'PY'
import hashlib
from pathlib import Path
import sys
label, raw, expected = sys.argv[1:]
h = hashlib.sha256()
with Path(raw).open("rb") as fh:
    for block in iter(lambda: fh.read(8 * 1024 * 1024), b""):
        h.update(block)
got = h.hexdigest()
if got != expected:
    raise SystemExit(f"FIABC_SOURCE_LOCAL_LAUNCH_BLOCKED: {label} SHA mismatch: {got}")
print("FIABC_SOURCE_LOCAL_SOURCE_SHA_PASS", label, got)
PY

if [[ -e "$WORK_ROOT" ]]; then
  [[ ! -L "$WORK_ROOT" ]] || die "WORK_ROOT may not be a symlink"
  if [[ -n "$(find "$WORK_ROOT" -mindepth 1 -maxdepth 1 -print -quit)" ]]; then
    die "WORK_ROOT must be fresh and empty: $WORK_ROOT"
  fi
else
  mkdir -p "$WORK_ROOT"
fi

mkdir -p "$WORK_ROOT/court/oracles" "$WORK_ROOT/court/t3" "$WORK_ROOT/court/logs"
cp "$LITS_ORACLE_REL" "$WORK_ROOT/court/oracles/LITS_I.standard.json"
cp "$WVS_ORACLE_REL" "$WORK_ROOT/court/oracles/WVS7.standard.json"
cp "$T3_REL" "$WORK_ROOT/court/t3/frozen-upstream.json"
cp "$STOP_REL" "$WORK_ROOT/court/PRE_CANDIDATE_STOP.json"

"$PYTHON_BIN" - \
  "$WORK_ROOT/court/oracles/LITS_I.standard.json" "$LITS_ORACLE_SHA256" \
  "$WORK_ROOT/court/oracles/WVS7.standard.json" "$WVS_ORACLE_SHA256" \
  "$WORK_ROOT/court/t3/frozen-upstream.json" "$T3_SHA256" \
  "$WORK_ROOT/court/PRE_CANDIDATE_STOP.json" "$STOP_IDENTITY_SHA256" \
  "$LITS_ORACLE_IDENTITY_SHA256" "$WVS_ORACLE_IDENTITY_SHA256" <<'PY'
import hashlib
import json
from pathlib import Path
import sys

def sha(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as fh:
        for block in iter(lambda: fh.read(8 * 1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

pairs = [
    (sys.argv[1], sys.argv[2], "LiTS oracle"),
    (sys.argv[3], sys.argv[4], "WVS7 oracle"),
    (sys.argv[5], sys.argv[6], "T3"),
]
for path, expected, label in pairs:
    got = sha(path)
    if got != expected:
        raise SystemExit(f"FIABC_SOURCE_LOCAL_LAUNCH_BLOCKED: {label} hash mismatch: {got}")

stop = json.loads(Path(sys.argv[7]).read_text(encoding="utf-8"))
checks = {
    "status": stop.get("status") == "PRE_CANDIDATE_STOP",
    "stop_identity": stop.get("stop_identity_sha256") == sys.argv[8],
    "t3_sha": stop.get("t3_receipt_sha256") == sys.argv[6],
    "candidate_processes": stop.get("candidate_processes_started") == 0,
    "candidate_outputs": stop.get("candidate_outputs_seen") == 0,
    "candidate_roots": stop.get("candidate_owned_roots_consulted") == [],
    "candidate_state": stop.get("candidate_owned_state_reused") is False,
    "lits_oracle_identity": stop.get("oracle_identities_frozen", {}).get("LITS_I", {}).get("oracle_identity_sha256") == sys.argv[9],
    "wvs_oracle_identity": stop.get("oracle_identities_frozen", {}).get("WVS7", {}).get("oracle_identity_sha256") == sys.argv[10],
}
bad = [name for name, ok in checks.items() if not ok]
if bad:
    raise SystemExit(f"FIABC_SOURCE_LOCAL_LAUNCH_BLOCKED: PRE_CANDIDATE_STOP invariant failure: {bad}")
print("FIABC_SOURCE_LOCAL_FROZEN_INPUTS_PASS")
PY

SUCCESSION_MANIFEST="$WORK_ROOT/court/fiabc_i07_current_head_succession_manifest.json"
LIFECYCLE_CONTEXT="$WORK_ROOT/court/fiabc_p10_lifecycle_context.json"
SUCCESSION_PRODUCER_RECEIPT="$WORK_ROOT/court/fiabc_i07_p10_producer_receipt.json"
DIRECT_PREFLIGHT="$WORK_ROOT/court/fiabc_i07_direct_preflight.json"
T5_PREFLIGHT="$WORK_ROOT/court/fiabc_t5_succession_preflight.json"

"$PYTHON_BIN" -B -m rawlsing_next.fiabc_succession_producer \
  --repo-root "$FIABC_REPO_ROOT" \
  --expected-head "$EXPECTED_EXECUTION_HEAD" \
  --manifest-output "$SUCCESSION_MANIFEST" \
  --lifecycle-output "$LIFECYCLE_CONTEXT" \
  --receipt-output "$SUCCESSION_PRODUCER_RECEIPT"

"$PYTHON_BIN" -B -m rawlsing_next.fiabc_succession_preflight \
  --manifest "$SUCCESSION_MANIFEST" \
  --lifecycle-context "$LIFECYCLE_CONTEXT" \
  --repo-root "$FIABC_REPO_ROOT" \
  --output "$DIRECT_PREFLIGHT"

"$PYTHON_BIN" -B "$SOURCE_LOCAL_DRIVER" \
  --preflight \
  --source "$SOURCE" \
  --continuation-map "$FIABC_REPO_ROOT/$CONTINUATION_MAP" \
  --current-court-contract "$FIABC_REPO_ROOT/$COURT_CONTRACT" \
  --work-root "$WORK_ROOT" \
  --repo-root "$FIABC_REPO_ROOT" \
  --source-path "$SOURCE_PATH" \
  --frozen-upstream-receipt "$WORK_ROOT/court/t3/frozen-upstream.json" \
  --succession-manifest "$SUCCESSION_MANIFEST" \
  --succession-lifecycle-context "$LIFECYCLE_CONTEXT" \
  >"$WORK_ROOT/court/logs/source_local_preflight.stdout.log" \
  2>"$WORK_ROOT/court/logs/source_local_preflight.stderr.log"

[[ -f "$T5_PREFLIGHT" ]] || die "source-local preflight did not emit T5 succession preflight"

"$PYTHON_BIN" - "$WORK_ROOT/cells" <<'PY'
from pathlib import Path
import sys
cells = Path(sys.argv[1])
if cells.exists() and any(p.is_file() for p in cells.rglob("*")):
    raise SystemExit("FIABC_SOURCE_LOCAL_LAUNCH_BLOCKED: candidate cell artifacts appeared during source-local preflight")
print("FIABC_SOURCE_LOCAL_ZERO_CANDIDATE_STATE_PASS")
PY

"$PYTHON_BIN" - "$WORK_ROOT" "$SOURCE" "$CONTROL_HEAD" "$LAUNCHER_SHA256" "$SOURCE_LOCAL_DRIVER_SHA256" <<'PY'
import json
from pathlib import Path
import platform
import sys
root = Path(sys.argv[1])
payload = {
    "schema": "RAWLSING_FIABC_SOURCE_LOCAL_LAUNCH_RECEIPT@1.0.0",
    "state": "SOURCE_LOCAL_PREFLIGHT_GREEN__ENTERING_MEASURED_SOURCE_BLOCK",
    "source": sys.argv[2],
    "execution_head": "3d8f2ad62600b6777dcb23a28404a067502e77a0",
    "control_head": sys.argv[3],
    "launcher_sha256": sys.argv[4],
    "source_local_driver_sha256": sys.argv[5],
    "host": {
        "system": platform.system(),
        "machine": platform.machine(),
        "python": platform.python_version(),
        "macos_version": platform.mac_ver()[0],
    },
    "six_cell_s17_authorized": False,
    "p2_synthesis_authorized": False,
}
(root / "court" / "source_local_launcher_receipt.json").write_text(
    json.dumps(payload, sort_keys=True, indent=2) + "\n", encoding="utf-8"
)
PY

printf '%s\n' "FIABC_SOURCE_LOCAL_PREFLIGHT_GREEN__STARTING_${SOURCE}_ABC_BLOCK"
printf '%s\n' "SOURCE=$SOURCE"
printf '%s\n' "WORK_ROOT=$WORK_ROOT"
printf '%s\n' "EXECUTION_HEAD=$EXPECTED_EXECUTION_HEAD"
printf '%s\n' "CONTROL_HEAD=$CONTROL_HEAD"

set +e
"$PYTHON_BIN" "$SOURCE_LOCAL_DRIVER" \
  --run \
  --source "$SOURCE" \
  --continuation-map "$FIABC_REPO_ROOT/$CONTINUATION_MAP" \
  --current-court-contract "$FIABC_REPO_ROOT/$COURT_CONTRACT" \
  --work-root "$WORK_ROOT" \
  --repo-root "$FIABC_REPO_ROOT" \
  --source-path "$SOURCE_PATH" \
  --backend-module "$BACKEND_MODULE" \
  --frozen-upstream-receipt "$WORK_ROOT/court/t3/frozen-upstream.json" \
  --succession-preflight-receipt "$T5_PREFLIGHT" \
  >"$WORK_ROOT/court/logs/source_local_measured.stdout.log" \
  2> >(tee "$WORK_ROOT/court/logs/source_local_measured.stderr.log" >&2)
rc=$?
set -e

printf '%s\n' "$rc" >"$WORK_ROOT/court/source_local_measured.exit_code"
if [[ "$rc" -ne 0 ]]; then
  printf 'FIABC_SOURCE_LOCAL_MEASURED_BLOCK_STOPPED__EXIT_%s\n' "$rc" >&2
  printf 'PRESERVE_WORK_ROOT=%s\n' "$WORK_ROOT" >&2
  exit "$rc"
fi

[[ -f "$WORK_ROOT/court/source_local_terminal.json" ]] || die "source-local terminal receipt absent after zero exit"

printf '%s\n' "FIABC_SOURCE_LOCAL_MEASURED_BLOCK_EXITED_ZERO"
printf '%s\n' "SOURCE_LOCAL_TERMINAL=$WORK_ROOT/court/source_local_terminal.json"
printf '%s\n' "PRESERVE_WORK_ROOT=$WORK_ROOT"
printf '%s\n' "SIX_CELL_S17_NOT_EXECUTED"
