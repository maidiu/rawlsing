# LiTS legacy physical-key closure

## Preserved source-backed blocker

The local pre-candidate court at
`ad63973cbd246b6c17a965b8692ba14ee7d1e221` passed runtime, both exact source
SHA gates, WVS oracle standardization, and the accepted banked `exact_cell`
transport.  It then stopped before LiTS oracle completion and before T3 with:

`SourceBackedC11FacadeError: unbound response value/state; no label/frequency/missingness inference`

No candidate process or measured P2X cell was started.

## Exact cause and bounded repair

The successor projection was constructed under the current typed physical-key
law, while the pinned accepted historical facade computes its response lookup
under the legacy physical-key law.  For example, the current exact governed
rule key for `Decimal(1)` is `194d2b63...`, while the pinned facade's legacy key
for the same accepted representation is `02902fd4...`.  Passing the current
keys unchanged into the historical owner therefore could not match any
response rule.

Code head `ea0baa4d87244a548ba9a6a46a883d307c65e3e4` now performs a closed
projection-owner adaptation before replay:

- exactly q301_2/194 and q301_7/199;
- exactly the seven already-authorized observed Decimal codes;
- exactly the declared system-missing binding;
- coordinate rules only for their already-declared system-missing binding;
- no weights, other slots, values, states, sources, labels, or inferred
  semantics.

Every unexpected slot or key fails closed.  The current global typed-key law
remains unchanged.

## Source-free qualification

Qualification closure head: `4c1641d1f1ec51a4116d0664dbf149e915465bdb`.

- `172 passed, 28 subtests passed in 22.98s`
- `RAWLSING_RECONCILED_FIABC_STATIC_CROSS_LANE_ASSERTIONS_PASS`
- `RAWLSING_CANONICAL_REINTEGRATION_SOURCE_FREE_QUALIFICATION_GREEN__READY_FOR_PRE_CANDIDATE_FREEZE`

The qualification was source-free and performed no oracle construction, T3
freeze, candidate work, or measured P2X.  The launch guards are rebound to the
new exact code and qualification heads; a fresh local pre-candidate court is
still required.
