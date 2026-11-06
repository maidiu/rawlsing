# D r9 evidence and commands

## Actual production-wrapper transport probe

Sourcefree SAV/config, selected `A/B/Y`, coordinate `G`; actual
`execute_native_compiler_source` with state-root and explicit permission.

| Case | Result |
|---|---|
| `state_root` only | accepted; no envelope artifact; `transport=null` |
| empty permission with state-root | refused `EXPLICIT_PRODUCER_PERMISSION_CEILING_REQUIRED`; no artifact |
| invalid permission string | same refusal; no artifact |
| positive + explicit ceiling | 30 facts / 30 envelopes / 15 ops / 18 candidates |
| changed post-consumer decision `A,A,B` | refused `SOURCE_READ_DECISION_CHANGED_AFTER_CONSUMER`; **artifact still present** |

Positive artifact: all 30 envelopes use the exact caller ceiling, all arities are
1, all 30 E responses are `TYPED_REFUSAL` /
`FIELD_FORGE_TWO_TARGET_RELATION_REQUIRED`, zero support profiles,
`structural_grant=false`, `raw_respondent_rows_included=false`.

Cold CLI on the first persisted envelope: exit 0, typed arity refusal,
`structural_grant=false`.

The blocking defect is the artifact left from the changed-postdecision refusal:
transport is written before the postdecision equality check.

## Changed sourcefree input

Changing one actual controlled SAV value produced a changed first fact ref and
changed envelope fact identity while preserving 30 facts; no positive profile
was forced.

## Preserved / test evidence

- Author focused test: 1 passed in 6.03s; it covers helper calls, permission
  refusal, missing-query fake, cold CLI, and tampered replay, but not the actual
  wrapper changed-postdecision artifact boundary.
- E codec code blob at accepted `f708b468…` and D head: `6acba005…` exact.
- Prior G `0360d2b4…` and `193594a1…` proofs retained; prior G R5 positive/held
  alias and R6 ABBA corrections remain historical.
- Floors preserved: 18,276/18,413/18,467; current 7/694/683/11; historical
  20/991; route 676/4,705/249.

## Limits

No original source read, actual original facts, E authentic handshake, A/C
scale, full-estate floor, 650 s decode, code repair, product edit, native/science
or protected acceptance. Sourcefree probes are TEST_ONLY_SOURCEFREE.
