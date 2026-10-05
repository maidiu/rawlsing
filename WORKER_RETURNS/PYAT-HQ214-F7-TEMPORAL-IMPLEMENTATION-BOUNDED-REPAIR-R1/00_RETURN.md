# PYAT HQ214 — F7 TEMPORAL COMPARABILITY IMPLEMENTATION BOUNDED REPAIR — R1

**Disposition: `F7_TEMPORAL_IMPLEMENTATION_REPAIR_COMPLETE__READY_FOR_FINAL_HOSTILE_REREVIEW`**

- Code-bearing commit: `a93352512aa9290112bff1eb680c54d43345078f`
- Repair base: `c3db090ff0503963e7914fee740c4b1d17e66cde`
- Commission tip: `50c3a66ca27b30ee2718cf9965cbaafd24a230df`
- Hostile review repaired against: `4478e949eb92ec411c5dec9878bb4f23b5cb2c01`

## First: I confirmed the review was right, objectively

Before changing anything I replayed the five HQ213 bypasses against `caf6644a`
in an isolated copy, using each module's own declared field shape. The
pre-repair implementation minted a directional claim in **all five**:

| HQ213 bypass | Pre-repair result |
|---|---|
| A1 partial registry | `TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED / INCREASE`, provenance `()` |
| A1b full registry | identical — the extra authorities changed nothing |
| A2 unrelated-operation authority | `TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED / INCREASE` |
| CARD three anchors | `TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED / INCREASE` |
| REQ requirements ref absent | `TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED / INCREASE` |

Empty authority provenance on a positive directional claim is exactly the
fail-open the review described. All five now refuse or map to a typed
insufficient-authority outcome.

## All nine repairs

**Repair 1** — every contract-required authority resolves to a positive exact
snapshot or a typed outcome (`ABSENT`, `CONFLICT`, `AUTHORITY_HASH_MISMATCH`,
`AUTHORITY_SCOPE_MISMATCH`, `OUT_OF_SCOPE`), each recorded in provenance. A test
parameterised over all seven authorities proves that dropping any single one
changes the outcome, which is the precise thing HQ213's A1b said was untested.

**Repair 2** — `TEMPORAL_COMPARABILITY` is bound to the exact comparison
operation and the governed use. Both `AUTHORITY_HASH_MISMATCH` and
`AUTHORITY_SCOPE_MISMATCH` are now reachable reasons. Making hash mismatch
genuinely reachable took a real decision: an exact ref naming a known
authority id/version but a different content hash is an immutable-integrity
violation, not mere absence, so it is now diagnosed as such.

**Repair 3** — exactly two anchors, two observations, one observation bound to
each anchor. Three or more refuses pre-receipt. One judgement call worth
flagging: I let *fewer* than two yield the contract's own
`TEMPORAL_INSUFFICIENT_ANCHORS` state rather than raise, because the contract
requires that state to stay reachable and a raise would have made one of the
twelve unreachable. Three-plus refuses, as commissioned.

**Repair 4** — `comparability_requirements_ref` is required, resolved, and its
surfaces drive state selection.

**Repair 5** — the caller can no longer mint a dispositive delta. The
`signed_delta` input is gone; the exact delta is derived as
`later_value - earlier_value` over the bound quantity surface, and a surface
whose measure is not the bound measure refuses. A test asserts `signed_delta` is
no longer even a request field.

**Repair 6** — the receipt carries the accepted 18-field closed contract under
the contract's own names. `delta` is restored as `delta`; `quantity_surface`,
`uncertainty_state`, `intervening_span_state`, `governed_use_id`,
`authority_snapshot_refs`, comparison-operation identity and the canonical
projection rule are all present.

**Repair 7** — `prior_f7_state` drives derivation. `test_witness_prior_map_is_not_asserted_against_itself`
drives five prior states through the producer and requires each mapped value to
actually appear as an observed reason, which is what the tautological version
failed to do.

**Repair 8** — `pair_crosses_source_universes` is deleted. Cross-universe status
is material-derived from the bound per-anchor universe refs, and an exact
positive `SOURCE_EQUIVALENCE` must cover the actual pair — proven by a
narrow-scoped equivalence authority that covers only one universe and is
refused.

**Repair 9** — the backfill guard reads the live frozen
`FORBIDDEN_BACKFILL_TARGET_STATES`. Proven by monkeypatching that surface:
removing `TEMPORAL_NONCOMPARABLE` makes the guard return `False` *and* makes the
producer refuse to mint the noncomparable receipt. A module-local copy would be
unaffected by that patch, which is what makes this a proof rather than a claim.

Plus **`F-NONE-01`**: a missing registry is now a typed absence record, never an
`AttributeError`.

## The three HQ214 adjudications

**A** — no thirteenth state. An ordered basis that cannot yield a lawful delta
raises a typed `TemporalComparabilityInputRefusal` before any receipt. The
vocabulary is still closed at 12, and state 9 is not reused.

**B** — `comparability_status` is `NOT_COMPARABLE` for all nine negative states
and `COMPARABLE` only for the three lawful ones, asserted by driving the states
rather than by inspecting constants.

**C** — no-basis yields `TEMPORAL_ORDER_UNAUTHORIZED` only when no
higher-precedence failure was selected. Where a higher failure exists, that
higher state is emitted and the no-basis observation is retained in
`provenance.no_basis_observation`. The module no longer raises on that
combination, which was HQ213's `F-ORDER-01` interlock.

## Court authenticity

The four vacuous tests HQ213 identified are replaced with real checks:

- The `PUBLIC_OBJECT_FAMILIES` test used an `isinstance` guard that silently
  substituted an empty set. It now asserts the registry is **non-empty** before
  asserting the property, so it can no longer pass vacuously.
- The locality test read a nonexistent class attribute. It now checks
  `isinstance` against the real base class.
- The prior-map test compared a table to itself. It now drives derivation.
- The deadband test caught `Exception`. Replaced with regex-built patterns that
  cannot match their own prose — I hit that trap twice while writing this court,
  first on a docstring listing `pytest.raises(Exception)` and then on the
  assertion string itself.

Focused court **49 → 83**, with named witnesses for all three blocking findings
and every major finding.

## Qualification

| Court | Result |
|---|---|
| Focused court, after | **83 passed**, 0 failed/error/skip/xfail |
| Focused court, run twice | 83 / 83 |
| Regression baseline at HQ211 head | 159 passed |
| Regression after | 159 passed |
| **Failure-ID set delta** | **empty** |
| Combined | **242 passed** |
| Cross-process replay | stable under `PYTHONHASHSEED` 0 / 1 / 12345 |

The regression delta is measured by reverting the implementation to the HQ211
head, running the slice, restoring, and diffing the two failure-ID sets.

**Environment classification, stated exactly:** reproduced on the shared local
qualification interpreter (CPython 3.11.3, `pytest` 9.1.1). I hold no provenance
proving this is the governed F7 qualification environment, so this is
**independently reproduced evidence, not governed certification.**

## Power ceiling unchanged

AST-level: the module's only internal imports are `pre553_empirical_authority`,
`pre553_empirical_objects` and `pre553_source_relations`. No F8 or world import.
The module never mints an `AuthoritySnapshot` and never mints a
`SOURCE_EQUIVALENCE`. No public-object or state-family edit; `relation_state` is
never `typed_state`. Every retained contract residual is left standing — no
architecture was reopened to make any of them disappear.

## Scope

Writes confined to the two commissioned production/test files and
`WORKER_RETURNS/PYAT-HQ214-F7-TEMPORAL-IMPLEMENTATION-BOUNDED-REPAIR-R1/**`.
No architecture reopen, no self-adoption, no source access, no C7, no
actor/person work. I used the single authorized sparse worktree and did not
clone.

Terminal: `HQ214_F7_TEMPORAL_IMPLEMENTATION_REPAIR_RETURNED__FINAL_HOSTILE_REREVIEW_REQUIRED`