# PYAT HQ215 — F7 TEMPORAL COMPARABILITY FINAL HOSTILE REREVIEW — R1

**Disposition:** `F7_FINAL_REPAIR_PARTIAL__NAMED_DEFECT`  
**Terminal:** `HQ215_F7_FINAL_REREVIEW_RETURNED__HQ_DECISION_REQUIRED`

## Exact frame

- Review branch: `agent/reviewer-pyat-hq215-f7-final-rereview-r1`
- Commission tip: `4a5094e8ca32efaedc1cc9af9329393f3bc9674c`
- Exact candidate base: `684a1b202767ad393bcead671a7ad239dabcdb14`
- Code-bearing commit: `a93352512aa9290112bff1eb680c54d43345078f`
- Accepted contract: `c57a96897788108db7b194e4e51691d1ca8ab729`
- Prior hostile review: `4478e949eb92ec411c5dec9878bb4f23b5cb2c01`
- Implementation blob: `feb097decbd160c5f259cde0a36f5033a7085fd2`
- Focused-court blob: `62c3acfe32f52e211c6a5b43ad229be6f96c888f`

The candidate lineage is clean: `684a1b20` is two documentary commits ahead of the code-bearing `a9335251`; no production change occurs after the code-bearing commit. This review is read-only with respect to implementation.

## Bottom line

The HQ214 repair closes several HQ213 defects: the 12-state vocabulary remains closed; 3+ anchors refuse; the caller-minted `signed_delta` field is gone; prior-F7 state mapping is live; cross-universe status is derived from the two bound universe refs rather than a caller boolean; negative/refusal states are classified `NOT_COMPARABLE`; no-basis precedence was repaired; the live frozen backfill surface is consulted; and the module remains below the F8/source-selection/interpolation/trajectory/causal/actor ceiling.

It is still **not ready for HQ adoption**. The repaired implementation continues to permit a positive directional receipt without proving that several contract determinants are the exact governed determinants. These are implementation defects, not a reason to reopen the F7 architecture.

## Blocking findings

### F7-RR-01 — `comparability_requirements_ref` is required but not bound to the consumed requirements

The implementation requires and parses an `ExactRef` at lines 658–662, but the actual state machine consumes the independent caller-provided `comparability_requirement_results` tuple at lines 813–816 and serializes the ref only into provenance. No resolver establishes that those result rows are the material named by that exact ref.

The focused court proves only (a) omission raises, (b) the ref appears in provenance, and (c) a separately supplied result such as `GEOGRAPHY_NOT_SHARED` changes state. It never substitutes two distinct requirement refs over the same results, nor resolves the referenced requirement set. HQ214's return says the ref is “resolved”; the code does not perform such a resolution.

This fails mandatory attack 4 and the accepted ceiling's requirement to check the exact pair against a **bound comparability requirement set**.

### F7-RR-02 — TEMPORAL_COMPARABILITY is not scoped to the exact governed-use ref

`governed_use_id` is an `ExactRef(kind, object_id, content_hash)`. The resolver helper discards kind and content hash and passes only `governed_use_id.object_id` (line 693) into scope checking. Thus a target-use scope that admits the string `USE-1` can authorize a different exact governed-use ref with the same object_id but different kind/content hash.

The existing hostile test checks only a foreign **object_id**. It does not attack same-object-id/different-exact-ref aliasing.

This fails mandatory attack 2's “exact governed_use_id” requirement. The operation binding itself is present and hash/scope mismatch reasons are reachable; the governed-use binding is not exact.

### F7-RR-03 — temporal identity remains presence-plus-caller-boolean, not exact identity resolution

The temporal identity contract is parsed only if present (lines 652–655). Identity success then depends on the caller boolean `identity_surface_jointly_satisfied` (lines 496 and 818–820). The positive `TEMPORAL_EVIDENCE` authority is resolved separately, but there is no resolution proving that the supplied `temporal_identity_contract_ref` is the identity material authorized by that snapshot.

An arbitrary well-formed identity ExactRef plus `identity_surface_jointly_satisfied=True` therefore satisfies the identity gate.

This is a residual of HQ213's F-DIR-01 at a narrower grain and fails mandatory attack 1's “TEMPORAL_EVIDENCE / identity” requirement.

### F7-RR-04 — cross-universe path bypasses the actual SOURCE_EQUIVALENCE relation result

Cross-universe status is correctly derived from the bound universes, but the implementation only requires that `source_equivalence_ref` be syntactically present. It then resolves a `SOURCE_EQUIVALENCE` authority snapshot itself and validates kind/operation plus universe scope (lines 785–807). It never resolves the supplied `source_equivalence_ref` through `SourceRelationResolver`, never proves that the ref denotes an authorized `SourceUniverseRelation`, and never binds that exact relation result to the actual pair.

The accepted implementation boundary is stronger: the source-relation owner must independently resolve the exact positive SOURCE_EQUIVALENCE result, and F7 may consume that already-resolved result. The existing source-relations module has exactly such an exact-ref resolver and `RelationDecision` surface; F7 bypasses it.

Consequently an arbitrary `SourceEquivalenceResult` ExactRef can accompany a suitably scoped authority snapshot and yield a positive temporal claim. This fails mandatory attack 8. It is an ownership-path bypass, but the module still does not mint SOURCE_EQUIVALENCE or widen into F8; I therefore classify the overall disposition as bounded partial repair rather than global authority overreach.

### F7-RR-05 — the “bound measure” check is vacuous on the positive court path

The request's `measure_authority_refs` are `AuthorityRef` objects. The quantity-surface check attempts to parse `quantity_surface["measure_ref"]` with `_require_ref`, which accepts `ExactRef`, not `AuthorityRef` (line 858). The resulting integrity exception is caught and converted to `measure_ref=None`; the mismatch comparison runs only when that parsed value is non-null (lines 858–864).

The positive court fixture supplies `MEASURE_REF`, which is an `AuthorityRef`. Therefore the ordinary positive path silently skips the binding check and serializes `quantity_surface.measure_ref` as null (lines 868–873), while still deriving and authorizing the directional delta.

The hostile mismatch test passes because it supplies a deliberately different **ExactRef**, causing a type-compatible key comparison against AuthorityRef keys that necessarily differs. That test does not prove the valid path is bound.

This fails mandatory attack 5 and the accepted “one exact quantity/estimand/measure surface” ceiling.

### F7-RR-06 — missing required order-basis ref follows the wrong contract path

The accepted contract explicitly states: for an authorized order disposition, a missing required `temporal_order_basis_ref` maps to `TEMPORAL_INSUFFICIENT_AUTHORITY / TEMPORAL_ORDER_BASIS_AUTHORITY_REF_ABSENT`.

The implementation only parses a basis ref when one is present (line 672) and never appends that absence reason. It can select a later state and then the receipt cross-field validator raises `TemporalComparabilityIntegrityError("an authorized order basis requires an exact basis ref")` (lines 1051–1054). The focused court explicitly expects that exception.

This is not the accepted terminal-state law.

### F7-RR-07 — partial-order requests do not obey total higher-state precedence

State selection first applies the 12-state precedence. But after selection, any request whose disposition is `PARTIAL_ORDER_NO_DIRECTION` is forced to be one of the two comparable-no-direction states; if a higher-priority failure won, the function raises instead (lines 943–948).

Example by direct control-flow proof: partial order + unresolved identity selects `TEMPORAL_IDENTITY_UNRESOLVED`, then raises because that state is not one of the two partial-order positive-comparability states. The same applies to insufficient authority and other higher failures.

Thus mandatory attack 11 is not satisfied for every terminal state: some lawful higher-priority terminal conditions are converted into exceptions solely because the requested order basis was partial.

## Cardinality

- 3+ anchors: correctly pre-receipt refused.
- Exactly two observations and two universe refs: enforced.
- Two anchors bind two observations: enforced on the positive path.
- Fewer than two anchors: HQ214 intentionally emits `TEMPORAL_INSUFFICIENT_ANCHORS`. This keeps the state reachable but means the closed receipt can carry fewer than the receipt contract's declared `anchor_refs exact_cardinality=2`. I record this as a contract tension, not an additional dispositive finding, because HQ214 explicitly adjudicated the reachability choice and HQ215 did not supply a contrary adjudication.

## State / delta / exact-zero / no-basis

These parts hold:

- no thirteenth relation state;
- ordered basis without derivable delta produces a typed pre-receipt refusal;
- all nine negative/refusal relation states map to `NOT_COMPARABLE` when a receipt is actually emitted;
- exact zero is exact only; no tolerance/deadband/epsilon;
- prior-F7 mapping is now used;
- clean no-basis yields `TEMPORAL_ORDER_UNAUTHORIZED`;
- no-basis plus higher failure yields the higher state and retains `no_basis_observation`;
- live backfill membership is consulted.

The partial-order precedence defect above is separate from the repaired no-basis case.

## Closed receipt / provenance

The implementation now carries the accepted top-level field names and includes operation identity, canonical projection rule, authority resolution rows, governed-use ref, uncertainty state and span state.

However, “closed shape present” is not equivalent to “closed determinants bound.” Findings RR-01 through RR-05 show that the receipt can faithfully serialize refs/provenance while still failing to prove that those refs are the exact authorities/material that justify the claim.

## Court authenticity

The HQ214 packet claims:

- focused: 83 passed;
- regression: 159 passed;
- combined: 242 passed;
- empty failure-ID delta;
- replay stable under PYTHONHASHSEED 0/1/12345.

The focused file contains 66 test functions plus parametrized expansion, and named witnesses exist for the former HQ213 findings. No broad `pytest.raises(Exception)` remains. The prior-map and live-backfill tests are no longer tautological.

But the court is not sufficient to clear this rereview:

1. the requirements-ref tests prove presence/provenance, not binding;
2. the governed-use scope test changes object_id, not exact-ref hash/kind;
3. the identity court does not prove the identity contract ref resolves to authorized identity material;
4. the cross-universe court scopes the authority but never resolves the relation-result ref;
5. the quantity/measure mismatch test uses an ExactRef while the positive fixture uses an AuthorityRef, masking the skipped valid-path check;
6. no test attacks partial-order + higher-precedence failure;
7. the missing-basis-ref test positively codifies behaviour contrary to the accepted contract.

No GitHub commit status/check run is attached to either `a9335251` or `684a1b20`, so the worker's 83/159/242 numbers remain documentary/local evidence rather than independently GitHub-certified evidence. That does not create a separate “missing evidence” disposition because the static defects above are already decisive.

### Environment classification defect

The HQ214 packet is internally inconsistent. `00_RETURN.md` says the reproduced environment was CPython **3.11.3** / pytest 9.1.1. `04_COURT_AND_REGRESSION_RESULTS.json` names `/tmp/c1-01-r8-release-spine-venv/bin/python` and Python **3.12.14** on macOS 13.7.8. Both call the evidence independently reproduced and not governed certification, which is the correct classification category, but the exact environment record is not single-valued. HQ should not adopt either exact interpreter claim without correction.

## Power ceiling

Held at the broad architectural ceiling:

- no F8 consumption or conditioning;
- no source selection;
- no interpolation/midpoint/currentness;
- no trend/rate/trajectory/rupture production;
- no causal/event interpretation;
- no scalar temporal pressure;
- no pooling/linkage/equivalence creation;
- no actor/person inference;
- no public-object/state-family widening.

The SOURCE_EQUIVALENCE finding is a result-resolution ownership bypass inside an otherwise bounded module, not evidence that F7 gained source-selection or equivalence-creation power.

## Final disposition

`F7_FINAL_REPAIR_PARTIAL__NAMED_DEFECT`

Minimum bounded repair before another final rereview:

1. bind `comparability_requirements_ref` to the exact consumed requirement material;
2. scope TEMPORAL_COMPARABILITY to the complete exact governed-use ref, not object_id;
3. bind temporal identity to exact authorized identity material rather than a caller truth boolean;
4. consume an exact authorized SOURCE_EQUIVALENCE relation result from the source-relation owner path;
5. make quantity/measure binding type-correct and positively prove the valid path;
6. restore the accepted missing-basis-ref terminal mapping;
7. make higher-priority failures survive partial-order disposition without post-selection contradiction;
8. repair the court witnesses and reconcile the environment record.

No F8 work, architecture reopen, source access, merge, or self-adoption is authorized by this return.

`HQ215_F7_FINAL_REREVIEW_RETURNED__HQ_DECISION_REQUIRED`
