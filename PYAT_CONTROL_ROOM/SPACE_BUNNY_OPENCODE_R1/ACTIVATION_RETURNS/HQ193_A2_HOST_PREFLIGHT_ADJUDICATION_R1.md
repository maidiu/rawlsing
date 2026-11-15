# HQ193 — A2 unattended acceptance, host-preflight adjudication, and worktree reclamation law

Status:
`A2_ADOPTED_UNATTENDED_SOURCE_FREE_WITH_BOUNDED_RESIDUALS__HOST_DISK_POLICY_PENDING__STALE_WORKTREE_RECLAMATION_AUTHORIZED`

## Dispatcher A2

Worker:
`agent/rabochii-pyat-hq191-a2-dispatcher-unattended-hardening-r1 @ 4b0b33102998abf9ce29fc0e584e278c85a44fe7`

Substantive candidate:
`50829fd0fba24eefd457abeb3cba4cd365460296`

Dispatcher blob:
`2db72c887b032622e09da6a5bd7723f7fb7055ee`

Independent hostile review:
`agent/reviewer-pyat-hq192-a2-dispatcher-unattended-hostile-review-r1 @ 99d6c2fb5fcee594b2f58a69934ccb92890dee13`

Accepted review disposition:
`ACCEPT_UNATTENDED_WITH_BOUNDED_RESIDUAL_LIMITATIONS`

HQ adopts the A2 dispatcher into control for:
`UNATTENDED_SOURCE_FREE_ORCHESTRATION_ON_THIS_HOST_WITH_BOUNDED_RESIDUAL_LIMITATIONS`

### L-1 reviewer-independence correction

The A2 worker correctly carried L-1 as unmet because a worker cannot self-certify reviewer independence.

The governing earlier review defined the relevant minimum repair as:
- different model/variant or different authority occupies the reviewer role;
- worker and reviewer identities differ and are recorded.

The HQ192 reviewer is DeepSeek V4.1 Flash and explicitly records independence from Space Bunny. Therefore:
`L-1_REVIEWER_INDEPENDENCE = SATISFIED`

The reviewer packet's prose that still says L-1 "remains unmet" is a stale carry-forward and is not current authority.

### Adopted capability ceiling

Allowed:
- unattended source-free worker/reviewer orchestration on this exact host;
- bounded multi-process admission using the repaired atomic slot transaction;
- scoped OpenCode permissions with blanket `--auto` refused;
- dispatcher-generated authority framing and byte-bound commission delivery;
- fail-closed Seatbelt requirement: absence/application failure must refuse launch rather than silently degrade;
- local Git/worktree/GitHub publication and return mechanics under existing HQ authority.

Explicitly not claimed:
- hermetic process isolation;
- network egress containment or destination filtering;
- role-level security from `--agent`;
- prompt-injection immunity;
- portability of `sandbox-exec` to future macOS releases;
- raw-source or live-C4 authority.

Operational restriction pending a future hardening:
- caller-supplied `permission_profile` overrides must not be used for unattended lanes unless HQ has explicitly reviewed them; the default scoped profile is the accepted unattended profile.
- the non-atomic shape of `deliverReturn` idempotence is a bounded residual, not a demonstrated current failure; a follow-up hardening may close it.
- writable OpenCode state/cache/config paths and unrestricted network egress remain disclosed limitations.

MR-4 kernel enforcement was not executable inside the DeepSeek review sandbox. HQ acceptance at this grain relies on:
- worker live kernel-enforcement evidence on the operating host;
- independent source inspection of fail-closed launcher behavior;
- absence of a counterexample in hostile review.
This is a bounded host-local acceptance, not a universal containment proof.

## Host preflight

Worker:
`agent/rabochii-pyat-hq192-host-preflight-remediation-r1 @ d3d2561980723fc20fedde9270aa5b5cbc9bf465`

Accepted disposition:
`HOST_PREFLIGHT_POLICY_THRESHOLD_REQUIRED`

Closed:
- root-anchored `/LOCAL_COURTS/` ignore law;
- dangling short interpreter symlink;
- exact freeze/tree/interpreter preflight helper.

Still open:
`HOST-PREFLIGHT-F3-DISK-CAPACITY-VOLATILITY`

Measured:
- free space 4.21–5.22 GiB in the reported series;
- 1.00 GiB maximum single 4-second interval swing;
- 499 MiB safely reclaimed by the worker;
- no governed source/output/peak-footprint magnitude exists from which a numeric live-run threshold can be derived.

HQ therefore does **not** invent a live-C4 disk threshold in HQ193.

The preflight remains correctly fail-closed until:
1. stale local worktrees are reclaimed;
2. post-reclamation free-space floor is measured;
3. HQ adopts an explicit operational safety threshold as a policy value, clearly typed as policy rather than historical/empirical source evidence.

## Worktree reclamation authority

The user's standing request is to remove unnecessary duplicate Rawlsing checkouts while preserving any unique local work and all current jobs.

HQ authorizes:
`SALVAGE_THEN_REMOVE_STALE_REGISTERED_WORKTREES`

A registered historical worktree may be removed if:
- it is not the canonical checkout;
- it is not an active current lane;
- no same-user active process is using it;
- its HEAD/local lineage is covered by origin;
- every unique local substantive tracked/untracked delta is first explicitly salvaged outside the repository with origin/base identity;
- disposable cache residue is not treated as preservation authority;
- no raw/source/sensitive unknown is encountered;
- removal uses `git worktree remove` after sanitation, not blind `rm -rf`.

Currently active/preserved local lane:
- `agent/rabochii-pyat-hq192-r9-os-accounting-interposition-r1` until returned.

The already-returned HQ192 A2 reviewer and host-preflight worktrees are no longer active merely because their directories exist; they may be reclaimed once same-user process use and unique local residue are cleared.

Do not automatically delete:
- `LOCAL_COURTS/**`;
- `data/**`;
- `deepseek-harness`;
- Git loose objects/shared object database;
- raw/source estates;
- user documents.

Git object pruning and `deepseek-harness` reclamation require separate later adjudication after active lanes finish.

## Worktree lifecycle law

The canonical commission template and operating design now state:
- worktrees are temporary execution isolation, not archival state;
- returned/reviewed/integrated worktrees should be audited and removed once no active process or successor needs them;
- unique local substantive deltas must be committed/pushed or explicitly salvaged first;
- cache files do not justify retaining an entire historical checkout.

## Current C4 stage

- freeze acceptance blockers: 0
- warrant-instrument blockers: 1 — R9
- live-execution blockers: 1 — host disk policy/capacity
- R7: CLOSED
- HQ182 temporary C4 non-adoption hold: still pending reserved Astra decision

No source access, locator discovery, warrant issuance, live C4, C7 or actor/person work is authorized by this decision.
