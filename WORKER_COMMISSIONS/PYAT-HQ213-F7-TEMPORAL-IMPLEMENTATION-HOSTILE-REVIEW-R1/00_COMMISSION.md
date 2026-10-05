# PYAT HQ213 — F7 TEMPORAL COMPARABILITY IMPLEMENTATION HOSTILE REVIEW — R1

**STATUS:** NEW — NEEDS LAUNCH  
**AGENT:** DeepSeek Harness independent hostile reviewer  
**MODEL / INTELLIGENCE:** **DeepSeek V4.1 Flash**  
**BRANCH:** `agent/reviewer-pyat-hq213-f7-temporal-implementation-r1`  
**EXACT CANDIDATE BASE:** `c3db090ff0503963e7914fee740c4b1d17e66cde`  
**CODE-BEARING COMMIT:** `caf6644a6033fb27c981ff0deb8d6e1b7d3d824e`  
**CANDIDATE:** `agent/rabochii-pyat-hq211-f7-implementation-r1 @ c3db090ff0503963e7914fee740c4b1d17e66cde`  
**ACCEPTED CONTRACT:** `c57a96897788108db7b194e4e51691d1ca8ab729`  
**REVIEW MODE:** READ-ONLY / HOSTILE / NO REPAIR  
**CHECKOUT:** SPARSE_REQUIRED

Use the shared-store sparse-worktree law. **DO NOT CLONE.**

## Mission

Hostile-review the first production implementation of the accepted F7 TEMPORAL_COMPARABILITY contract.

This candidate adds a new central authority kind and a temporal relation producer. It is not adoptable without independent hostile acceptance.

Do not repair, merge, or self-adopt.

## Mandatory attacks

1. **Registry minimality**
   Verify exactly one new `AUTHORITY_KINDS` member and exactly one matching `AUTHORITY_KIND_CEILINGS` entry. No sibling kind, public-object family, state-family widening, or unrelated authority change.

2. **Contract fidelity**
   Compare implementation line-by-line against the accepted documentary contract at `c57a968...`.
   Verify all 12 relation states, exact precedence, scalar reason selection, cross-field invariants, exact-zero NO_AUTHORIZED_CHANGE, typed no-basis refusal, and prior-state mappings.

3. **No-basis uniqueness**
   Prove `TEMPORAL_ORDER_UNAUTHORIZED` is reachable only through `ORDER_UNKNOWN_NONCOMPARABLE / NO_PERMITTED_ORDER_BASIS_APPLIES`.
   Missing basis authority must not collapse into the same state.

4. **Directional claim law**
   Attempt to obtain INCREASE/DECREASE/NO_AUTHORIZED_CHANGE without:
   - COMPARABLE;
   - ORDERED_RELATION_AUTHORIZED;
   - direction-permitting basis;
   - exact delta;
   - all required authorities positive.
   Every bypass must fail closed.

5. **Exact-zero law**
   Attack with small non-zero values, negative zero representations, decimal/string variants, NaN/inf-like values if structurally accepted, and malformed numeric payloads. No deadband/tolerance may emerge.

6. **Cross-universe noncollapse**
   Verify source-relation owner independently resolves SOURCE_EQUIVALENCE and temporal module only consumes its exact positive result.
   Temporal code must not mint/equate sources or bypass missing equivalence.

7. **Power ceiling**
   Search production and public API for any F8 consumption/conditioning, source selection, interpolation, trajectory/trend, rupture production, currentness, scalar pressure, causal/event semantics, pooling, estimand composition, or actor/person inference.

8. **Receipt representation**
   Verify receipt remains module-local/content-addressed and is not inserted into `PUBLIC_OBJECT_FAMILIES`, `STATE_FAMILIES`, or `CanonicalSemanticObject.typed_state`.

9. **Backfill noncollapse**
   Verify literal `TEMPORAL_NONCOMPARABLE` remains forbidden as a backfill target and no temporal receipt/pair can be upgraded by generic backfill.

10. **Typed residual**
   Candidate escalates `ORDERED_AUTHORIZED_BASIS_WITHOUT_SUPPLIED_DELTA`.
   Determine whether this is a truthful fail-closed residual consistent with contract, or evidence of an incomplete implementation. Do not wave it away because the focused court is green.

11. **Court authenticity**
   Independently reproduce the claimed 49 focused + 159 regression = 208 green surface where possible.
   Attack state reachability tests, multi-failure precedence, reason determinism, probe-only no-receipt, partial-order direction refusal, cross-universe positive/refusal, and replay identity for tautology/self-description.

12. **Environment classification**
   Preserve honest evidence classification. No reconstructed environment may be called governed unless provenance proves it.

## Required return

Write only under:
`WORKER_RETURNS/PYAT-HQ213-F7-TEMPORAL-IMPLEMENTATION-HOSTILE-REVIEW-R1/`

Required:
- `00_REVIEW.md`
- `01_AUTHORITY_AND_CONTRACT_FIDELITY_ATTACK.json`
- `02_STATE_DIRECTION_AND_EXACT_ZERO_ATTACK.json`
- `03_NONCOLLAPSE_POWER_AND_COURT_ATTACK.json`
- `04_FINAL_DISPOSITION.json`

Allowed dispositions:
- `ACCEPT_F7_TEMPORAL_COMPARABILITY_IMPLEMENTATION__READY_FOR_HQ_ADOPTION`
- `F7_TEMPORAL_IMPLEMENTATION_PARTIAL__BOUNDED_REPAIR_REQUIRED`
- `F7_TEMPORAL_IMPLEMENTATION_AUTHORITY_OVERREACH`
- `F7_TEMPORAL_IMPLEMENTATION_ARCHITECTURE_CONFLICT`
- `F7_REVIEW_BLOCKED_BY_MISSING_EXACT_EVIDENCE`

Commit, push only this branch, re-fetch/verify exact remote HEAD, report exact pushed SHA.

Terminal:
`HQ213_F7_TEMPORAL_IMPLEMENTATION_REVIEW_RETURNED__HQ_DECISION_REQUIRED`
