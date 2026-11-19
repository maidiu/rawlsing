#!/usr/bin/env bash
# Sourcefree guard tests only. No original SRC04 read/launch occurs here.
set -euo pipefail
: "${EXPECTED_ANVIL_HEAD:?Set EXPECTED_ANVIL_HEAD to the exact 40-character commit SHA}"
W="WORKER_RETURNS/ANVIL_ALL35_ORIGINAL_WITNESS_RUNNER_20261118"
if [[ -n "${ANVIL_ARCHIVE_FROM_REPO:-}" ]]; then
  # In a folder-only git archive, compare live files against the immutable
  # source repository object rather than requiring a second full worktree.
  SRC_REPO="$(git -C "$ANVIL_ARCHIVE_FROM_REPO" rev-parse --show-toplevel)"
  git -C "$SRC_REPO" cat-file -e "${EXPECTED_ANVIL_HEAD}^{commit}"
  for f in MANIFEST.json run_sourcefree_checks.sh witness_caller.py test_witness_integration_guards.py test_witness_runner.py single_pass_handoff.py; do
    git -C "$SRC_REPO" show "${EXPECTED_ANVIL_HEAD}:$W/$f" | cmp - "$W/$f" || {
      printf 'REFUSED ARCHIVE FILE DRIFT %s\n' "$f" >&2
      exit 22
    }
  done
  printf 'ARCHIVE_PIN_VERIFIED %s\n' "$EXPECTED_ANVIL_HEAD"
else
  REPO_ROOT="$(git rev-parse --show-toplevel)"
  cd "$REPO_ROOT"
  CURRENT="$(git rev-parse HEAD)"
  if [[ "$CURRENT" != "$EXPECTED_ANVIL_HEAD" ]]; then
    printf 'REFUSED WRONG HEAD current=%s expected=%s\n' "$CURRENT" "$EXPECTED_ANVIL_HEAD" >&2
    exit 20
  fi
  if [[ -n "$(git status --porcelain --untracked-files=no)" ]]; then
    echo "REFUSED tracked tree dirty; use a detached clean worktree or small archive" >&2
    exit 21
  fi
  printf 'SOURCEFREE_HEAD_VERIFIED %s\n' "$CURRENT"
fi
bash -n "$W/run_sourcefree_checks.sh"
export PYTHONDONTWRITEBYTECODE=1
python3 - "$W" <<'PY'
import hashlib,json,pathlib,sys
root=pathlib.Path(sys.argv[1])
m=json.loads((root/"MANIFEST.json").read_text())
n=0
for rel,expected in sorted(m["files"].items()):
    p=root/rel
    if p.is_symlink() or not p.is_file() or not p.resolve().is_relative_to(root.resolve()):
        raise SystemExit(f"MANIFEST_BAD_PATH: {rel}")
    h=hashlib.sha256()
    with p.open("rb") as f:
        for block in iter(lambda:f.read(1024*1024),b""):
            h.update(block)
    if h.hexdigest()!=expected["sha256"] or p.stat().st_size!=expected["bytes"]:
        raise SystemExit(f"MANIFEST_MISMATCH: {rel}")
    n+=1
if m.get("new_test_execution")!="NOT_RUN":
    raise SystemExit("MANIFEST_TEST_GRADE_UNEXPECTED")
print(f"MANIFEST_DIGESTS_OK {n} files")
for name in ("witness_caller.py","single_pass_handoff.py","test_witness_integration_guards.py"):
    compile((root/name).read_bytes(),str(root/name),"exec")
print("PYTHON_SYNTAX_OK 3 files")
PY
python3 -m unittest discover -s "$W" -p test_witness_integration_guards.py -v
python3 -m unittest discover -s "$W" -p test_witness_runner.py -v
echo "LOCAL_SOURCEFREE_GUARD_TESTS_DONE: source/native/independent G5 not inferred"
