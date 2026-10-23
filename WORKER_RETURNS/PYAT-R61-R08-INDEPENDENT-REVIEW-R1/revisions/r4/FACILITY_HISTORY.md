# Replacement execution and corrective-facility history

This file records the facility history separately from the product verdict. It
does not change the frozen EXPECTATIONS or any candidate/native/HQ content.

## Prior failed session (terminal, not reused)

- Session `ses_e963b802affeDF1y8OQX2SKdTK` was the first R08V R4 reviewer
  session. It is terminal `FACILITY_CWD_MISMATCH`: the persistent OpenCode
  session directory/default tool root did not match the assigned worktree.
- That session produced no product verdict. No old product test result, positive
  or hostile observation from it is assumed or counted here.
- No duplicate reviewer run was started for this logical review job. This is the
  one authorized replacement execution, on the existing DeepSeek MAX/Global
  harness, under coordinator correction
  `3249eb333e1288362af649242d17f5ae9e689817`.

## Preflight actually observed by this replacement session

- `pwd` -> `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/r61-r08v-r4`.
- `git rev-parse --show-toplevel` -> the same exact root.
- `git branch --show-current` ->
  `agent/opencode-pyat-r61-r08v-r4-independent-review-r1`.
- `git status` -> sparse checkout with 6% of tracked files present; working tree
  clean; no tracked change.
- These matched the commission's exact root and branch, so the session
  continued. No alternate worktree, director worktree or fresh repository copy
  was used.

## Coordinator inputs

- The correction and the original commission (`9307abc2a...`) are not in the
  reviewer branch tree. They were read read-only with `git show` at the named
  commits; no checkout, merge, reset or branch mutation was performed.
- The frozen reviewer EXPECTATIONS `4cf30eee...` was already present and
  committed locally; it was preserved byte-for-byte.
- Candidate `48a2eaf6d...` and code commit `3c69a13e6...` were read with `git
  show`/`git hash-object`; the working-tree code/test blobs match the pins.
- No author/candidate code was changed. The author session
  `ses_e98c8dfe6ffewNYOqJpvqK21a6` was not used, woken or addressed.

## Sparse checkout facility note

The existing sparse review checkout initially lacked three tracked fixture
authority directories used by the pinned native AT07/n10e fixture
(`WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R2`, `-R3`, `-R8`). This session
materialized those already-tracked read-only inputs in the SAME worktree with
`git sparse-checkout add` and did not change their contents. `git status` after
materialization showed only the reviewer-root artifacts as untracked; no tracked
file differs from HEAD. This is a checkout-materialization facility note, not a
candidate or native-owner edit.

## No changes outside the reviewer root

- No director/HQ/default branch mutation.
- No provider/model/account change, no subagents, no extra sessions.
- No author/candidate repair, self-adoption or author wake.
- The only intended commit is on this reviewer branch, with reviewer artifacts
  under `WORKER_RETURNS/PYAT-R61-R08-INDEPENDENT-REVIEW-R1/revisions/r4/`, plus
  the pre-existing frozen EXPECTATIONS commit that was already in the local
  branch and is intentionally pushed unchanged.
