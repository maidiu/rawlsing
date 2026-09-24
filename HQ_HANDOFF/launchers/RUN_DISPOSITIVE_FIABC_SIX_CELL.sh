#!/usr/bin/env bash
set -euo pipefail

EXPECTED_BRANCH="agent/rabochii-prev3-ee-p2x-final-abc-equal-work-execution-r1"
EXPECTED_HEAD="b53ff08921af263b9db4d1ad038f35fbc12b990a"

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

: "${LITS_PATH:?set LITS_PATH to the exact canonical LiTS-I source}"
: "${WVS_PATH:?set WVS_PATH to the exact canonical WVS7 source}"
: "${WORK_ROOT:?set WORK_ROOT to a fresh persistent court root outside /private/tmp and /tmp}"

FIABC_REPO_ROOT="${FIABC_REPO_ROOT:-$PWD}"
PYTHON_BIN="${PYTHON_BIN:-python3}"

die() {
  printf 'FIABC_DISPOSITIVE_LAUNCH_BLOCKED: %s\n' "$*" >&2
  exit 2
}

command -v "$PYTHON_BIN" >/dev/null 2>&1 || die "Python interpreter not found: $PYTHON_BIN"

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
LITS_PATH="$("$PYTHON_BIN" - "$LITS_PATH" <<'PY'
from pathlib import Path
import sys
print(Path(sys.argv[1]).resolve())
PY
)"
WVS_PATH="$("$PYTHON_BIN" - "$WVS_PATH" <<'PY'
from pathlib import Path
import sys
print(Path(sys.argv[1]).resolve())
PY
)"

case "$WORK_ROOT" in
  /private/tmp|/private/tmp/*|/tmp|/tmp/*) die "WORK_ROOT must be persistent and outside temporary directories: $WORK_ROOT" ;;
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
    raise SystemExit("FIABC_DISPOSITIVE_LAUNCH_BLOCKED: WORK_ROOT must be outside the repository checkout")
PY

cd "$FIABC_REPO_ROOT"

[[ "$(git branch --show-current)" == "$EXPECTED_BRANCH" ]] || die "wrong branch: expected $EXPECTED_BRANCH"
[[ "$(git rev-parse --verify HEAD^{commit})" == "$EXPECTED_HEAD" ]] || die "wrong HEAD: expected $EXPECTED_HEAD"
[[ -z "$(git status --porcelain --untracked-files=all)" ]] || die "protected execution worktree is dirty"

IMMUTABLE_SUCCESSION_EVIDENCE_COMMITS=(
  "0b96b8de9aac774566f872cf0630ebd4ddeb70e6"
  "76c73e5c15eb512fa0b3217bc9e313d2b54f9a2d"
  "0c0dd1f23bc59017552afdbd5af2021f051d48f7"
)
for commit in "${IMMUTABLE_SUCCESSION_EVIDENCE_COMMITS[@]}"; do
  if ! git cat-file -e "${commit}^{commit}" 2>/dev/null; then
    git fetch --no-tags origin "$commit"
  fi
  git cat-file -e "${commit}^{commit}" 2>/dev/null || die "immutable succession evidence commit unavailable: $commit"
done
echo "FIABC_IMMUTABLE_SUCCESSION_EVIDENCE_FETCH_PASS ${IMMUTABLE_SUCCESSION_EVIDENCE_COMMITS[*]}"

[[ -f "$LITS_PATH" ]] || die "LiTS source missing: $LITS_PATH"
[[ -f "$WVS_PATH" ]] || die "WVS7 source missing: $WVS_PATH"

for p in "$LITS_ORACLE_REL" "$WVS_ORACLE_REL" "$T3_REL" "$STOP_REL" "$CONTINUATION_MAP" "$COURT_CONTRACT"; do
  [[ -f "$p" ]] || die "required governed file missing: $p"
done

"$PYTHON_BIN" - <<'PY'
import importlib.metadata
import platform
import sys
expected = {
    "implementation": "CPython",
    "python": "3.11.3",
    "pyreadstat": "1.3.6",
    "pyarrow": "25.0.1",
    "system": "Darwin",
    "machine": "x86_64",
}
observed = {
    "implementation": platform.python_implementation(),
    "python": platform.python_version(),
    "pyreadstat": importlib.metadata.version("pyreadstat"),
    "pyarrow": importlib.metadata.version("pyarrow"),
    "system": platform.system(),
    "machine": platform.machine(),
}
if observed != expected:
    raise SystemExit(f"FIABC_DISPOSITIVE_LAUNCH_BLOCKED: runtime mismatch: expected={expected!r} observed={observed!r}")
print("FIABC_RUNTIME_GATE_PASS", observed)
PY

"$PYTHON_BIN" - "$LITS_PATH" "$WVS_PATH" "$LITS_SOURCE_SHA256" "$WVS_SOURCE_SHA256" <<'PY'
import hashlib
from pathlib import Path
import sys

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(8 * 1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

for label, raw, expected in (
    ("LITS_I", sys.argv[1], sys.argv[3]),
    ("WVS7", sys.argv[2], sys.argv[4]),
):
    got = sha256(Path(raw))
    if got != expected:
        raise SystemExit(f"FIABC_DISPOSITIVE_LAUNCH_BLOCKED: {label} SHA mismatch: {got}")
    print("FIABC_SOURCE_SHA_PASS", label, got)
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

"$PYTHON_BIN" -   "$WORK_ROOT/court/oracles/LITS_I.standard.json" "$LITS_ORACLE_SHA256"   "$WORK_ROOT/court/oracles/WVS7.standard.json" "$WVS_ORACLE_SHA256"   "$WORK_ROOT/court/t3/frozen-upstream.json" "$T3_SHA256"   "$WORK_ROOT/court/PRE_CANDIDATE_STOP.json" "$STOP_IDENTITY_SHA256"   "$LITS_ORACLE_IDENTITY_SHA256" "$WVS_ORACLE_IDENTITY_SHA256" <<'PY'
import hashlib
import json
from pathlib import Path
import sys

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(8 * 1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

pairs = [
    (Path(sys.argv[1]), sys.argv[2], "LiTS oracle"),
    (Path(sys.argv[3]), sys.argv[4], "WVS7 oracle"),
    (Path(sys.argv[5]), sys.argv[6], "T3"),
]
for path, expected, label in pairs:
    got = sha256(path)
    if got != expected:
        raise SystemExit(f"FIABC_DISPOSITIVE_LAUNCH_BLOCKED: {label} hash mismatch: {got}")
    print("FIABC_FROZEN_INPUT_SHA_PASS", label, got)

stop_path = Path(sys.argv[7])
stop_identity = sys.argv[8]
lits_identity = sys.argv[9]
wvs_identity = sys.argv[10]
stop = json.loads(stop_path.read_text(encoding="utf-8"))
checks = {
    "status": stop.get("status") == "PRE_CANDIDATE_STOP",
    "stop_identity": stop.get("stop_identity_sha256") == stop_identity,
    "t3_sha": stop.get("t3_receipt_sha256") == sys.argv[6],
    "candidate_processes": stop.get("candidate_processes_started") == 0,
    "candidate_outputs": stop.get("candidate_outputs_seen") == 0,
    "candidate_roots": stop.get("candidate_owned_roots_consulted") == [],
    "candidate_state": stop.get("candidate_owned_state_reused") is False,
    "lits_oracle_identity": stop.get("oracle_identities_frozen", {}).get("LITS_I", {}).get("oracle_identity_sha256") == lits_identity,
    "wvs_oracle_identity": stop.get("oracle_identities_frozen", {}).get("WVS7", {}).get("oracle_identity_sha256") == wvs_identity,
}
bad = [name for name, ok in checks.items() if not ok]
if bad:
    raise SystemExit(f"FIABC_DISPOSITIVE_LAUNCH_BLOCKED: PRE_CANDIDATE_STOP invariant failure: {bad}")
print("FIABC_PRE_CANDIDATE_STOP_PASS", stop_identity)
PY

HEAD="$(git rev-parse --verify HEAD^{commit})"
SUCCESSION_MANIFEST="$WORK_ROOT/court/fiabc_i07_current_head_succession_manifest.json"
LIFECYCLE_CONTEXT="$WORK_ROOT/court/fiabc_p10_lifecycle_context.json"
SUCCESSION_PRODUCER_RECEIPT="$WORK_ROOT/court/fiabc_i07_p10_producer_receipt.json"
DIRECT_PREFLIGHT="$WORK_ROOT/court/fiabc_i07_direct_preflight.json"
T5_PREFLIGHT="$WORK_ROOT/court/fiabc_t5_succession_preflight.json"

"$PYTHON_BIN" -B -m rawlsing_next.fiabc_succession_producer   --repo-root "$FIABC_REPO_ROOT"   --expected-head "$HEAD"   --manifest-output "$SUCCESSION_MANIFEST"   --lifecycle-output "$LIFECYCLE_CONTEXT"   --receipt-output "$SUCCESSION_PRODUCER_RECEIPT"

"$PYTHON_BIN" -B -m rawlsing_next.fiabc_succession_preflight   --manifest "$SUCCESSION_MANIFEST"   --lifecycle-context "$LIFECYCLE_CONTEXT"   --repo-root "$FIABC_REPO_ROOT"   --output "$DIRECT_PREFLIGHT"

"$PYTHON_BIN" -B rawlsing_next/ee_p2x_darwin_court_driver.py   --preflight   --continuation-map "$CONTINUATION_MAP"   --current-court-contract "$COURT_CONTRACT"   --succession-manifest "$SUCCESSION_MANIFEST"   --succession-lifecycle-context "$LIFECYCLE_CONTEXT"   --work-root "$WORK_ROOT"   --repo-root "$FIABC_REPO_ROOT"   --lits-path "$LITS_PATH"   --wvs-path "$WVS_PATH"   >"$WORK_ROOT/court/logs/preflight.stdout.log"   2>"$WORK_ROOT/court/logs/preflight.stderr.log"

[[ -f "$T5_PREFLIGHT" ]] || die "driver preflight did not emit $T5_PREFLIGHT"

if [[ -d "$WORK_ROOT/cells" ]] && [[ -n "$(find "$WORK_ROOT/cells" -type f -print -quit)" ]]; then
  die "candidate cell artifacts appeared during preflight"
fi

"$PYTHON_BIN" - "$T5_PREFLIGHT" "$WORK_ROOT/court/t3/frozen-upstream.json" "$T3_SHA256" <<'PY'
import hashlib
import json
from pathlib import Path
import sys

preflight = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
status = str(preflight.get("status", ""))
if "PASS" not in status and preflight.get("passed") is not True:
    raise SystemExit(f"FIABC_DISPOSITIVE_LAUNCH_BLOCKED: succession preflight not PASS: {status!r}")

h = hashlib.sha256(Path(sys.argv[2]).read_bytes()).hexdigest()
if h != sys.argv[3]:
    raise SystemExit(f"FIABC_DISPOSITIVE_LAUNCH_BLOCKED: T3 changed during preflight: {h}")
print("FIABC_SUCCESSION_PREFLIGHT_PASS", status)
print("FIABC_T3_STILL_FROZEN", h)
PY

"$PYTHON_BIN" - "$WORK_ROOT" "$FIABC_REPO_ROOT" "$HEAD" "$LITS_PATH" "$WVS_PATH" "$T3_SHA256" "$STOP_IDENTITY_SHA256" <<'PY'
import json
from pathlib import Path
import platform
import sys
payload = {
    "schema": "RAWLSING_FIABC_DISPOSITIVE_LAUNCH_RECEIPT@1.0.0",
    "state": "PRE_CANDIDATE_PREFLIGHT_GREEN__ENTERING_MEASURED_COURT",
    "work_root": sys.argv[1],
    "repo_root": sys.argv[2],
    "execution_head": sys.argv[3],
    "lits_path": sys.argv[4],
    "wvs_path": sys.argv[5],
    "t3_sha256": sys.argv[6],
    "pre_candidate_stop_identity_sha256": sys.argv[7],
    "host": {
        "system": platform.system(),
        "machine": platform.machine(),
        "python": platform.python_version(),
    },
}
Path(sys.argv[1], "court", "dispositive_launcher_receipt.json").write_text(
    json.dumps(payload, sort_keys=True, indent=2) + "\n",
    encoding="utf-8",
)
PY

printf '%s\n' "FIABC_DISPOSITIVE_PREFLIGHT_GREEN__STARTING_SIX_CELL_MEASURED_COURT"
printf '%s\n' "WORK_ROOT=$WORK_ROOT"
printf '%s\n' "EXECUTION_HEAD=$HEAD"
printf '%s\n' "T3_SHA256=$T3_SHA256"
printf '%s\n' "PRE_CANDIDATE_STOP=$STOP_IDENTITY_SHA256"

set +e
"$PYTHON_BIN" rawlsing_next/ee_p2x_darwin_court_driver.py   --run   --continuation-map "$CONTINUATION_MAP"   --current-court-contract "$COURT_CONTRACT"   --succession-preflight-receipt "$T5_PREFLIGHT"   --frozen-upstream-receipt "$WORK_ROOT/court/t3/frozen-upstream.json"   --backend-module "$BACKEND_MODULE"   --work-root "$WORK_ROOT"   --repo-root "$FIABC_REPO_ROOT"   --lits-path "$LITS_PATH"   --wvs-path "$WVS_PATH"   >"$WORK_ROOT/court/logs/measured_run.stdout.log"   2> >(tee "$WORK_ROOT/court/logs/measured_run.stderr.log" >&2)
rc=$?
set -e

printf '%s\n' "$rc" >"$WORK_ROOT/court/measured_run.exit_code"
if [[ "$rc" -ne 0 ]]; then
  printf 'FIABC_DISPOSITIVE_MEASURED_COURT_STOPPED__EXIT_%s\n' "$rc" >&2
  exit "$rc"
fi

printf '%s\n' "FIABC_DISPOSITIVE_MEASURED_COURT_PROCESS_EXITED_ZERO"
printf '%s\n' "PRESERVE_WORK_ROOT=$WORK_ROOT"
