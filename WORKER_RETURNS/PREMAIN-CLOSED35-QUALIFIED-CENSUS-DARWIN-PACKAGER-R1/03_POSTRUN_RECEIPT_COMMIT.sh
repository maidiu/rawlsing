#!/bin/bash
set -euo pipefail
umask 077

EXPECTED_BRANCH="agent/rabochii-premain-closed35-qualified-representation-census-harness-r1"
EXPECTED_HEAD="efe8de2b032c93d1820fd3f8c82fe2f1acabbf87"
RESULT_BRANCH="agent/rabochii-premain-closed35-qualified-representation-census-results-r1"
RESULT_DIR="WORKER_RETURNS/PREMAIN-CLOSED35-QUALIFIED-REPRESENTATION-CENSUS-RESULTS-R1"
AGGREGATES=(
  "CLOSED35_REPRESENTATION_OBSERVATIONS.json"
  "CLOSED35_TYPED_JOIN_MATRIX.csv"
  "CLOSED35_EDGE_PRESERVATION_RECEIPT.json"
  "CLOSED35_HISTORICAL_DEPENDENCY_PROVENANCE.json"
  "CLOSED35_RUNTIME_RECEIPT.json"
  "CLOSED35_CENSUS_SUMMARY.json"
)

if [[ $# -ne 1 ]]; then
  echo "usage: $0 <authoritative-census-output-root>" >&2
  exit 2
fi
OUTPUT_ROOT="$1"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BRIDGE="$SCRIPT_DIR/02_SOURCE_ESTATE_TO_PATH_MANIFEST.py"
PYTHON_BIN="${PYTHON_BIN:-python3}"

die() { echo "CLOSED35_POSTRUN_COMMIT BLOCKED: $*" >&2; exit 87; }

[[ -f "$BRIDGE" ]] || die "companion verifier missing: $BRIDGE"
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null)" || die "run from the Rawlsing repository"
[[ "$(git -C "$REPO_ROOT" branch --show-current)" == "$EXPECTED_BRANCH" ]] || die "must remain on frozen harness branch"
[[ "$(git -C "$REPO_ROOT" rev-parse HEAD)" == "$EXPECTED_HEAD" ]] || die "harness head drift"
[[ -z "$(git -C "$REPO_ROOT" status --porcelain --untracked-files=all)" ]] || die "checkout is not clean"

"$PYTHON_BIN" "$BRIDGE" verify-results --repo-root "$REPO_ROOT" --output-root "$OUTPUT_ROOT"

if find "$OUTPUT_ROOT" -type f \( -iname '*.sav' -o -iname '*.dta' -o -iname '*.zip' -o -iname '*.7z' -o -iname '*.rar' -o -iname '*.tar' -o -iname '*.gz' \) -print -quit | grep -q .; then
  die "raw survey/archive material is present in output tree"
fi
if find "$OUTPUT_ROOT" -type f | grep -Eiq '(candidate[_-]?[abc]|measured[_-]?p2x|measured[_-]?six[_-]?cell)'; then
  die "candidate or measured-P2X material is present in output tree"
fi

if git -C "$REPO_ROOT" show-ref --verify --quiet "refs/heads/$RESULT_BRANCH"; then
  git -C "$REPO_ROOT" merge-base --is-ancestor "$EXPECTED_HEAD" "$RESULT_BRANCH" || die "existing results branch is not descended from frozen harness head"
  spill="$(git -C "$REPO_ROOT" diff --name-only "$EXPECTED_HEAD..$RESULT_BRANCH" | grep -v "^$RESULT_DIR/" || true)"
  [[ -z "$spill" ]] || die "existing results branch contains out-of-scope paths: $spill"
fi

WT="$(mktemp -d "${TMPDIR:-/private/tmp}/closed35-results-worktree.XXXXXX")"
ADDED_WORKTREE=0
cleanup() {
  if [[ "$ADDED_WORKTREE" == 1 ]]; then
    git -C "$REPO_ROOT" worktree remove --force "$WT" >/dev/null 2>&1 || true
  fi
  rm -rf "$WT" >/dev/null 2>&1 || true
}
trap cleanup EXIT

if git -C "$REPO_ROOT" show-ref --verify --quiet "refs/heads/$RESULT_BRANCH"; then
  git -C "$REPO_ROOT" worktree add "$WT" "$RESULT_BRANCH"
else
  git -C "$REPO_ROOT" worktree add -b "$RESULT_BRANCH" "$WT" "$EXPECTED_HEAD"
fi
ADDED_WORKTREE=1

rm -rf "$WT/$RESULT_DIR"
mkdir -p "$WT/$RESULT_DIR/source_receipts"
n=1
while [[ "$n" -le 35 ]]; do
  printf -v i "%02d" "$n"
  src="$OUTPUT_ROOT/source_receipts/SOURCE_${i}_REPRESENTATION_RECEIPT.json"
  [[ -f "$src" ]] || die "missing source receipt $i"
  cp "$src" "$WT/$RESULT_DIR/source_receipts/"
  n=$((n + 1))
done
for name in "${AGGREGATES[@]}"; do
  [[ -f "$OUTPUT_ROOT/$name" ]] || die "missing aggregate $name"
  cp "$OUTPUT_ROOT/$name" "$WT/$RESULT_DIR/$name"
done

if find "$WT/$RESULT_DIR" -type f \( -iname '*.sav' -o -iname '*.dta' -o -iname '*.zip' -o -iname '*.7z' -o -iname '*.rar' -o -iname '*.tar' -o -iname '*.gz' \) -print -quit | grep -q .; then
  die "raw source material reached results worktree"
fi

git -C "$WT" add -- "$RESULT_DIR"
staged_text="$(git -C "$WT" diff --cached --name-only)"
if [[ -z "$staged_text" ]]; then
  echo "CLOSED35_POSTRUN_COMMIT no-op: results branch already contains byte-identical receipts"
  echo "branch: $RESULT_BRANCH"
  echo "head: $(git -C "$WT" rev-parse HEAD)"
  exit 0
fi
staged_count="$(printf '%s\n' "$staged_text" | sed '/^$/d' | wc -l | tr -d ' ')"
[[ "$staged_count" -eq 41 ]] || die "expected exactly 41 staged receipt/aggregate files, got $staged_count"

while IFS= read -r path; do
  [[ -n "$path" ]] || continue
  case "$path" in
    "$RESULT_DIR"/source_receipts/SOURCE_??_REPRESENTATION_RECEIPT.json) ;;
    "$RESULT_DIR"/CLOSED35_REPRESENTATION_OBSERVATIONS.json) ;;
    "$RESULT_DIR"/CLOSED35_TYPED_JOIN_MATRIX.csv) ;;
    "$RESULT_DIR"/CLOSED35_EDGE_PRESERVATION_RECEIPT.json) ;;
    "$RESULT_DIR"/CLOSED35_HISTORICAL_DEPENDENCY_PROVENANCE.json) ;;
    "$RESULT_DIR"/CLOSED35_RUNTIME_RECEIPT.json) ;;
    "$RESULT_DIR"/CLOSED35_CENSUS_SUMMARY.json) ;;
    *) die "disallowed staged path: $path" ;;
  esac
done <<EOF
$staged_text
EOF

git -C "$WT" commit -m "PREMAIN CLOSED35: capture authoritative qualified census receipts"
NEW_HEAD="$(git -C "$WT" rev-parse HEAD)"
echo "CLOSED35_POSTRUN_COMMIT PASS"
echo "branch: $RESULT_BRANCH"
echo "head: $NEW_HEAD"
echo "push: NOT PERFORMED"
