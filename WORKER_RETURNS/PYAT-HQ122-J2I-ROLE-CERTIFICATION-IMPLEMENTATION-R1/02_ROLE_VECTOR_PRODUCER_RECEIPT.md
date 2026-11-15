# HQ122 J2I — ROLE VECTOR PRODUCER RECEIPT

Implemented owner:

`rawlsing_next/pre553_j_role_certification.py`

Producer entrypoint:

`build_j_family_item_role_vector(...)`

Contract:

`PRE553_J_FAMILY_ITEM_ROLE_SUCCESSION@1.0.0`

Carrier:

`ComponentAuthorityVectorReceipt@1.0.0`

Authority dimension:

`J_FAMILY_ITEM_ROLE`

## Conserved positive vocabulary

Exactly:

```text
exception_case
elective_case
social_condition
family_size_condition
economic_condition
target_case
```

No synonyms and no lexical/ordinal/name/proximity inference are implemented.

`ComponentAuthorityBinding.role` is fixed to nonsemantic metadata:

`FAMILY_ITEM_ROLE_MEMBER`

The semantic role value is represented only by:

`authoritative_value_digest(exact_role_token)`

plus exact `value_authority_ref`.

## Typed-state law

The adapter admits only:

- `VALUE`
- `UNRESOLVED`
- `DENIED`
- `NONCOMPARABLE`

A positive VALUE assignment that invokes historical/current succession but lacks an exact predecessor/current mapping ref is downgraded to `UNRESOLVED`; it is never converted to `target_case`.

DENIED/NONCOMPARABLE require exact negative/limit refs through the generic component-authority binding contract.

The producer requires exactly one assignment per governed component and exact ordinal equality with the explicit governed component order.

## Replay

The producer derives one exact role-vector replay root from:

- subject ref;
- ordered governed component IDs;
- role contract ref;
- mapping contract ref;
- adopted role authority ref;
- effective per-component typed role assignments;
- predecessor/current mapping refs;
- dependency/negative refs;
- replay-contract ref.

Generic component-vector reload is deterministic and exact in hostile qualification.
