# FFIF006 — LOSS-BUDGET OBJECT DECISION

## Decision

Rawlsing requires a separate typed object:

`CLAIM_INVARIANT_TOLERANCE_CONTRACT` (`CITC`).

The CITC must not be embedded as untyped fields inside the CIM. Claim identity and tolerance authority have different owners, evidence, revision paths, and reuse rules. However, the CIM must bind the immutable CITC ref/hash in its `COMPARISON_CLAIM_KEY`.

This yields fewer objects than separate generic loss-budget, materiality, and invariant manifests: one CITC contains the claim-scoped invariant-by-dimension contract, while raw realized losses remain in view loss manifests.

## Minimum CITC

```text
CLAIM_INVARIANT_TOLERANCE_CONTRACT {
  contract_id
  contract_version
  proposition_ref
  proposition_hash

  rows[] {
    assertion_slot_ref
    invariant_ref
    loss_dimension_id
    criticality_state
    tolerance_type
    tolerance_value_or_rule
    unit_and_scale
    direction_of_worse_loss
    aggregation_rule_or_NONE
    support_requirement_ref
    uncertainty_interaction_rule
    source_resolution_ref_or_NONE
    error_model_or_design_precision_ref_or_NONE
    authority_basis
    authority_ref
    evidence_refs[]
    allowed_uses[]
    forbidden_uses[]
    downstream_requirement_ref_or_NONE
  }

  freeze_receipt_ref
  frozen_before_output_refs[]
  canonicalization_spec
  contract_hash
  validity_conditions[]
  invalidation_conditions[]
  supersedes[]
  superseded_by[]
}
```

## Tolerance types

- `EXACT_ZERO`
- `ABSOLUTE_MARGIN`
- `RELATIVE_MARGIN`
- `COMPONENTWISE_RULE`
- `SET_RECALL_RULE`
- `ORDER_OR_TOPOLOGY_RULE`
- `EQUIVALENCE_MARGIN_WITH_TEST`
- `NO_REQUIREMENT_FOR_CLAIM`
- `UNRESOLVED__NO_EXECUTION`

No generic scalar `LOSS = 0.17` is lawful unless one atomic claim genuinely has one dimension and unit.

## Authority rule

Empirical materiality may be authorized only by a competent claim-materiality adjudication that binds claim semantics to relevant source resolution and, where inferential, a design/error model. Preregistered analytic purpose or substantive minimum effect may contribute when the proposition explicitly warrants them.

TTAR supplies the transform's loss profile, not tolerability. PRA supplies role semantics, not tolerability. A view producer supplies realized loss, not tolerability. CVCR applies the contract, not authors it. Downstream PRE-V3 and engineering authorities set utility/cost requirements only.

## No post-hoc tolerance

The contract hash must be frozen before view outputs or final-holdout comparative results exist. Any later threshold change creates a new comparison claim version and requires replay from raw immutable outputs. It may not overwrite the prior decision.

Mandatory hostile fixtures:

1. threshold moved until geometry and atlas agree;
2. tolerance widened because a preferred view fails;
3. tolerance narrowed after exciting disagreement;
4. different tolerances applied to views answering one slot;
5. downstream utility rewrites empirical tolerance;
6. minority threshold selected after observing minority mass;
7. predictive metric selected after results;
8. confidence/equivalence regime changed after comparison.

Each must return `POSTHOC_TOLERANCE_MUTATION__COMPARISON_INVALID` or a new, explicitly versioned comparison—never silent acceptance.

## Preregistration is necessary, not sufficient

Every nonzero empirical tolerance requires at least one relevant evidence basis:

- claim definition/logical quantifier;
- source resolution;
- authorized error model/design precision;
- claim-warranted substantive minimum effect;
- frozen actor-independent analytic information requirement.

Historical precedent and convention may support but never close authority alone. There is no universal 5% rule.

