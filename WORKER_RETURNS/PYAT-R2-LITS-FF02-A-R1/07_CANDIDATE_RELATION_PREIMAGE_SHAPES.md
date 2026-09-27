# FF02-A — Documentary candidate relation preimage shapes

Every shape below is documentary only:

`CANDIDATE_PENDING_HQ_ADOPTION__NOT_CURRENT_STRUCTURAL_TRUTH`

No object ID, authority hash or current-selection receipt is minted here.

## Common immutable envelope

```text
status = CANDIDATE_PENDING_HQ_ADOPTION__NOT_CURRENT_STRUCTURAL_TRUTH
producer_candidate_id/hash = exact current PRE553 candidate
producer_query_refs = exact current EmpiricalQuerySpec refs by role
producer_predicate_refs = exact current EmpiricalPredicate refs by role
producer_fact_refs = exact current EmpiricalFact refs by role
empirical_universe_ref = EmpiricalUniverse@1.0.0:urn:rawlsing:pre553:EmpiricalUniverse:sha256:83af05f5891e8accc18eeb99e5a1fd99242a509d9a38276004675c0e26be8080#83af05f5891e8accc18eeb99e5a1fd99242a509d9a38276004675c0e26be8080
risk_set_ref = RISK_SET:urn:rawlsing:pre553:as2b:lits1-q301-bounded:sha256:31f7ec452d8d75eebf7963d1ce1715b38f5329a31c757d9088819c99f5d4db45#31f7ec452d8d75eebf7963d1ce1715b38f5329a31c757d9088819c99f5d4db45
measure_basis_ref = AS3_QUERY_MEASURE_BASIS:urn:rawlsing:pre553:as3:measure-raw:sha256:25e90c83f1f226ce7eb6a337018635b28427ae90446f3e4d825a1788c43336ec#25e90c83f1f226ce7eb6a337018635b28427ae90446f3e4d825a1788c43336ec
source_sha256 = 7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09
c11_release_ref = C11LogicalRelease:LITS1-I02-F02-SUCCESSOR-7cac43e2ca5b31cb-bf305bf3f169d669#192926fabd9c9c3d40e43b1d7705ca2bcfe7f8d06e286be26d4b886d436df43f
producer_authority_closure_digest = aad04e65baf1dda42f2e820efddf7aee0fa8f36eb0a0a8cbcb5cc4ebb4ecd5d0
candidate_replay_ref = exact row-specific PRE553_I05_DISCOVERY_REPLAY
frontier_replay_ref = PRE553_I05_FRONTIER_REPLAY:urn:rawlsing:pre553:i05:frontier-replay:sha256:dbd18f3c3393256b2062061f2096adcbf4c44605ad5b592b75d59824c0428640#dbd18f3c3393256b2062061f2096adcbf4c44605ad5b592b75d59824c0428640
information_loss = NONE__REFERENCE_PRESERVING
producer_semantics_reowned = false
structural_target_use_permission = PENDING_HQ_ADOPTION
actor_person_v3_effect = NONE
```

## EXACT_SUPPORT_RELATION

Additional semantic material:
```text
relation_semantics = EXACT_SUPPORT_WITHIN_FROZEN_SOURCE_SCOPE
participant commitment = exact producer target/state only
positive premise = current TARGET_CELL_SUPPORTED validator
inter_variable_relation = NOT_ASSERTED
```

## EXACT_DEPENDENCE_RELATION

```text
relation_semantics = EXACT_NON_DIRECTIONAL_DEPENDENCE_WITHIN_FROZEN_SCOPE
premises = exact JOINT + MARGINAL_0 + MARGINAL_1 facts
validator = JOINT_NOT_PRODUCT_OF_MARGINALS
directionality = NONE
causal_semantics = NONE
```

## EXACT_CONDITIONED_REDISTRIBUTION_DIFFERENCE_RELATION

```text
relation_semantics = EXACT_CONDITIONED_REDISTRIBUTION_DIFFERENCE_WITHIN_FROZEN_SCOPE
premises = exact CONDITION + BASELINE facts
validator = DISTRIBUTION_DIFFERS_FROM_BASELINE
conditioning_semantics = producer-owned exact query/predicate refs
causal_effect = NOT_ASSERTED
mechanism = NOT_ASSERTED
```

## EXACT_SOURCE_LOCAL_JOINT_RELATION

```text
relation_semantics = EXACT_SOURCE_LOCAL_JOINT_CELL_SUPPORT
premise = exact BASE joint fact
validator = TARGET_CELL_SUPPORTED
joint_identity = producer-owned target topology
dependence = NOT_ASSERTED
branch_set = NOT_ASSERTED
order_metric_neighborhood_topology = NOT_ASSERTED_BEYOND_PRODUCER_IDENTITY
```

## VALID_EMPTY typed refusal

```text
empirical_state = VALID_EMPTY
requested_positive_relation = CONDITIONAL_REVERSAL
positive_relation = NONE
zero_value_substitution = FORBIDDEN
absence_beyond_exact_query = NOT_ASSERTED
counterfactual = NOT_ASSERTED
```
