# LiTS explicit validation-rule authority closure

## Preserved source-backed blocker

The local pre-candidate court at
`7b38c22dd469735eed0b0c01c304a028dd3046cf` passed runtime, both source SHA
gates, WVS oracle standardization, LiTS physical replay, the accepted C11
release, and entered the candidate-neutral I05 discovery executor.  It stopped
before LiTS oracle output and T3 with:

`Pre553AuthorityError: candidate validation rule exceeds exact discovery validation authority`

No A/B/C process or measured P2X cell was started.

## Exact authority fact

The pinned LiTS DiscoveryAuthority
`52f4b3c1e7b8697e4350d175ba1de7806bef55a1c719848546414854d2b2f829`
contains five explicit `validation_rules.rules` records.  Their literal `kind`
fields are exactly:

- `CONDITIONAL_REVERSAL`
- `DISTRIBUTION_DIFFERS_FROM_BASELINE`
- `JOINT_NOT_PRODUCT_OF_MARGINALS`
- `TARGET_CELL_SUPPORTED`

Those are exactly the validation kinds used by the frozen 50-candidate,
77-query-role frontier.  The executor previously read only the optional
`validation_rules.kinds` shorthand and ignored the more explicit rules.

## Fail-closed interpreter repair

Code head `3bef6f693778cb4191fee3007134987991490296` recognizes literal kinds in an
explicit rules-only envelope.  It rejects malformed or unknown kinds, rejects
rules that exceed a simultaneously declared kinds envelope, preserves an empty
authority when neither representation is present, and does not infer any rule
from source values, outputs, labels, or frequencies.

This repairs authority interpretation without changing the frozen
DiscoveryAuthority, its identity, the runtime catalog, active binding, runtime
release, frontier, or candidate order.

## Source-free qualification

Qualification closure head: `d0313239a5e973b4a4cae87a39a16e4aca3066ab`.

- `186 passed, 28 subtests passed in 25.85s`
- `RAWLSING_RECONCILED_FIABC_STATIC_CROSS_LANE_ASSERTIONS_PASS`
- `RAWLSING_CANONICAL_REINTEGRATION_SOURCE_FREE_QUALIFICATION_GREEN__READY_FOR_PRE_CANDIDATE_FREEZE`
- `FIABC_LITS_EXPLICIT_VALIDATION_RULE_AUTHORITY_PASS [...] 50 77`

The qualification and authority audit were source-free and performed no oracle
construction, T3 freeze, A/B/C work, or measured P2X.  A fresh local
source-backed pre-candidate court remains required.
