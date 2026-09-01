# FFIF006 — CLAIM IDENTITY CONSTITUTION

Status: `DESIGN_COMPLETE__NO_CURRENT_AUTHORITY_MINTED`

## Holding

Rawlsing requires a distinct `CLAIM_IDENTITY_MANIFEST` (`CIM`). A broad prose question, a query ID, or the common semantic input hash alone is not a claim identity.

The CIM has two nested identities:

1. `EMPIRICAL_PROPOSITION_KEY` — what empirical proposition is asserted.
2. `COMPARISON_CLAIM_KEY` — that proposition plus the frozen support/uncertainty and invariant-tolerance contracts used to adjudicate agreement, sufficiency, materiality, or bounded nonreducibility.

Formally:

`PROPOSITION_HASH = H(normalized proposition coordinates)`

`COMPARISON_HASH = H(PROPOSITION_HASH + support_uncertainty_contract_hash + invariant_tolerance_contract_hash + constitutive representation restriction, if any)`

This distinction prevents two opposite failures. Tolerance changes do not pretend that the underlying proposition changed; yet a comparator cannot change tolerance and still claim to have executed the same comparison.

## Minimum lawful CIM

```text
CLAIM_IDENTITY_MANIFEST {
  schema_version
  claim_id
  claim_version

  normalized_empirical_proposition
  assertion_slot_type
  proposition_operands[]
  empirical_unit_ref
  claim_scope_ref
  risk_set_ref
  population_target_ref
  temporal_context_scope
  estimand_ref
  weight_target_ref_or_NONE
  quantifier
  conditioning_set_ref_or_NONE
  comparison_baseline_ref_or_NONE
  assertion_scale_and_value_domain
  target_invariant_ref_or_bundle_ref
  semantic_input_manifest_ref
  semantic_input_manifest_hash
  source_native_ancestry_ceiling_ref
  inferential_class

  support_uncertainty_contract_ref
  support_uncertainty_contract_hash
  invariant_tolerance_contract_ref
  invariant_tolerance_contract_hash

  representation_scope_mode
  allowed_representation_family_refs[]

  proposition_hash
  comparison_claim_hash
  authority_refs[]
  validity_conditions[]
  invalidation_conditions[]
  forbidden_promotions[]
  supersedes[]
  superseded_by[]
}
```

## Constitutive boundary

Constitutive fields determine what must be true, of which units, under which semantic universe, over which population/risk set, at what scale, with which quantifier, conditioning, baseline, estimand, and invariant.

Execution metadata does not enter the proposition key: algorithm, estimator implementation, seed, software version, view output hash, runtime, storage, and observed result. Those belong in execution/view receipts.

Support/uncertainty and materiality rules are not part of the proposition hash, but they are mandatory in the comparison hash. Different contracts therefore yield:

`SAME_EMPIRICAL_PROPOSITION__DIFFERENT_COMPARISON_CONTRACT`

not direct agreement/disagreement.

## Representation neutrality

Default:

`representation_scope_mode = REPRESENTATION_NEUTRAL`

and `allowed_representation_family_refs[]` is empty.

A representation family becomes constitutive only when the proposition itself is explicitly representation-indexed, such as `NEIGHBORHOOD_STABILITY_UNDER_GEOMETRY_CONTRACT_G7`. It may not be added merely because one method can answer the claim conveniently. Otherwise every arm would answer a formally different claim and cross-view comparison would collapse.

## Semantic and role binding

The CIM binds the exact common semantic input hash, including the ordered TTAR sequence. A changed TTAR changes the semantic universe and therefore the proposition identity unless a parent proposition explicitly defines multiple registered semantic variants.

Any operand such as `educational position` must bind the exact PRA role authority. Changing `ACTIVE_POSITION` to `CONDITIONING_ONLY`, `SUPPLEMENTARY`, or `EXCLUDED` changes the operand/conditioning relation and creates a new proposition or invalidates an arm-local mutation.

PRA does not authorize the loss tolerance. TTAR does not authorize the social role. The CIM only binds their prior outputs.

## Fail-closed claim identity states

- `CLAIM_IDENTIFIED`
- `CLAIM_UNDERSPECIFIED`
- `CLAIM_IDENTITY_AUTHORITY_MISSING`
- `CLAIM_SEMANTIC_INPUT_UNRESOLVED`
- `CLAIM_ROLE_AUTHORITY_UNRESOLVED`
- `CLAIM_COMPARISON_CONTRACT_UNRESOLVED`
- `SAME_PROPOSITION_DIFFERENT_COMPARISON_CONTRACT`
- `DIFFERENT_CLAIM`
- `CLAIM_SUPERSEDED`

Only `CLAIM_IDENTIFIED` with one frozen comparison hash may enter a CVCR materiality court.

## Anti-reification ceiling

The CIM may name empirical invariants. It may not insert `FIELD`, `CLASS`, `CAPITAL`, `HEGEMONY`, `HOMOLOGY`, `MECHANISM`, `PERSONALITY`, or `WORLDVIEW` as assertion operands unless a separate competent upstream authority has already made that exact empirical object lawful. A theoretical noun cannot normalize an underspecified empirical question.

