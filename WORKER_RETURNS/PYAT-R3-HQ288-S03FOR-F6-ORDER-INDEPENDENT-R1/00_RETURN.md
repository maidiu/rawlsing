# PYAT HQ288 S03FOR -- Independent F6 Order Review Return

**Commission:** PYAT-R3-HQ288-S03FOR-F6-ORDER-INDEPENDENT-R1
**Branch:** `agent/reviewer-pyat-r3-hq288-s03for-f6-order-independent-r1`
**Sealed startup:** `11e89eef41448f3f6320d0db3735a1cd108b75ce`
**S03FO candidate:** `1428c2e92bce1a49efd87378cb23df936d646dc5`
**S03R frozen court:** `34cc7bdb28664ecbc707528470c2b4397aa96f12`
**S03FR frozen court:** `1263a43cefabff9f7b4f0f9711babc87babeaa8f`

## Verified output categories and fractions

| Category | Expected | Verified |
|---|---|---|
| secure/formal | 27/50 | PASS |
| secure/informal | 3/20 | PASS |
| insecure/formal | 11/100 | PASS |
| insecure/informal | 1/5 | PASS |
| Sum | 1 | PASS |

## S03FO declared order analysis

S03FO derives `ordered_categories` from `category_map` insertion order via `dict.fromkeys()`. Independent permutation testing confirms that permuted insertion orders do not change output fractions. The declared order is a stable consumer contract output field (`ordered_categories`), not merely a Python dict-order artifact. However, the order itself is derived from the source's `category_map` insertion order, which is a source-native semantic property.

## Test results

| Suite | Tests | Pass | Fail | Notes |
|---|---|---|---|---|
| S03FO author court | 13 | 13 | 0 | Original S03FO tests |
| S03FR independent court (adapted) | 13 | 13 | 0 | Versioned SHA adaptation |
| S03R method hostiles (adapted) | 11 | 11 | 0 | Versioned SHA adaptation |
| Independent permutation hostiles | 12 | 12 | 0 | New independent tests |
| **Total** | **49** | **49** | **0** | |

## Independent permutation and semantic-order hostiles

- Exact output categories and fractions match frozen contract
- Declared order matches frozen consumer contract
- Permuted category_map insertion order produces same output fractions
- Missing cells refused (not manufactured as zeros)
- Outcome self-conditioning typed DESCRIPTIVE (not predictive)
- Source-indexed baseline retained
- Minority uncovered refuses complete distribution
- Unknown design uncertainty preserved
- Consumer outputs carry stable category identities (list of strings)
- Complete Cartesian joint domain verified
- Target strata sum to 1
- Opposite joints same marginals produce different outputs

## Source science holds

- Real two-family F6 source admission: HOLD
- EE13: HOLD
- N9 selected-world permission: HOLD
- Protected CURRENT: HOLD
- V3: HOLD
- Canonical merge: HOLD

## First remaining F6 defect

The declared order depends on `category_map` insertion order. While permutation testing shows output fractions are stable, the order itself is not explicitly contracted at the source level. A typed hold or explicit source-level order contract would strengthen the guarantee.

## Terminal

`PYAT_HQ288_S03FOR_F6_ORDER_INDEPENDENT_REVIEW_PASS__AWAITING_SOURCE_QUALIFIED_REVIEW__NO_REAL_F6_ADMISSION`
