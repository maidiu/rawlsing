# Admin protection and owner CAS gates

## Live observations (2026-10-31)

| Surface | Exact observation | Conclusion |
|---|---|---|
| Current PRE-MAIN | `integration/pre-main-reconciliation-r1` @ `8e44ca9c751049d65e6def47600b5c073ee04b29` | live branch, no control files present |
| Current branch metadata | `protected=false`; `protection_url` present | branch is not protected |
| Repository rulesets | `[]` | no ruleset enforcement |
| Required-status-check endpoint | HTTP 403 for this credential | **cannot verify installed required checks**; no evidence of one |
| PR #519 head | `59c9a7a4a4fae60d809c1ef545ff4e48906d0dd0` | current PR head |
| PR #519 merge ref | `7abc24f2ec3884702d0bc41248ae13d7a367a6ae`; parents `299f41e9…` and `59c9a7a4…` | PR merge still based on `299f41e9`, not current PRE-MAIN |
| Seed | `4ffe5f95b84505431a928f7ef6d0e7b5931f63d8`; 11 events / 11 workers / 4 PRs; `owner_approval_status=PENDING` | owner approval absent |
| Workflow | `PRE-MAIN Branch Fan-in Receipt Integrity (sourcefree)`; job `receipt-contract`; workflow blob `ce1ef40b…` | optional path-filtered CI, not a proven required check |
| Privileged verifier | none in PR #519; validator law explicitly says offline bytes cannot certify adoption | no signed/owner verifier |
| F4 branch | `9fb7caeb…` not an ancestor of `8e44ca9c` | divergent, HELD |

## What is actually required

1. **Repository administrator:** create/verify an active branch protection or repository ruleset on `integration/pre-main-reconciliation-r1` that:
   - requires the exact receipt check from workflow `PRE-MAIN Branch Fan-in Receipt Integrity (sourcefree)`, job `receipt-contract`;
   - requires independent approval;
   - denies unapproved direct/force pushes and bypass.
   - Read back `protected=true`, the exact required context and bypass list. A 403 from this credential is not installation evidence.

2. **PR #519 author and authorized maintainer:** rebase/merge-forward the reviewed PR #519 head onto current PRE-MAIN `8e44ca9c`, keep the 32/32 corpus and F0R3 validator patch, and re-lock the new exact head. The current PR merge ref still targets `299f41e9`; it is not current.

3. **Original PRE-MAIN owner:** approve the exact initial 11-event seed provenance and the re-locked source cut. Until then the seed remains `PENDING`, not canonical authority.

4. **Authorized maintainer/source owners:** authorize a separate privileged verifier for signed source/science ownership, merged target SHA, real importing first consumer, and paired CURRENT_PROGRESS MD+JSON. The offline validator cannot be that verifier.

5. **Sorok incumbent:** reconcile the current MD revision 36 with JSON revision 35 in one truthful paired CAS revision at the same commit. This review did not edit either file.

6. **FIABC/Pyat owner:** classify F0R3's observed governed run with 144 pass / 3 fail against the base and changed source. This review did not rerun it; it is separate from the receipt-contract job.

7. **HQ/F4 owner:** abandon F4 as a parallel activation branch or explicitly re-cut it from the reviewed PR #519 head. Do not maintain a second competing control law or shadow HQ.

## Owner CAS boundary

The only lawful adoption sequence is:

1. exact PR head re-locked on current PRE-MAIN;
2. independent review acceptance of the exact F0R3 validator patch;
3. seed owner approval and privileged verifier evidence;
4. administrator-required check and independent approval installed/read back;
5. authorized maintainer protected merge/CAS;
6. post-merge readback of both progress files at the same revision/commit and the real importing first consumer;
7. append-only adoption event only after the real merged commit exists.

No field, branch name, CI green run or filled JSON receipt can substitute for these gates.
