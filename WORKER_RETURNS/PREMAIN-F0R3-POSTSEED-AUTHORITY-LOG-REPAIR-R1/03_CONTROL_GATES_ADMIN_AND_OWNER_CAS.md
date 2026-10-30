# F0R3 control gates, administrative obligations and owner CAS decision

**Date:** 2026-10-30
**Repository:** `maidiu/rawlsing`
**Candidate:** `WORKER_RETURNS/PREMAIN-F0R3-POSTSEED-AUTHORITY-LOG-REPAIR-R1/candidate/verify_branch_fanin.py`, blob `2fc1c3c7ae6113d12b70abb655ff123a6ae9c895`.
**Source validator:** blob `6fa0ce132e68f1fea7d67321129a2af2627a5d94` (unchanged at PR #519 head `59c9a7a4a4fae60d809c1ef545ff4e48906d0dd0`).
**Canonical PRE-MAIN:** `299f41e97a43c67be9cc76a79fa49b48f4e12e54`.

## 1. Actual observed gate state

| Surface | Observation | Meaning |
|---|---|---|
| PR #519 | open, draft, unmerged; head `59c9a7a4a4fae60d809c1ef545ff4e48906d0dd0`; base `299f41e97a43c67be9cc76a79fa49b48f4e12e54`; mergeable true; mergeable_state unstable | The sealed `342164...` cut is not the live head. Owner must re-lock the current head or a later exact SHA. |
| PRE-MAIN branch protection | `protected=false` | Direct pushes and unreviewed merges are not blocked by branch protection. |
| Repository rulesets | `0` | No ruleset supplies required checks, review or bypass constraints. |
| Required status checks | protection endpoint returns `404 Branch not protected`; required checks absent | The receipt workflow is optional CI, not a required merge gate. |
| Current receipt CI | run `41082520979`, job `124155062531`, conclusion `success`; 32 events / 32 flights; 13 mutation witnesses | Green on the old suite; does **not** exercise N1–N4. |
| Current governed CI | run `41082521136`, 3 failed / 144 passed; same FIABC identity/packaging assertions | Separate FIABC/Pyat owner classification required; no test weakening by this return. |
| Seed | blob `4ffe5f95b84505431a928f7ef6d0e7b5931f63d8`; `owner_approval_status=PENDING`; 11 events / 11 workers / 4 PRs | Frozen candidate seed is not an owner-approved canonical seed. |
| Sorok progress | MD revision 36, blob `fd6ce00595e7b1ea9bb997cf7bd9fcb4e83eccbe`; JSON revision 35, blob `c7fb05d8e5d0240959191041a73e76e2f14cb436` | Paired CAS is not synchronized. Rightful Sorok owner must reconcile; this return does not. |
| Candidate CI | not run | Workflow has no `workflow_dispatch`; only PR path-filtered and push-to-PRE-MAIN triggers; no candidate PR opened. Local exact Python run instead. |

## 2. Optional versus required obligations

**Optional today, insufficient for enforcement:**

- a green `PRE-MAIN Branch Fan-in Receipt Integrity (sourcefree)` workflow run;
- a filled JSON CAS field;
- a branch name containing `owner` or `review`;
- a PR description, comment, or local report claiming protection.

**Required, and not installed/verified by this author:**

1. **Repository administrator / PRE-MAIN maintainer:** protect `integration/pre-main-reconciliation-r1` (or the authorized successor) with a real branch protection/ruleset that requires the exact `receipt-contract` check (workflow `PRE-MAIN Branch Fan-in Receipt Integrity (sourcefree)`, job `receipt-contract`), requires independent review, and denies unapproved bypass/direct force-push. Read back `protected=true`, the exact required context, review rule, and bypass list.
2. **Repository administrator / workflow owner:** add a mandatory atomic-pair check for Sorok/Pyat progress MD+JSON changes, because the current path filter covers `CROSS_HQ_CONTROL_ROOM/BRANCH_FANIN/**` and the workflow file, not progress-only changes. The pair must be bound to one revision and one enclosing target commit.
3. **Authorized maintainer + original owners:** authorize a **separate privileged verifier** that can authenticate the real merged target SHA, authorized owner grant, source-owner permission, actual first consumer, current paired progress, and repository protection. The offline validator cannot and must not be treated as that verifier.
4. **Original PRE-MAIN owner:** approve the exact initial 11-entry seed provenance (currently `PENDING`) and the current source cut. A pinned blob is not a signed authoritative initial inventory.
5. **Original FIABC/Pyat owner:** classify the 3 governed failures against the base and changed bytes. Do not waive or edit frozen tests without source evidence.
6. **Original Sorok owner:** reconcile MD36/JSON35 in one truthful paired CAS revision. Do not edit Pyat's report without Pyat's owner.

## 3. Owner CAS decision instructions

The following is an instruction set for the authorized owner, not a grant by this author. This author does not merge, adopt, protect, or approve.

### Preconditions (all must hold)

- A distinct source-qualified reviewer has reviewed the exact candidate validator SHA and returned an independent hostile verdict on the exact live PR head.
- The live PR head is re-locked by direct readback; validator, seed, workflow, event log and flight blobs are recorded.
- The candidate patch applies to that exact validator blob without conflict (`git apply --check`).
- The seed provenance is approved by the original owner, or the seed remains explicitly noncanonical and no adoption is claimed.
- The repository administrator has installed and read back the required check and independent review protections.
- The separate privileged verifier exists and can authenticate merge target, owner grant, first consumer and paired progress.
- No conflicting active writer/lease is on the same branch/worktree.

### Controlled sequence

1. **Re-lock.** Read PR #519 and canonical PRE-MAIN directly. Abort if PR head changed from the reviewed SHA, if the validator/seed/workflow blob changed, or if PRE-MAIN moved from the authorized base.
2. **Apply scoped source.** Apply only the candidate validator patch in an owner-authorized branch. Do not touch the seed, log, flight, workflow, original science, actor code, or another HQ's progress.
3. **Run exact sourcefree tests.** Run `python3 CROSS_HQ_CONTROL_ROOM/BRANCH_FANIN/verify_branch_fanin.py --selftest --baseline-ref 299f41e97a43c67be9cc76a79fa49b48f4e12e54` and the candidate unittest/reproduction commands. Require 20 negative witnesses plus the legal nonadopted candidate, and require N1–N4 to be rejected.
4. **Independent review.** Obtain a distinct source-qualified hostile review of the exact patched SHA. The author of this return cannot be that reviewer and cannot accept its own work.
5. **Protection readback.** The administrator must read back protected=true, the exact required `receipt-contract` context, independent review, and no unauthorized bypass. A green optional run alone is not sufficient.
6. **Owner CAS.** Only the authorized PRE-MAIN maintainer may merge through the protected path. The pre-merge ledger must not invent the future merge SHA. Record `ADOPTED_CAS_VERIFIED` only after the actual merged commit exists, with the real owner grant, verified target, actual first consumer and paired progress revision.
7. **Post-merge readback.** Read the merged target SHA, both progress files at the same revision/commit, and the actual importing first consumer. If any readback fails, record a new append-only corrective event; do not rewrite history.

### Abort conditions

Abort or HOLD, without adoption, if any of the following occurs:

- PR #519 head, validator blob, seed blob, workflow blob, or canonical PRE-MAIN moves after review;
- patch conflicts or tests fail;
- a required check is still optional or its exact context is not read back;
- seed approval remains `PENDING` while any adoption is proposed;
- the independent reviewer is the author or otherwise not independent;
- the privileged verifier cannot authenticate the merged target, owner grant, first consumer, or paired progress;
- Sorok/Pyat progress remains split, or FIABC failures are not classified;
- any attempt is made to convert a branch name, CI run, comment, or filled CAS field into authority.

## 4. Exact commands for the owner

```bash
# readback
gh api repos/maidiu/rawlsing/pulls/519 --jq '{head:.head.sha,base:.base.sha,draft,merged,state}'
gh api repos/maidiu/rawlsing/branches/integration/pre-main-reconciliation-r1 --jq '{protected,sha:.commit.sha}'
gh api repos/maidiu/rawlsing/rulesets --jq 'length'

# apply candidate in an owner-authorized branch, never directly in PR519 from this worker
git apply --check WORKER_RETURNS/PREMAIN-F0R3-POSTSEED-AUTHORITY-LOG-REPAIR-R1/candidate/verify_branch_fanin.py.patch
git apply WORKER_RETURNS/PREMAIN-F0R3-POSTSEED-AUTHORITY-LOG-REPAIR-R1/candidate/verify_branch_fanin.py.patch

# exact sourcefree gate
python3 CROSS_HQ_CONTROL_ROOM/BRANCH_FANIN/verify_branch_fanin.py \
  --selftest --baseline-ref 299f41e97a43c67be9cc76a79fa49b48f4e12e54

# self-contained candidate replay
cd WORKER_RETURNS/PREMAIN-F0R3-POSTSEED-AUTHORITY-LOG-REPAIR-R1/candidate
python3 test_f0r3_postseed_witnesses.py
python3 reproduce_f0r3.py --data-dir .
python3 reproduce_f0r3.py --data-dir current_head_59c9a7a4
```

## 5. Nonclaims

This document is not a branch-protection change, not an owner CAS, not a merge authorization, not a source grant, not a scientific decision, and not an independent review. It records exact observations and the decisions that remain with the original owners. The author has not touched PR #519, PRE-MAIN, PR514/516/517/518, F4, or any active worker.
