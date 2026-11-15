#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat >&2 <<'EOF'
Usage:
  prepare_sparse_worktree.sh <canonical_repo> <worktree_path> <worker_branch> <expected_remote_sha> <sparse_pattern> [<sparse_pattern>...]

Purpose:
  Prepare an isolated SPARSE worktree from an already-present canonical clone.
  This script never clones the repository.

Rules:
  - fetch origin explicitly;
  - verify origin/<worker_branch> exactly equals <expected_remote_sha>;
  - refuse if the destination exists;
  - refuse if a same-named local branch already exists, rather than guessing/resetting it;
  - create the worktree with --no-checkout;
  - enable non-cone sparse checkout using only the commissioned patterns;
  - checkout the exact branch and verify HEAD.

Read-only evidence outside the sparse checkout should be accessed with git show,
git cat-file, git ls-tree, git diff, etc. Expand sparse checkout only when the
commission explicitly permits the additional materialized path.
EOF
  exit 64
}

[[ $# -ge 5 ]] || usage

repo=$1
wt=$2
worker_branch=$3
expected=$4
shift 4
patterns=("$@")

[[ "$expected" =~ ^[0-9a-f]{40}$ ]] || { echo "expected SHA must be full 40-hex" >&2; exit 65; }
[[ -d "$repo/.git" || -f "$repo/.git" ]] || { echo "canonical repo not found: $repo" >&2; exit 66; }
[[ ! -e "$wt" ]] || { echo "destination already exists: $wt" >&2; exit 67; }

git -C "$repo" fetch origin

observed=$(git -C "$repo" rev-parse "refs/remotes/origin/$worker_branch")
[[ "$observed" == "$expected" ]] || {
  echo "REMOTE_SHA_MISMATCH expected=$expected observed=$observed branch=$worker_branch" >&2
  exit 68
}

if git -C "$repo" show-ref --verify --quiet "refs/heads/$worker_branch"; then
  echo "LOCAL_BRANCH_ALREADY_EXISTS__REFUSE_TO_GUESS branch=$worker_branch" >&2
  exit 69
fi

mkdir -p "$(dirname "$wt")"
git -C "$repo" worktree add --no-checkout -b "$worker_branch" "$wt" "$expected"

git -C "$wt" sparse-checkout init --no-cone
git -C "$wt" sparse-checkout set --no-cone "${patterns[@]}"
git -C "$wt" checkout "$worker_branch"

head=$(git -C "$wt" rev-parse HEAD)
remote=$(git -C "$repo" rev-parse "refs/remotes/origin/$worker_branch")
[[ "$head" == "$expected" && "$remote" == "$expected" ]] || {
  echo "POST_CREATE_IDENTITY_MISMATCH head=$head remote=$remote expected=$expected" >&2
  exit 70
}

if [[ -n "$(git -C "$wt" status --porcelain --untracked-files=all)" ]]; then
  echo "WORKTREE_NOT_CLEAN_AFTER_PREPARE" >&2
  git -C "$wt" status --short >&2
  exit 71
fi

printf 'SPARSE_WORKTREE_READY\n'
printf 'path=%s\n' "$wt"
printf 'branch=%s\n' "$worker_branch"
printf 'sha=%s\n' "$expected"
printf 'patterns:\n'
printf '  %s\n' "${patterns[@]}"
