# PYAT HQ192 — Host preflight remediation — R1

Repository: `maidiu/rawlsing`

Role: **RABOCHII / LOCAL-HOST OPERATIONS IMPLEMENTER — SPACE BUNNY**

Branch:
`agent/rabochii-pyat-hq192-host-preflight-remediation-r1`

Exact implementation base:
`491dac21b9f833c57bcb2ddb39f442c3dba0017c`

The exact commissioned startup SHA is supplied by HQ after this commit is published.

Return directory:
`WORKER_RETURNS/PYAT-HQ192-HOST-PREFLIGHT-REMEDIATION-R1/`

## Mission

Resolve or precisely preserve the new live-run blocker:
`HOST-PREFLIGHT-F3-DISK-CAPACITY-VOLATILITY`

Also close the two bounded operational hazards:
- `LOCAL_COURTS/` not ignored;
- dangling short interpreter symlink.

R7 itself is CLOSED. Do not reopen it.

## Startup

Fetch origin; verify exact remote startup SHA; isolated clean worktree; no blind pull; stop on mismatch.

## Safety law

No sudo.
No system security changes.
No recursive chmod/chown.
No deletion of user documents, raw sources, governed evidence environments or another lane's active work.
No source directory inspection.
No global package/toolchain mutation.

## Disk work

1. Measure filesystem capacity repeatedly, not once.
2. Inventory **only safe-to-inspect project/tooling/temp surfaces**:
   - Git registered worktrees and their clean/dirty/branch/remote-return state;
   - lane-owned `/private/tmp` / `/tmp` fixtures;
   - project-local caches/tooling estates under `LOCAL_COURTS` by directory size, without opening survey/source data;
   - package caches only at metadata/path-size level if clearly non-source.
3. Classify each cleanup candidate:
   - SAFE_AUTOMATIC: disposable lane temp, stale clean worktree whose work is pushed/returned, reproducible cache;
   - REQUIRES_USER_APPROVAL;
   - PRESERVE.
4. You may delete only SAFE_AUTOMATIC items with exact before/after accounting.
5. Never delete the R7 qualification environment or interpreter toolchain.
6. Never inspect raw-source contents or source directories.

## Live-run free-space threshold

Search governed repository evidence for declared source/output sizes and execution write behavior without touching source files.

Derive a conservative **candidate preflight threshold** only if supported by governed size evidence plus declared temporary/output behavior.

Do not invent a threshold.

If the repository does not support a defensible numeric threshold, return:
`HOST_PREFLIGHT_POLICY_THRESHOLD_REQUIRED`
with measured free space and a quantified cleanup result.

Any eventual live runner must fail closed if current free space is below the adopted threshold immediately before launch.

## LOCAL_COURTS ignore

Add a narrowly scoped repository ignore rule for `LOCAL_COURTS/` if no conflicting repository law exists.

Verify:
- `git check-ignore LOCAL_COURTS/...` succeeds;
- existing tracked files are unaffected;
- no broad ignore masks governed paths.

## Dangling symlink

Repair or remove only the known dangling local symlink:
`LOCAL_COURTS/tooling/python/cpython-3.11-macos-x86_64-none`

Target should resolve to the real:
`LOCAL_COURTS/tooling/python/cpython-3.11.3-macos-x86_64-none`

Verify target exists and full interpreter SHA remains:
`11d6f541a870a141249ce98d45834a6789e29c07031e85ce17f3e67f24c535f6`

Do not modify the interpreter bytes.

## SHA-pinned execution preflight

Produce a source-free preflight helper/artifact that verifies:
- exact executable freeze commit `8ff40d37de69db2d8a6053a7c2242f481677f1a4`;
- exact `rawlsing_next` tree `b0c1ab472cde033e21f1c2f63fbcbea2f0cccef0`;
- exact R7 interpreter digest/environment identity;
- adopted disk threshold, if one can lawfully be derived.

No live C4 execution.

## Allowed write terrain

Repository:
- `.gitignore`
- `PYAT_CONTROL_ROOM/SPACE_BUNNY_OPENCODE_R1/ACTIVATION_RETURNS/HOST-PREFLIGHT-R1/**`
- `WORKER_RETURNS/PYAT-HQ192-HOST-PREFLIGHT-REMEDIATION-R1/**`

Local:
- only the known symlink above;
- SAFE_AUTOMATIC cleanup targets recorded in the return.

## Dispositions

Exactly one:
- `HOST_PREFLIGHT_CLOSED__CANDIDATE_READY_FOR_HQ_REVIEW`
- `HOST_PREFLIGHT_PARTIAL__DISK_BLOCKER_REMAINS`
- `HOST_PREFLIGHT_POLICY_THRESHOLD_REQUIRED`
- `HOST_CAPABILITY_BLOCKED`

## Return

Commit repository changes/result packet, push, re-fetch, verify.
Report substantive SHA and remote tip separately.

Terminal:
`HQ192_HOST_PREFLIGHT_RETURNED__HQ_REVIEW_REQUIRED`

## Holds

Zero source access, locators, warrant, live C4, C7 or actor work.
