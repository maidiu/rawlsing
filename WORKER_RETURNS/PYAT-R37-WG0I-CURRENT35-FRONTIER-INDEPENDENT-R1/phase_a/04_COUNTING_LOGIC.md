# WG0I Phase A — independent counting logic

All counts are recomputed from the pinned accepted authority, never copied from
WG0R output.

## Source and item census

- 35 sources: `atlas_id` SRC01..SRC35, exactly once.
- 18,259 active O35E items = sum of per-wave `items`; each wave's item count must
  equal its `qra_row_count` and the sum of its `qra_status_counts`.
- 259 excluded Asian W6 rows + 18,259 active = 18,518 all rows.
- The 18,276 governed implementation spine and 18,259 O35E active rows are
  different units; the 17-row difference must be typed by exact crosswalk, not
  dropped. The QSR 18,792 and 18,413 historical columns are also different units.

## Status census (exact)

| Status | Count |
|---|---:|
| GOVERNED_ADMINISTRATIVE_DISPOSITION | 966 |
| GOVERNED_NON_DIRECTIONAL_DISPOSITION | 12,611 |
| GOVERNED_QSMV2_RELATION_AUTHORITY | 4,397 |
| GOVERNED_MANUAL_RELATION_AUTHORITY | 173 |
| BLOCKED_IDENTITY_OR_AUTHORITY_JOIN | 9 |
| BLOCKED_STRUCTURAL_MAPPING_AUTHORITY | 41 |
| FROZEN_ACCEPTED_GSS | 52 |
| BLOCKED_SOURCE_AUTHORITY | 10 |
| **Total** | **18,259** |

## Primary disposition (item grain, partition)

- `SOURCE_INTRINSIC_NONAPPLICABLE` = 966 administrative + 12,611 non-directional = **13,577**
  (at the directed measurement-relation grain; marginal/structural operations remain HOLD).
- `AUTHORITY_HELD` = 4,397 QSMV2 + 173 manual relation + 9 identity-blocked + 41
  structural-blocked + 10 source-blocked = **4,630**.
- `EXECUTED_WITH_CONSUMER` = **52** frozen GSS accepted relations (historical grain).
- `PERMITTED` = **0**.
- `UNDECIDED` = **0** at item primary status; all 18,259 items have incomplete
  option/carrier/route/risk binding, recorded on the binding axis, not as a sixth
  primary class.
- `PRODUCER_PENDING` = **18,259** on the current-frontier axis: all 35 sources have
  null item-inventory, authorized-frontier, expected-products-manifest and
  final-consumer refs.

## Operation census

- 7 operation classes: I03_RAW_MARGINAL, I03_GOVERNED_WEIGHTED,
  I03_DIRECTED_CONDITIONAL, I05_EXACT_BOUNDED_DISCOVERY, I04_STRUCTURAL_ADMISSION,
  BATCH_EXPECTED_WORK, OC01_SOURCE_LOCAL_CONSUMER.
- 18,259 items × 7 classes = **127,813 potential operation rows**.
- Every row inherits `HOLD_UNISSUED_ORIGINAL_SOURCE_ITEM_OP_BINDING`; `PERMITTED = 0`,
  `EXECUTED_WITH_CONSUMER_CURRENT = 0`.

## Estate, tasks and queue

- 35 sources × 54 axes = **1,890 cells**: 1,050 source-native + 560 EE + 280 F1–F8.
  Status: 1,050 `EXACT_SCOPED_RECONCILIATION_REQUIRED__NOT_ASSERTED_MISSING`,
  560 `GENERAL_OWNER_OR_ARCHITECTURE_PRESENT_AT_BASELINE__THIS_WAVE_OPERATION_OCCUPANCY_UNVERIFIED`,
  280 `NOT_CERTIFIED_AT_THIS_EXACT_SCOPE`.
- **101** task rows, all `OPEN_EVIDENCE_BINDING__NOT_A_DEFECT_VERDICT`; the shared
  critical gate status is `NOT_PROVED_AT_COMPLETE_CLOSED35_ORIGINAL_ITEM_OPERATION_GRAIN`.
- 35 queue sources × 5 current refs = **175 null refs** (item inventory, authorized
  frontier, expected-products manifest, final consumer, source-intrinsic
  nonapplicability). All 35 `source_use_status` are
  `HOLD_NO_VERIFIED_CURRENT_SIGNED_ORIGINAL_RIGHT`; permission/U/E_pre refs are null,
  eligible counts null, native runs zero, sample/risk/design editions UNBOUND.

## Accepted historical positives (not current all35)

- LiTS-I AS2B: 29,002 respondents, 58,004 events, 58,004 routing facts, 145,010
  coordinate facts, 0 weight facts; 8 I03 executed / 8 passed; 8/8 hostile; exact
  projection/release/repository/manifest hashes at commit `923f2c00…`.
- GSS frozen accepted: 52.
- O35E test-only: 18,259 items, original run `NOT_EXECUTED__SOURCE_AND_ISSUER_HOLD`,
  0 new original products, 0 new U/E_pre.

## Six-label distinction

The labels are not a single partition across all grains. `PERMITTED` is zero;
`AUTHORITY_HELD` and `SOURCE_INTRINSIC_NONAPPLICABLE` are the item-primary
partition with `EXECUTED_WITH_CONSUMER`; `PRODUCER_PENDING` is the separate
current-frontier axis applying to all 18,259 items; `UNDECIDED` is zero at item
primary status but all items carry binding incompleteness. Any claim that a
current operation is PERMITTED or EXECUTED must supply the exact competent
original U + E_pre + current source-use permission + operation requirement.
