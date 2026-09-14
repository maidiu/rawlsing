# PRE-V3 empirical source-state to product-target-disposition contract r1

## Result

PASS. The reusable objective-world contract is implemented with the exact staged path:

`RAW_SOURCE_STATE -> SOURCE_LOCAL_GOVERNED_STATE -> PRODUCT_TARGET_DISPOSITION -> DENOMINATOR_RESOLUTION_CHECK -> EMPIRICAL_RESULT`

The helper retains the observed native state, requires an explicit source-local authority before a governed semantic state is accepted, and keeps product-target disposition separate from both. It never derives semantic meaning from a native numeric state.

## Gate behavior

The target disposition vocabulary is exactly:

- `NUMERATOR_AND_DENOMINATOR`
- `DENOMINATOR_ONLY`
- `EXCLUDED_FROM_TARGET_DENOMINATOR`
- `UNRESOLVED`

For a concrete target, any `UNRESOLVED` record fails `DENOMINATOR_RESOLUTION_CHECK`; result emission is rejected before numerator or denominator arithmetic. After a passing gate, only numerator-and-denominator plus denominator-only records enter the denominator. Excluded records remain auditable but are not counted in that denominator.

## Synthetic proofs

The fixture proves that two synthetic sources can carry the same raw numeric state while their explicitly governed source-local semantic states differ. A governed state can still remain unresolved at product disposition. A second resolved case proves the post-gate arithmetic and exclusion behavior.

The machine-readable checker also verifies the five-stage audit sequence, synthetic-only source identifiers, and absence of prohibited legacy vocabulary from all five new artifacts.

Run:

```text
python3 evidence/selftest/prev3_source_state_target_disposition_contract.py
python3 -m py_compile tools/prev3_source_state_target_disposition.py evidence/selftest/prev3_source_state_target_disposition_contract.py
```

## Bounds and successor gate

This return is source-agnostic and objective-world only. It introduces no concrete source semantics and performs no learned positive empirical execution. HQ must combine it with separately governed source-local semantic authority before any later positive execution lane may proceed.
