# GT3/GT4 M2 — METABOLISM CONTENT-ADDRESSING REPAIR R1

## Terminal

`PASS__GT34_M2_METABOLISM_CONTENT_ADDRESSING_REPAIRED__CANDIDATE_READY_FOR_REAUDIT`

## Execution boundary

- repository: `maidiu/rawlsing`
- branch: `agent/rabochii-gt34-m2-metabolism-content-address-repair-r1`
- exact working-ancestry start: `913f2274bfb5a2b204a8666b34aa1b658eb86966`
- immutable instruction ref: `8e81c1d2e6351a7363494a1aa1ea16a8395519d5`
- instruction blob: `afdca448d5febe1727033839f65898c99721b9ab`
- worker: `M2 — METABOLISM CONTENT-ADDRESSING REPAIR R1`
- profile: `SEMANTIC_AUTHORITY`
- production implementation: NONE
- authority adoption: NONE
- PSEPF execution: NONE
- actor mutation: NONE

Repair scope was limited exactly to L2 defects:

- `UNDERDEFINED_SELF_HASHING_OPERATION_ENTRY`
- `UNDEFINED_DECISION_RECEIPT_HASH_PROJECTION`

No K2 jurisdiction, decision state, operation kind, ownership boundary, target-owner rule, valid-empty semantics, portability law, RNG law, or direct-assignment firewall was widened or redesigned.

---

## Source candidate and defect evidence

K2 return:

`data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/GT3_GT4_AUTHORITY_CANARY_WAVE_R1/K2_METABOLISM_AUTHORITY_CANDIDATE_R1/00_RETURN.md`

K2 return blob:

`4db58eb64c8e8f4e430ebea6980d7a1f21b518b1`

Old candidate authority hash:

`bc6c75adbb783b0c00af503375a77ef53be905d3113b4c433f10ddc7d6c96334`

Old valid-empty registry hash:

`b65c4577893878ceb36a3b8b74ad7cf873a7807a35ad209efafcd8be5d1f547c`

L2 proved that both old hashes recomputed exactly but that the candidate did not define the operation-entry or decision-receipt hash projections required for exact implementation/replay.

Repository canonical semantic hash law remains the accepted current law from:

`rawlsing_next/pre553_empirical_objects.py`

blob:

`91974c52ce8c0acafa939be0d7d83f4a5c8085b7`

Exact law consumed by this repair:

`canonical_json(value) = json.dumps(canonicalize(value), sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)`

`semantic_hash(value) = lowercase_hex(SHA256(UTF8(canonical_json(value))))`

For semantically set-like fields, current `canonical_set` law is consumed exactly: canonicalize each member, key by canonical JSON, collapse identical canonical members, and emit in ascending canonical-JSON order.

---

# Repair A — operation-entry semantic projection

Authority material:

`V3_EMPIRICAL_POSSIBILITY_METABOLISM_OPERATION_ENTRY_SEMANTIC_PROJECTION@1.0.0`

Semantic contract hash of the projection-law object itself:

`ab0866cf59676a097cb49d5c77cdd3898b92c9abab7dc223eaa7e9151177587f`

The projection includes **every semantic field** of
`V3_EMPIRICAL_POSSIBILITY_METABOLISM_OPERATION_REGISTRY_ENTRY@1.0.0`.

It excludes only:

`operation_ref.operation_content_hash`

because that value is derived from the projection.

The semantic parts of `operation_ref` remain inside the digest as:

- `operation_id`
- `operation_version`

The final `operation_ref` is materialized or validated only **after** the digest exists.

Exact formula:

`operation_content_hash = lowercase_hex(SHA256(UTF8(canonical_json(operation_entry_semantic_projection))))`

There is no self-hash cycle.

There is no alternate projection and no caller-selectable projection.

Unknown/unlisted entry fields are schema failure rather than silently excluded identity material.

Top-level v1 collection law:

Set-like:
- `accepted_upstream_input_states`
- `requested_use_classes`
- `causal_parent_requirements`
- `negative_limit_refs`

Semantically ordered top-level sequences:
- NONE in the v1 operation entry.

Any ordered sequence inside an exact referenced object remains owned by that object's exact content identity and is not reordered by this projection.

---

# Repair B — decision-receipt semantic projection

Authority material:

`V3_EMPIRICAL_POSSIBILITY_METABOLISM_DECISION_RECEIPT_SEMANTIC_PROJECTION@1.0.0`

Semantic contract hash of the projection-law object itself:

`e0b6a723aaa31f07c0bf9d156961c9fdcd424e3b6705acbfc04d2612278b2e80`

The projection includes every K2 replay-material receipt field:

- `actor_ref`
- `actor_identity_authority_ref`
- `v3_empirical_possibility_input_ref`
- `psepf_ref`
- `psepf_replay_ref`
- `comparator_receipt_refs`
- `conditioner_ancestry_refs`
- `source_universe_ref`
- `release_ref`
- `empirical_reference_time_ref`
- `measure_basis_ref`
- `estimand_refs`
- `uncertainty_ref_or_typed_state_ref`
- `v3_decision_time_ref`
- `v3_effective_use_time_ref`
- `requested_use_class`
- `requested_operation_ref`
- `operation_registry_ref`
- `resolved_operation_entry_ref_or_typed_absence`
- `requested_downstream_owner_ref_or_read_only_marker`
- `resolved_downstream_owner_ref_or_typed_absence`
- `causal_parent_contract_ref_or_typed_absence`
- `causal_parent_refs`
- `pre_state_checkpoint_ref`
- `runtime_rule_registry_ref`
- `rng_decision_receipt_refs_or_empty`
- `decision_state`
- `decision_reason_code`

It excludes only:

`decision_receipt_hash`

Exact formula:

`decision_receipt_hash = lowercase_hex(SHA256(UTF8(canonical_json(decision_receipt_semantic_projection))))`

The same projection/hash law applies without exception to:

- positive receipts;
- `DENY`;
- `VALID_EMPTY`;
- `NONCOMPARABLE`;
- `STALE`;
- `UNRESOLVED_INPUT`;
- `UNRESOLVED_AUTHORITY`;
- `INTEGRITY_FAILURE`.

The downstream mutation owner can independently reconstruct the projection from immutable receipt material, recompute the SHA-256 digest, and require exact equality before treating the receipt as the referenced metabolism decision.

Top-level v1 set-like receipt fields:

- `comparator_receipt_refs`
- `conditioner_ancestry_refs`
- `estimand_refs`
- `causal_parent_refs`
- `rng_decision_receipt_refs_or_empty`

Semantically ordered top-level receipt sequences:
- NONE in the v1 decision receipt.

Semantic order inside exact referenced ancestry/replay/RNG objects remains governed by those referenced objects' identities.

Unknown/unlisted receipt fields are schema failure; they cannot be silently omitted from the content identity. The only permitted derived exclusion is `decision_receipt_hash`.

---

# Corrected complete candidate identities

## Corrected authority candidate

ID/version remains:

`V3_EMPIRICAL_POSSIBILITY_METABOLISM_AUTHORITY@1.0.0`

because the candidate has never been adopted and this worker is repairing its pre-adoption machine identity law only.

Corrected complete semantic hash:

`e1ce806ebd443d562c7d5afdb14f00739a3b7478e2a2fcf1acfc9acb89b2e34e`

Superseded pre-repair candidate hash:

`bc6c75adbb783b0c00af503375a77ef53be905d3113b4c433f10ddc7d6c96334`

The old hash remains historical K2/L2 evidence only and must not be adopted as the corrected candidate.

## Corrected valid-empty registry

ID/version/state remains exactly:

`V3_EMPIRICAL_POSSIBILITY_METABOLISM_OPERATION_REGISTRY@1.0.0`

`VALID_EMPTY_NO_ACCEPTED_OPERATIONS`

Recomputed semantic hash:

`b65c4577893878ceb36a3b8b74ad7cf873a7807a35ad209efafcd8be5d1f547c`

This is **identical** to the old registry hash because M2 made no change to the valid-empty registry material itself.

It still contains:

- `entries = []`
- `positive_read_operations = 0`
- `positive_transition_operations = 0`
- caller selection = false
- fuzzy/latest/default selection forbidden.

Therefore the corrected candidate package still carries:

`ZERO_POSITIVE_AUTHORITY`.

The registry's unchanged hash does not preserve the superseded authority candidate: HQ adoption must bind the corrected authority hash and the exact registry hash as a pair, exactly as K2's adoption law already required.

---

# Complete corrected authority candidate material

```json
{
  "schema": "V3_EMPIRICAL_POSSIBILITY_METABOLISM_AUTHORITY@1.0.0",
  "authority_id": "V3_EMPIRICAL_POSSIBILITY_METABOLISM_AUTHORITY",
  "authority_version": "1.0.0",
  "owner": "V3_EMPIRICAL_POSSIBILITY_INTAKE_METABOLISM_COURT",
  "jurisdiction": {
    "positive_effect": "DECIDE_READ_OR_NAMED_TRANSITION_ELIGIBILITY_FOR_ONE_EXACT_ALREADY_PRODUCED_V3_EMPIRICAL_POSSIBILITY_INPUT_AND_ONE_EXACT_ACTOR_USE_CONTEXT_ONLY",
    "input_family": "V3EmpiricalPossibilityInput",
    "does_not_create_empirical_semantics": true,
    "does_not_create_downstream_actor_state_semantics": true,
    "does_not_mutate_actor": true,
    "does_not_select_downstream_mutation_owner": true,
    "source_scope_for_first_operation": "EXACTLY_ONE_SOURCE_UNIVERSE_AND_RELEASE",
    "measurement_transfer_or_portability": "FORBIDDEN_NOT_CONSUMED"
  },
  "input_binding_contract": {
    "required_exact_fields": [
      "actor_ref",
      "actor_identity_authority_ref",
      "v3_empirical_possibility_input_ref",
      "psepf_ref",
      "psepf_replay_ref",
      "comparator_receipt_refs",
      "conditioner_ancestry_refs",
      "source_universe_ref",
      "release_ref",
      "empirical_reference_time_ref",
      "measure_basis_ref",
      "estimand_refs",
      "uncertainty_ref_or_typed_state_ref",
      "upstream_negative_or_limit_refs",
      "v3_decision_time_ref",
      "v3_effective_use_time_ref",
      "requested_use_class",
      "requested_operation_ref",
      "requested_downstream_owner_ref_or_read_only_marker",
      "pre_state_checkpoint_ref",
      "causal_parent_refs",
      "runtime_rule_registry_ref"
    ],
    "cardinality_law": {
      "actor_ref": "EXACTLY_ONE",
      "v3_empirical_possibility_input_ref": "EXACTLY_ONE",
      "psepf_ref": "EXACTLY_ONE",
      "source_universe_ref": "EXACTLY_ONE",
      "release_ref": "EXACTLY_ONE",
      "measure_basis_ref": "EXACTLY_ONE",
      "comparator_receipt_refs": "ONE_OR_MORE_EXACT",
      "conditioner_ancestry_refs": "ONE_OR_MORE_EXACT",
      "estimand_refs": "ONE_OR_MORE_EXACT",
      "causal_parent_refs": "EXACT_SET_AS_REQUIRED_BY_REGISTERED_OPERATION"
    },
    "binding_law": [
      "PSEPF_AND_V3_INPUT_IDENTITIES_ARE_REFERENCED_NOT_COPIED",
      "COMPARATOR_AND_CONDITIONER_ANCESTRY_MUST_MATCH_THE_EXACT_INPUT_DEPENDENCY_CLOSURE",
      "SOURCE_RELEASE_MEASURE_ESTIMAND_AND_UNCERTAINTY_ARE_UPSTREAM_REFS_NOT_REAUTHORED_VALUES",
      "V3_DECISION_AND_EFFECTIVE_USE_TIME_ARE_V3_INTAKE_CONTEXT_NOT_UPSTREAM_MEASUREMENT_REWRITES",
      "PRE_STATE_CHECKPOINT_AND_CAUSAL_PARENT_SET_BIND_THE_V3_CAUSAL_CONTEXT",
      "NO_FUZZY_LATEST_DEFAULT_OR_LABEL_BASED_RESOLUTION"
    ]
  },
  "decision_space": [
    "ALLOW_READ_ONLY",
    "ELIGIBLE_FOR_NAMED_TRANSITION_RULE",
    "DENY",
    "VALID_EMPTY",
    "NONCOMPARABLE",
    "STALE",
    "UNRESOLVED_INPUT",
    "UNRESOLVED_AUTHORITY",
    "INTEGRITY_FAILURE"
  ],
  "decision_precedence": [
    "INTEGRITY_FAILURE",
    "UNRESOLVED_AUTHORITY",
    "NONCOMPARABLE",
    "STALE",
    "VALID_EMPTY",
    "UNRESOLVED_INPUT",
    "DENY",
    "ALLOW_READ_ONLY",
    "ELIGIBLE_FOR_NAMED_TRANSITION_RULE"
  ],
  "decision_semantics": {
    "ALLOW_READ_ONLY": "Exact registered READ_ONLY operation permits dereference/use as empirical possibility context only; zero actor mutation authority.",
    "ELIGIBLE_FOR_NAMED_TRANSITION_RULE": "Exact registered TRANSITION_ELIGIBILITY operation permits the named downstream mutation owner to independently evaluate its exact transition rule; this receipt is not mutation or state truth.",
    "DENY": "Exact metabolism authority or registered operation denies the requested use; no fallback.",
    "VALID_EMPTY": "Preserve lawful upstream/input valid-empty state for this use; no fabricated candidate, event, probability, or mutation.",
    "NONCOMPARABLE": "Required source/conditioner/measure/estimand/time relation for this exact use is explicitly noncomparable; no transfer or nearest substitute.",
    "STALE": "The exact input is stale for this V3 decision/effective-use context under the registered temporal-applicability rule; upstream field truth is not globally withdrawn.",
    "UNRESOLVED_INPUT": "Upstream empirical-possibility state is unresolved for the requested operation while integrity remains intact; not recoded as authority absence.",
    "UNRESOLVED_AUTHORITY": "Required exact operation, registry, mutation owner, rule, permission, temporal rule, causal-parent authority, or stochastic authority cannot be positively resolved.",
    "INTEGRITY_FAILURE": "Hash/schema/ref/replay/checkpoint/dependency mismatch; semantic decision is not attempted."
  },
  "operation_registry_contract": {
    "schema": "V3_EMPIRICAL_POSSIBILITY_METABOLISM_OPERATION_REGISTRY_ENTRY@1.0.0",
    "entry_required_fields": [
      "operation_ref",
      "status",
      "operation_kind",
      "accepted_input_class_ref",
      "accepted_upstream_input_states",
      "requested_use_classes",
      "temporal_applicability_rule_ref",
      "source_scope_cardinality",
      "measurement_transfer_allowed",
      "metabolism_effect_ceiling",
      "downstream_consumer_authority_ref",
      "downstream_mutation_owner_authority_ref_or_read_only_none",
      "downstream_transition_rule_ref_or_read_only_none",
      "downstream_mutation_ceiling_ref_or_read_only_none",
      "causal_parent_contract_ref",
      "causal_parent_requirements",
      "execution_mode",
      "adp020_contract_or_deterministic_none",
      "replay_rule_ref",
      "negative_limit_refs"
    ],
    "operation_ref_contract": {
      "required": [
        "operation_id",
        "operation_version",
        "operation_content_hash"
      ],
      "hash": "SHA256_OVER_V3_EMPIRICAL_POSSIBILITY_METABOLISM_OPERATION_ENTRY_SEMANTIC_PROJECTION@1.0.0",
      "projection_ref": "V3_EMPIRICAL_POSSIBILITY_METABOLISM_OPERATION_ENTRY_SEMANTIC_PROJECTION@1.0.0",
      "validation": "DERIVE_HASH_FROM_PROJECTION_FIRST_THEN_MATERIALIZE_OR_VALIDATE_OPERATION_REF__NO_SELF_REFERENCE"
    },
    "operation_kinds": [
      "READ_ONLY",
      "TRANSITION_ELIGIBILITY"
    ],
    "positive_transition_requirements": [
      "ENTRY_STATUS_ACCEPTED_CURRENT",
      "EXACT_ACCEPTED_INPUT_CLASS",
      "EXACT_REQUESTED_USE_CLASS",
      "EXACT_DOWNSTREAM_MUTATION_OWNER_AUTHORITY_REF",
      "EXACT_DOWNSTREAM_TRANSITION_RULE_REF",
      "EXACT_DOWNSTREAM_MUTATION_CEILING_REF",
      "EXACT_TEMPORAL_APPLICABILITY_RULE_REF",
      "EXACT_CAUSAL_PARENT_CONTRACT_AND_REQUIRED_PARENT_REFS",
      "EXACT_PRE_STATE_CHECKPOINT_REF",
      "EXACT_REPLAY_RULE_REF",
      "NO_UPSTREAM_NONCOMPARABLE_STALE_VALID_EMPTY_OR_UNRESOLVED_BLOCK",
      "IF_STOCHASTIC_EXACT_ADP020_AUTHORITY_RULE_STREAM_OPERATION_AND_RECEIPTS"
    ],
    "read_only_requirements": [
      "ENTRY_STATUS_ACCEPTED_CURRENT",
      "EXACT_ACCEPTED_INPUT_CLASS",
      "EXACT_REQUESTED_USE_CLASS",
      "EXACT_DOWNSTREAM_CONSUMER_AUTHORITY_REF",
      "METABOLISM_EFFECT_CEILING_READ_ONLY_NO_MUTATION",
      "DOWNSTREAM_MUTATION_OWNER_IS_TYPED_NONE_READ_ONLY",
      "NO_V2_RENDER_OR_ACTOR_STATE_SEMANTIC_PROMOTION"
    ],
    "execution_modes": [
      "DETERMINISTIC",
      "STOCHASTIC_ADP020"
    ],
    "stochastic_law": {
      "authority": "ADP-020",
      "authority_version": "1.0.0",
      "exact_authority_ref_required_per_positive_stochastic_entry": true,
      "static_named_stream_required": true,
      "allowed_rng_operation_required": true,
      "candidate_semantics_remain_outside_adp020": true,
      "rng_selection_is_not_transition_admission": true,
      "deterministic_path_consumes_no_dummy_draw": true
    },
    "generic_allow_active_causal_permission_atom": "FORBIDDEN",
    "caller_selected_unregistered_operation": "FORBIDDEN",
    "empty_registry_behavior": "VALID_EMPTY_REGISTRY__NO_POSITIVE_READ_OR_TRANSITION_OPERATION_AUTHORIZED",
    "operation_entry_semantic_projection": {
      "schema": "V3_EMPIRICAL_POSSIBILITY_METABOLISM_OPERATION_ENTRY_SEMANTIC_PROJECTION@1.0.0",
      "source_entry_schema": "V3_EMPIRICAL_POSSIBILITY_METABOLISM_OPERATION_REGISTRY_ENTRY@1.0.0",
      "semantic_field_projection": [
        "operation_ref.operation_id",
        "operation_ref.operation_version",
        "status",
        "operation_kind",
        "accepted_input_class_ref",
        "accepted_upstream_input_states",
        "requested_use_classes",
        "temporal_applicability_rule_ref",
        "source_scope_cardinality",
        "measurement_transfer_allowed",
        "metabolism_effect_ceiling",
        "downstream_consumer_authority_ref",
        "downstream_mutation_owner_authority_ref_or_read_only_none",
        "downstream_transition_rule_ref_or_read_only_none",
        "downstream_mutation_ceiling_ref_or_read_only_none",
        "causal_parent_contract_ref",
        "causal_parent_requirements",
        "execution_mode",
        "adp020_contract_or_deterministic_none",
        "replay_rule_ref",
        "negative_limit_refs"
      ],
      "derived_excluded_fields": [
        "operation_ref.operation_content_hash"
      ],
      "set_like_fields": [
        "accepted_upstream_input_states",
        "requested_use_classes",
        "causal_parent_requirements",
        "negative_limit_refs"
      ],
      "ordered_sequence_fields": [],
      "set_normalization": "REPOSITORY_CANONICAL_SET: canonicalize each member; key by repository canonical_json; identical canonical members collapse to one; emit members in ascending canonical_json order",
      "ordered_sequence_law": "NO_TOP_LEVEL_V1_OPERATION_ENTRY_SEQUENCE_FIELD_IS_SEMANTICALLY_ORDERED; any ordered sequence inside an exact referenced semantic object remains governed by that referenced object's own content identity and is not reordered here",
      "undeclared_sequence_field_policy": "REJECT_SCHEMA_MISMATCH",
      "unlisted_entry_field_policy": "REJECT_SCHEMA_MISMATCH__NO_SILENT_HASH_EXCLUSION",
      "operation_ref_field_policy": "ONLY_operation_id_operation_version_operation_content_hash_ALLOWED",
      "mapping_and_scalar_canonicalization": "REPOSITORY_CANONICALIZE",
      "projection_shape": "canonical mapping containing schema plus every semantic field above; operation_ref is projected as {operation_id,operation_version} and never includes operation_content_hash",
      "canonical_json_law": "json.dumps(canonicalize(projection), sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False)",
      "sha256_law": "operation_content_hash = lowercase_hex(SHA256(UTF8(canonical_json(operation_entry_semantic_projection))))",
      "operation_ref_materialization": "AFTER digest computation, materialize or validate {operation_id,operation_version,operation_content_hash}; operation_id/version must equal the projected values and operation_content_hash must equal the independently recomputed digest",
      "self_reference": "FORBIDDEN",
      "alternate_projection": "FORBIDDEN",
      "caller_selected_projection": "FORBIDDEN",
      "projection_or_hash_mismatch": "INTEGRITY_FAILURE"
    }
  },
  "non_ownership": [
    "PSEPF_CELLS_MASSES_SUPPORT_GEOMETRY",
    "COMPARATOR_SEMANTICS",
    "EMPIRICAL_PREDICATE_OR_QUERY_SEMANTICS",
    "SOURCE_UNIVERSE_RELEASE_MEASURE_ESTIMAND_SEMANTICS",
    "MEASUREMENT_PORTABILITY_OR_EQUIVALENCE",
    "V557_V558_STRUCTURAL_CONTEXT_SEMANTICS",
    "DOWNSTREAM_ACTOR_STATE_OR_TRANSITION_SEMANTICS",
    "V3_MUTATION_EXECUTION",
    "ADP020_RANDOMNESS_SEMANTICS",
    "V2_RENDERING_PERSONA_VOICE"
  ],
  "direct_assignment_firewall": [
    "PSEPF_MASS_TO_ACTOR_BELIEF_PROBABILITY",
    "MODAL_POPULATION_CELL_TO_ACTOR_RESPONSE_OR_PERSONA",
    "POPULATION_CONFIGURATION_TO_ACTOR_STRUCTURAL_POSITION",
    "EMPIRICAL_POSSIBILITY_TO_MEMORY_OR_KNOWLEDGE",
    "EMPIRICAL_POSSIBILITY_TO_PERSONALITY_TYPE_OR_ATTRACTOR",
    "UNREGISTERED_DIRECT_ACTOR_STATE_MUTATION",
    "RAW_EMPIRICAL_OR_STRUCTURAL_PRIOR_TO_ACTOR_STATE",
    "RENDERED_OR_LLM_OUTPUT_TO_CAUSAL_STATE"
  ],
  "replay_contract": {
    "receipt_schema": "V3_EMPIRICAL_POSSIBILITY_METABOLISM_DECISION_RECEIPT@1.0.0",
    "every_decision_binds": [
      "actor_ref",
      "actor_identity_authority_ref",
      "v3_empirical_possibility_input_ref",
      "psepf_ref",
      "psepf_replay_ref",
      "comparator_receipt_refs",
      "conditioner_ancestry_refs",
      "source_universe_ref",
      "release_ref",
      "empirical_reference_time_ref",
      "measure_basis_ref",
      "estimand_refs",
      "uncertainty_ref_or_typed_state_ref",
      "v3_decision_time_ref",
      "v3_effective_use_time_ref",
      "requested_use_class",
      "requested_operation_ref",
      "operation_registry_ref",
      "resolved_operation_entry_ref_or_typed_absence",
      "requested_downstream_owner_ref_or_read_only_marker",
      "resolved_downstream_owner_ref_or_typed_absence",
      "causal_parent_contract_ref_or_typed_absence",
      "causal_parent_refs",
      "pre_state_checkpoint_ref",
      "runtime_rule_registry_ref",
      "rng_decision_receipt_refs_or_empty",
      "decision_state",
      "decision_reason_code",
      "decision_receipt_hash"
    ],
    "positive_transition_handoff": "DOWNSTREAM_MUTATION_OWNER_MUST_REFERENCE_EXACT_METABOLISM_DECISION_RECEIPT_AND_INDEPENDENTLY_OWN_AND_RECORD_ANY_MUTATION",
    "negative_replay": "NEGATIVE_OR_UNRESOLVED_RECEIPTS_ARE_CONTENT_ADDRESSED_AND_REPLAYABLE_WITHOUT_DEFAULT_REPAIR",
    "rng_receipt_law": "NONEMPTY_ONLY_WHEN_THE_REGISTERED_OPERATION_IS_STOCHASTIC_AND_ADP020_ACTUALLY_CONSUMES_ENTROPY",
    "decision_receipt_semantic_projection": {
      "schema": "V3_EMPIRICAL_POSSIBILITY_METABOLISM_DECISION_RECEIPT_SEMANTIC_PROJECTION@1.0.0",
      "source_receipt_schema": "V3_EMPIRICAL_POSSIBILITY_METABOLISM_DECISION_RECEIPT@1.0.0",
      "semantic_field_projection": [
        "actor_ref",
        "actor_identity_authority_ref",
        "v3_empirical_possibility_input_ref",
        "psepf_ref",
        "psepf_replay_ref",
        "comparator_receipt_refs",
        "conditioner_ancestry_refs",
        "source_universe_ref",
        "release_ref",
        "empirical_reference_time_ref",
        "measure_basis_ref",
        "estimand_refs",
        "uncertainty_ref_or_typed_state_ref",
        "v3_decision_time_ref",
        "v3_effective_use_time_ref",
        "requested_use_class",
        "requested_operation_ref",
        "operation_registry_ref",
        "resolved_operation_entry_ref_or_typed_absence",
        "requested_downstream_owner_ref_or_read_only_marker",
        "resolved_downstream_owner_ref_or_typed_absence",
        "causal_parent_contract_ref_or_typed_absence",
        "causal_parent_refs",
        "pre_state_checkpoint_ref",
        "runtime_rule_registry_ref",
        "rng_decision_receipt_refs_or_empty",
        "decision_state",
        "decision_reason_code"
      ],
      "derived_excluded_fields": [
        "decision_receipt_hash"
      ],
      "set_like_fields": [
        "comparator_receipt_refs",
        "conditioner_ancestry_refs",
        "estimand_refs",
        "causal_parent_refs",
        "rng_decision_receipt_refs_or_empty"
      ],
      "ordered_sequence_fields": [],
      "set_normalization": "REPOSITORY_CANONICAL_SET: canonicalize each member; key by repository canonical_json; identical canonical members collapse to one; emit members in ascending canonical_json order",
      "ordered_sequence_law": "NO_TOP_LEVEL_V1_DECISION_RECEIPT_SEQUENCE_FIELD_IS_SEMANTICALLY_ORDERED; semantic order inside any exact referenced replay/RNG/ancestry object remains governed by that object's own content identity and is not reordered here",
      "undeclared_sequence_field_policy": "REJECT_SCHEMA_MISMATCH",
      "unlisted_receipt_field_policy": "REJECT_SCHEMA_MISMATCH__NO_SILENT_HASH_EXCLUSION_EXCEPT_decision_receipt_hash",
      "mapping_and_scalar_canonicalization": "REPOSITORY_CANONICALIZE",
      "projection_shape": "canonical mapping containing schema plus every replay-material semantic field above and excluding only decision_receipt_hash",
      "canonical_json_law": "json.dumps(canonicalize(projection), sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False)",
      "sha256_law": "decision_receipt_hash = lowercase_hex(SHA256(UTF8(canonical_json(decision_receipt_semantic_projection))))",
      "receipt_hash_materialization": "AFTER digest computation, set or validate decision_receipt_hash equal to the independently recomputed digest",
      "all_decision_states_same_hash_law": true,
      "self_reference": "FORBIDDEN",
      "alternate_projection": "FORBIDDEN",
      "caller_selected_projection": "FORBIDDEN",
      "projection_or_hash_mismatch": "INTEGRITY_FAILURE"
    },
    "decision_receipt_hash_contract": {
      "projection_ref": "V3_EMPIRICAL_POSSIBILITY_METABOLISM_DECISION_RECEIPT_SEMANTIC_PROJECTION@1.0.0",
      "validation": "RECOMPUTE_FROM_RECEIPT_SEMANTIC_PROJECTION_AND_REQUIRE_EXACT_MATCH",
      "caller_supplied_hash_authority": false
    }
  },
  "current_selection_law": {
    "authority_and_registry_selection": "EXACT_ACCEPTED_CURRENT_ONLY",
    "caller_selectable_current_registry": false,
    "fuzzy_latest_default_selection": false,
    "historical_replay_may_resolve_exact_old_version": true,
    "currentness_is_not_semantic_truth": true
  }
}
```

# Complete valid-empty registry material

```json
{
  "schema": "V3_EMPIRICAL_POSSIBILITY_METABOLISM_OPERATION_REGISTRY@1.0.0",
  "registry_id": "V3_EMPIRICAL_POSSIBILITY_METABOLISM_OPERATION_REGISTRY",
  "registry_version": "1.0.0",
  "state": "VALID_EMPTY_NO_ACCEPTED_OPERATIONS",
  "authority_id": "V3_EMPIRICAL_POSSIBILITY_METABOLISM_AUTHORITY",
  "authority_version": "1.0.0",
  "entries": [],
  "positive_read_operations": 0,
  "positive_transition_operations": 0,
  "selection_law": {
    "accepted_current_only": true,
    "caller_selectable": false,
    "fuzzy_latest_default_forbidden": true
  }
}
```

---

# Hostile self-checks

These checks exercise the repaired **identity law only** using synthetic non-production material. They do not execute PSEPF or actor state.

### 1. No self-hashing cycle — PASS

Synthetic operation semantic projection digest:

`748c4455ebab94f6f955894ae08d0042d6c692a794e7ca168f95379644b31c72`

The projection is computed without `operation_content_hash`; the derived hash is then validated against that digest.

### 2. Set reordering is canonical — PASS

Reversing all four operation-entry set-like fields recomputed the same digest:

`748c4455ebab94f6f955894ae08d0042d6c692a794e7ca168f95379644b31c72`

Equality:

`true`

Reversing all decision-receipt set-like fields likewise recomputed the same receipt digest:

`bd2538c304879c847e4abc1732b4b1dd9480d4d2afadf39a8842d8e77522cbcd`

Equality:

`true`

### 3. Semantic change changes canonical projection identity — PASS

Changing synthetic operation kind from `TRANSITION_ELIGIBILITY` to `READ_ONLY` changed the digest:

original:

`748c4455ebab94f6f955894ae08d0042d6c692a794e7ca168f95379644b31c72`

changed:

`0cb6ddaca631673b105277aea8e6523d7c646f7cc4cc7db75b7c3556b58bb156`

Changing synthetic receipt decision state from `DENY` to `STALE` changed the digest:

original:

`bd2538c304879c847e4abc1732b4b1dd9480d4d2afadf39a8842d8e77522cbcd`

changed:

`da98d31f2fc2233f5cee60c0b244f2d2be073c11682b629d9e3353fe064687dd`

Under project SHA-256 identity law, any different canonical semantic bytes that somehow produced the same digest would be treated as an integrity/collision failure, never as authority to identify the two semantic objects.

### 4. Derived hash cannot define a second compliant object — PASS

Changing only the supplied synthetic `operation_content_hash` leaves projection bytes/digest unchanged:

projection digest:

`748c4455ebab94f6f955894ae08d0042d6c692a794e7ca168f95379644b31c72`

but the supplied derived hash is then unequal to the independently recomputed digest and is therefore:

`INTEGRITY_FAILURE`.

A caller cannot choose a different hash while preserving compliance.

The same law applies to `decision_receipt_hash`.

### 5. Ordered-vs-set semantics are explicit — PASS

Every top-level v1 collection field is explicitly classified.

All listed set-like fields use repository `canonical_set`.

There are no top-level semantically ordered sequence fields in either v1 projection.

No implementation may reinterpret a set-like field as ordered or introduce an undeclared sequence field.

### 6. No caller-selected projection — PASS

Both projection schema IDs are fixed authority material.

Alternate projections are explicitly forbidden.

Unknown/unlisted fields fail schema validation rather than falling outside the digest by convenience.

### 7. No semantic widening — PASS

The following K2 material is unchanged:

- jurisdiction;
- nine-state decision space and precedence;
- `ALLOW_READ_ONLY` meaning;
- `ELIGIBLE_FOR_NAMED_TRANSITION_RULE` meaning;
- operation kinds;
- positive transition requirements;
- read-only requirements;
- source cardinality;
- measurement-transfer prohibition;
- target-owner separation;
- stochastic/ADP-020 law;
- non-ownership list;
- direct-assignment firewall;
- valid-empty registry;
- current-selection law.

M2 adds identity/replay determinacy only.

---

# Re-audit disposition

The exact two defects proved by L2 are repaired in candidate authority material:

`UNDERDEFINED_SELF_HASHING_OPERATION_ENTRY = CLOSED_BY_EXPLICIT_PROJECTION_AND_POST_DIGEST_REF_VALIDATION`

`UNDEFINED_DECISION_RECEIPT_HASH_PROJECTION = CLOSED_BY_EXPLICIT_FULL_REPLAY_PROJECTION_AND_SHA256_LAW`

No substantive authority-model change was required.

The corrected candidate is ready for an independent hostile re-audit.

## Terminal

`PASS__GT34_M2_METABOLISM_CONTENT_ADDRESSING_REPAIRED__CANDIDATE_READY_FOR_REAUDIT`
