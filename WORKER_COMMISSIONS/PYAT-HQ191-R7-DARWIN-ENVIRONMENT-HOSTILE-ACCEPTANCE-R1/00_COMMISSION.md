# PYAT HQ191 — R7 Darwin environment hostile independent acceptance — R1

Repository: `maidiu/rawlsing`

Role: **HOSTILE INDEPENDENT REVIEWER / LOCAL-HOST RUNTIME ACCEPTANCE**

Preferred reviewer: **DeepSeek V4.1 Flash**.

Review branch:
`agent/reviewer-pyat-hq191-r7-darwin-environment-hostile-acceptance-r1`

The exact commissioned startup SHA is supplied by HQ in the launch directive after this commission commit is published.

Target worker branch:
`agent/rabochii-pyat-hq190-b-r7-darwin-environment-closure-r1`

Exact returned target tip:
`def6d369878cb273ca06f97e08c4fb0a2964611e`

Substantive R7 result:
`11f68e122c728dd8be6a6fd45bd7e8ef959060b7`

Target disposition:
`R7_CLOSED__CANDIDATE_READY_FOR_INDEPENDENT_ACCEPTANCE`

Return directory:
`WORKER_RETURNS/PYAT-HQ191-R7-DARWIN-ENVIRONMENT-HOSTILE-ACCEPTANCE-R1/`

## Mission

Assume R7 is **not** closed until independently proven.

Do not repair the worker result. Do not merely check its prose for consistency. Attack the exact two R7 closure claims:
1. complete runtime fingerprinting;
2. durable/reproducible source-free qualification environment sufficient for the later governed C4 run on this host.

## Mandatory startup

1. `git fetch origin`.
2. Do not use blind `git pull`.
3. Resolve this review branch and verify it equals the exact startup SHA supplied by HQ.
4. Resolve the target worker branch and verify it equals `def6d369878cb273ca06f97e08c4fb0a2964611e`.
5. Verify `11f68e122c728dd8be6a6fd45bd7e8ef959060b7` is the substantive result ancestor identified by the return.
6. Use an isolated review worktree.
7. Stop before substantive review on any mismatch.

## Exact claims to attack

### A. Runtime identity
Independently verify, against the actual local files if access permits:
- base interpreter full SHA-256:
  `11d6f541a870a141249ce98d45834a6789e29c07031e85ce17f3e67f24c535f6`;
- libpython full SHA-256;
- all five compiled-extension full SHA-256 values;
- each historical 32-hex prefix is in fact the prefix of the newly measured full digest, not a separately invented value.

Do not accept JSON claims without hashing the files yourself if the review runtime can access them.

### B. Durable environment
Target environment:
`/Users/matthewsmith/Desktop/Rawlsing/LOCAL_COURTS/qualification/r7-c4-source-free-venv`

Verify if accessible:
- it exists;
- it is not under a per-session temp directory;
- exact interpreter resolves as claimed;
- package inventory is complete and exactly pinned;
- `narwhals==2.26.0` is present;
- the environment actually uses the claimed interpreter;
- the recipe can reconstruct the intended package state at least at the declared local-host grain.

Distinguish **durable on this host** from **portable/reconstructible on another host**.

### C. Source-free requalification
Against exact freeze:
`8ff40d37de69db2d8a6053a7c2242f481677f1a4`

and exact `rawlsing_next` tree:
`b0c1ab472cde033e21f1c2f63fbcbea2f0cccef0`

independently challenge:
- 55 tests collected before timed run;
- 55/55 twice;
- no failures/errors/skips;
- correct six-file court, not a narrowed substitute;
- imports actually resolve from the freeze worktree;
- closure counts 21 and 23 at the claimed grains;
- no unexpected dynamic-loader/subprocess/source edges at the prior C4C3 evidence grain.

If the local review sandbox cannot execute the court, say so explicitly and distinguish file/commit verification from runtime re-observation.

### D. Failure/retry honesty
Check the two disclosed infrastructure failures and the destructive `__pycache__` incident.

Verify:
- no test failure was retried until green;
- the deleted tracked custody artifacts were restored byte-identically;
- no commit contains the deletion;
- final freeze tree identity is clean.

### E. Host-bound operational blockers
Attack whether these are merely limitations or actual live-run blockers:
- disk at ~99% with ~6.3 GiB free;
- LOCAL_COURTS not gitignored;
- dangling interpreter symlink;
- unversioned interpreter;
- external package-index dependence.

Especially answer:
**Would the current disk headroom make a governed multi-gigabyte live C4 run unsafe or non-credible even if R7 itself is technically closed?**

Do not silently fold a new host-resource blocker into R7 if it is conceptually separate; type it separately.

### F. Lineage finding
The worker reports its branch/control lineage has `rawlsing_next` tree `2a1ac8e2...`, while the exact freeze has `b0c1ab47...`, and the freeze is not an ancestor.

Determine whether this is:
- expected because control/documentary ancestry and the executable freeze are cross-lineage and exact freeze execution is SHA-pinned; or
- a genuine live-run/adoption blocker requiring reintegration before execution.

Do not call ordinary cross-lineage evidence a regression merely because branch HEAD differs.

## Review questions

Answer separately:

1. Is the fingerprint component closed on this host?
2. Is the environment durable enough on this host for a governed later run?
3. Is exact source-free requalification of the freeze independently supported?
4. Is R7 removable as the live-execution blocker?
5. Does any **new, separately typed** live-run blocker emerge?
6. What minimum action is required before live C4?

## Allowed dispositions

Exactly one:
- `ACCEPT_R7_CLOSED__LIVE_BLOCKER_REMOVABLE`
- `ACCEPT_R7_CLOSED__SEPARATE_HOST_PREFLIGHT_BLOCKER_REMAINS`
- `R7_PARTIAL__LIVE_BLOCKER_REMAINS`
- `MATERIAL_COUNTEREXAMPLE__R7_CLOSURE_UNSOUND`

## Write terrain

Only:
`WORKER_RETURNS/PYAT-HQ191-R7-DARWIN-ENVIRONMENT-HOSTILE-ACCEPTANCE-R1/**`

Temporary source-free fixture/worktree files may live outside the repo.

Do not modify the R7 candidate, production, control, source/warrant artifacts, or historical returns.

## Required packet

At minimum:
- `00_REVIEW.md`
- `01_TARGET_AND_RUNTIME_IDENTITY.json`
- `02_ENVIRONMENT_DURABILITY_CHECK.json`
- `03_SOURCE_FREE_REQUALIFICATION_CROSSCHECK.json`
- `04_INCIDENT_AND_RETRY_REVIEW.json`
- `05_LINEAGE_AND_HOST_PREFLIGHT.json`
- `06_CAPABILITY_CEILING.json`
- `07_FINAL_DISPOSITION.json`

## Return law

Commit the substantive review result; push this review branch; re-fetch and verify local HEAD == remote.

Return artifacts bind the stable substantive review-result SHA. Do **not** embed the enclosing branch-tip SHA recursively.

Report:
- branch;
- pushed remote tip SHA;
- substantive review-result SHA;
- disposition;
- terminal.

## Holds

Zero raw-source access.
Zero locator discovery.
Zero warrant issuance.
Zero live C4.
Zero production mutation.
Zero C7/actor work.

Terminal:
`HQ191_R7_HOSTILE_ACCEPTANCE_RETURNED__HQ_ADJUDICATION_REQUIRED`
