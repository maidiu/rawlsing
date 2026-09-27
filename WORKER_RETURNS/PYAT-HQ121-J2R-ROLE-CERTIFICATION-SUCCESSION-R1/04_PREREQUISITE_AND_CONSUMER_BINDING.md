# J2R — M1 PREREQUISITE AND CONSUMER BINDING

Status:

`CURRENT_M1_SCHEMA_SUFFICIENT__NAMED_PREREQUISITE_CHANNEL_REQUIRED__NO_CORE_SCHEMA_WIDENING`

## 1. Exact consumer

The exact current semantic consumer is the M1 family validator bound to:

- claim family: `PRE553_J_JOINT_RELATION_EVIDENCE`;
- claim rule: `PRE553_J_COMPONENT_CERTIFICATION_CONTRIBUTION_RULE@1.0.0`;
- validator algorithm identity: `PRE553_J_COMPONENT_CERTIFICATION_CONTRIBUTION_VALIDATOR@1.0.0`.

The generic runtime is:

`rawlsing_next/pre553_learned_empirical_adjudication.py`

blob:

`ed70099f431645d371065ffeec03f3da3d00a666`.

The validator registration must be exact; current `M1ValidatorRegistry` permits no latest/default/fuzzy fallback.

## 2. Named prerequisite channel

Required channel ID:

`j_family_item_role_vector`

Required channel kind:

`PRE553_J_FAMILY_ITEM_ROLE_VECTOR`

Required semantic relation kinds:

- `GOVERNED_FAMILY_ITEM_ROLE_FOR_COMPONENT_SET`;
- `ROLE_VECTOR_PREMISE_FOR_J_CERTIFICATION`.

Required `dependency_refs`:

1. exact `ComponentAuthorityVectorReceipt@1.0.0` ref for `J_FAMILY_ITEM_ROLE`;
2. exact role-dimension contract ref;
3. exact predecessor/current component mapping ref(s), where succession is used;
4. exact replay root/ref required to reconstruct the role vector.

Required `authority_refs`:

1. exact adopted `PRE553_J_FAMILY_ITEM_ROLE_AUTHORITY@1.0.0` ref;
2. exact current subject/family authority required by the selected current-use binding;
3. any exact per-value authority refs required by the vector contract.

Required exact `detail` material:

```text
contract_id = PRE553_J_FAMILY_ITEM_ROLE_SUCCESSION@1.0.0
authority_dimension = J_FAMILY_ITEM_ROLE
vector_subject_ref = exact current joint subject ref
role_vector_ref = exact ComponentAuthorityVectorReceipt ref
governed_component_ids = exact ordered current component IDs
role_vocabulary_version = PRE553_J_FAMILY_ITEM_ROLE_SUCCESSION@1.0.0
mapping_mode = EXACT_IDENTITY_SIX_TOKEN_VOCABULARY_WITH_TYPED_NEGATIVE_UNRESOLVED
current_joint_contract = CURRENT_JOINT_AUTHORITY_CONTRACT@1
semantic_ceiling = J_FAMILY_ITEM_ROLE_PREMISE_ONLY
```

## 3. Channel state law

Channel `SATISFIED` requires:

- exact required authority refs;
- exact role-vector contract/version;
- exact subject ref;
- exact governed component set;
- complete one-to-one component coverage;
- every required role binding in `VALUE`;
- every VALUE digest resolves to one allowed six-token role;
- exact mapping/replay closure.

Channel is `UNRESOLVED` when any required component role is missing/unknown/unresolved or the required positive mapping has not been proved, provided no stronger conflict/denial is present.

Channel is `BLOCKED` or the exact stronger typed state when:
- authority is denied/noncomparable/conflicting;
- component set conflicts;
- authority ref is not the exact binding-selected ref;
- an ambiguous duplicate role binding exists;
- replay/preimage does not reproduce;
- an unknown token is serialized as a purported positive VALUE.

The family validator may preserve the stronger prerequisite state but must never reinterpret it as SATISFIED.

## 4. Why additional_dependency_refs are insufficient

`additional_dependency_refs` lawfully preserve exact reachability/lineage and are valuable for I4 conservation.

They do not:
- identify the semantic dimension;
- validate role vocabulary;
- validate value authority;
- validate component coverage;
- dereference/interpret the role vector for a family rule.

Therefore the role-vector ref should also appear in dependency/replay closure, but semantic consumption is through the named prerequisite channel.

## 5. Why no M1 schema field is required

`M1PrerequisiteChannel` already carries:

- exact channel identity/kind;
- typed state;
- exact authority refs;
- exact dependency refs;
- exact relation kinds;
- exact structured detail.

`M1FamilyRuleBinding` already names required prerequisite channels and exact validator authority/parameters/replay/output ceiling.

`FamilyValidationResult` already carries exact determinant and explanation material.

Therefore:

`M1_SCHEMA_CHANGE = NOT_REQUIRED`.

A typed core role-vector field is forbidden unless a later implementation court demonstrates an ambiguity that the exact channel contract cannot represent.

## 6. Binding/currentness law

For `CURRENT_GOVERNED_USE`, the exact M1 family binding must use an exact `current_selection_authority_ref`.

It must not:
- select a role authority by chronology;
- use "latest", semver fallback, nearest, fuzzy, or default;
- accept a changed role authority under an old validator fingerprint;
- treat J01-B structure-level succession as per-component role authority.

If the role authority changes, the exact M1 binding/registration must be re-adopted or the request blocks.

## 7. Consumer proof and old field retirement

The M1 validator consumes the role vector to:
- prohibit relation promotion without exact role authority;
- preserve family semantic role as an exact determinant;
- derive the exact six-state contribution vector together with exact current evidence premises;
- enforce relation-count/context distinction.

This is an actual semantic consumer contract, not dormant provenance.

Because M1 consumes the contribution vector internally and freezes it in determinant/replay, the two old duplicate physical contribution fields need not be recreated.
