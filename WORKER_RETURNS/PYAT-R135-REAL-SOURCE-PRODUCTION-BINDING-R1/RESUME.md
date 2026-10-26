# R135 resume

## Status

`PRODUCTION_TRANSPORT_QUALIFIED_ON_SYNTHETIC_HARNESS__NOT_SOURCE_RUN`

- Branch: `agent/opencode-pyat-r135-real-source-production-binding-r1`
- Startup/base: `d933411889dbcbcafc8d3a2c596e44fc69820f63`
- Return: `WORKER_RETURNS/PYAT-R135-REAL-SOURCE-PRODUCTION-BINDING-R1/`
- Source reads: 0. Synthetic harness only.

## Reached

- External 7-authority set accepted by source materializer.
- External production query authority accepted by catalog builder.
- New production transport calls existing `execute_issued_workload` with
  `allow_test_only=False`.
- Actual synthetic native positive, value-dependent output, restoration and
  exact refusal probes pass.
- Existing TEST_ONLY paths remain valid.

## External dependency

The binding needs a genuine source-specific authority set, exact query/discovery
law, U/Epre/native objects and a current `IssuedWorkloadRecord`. The source
custodian and competent scientific owner issue them. This is not a missing
runtime module or global unavailability.

## Next

Distinct existing reviewer, then source-specific production issuance. R131
stopped; all prior holds unchanged.
