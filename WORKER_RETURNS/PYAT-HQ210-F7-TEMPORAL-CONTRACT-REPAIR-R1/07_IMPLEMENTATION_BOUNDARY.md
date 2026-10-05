# 07 — Repaired implementation boundary

Lane: `PYAT-HQ210-F7-TEMPORAL-CONTRACT-REPAIR-R1`

Status: **REPAIRED_CONTRACT_SUCCESSOR__NOT_ADOPTED__NO_IMPLEMENTATION**

This document answers the hostile review's implementation-ceiling question. It is not itself an implementation authorization.

## Exact future implementation surface

A later HQ commission may authorize exactly these production additions:

1. In `rawlsing_next/pre553_empirical_authority.py`, add exactly one authority kind:
   `TEMPORAL_COMPARABILITY`.
2. Add exactly one matching `AUTHORITY_KIND_CEILINGS` entry. The ceiling must be no broader than:
   **operation-scoped comparability and ordering of exactly identified temporal anchors for one governed use; production of the bounded temporal relation receipt; no downstream consumer power.**
3. Add one bounded temporal-comparison module implementing:
   - exact input/ref validation;
   - the three authorized order-basis classes plus the fourth typed no-basis refusal;
   - the deterministic 12-state precedence and scalar reason selection;
   - exact-zero `NO_AUTHORIZED_CHANGE`;
   - canonical replay/content addressing;
   - cross-field invariants and typed refusals.
4. Add a court for those exact laws.
5. For a cross-universe pair, consume a separately resolved positive `SOURCE_EQUIVALENCE` result through the existing source-relation authority path.

No other production surface is implied.

## Authority-kind ceiling obligation

The current authority registry has a strict kind/ceiling pairing. Therefore adding
`TEMPORAL_COMPARABILITY` necessarily requires its matching ceiling entry in the same
implementation change. A kind without a ceiling, or a ceiling without its kind, is invalid.

The proposed ceiling authorizes only:

- checking the exact pair against a bound comparability requirement set;
- using one exact authorized order basis where a basis exists;
- refusing when no lawful basis exists;
- emitting one bounded receipt with exact state, reason, delta/uncertainty where lawful, and replay material.

It does **not** authorize source selection, source equivalence, pooling, backfill, interpolation,
currentness, causal interpretation, trend, trajectory, temporal pressure, F8 conditioning, or
actor/person inference.

## Receipt registration decision

`TEMPORAL_RELATION_RECEIPT` **does not become a member of**
`PUBLIC_OBJECT_FAMILIES` under this contract.

It is a closed, immutable/content-addressed result object owned by the temporal comparison module.
Its `relation_state` is a module-local closed field validated by that module. It is **not**
`CanonicalSemanticObject.typed_state`.

Therefore this contract authorizes:

- **no** `PUBLIC_OBJECT_FAMILIES` edit;
- **no** `STATE_FAMILIES` edit;
- **no** widening of `CanonicalSemanticObject`.

If a future terminal consumer proves that public-object registration is necessary, that is a
separate authority/representation decision and must be recommissioned rather than inferred here.

## Existing typed-state law

Existing `AUTHORITY_STATE` values remain exactly where they already live.

When authority resolution returns `AUTHORITY_HASH_MISMATCH`,
`AUTHORITY_SCOPE_MISMATCH`, missing authority, conflict, or out-of-scope, the temporal producer:

1. preserves the exact authority-resolution state in provenance;
2. maps the receipt-level terminal outcome to `TEMPORAL_INSUFFICIENT_AUTHORITY`;
3. chooses the exact scalar temporal reason code under the repaired reason precedence.

No `AUTHORITY_STATE` literal is inserted into `TEMPORAL_RELATION_STATE`.

## Cross-universe two-path resolution

Cross-universe comparison requires **two independent positive paths**.

**Path A — source relation.** The existing source-relation owner resolves
`SOURCE_EQUIVALENCE` through its own authority discipline
(`RELATION_AUTHORITY_KINDS` / exact relation-authority validation). The temporal module cannot
mint, infer, or bypass this result.

**Path B — temporal comparison.** The temporal owner resolves exact
`TEMPORAL_COMPARABILITY` under the general authority registry and consumes the already-resolved
`source_equivalence_ref` as a prerequisite.

Both must be positive. Neither implies the other. Same-family membership is not equivalence;
source equivalence is not temporal comparability.

## Explicit non-surfaces

This contract cannot authorize implementation of:

- F8 consumption, conditioning, source selection, or possibility-geometry/distribution transform;
- cause, event attribution, mediation, or mechanism;
- continuity, interpolation, midpoint substitution, or inferred missing values;
- monotonicity, rate, trend, acceleration, or trajectory;
- >=3-anchor trajectory rules;
- rupture producer, rupture threshold, or causal event slot;
- source semantic equivalence creation, respondent linkage, overlap authority, pooling, or
  estimand composition;
- currentness or lifecycle selection;
- scalar temporal pressure, coefficients, magnitude bands, V553 deadbands, or V553 thresholds;
- `EmpiricalFact` time-field changes;
- a universal grain enum or universal point-year/interval binary;
- temporal-gap object creation;
- actor/person uptake, memory, belief, desire, orientation, capacity, distress, or development.

## Production surfaces explicitly frozen

A later implementation must not mutate merely to satisfy this contract:

- `FORBIDDEN_BACKFILL_TARGET_STATES`: its literal `TEMPORAL_NONCOMPARABLE` membership must remain;
- existing `FAIL_CLOSED_STATES`;
- `FORBIDDEN_SELECTOR_TOKENS`;
- `EmpiricalFact.REQUIRED_FIELDS`;
- `rawlsing_next/m1_temporal_v554_admission_dedup.py`;
- any V553/V554 historical module.

## Named residuals that implementation does not silently solve

- `IDENTITY_CONTRACT_INSTANCE_MISSING`
- `TIME_INDEXED_OBSERVATION_OBJECT_ABSENT`
- `TIME_REFS_CURRENTLY_EXACT_AND_GRAIN_UNVALIDATED`
- `RUPTURE_CANDIDATE_PRODUCER_AND_CALIBRATION_AUTHORITY_UNCONSTITUTED`
- `TEMPORAL_GAP_OBJECT_ABSENT__TYPED_SPAN_STATE_SUBSTITUTE`
- `FAMILY_SCOPED_TIME_MAPPING_MATERIAL_UNADOPTED`

These remain explicit bounded dependencies or refusals. None licenses architecture widening.
