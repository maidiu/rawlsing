# HQ192 — R7/R9/A2 adjudication

Status:
`R7_CLOSED__HOST_PREFLIGHT_BLOCKER_SUBSTITUTED__R9_REMAINS__A2_HOSTILE_REVIEW_REQUIRED`

## R7

Reviewed worker:
`agent/rabochii-pyat-hq190-b-r7-darwin-environment-closure-r1 @ def6d369878cb273ca06f97e08c4fb0a2964611e`

Reviewed hostile acceptance:
`agent/reviewer-pyat-hq191-r7-darwin-environment-hostile-acceptance-r1 @ b0169b1ceb79e7e8b918e643d5164ec15f67dae5`

HQ accepts:
`ACCEPT_R7_CLOSED__SEPARATE_HOST_PREFLIGHT_BLOCKER_REMAINS`

R7 is therefore **closed**.

The previous live-execution blocker is removed as R7 and replaced by a separately typed host-preflight blocker:

`HOST-PREFLIGHT-F3-DISK-CAPACITY-VOLATILITY`

Reason:
- data volume repeatedly at 99–100%;
- approximately 2–6 GiB free during independent review;
- multi-gigabyte governed live C4 would risk uncontrolled ENOSPC after partial writes;
- partial/retry-dependent evidence is not acceptable for the governed run.

This is not a defect in the R7 environment qualification.

Additional host-preflight hazards:
- `LOCAL_COURTS/` is not ignored and is multi-GiB;
- the short interpreter symlink is dangling;
- interpreter portability remains host-local;
- exact freeze execution must remain SHA-pinned to `8ff40d37de69db2d8a6053a7c2242f481677f1a4`.

Cross-lineage difference between control ancestry and the executable freeze is classified:
`EXPECTED_CROSS_LINEAGE__NOT_A_REGRESSION__NOT_A_BLOCKER_WHILE_EXECUTION_IS_EXACT_SHA_PINNED`.

## R9

Reviewed return:
`agent/rabochii-pyat-hq191-r9-budget-enforcement-court-r1 @ 1067828d75f3eab483e9b2a95e4b3ef703661118`

HQ accepts:
`R9_PARTIAL__SPECIFIC_ACCOUNTS_STILL_UNGOVERNABLE`

R9 remains the sole warrant-instrument technical blocker.

Accepted findings:
- historical expected counts, synthetic observations and proposed policy maxima remain correctly separated;
- seven mandatory account classes are governable at the Python reader/decoder layer with pre-operation abort demonstrated;
- no OS-open count was fabricated;
- path-level `open(2)` inside the compiled reader remains invisible to Python interception;
- selected-column operations occur above the decoder layer and must be bound where they actually occur;
- SRC26 header-prefix operation must be bound at the layer that performs it;
- byte counts remain conditional on an observable layer;
- SRC27's four lower-layer accounts remain separately typed and are not derived from the one-pass law;
- SRC35 remains hard-zero fresh access.

The proposed C3 maxima remain **candidate policy ceilings**, not adopted warrant authority and not historical facts.

The next R9 lane must test the remaining lower/higher layers directly rather than weakening O1-C07 by relabeling logical accesses as path opens.

## Dispatcher A2

Returned:
`agent/rabochii-pyat-hq191-a2-dispatcher-unattended-hardening-r1 @ 4b0b33102998abf9ce29fc0e584e278c85a44fe7`

Substantive implementation:
`50829fd0fba24eefd457abeb3cba4cd365460296`

Dispatcher blob:
`2db72c887b032622e09da6a5bd7723f7fb7055ee`

Claim:
`CANDIDATE_READY_FOR_UNATTENDED_HOSTILE_REVIEW`

HQ does not adopt this candidate yet.

The candidate reports:
- MR-1 atomic admission;
- MR-2 sequence ownership;
- MR-3 scoped OpenCode permissions with `--auto` refused;
- MR-4 kernel-enforced macOS Seatbelt containment;
- MR-5 commission byte binding + dispatcher-generated authority frame;
- MR-6 proven-dead lock reclaim + directory fsync;
- 44/44 regression;
- live OpenCode E2E without `--auto`.

Independent hostile review is mandatory before any unattended capability lift.

## Current stage register

C4/freeze technical state:
- freeze acceptance blockers: 0
- warrant-instrument blockers: 1 — R9
- live-execution blockers: 1 — HOST-PREFLIGHT-F3-DISK-CAPACITY-VOLATILITY
- R7: CLOSED
- advisories: 9
- counterexamples: 1 — historical overbroad M01 closure justification

HQ182 temporary C4 non-adoption hold remains pending the reserved Astra decision.

## Hard holds

Still prohibited:
- locator discovery;
- warrant issuance;
- raw-source access;
- live C4;
- C7;
- PRE-V3→V3 actor/person implementation.
