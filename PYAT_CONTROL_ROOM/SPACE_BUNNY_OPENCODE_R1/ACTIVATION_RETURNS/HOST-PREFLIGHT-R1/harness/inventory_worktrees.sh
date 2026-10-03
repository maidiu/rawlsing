#!/bin/bash
# HQ192 worktree inventory, corrected. Separates REAL dirty state (modified
# tracked files / meaningful untracked work) from macOS .DS_Store noise, which is
# Finder metadata and not lane work. Read-only.
set -u
MAIN=/Users/matthewsmith/Desktop/Rawlsing
cd "$MAIN" || exit 1
printf '%-46s %8s  %-10s %-9s %s\n' WORKTREE MiB TRACKED_MOD REAL_UNTRACKED REMOTE_HAS_HEAD
git worktree list --porcelain | awk '
  /^worktree /{wt=$2} /^branch /{br=$2} /^HEAD /{hd=$2}
  /^$/{ if(wt!=""){print wt"\t"hd"\t"br; wt="";br="";hd=""} }
  END{ if(wt!="") print wt"\t"hd"\t"br }
' | while IFS=$'\t' read -r wt hd br; do
  [ -z "$wt" ] && continue
  sz=$(du -sm "$wt" 2>/dev/null | cut -f1); [ -z "$sz" ] && sz=0
  # modified tracked files = genuine work-in-progress
  tm=$(git -C "$wt" status --porcelain --untracked-files=no 2>/dev/null | wc -l | tr -d ' ')
  # untracked EXCLUDING .DS_Store noise
  ru=$(git -C "$wt" status --porcelain 2>/dev/null | grep -v '\.DS_Store$' | wc -l | tr -d ' ')
  if git branch -r --contains "$hd" 2>/dev/null | grep -q .; then rc="yes"; else rc="NO-UNPUSHED"; fi
  name=$(basename "$wt"); [ "$name" = "Rawlsing" ] && name="Rawlsing(MAIN)"
  printf '%-46s %8s  %-10s %-9s %s\n' "${name:0:44}" "$sz" "$tm" "$ru" "$rc"
done
