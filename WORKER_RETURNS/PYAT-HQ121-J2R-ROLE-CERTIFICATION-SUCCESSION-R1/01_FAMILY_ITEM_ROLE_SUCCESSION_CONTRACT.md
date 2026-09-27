# PRE553_J_FAMILY_ITEM_ROLE_SUCCESSION@1.0.0

Status:

`CONSTITUTED__READY_FOR_HQ_ADOPTION`

## 1. Contract identity and semantic grain

Contract:

`PRE553_J_FAMILY_ITEM_ROLE_SUCCESSION@1.0.0`

Authority dimension:

`J_FAMILY_ITEM_ROLE`

Current authority family to be materialized by the minimal implementation after HQ adoption:

- authority_id: `PRE553_J_FAMILY_ITEM_ROLE_AUTHORITY`
- authority_version: `1.0.0`
- authority content basis: this contract + `02_ROLE_VOCABULARY_AND_MAPPING.tsv` + the exact HQ adoption that admits them.

No positive `VALUE` role-vector binding may be emitted before an exact current `AuthorityRef` exists for that adopted authority content.

The semantic grain is:

`ONE EXACT CURRENT JOINT SUBJECT × ONE EXACT GOVERNED COMPONENT SET × ONE FAMILY-ITEM-ROLE DIMENSION`.

It is not:
- a generic participant-role vocabulary;
- a target topology;
- a response-direction vocabulary;
- a product lifecycle state;
- a Field Forge position role.

## 2. Exact subject and family identity

A role vector may exist only for an exact current joint subject admitted at the `CURRENT_JOINT_AUTHORITY_CONTRACT@1` grain and identified by exact current refs.

J01-B project-current adoption:

`805418167a57d95e7098105306aff1321a7d9560`

Exact J01-B global court:

`ed641eb74ead4dc5db1cada84af007577758b1e2`

Frozen J01-A authority:

`44e97e420d38b6a2b0c44034929b5994a352d8b6`

Frozen J01-A carrier SHA-256:

`b21a79947f19f4c520ea493480a38ef8b23cb6797444eeb913bc8575b6cafb64`

This contract must not mutate the 1,411-current-candidate denominator, family identity, or lawful J01-B ambiguity.

`CURRENT_JOINT_AUTHORITY_CONTRACT@1` supplies subject/family succession identity. It does **not** automatically supply a component role value.

## 3. Exact governed component set

The governed component set is the exact current I03/current-query component set for the subject, with exact component identity and order/topology.

Required invariants:

1. `governed_component_ids` are explicit, nonempty, unique, and equal to the exact current subject component set.
2. Every binding references one exact current component.
3. No historical component may be silently appended to make an old packet shape reappear.
4. No current component may be dropped because no historical role is known.
5. An extra, missing, duplicate/ambiguous, or reordered component set is a fail-closed prerequisite/integrity condition, not a cue to infer roles.
6. Historical/current component correspondence must be exact evidence. Structure-level J01-B succession alone does not prove component-level correspondence.

## 4. Historical role authority and predecessor evidence

The exact preserved predecessor evidence is:

- historical family registry:
  `data/ddm_build_copy/manifests/question_family_registry.yaml`
  at commission head blob `54eb6dd138b5e30305b0308fcdb8f078994b1c40`;
- historical V550J role consumption:
  `data/ddm_build_copy/ddm_v550j_joint_patterns.py`
  blob `644aab23675b26134040d1df5cc25538b613e163`;
- J2 forensic adjudication:
  `107e5fabc28b556ae852ad19643b02af40d43bee`.

The registry proves the exact governed family-item vocabulary and shows that the role selected response-role and target-resolution rules. V550J proves that `item_role_groups` were materialized into per-item `item_role` and consumed by family semantic resolution.

The registry is historical predecessor evidence, not by itself a current runtime authority load.

## 5. Exact role vocabulary

The current successor preserves the historical governed family-item role vocabulary exactly:

```text
exception_case
elective_case
social_condition
family_size_condition
economic_condition
target_case
```

No synonym expansion is authorized.

In particular:

- `outside_family` is a historical association/diagnostic token, not a governed family-item role in the exact `item_role_groups` authority and is outside this vocabulary.
- `support` and `oppose` are response-semantic roles, not family-item roles.
- V551 evidence roles are a distinct semantic input and are not collapsed into this dimension.

## 6. Historical -> current mapping law

For each of the six governed historical tokens, the current mapping is exact identity.

No smaller/larger replacement vocabulary is adopted.

A `VALUE` binding is lawful only when all are true:

1. exact current subject/family identity is admitted;
2. exact current component identity is known;
3. exact predecessor/current component relation is proved where succession is invoked;
4. exactly one governed historical role token applies;
5. the token is one of the six allowed values;
6. exact current family-role authority and exact mapping authority are present;
7. replay/dependency closure contains the predecessor/mapping evidence.

Otherwise the value must remain typed:

- no mapping / missing authority / unknown token -> `UNRESOLVED`;
- explicit authority denial -> `DENIED`;
- competent finding of noncomparability -> `NONCOMPARABLE`;
- an exact governed component with no role value cannot be promoted through `GOVERNED_EMPTY`; for this required semantic dimension it makes the M1 prerequisite unresolved.

The historical V550J fallback `... or "target_case"` is expressly **not** current mapping authority. It may not convert missing role authority into `target_case`.

## 7. Exact carrier law

Carrier/proof substrate:

`ComponentAuthorityVectorReceipt@1.0.0`

Current implementation blob inspected:

`rawlsing_next/pre553_component_authority_vector.py@7c5993540e3dcfde5110f882fd1e26a298f47ac6`.

Required use:

```text
vector_subject_ref
  = exact current joint subject ref

authority_dimension_contract_ref
  = exact ref of PRE553_J_FAMILY_ITEM_ROLE_SUCCESSION@1.0.0

vector_rule_authority_ref
  = exact adopted PRE553_J_FAMILY_ITEM_ROLE_AUTHORITY ref

governed_component_ids
  = exact current governed component IDs

for each component:
  component_ref
    = exact current component ref

  ComponentAuthorityBinding.role
    = stable nonsemantic participant descriptor, e.g. FAMILY_ITEM_ROLE_MEMBER
      (MUST NOT be interpreted as the governed role value)

  authority_state
    = VALUE | UNRESOLVED | DENIED | NONCOMPARABLE
      (GOVERNED_EMPTY cannot satisfy this required role premise)

  authoritative_value_digest
    = authoritative_value_digest(exact six-token role value)
      only when authority_state == VALUE

  value_authority_ref
    = exact current role authority ref

  negative_or_limit_refs
    = exact denial/noncomparability/mapping-limit evidence where required
```

The receipt's exact coverage, ambiguity, unresolved, negative, proof-hash, and replay machinery are adopted as the carrier integrity substrate.

## 8. Exact replay/dependency/determinant closure

A role-vector receipt used by M1 must bind or carry exact refs sufficient to reconstruct:

- current joint subject identity;
- current family identity;
- exact current component refs/order;
- `CURRENT_JOINT_AUTHORITY_CONTRACT@1` authority/adoption;
- exact historical predecessor role authority where succession is invoked;
- exact historical->current component mapping evidence;
- this role contract/version;
- current role authority;
- value authority per component;
- all negative/noncomparability refs;
- producer replay root.

The M1 determinant must include the exact role-vector ref and exact component ordered digest/set identity. `additional_dependency_refs` may conserve these refs, but semantic consumption occurs through the named prerequisite channel defined in `04_PREREQUISITE_AND_CONSUMER_BINDING.md`.

## 9. Exact consumer

The current successor consumer is:

`PRE553_J_COMPONENT_CERTIFICATION_CONTRIBUTION_RULE@1.0.0`

implemented as an exact M1 family validator registration.

The validator must validate the role-vector authority and vocabulary; it may not merely check that a dependency ref exists.

Current target/response semantics remain owned by their exact current authorities. This role successor does not re-run V550J target/response inference.

## 10. Semantic ceiling

This contract establishes only the governed family-item role dimension and its exact succession/negative-state law.

It does not:
- prove positive role occupancy for every current J candidate;
- authorize live respondent execution;
- create a source reading permission;
- establish empirical relation truth;
- publish/select a learned product;
- create Field Forge roles or relations;
- alter B5 lifecycle;
- authorize V3/person state.

Positive current role load is a later exact source-capable authority/load proof.
