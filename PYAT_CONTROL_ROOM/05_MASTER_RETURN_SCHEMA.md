# VOZHD PYAT — MASTER RETURN SCHEMA

Every substantive function/object/contract row should provide these fields.

```text
pyat_item_id
canonical_name
item_kind
historical_family_or_origin
terminal_capability_served

prior_adjudication_status
prior_authority_refs

current_semantic_owner
current_authority_refs
current_consumer_or_terminal_demand

route_b_relevance
route_b_support_status
route_b_implementation_refs

field_forge_relationship
v553_v558_relationship

vision_status
architecture_status
authority_status
implementation_status
source_free_proof_status
real_source_proof_status
end_to_end_composition_status

negative_unresolved_state_behavior
replay_provenance_behavior
lifecycle_invalidation_behavior

current_code_refs
current_test_refs
known_stale_or_superseded_refs

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
- `FORMALLY_RETIRED`
- `SUPERSEDED_AT_GRAIN`
- `IMPLEMENTED_NOT_COMPOSED`
- `ARCHITECTURE_CLOSED_IMPLEMENTATION_OPEN`
- `ADOPTION_CANDIDATE`
- `OPEN`
- `BLOCKED`
- `CONTRADICTORY_INHERITANCE`

## Hard requirement

No significant historical capability may disappear because a modern module uses different nouns.

Map functions by **terminal behavior and information obligation**, not filename similarity.
