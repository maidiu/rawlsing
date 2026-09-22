# LiTS ASTRA hash-domain closure

## Observed local blocker

The source-backed pre-candidate court at governed head
`7acd86ea5f83ae620e62e0db104b4958bbfb7875` passed the runtime/source gates,
the WVS candidate-neutral oracle, LiTS representation replay, current common
C11, neutral I05, and retained constituent-I03 closure. It then stopped before
candidate execution at:

`current neutral LiTS learned product does not equal accepted ASTRA identity`

The run reported zero candidate outputs and zero candidate processes.

## Exact defect

The stopped comparison crossed identity domains. It compared
`semantic_hash(PRE553_LEARNED_EMPIRICAL_EXECUTION_RECEIPT@1.0.0)` with the
immutable identity of the historical
`ASTRA_D04_R2_TYPED_LEARNED_EMPIRICAL_PRODUCT@1.0.0`. Those are distinct
schemas and their object hashes are not interchangeable.

The accepted ASTRA product remains immutable. The lawful cross-representation
gate is the accepted semantic replay identity, together with the exact accepted
frontier cardinality and typed terminal counts.

## Repair

Code head `28b29ac728dc816eaf4ccd1e0d7a021d20bd935e`:

- preserves ASTRA product identity
  `47d36b1459c2458c480b58631d2c78af68be4dde44015a9220b09177b1eeb28d`
  as the immutable prior-product anchor;
- requires current neutral semantic replay identity
  `301735d4563314a0d7c133fa1afbb0ca57679b3fad887c66e77a909494779eb5`;
- requires exactly 50 candidates, 77 query roles, 49
  `EVALUATED_SUPPORTED`, and 1 `EVALUATED_VALID_EMPTY`;
- keeps the current carrier-neutral execution identity separately as the
  replay/exact-output identity;
- fails closed on semantic replay, terminal count, cardinality, or execution
  identity drift.

No value/label/frequency/missingness semantics were inferred. No A/B/C
candidate path was invoked.

## Source-free qualification

Qualification closure head:
`96a9301d37f67bfb02c5bda1efc50b17b37b581d`.

Result:

- `190 passed, 28 subtests passed`;
- `RAWLSING_RECONCILED_FIABC_STATIC_CROSS_LANE_ASSERTIONS_PASS`;
- `RAWLSING_CANONICAL_REINTEGRATION_SOURCE_FREE_QUALIFICATION_GREEN__READY_FOR_PRE_CANDIDATE_FREEZE`.

The next required evidence is a fresh local source-backed pre-candidate rerun.
It remains candidate-neutral and must stop before A/B/C.
