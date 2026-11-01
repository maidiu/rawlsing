# Executed source and validation receipts

## Worktree

```text
Repository: maidiu/rawlsing
Branch: research/sorok-rrif-hq-decision-subtraction-first-20261031-r1
Worktree: /Users/matthewsmith/Desktop/Rawlsing_Worktrees/sorok-rrif-gate01-exclusive-20261031
HEAD: 3162a4af6b0d543b8da1fb2f5e84c3537ad12716
PRE-MAIN readback: 8e44ca9c751049d65e6def47600b5c073ee04b29
OS: macOS 13.7.8 x86_64
Python: 3.11.3
Git: 2.39.1
```

The worktree was created fresh from the assigned remote branch after checking
`git worktree list --porcelain` and confirming the target path/branch were free.

## Commands run

```sh
git fetch --no-tags origin refs/heads/research/sorok-rrif-hq-decision-subtraction-first-20261031-r1
git worktree add --track -b research/sorok-rrif-hq-decision-subtraction-first-20261031-r1 \
  "$HOME/Desktop/Rawlsing_Worktrees/sorok-rrif-gate01-exclusive-20261031" \
  refs/remotes/origin/research/sorok-rrif-hq-decision-subtraction-first-20261031-r1
git rev-parse HEAD
git merge-base --is-ancestor 8e44ca9c751049d65e6def47600b5c073ee04b29 HEAD
git ls-tree -r HEAD
git show <commit>:<decision/source path>
git rev-parse <commit>:<decision/source path>
python3  # first-pass A/B/C/D JSON merge and exact-blob presence
python3  # bridge classification and disjointness
python3 -m json.tool <output>.json
```

## Actual counts

```text
Original branch records:                294
Unique original branch names:           294
Excluded from recovery:                 189
Accepted integration-only:                8
True-undecided survivors:                97
Sum:                                    294
Named function symbols in bridges:     1,252
Code-entrypoint records:               1,510
Exact primary source blob in current:     0/294
Actual current first consumers proved:    0/294
Decision events:                          19
```

Disjointness and absence checks are in
`07_COVERAGE_AND_HQ_ACCEPTANCE_NEGATIVE_TESTS.json`. B3AS/C9R/JOIN-E/DEV-R are
not in the survivor file. Accepted-scoped records remain
`ACCEPTED_SCOPED_NOT_IN_PREMAIN`; no `EXACTLY_INCORPORATED_NOW` record exists.

## Not run

- No historical worker script was executed.
- No source branch was imported into current PREMAIN.
- No native survey/actor/world corpus was read or executed.
- No model/provider/network, database, C9/C12 key/anchor, human A5 or production
  service was used.
- No PRE-MAIN, other HQ, Programma, O-LIVE or active worker was modified.

Content commit: dfb161655ffc4e90eea6a79db69a73f5664a295d. Final remote tip is read back after this follow-up readback commit.
