# HQ122 J2I — J VALIDATOR AND DETERMINANT RECEIPT

Claim family:

`PRE553_J_JOINT_RELATION_EVIDENCE`

Claim rule:

`PRE553_J_COMPONENT_CERTIFICATION_CONTRIBUTION_RULE@1.0.0`

Validator algorithm:

`PRE553_J_COMPONENT_CERTIFICATION_CONTRIBUTION_VALIDATOR@1.0.0`

Selection purpose:

`CURRENT_GOVERNED_USE`

Registration is exact through the existing immutable `M1ValidatorRegistry`.

## Current-evidence premise transport

The caller supplies exact per-component evidence/match/eligibility premises through the already-hashed M1 `requested_scope` under:

`pre553_j_component_certification_premises`

No M1 core field or schema was added.

Each premise binds:

- component ID/ref/ordinal;
- evidence-match disposition;
- relation-eligibility disposition;
- exact special/missing flag;
- exact governed-nonrelation explanation flag;
- authority refs;
- dependency refs;
- negative/limit refs.

The J validator requires the premise vector to match the exact governed role-vector component set and order.

## Contribution law

Exact implemented precedence:

1. denied/noncomparable/conflicting role/evidence authority or ambiguous match -> `blocked_component`;
2. non-VALUE role or unresolved match/eligibility -> `unresolved_component`;
3. exact special/missing response -> `special_or_missing_component`;
4. exact governed explained nonrelation -> `explained_nonrelation_component`;
5. exact accepted match + VALUE role + relation eligibility -> `relation_component`;
6. exact accepted match otherwise -> `context_component`;
7. otherwise -> `unresolved_component`.

Negative/unknown role authority cannot reach the relation branch.

## Aggregate law

- blocked > 0 -> `BLOCKED`
- unresolved > 0 -> `UNRESOLVED`
- relation < 2 -> `RULE_NOT_SATISFIED / INSUFFICIENT_JOINT_RELATION_COMPONENTS`
- relation >= 2 + context-like > 0 -> `RULE_SATISFIED / J_JOINT_RELATION_EVIDENCE_WITH_CONTEXT`
- relation >= 2 + context-like == 0 -> `RULE_SATISFIED / J_JOINT_RELATION_EVIDENCE`

## Determinant

The validator freezes in exact M1 determinant material:

- ordered per-component ref/id/ordinal;
- role token or typed state;
- contribution token;
- match disposition;
- eligibility disposition;
- authority refs;
- dependency refs;
- negative/limit refs;
- relation/context/blocked/unresolved counts;
- role-vector ref;
- role-vector coverage proof hash;
- contribution rule id;
- prerequisite-channel ref;
- replay-contract ref.

No second contribution-vector object was added.
