# PYAT HQ280 — GitHub-first worker return protocol R1

**Issuing role:** Pyat HQ operational coordination. **Status:** HQ_STAGED_WORKER_DELIVERY_PROTOCOL, not scientific/semantic/source use adoption.
**Reason:** WGA/WGA-R/WGC/WGD/WGE/WGE-R repeatedly delivered small non-sensitive ZIPs outside Git, unnecessarily forcing the project director to upload them to ChatGPT while the sealed worker branches remained at startup SHA. WGE-R delivered ten non-sensitive files totalling 42,725 uncompressed bytes (ZIP 20,994 bytes) with no worker push. This is a commission-design failure.

## Default for all new Pyat commissions
1. Assign **exact existing branch and exact sealed startup SHA**. Worker reads exact commission and observes current control. Do not mutate canonical or semantic authority.
2. For ordinary markdown/JSON/JSONL/scripts/tests and other modest non-sensitive output, **write the actual return as individual files under the commission-specific `WORKER_RETURNS/` directory on the assigned branch**. Do not package only an out-of-repo ZIP.
3. Worker **commits and pushes** the complete permitted return to that branch (and only that branch), verifies `git ls-remote`/branch HEAD or equivalent actual remote receipt, reports exact commit SHA, base, changed files, blob hashes, execution facts and held work. No worker self-adoption.
4. **The GitHub return is the default handoff to HQ.** HQ fetches the branch and reads the exact committed reports, scripts, assertions and manifest. The user should not serve as a routine courier or be asked to re-upload tiny ZIPs.
5. Keep large binary traces, sensitive respondent-lineage outputs, raw survey data and excluded payloads out of Git. Place only exact hash/byte-count/path/access-custody receipts in the branch, with a separately-delivered artifact *only if necessary*. This exception must be precise.
6. **If push/auth/network genuinely unavailable**, worker returns an exact failure reason, current branch/worktree state, minimal non-sensitive ZIP fallback and clearly marks all artifacts **NOT_PUSHED**. Never claim a successful push from local commits alone.
7. Independent reviewers likewise write and push their evidence plus verdict. For reviews containing externally obtained input ZIPs, do not re-publish a huge/sensitive source input; add its verified SHA, contents manifest and exact necessary excerpts/results to the reviewer branch.
8. HQ separates **worker-authored, worker-pushed original evidence** from **HQ-authored recovery/intake notes**. No misrepresentation of provenance.

## Existing WGE-R exception, NOT the future pattern

A reviewer completed WGE-R while the sealed commission directed outside-repository outputs. HQ received and SHA-verified its 20,994-byte ZIP; an HQ-authored receipt was banked at `WORKER_RETURNS/PYAT-HQ280-WGER-INDEPENDENT-RETAINED-E2B-EXECUTION-REVIEW-R1/00_HQ_RECEIVED_RETURN_AND_GITHUB_CUSTODY_GAP.md` on the assigned reviewer branch. This note is not the full worker-original ten-file return. Do not retrospectively claim it is.

## Future commission acceptance condition

An ordinary non-sensitive return is DELIVERY_COMPLETE only after a verifiable push of its **actual** individual report/script files. A success terminal printed in a local session or a ZIP path in `/tmp/` is not GitHub custody.

**Terminal:** `HQ280_GITHUB_FIRST_RETURNS_REQUIRED__USER_COURIER_NOT_DEFAULT__PERMISSION_GATES_UNCHANGED`.
