# Executable dependency graph

## G8 — FAIL

Exact predecessor script execution graph:

`host python3 -I -S`
→ built-in `sys`
→ isolation-flag barrier
→ stdlib `argparse,csv,json,re,subprocess,pathlib,typing`
→ `_git_cwd()`
→ `subprocess.run(["git", "-C", ...])`
→ all subsequent repository trust operations through bare `git`.

The script imports no Rawlsing helper: PASS.

But it has an undeclared/unpinned executable dependency after the Python barrier: `git`, resolved through inherited process `PATH`. The candidate does not:
- resolve Git to a fixed trusted external path;
- reject a Git executable located in or under the repository;
- sanitize/reconstruct PATH before first Git invocation;
- attest the resolved Git executable;
- name Git executable provenance as an explicit external threat-model prerequisite equivalent to the host Python executable.

Worse, `_git_cwd()` invokes this bare `git` before the script can calculate/reject repository import paths. A hostile Git shim can therefore influence the repository root used by later checks.

`G8 = FAIL_CANDIDATE_CONTROLLED_OR_UNTRUSTED_GIT_EXECUTABLE_RESOLUTION`.