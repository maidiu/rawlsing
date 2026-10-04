# Pyat HQ200 — session/plan adjudicated; warrant-binding wave

Status:
`SEVEN_SOURCE_PLAN_ACCEPTED__SRC27_ONE_OPEN_COMPATIBLE__SESSION_CANDIDATE_PENDING_REVIEW__WARRANT_BINDING_WAVE`

Accepted seven-source plan:
`09e1325da6ee880374a4065ae748cc03de93c421`

Session candidate:
- code-bearing: `90ccbd54c549f67358d0c02ad18ff90b843cf3ee`
- clean tip: `76970cfdfc8968e975595ea288cf44b448205e30`
- adopted: NO; independent acceptance pending.

## SRC27 count semantics

HQ accepts one-open compatibility and the descriptive reading of the historical "multiple path-level opens" phrase.

Frozen authority:
- full_route_passes: expected 1 / max 1
- full_reads: floor >=1; no frozen ceiling
- decoder_invocations: mandatory account, historical expected count unbound
- path_opens: mandatory account, historical numeric value unbound
- retries: max 0

Implementation policy may impose decoder_invocations max 1, but it must remain typed as policy, not historical expectation.

Outer Route-B pass remains distinct from decoder/full/chunk/reader/path-open accounts.

## Source-plan consequences

- SRC02: SELECTED Q10B; full 0; no prefix.
- SRC06: SELECTED Q101/Q2061B; full 0; no prefix.
- SRC08: METADATA_ONLY + Big5; selected/full 0; no prefix.
- SRC12: METADATA_ONLY + Windows-1252; selected/full 0; no prefix.
- SRC14: SELECTED v372; full 0; no prefix.
- SRC26: METADATA_ONLY + exact 176-byte prefix; selected/full 0.
- SRC27: FULL + latin1 + outer full-route pass exact/max1; no prefix.

Encoding does not determine row-data mode.

## Active SPARSE_REQUIRED lanes

Independent session acceptance:
`agent/reviewer-pyat-hq200-r1 @ f10b35a0e013695f598e6fe951c5282e0aa480a2`

Generic warrant-plan + outer route-pass binding:
`agent/rabochii-pyat-hq200-r1 @ 8b977a2e33a1f03e34ea3cc5b815bc2525f388ab`

Unsigned seven-source warrant successor:
`agent/rabochii-pyat-hq200-r2 @ e15d3647fbc1e149786a3f33e660ac2e16e0f78f`

## Remaining source-free frontier

- session candidate independent acceptance;
- outer full-route-pass account/ceiling;
- generic bound execution layer;
- warrant instrument/runtime-plan binding;
- source-dependent numeric byte budgets remain unbound.

R9 remains open.
Host disk policy/capacity remains the separate live-run blocker.
HQ182 C4 non-adoption hold remains pending reserved Astra.
All source/warrant/live/C7/actor holds remain.

Next:
`LAUNCH_ALL_THREE_HQ200_SPARSE_LANES_IN_PARALLEL`
