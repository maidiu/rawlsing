# M1 TYPED DISPOSITION SCHEMA R1

Proposed post-adoption family:

`LearnedEmpiricalDisposition@1.0.0`

This document is a normative schema contract, not an implementation.

## 1. Identity role

`LearnedEmpiricalDisposition` is an adjudication receipt. Its deterministic object identity SHALL include its exact governing rule/authority bindings and evidence closure.

It SHALL NOT be used as the canonical P1 `SEMANTIC_CLAIM_IDENTITY`. The latter is separately supplied by the family validator only when a truth-bearing claim is lawfully constituted.

## 2. Required fields

| Field | Requirement | Meaning |
|---|---|---|
| `schema_id` | exact | `LearnedEmpiricalDisposition` |
| `schema_version` | exact | `1.0.0` |
| `jurisdiction_contract_id` | exact | M1 adjudication contract identity |
| `disposition_id` | derived | deterministic object identity |
| `content_hash` | derived | canonical disposition projection hash |
| `disposition_class` | typed | `SUBSTANTIVE`, `ABSTENTION`, `BLOCKED`, `UNRESOLVED`, `INTEGRITY_FAILURE` |
| `rule_outcome` | typed | `RULE_SATISFIED`, `RULE_NOT_SATISFIED`, `NOT_EVALUATED`, `UNRESOLVED` |
| `reason_code` | exact | family or jurisdiction reason token |
| `claim_family_id` | exact | semantic claim/relation family |
| `claim_rule_id` | exact | exact family rule semantic identity |
| `relation_proposition_identity_ref` | exact or typed absence | P1 proposition identity adjudicated |
| `semantic_claim_identity_ref` | exact or typed absence | only if bound family validator lawfully emits truth-bearing claim |
| `semantic_assertion_polarity_or_state` | typed | validator-owned; `NONE` when no truth-bearing claim |
| `family_rule_binding_ref` | exact | exact M1 rule-binding object |
| `validator_authority_ref` | exact | id/version/hash authority instance |
| `rule_selection_authority_ref` | exact or typed purpose-bound absence | required whenever current selection is claimed; exact-pinned replay may declare pinned purpose |
| `discovery_result_receipt_refs` | exact set | I05 receipts consumed |
| `discovery_authority_refs` | exact set | exact discovery authorities |
| `empirical_fact_refs` | exact set | support/evidence facts |
| `validation_fact_refs` | exact set | validation facts, allowed to equal support refs only if rule says so |
| `empirical_query_spec_refs` | exact set | query semantic preimages required by rule |
| `empirical_predicate_refs` | exact set | predicate semantic preimages required by rule |
| `source_universe_refs` | exact set | source/universe scope |
| `risk_set_refs` | exact set | exact risk/denominator scope |
| `topology_scope_refs` | exact set/typed material | exact topology scope |
| `measure_basis_refs` | exact set | measure identities |
| `weight_design_estimand_refs` | exact set or typed N/A | only if rule requires |
| `comparability_authority_refs` | exact set or typed N/A | operation-scoped |
| `composition_authority_refs` | exact set or typed N/A | operation-scoped |
| `coverage_claims` | exact typed set | preserve I05 coverage semantics |
| `coverage_states` | exact typed set | preserve candidate terminal states |
| `conserved_empirical_states` | exact typed multiset/vector | no state collapse |
| `support_uncertainty_state` | exact typed | inherited/evaluated uncertainty |
| `support_uncertainty_refs` | exact set | methods/results/authority |
| `blocking_negative_authority_refs` | exact set | denials, missing/conflict/noncomparability refs |
| `required_prerequisite_channel_states` | exact mapping | family-rule-required premise closure |
| `semantic_ceiling` | exact | upper bound on interpretation/use |
| `authority_closure_refs` | exact set | all constitutive governing authorities |
| `dependency_refs` | exact set | immutable input/dependency closure |
| `validator_algorithm_identity` | exact | code/algorithm identity if semantically required |
| `validator_parameters_ref` | exact | deterministic family-rule parameters |
| `determinant_manifest_ref` | exact | complete machine-readable result determinants |
| `explanation_ref` | exact | deterministic explanation object/text hash |
| `replay_ref` | exact | replay recipe/root |
| `product_release_effect` | exact false | M1 cannot release products |
| `current_selection_effect` | exact false | M1 cannot make products current |
| `structural_admission_effect` | exact false | M1 cannot structurally admit |
| `consumer_permission_effect` | exact false | M1 cannot grant downstream use |

## 3. Rule binding schema

`M1FamilyRuleBinding@1.0.0` SHALL contain:

- `claim_family_id`
- `claim_rule_id`
- `validator_authority_ref`
- `selection_purpose`: `CURRENT_GOVERNED_USE` or `EXACT_PINNED_REPLAY`
- `current_selection_authority_ref` when purpose is current governed use
- `applicability_scope`
- `allowed_input_object_families_and_states`
- `required_prerequisite_channels`
- `required_source_relation_kinds`
- `required_measure_weight_estimand_authorities`
- `required_coverage_strength`
- `uncertainty_policy_ref`
- `output_semantic_contract`
- `semantic_ceiling`
- `validator_algorithm_identity_if_required`
- `validator_parameters_ref`
- `replay_contract_ref`

The binding itself must have deterministic identity and exact authority closure.

## 4. Positive and nonpositive result law

### Substantive positive
`disposition_class=SUBSTANTIVE` + `rule_outcome=RULE_SATISFIED`.

This is permitted only after exact rule execution. It creates a truth-bearing semantic claim only if the family rule output contract says so and supplies P1-complete claim identity.

### Substantive not-satisfied
`disposition_class=SUBSTANTIVE` + `rule_outcome=RULE_NOT_SATISFIED`.

This is an adjudication result, not automatically negative truth.

### Abstention
For valid inputs on which the exact family rule cannot or must not decide, e.g. rule-defined valid-empty, noncomparability, insufficient/coverage-limited evidence.

### Blocked
For missing/denied/conflicting required authority, missing rule binding, applicability mismatch, or unresolved required premise.

### Unresolved
For a governed unresolved state not reducible to denial or integrity failure.

### Integrity failure
For hash/ref/schema/replay/semantic-projection mismatch or impossible internal state.

## 5. Orthogonal evidence conservation

The schema SHALL preserve upstream evidence states even when a substantive rule returns a result.

Forbidden collapses include:

`OBSERVED_ZERO -> ZERO_SUPPORT`

`ZERO_SUPPORT -> VALID_EMPTY`

`VALID_EMPTY -> RULE_NOT_SATISFIED`

`NONCOMPARABLE -> RULE_NOT_SATISFIED`

`COVERAGE_LIMITED -> GLOBAL_ABSENCE`

`BLOCKED -> NEGATIVE_TRUTH`

`UNRESOLVED -> DENIED`

`INTEGRITY_FAILURE -> VALID_EMPTY`

## 6. Canonicalization

Set-like exact refs are sorted/deduplicated canonically. Ordered or role-bearing family payloads MUST retain their family-defined order/roles and must not be set-flattened.

Binary floating-point values SHALL NOT be used in semantic identity when exact canonical numerics are available under existing PRE553 law.

A deterministic content hash is necessary for replay but is never sufficient proof that the substantive rule or claim semantics are correct.
