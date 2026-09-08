# OBL060 BOUNDED REPAIR R2 — INDEPENDENT HOSTILE MATRIX

Reviewer identity:
`RABOCHII_SUBV_E_OBL060_BOUNDED_REPAIR_R2_INDEPENDENT_HOSTILE_REVIEWER_R1`

Frozen repaired target:
`c35d98db1ef787fb3a4986a963d7c389bd841432`

Reviewer base execution-control commit:
`865d2cbe9aa323d334b2eae42150f1cf2db03a4d`

This reviewer is distinct from the occurrence-authority identity and the candidate/source-owner implementation role. It may attack only. It must not modify either R1 or R2 candidate semantics.

## Attack families

1. Reproduce the R1 blocker against R2: `issued_at_epoch=True` must fail closed.
2. Boolean expiry timestamps (`True` and `False`) must fail closed.
3. Boolean `now_epoch` values must fail closed.
4. Exact-type protection must reject arbitrary `int` subclasses for issuance, expiry, receipt fields, and `now_epoch`.
5. A digest-consistent receipt whose timestamp is mutated to boolean must still fail before acceptance.
6. A malformed receipt issued directly through the frozen R1 implementation must not be launderable through R2 validation.
7. Non-integral timestamp representations (float/string/None) must fail closed.
8. Valid exact built-in integer timestamps must remain accepted for the one lawful `NONCURRENT_SYNTHETIC` positive fixture.
9. R2 must not change occurrence-authority identity, independence-authority identity, mandatory rejection bases, scope, receipt kind, or fixture class.
10. Occurrence and independence authority identities must remain non-identical.
11. R2 must not expose any forbidden effect surface or current-positive mutation surface.
12. All R1 mandatory-rejection bases must remain rejected through the R2 authority surface.

## Review law

A hostile PASS requires every attack above to pass without repairing the target. Any failure returns the smallest exact blocker. No second reviewer is authorized within this review identity.
