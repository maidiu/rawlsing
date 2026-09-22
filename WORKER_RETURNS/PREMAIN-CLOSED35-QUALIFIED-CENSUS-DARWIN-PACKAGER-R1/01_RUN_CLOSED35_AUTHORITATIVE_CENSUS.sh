#!/bin/bash
set -euo pipefail
umask 077

EXPECTED_BRANCH="agent/rabochii-premain-closed35-qualified-representation-census-harness-r1"
EXPECTED_HEAD="efe8de2b032c93d1820fd3f8c82fe2f1acabbf87"
QUALIFIED_HEAD="11704fbfa16797fbdd55dadc7929aaad729c9454"
ESTATE_BRANCH="agent/rabochii-premain-closed35-source-estate-closure-r1"
ESTATE_HEAD="4e230628ae31b6b4de581f3a797e1d1bcb0047a0"
PACKAGER_BRANCH="agent/rabochii-premain-closed35-qualified-census-darwin-packager-r1"
RETURN_DIR="WORKER_RETURNS/PREMAIN-CLOSED35-QUALIFIED-CENSUS-DARWIN-PACKAGER-R1"
HARNESS_RUNNER="WORKER_RETURNS/PREMAIN-CLOSED35-QUALIFIED-REPRESENTATION-CENSUS-HARNESS-R1/02_RUN_CLOSED35_QUALIFIED_REPRESENTATION_CENSUS.sh"

if [[ $# -ne 3 ]]; then
  echo "usage: $0 <surveys.zip> <LITS-2006-data.dta> <WVS-Wave-7.sav.zip>" >&2
  exit 2
fi

SURVEYS_ZIP="$1"
LITS1="$2"
WVS7_ZIP="$3"
PYTHON_BIN="${PYTHON_BIN:-python3}"
RUN_ROOT="${RAWLSING_CLOSED35_RUN_ROOT:-$HOME/Library/Caches/Rawlsing/closed35-qualified-census-r1}"
STAGE_ROOT="$RUN_ROOT/staged_sources"
PATH_MANIFEST="$RUN_ROOT/CLOSED35_SOURCE_PATH_MANIFEST.json"
BINDING="$RUN_ROOT/PACKAGER_RUN_BINDING.json"
OUTPUT_ROOT="$RUN_ROOT/census_output"
PACKAGE_ROOT="$RUN_ROOT/package"

die() { echo "CLOSED35_PACKAGER BLOCKED: $*" >&2; exit 86; }
on_error() {
  rc=$?
  echo "CLOSED35_PACKAGER stopped with rc=$rc; partial immutable receipts, if any, remain under: $OUTPUT_ROOT" >&2
  exit "$rc"
}
trap on_error ERR

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null)" || die "run from the Rawlsing repository"
CURRENT_BRANCH="$(git -C "$REPO_ROOT" branch --show-current)"
CURRENT_HEAD="$(git -C "$REPO_ROOT" rev-parse HEAD)"
[[ "$CURRENT_BRANCH" == "$EXPECTED_BRANCH" ]] || die "wrong branch: $CURRENT_BRANCH"
[[ "$CURRENT_HEAD" == "$EXPECTED_HEAD" ]] || die "wrong harness head: $CURRENT_HEAD"
[[ -z "$(git -C "$REPO_ROOT" status --porcelain --untracked-files=all)" ]] || die "checkout is not clean"
git -C "$REPO_ROOT" merge-base --is-ancestor "$QUALIFIED_HEAD" "$CURRENT_HEAD" || die "qualified implementation ancestry failed"
[[ "$(uname -s)" == "Darwin" ]] || die "Darwin required"
[[ "$(uname -m)" == "x86_64" ]] || die "x86_64 required"

for f in "$SURVEYS_ZIP" "$LITS1" "$WVS7_ZIP"; do
  [[ -f "$f" ]] || die "carrier missing: $f"
done

if ! git -C "$REPO_ROOT" cat-file -e "$ESTATE_HEAD^{commit}" 2>/dev/null; then
  echo "[0/5] fetching pinned source-estate object"
  git -C "$REPO_ROOT" fetch --no-tags origin "$ESTATE_BRANCH"
  [[ "$(git -C "$REPO_ROOT" rev-parse FETCH_HEAD)" == "$ESTATE_HEAD" ]] || die "source-estate fetch did not resolve to pinned head"
fi

mkdir -p "$PACKAGE_ROOT"

resolve_packager_ref() {
  if [[ -n "${CLOSED35_PACKAGER_REF:-}" ]]; then
    git -C "$REPO_ROOT" rev-parse --verify "${CLOSED35_PACKAGER_REF}^{commit}" 2>/dev/null || return 1
    return 0
  fi
  for ref in "refs/heads/$PACKAGER_BRANCH" "refs/remotes/origin/$PACKAGER_BRANCH"; do
    if git -C "$REPO_ROOT" rev-parse --verify "$ref^{commit}" >/dev/null 2>&1; then
      CLOSED35_PACKAGER_REF="$(git -C "$REPO_ROOT" rev-parse "$ref^{commit}")"
      export CLOSED35_PACKAGER_REF
      return 0
    fi
  done
  return 1
}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" 2>/dev/null && pwd || true)"
if [[ -f "$SCRIPT_DIR/02_SOURCE_ESTATE_TO_PATH_MANIFEST.py" && -f "$SCRIPT_DIR/03_POSTRUN_RECEIPT_COMMIT.sh" ]]; then
  cp "$SCRIPT_DIR/02_SOURCE_ESTATE_TO_PATH_MANIFEST.py" "$PACKAGE_ROOT/02_SOURCE_ESTATE_TO_PATH_MANIFEST.py"
  cp "$SCRIPT_DIR/03_POSTRUN_RECEIPT_COMMIT.sh" "$PACKAGE_ROOT/03_POSTRUN_RECEIPT_COMMIT.sh"
else
  resolve_packager_ref || die "set CLOSED35_PACKAGER_REF to the fetched packager commit"
  PACKAGER_COMMIT="$(git -C "$REPO_ROOT" rev-parse "${CLOSED35_PACKAGER_REF}^{commit}")"
  git -C "$REPO_ROOT" show "$PACKAGER_COMMIT:$RETURN_DIR/02_SOURCE_ESTATE_TO_PATH_MANIFEST.py" > "$PACKAGE_ROOT/02_SOURCE_ESTATE_TO_PATH_MANIFEST.py"
  git -C "$REPO_ROOT" show "$PACKAGER_COMMIT:$RETURN_DIR/03_POSTRUN_RECEIPT_COMMIT.sh" > "$PACKAGE_ROOT/03_POSTRUN_RECEIPT_COMMIT.sh"
fi
chmod 700 "$PACKAGE_ROOT/02_SOURCE_ESTATE_TO_PATH_MANIFEST.py" "$PACKAGE_ROOT/03_POSTRUN_RECEIPT_COMMIT.sh"
BRIDGE="$PACKAGE_ROOT/02_SOURCE_ESTATE_TO_PATH_MANIFEST.py"

echo "[1/5] exact checkout/runtime preflight"
"$PYTHON_BIN" "$BRIDGE" preflight   --repo-root "$REPO_ROOT"   --surveys-zip "$SURVEYS_ZIP"   --lits1 "$LITS1"   --wvs7-zip "$WVS7_ZIP"

echo "[2/5] verify three carriers; stage exact CLOSED35 estate; emit path manifest"
"$PYTHON_BIN" "$BRIDGE" stage   --repo-root "$REPO_ROOT"   --surveys-zip "$SURVEYS_ZIP"   --lits1 "$LITS1"   --wvs7-zip "$WVS7_ZIP"   --stage-root "$STAGE_ROOT"   --manifest-out "$PATH_MANIFEST"   --binding-out "$BINDING"   --output-root "$OUTPUT_ROOT"

echo "[3/5] authoritative qualified CLOSED35 representation census"
export PYTHON_BIN
bash "$REPO_ROOT/$HARNESS_RUNNER" "$PATH_MANIFEST" "$OUTPUT_ROOT"

echo "[4/5] verify 35 immutable source receipts and six aggregates"
"$PYTHON_BIN" "$BRIDGE" verify-results --repo-root "$REPO_ROOT" --output-root "$OUTPUT_ROOT"

echo "[5/5] authoritative census receipt tree complete"
echo "results: $OUTPUT_ROOT"
echo "post-run local commit helper:"
printf '  bash %q %q\n' "$PACKAGE_ROOT/03_POSTRUN_RECEIPT_COMMIT.sh" "$OUTPUT_ROOT"
echo "NO CANDIDATE OR MEASURED-P2X EXECUTION WAS DISPATCHED BY THIS WRAPPER"
