# FFIF006 — WEAKER-OBJECT SUFFICIENCY CONTRACT

## Claim-relative weakness

There is no global order in which a conditional table is always weaker than geometry, or an atlas is always stronger than a rank relation.

`WEAKER(W1,W2,C)` is defined only for a frozen claim `C` and its tolerance contract.

## Commitment vector

Each candidate declares a non-scalar commitment vector:

- `semantic_commitments`: new identity, equivalence, order, partition, transport, or role assertions;
- `representation_commitments`: metric, adjacency, neighborhood, latent-class, mixture, motif, smoothing, or model assumptions;
- `information_retained_and_lost`: typed invariant coverage and loss dimensions;
- `inferential_commitments`: estimation, generalization, priors, link/error assumptions;
- `query_commitments`: which assertion slots are primitive, derived, undefined, or require another object at query time;
- `derived_object_count_and_dependencies`;
- `storage_compute_latency`: engineering dimensions only.

Bytes, dimensionality, and compute do not define epistemic weakness.

## Sufficiency predicate

Candidate `W` is `CLAIM_SUFFICIENT_FOR_C` iff:

1. `W` is empirically admissible from the exact common semantic input;
2. every atomic slot/invariant required by `C` is answerable or returns the exact authorized uncertainty state;
3. every bounded loss is within the frozen contract;
4. no hard-zero invariant fails;
5. `W` does not consult an excluded stronger view at query time;
6. `W` imports no authority stronger than the CIM permits;
7. replay is exact or governed by the frozen numerical tolerance.

## Partial-order rule

For two claim-sufficient candidates:

- `STRICTLY_WEAKER_FOR_C`: W1 has no stronger substantive/representational commitment on any claim-relevant dimension and is strictly weaker on at least one;
- `COMMITMENT_EQUIVALENT_FOR_C`: relevant commitments and invariant coverage are equivalent;
- `INCOMPARABLE_COMMITMENTS_FOR_C`: each is weaker on different dimensions;
- `NOT_CLAIM_SUFFICIENT`: candidate exits the dominance court.

Engineering cost is used only after this classification. A cheaper but claim-insufficient object does not dominate.

## Minimal sufficient set

If no single object is sufficient, test preregistered combinations. A set is minimal only when:

- its union covers every required invariant;
- removal of any member breaks sufficiency;
- no lawful transform of one member makes another redundant;
- no single object in the finite candidate universe is sufficient;
- no retained member is present only for downstream prestige or visual interpretation.

Possible outputs:

- `SINGLE_WEAKER_OBJECT_SUFFICIENT`
- `SINGLE_STRONGER_OBJECT_REQUIRED`
- `MULTI_VIEW_MINIMAL_SET_REQUIRED`
- `NO_ADMITTED_OBJECT_SET_SUFFICIENT`
- `UNRESOLVED__COMMITMENT_ORDER`
- `UNRESOLVED__TOLERANCE_AUTHORITY`

## Loss-budget interaction

Every sufficiency cell points to one invariant-tolerance row. A candidate cannot be called sufficient by averaging across rows. Known claim-irrelevant loss may be accepted; loss of a claim-required invariant either exceeds tolerance or invalidates the candidate.

## Bounded nonreducibility

`MULTI_VIEW_MINIMAL_SET_REQUIRED` is necessary but insufficient for bounded nonreducibility. FFIF004's transform tests, nuisance/holdout tests, finite-universe closure, nonredundancy proof, and supersession clause still apply.

## Receipt

```text
WEAKER_OBJECT_COURT_RECEIPT {
  comparison_claim_hash
  invariant_tolerance_contract_hash
  candidate_universe_ref_hash
  candidate_commitment_vectors[]
  invariant_sufficiency_matrix
  transform_test_refs[]
  partial_order_relations[]
  minimal_sufficient_object_or_set[]
  engineering_selection_if_any
  unresolved_judgments[]
  forbidden_promotions[]
  provenance
  supersession
}
```

