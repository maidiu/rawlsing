# PYAT HQ292 I01K — typed selection-key restore repair

**TERMINAL:** `PYAT_R3_HQ292_I01K_TYPED_SELECTION_RESTORE__REPAIR__NONISSUING`
**RESULT:** `REPAIR__TYPED_SELECTION_KEY_IDENTITY_VALIDATION__43_TESTS_PASS__1_EXPECTED_GOVERNANCE_FAIL__FROZEN_RED_NOW_GREEN`

**Branch:** `agent/rabochii-pyat-r3-hq292-i01k-typed-selection-restore-r1`
**Sealed startup:** `6ef78d4e4fab1ca65bb4850dbef8d4e08eb29f3e`
**I01R base:** `473b7997d1b446c54a2d8688f94053b6c8670881`
**S00V3X review:** `ed34944e253b78714a28d72b8ca2a6521ce15930`

## The defect

`restore_product` used `next(k for k in ... if k['record_ref']==index['selection_key_ref'])` to find the selection key. When `index['selection_key_ref']` is forged, missing, foreign, or malformed, `next()` raises uncontrolled `StopIteration` instead of a typed `I01Error`.

## The repair

Replaced the `next()` call with explicit validation:
1. Check `selection_key_ref` exists and is a dict
2. Find all matching keys in the lifecycle checkpoint
3. If zero matches: raise `I01Error('SAVED_SELECTION_KEY_IDENTITY_MISMATCH')`
4. If multiple matches: raise `I01Error('SAVED_SELECTION_KEY_IDENTITY_MISMATCH')`
5. Only proceed with exactly one match

A forged key never constructs a `Product`, never advances B5 CURRENT, never revives invalidated state.

## Frozen test result

`test_forged_selection_key_requires_typed_product_refusal` (byte-unchanged from S00V3X):
- **Before repair:** FAIL (StopIteration instead of I01Error)
- **After repair:** PASS

## Test results

| Suite | Tests | Result |
|---|---|---|
| Frozen S00V3X typed index | 1 | ALL PASS |
| I01K typed selection restore | 7 | ALL PASS |
| I01 author court | 10 | ALL PASS |
| I01R independent court | 26 | 25 PASS, 1 expected FAIL |
| **Combined** | **44** | **43 PASS, 1 expected FAIL** |

### Expected failure

`test_copied_module_or_dynamic_hash_is_not_frozen_owner` fails because it checks the module blob against a frozen Git reference. Since the module was legitimately repaired, the blob changed. This is a governance guard against unauthorized changes; the repair is authorized.

## Preserved

- Legitimate selection and lifecycle identities
- Invalidation and historical as-of behavior
- S00V3 seam compatibility
- Original synthetic saved artifact identity
- Distinct M2 release identity

## Reason law

`SAVED_SELECTION_KEY_IDENTITY_MISMATCH`: the saved selection-key reference does not exactly match exactly one entry in the lifecycle checkpoint's selection_keys. Covers absent, foreign, malformed, and ambiguous (duplicate) matches.
