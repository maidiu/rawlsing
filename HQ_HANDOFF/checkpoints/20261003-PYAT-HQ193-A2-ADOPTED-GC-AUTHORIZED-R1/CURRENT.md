# Pyat HQ193 — A2 adopted; host disk policy pending; stale worktree reclamation authorized

Status:
`A2_ADOPTED_UNATTENDED_SOURCE_FREE_WITH_BOUNDED_RESIDUALS__HOST_DISK_POLICY_PENDING__STALE_WORKTREE_RECLAMATION_AUTHORIZED`

## Dispatcher

Adopted dispatcher blob:
`2db72c887b032622e09da6a5bd7723f7fb7055ee`

Worker:
`agent/rabochii-pyat-hq191-a2-dispatcher-unattended-hardening-r1 @ 4b0b33102998abf9ce29fc0e584e278c85a44fe7`

Substantive candidate:
`50829fd0fba24eefd457abeb3cba4cd365460296`

Independent review:
`agent/reviewer-pyat-hq192-a2-dispatcher-unattended-hostile-review-r1 @ 99d6c2fb5fcee594b2f58a69934ccb92890dee13`

Accepted disposition:
`ACCEPT_UNATTENDED_WITH_BOUNDED_RESIDUAL_LIMITATIONS`

Capability:
`UNATTENDED_SOURCE_FREE_ORCHESTRATION_ON_THIS_HOST_WITH_BOUNDED_RESIDUAL_LIMITATIONS`

L-1 reviewer independence is satisfied by DeepSeek V4.1 Flash reviewing Space Bunny's candidate.

Not claimed:
- hermetic isolation;
- network egress scoping;
- role-level security from --agent;
- prompt-injection immunity;
- raw-source or live-C4 authority.

Default scoped permission profile is the accepted unattended profile. Caller-supplied permission-profile widening is not authorized for unattended lanes absent later HQ review.

## Host preflight

Return:
`agent/rabochii-pyat-hq192-host-preflight-remediation-r1 @ d3d2561980723fc20fedde9270aa5b5cbc9bf465`

Accepted disposition:
`HOST_PREFLIGHT_POLICY_THRESHOLD_REQUIRED`

Closed:
- root LOCAL_COURTS ignore;
- short interpreter symlink;
- exact freeze/tree/interpreter preflight.

Open:
`HOST-PREFLIGHT-F3-DISK-CAPACITY-VOLATILITY`

HQ193 does not invent a numeric live-run threshold before stale checkout reclamation and absent governed peak-footprint evidence.

## Worktree reclamation

Authorized:
`SALVAGE_THEN_REMOVE_STALE_REGISTERED_WORKTREES`

Preserve:
- canonical checkout;
- currently active R9 OS-accounting lane;
- any worktree used by an active same-user process;
- any unique substantive local delta until salvaged;
- any source/sensitive/unknown material;
- LOCAL_COURTS, data, deepseek-harness and shared Git objects.

Returned/reviewed historical worktrees are not archival authority and should not persist merely due disposable cache residue.

## C4

Current register:
- freeze acceptance blockers: 0
- warrant-instrument blockers: 1 — R9
- live-execution blockers: 1 — host disk policy/capacity
- R7: CLOSED
- advisories: 9
- counterexamples: 1

HQ182 temporary C4 non-adoption hold remains pending reserved Astra adjudication.

Active implementation:
`agent/rabochii-pyat-hq192-r9-os-accounting-interposition-r1`

## Holds

No locator discovery.
No warrant issuance.
No raw-source access.
No live C4.
No C7.
No PRE-V3→V3 actor/person implementation.
