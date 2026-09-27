# PRE553_J_COMPONENT_CERTIFICATION_CONTRIBUTION_RULE@1.0.0

Status:

`CONSTITUTED__READY_FOR_HQ_ADOPTION_AND_MINIMAL_M1_IMPLEMENTATION`

## 1. Rule identity

Rule:

`PRE553_J_COMPONENT_CERTIFICATION_CONTRIBUTION_RULE@1.0.0`

M1 claim family:

`PRE553_J_JOINT_RELATION_EVIDENCE`

Required validator algorithm identity for the later minimal implementation:

`PRE553_J_COMPONENT_CERTIFICATION_CONTRIBUTION_VALIDATOR@1.0.0`

Current generic jurisdiction:

`PYAT_M1_LEARNED_EMPIRICAL_ADJUDICATION@1.0.0`

This rule replaces the historical location of the certification act. It does not resurrect V551J packet execution.

## 2. Exact preserved contribution vocabulary

The historical v2.2.3 contribution vocabulary is preserved exactly:

```text
relation_component
context_component
special_or_missing_component
explained_nonrelation_component
blocked_component
unresolved_component
```

No renamed successor vocabulary is needed.

The historical duplicate fields `component_evidence_role` and `component_certification_contribution` carried the identical derived token. Current law therefore requires one ordered contribution determinant, not two duplicate physical fields.

## 3. Required exact premises

For each governed component, the validator must have exact, authority-bound access to:

1. exact current component identity/ref and component order;
2. exact `J_FAMILY_ITEM_ROLE` binding and authority state from the role-vector prerequisite;
3. exact evidence/match disposition needed to distinguish accepted match, ambiguous match, special/missing, explained nonrelation, and unexplained missing;
4. exact relation-evidence eligibility/context status under the current evidence authority;
5. exact negative/conflict refs where present;
6. exact replay refs sufficient to reconstruct the same ordered contribution vector.

No premise may be synthesized from lexical similarity, ordinal adjacency, target label, filename, or historical proximity.

## 4. Authority gate precedes positive contribution

Before the historical contribution decision is applied:

- role-vector/component-set/replay integrity failure -> M1 `INTEGRITY_FAILURE`;
- exact role authority `DENIED`, `NONCOMPARABLE`, `CONFLICTING`, or authority-ref mismatch -> affected component cannot be relation-bearing; validation is `BLOCKED`;
- exact role authority `UNRESOLVED`, `MISSING`, `UNKNOWN`, or required `GOVERNED_EMPTY` -> affected contribution is `unresolved_component`; validation is `UNRESOLVED`;
- a `VALUE` digest not resolving to one of the six exact family-role tokens is contract-invalid and cannot be relation-bearing.

This is the current fail-closed authority strengthening required to avoid manufacturing positive relation evidence. It does not change any historical positive distinction.

## 5. Per-component contribution rule

After exact premise/authority checks, classify each component with the following exact precedence:

```text
IF evidence match is ambiguous
    -> blocked_component

ELSE IF exact role/evidence authority is denied, conflicting, or noncomparable
    -> blocked_component

ELSE IF exact role/evidence premise is missing, unknown, unresolved,
        or required historical->current role mapping is absent
    -> unresolved_component

ELSE IF component is an exact special/missing response with no required relation match
    -> special_or_missing_component

ELSE IF component is an exact governed context/nonrelation component
        whose absence from relation evidence is explained by competent authority
    -> explained_nonrelation_component

ELSE IF component has an exact accepted match
        AND exact role authority is VALUE
        AND exact current evidence authority allows it as relation evidence
        AND no exact context/nonrelation premise excludes relation use
    -> relation_component

ELSE IF component has an exact accepted match
    -> context_component

ELSE
    -> unresolved_component
```

This preserves the historical v2.2.3 distinction while making the required current authority ceiling explicit.

## 6. Aggregate certification law

The validator freezes the ordered component vector:

```text
[
  {component_ref, ordinal, contribution_token, role_vector_binding_ref,
   exact_match_or_explanation_refs, authority_refs, negative_or_limit_refs},
  ...
]
```

and computes:

- `relation_count` = count(`relation_component`);
- `context_count` = count(`context_component`, `special_or_missing_component`, `explained_nonrelation_component`);
- `blocked_count` = count(`blocked_component`);
- `unresolved_count` = count(`unresolved_component`).

Exact M1 outcome order:

1. integrity mismatch -> `INTEGRITY_FAILURE`;
2. `blocked_count > 0` -> `BLOCKED`;
3. `unresolved_count > 0` -> `UNRESOLVED`;
4. `relation_count < 2` -> `RULE_NOT_SATISFIED`, reason `INSUFFICIENT_JOINT_RELATION_COMPONENTS`;
5. `relation_count >= 2 && context_count > 0` -> `RULE_SATISFIED`, determinant shape `JOINT_RELATION_EVIDENCE_WITH_CONTEXT`;
6. `relation_count >= 2 && context_count == 0` -> `RULE_SATISFIED`, determinant shape `JOINT_RELATION_EVIDENCE`.

Thus relation+context is mechanically distinct from relation-only evidence.

## 7. Exact M1 reason-code vocabulary for this rule

The minimal implementation must use exact rule-local reason codes sufficient to distinguish:

- `J_ROLE_PREREQUISITE_BLOCKED`
- `J_ROLE_PREREQUISITE_UNRESOLVED`
- `J_COMPONENT_SET_MISMATCH`
- `J_ROLE_VECTOR_REPLAY_MISMATCH`
- `J_AMBIGUOUS_COMPONENT_MATCH`
- `J_COMPONENT_CONTRIBUTION_UNRESOLVED`
- `INSUFFICIENT_JOINT_RELATION_COMPONENTS`
- `J_JOINT_RELATION_EVIDENCE_WITH_CONTEXT`
- `J_JOINT_RELATION_EVIDENCE`

A later implementation may add narrower exact reason codes but may not collapse these distinctions.

## 8. Determinant/replay requirements

The M1 `FamilyValidationResult.determinant_material` must contain enough exact material to reconstruct, byte-for-semantics, the same ordered contribution vector and aggregate counts, including:

- role-vector exact ref;
- role authority exact refs;
- exact governed component ordered identities/refs;
- per-component exact contribution token;
- per-component match/eligibility/explanation refs;
- relation/context/blocked/unresolved counts;
- contribution rule/version;
- prerequisite-channel exact ref;
- required negative/limit refs;
- replay-contract ref.

`explanation_material` must expose the reason-code and contribution summary but is not a substitute for determinant identity.

A second `ComponentAuthorityVectorReceipt` for the contribution dimension is **not required now** because M1 is the exact current consumer and no later current consumer requiring independent contribution-vector dereference was proved. If such a consumer is later governed, that later contract must explicitly add an independently resolvable carrier without changing this rule.

## 9. Current M1 outcome ceiling

M1 outcomes are limited to the existing runtime vocabulary:

- `RULE_SATISFIED`
- `RULE_NOT_SATISFIED`
- `ABSTAINED`
- `BLOCKED`
- `UNRESOLVED`
- `INTEGRITY_FAILURE`.

This J rule does not create product release/currentness, structural admission, consumer permission, causal truth, actor state, or V3 state.

## 10. Historical conservation proof

Historical V551J v2.2.3 at blob
`740bae4cfd4da7ed8aa2c9a2321c47f26ba7c7e8`
derived the same six tokens and consumed them by:

- counting `relation_component`;
- counting context/special/explained nonrelation;
- blocking unresolved;
- requiring at least two relation components;
- distinguishing certified joint evidence with context.

C4R1 independently identified component roles/certification-contribution roles as information-bearing capital. C4R2A later demonstrated a possible physical envelope but was explicitly reclassified non-authoritative. This constitution preserves the function in current M1 instead of adopting that historical/prototype topology.
