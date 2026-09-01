# FFIF007 — WEAKER-OBJECT PARTIAL ORDER

## 1. No scalar strength score

Information volume, model complexity, compression, compute, and semantic commitment do not lie on one axis. An exact table can be byte-heavy but assumption-light; a tiny latent model can be compressed but commitment-heavy.

Therefore `OBJECT_STRENGTH_SCORE` is rejected.

## 2. Three relations, not one confused relation

### A. Claim capability

`CAP_C(A)` is the set of constitutive assertion slots A can answer within CITC, including whether each answer is primitive, lawfully derived, uncertainty-only, or undefined.

### B. Commitment preorder

Let `K_C(A)` be A's typed commitment vector restricted to claim-relevant coordinates:

- semantic identity/equivalence/order/group/transport;
- representational metric/adjacency/neighborhood/mixture/motif/smoothing;
- inferential model/generalization/prior/error assumptions;
- authority and stronger-object query dependencies.

`A NO_STRONGER_COMMITMENT_THAN_C B` only when A is no stronger on every comparable coordinate. Any crossed coordinate yields `INCOMPARABLE_COMMITMENTS_FOR_C`.

Information retained/lost is judged through CAP/CITC, not forced into this commitment vector. Engineering cost is separate.

### C. Claim-relative weak dominance

`A <=_C B` iff:

1. A and B are valid AOS members under the same comparison key;
2. every claim-constitutive assertion B can lawfully satisfy is also satisfied by A within CITC, and A is itself claim-sufficient where dominance is used for selection;
3. A requires no stronger claim-relevant semantic, representational, inferential, or authority commitment than B;
4. A does not consult B or an excluded stronger object at query time.

`A <_C B` requires at least one strictly weaker commitment coordinate.

This is a partial relation. Noncomparability is expected and informative.

## 3. Attack on the candidate formulation

The prompt's candidate—“A can answer every claim-constitutive assertion B answers while requiring no stronger assumptions”—is substantially correct but incomplete unless it also binds:

- identical comparison key and CITC;
- validity/admissibility;
- uncertainty behavior;
- no hidden stronger-view query dependency;
- typed noncomparability rather than a forced ranking.

## 4. Exact classifications

- `STRICTLY_SUFFICIENT_WEAKER_OBJECT`: A <_C B and A is claim-sufficient.
- `CLAIM_EQUIVALENT_OBJECTS`: A and B have equivalent claim interface and commitment vector; method/implementation utility may choose.
- `NONCOMPARABLE_OBJECTS`: crossed commitments or distinct nonredundant invariant interfaces.
- `STRICTLY_DOMINATED_OBJECT`: another included AOS is strictly sufficient and weaker.
- `ADDS_NONREDUNDANT_INVARIANT`: object supplies a constitutive slot no retained comparator supplies.
- `ADDS_ONLY_UTILITY`: no unique constitutive slot; may improve cost/prediction only after empirical sufficiency.
- `INVALID_FOR_CLAIM`: failed admissibility or hard invariant.
- `UNRESOLVED_COMMITMENT_ORDER`: no authority-valid relation can be frozen.

## 5. Computational cost

`COMPUTATIONALLY_CHEAPER != EMPIRICALLY_WEAKER`.

After minimal empirical sets are found, storage/latency/compute/maintainability may select among claim-equivalent or nondominated sufficient choices. The engineering decision is a separate field and cannot rewrite the empirical order.

## 6. Examples

- A direct `P(D|C)` object strictly dominates geometry for a claim requiring only that conditional distribution, if both are valid and the direct object adds no stronger assumptions.
- An ordinal neighborhood relation can dominate cardinal coordinates for an order-only claim.
- Exact configurations and cardinal geometry are often incomparable: the former retains more native conjunction information but the latter imports metric structure.
- A fast predictive latent model does not dominate a direct conditional object merely because its score is higher; predictive utility is not weaker commitment.

