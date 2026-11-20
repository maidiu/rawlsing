# P0 R2 finite handoff — affirmative analysis decision, actual carrier refusal

## Base

`21d38962d44a89f6f08f3b9df345f5a33edd0915` on
`agent/pyat-p0-two-saved-waves-20261120`, starting from C6
`27e5464f10e8f1339f57cde734b5ae42084b33a8`.

## Actual result

- Recorded a new, scoped, affirmative user analysis decision for the two exact
  saved releases: Arab Barometer Wave 1/SRC04 and GSS1972/SRC16, host
  `MainMac`, purpose `P0_TWO_SAVED_WAVES_ANALYTICAL_DOWNSTREAM_R2`.
- Preserved the existing construction receipts and did not alter any historical
  grant.
- Bound each exact decision through the existing `IssuedWorkloadRecord` /
  `CurrentDecisionResolver` shape and attempted the first C6 real-carrier gate.
- Both waves independently refused at `TYPED_EXTERNAL_I02_ROOT_ADMISSION`:
  `ExternalI02IntegrityError: unsupported externally held certificate schema`.
  The actual saved carriers are `ANVIL_STREAM_C11_ESTATE@1`; C6 direct admission
  requires its direct-I02 carrier.
- No source was opened, no Parquet was read, and no respondent rows were
  emitted. I03/I05/Batch/S04/DHIKR/FF01/C4/C5/C6 are `NOT_REACHED`.
- The stream-carrier-to-direct-I02 adapter is a broader REMONT seam, not a P0
  ordinary repair. No projection/rebuild/run bypass was used.

## Disjoint branch

The prior sourcefree C6 vertical (131/131, C4+C5 22/22, C4+C5+C6 36/36) remains
accepted engineering evidence at `21d38962…`, but is expressly **not** used as a
substitute for the actual saved-wave run.

## Scope limits

This return does not establish a valid estimator, a preexisting compiler-issued
QUERY, or native-provider compatibility. No protected edits, no public
respondent data, no raw survey reopen and no expanded waves.
