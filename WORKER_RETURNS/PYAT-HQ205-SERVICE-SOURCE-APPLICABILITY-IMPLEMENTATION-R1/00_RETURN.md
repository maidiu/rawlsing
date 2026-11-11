# HQ205 — service-source applicability, source-free implementation — R1

**Disposition: `SERVICE_SOURCE_APPLICABILITY_IMPLEMENTED__READY_FOR_INDEPENDENT_REVIEW`**
**Terminal: `HQ205_SERVICE_SOURCE_APPLICABILITY_IMPLEMENTATION_RETURNED__HQ_REVIEW_REQUIRED`**

Implements ONLY the HQ-ratified minimal form:

`ADMISSIBLE_SET_ONLY__RANKING_AND_SELECTION_NOT_AUTHORIZED`

No raw source access, no warrant, no live C4, no C7, no actor/person work, no
self-adoption.

## Identity

| Field | Value |
|---|---|
| Branch | `agent/rabochii-pyat-hq205-hc-impl-r1` |
| Startup SHA (exact, verified) | `dcf9ab533433e2b6db9fbd8dfd9081e76f5f1984` |
| Ratified documentary derivation | `6c0d4739dc56a957a8bdd2512b24756cf466511b` |
| HQ205 adjudication | `0e8d5bcd98e5aba63cd7312f778dedbfe8b6b646` |

Only the exact governed branch ref was fetched.

## What was added

Two files. **Zero existing files modified; zero existing owners edited.**

| File | Lines | Role |
|---|---|---|
| `rawlsing_next/pre553_service_source_applicability.py` | 829 | the owner/resolver |
| `rawlsing_next/tests/test_pre553_service_source_applicability_court.py` | 510 | 60 hostile source-free courts |

Placed as same-grain bounded succession from `pre553_structural_admission.py`, the
immediate sibling row in the same D15 ledger, reusing its idioms verbatim: a frozen
`DECISION_PRECEDENCE`, a coarser `PUBLIC_STATE_BY_DECISION`, a `DECISION_MATRIX` of
per-state power flags, unknown-and-conflicting folded into one `UNRESOLVED` public
state, and a single `POSITIVE_DECISION`.

**No owner collision.** A search of all of `rawlsing_next` found no existing
service-source applicability owner, so `…_OWNER_COLLISION__HQ_REQUIRED` was not
triggered.

## The derivation was stricter than the commission — and was preserved

The commission listed a minimum of six decision states. The ratified derivation
carried a **10-value exact decision precedence** and a **7-value public state map**.
Both were implemented verbatim:

```
INTEGRITY_FAILURE · MISSING_APPLICABILITY_AUTHORITY ·
UNKNOWN_OR_CONFLICTING_APPLICABILITY_AUTHORITY · REQUEST_KEY_INCOMPLETE_OR_AMBIGUOUS ·
SOURCE_OUT_OF_DECLARED_SCOPE · SOURCE_NOT_APPLICABLE_TO_THIS_SERVICE_AND_USE ·
SOURCE_NONCOMPARABLE_AT_THIS_TARGET · NEGATIVE_AUTHORITY_ONLY ·
UNDETERMINED_NO_POSITIVE_AUTHORITY · ADMITTED
```

Public: `APPLICABLE · NOT_APPLICABLE · NONCOMPARABLE · OUT_OF_SCOPE ·
MISSING_AUTHORITY · UNRESOLVED · INTEGRITY_FAILURE`, coarsened only through the map
so the vocabulary cannot be widened.

`SERVICE_SOURCE_APPLICABILITY_STATE` is a **new** family, never aliased to
`SOURCE_UNIVERSE_RELATION_STATE`, `P07_RELATION_DECISIONS`, `EMPIRICAL_FACT_STATE`,
`AUTHORITY_STATE` or `STRUCTURAL_ADMISSION_STATE` — because `NOT_APPLICABLE`,
`NONCOMPARABLE` and `OUT_OF_SCOPE` each already exist in more than one family, and
aliasing would make an applicability refusal indistinguishable from a relation
refusal.

## One deliberate generalization, stated openly

The derivation *illustrated* `INCOMPLETE` coverage with a single example
(`UNDETERMINED_NO_POSITIVE_AUTHORITY`). I implemented the **general** definition —
`COMPLETE` means every candidate received a **terminal** decision, so any of the five
non-terminal decisions forces `INCOMPLETE`. This is strictly safer: `COMPLETE` can
never be reported while any candidate is undecided.

## Binding decisions implemented

| Decision | Implementation |
|---|---|
| `candidate_class_ref` mandatory | in the key, and the class must match the bound exactly |
| distinct state family | `SERVICE_SOURCE_APPLICABILITY_STATE`, alias-proven |
| positive state `APPLICABLE` | `POSITIVE_PUBLIC_STATE` |
| incomplete coverage never masquerades as complete | `is_complete_admissible_set()` false; receipt labelled `…__COVERAGE_INCOMPLETE` |
| exhaustive downstream ops fail closed | `assert_complete_coverage` refuses with `APPLICABILITY_COVERAGE_INCOMPLETE` |
| admission provenance required | `ADMITTED` without it is refused; non-positive carrying it is refused |
| no selection-reason record | no such field exists at receipt or decision grain |
| canonical ordering replay-only | `ORDERING_SEMANTICS` states zero rank/priority/preference/weight/fallback |

`NO_ADMITTED_SOURCE_IN_CANDIDATE_CLASS` is **structurally impossible** under
`INCOMPLETE` coverage — both the receipt constructor and the resolver refuse it, so an
under-examined class can never be laundered into "there are no applicable sources".

## Power noncollapse

Only `ADMITTED` carries any positive flag. `may_condition_F8`,
`may_transform_geometry_or_distribution`, `may_pool_respondents`,
`may_support_individual_inference`, `may_rank_or_select`,
`may_grant_target_use_permission` and `may_authorise_backfill` are **False for every
state including `ADMITTED`** — eligibility is not conditioning.

`assert_receipt_does_not_authorize` refuses all 14 separate powers (pooling,
selection, ranking, priority, semantic equivalence, respondent linkage, overlap,
estimand composition, backfill, currentness, permission grant, F8 transform,
individual inference, actor/person state).

Smuggling is refused at the key: `ranking`, `score`, `weight`, `priority`,
`preference`, `selection_reason`, `pooling`, `linkage`, `overlap`, `backfill`,
`currentness`, `evidence`, `support`, `sufficiency`, `sample_size` and 10 more.

## The evidence distinction, structurally enforced

`ServiceSourceApplicabilityDecision.REQUIRED_FIELDS` is exact and contains **no**
internal-evidence-sufficiency field, with an explicit `FORBIDDEN_FIELDS` enumeration.
An AST court asserts the resolver contains **zero** reads of any evidence attribute.
So an `APPLICABLE` source's later `ZERO_SUPPORT`/`OBSERVED_ZERO` outcome cannot move
an applicability state, and `NO_ADMITTED_SOURCE_IN_CANDIDATE_CLASS` can never be
rendered as a statement about evidence volume.

## Court: 60/60, deterministic, all 15 required cases present

`60 passed`, three consecutive runs. All fifteen commission-required cases are
present, including the parametrised refusal of all 14 forbidden purposes.

## Two real production defects found and fixed

1. **`ServiceApplicabilityRequest.build()` surfaced an incomplete key as a Python
   constructor `TypeError`** instead of the typed `SERVICE_REQUEST_UNDETERMINED`
   refusal the contract requires. A `TypeError` is not a refusal. Now validated
   before construction.
2. **`ApplicabilityAuthorityRecord` validated `admission_authority_ref.authority_version`
   before coercing a mapping to `AuthorityRef`**, raising `AttributeError` on the
   normal mapping input path. Coercion now precedes validation.

Three court-authoring bugs were also caught — including a hygiene check that wrongly
banned the literal `POOLING`, when naming a forbidden purpose *is* the refusal
mechanism. The declarative refusal vocabularies are now exempt; only capability
surfaces are banned.

## Regression: zero new failures

| | before | after |
|---|---|---|
| failure/error IDs | 280 | **280** |
| failed / errors | 227 / 53 | **227 / 53** |
| passed | 2276 | **2336** |

New: **0**. No longer failing: **0**. `passed +60` is exactly the new court. The
pre-existing 227 failures and 53 errors are unrelated sparse-fixture and environment
artifacts carried from current control.

## Limits and open items

- This is a source-free authority **seam**. No source universe, service, target or
  candidate class is populated. This lane delivers the FORM, not occupancy.
- Service-specific applicability authority must still be authored per service/source
  pair before any admissible set is non-empty in practice.
- Real candidate-class coverage will be `INCOMPLETE` until that authority exists —
  which is the correct, intended fail-closed posture.
- H-A temporal directionality and H-D F8 geometry transformation are untouched.

## Holds preserved

No raw source access, warrant, live C4, C7, or actor/person work. No self-adoption:
this implements the ratified form and returns it for independent review. No existing
owner was edited.

## Terminal

`HQ205_SERVICE_SOURCE_APPLICABILITY_IMPLEMENTATION_RETURNED__HQ_REVIEW_REQUIRED`
