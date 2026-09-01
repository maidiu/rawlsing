# FFIF001 — CROSS-VIEW CONSISTENCY AND DISAGREEMENT RULES

## 1. Core law

Multiple views do not vote on ontology.

`N_METHODS_AGREE != STRUCTURAL_TRUTH`

and:

`N_METHODS_DISAGREE != RELATIVISM`.

Every disagreement is first decomposed into input, invariant, method, evidence, and claim layers.

## 2. Common-input gate

Two views may be compared only when their comparison receipt proves equality or explicitly typed difference in:
- observation-substrate version/hash;
- empirical-unit universe;
- measurement exposure/risk set;
- source/value semantics;
- estimand/weight target;
- train/design/holdout partition where relevant;
- ancestry exclusions.

If these differ unintentionally:
`DISAGREEMENT_INVALID__NONCOMMON_INPUT`.

## 3. Invariant-contract gate

Each view declares:
- invariants it must preserve exactly;
- invariants it approximates;
- invariants outside its claim;
- known losses.

A view failing a hard invariant is:
`VIEW_INVALID_FOR_CLAIM`.

This is not “one perspective among others.”

## 4. Disagreement classes

### D1 — INVALID VIEW
One view violates its own admissibility/falsifier/invariant contract.

Examples:
- geometry joins disconnected exposure components;
- atlas deletes rare observed facts;
- graph treats unresolved nonedge as independence;
- latent model unstable/nonidentifiable under its preregistered rule.

Action: exclude that view for the claim.

### D2 — DIFFERENT INVARIANTS PRESERVED
Both views are valid but answer different aspects.

Example:
- exact configuration shows a rare contradictory branch;
- geometry accurately preserves majority neighborhoods while losing that branch.

Action: return `REPRESENTATION_TRADEOFF`; do not demand convergence.

### D3 — CLAIM EXCEEDS EVIDENCE
All relevant views are unstable, sparse, noncomposable, or representation-sensitive beyond tolerance.

Action: `ABSTAIN__CLAIM_EXCEEDS_AVAILABLE_EVIDENCE`.

### D4 — GENUINE NONREDUCIBILITY CANDIDATE
Two or more valid views over the same inputs preserve their required invariants yet expose materially different structures that cannot be transformed into one another without violating a hard invariant.

Action: preserve both and issue `NONREDUCIBLE_STRUCTURE_CANDIDATE`. This is an empirical architecture result, not metaphysical proof that society has multiple ontologies.

### D5 — REPRESENTATION-SENSITIVE BUT DECISION-IRRELEVANT
Views differ numerically but downstream frozen query answers remain within tolerance.

Action: report sensitivity, permit weaker common claim.

### D6 — CROSS-CONTEXT TRANSPORT FAILURE
A local view is valid in each context but the mapping/alignment needed for comparison is not authorized or stable.

Action: retain local results; forbid recurrence/homology/common-axis claim.

## 5. Robustness levels

Prospective vocabulary:
- `SOURCE_FACT_ROBUST`: exact observation/topology preserved independent of social representation.
- `VIEW_INTERNAL_ROBUST`: stable within one view family under lawful nuisance variants.
- `CROSS_VIEW_QUERY_ROBUST`: multiple admitted views return materially equivalent answer to a frozen query.
- `REPRESENTATION_DEPENDENT`: valid views return materially different answers.
- `NOT_IDENTIFIED`: evidence/admissibility cannot distinguish.

Never promote `CROSS_VIEW_QUERY_ROBUST` to “the structure is objectively X” without separate structural admission.

## 6. Disagreement receipt

```text
CROSS_VIEW_RECEIPT {
  claim_id
  common_input_hash
  view_ids[]
  invariant_contracts[]
  hard_gate_results[]
  comparable_outputs[]
  quantitative_differences[]
  information_losses[]
  representation_sensitivity
  disagreement_class
  allowed_common_claim
  view_specific_claims[]
  forbidden_promotions[]
  provenance
}
```

## 7. Atlas vs geometry examples

- Atlas preserves exact rare conjunction; geometry cannot reconstruct it: `D2`, unless rare preservation was a hard geometry requirement for that claim, in which case geometry is `D1`.
- Geometry yields stable neighborhoods that improve heldout query compression; atlas has no intrinsic neighborhood: `D2`, geometry earns incremental value.
- Geometry rotates under block clone while atlas substantive facts remain invariant: geometry `D1` for robust structural claim.
- Atlas motif inventory oscillates with support threshold while geometry neighborhood query remains stable: atlas compact motif view `D1` for motif claim; exact atlas fact floor remains valid.
- Both change radically under estimand/weight target: not disagreement until target is frozen.

## 8. No reconciliation by semantic storytelling

Forbidden resolution:
“Geometry's D1 looks like class, therefore it explains the atlas.”

Forbidden resolution:
“The atlas is exact, therefore geometric gradient is merely artifact.”

Resolution must occur through explicit transformation, invariant, holdout, and falsifier evidence.

## 9. Structural interpretation boundary

Only after the receipt may a later competent court ask whether an admitted empirical pattern supports stronger language. This court does not call axes classes, clusters fields, associations pressure mechanisms, or motifs ideologies.
