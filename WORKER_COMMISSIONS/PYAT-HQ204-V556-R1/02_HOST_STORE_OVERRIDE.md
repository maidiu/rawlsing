# HQ204 V556 — host-store override

Authority:
`PYAT_CONTROL_ROOM/SPACE_BUNNY_OPENCODE_R1/HOST_SPECIFIC_GIT_STORE_OVERRIDE_HQ204_R1.md`

Control commit:
`06f306d8a80d94794ced8f222e71fa1ce467ad66`

For this worker on the current host:

- `$HOME/Desktop/Rawlsing` is AUTHORIZED as the canonical local Git object store IF it verifies as a Git repository whose origin is `maidiu/rawlsing`.
- The earlier path `$HOME/Desktop/as2b-lits1-DiSDJn/repository` was specific to another Mac and is NOT required here.
- Do not create a new clone.
- Create/use an isolated sparse worktree under `$HOME/Desktop/Rawlsing_Worktrees`.
- Fetch only exact governed refs required by the commission.
- Preserve all other HQ204 V556 commission law unchanged.

Before work:
1. verify `git -C "$HOME/Desktop/Rawlsing" rev-parse --is-inside-work-tree`;
2. verify origin is `maidiu/rawlsing`;
3. fetch the exact worker ref;
4. verify the worker branch resolves to the exact current commissioned tip after this addendum;
5. then prepare the sparse worktree and continue.

This addendum supersedes only the host-path portion of the earlier launch prompt.
