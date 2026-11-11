# LiTS accepted replay transport repair

## Source-backed failure preserved

The first local pre-candidate replay at execution head
`ef8eff9625f269173ac2c17af3f92d913babb275` passed the Darwin runtime gate,
both exact source SHA gates, and the candidate-neutral WVS oracle producer.  It
then stopped before the LiTS oracle and before T3 with:

`Pre553IntegrityError: float/NaN/Infinity forbidden in semantic identity`

No candidate process or measured P2X cell was started.

The traceback established a production integration defect: the successor
producer applied the new response-slot representation authority but bypassed
the exact accepted banked producer's pinned `exact_cell` physical transport
adapter.  The historical facade therefore received a decoder float from a
projected slot and rejected it before response-state lookup.

## Bounded repair

Code head `d74a9e571ee80ee250f9ce51682ddad4ec5b6faf` now composes the two already
pinned laws in order:

1. apply the exact LiTS-I q301_2/q301_7 representation authority; then
2. pass every replay cell through `exact_cell` from the exact accepted banked
   producer blob `c51b56779ab9d79126619b7733d41f5253c8150f`.

This restores the accepted transport path.  It does not change the live global
typed-key law, infer semantics from values or labels, or broaden the new
response representation authority.  Regression coverage consumes the actual
cell iterator and checks both a governed response float and a numeric
coordinate float, closing the gap that the prior mock failed to exercise.

## Source-free requalification

Qualification closure head: `b73ceb069d284f63856563b51c651e2605b0bf88`.

The required complete source-free qualification produced:

- `172 passed, 28 subtests passed in 27.89s`
- `RAWLSING_RECONCILED_FIABC_STATIC_CROSS_LANE_ASSERTIONS_PASS`
- `RAWLSING_CANONICAL_REINTEGRATION_SOURCE_FREE_QUALIFICATION_GREEN__READY_FOR_PRE_CANDIDATE_FREEZE`

The qualification did not read LiTS or WVS source bytes and did not construct
an oracle, freeze T3, start A/B/C, or run measured P2X.

The pre-candidate and measured launch guards are rebound to the code and
qualification heads above.  A fresh local source-backed pre-candidate court is
still required; this receipt does not claim that court is green.
