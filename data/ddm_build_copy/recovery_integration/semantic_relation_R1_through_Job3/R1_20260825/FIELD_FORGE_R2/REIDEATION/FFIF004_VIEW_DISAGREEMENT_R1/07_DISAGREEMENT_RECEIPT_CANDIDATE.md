# FFIF004 — DISAGREEMENT RECEIPT CANDIDATE

## 1. Ruling

A first-class disagreement object survives, but the earlier generic `CROSS_VIEW_RECEIPT` is tightened into:

`CLAIM_SCOPED_VIEW_COMPARISON_RECEIPT` (`CVCR`).

The word `COMPARISON` is preferred because many lawful receipts terminate in agreement, claim split, known loss, invalidity, or abstention rather than disagreement.

## 2. Minimal schema

```text
CLAIM_SCOPED_VIEW_COMPARISON_RECEIPT {
  receipt_id
  receipt_version

  claim_identity_manifest_ref
  claim_identity_hash
  claim_identity_status

  common_input_manifest_ref
  common_input_hash
  common_semantic_ttar_manifest_ref
  common_semantic_hash
  empirical_unit_risk_set_ref
  estimand_ref
  uncertainty_support_contract_ref

  view_refs[]
  view_family[]
  view_contract_refs[]
  view_output_hashes[]

  target_invariant_bundle_ref
  normalized_assertion_slots[]

  hard_validity_results[]
  view_internal_validity[]
  support_identifiability_status[]

  agreement_components[]
  disagreement_components[]
  undefined_for_view_components[]

  known_loss_explanations[]
  lawful_nuisance_results[]
  holdout_or_replay_results[]

  representation_sensitivity_status
  weaker_object_court_ref
  minimal_sufficient_object_set[]

  resolution_status
  allowed_common_claims[]
  view_specific_claims[]
  forbidden_promotions[]
  interpretive_ceiling

  provenance
  supersedes
  superseded_by
}
```

## 3. Resolution statuses

The court adopts the following finite set provisionally:

- `INVALID_COMMON_INPUT`
- `SEMANTIC_INPUT_DIVERGENCE`
- `CLAIM_SPLIT_REQUIRED`
- `CLAIM_IDENTITY_UNRESOLVED`
- `INVALID_VIEW_REMOVED`
- `INSUFFICIENT_EVIDENCE`
- `NONIDENTIFIABILITY`
- `VIEW_ROBUST_FOR_CLAIM`
- `KNOWN_LOSS_EXPLAINS_DIFFERENCE`
- `REPRESENTATION_DEPENDENCE_RETAINED`
- `WEAKER_OBJECT_SUFFICIENT`
- `MULTI_VIEW_RETENTION_REQUIRED`
- `BOUNDED_NONREDUCIBILITY_CANDIDATE`
- `BOUNDED_NONREDUCIBILITY_SUPPORTED`
- `UNRESOLVED_COMPARISON`

`GENUINE_EMPIRICAL_NONREDUCIBILITY` without a bounded universe/scope is intentionally absent.

## 4. Who may emit it

The CVCR may be emitted only by a comparison/adjudication producer that:

- consumes immutable outputs from independently executed view producers;
- can verify common-input/semantic hashes;
- can execute deterministic normalization and registered validity checks;
- can consume, but not invent, finite semantic adjudications such as claim identity and materiality/loss authority.

A view producer may emit its own `VIEW_CONTRACT_RECEIPT`; it may not self-certify cross-view robustness, representation dependence, or nonreducibility.

## 5. Deterministic computation vs semantic adjudication

Deterministic:

- hash equality;
- exact input/ref comparison;
- assertion-slot normalization under registered mappings;
- tolerance/interval comparison once tolerance is authorized;
- hostile/null metric evaluation;
- invariant coverage matrix;
- weaker-object sufficiency checks that are fully specified;
- provenance/replay verification.

Finite semantic adjudication remains for:

- whether two prose claims are genuinely the same empirical proposition;
- which invariants are constitutive of a bundled claim;
- which loss/materiality tolerances are substantively authorized;
- whether the candidate weaker-object universe is sufficiently closed for a bounded nonreducibility status.

These judgments must be precomputed/banked where repeatable. Runtime may not improvise them from whichever result looks persuasive.

## 6. Defeaters

The receipt is invalid if:

- a compared output cannot be reproduced from its declared common input;
- claim identity was assigned after seeing which result was preferred;
- view contracts changed after comparison;
- known semantic differences were hidden inside preprocessing;
- the receipt treats `UNDEFINED_FOR_VIEW` as `FALSE`;
- it counts methods rather than adjudicating invariants;
- nonreducibility is emitted without the weaker-object and closure courts.

## 7. Replay

Replay requires:

1. exact common input and TTAR manifests;
2. immutable view output refs and contracts;
3. comparator code/version;
4. claim-normalization registry;
5. uncertainty/tolerance authority;
6. validity and nuisance fixture refs;
7. weaker-object universe and sufficiency rules;
8. deterministic output hashes;
9. any manual semantic adjudication receipts.

A later superseding receipt must preserve the prior receipt and state exactly which input, authority, view, or decision rule changed.

## 8. Consumers

Lawful consumers include:

- future FFX002 execution;
- representation architecture synthesis;
- downstream structural-admission courts through the restricted interface in `11`;
- PRE-V3 actor-independent packet design where a consumer needs to know whether an empirical pattern is view-robust, view-sensitive, or representation-specific.

The receipt itself emits no sociology.
