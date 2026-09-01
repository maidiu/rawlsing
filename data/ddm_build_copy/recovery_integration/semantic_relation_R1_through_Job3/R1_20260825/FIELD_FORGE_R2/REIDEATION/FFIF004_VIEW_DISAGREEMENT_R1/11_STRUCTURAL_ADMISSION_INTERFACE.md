# FFIF004 — STRUCTURAL ADMISSION INTERFACE

## 1. Purpose

A later structural-admission court should not consume a representation output as if its coordinates/classes/motifs were already sociological facts.

It should consume a typed empirical comparison packet that states how representation-dependent the pattern is and what invariants actually survived.

This is safer than a single “best representation,” but only if the status names remain narrow.

## 2. Allowed interface statuses

### `VIEW_ROBUST_PATTERN`

Encodes:

> Multiple independently admissible views capable of answering the same frozen empirical assertion agree within tolerance.

Does not encode:

> the pattern is theory-free, causal, or ontologically privileged.

A later court may treat this as stronger representation-robust empirical premise, not as automatic structural admission.

### `VIEW_SENSITIVE_PATTERN`

Encodes:

> The same lawful empirical claim changes materially across admissible representations.

A structural court must preserve the sensitivity and may not choose the theoretically convenient view without additional empirical authority.

### `MULTI_VIEW_SUPPORTED_PATTERN`

Encodes:

> The frozen bundled claim requires a minimal nonredundant set of admitted views/objects to preserve all required empirical invariants.

This is stronger than mere sensitivity but weaker than nonreducibility unless the full proof burden passes.

### `REPRESENTATION_SPECIFIC_ONLY`

Encodes:

> The pattern is lawful inside one representation contract but is undefined, untested, or not preserved elsewhere.

A later court may use it only with the representation dependency explicitly attached.

### `BOUNDED_NONREDUCIBILITY_SUPPORTED`

Encodes only:

> Within the declared claim/input/loss/object universe, no lawful single weaker object or transform preserves the full required invariant bundle.

It does not authorize mystical “contradictory social reality” language.

### `UNRESOLVED`

Encodes insufficient evidence, nonidentifiability, ambiguous claim identity, unclosed weaker-object universe, or other unresolved comparison.

A structural court must abstain from using the unresolved component as a positive premise.

## 3. Required packet fields

A structural-admission consumer should receive, at minimum:

```text
STRUCTURAL_ADMISSION_EMPIRICAL_INTERFACE {
  empirical_pattern_refs[]
  claim_identity_ref
  common_input_ref
  target_invariant_bundle_ref
  representation_status
  admitted_view_refs[]
  invalid_or_excluded_view_refs[]
  agreement_components[]
  sensitivity_components[]
  known_losses[]
  uncertainty_support
  locality_conditioning_scope
  weaker_object_status
  bounded_nonreducibility_scope_if_any
  provenance
  forbidden_promotions[]
}
```

## 4. What later structural admission may consume

It may consume empirical premises such as:

- exact configuration existence/support;
- stable conditional redistribution;
- local neighborhood/order relation;
- explicit measurement/social relation topology where the relation is governed;
- bounded motif recurrence;
- claim-scoped transport signature;
- whether those premises are view-robust, view-sensitive, or multi-view necessary;
- uncertainty, support, locality, and loss.

## 5. What it may not inherit automatically

The interface may not directly emit or silently imply:

- `FIELD`;
- `CAPITAL`;
- `CLASS`;
- `HEGEMONY`;
- `HOMOLOGY`;
- `PRESSURE` as mechanism;
- `MECHANISM`;
- `PERSONALITY`;
- `WORLDVIEW`;
- actor motive/identity/psyche.

A geometry axis label, latent class label, motif nickname, or nonreducibility status is not structural-admission authority.

## 6. Attack on `VIEW_ROBUST_PATTERN`

Cross-view agreement can be counterfeit if all views share one upstream semantic transformation, source artifact, or risk-set error.

Therefore `VIEW_ROBUST_PATTERN` requires the hard common-input/semantic validity gates to have passed. It means robustness **conditional on the frozen governed input**, not independence from all upstream ontology.

## 7. Attack on `MULTI_VIEW_SUPPORTED_PATTERN`

Two views answering different claims do not become stronger evidence by being combined.

The status requires one bundled claim whose invariant components are explicitly co-required. Otherwise the correct output is simply multiple separate empirical premises.

## 8. Attack on nonreducibility consumption

A structural court may not reason:

> This empirical object is nonreducible, therefore society is contradictory/dialectical/field-like.

The only lawful inference is:

> The current bounded empirical claim cannot be represented sufficiently by one admitted weaker object without loss.

Any theoretical interpretation requires independent admission criteria.

## 9. Consumer-side duty

A structural court must state which empirical assertion(s) from the interface its structural proposition depends on and what would happen if the comparison status changed from robust to view-sensitive or unresolved.

If the structural proposition survives only by silently discarding an inconvenient valid view, the admission fails.

## 10. Safer interface conclusion

Yes: typed view-robust/view-sensitive/multi-view statuses are safer inputs than one privileged representation output.

But the safety comes from preserving disagreement, loss, and uncertainty—not from turning “multi-view” into a new badge of truth.
