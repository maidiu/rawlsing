# Pyat HQ195 — sparse-by-default law adopted; R9 architecture/runtime fork bound

Status:
`SPARSE_BY_DEFAULT_LAW_ADOPTED__R9_ARCHITECTURE_WARRANT_FORK_BOUND`

## Sparse checkout law

Local worker/reviewer commissions now default to:
`SPARSE_REQUIRED`

A full materialized working tree is exceptional:
`FULL_REQUIRED`

and must carry a concrete reason that sparse checkout would alter test discovery, imports, packaging, repository-wide behavior, or another property under proof.

Fresh full clones are not the normal worker mechanism.

Canonical helper:
`PYAT_CONTROL_ROOM/SPACE_BUNNY_OPENCODE_R1/runtime/prepare_sparse_worktree.sh`

The helper:
- reuses the canonical clone and shared Git objects;
- fetches origin;
- verifies the exact remote commissioned SHA;
- refuses destination reuse;
- refuses same-named local-branch ambiguity;
- creates `--no-checkout` worktree state;
- applies the exact non-cone sparse manifest;
- verifies exact HEAD and clean startup.

Read-only evidence outside the sparse materialization set should normally be accessed with exact Git-object commands.

Silent conversion of a SPARSE_REQUIRED commission into a full checkout is prohibited.

Returned sparse worktrees remain temporary execution state and follow the existing salvage/remove lifecycle law.

## R9 state

R9 remains open.

Accepted HQ194 state:
- current host runtime cannot lawfully observe/enforce literal compiled-reader OS path-open accounting with the tested unprivileged mechanisms;
- SRC26 header-prefix owner is now located and governable at the Python layer;
- selected-column count has no executable reader owner in the current closure;
- O1-C07 remains unsatisfied at the literal path-open account.

The authority/runtime fork is now investigated in parallel.

## Active lanes

### Space Bunny — stage ownership / architecture warrant

Branch:
`agent/rabochii-pyat-hq195-r9-stage-ownership-architecture-warrant-r1`

Commission tip:
`501494b18afdd623fc3561951daf36714e5690c9`

Checkout:
`SPARSE_REQUIRED`

This lane reconciles pre-issuance, issuance, pre-launch, during-execution and return ownership and tests whether the remaining problem satisfies C4's explicit ARCHITECTURE_WARRANT terminal.

### Space Bunny — minimally instrumented runtime feasibility

Branch:
`agent/rabochii-pyat-hq195-r9-instrumented-runtime-feasibility-r1`

Commission tip:
`f895b3dc2934a3d742722657ea43ba174d10043b`

Checkout:
`SPARSE_REQUIRED`

Materialized runtime surface is limited principally to `rawlsing_next/` plus the lane's own commission/return/evidence paths. It tests whether a disposable instrumented pyreadstat/ReadStat runtime could expose/enforce the literal missing account and states the exact R7 requalification burden.

### DeepSeek — independent governing-contract interpretation

Branch:
`agent/reviewer-pyat-hq195-r9-contract-independent-interpretation-r1`

Commission tip:
`a48acdc2f7e26557fca8e387b12c619bb94fe447`

Checkout:
`SPARSE_REQUIRED`

The reviewer must not read the parallel stage worker's conclusion before returning its own interpretation.

## Current blocker register

- freeze acceptance blockers: 0
- warrant-instrument blockers: 1 — R9
- live-execution blockers: 1 — host disk policy/capacity
- R7: CLOSED

HQ182 temporary C4 non-adoption hold remains pending the reserved Astra decision.

## Holds

No source locator discovery.
No warrant issuance.
No raw-source access.
No live C4.
No C7.
No PRE-V3→V3 actor/person implementation.

Next:
`LAUNCH_ALL_THREE_HQ195_SPARSE_LANES_IN_PARALLEL__HQ_ADJUDICATES_FIRST_RETURN`
