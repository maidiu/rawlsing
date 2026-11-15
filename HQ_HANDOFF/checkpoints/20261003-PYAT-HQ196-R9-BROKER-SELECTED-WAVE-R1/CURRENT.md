# Pyat HQ196 — R9 contract settled; broker-selected wave bound

Status:
`R9_CONTRACT_MEANING_SETTLED__ARCHITECTURE_WARRANT_NOT_ADOPTED__BROKER_SELECTED_WAVE_BOUND`

## Accepted interpretation

O1-C07 requires two distinct stages:
- before launch: expected budgets, instrumentation and measurement basis are frozen;
- during execution/return: exact observed counts are measured and retained.

Literal path-level opens, reader invocations and decoder invocations remain non-substitutable accounts.

## HQ195 adjudication

Architecture-warrant candidate:
`NOT_ADOPTED`

Reason:
HQ195 runtime feasibility found an existing pyreadstat 1.3.6 file-like-object seam. On that candidate route the application can own the path-level open and supply a file-like object to the compiled reader without rebuilding pyreadstat, using privilege, or changing the R7 package/runtime identity.

The broker route remains:
`FEASIBILITY_CANDIDATE__HOSTILE_REVIEW_AND_EQUIVALENCE_REQUIRED`

## Selected-read candidate gap

Frozen O1-C07 expects for SRC02/SRC06/SRC14:
- selected_reads = 1
- full_reads = 0

Exact freeze decoder has no `usecols`; its batch reader passes the source path to `read_file_in_chunks` without selected-column configuration.

Status:
`R9-SEL-03_CANDIDATE_IMPLEMENTATION_GAP__HOSTILE_REVIEW_REQUIRED`

## DQ-01

The later warrant candidate dropped C4B's per-source `source_access_accounting` blocks.

A successor instrument must restore them and keep:
- expected/pre-launch budget;
- measurement basis/instrumentation;
- runtime observed count

as distinct fields.

## Active SPARSE_REQUIRED lanes

Review:
`agent/reviewer-pyat-hq196-r9-broker-selected-hostile-review-r1 @ 98899701e80e13e9f716416aaf6cd8d7a21753d9`

Implementation — exact executable-freeze lineage:
`agent/rabochii-pyat-hq196-r9-broker-selected-implementation-freeze-r1 @ 55f75664949b4a92431b54351e7244ff1fa4a652`

Warrant/accounting successor:
`agent/rabochii-pyat-hq196-r9-warrant-accounting-successor-r1 @ 3e215413ead20bf62dd836f68eb22639ec873868`

Do not launch:
`agent/rabochii-pyat-hq196-r9-broker-selected-implementation-r1`
This provisional branch was created from documentary control before HQ caught the cross-lineage implementation-base error. It is uncommissioned.

## Blocker register

- freeze blockers: 0
- warrant-instrument blockers: 1 — R9
- live-execution blockers: 1 — host disk policy/capacity
- R7: CLOSED
- HQ182 C4 non-adoption hold: pending Astra

## Holds

No locator discovery, warrant issuance, raw-source access, live C4, C7 or actor/person work.
