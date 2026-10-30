# PRE-MAIN F0R3 — post-seed authority/reviewer/PR custody repair return

**Repository:** `maidiu/rawlsing` (PRIVATE)
**Branch:** `agent/pre-main-f0r3-repair-postseed-review-cas-witnesses-r1`
**Sealed startup (commissioned source cut):** `342164a09e10aa70812299c12386ed0923308228`
**Branch tip at work start (commission tip):** `99ad7621cc9f2b1570b4a5bced89f0964c935daa`
**Actual PR #519 head read back during work:** `59c9a7a4a4fae60d809c1ef545ff4e48906d0dd0`
**Canonical PRE-MAIN read cut:** `299f41e97a43c67be9cc76a79fa49b48f4e12e54`
**Role:** independent I2 sourcefree control-code repair author, not F0/F0R2 reviewer, not PRE-MAIN maintainer, not repository administrator, not own reviewer.
**Selected pair:** Local OpenCode / DeepSeek V4.1-Flash MAX as dispatched. Harness reports model `opencode-go/deepseek-v4.1-flash`; host is local macOS Darwin x86_64 with Python 3.11.3. Actual provider and MAX effort are not independently attestable from inside the harness; no model switch was made.
**Worktree:** `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/premain-f0r3-repair-20261030-r1` (isolated; no other worktree or active worker touched).

## Overall disposition

**CANDIDATE_ENGINEERING_PASS_SCOPED__CURRENTNESS_HOLD__SCIENTIFIC_HOLD__AUTHORITY_RED.**
The candidate closes the four F0R2 N1–N4 post-seed false-positive classes at the exact sourcefree test grain. It is **not** an adoption, not a science grant, not an owner CAS, not a protected-check installation, and not a PR #519 merge. PR #519 moved after the sealed source cut; the unchanged validator blob still applies, but the owner must re-lock the new head before any use.

## Currentness finding (material)

The sealed source cut `342164...` was the PR #519 head when F0R2 closed. During this work the authenticated PR head moved to `59c9a7a4...` through three appended PR commits. At the new head:

- validator blob is unchanged: `6fa0ce132e68f1fea7d67321129a2af2627a5d94`;
- seed blob is unchanged: `4ffe5f95b84505431a928f7ef6d0e7b5931f63d8`;
- workflow blob is unchanged: `ce1ef40b5f2568c52a44d1ddc01a98647f3bf322`;
- event log moved to `60fd8e26b3d8c4bd66f27900b82c9359cf4ad652` (32 events);
- flight register moved to `9306df304a8f12029c8daacb2eb97c9fcb58df56` (32 workers, 5 PR rows).

The candidate was executed against both data cuts. No stale 19/19 result is transferred to 32/32: the candidate passes the actual current 32/32 data, and the original validator still admits N1–N4 on that same actual current data. The current-head receipt CI is green on the **old** 13-witness suite (`run 41082520979`, job `124155062531`: 32 events, 32 flights, 13 mutation witnesses). That green does not test N1–N4.

## FINDING → INTERPRETATION → ACTION → OWNER

| FINDING | INTERPRETATION | ACTION | OWNER |
|---|---|---|---|
| Original validator at blob `6fa0ce...` admits N1 fabricated `source_authority`, N2 scientific promotion to `ACCEPT_SCOPED`, N3 review of a commissioned-only SHA, and N4 arbitrary post-seed PR status. N6 PR backfill and N7 authority promotion are also admitted. | The old suite's green is a false positive for these post-seed custody claims; those witnesses did not exist in the old suite. | Candidate rejects N1–N4 with `UNVERIFIED_SOURCE_AUTHORITY`, `SCIENCE_NONISSUER`, `REVIEWER_TARGET_RETURNED_ONLY`, `PR_REMOTE_STATE_UNVERIFIED`; N5–N7 add monotonic/authority controls. | PR #519 control author; separate reviewer; not this author. |
| Candidate passes 20 negative witnesses plus the legal nonadopted `OWNER_ADOPTION_CANDIDATE`, with the original 13 preserved and the 11-event seed still frozen and `owner_approval_status=PENDING`. | Engineering repair is real and reproducible at the exact sourcefree grain; it is not institutional authority or science. | Independent source-qualified hostile review of the exact candidate blob; owner decision remains separate. | Incumbent HQ + distinct source reviewer; original PRE-MAIN owner for CAS. |
| PR #519 moved from `342164...` to `59c9a7a4...`; only log/flight and a dispatch document changed, not validator/seed/workflow. | The sealed cut is no longer the live PR head. Candidate source still applies to the unchanged validator, but currentness cannot be inferred. | Re-lock the live head, re-run the patched validator against the actual current log/flight, and bind review to the exact patched SHA. | PR #519 author/CI and authorized PRE-MAIN maintainer. |
| PRE-MAIN remains `protected=false`; rulesets count is `0`; protection and required-status endpoints return `404 Branch not protected`. | The receipt workflow is optional CI, not enforced fan-in. A green run cannot block direct write or unreviewed merge. | Repository administrator must install and read back required `receipt-contract` check, independent review, no unauthorized bypass. | Repository administrator + incumbent PRE-MAIN maintainer. |
| Offline bytes cannot verify reviewer identity/signature, source-owner grant, merged target, real first consumer, or paired progress MD/JSON. | The candidate is a guardrail, not a privileged verifier. Fully filled CAS fields remain unverified. | Build/authorize a separate privileged verifier; do not promote offline PASS to adoption. | Authorized maintainer, repo admin, original source/actor owners. |
| Sorok progress remains MD revision 36 (`fd6ce005...`) vs JSON revision 35 (`c7fb05d8...`); FIABC governed run remains 144 PASS / 3 FAIL on the same identity assertions. | These are separate owner/CAS and source-classification defects, not repaired by this control patch. | Keep visible; no test weakening; rightful owners reconcile. | Sorok incumbent/PRE-MAIN owner; FIABC/Pyat original owners. |

## Three courts

- **ENGINEERING: PASS_SCOPED for the candidate validator and tests actually executed on exact sourcefree data.** `HOLD` for currentness binding, protected enforcement, independent review, and adoption. The old validator remains `ACCEPT_SCOPED` only at its prior narrow grain; its N1–N4 admission is RED for the new custody claims.
- **SCIENTIFIC: HOLD.** No original CAN/ADP/SCI05/Pyat source, developmental rule, native person, or performed consumer was issued or verified. Scientific `ACCEPT_SCOPED` is rejected offline as `SCIENCE_NONISSUER`.
- **AUTHORITY: RED.** No owner grant, source grant, protected required check, independent reviewer acceptance, owner CAS, or actual first consumer. No branch, CI run, or filled JSON field confers authority.

## Actually executed commands and exits

All commands below were run in the isolated worktree above unless stated.

| Command | Exit | Observed result |
|---|---:|---|
| `python3 CROSS_HQ_CONTROL_ROOM/BRANCH_FANIN/verify_branch_fanin.py --selftest --baseline-ref 299f41e97a43c67be9cc76a79fa49b48f4e12e54` | 0 | 19 events / 19 flights; 13 mutation witnesses rejected + legal nonadopted candidate. |
| `cd WORKER_RETURNS/PREMAIN-F0R3-POSTSEED-AUTHORITY-LOG-REPAIR-R1/candidate && python3 verify_branch_fanin.py --selftest --baseline-ref 299f41e97a43c67be9cc76a79fa49b48f4e12e54` | 0 | Sealed 19/19 data; 20 mutation witnesses rejected + legal nonadopted candidate. |
| `cd .../candidate/current_head_59c9a7a4 && python3 verify_branch_fanin.py --selftest --baseline-ref 299f41e97a43c67be9cc76a79fa49b48f4e12e54` | 0 | Actual current 32/32 data; 20 mutation witnesses rejected + legal nonadopted candidate. |
| `cd .../candidate && python3 test_f0r3_postseed_witnesses.py` | 0 | 12 tests; OK; 20-witness selftest also passed. |
| `cd .../candidate && python3 reproduce_f0r3.py --data-dir .` | 0 | Sealed-cut N1–N4/N6/N7 admitted by original, rejected by candidate; legal candidate accepted by both. |
| `cd .../candidate && python3 reproduce_f0r3.py --data-dir current_head_59c9a7a4` | 0 | Current-head N1–N4/N6/N7 admitted by original, rejected by candidate; legal candidate accepted by both. |
| `git apply --check WORKER_RETURNS/PREMAIN-F0R3-POSTSEED-AUTHORITY-LOG-REPAIR-R1/candidate/verify_branch_fanin.py.patch` | 0 | Candidate patch applies cleanly to the unchanged source validator. |
| `python3 -m py_compile ...` for candidate validator, tests, reconstruction | 0 | Syntax clean. |

## NOT_RUN / not claimed

- No candidate-branch GitHub Actions run: the receipt workflow is `pull_request` path-filtered and `push`-to-PRE-MAIN only, with no `workflow_dispatch`; no candidate PR was opened. The exact Python job was run locally instead. This is `CI_NOT_AVAILABLE`, not a CI PASS.
- No edit, push, merge, or review of PR #519; no PRE-MAIN/main mutation; no F4, PR514/516/517/518 mutation; no branch-protection change.
- No original science/source/native corpus execution; no CAN/ADP/SCI05/Pyat issuance; no production consumer.
- No actual owner CAS, protected-check enforcement, first-consumer readback, or post-merge adoption event.
- No independent attestation of MAX reasoning effort or provider economics; only the harness-reported model and local host identity are stated.

## Exact source/test blobs

| Surface | Git blob |
|---|---|
| Source validator (sealed and current) | `6fa0ce132e68f1fea7d67321129a2af2627a5d94` |
| Source seed (sealed and current) | `4ffe5f95b84505431a928f7ef6d0e7b5931f63d8` |
| Sealed event log `342164...` | `2b899397bdac9c2e92d4db295278743e2499eca9` |
| Sealed flight `342164...` | `7c20af660ce6c323e99f5dd038abf4c4ac3b5891` |
| Current head event log `59c9a7a4...` | `60fd8e26b3d8c4bd66f27900b82c9359cf4ad652` |
| Current head flight `59c9a7a4...` | `9306df304a8f12029c8daacb2eb97c9fcb58df56` |
| Workflow (unchanged) | `ce1ef40b5f2568c52a44d1ddc01a98647f3bf322` |
| Candidate validator | `2fc1c3c7ae6113d12b70abb655ff123a6ae9c895` |
| Candidate patch | `424d87370b0e5fdfad13705335558eff37be9257` |
| Candidate tests | `80eaf4feaaa34760129c7efe3a4019f67465052a` |
| Candidate reproduction harness | `d5ce55cbfbecf8f8da264977e9c365cd15d4f388` |

## DONE / REMAINING / CRITICAL BLOCKERS / LARGEST PRODUCTIVE MOVE / FLIGHT / DELTA

- **DONE:** exact F0/F0R2 law and evidence read; sealed and current source blobs locked; old validator's N1–N4 false positives reproduced under real Python; candidate fail-closed repair implemented; 20 negative witnesses plus legal nonadopted candidate; original 13 and 11-entry PENDING seed preserved; exact current 32/32 check; local end-to-end tests; admin/progress/FIABC state read back.
- **REMAINING:** distinct independent hostile review of the exact candidate SHA; owner re-lock of the live PR head; original owner seed approval; administrator-installed and read-back required check; separate privileged verifier; Sorok paired progress; FIABC/Pyat 3-failure classification; authorized owner CAS and actual first-consumer readback.
- **CRITICAL BLOCKERS:** PR #519 current head moved past the sealed cut; target remains unprotected; seed remains owner-PENDING; no required check; no independent reviewer acceptance; no privileged verifier; Sorok MD/JSON split; FIABC governed failures.
- **LARGEST PRODUCTIVE MOVE:** review and, if accepted, apply this single validator patch to the live PR head on a protected path, then obtain owner seed approval and protected required-check readback before any CAS.
- **FLIGHT:** no active worker, PR #519, PR514/516/517/518, canonical PRE-MAIN, or F4 was disturbed. No model switch. No worktree collision.
- **DELTA:** four post-seed custody bypasses now have exact Python RED witnesses; a real current-head green false-positive is demonstrated; candidate is ready for independent review but not adoption.

## No self-adoption

This return is an input to incumbent HQ and a distinct source-qualified reviewer. The author does not review, approve, merge, or adopt its own candidate. The seed remains unapproved and `PENDING`; no event is `ADOPTED_CAS_VERIFIED`; no PRE-MAIN or PR #519 write was made.

**Push readback:** the exact immutable remote SHA of this return commit is reported in the final HQ message after `git push` and `git ls-remote` readback, because embedding the future commit SHA in its own content would be self-referential. The worktree was clean at commit time; the branch was pushed only after the return artifacts were complete.
