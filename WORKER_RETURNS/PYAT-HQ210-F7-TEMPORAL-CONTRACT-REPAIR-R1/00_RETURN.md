# PYAT HQ210 — F7 temporal comparability contract bounded repair — R1

**Disposition:** `F7_TEMPORAL_CONTRACT_REPAIR_COMPLETE__READY_FOR_HQ_FINAL_ACCEPTANCE`

**Terminal:** `HQ210_F7_TEMPORAL_CONTRACT_REPAIR_RETURNED__HQ_FINAL_DECISION_REQUIRED`

## Exact frame

- Branch: `agent/rabochii-pyat-hq210-f7-contract-repair-r1`
- Commission tip: `7a6ecae8002088630c5ffb2eea286efda1b3316b`
- Startup base: `7cc1ce20238e06e4b785b6a804cc885cd19d641a`
- Contract repaired: `19fd6f6e9f3e24c716310335325cef4c75e6fa56`
- Hostile review: `f1a0dbbc8491e0d23df9005abd55b83e0261424e`
- Primary F7 forensic return: `ac444c5a345cded633a8e5b30ccd8b718f903d55`

This is a corrected documentary successor packet. Historical return files are untouched. No production implementation is performed or authorized by this lane.

## Preserved architecture

The hostile review's sustained findings remain binding:

- exactly one new authority kind, `TEMPORAL_COMPARABILITY`, is minimal;
- the seven reuse targets remain existing authority kinds;
- identity, observation, positive relation/comparison, rupture, and gap/absence remain non-collapsed;
- `TEMPORAL_NONCOMPARABLE != EMPIRICAL_FACT_NONCOMPARABLE`;
- time grain remains operation/rule-bound, polymorphic, exact-ref based and fail-closed;
- two exact authorized anchors may suffice for one ordered relation;
- no >=3-anchor trajectory rule;
- no direction from mere difference;
- no temporal coincidence -> cause;
- no V553 scalar temporal-pressure resurrection.

## Seven repairs closed

### 1. Order-basis/refusal coherence

`ORDER_UNKNOWN_NONCOMPARABLE` is no longer an authorized order basis. It is a **typed order-disposition refusal class**.

Authorized order bases are exactly:

1. `CALENDAR_TOTAL_ORDER`
2. `FAMILY_LOCAL_ORDINAL`
3. `PARTIAL_ORDER_NO_DIRECTION`

The fourth mandated distinction remains represented as:

4. `ORDER_UNKNOWN_NONCOMPARABLE` — **NO AUTHORIZED BASIS EXISTS**

For that fourth class, `temporal_order_basis_ref` MUST be absent.

`TEMPORAL_ORDER_UNAUTHORIZED` now has exactly one production path:

`order_disposition == ORDER_UNKNOWN_NONCOMPARABLE -> TEMPORAL_ORDER_UNAUTHORIZED / NO_PERMITTED_ORDER_BASIS_APPLIES`.

If an otherwise-required authority/basis ref is missing or its snapshot fails, the result is instead `TEMPORAL_INSUFFICIENT_AUTHORITY`, never a second path to `TEMPORAL_ORDER_UNAUTHORIZED`.

### 2. Cross-field invariants

`TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED` is lawful iff ALL hold:

- `comparability_status == COMPARABLE`;
- `relation_status == ORDERED_RELATION_AUTHORIZED`;
- an authorized `temporal_order_basis_ref` is present;
- its basis is `CALENDAR_TOTAL_ORDER` or `FAMILY_LOCAL_ORDINAL` and therefore `permits_direction == true`;
- `direction_claim` is exactly one of `INCREASE | DECREASE | NO_AUTHORIZED_CHANGE`;
- `delta` is present and `non_delta_presence == DELTA_PRESENT`;
- all required authority snapshots resolve positively and all required comparability surfaces pass.

Contradictory tuples are contract-invalid and MUST refuse rather than normalize.

A partial authorized basis requires `ORDER_RELATION_REFUSED` plus `DIRECTION_NOT_CLAIMABLE`.
No state may combine directional authorization with `DIRECTION_NOT_CLAIMABLE`.

### 3. NO_AUTHORIZED_CHANGE

No deadband is part of this contract.

`NO_AUTHORIZED_CHANGE` means **exact signed delta = 0 under the authorized difference operation**.

No epsilon, tolerance, inherited V553 +/-0.05 threshold, confidence rule, or unbound deadband may be used. A non-zero exact signed delta must yield `INCREASE` or `DECREASE`.

Any future deadband/tolerance semantics require a separately adopted authority contract and are outside this repaired contract.

### 4. Deterministic relation-state derivation

A total precedence law now determines exactly one `relation_state` from identical inputs. All observed failures remain in `comparability_requirement_results`; precedence chooses the public terminal state without erasing lower-priority defects.

Precedence, highest first:

1. `TEMPORAL_INSUFFICIENT_AUTHORITY`
2. `TEMPORAL_IDENTITY_UNRESOLVED`
3. `TEMPORAL_INSUFFICIENT_ANCHORS`
4. `TEMPORAL_CROSS_UNIVERSE_EQUIVALENCE_ABSENT`
5. `TEMPORAL_MAPPING_MATERIAL_ABSENT`
6. `TEMPORAL_ESTIMAND_MISMATCH`
7. `TEMPORAL_MEASURE_MISMATCH`
8. `TEMPORAL_NONCOMPARABLE`
9. `TEMPORAL_ORDER_UNAUTHORIZED`
10. `TEMPORAL_INTERVAL_OVERLAP_NO_DIRECTION`
11. `TEMPORAL_COMPARABLE_NO_DIRECTION`
12. `TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED`

`relation_state_reason` is one scalar enum, always required, selected by a state-local reason precedence. The positive state now has reason `AUTHORIZED_ORDERED_PAIR_UNDER_BOUND_COMPARABILITY`.

Existing fail-closed `AUTHORITY_STATE` values do not leak into the temporal state family: `AUTHORITY_HASH_MISMATCH` and `AUTHORITY_SCOPE_MISMATCH` map to `TEMPORAL_INSUFFICIENT_AUTHORITY` while their original authority-resolution state remains in provenance.

Prior F7 candidate terminals are explicitly resolved:
- `TEMPORAL_AUTHORITY_MISSING` -> `TEMPORAL_INSUFFICIENT_AUTHORITY`
- `TEMPORAL_AUTHORITY_CONFLICT` -> `TEMPORAL_INSUFFICIENT_AUTHORITY`
- `TEMPORAL_OUT_OF_SCOPE` -> `TEMPORAL_INSUFFICIENT_AUTHORITY`
- `TEMPORAL_INTERPOLATION_NOT_AUTHORIZED` -> `TEMPORAL_NONCOMPARABLE`
- `TEMPORAL_PROBE_ONLY` -> **NO TEMPORAL_RELATION_RECEIPT MAY BE EMITTED**
- `TEMPORAL_RESPONSE_SURFACE_MISMATCH` -> `TEMPORAL_NONCOMPARABLE`

### 5. Implementation ceiling

A later implementation commission may add only:

- `TEMPORAL_COMPARABILITY` to `AUTHORITY_KINDS`;
- one matching `AUTHORITY_KIND_CEILINGS` entry;
- a bounded comparison module implementing the repaired receipt/state/order laws;
- exact-authority resolution through the existing authority discipline;
- the existing source-relation resolution path for cross-universe `SOURCE_EQUIVALENCE`.

This contract chooses **not** to make `TEMPORAL_RELATION_RECEIPT` a `PUBLIC_OBJECT_FAMILIES` member. It is a closed content-addressed receipt local to the temporal comparison module. `relation_state` is therefore a receipt-local validated field, **not** `CanonicalSemanticObject.typed_state`; no `STATE_FAMILIES` edit is authorized.

No downstream F8 consumption is authorized.

### 6. Documentary corrections

- `TEMPORAL_RELATION_STATE` has **12** members, not 11.
- F7's gap/absence historical record is **H10**, not H08. H08 is scalar temporal pressure and remains obsolete.
- Conserved-function numbering now carries both systems:
  - commission conserved-five indices: identity 1, observation 2, delta 3, rupture 4, gap 5;
  - F7 succession-map indices: identity 0, observation 1, positive relation 2, delta 3, trajectory 4, rupture 5, gap 6, temporal directionality 7.
- Source-side `EMPIRICAL_FACT_NONCOMPARABLE` producer evidence includes all three producer sites:
  - `:639-640` `EMPIRICAL_FACT_NONCOMPARABLE`
  - `:680-681` `ESTIMAND_NOT_ALLOWED_BY_RULE`
  - `:686-687` `MEASURE_WEIGHT_BASIS_NOT_ALLOWED_BY_RULE`

### 7. Noncollapse/backfill direction

The literal `TEMPORAL_NONCOMPARABLE` MUST remain in
`FORBIDDEN_BACKFILL_TARGET_STATES`.

Additionally:

- a `TEMPORAL_RELATION_RECEIPT` is never itself a source-backfill target;
- a pair whose `relation_state == TEMPORAL_NONCOMPARABLE` may never be backfilled into a positive temporal state;
- source backfill authority cannot manufacture temporal comparability;
- no interpolation, midpoint, nearest-anchor, default-time or cross-source backfill may erase the refusal.

## Outcome

All seven hostile-review defects are closed at documentary contract grain without adding another authority kind, adding production state, reinstating a universal time algebra, or authorizing implementation.

No material authority conflict was found.

`HQ210_F7_TEMPORAL_CONTRACT_REPAIR_RETURNED__HQ_FINAL_DECISION_REQUIRED`
