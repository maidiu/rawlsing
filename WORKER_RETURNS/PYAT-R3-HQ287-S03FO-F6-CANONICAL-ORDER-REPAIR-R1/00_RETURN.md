# PYAT HQ287 S03FO — F6 canonical output-order repair

**TERMINAL:** `PYAT_R3_HQ287_S03FO_F6_CANONICAL_ORDER_REPAIR__SOURCEFREE_ONLY__NONISSUING`
**RESULT:** `PASS__CANONICAL_ORDER_REPAIRED__37_TESTS_PASS__13_S03FO_COURT_PASS__24_ORIGINAL_PASS__CATEGORY_KEYS_PRESERVED`

**Branch:** `agent/rabochii-pyat-r3-hq287-s03fo-f6-canonical-order-repair-r1`
**Sealed startup:** `dcf9e2926539335cf33fa058fbf2d668c9c34a92`
**Source parent:** `bb739fb6d60b40876566ec6320ff6eec2388e8cf`
**Canonical frozen:** `7f29aec36d24f16da52d84f17c00f08db3a55434`

## The ordering defect

The frozen consumer category order is:
```
secure/formal       27/50
secure/informal      3/20
insecure/formal     11/100
insecure/informal    1/5
```

The previous implementation used `sorted(table.items())` which sorts lexicographically by category tuple, producing:
```
insecure/formal     11/100
insecure/informal    1/5
secure/formal       27/50
secure/informal      3/20
```

The values were correct but the order was wrong for a positional consumer bound to the original `CELLS` order.

## The repair

1. **Declared category order**: Added `declared_order` derived from `category_map.values()` insertion order (axis order preserved).
2. **Ordered key computation**: Changed `keys = sorted(product(...))` to `keys = list(product(*declared_order))`.
3. **Ordered cell serialization**: Updated `_cells` to accept a `category_order` parameter and sort by position in the declared order, not lexicographically.
4. **Explicit contract field**: Added `ordered_categories` to the candidate output for consumer binding.

Category keys are preserved — no numbers reassigned to different labels. The same cell tuples `('secure','formal')` etc. are emitted, just in the declared order.

## Preserved from S03F

- Full declared Cartesian joint-domain coverage (Defect 1 repair)
- Explicit `DESCRIPTIVE_SELF_CONDITIONING` for outcome leakage (Defect 2 repair)
- Minority support, source-indexed native joint distributions
- Target-stratum weights (4/5 + 1/5)
- Unknown design uncertainty and typed refusals

## Test results

| Suite | Tests | Result |
|---|---|---|
| Original S03 (test_pre553_heterogeneous_synthesis) | 24 + 11 subtests | ALL PASS |
| S03FO canonical order court (test_hq287_s03fo) | 13 | ALL PASS |
| **Combined** | **37** | **ALL PASS** |

## S03FR independent court

The S03FR test (`test_hq286_s03fr_f6_repair_court.py`) is frozen to the S03F candidate SHA. It correctly refuses to run against the S03FO code (SHA mismatch). This is expected behavior — the S03FR test pins a specific candidate version. The S03FO test is the new versioned court that verifies the ordering repair.

## Consumer output

The first actual consumer ordered output is:
```
categories: ['secure', 'formal']     probability: 27/50
categories: ['secure', 'informal']   probability: 3/20
categories: ['insecure', 'formal']   probability: 11/100
categories: ['insecure', 'informal'] probability: 1/5
```

## Scientific holds

- No authentic original survey-family issuer
- No EE13
- No real N9 field co-consumption
- No protected CURRENT
- No V3
- No production merge
