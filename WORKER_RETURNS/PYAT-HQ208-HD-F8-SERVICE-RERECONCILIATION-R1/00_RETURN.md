# PYAT HQ208 — H-D / F8 service-source rereconciliation — R1

**Disposition:** `HD_PARTIAL__DOWNSTREAM_BINDING_SEAM_MISSING`

**Terminal:** `HQ208_HD_F8_SERVICE_RERECONCILIATION_RETURNED__HQ_ADJUDICATION_REQUIRED`

## Exact frame

- Branch: `agent/rabochii-pyat-hq208-hd-f8-rereconciliation-r1`
- Commission tip: `372552570b4c3ec19f91158abc9774e3cf21e522`
- HQ startup base: `26f26a56826e027f0149d12eaa1a5402dea942d9`
- Adopted service-source fan-in: `3eda3eb598cf9fe6b14df60323af52ae446b21fa`
- Accepted implementation: `e7d3598494472a9aea7dd2c69f6aacb11585905c`
- Independent review: `e3fec8be5d4c192d2d6f86059d9e1ee7a683fbd1`
- Prior H-D return: `2bdd78582a93d334cbdab918c79f4e82c3cf679c`

## Load-bearing finding preserved

`F8_DOES_NOT_TRANSFORM_POSSIBILITY_GEOMETRY` remains exact.

Current `rawlsing_next/source_backed_positioned_subject_possibility.py` is Git blob
`62e5eced47b64512f47b004e3e13a6ef3fe21de7`, byte-identical at the HQ203
examined control `3760ba31761cd6e27e978c31749161feced1a47a` and current control
`26f26a56826e027f0149d12eaa1a5402dea942d9`.

Its algorithm remains
`EXACT_CONDITIONAL_LOOKUP__NO_SMOOTHING_INTERPOLATION_OR_EXTRAPOLATION`.
F8 selects exact pre-materialized evidence geometry or performs governed strictly-decreasing
specificity walkback within the same source/release. It does not compute or transform geometry.

The objective-consumer owner is also unchanged: Git blob
`f30fca20e7b56e00348e82765d95f974b4b6a195` at both controls.

## What changed

Current control now contains the adopted source-free
`rawlsing_next/pre553_service_source_applicability.py` owner, Git blob
`3e40caca29e8c96ee1f412f919cfc7dba63f96c4`.

Its authority is exactly:

`ADMISSIBLE_SET_ONLY__RANKING_AND_SELECTION_NOT_AUTHORIZED`.

Therefore HQ203's former `service-source applicability = SOURCE_SELECTOR / UNBOUND`
classification must be narrowed. The new owner establishes source **eligibility/admissibility**,
not source selection.

On `ADMITTED`, only these positive powers exist:

- `positive_admission`
- `may_enter_source_set`
- `may_constrain_downstream_query_scope`

These remain false on every state, including `ADMITTED`:

- `may_rank_or_select`
- `may_pool_respondents`
- `may_grant_target_use_permission`
- `may_authorise_backfill`
- `may_condition_F8`
- `may_transform_geometry_or_distribution`
- `may_support_individual_inference`

Thus the old applicability-form deficit is closed at the source-free eligibility grain.
Generic source selection, ranking, and priority remain unauthorized.

## Decisive remaining gap: authority exists, consumer integration does not

Between HQ203 control `3760ba317...` and current control `26f26a568...`, the relevant
production change is the applicability owner itself. F8 and the objective-consumer owner did not
change, and no receipt-to-F8 binder was added.

Current F8 still receives caller/owner-supplied
`PositionedSubjectPossibilityModelRule.source_universe_refs` plus exactly one
`PositionedSubjectPossibilityQuery.source_universe_ref`. Its source enforcement remains a
membership check: a query source outside the model rule set fails closed with
`MODEL_SOURCE_UNIVERSE_OUT_OF_SCOPE`.

No current F8 API consumes `CandidateClassApplicabilityReceipt`, its replay identity, or its
per-source admission provenance. Therefore the new authority cannot yet constrain F8 without a
missing downstream binding seam.

That exact gap determines:
`HD_PARTIAL__DOWNSTREAM_BINDING_SEAM_MISSING`.

## C1 residual — do not over-block

The three C1 analytical modules remain absent from current control:

- `rawlsing_next/pre553_analytical_composition.py`
- `rawlsing_next/pre553_empirical_possibility_provider.py`
- `rawlsing_next/pre553_analytical_state_and_route.py`

This blocks claims about the broader accepted C1 analytical chain, joint/multi-arity production,
and C1 route/consumer semantics. It does **not** block the narrower static scalar claim that a
service-applicability receipt may constrain source scope for the already-current F8 path.

## F7 residual — do not over-block

HQ206 accepted `TEMPORAL_COMPARABILITY` as a bounded missing authority kind and explicitly did
not authorize production implementation. F7 therefore remains required for positive comparable-wave
movement, temporal products as F8 conditioners, cross-source temporal relations, temporal
pressure/directionality, or reading `effective_time_or_interval` as more than an exact scope label.

F7 is **not** required for a static exact-release eligibility-to-F8 source-scope binding.

## Required fail-closed law

The future service/F8 seam must preserve:

1. `INCOMPLETE` coverage as incomplete. Exhaustive source-set use requires `COMPLETE`.
2. `NO_ADMITTED_SOURCE_IN_CANDIDATE_CLASS` as a COMPLETE-coverage success, not no evidence.
3. Applicability `NONCOMPARABLE` and F8 evidence `NONCOMPARABLE` as distinct typed states.
4. Currentness as separate lifecycle authority; applicability cannot infer it.
5. Multiple admitted sources as separate source-indexed entries; no averaging, pooling, or winner.
6. Target-use permission refs as bound inputs, never grants.
7. Missing/conflicting applicability authority as `MISSING_AUTHORITY`/`UNRESOLVED`, never positive.

## Minimum remaining preconditions for narrow H-D final adoption

For the static/source-free scalar F8 boundary only:

1. Add an explicit applicability-receipt -> F8 source-scope binding seam.
2. Require COMPLETE coverage whenever the consumer claims the exhaustive admissible source set.
3. Preserve the unranked set. With multiple admitted sources, independently evaluate each
   source-indexed F8 path or consume a separately authorized exact source identity; never choose
   first/best/latest/local/preferred inside this seam.
4. Carry exact applicability request/receipt replay identity and admission provenance into the
   binding material.
5. Keep lifecycle currentness and target-use permission as separate authorities.
6. Keep the F8 algorithm and actor firewall unchanged.

Not required for this exact narrow claim: broader C1 adoption, F7 temporal comparability,
a pressure/hegemony object, a whole-world container, or cross-source pooling/composition.

Real applicability occupancy remains required before a live mature-world service can yield a
nonempty set, but not to finalize this source-free contract seam.

## New implementation lane

A bounded implementation lane **is justified**.

Exact seam:
`SERVICE_APPLICABILITY_TO_F8_SOURCE_SCOPE_BINDING`.

It should be a thin adapter/binder, not a new world ontology and not a source-selection owner.

It may:
- validate an exact F8 query source against an admitted receipt entry; or
- expose the entire unranked admitted `source_universe_refs` set for independent source-indexed
  F8 evaluation.

It must not rank, select, prioritize, pool, infer equivalence/linkage/overlap, compose estimands,
backfill, decide currentness, grant permission, create conditioner semantics, change
geometry/distribution, or infer actor/person state.

Mandatory refusals include request/receipt grain mismatch, candidate-class mismatch, exhaustive use
under INCOMPLETE coverage, query source outside the admitted set, nonpositive applicability passed
as admission, attempted selection/ranking/priority, attempted multi-source pooling/composition,
missing/conflicting currentness when a current claim is asserted, and replay/provenance mismatch.

## Disposition discrimination

- Not `HD_SERVICE_PRECONDITION_CLOSED__F8_BOUNDARY_FINALIZABLE_AFTER_NAMED_RESIDUALS`:
  applicability is closed, but its F8 consumer seam is absent.
- Yes `HD_PARTIAL__DOWNSTREAM_BINDING_SEAM_MISSING`.
- Not `HD_PARTIAL__C1_OR_F7_PREREQUISITE_STILL_REQUIRED`: they gate broader claims, not the
  narrow static eligibility/F8 seam.
- Not `HD_AUTHORITY_OVERREACH_FOUND`: the adopted owner stays inside its power ceiling.
- Not `HD_REVIEW_BLOCKED_BY_MISSING_EXACT_EVIDENCE`: exact current evidence is sufficient.

No raw-source access, locator discovery, warrant issuance, live C4, C7 implementation,
PREV3->V3 actor/person implementation, Astra referral, production implementation, merge, or
self-adoption occurred.

`HQ208_HD_F8_SERVICE_RERECONCILIATION_RETURNED__HQ_ADJUDICATION_REQUIRED`
