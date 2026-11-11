# Pyat HQ — N10E AT17 adopted; C1-03 waits only on C1-03A + C1-03R

Checkpoint: `20261001-PYAT-HQ147-N10E-AT17-ADOPTED-C1-03-OVERNIGHT-R1`

Governing decision:
`HQD-2026-10-01-147`

## N10E / AT17

Accepted executable/test state:
`52e41a41e8bc3b77390016a049095b5aea1721d0`

Independent narrow rereview:
`43cdc1a8d1077be78a879ef06232a454736084d9`

Disposition:
`APPROVE_AT_DECLARED_GRAIN`

Banked integration branch:
`integration/pyat-hq147-n10e-at17-source-free-accepted-r1`

Provider blob:
`23167aa25291fb148b1e3cf210ac33fe7769b783`

Accepted grain:
`SOURCE_FREE_AT17_PROVIDER_CORE`

Final court:
`88 passed, 0 failed, 0 errors, 0 skipped, 15.14s`

Nonblocking rereview notes:
- `N10E-REREVIEW-DOC-001`: two fixture comments say changed P1 stays 60 although executable truth is 70.
- `N10E-REREVIEW-DOC-002`: reconciliation overstates literal shell-command presence in raw pytest output.

Neither affects code/proof acceptance.

## C1-03 active overnight lanes

### C1-03A — Space Bunny

Branch:
`agent/opencode-pyat-hq146-c1-03a-negative-route-consumer-r1`

Commission tip:
`da29402473ad671625feb49fad5142a1d689978b`

Scope:
`AT14 + AT15 + AT16`

### C1-03R — DeepSeek

Branch:
`agent/deepseek-pyat-hq146-c1-03r-replay-invalidation-r1`

Commission tip:
`8ce2a1aaa457fb1b08da9fca917dbb342bb98d41`

Scope:
`AT18 + AT19`

## C1-03 join condition

AT17 dependency is SATISFIED.

Final C1-03 join waits only for:
1. independently accepted C1-03A;
2. independently accepted C1-03R.

Then bind the combined C1-03 join against:
- accepted C1-02 AT08–AT13;
- accepted N10E AT17 provider core;
- accepted C1-03A AT14–16;
- accepted C1-03R AT18–19.

No raw-source execution.
No C4.
No C1-R before C1-03 join.
No PRE-V3→V3 actor implementation.
