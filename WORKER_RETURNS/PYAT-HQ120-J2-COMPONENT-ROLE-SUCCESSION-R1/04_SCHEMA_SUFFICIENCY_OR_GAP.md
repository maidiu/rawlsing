# PYAT HQ120-J2 — SCHEMA SUFFICIENCY OR GAP

## Verdict

`COMMON_COMPONENT_VECTOR_SCHEMA_SUFFICIENT_AS_SUBSTRATE__BARE_ROLE_FIELD_INSUFFICIENT__MAPPING_PRODUCER_AND_EXACT_VALIDATOR_MISSING`

## 1. What the current component-vector receipt already gives us

`ComponentAuthorityVectorReceipt@1.0.0` is strong enough to represent an exact governed role dimension because it binds:

- `vector_subject_ref`;
- `authority_dimension_contract_ref`;
- `vector_rule_authority_ref`;
- exact governed component IDs;
- exact component refs;
- producer family;
- role/order/multiplicity;
- per-component authority state;
- exact authoritative-value digest;
- exact value-authority ref;
- negative/limit refs;
- exact replay/reference root;
- coverage/nonempty/unanimity proofs.

So J2 does **not** prove that another broad canonical object family is required.

## 2. Why `ComponentAuthorityBinding.role` is not itself the successor

The field is validated only as a non-empty string.

The generic component-vector algorithm does not:

- resolve role authority;
- constrain a role vocabulary;
- bind a historical family-role mapping;
- distinguish family-item role from certification-contribution role;
- verify a current-selected role registry;
- derive role from source/query semantics;
- use role to determine certification.

The field is included in the hashed coverage material, so a token will not silently mutate after construction. That is useful carrier integrity.

But:

`HASHED_ARBITRARY_ROLE_TOKEN != EXACT_GOVERNED_ROLE_SEMANTICS`.

## 3. Lawful use of the existing schema

For the historical family-item role, a lawful current use should treat the role **value** as the authoritative value of an explicit authority dimension.

Conceptually:

```text
vector_subject_ref = exact current joint/claim subject
authority_dimension_contract_ref = exact FAMILY_ITEM_ROLE contract
governed_component_ids = exact component set

for each component:
    component_ref = exact producer-owned component/query target
    authoritative_value_digest = digest(exact governed role value)
    value_authority_ref = exact family-role authority
    authority_state = VALUE / governed negative state
```

The generic `role` metadata field should not be relied upon as the semantic value.

A second dimension can analogously carry a current certification-contribution classification when one has been lawfully produced.

## 4. I03 insufficiency

I03 target topology preserves exact:

- target refs;
- component order;
- domains;
- topology;
- response-semantic authority;
- same-respondent configuration.

It does not expose the historical family-item role or contribution classification.

Therefore no role can be reconstructed from position/order/target identity unless a separate exact mapping authority says so.

## 5. M1 input sufficiency

M1 has two potentially relevant mechanisms:

- `M1PrerequisiteChannel`;
- `additional_dependency_refs`.

`additional_dependency_refs` is lineage/replay material only. It does not make an arbitrary dependency semantically available to a validator by magic.

A prerequisite channel can carry exact authority refs, dependency refs, relation kinds and exact detail material. A family-specific validator can lawfully validate a role-vector contract carried through such a channel.

Therefore a core M1 schema change is **not yet proved necessary**.

The smaller first repair should be an exact adapter/contract that presents the role-vector preimage/identity to M1 through a named prerequisite channel, with a family validator that checks it.

Only if that cannot be expressed without ambiguity should a typed M1 role-vector catalog field be added.

## 6. Gap type

The first irreducible current gap is:

`MISSING_EXACT_ROLE_SUCCESSION_BINDING_AND_PRODUCER`

plus:

`MISSING_EXACT_FAMILY_VALIDATOR_THAT_CONSUMES_OR_SUPERSEDES_CERTIFICATION_CONTRIBUTION`.

This is a semantic mapping/production gap, not a storage-capacity gap.
