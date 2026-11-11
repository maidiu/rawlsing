# GT12-C — FIELD FORGE EXACT CONDITIONAL-SUPPORT RELATION PRODUCER R1

Status:

`PASS__GT12C_FF_CONDITIONAL_SUPPORT_RELATION_READY_FOR_CENTRAL_INTEGRATION`

## Scope executed

Repository: `maidiu/rawlsing`

Branch:

`agent/rabochii-warplan-gt12-c-ff-conditional-support-r1`

Exact starting HEAD:

`2c95e64b9be9eb9c730028c840e04596dc556893`

Immutable implementation-wave instruction/evidence:

`17b9abc5c8c3038d14670c6e68136bb868f5073a`

Frozen canary contract:

`a9416094cbb4653dd2de2e4aa7b67577a355560c`

No sibling GT1/GT2 implementation branch was consumed.

## Implementation

Added:

- `rawlsing_next/field_forge_conditional_support.py`

The module implements only:

`EXACT_CONDITIONAL_SUPPORT_PROFILE_WITHIN_SCOPE@1.0.0`

with frozen role order:

- `CONDITIONER = Q86B`
- `TARGET = Q86A`

The producer consumes one exact I03 two-target `EmpiricalFact@1.0.0` plus its exact `EmpiricalQuerySpec@1.0.0`, scope/risk-set, authority, provenance and replay closure.

Positive output contains only:

- exact Q86B native condition-state identities;
- exact denominator/support count for each Q86B state;
- exact Q86A native target-state identities;
- exact Q86A x Q86B joint support counts;
- exact producer/query/risk-set/universe/authority/provenance/replay refs;
- exact producer and narrowed relation permission ceilings;
- `NONE__REFERENCE_PRESERVING`;
- deterministic relation identity and replay.

No ratio is computed or stored.

State-domain enumeration is explicitly:

`IDENTITY_ONLY__NO_ORDINAL_OR_METRIC_MEANING`.

The module verifies the I03 target-domain identity against the exact Q86B x Q86A query components and requires the complete native Cartesian cell projection for a positive relation.

## Typed nonpositive behavior

Nonpositive producer `EmpiricalFact` states do not self-promote.

The relation/result preserves the exact producer typed state, marks `producer_state_blocking=True`, and emits no positive count profile.

This keeps valid-empty/noncomparable/unresolved/integrity outcomes first-class without inventing replacement values.

## Permission law

The builder requires an exact producer permission ceiling supplied by the integrating caller and permits only an exact subset at FIELD FORGE relation grain.

Permission widening fails closed.

This lane does not mint the later `STRUCTURAL_MEDIATION_INPUT` admission permission; that remains GT12-D jurisdiction.

## Hostile tests

Added:

- `rawlsing_next/tests/test_field_forge_conditional_support.py`

Focused coverage includes:

1. exact Q86B condition denominators;
2. exact Q86A joint counts including observed zero cells;
3. no ratio field;
4. deterministic relation identity/replay;
5. frozen Q86B-conditioner / Q86A-target role order;
6. target-domain identity tamper rejection;
7. permission widening rejection;
8. nonpositive producer-state blocking;
9. exact query/authority/replay/scope preservation;
10. incomplete native joint-domain rejection.

## Explicit non-authority

The implementation does not create or infer:

- causal direction;
- conditioner-as-cause;
- target-as-effect;
- redistribution mechanism;
- pressure/pathway;
- structural mechanism;
- FIELD/CAPITAL/HEGEMONY/HOMOLOGY;
- population generalization;
- order, metric or geometry;
- actor fact or V3 transition;
- PRE-V3 admission;
- M1/V554 basis authority.

It does not modify I03, I04/P06, M1, M4, M5 or V3.

No source acquisition was performed. No PRE-MAIN or `main` movement was performed.

Terminal:

`PASS__GT12C_FF_CONDITIONAL_SUPPORT_RELATION_READY_FOR_CENTRAL_INTEGRATION`
