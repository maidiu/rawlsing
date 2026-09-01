# FFIF003 — CANDIDATE TRANSPORT OBJECT

## 1. Ruling on the prompt's candidate schema

`REWRITE_REQUIRED`.

The proposed fields correctly identify endpoints, invariant, transform, estimands, risk sets, nulls, provenance, and supersession. But the schema leaves the most dangerous freedom implicit: **who authorized the correspondence, what maps were allowed, how the chosen map was selected, and whether many alternative maps would have produced the same result.**

A generic `support/uncertainty` field is also too weak. Transport can fail through semantic authority, local support, map identifiability, representation stability, or null performance; these must remain distinguishable.

## 2. Minimal typed object

### Identity / lifecycle

- `transport_claim_id`
- `schema_version`
- `claim_type`
- `transport_status`
- `provenance_refs[]`
- `created_from_local_freeze_refs[]`
- `supersedes[]`
- `superseded_by[]`

### Endpoint identity

- `origin_context_ref`
- `destination_context_ref`
- `origin_local_object_ref`
- `destination_local_object_ref`
- `origin_local_object_hash`
- `destination_local_object_hash`
- `origin_local_estimand_ref`
- `destination_local_estimand_ref`
- `origin_risk_set_ref`
- `destination_risk_set_ref`

Hashes/immutable refs are essential: a transport result cannot remain valid while a local object silently changes.

### Semantic / role authority

- `required_semantic_correspondence_refs[]`
- `required_role_correspondence_refs[]`
- `mapping_authority_refs[]`
- `source_native_replay_refs[]`

`required_role_correspondence_refs[]` must be empty, not guessed, if the claim does not require role equivalence. This prevents a motif claim from silently minting it.

### Transport operator

- `preserved_invariant_id`
- `preservation_predicate`
- `admissible_map_family`
- `candidate_mapping_space_ref`
- `selected_mapping`
- `mapping_selection_rule`
- `mapping_directionality`
- `allowed_transform`
- `forbidden_transform[]`

The selected map without its candidate space and selection rule is not auditable.

### Representation dependencies

- `origin_representation_contract_ref`
- `destination_representation_contract_ref`
- `representation_dependency_refs[]`
- `local_stability_receipts[]`

### Falsification / evidence

- `null_test_refs[]`
- `negative_control_refs[]`
- `alternative_mapping_result_ref`
- `map_identifiability_status`
- `support_status_origin`
- `support_status_destination`
- `decision_rule_ref`
- `decision_receipt_ref`

### Inferential ceiling

- `asserted_recurrence_scope`
- `claim_ceiling`
- `forbidden_inference[]`
- `measurement_portability_status_ref`
- `homology_status`
- `temporal_transport_status`

For this court, `homology_status` must default to `NOT_ADJUDICATED__NOT_EMITTED_BY_TRANSPORT`. `measurement_portability_status_ref` may point only to separate authority; absence cannot be filled by FFIF003.

## 3. Fields from the prompt: dispositions

| prompt candidate | disposition | reason |
|---|---|---|
| `transport_claim_id` | KEEP | stable identity |
| `claim_type` | KEEP | determines proof burden |
| `origin_context` / `destination_context` | KEEP_AS_REFS | context identity must be governed |
| `origin_local_object` / `destination_local_object` | KEEP_AS_IMMUTABLE_REFS_PLUS_HASHES | prevent silent endpoint drift |
| `required_semantic_correspondence_refs` | KEEP | core firewall |
| `preserved_invariant` | KEEP_AS_ID_PLUS_PREDICATE | label alone is underdefined |
| `allowed_transform` | KEEP_PLUS_FORBIDDEN | allowable freedom must be bounded both ways |
| `forbidden_inference` | KEEP | essential claim ceiling |
| `local_estimands` | SPLIT_BY_ENDPOINT | no merged estimand object |
| `local_risk_sets` | SPLIT_BY_ENDPOINT | no merged risk set |
| `support/uncertainty` | REJECT_AS_SINGLE_FIELD | collapses distinct failure modes |
| `representation_dependencies` | KEEP_AS_REFS | transport may be representation-dependent |
| `null_tests` | KEEP_PLUS_NEGATIVE_CONTROLS_AND_MAP_MULTIPLICITY | null target is broader than no association |
| `transport_status` | KEEP | typed adjudication |
| `provenance` | KEEP_AS_REFS | replay |
| `supersession` | KEEP_SPLIT | lifecycle clarity |

## 4. Canonical decision law

A transport object is invalid if any of the following is true:

1. either local endpoint was constructed using the other context to choose its structure;
2. the correspondence was selected by observed target agreement without an exploratory-only flag;
3. `preserved_invariant_id` lacks an exact preservation predicate;
4. the admissible map family is not bounded;
5. local estimand/risk-set refs are absent where the empirical claim depends on them;
6. source-native identities cannot be replayed;
7. a required null/negative control fails;
8. many substantively different admissible maps produce the same signature and no identifiability argument survives;
9. `forbidden_inference` omits measurement equivalence/portability, role equivalence, homology, or temporal equivalence when those are not separately authorized.

## 5. Why this object is not a universal crosswalk

The object is **claim-scoped and pair/direction-scoped**. Different claims over the same two contexts may require different correspondences. That is not inconsistency if the preserved invariants differ.

The architecture must resist deduplicating these into one global cross-context ontology merely for convenience. A reusable mapping can be promoted only by a separate authority process that proves its broader domain.
