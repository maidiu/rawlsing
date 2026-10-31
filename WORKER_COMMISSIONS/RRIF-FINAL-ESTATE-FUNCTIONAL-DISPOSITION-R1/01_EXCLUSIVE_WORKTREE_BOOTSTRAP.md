# RRIF #573 — Mandatory self-provisioned worktree bootstrap

**Must execute; not a suggestion.** The locally selected agent, not the user, creates and verifies its own Git worktree and does all work there. Never perform source inspection or tests in a shared checkout. Confirm model/editor/host choice selected by user. Never force-push/rebase/delete/reset an active worker's worktree.

From an authenticated local `maidiu/rawlsing` clone or registered worktree, run:

```bash
set -euo pipefail
git rev-parse --is-inside-work-tree | grep -qx true
TARGET_BRANCH='agent/pyat-rrif-final-estate-functional-disposition-20261031-r1'
RRIF_DISPATCH_SHA="${RRIF_DISPATCH_SHA:?Set to exact current 40-hex SHA stated on GitHub issue #573}"
[[ "$RRIF_DISPATCH_SHA" =~ ^[0-9a-f]{40}$ ]] || { echo DISPATCH_SHA_INVALID; exit 2; }
WORKTREE_DIR="$HOME/Desktop/Rawlsing_Worktrees/rrif-573-exclusive-20261031"
LOCAL_SESSION_BRANCH='rrif-session-573-20261031'
git fetch --no-tags origin "refs/heads/$TARGET_BRANCH"
ACTUAL_REMOTE_SHA="$(git rev-parse --verify FETCH_HEAD)"
[[ "$ACTUAL_REMOTE_SHA" == "$RRIF_DISPATCH_SHA" ]] || { echo DISPATCH_HEAD_MOVED_STOP; exit 3; }
git worktree list --porcelain
if [[ -e "$WORKTREE_DIR" ]] || git show-ref --verify --quiet "refs/heads/$LOCAL_SESSION_BRANCH"; then
  echo WORKTREE_COLLISION_OR_EXISTING_SESSION_STOP
  exit 4
fi
mkdir -p "$(dirname "$WORKTREE_DIR")"
git worktree add -b "$LOCAL_SESSION_BRANCH" "$WORKTREE_DIR" "$RRIF_DISPATCH_SHA"
cd "$WORKTREE_DIR"
[[ "$(git rev-parse --verify HEAD)" == "$RRIF_DISPATCH_SHA" ]] || exit 5
[[ -z "$(git status --porcelain)" ]] || { echo WORKTREE_NOT_CLEAN; exit 6; }
printf 'ISSUE=573 WORKTREE=%s START_SHA=%s\n' "$PWD" "$(git rev-parse HEAD)"
```

If the path or local branch exists: **STOP**, investigate existing worker lease/process and whether this is an earlier live run of the same commission. Never delete it or start a duplicate. If the local shell/Git clone is unavailable: **S2_NOT_AVAILABLE**, never pretend execution. No original survey/source or native security code execution is permitted without separate authority.

Then perform every mission requirement in `00_COMMISSION.md` inside the new worktree; use historical Git objects inertly unless a safe sourcefree run is expressly qualified. Commit only allowed return artifacts, and push only fast-forward to the assigned remote branch. Before push, recheck that `git ls-remote origin refs/heads/$TARGET_BRANCH` equals the pinned dispatch SHA; if changed, STOP and report. No force push, no protected PRE-MAIN mutation. Verify resulting remote SHA and files after push. Independent review remains separate.
