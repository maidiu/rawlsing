# FFIF005 — MAP FAMILY AND SELECTION CONTRACT

## 1. Mapping-plan block

The FFIF003 transport contract should embed the following nonauthoritative plan block:

```text
CLAIM_SCOPED_MAPPING_PLAN {
  mapping_plan_id
  transport_claim_ref
  claim_identity_hash
  origin_context_ref
  destination_context_ref
  origin_local_object_refs[]
  destination_local_object_refs[]
  local_object_hashes[]
  local_invariant_refs[]

  candidate_generation_log_ref
  candidate_edge_refs[]
  edge_authority_refs[]
  rejected_edge_refs[]

  correspondence_types[]
  admissible_map_family_spec
  admissible_map_family_cardinality_or_bound
  map_equivalence_class_rule
  directionality
  partiality_and_unmapped_policy
  map_complexity_budget

  selection_feature_manifest
  selection_rule
  tie_rule
  unresolved_rule
  selected_map_or_retained_set

  target_outcome_firewall_ref
  forbidden_mapping_evidence_fields[]
  alternative_map_plan
  null_family_ref
  multiplicity_decision_rule

  TTAR_refs[]
  PRA_or_role_refs[]
  risk_set_estimand_refs[]
  allowed_invariants[]
  forbidden_inferences[]
  validity_and_invalidation
  provenance
  supersession
  mapping_plan_hash
}
```

This object records authority; it does not supply authority.

## 2. Exact local-object identity minimum

A map endpoint is not the label `education`, `trust`, `working class`, `religious group`, or any other prose domain. Each endpoint must bind:

- `local_context_ref` — exact source/release/wave/country/form/module/split scope required by the object;
- `local_common_semantic_manifest_ref/hash`;
- `local_view_ref` and `representation_contract_ref`;
- `local_object_ref` and immutable `local_object_hash`;
- `local_claim_role` / exact invariant-component ref;
- source-native replay/ancestry refs;
- ordered TTAR ancestry for every derived semantic state, or exact explicit `NONE`;
- PRA/other role refs when the object is mapped by analytic role;
- local risk-set and estimand refs where the invariant is empirical/respondent-bearing;
- local support/uncertainty and representation-status refs where claim-relevant.

The minimum is claim-relative but none of context, object identity/hash, claim role/invariant, semantic ancestry, and representation provenance may be replaced by a display label. Risk-set/estimand may be explicitly `NOT_APPLICABLE` only for a purely source-topology correspondence.

## 3. Map-shape decisions

### `ONE_UNIQUE_MAP`

Use only when independent authority plus the frozen rule leaves one materially distinct map. Exact identity is the cleanest case. A unique outcome optimum is not a unique authorized map.

### `FINITE_COMPETING_MAP_SET`

Use when several maps pass edge/family authority and no independent selector distinguishes them. Retain all maps. A transport claim may survive only as map-robust, map-indexed, or unresolved.

### `PARTIAL_MAP`

Use when only a strict endpoint subset has authorized correspondence. Freeze the reduced domain before testing. Unmapped objects remain explicit; they are not missing values and cannot be imputed into the common signature.

### `ONE_TO_MANY_CORRESPONDENCE`

Use when one exact role/object lawfully corresponds to a finite destination set and the preservation predicate is explicitly set-valued. It must not duplicate one observation into several independent measurements or count the destination set as repeated evidence.

### `MANY_TO_ONE_CORRESPONDENCE`

Use only in one of two typed forms:

- `SET_VALUED_NONCOLLAPSING`: local members remain distinct and the predicate consumes the full set;
- `SEMANTIC_COARSENING`: distinctions are collapsed, requiring TTAR with explicit loss and ancestry.

If downstream computation cannot distinguish these forms, fail closed to `TTAR_REQUIRED`.

### `ORDER_PRESERVING_MAP_FAMILY`

Requires independently lawful local orders, direction/tie/coarsening rules, and claim-scoped transport authority. A monotone family may remain large; order alone does not select one map.

### `ROLE_CONSTRAINED_PERMUTATION_FAMILY`

Every candidate edge must already be role-authorized. A coarse role label such as `identity`, `trust`, or `economic position` is not sufficient. The family is used both as admissible alternatives and as the main semantic permutation null.

### `NO_MAP`

Use when no authorized edge family exists, endpoint role authority is missing, the family is unbounded, or the only selector is target outcome fit.

## 4. Selection-rule hierarchy

Strongest to weakest:

1. exact identity/version bridge;
2. unique independently adjudicated semantic relation;
3. deterministic rule over authorized outcome-independent features with no tie;
4. finite manual adjudication using a sealed evidence packet;
5. retain finite competing set;
6. `UNRESOLVED` / `NO_AUTHORIZED_MAP`.

Selection by recurrence score is absent.

## 5. Tie and abstention law

If the frozen rule ties:

- do not add an unregistered tiebreaker;
- retain the tied set;
- test map robustness/multiplicity;
- return `NO_IDENTIFIABLE_MAP` if the result depends on the tie;
- allow a weaker map-invariant claim only if independently defined and supported.

## 6. Directionality

Partial and coarsening maps are usually directional. A->B success does not license B->A. Reverse transport requires its own claim, TTAR scope, family, selection rule, and falsification.

## 7. Validity conditions

The plan is invalid if:

- local endpoints changed after plan freeze;
- any map edge lacks exact authority;
- `H` is not finite/bounded or replayably generated;
- the selected map is not in `H`;
- the selection rule consumes prohibited target evidence;
- ties are silently resolved;
- many-to-one coarsening lacks TTAR;
- PRA/role authority is assumed from the map;
- alternative maps or nulls are omitted where multiplicity exists;
- the claim ceiling omits portability/PRA/homology prohibitions.
