# VOZHD PYAT — MASTER RETURN SCHEMA

Status: `CURRENT_R2_FUNCTION_AND_PRODUCT_GRAIN`

Every substantive function/object/contract row should provide these fields.

```text
pyat_item_id
canonical_name
item_kind
terminal_capability_served

historical_family_or_origin
historical_stage_or_carrier_if_any
historical_authority_refs
historical_date_or_commit
historical_grain

current_semantic_owner
current_authority_refs
current_authority_date_or_commit
same_grain_succession_status
later_awareness_note

source_family
source_release_or_scope
source_identity_if_applicable

route_b_relevance
route_b_support_status
route_b_current_owner_refs
route_b_realization_refs
route_b_projection_or_authority_refs

pre_field_forge_product_kind
pre_field_forge_release_or_ref
pre_field_forge_product_status
learned_world_relationship

field_forge_relationship
field_forge_input_readiness
field_forge_structural_output_or_refusal

objective_prev3_relationship
current_consumer_or_terminal_demand

architecture_status
authority_status
implementation_status
source_free_proof_status
real_source_proof_status
populated_product_status
end_to_end_composition_status

negative_unresolved_state_behavior
replay_provenance_behavior
currentness_behavior
lifecycle_invalidation_behavior

current_code_refs
current_test_refs
known_stale_or_superseded_refs
compatibility_only_refs

disposition
residual_gap
blocking_dependency
recommended_next_action

evidence_refs
worker_confidence
```

## Disposition vocabulary

Prefer:

- `CURRENT_OWNED`
- `CURRENT_SUCCESSOR_PROVED`
- `CURRENT_OWNER_EXISTS__PROOF_MISSING`
- `CURRENT_READY_FOR_DECLARED_OPERATION`
- `FORMALLY_RETIRED`
- `SUPERSEDED_AT_GRAIN`
- `IMPLEMENTED_NOT_COMPOSED`
- `ARCHITECTURE_CLOSED_IMPLEMENTATION_OPEN`
- `POPULATION_MISSING`
- `SOURCE_SPECIFIC_REALIZATION_MISSING`
- `OPERATION_SPECIFIC_AUTHORITY_MISSING`
- `FIELD_FORGE_READY`
- `FIELD_FORGE_TYPED_REFUSAL`
- `HISTORICAL_ONLY`
- `OPEN`
- `BLOCKED`
- `CONTRADICTORY_INHERITANCE`

## Historical-stage handling

The former `v553_v558_relationship` column is no longer a current architecture column.

If a historical Dva stage is relevant, record it under:

- `historical_stage_or_carrier_if_any`;
- `historical_family_or_origin`;
- `objective_prev3_relationship`.

Do not create a missing-current-stage gap merely because a historical stage label lacks a current one-to-one node.

## Hard requirement

No significant historical capability may disappear because a modern module uses different nouns.

Map by **terminal behavior, semantic jurisdiction, information obligation, authority and consumer demand**, not filename similarity or historical stage adjacency.
