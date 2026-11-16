# PYAT HQ210 — SERVICE APPLICABILITY → F8 SOURCE-SCOPE BINDING — R1

**Disposition:** `HD_F8_SOURCE_SCOPE_BINDING_COMPLETE__READY_FOR_INDEPENDENT_REVIEW`

**Branch:** `agent/rabochii-pyat-hq210-hd-f8-binding-r1`
**Commission tip (verified exact):** `904895d8ad072824f38464f579904e5193d55667`
**Exact startup base:** `7cc1ce20238e06e4b785b6a804cc885cd19d641a` (verified = parent)
**Governing rereconciliation:** `6e2649c4d111fd0ec176c9fa29ce1da27ccc448e`
**Binding F8 law:** `F8_DOES_NOT_TRANSFORM_POSSIBILITY_GEOMETRY`
**Checkout:** `SPARSE_REQUIRED` — reused the HQ-prepared worktree, no clone, no broad fetch.

**Terminal:** `HQ210_HD_F8_SOURCE_SCOPE_BINDING_RETURNED__INDEPENDENT_REVIEW_REQUIRED`

---

## What this closes

HQ208 proved the gap in one line:

> *"no binding from CandidateClassApplicabilityReceipt/replay identity to
> `PositionedSubjectPossibilityModelRule.source_universe_refs` or exact query-source validation"*

That gap is now closed by **one thin binder in two new files**. No adopted owner was touched.

```
rawlsing_next/pre553_service_f8_source_scope_binding.py                        (new)
rawlsing_next/tests/test_pre553_service_f8_source_scope_binding_court.py      (new)
```

Blobs before → after, for the three owners HQ210 forbade me to modify:

| owner | blob | state |
|---|---|---|
| `pre553_service_source_applicability.py` | `3e40caca…` | **UNCHANGED** |
| `source_backed_positioned_subject_possibility.py` | `62e5eced…` | **UNCHANGED** |
| `objective_consumer_bounded_evidence.py` | `f30fca20…` | **UNCHANGED** |

The commission allowed a minimal wiring change *only if exact implementation proved it unavoidable*, and
required stopping to name a blocker rather than silently editing. **No wiring need arose, so there is no
blocker to report.**

---

## The two positive powers, and only two

1. **`assert_query_source_admitted`** — validate **one** exact F8 query source at **one** exact release
   against a positive admitted entry, returning its admission provenance.
2. **`expose_unranked_admitted_source_set`** — expose the complete unranked admitted set for independent
   source-indexed F8 evaluation.

There is no third. Two binding modes, no third. The seven selection-shaped methods
(`first_admitted_source`, `ranked_sources`, `pooled_source_set`, `conditioned_f8_geometry`,
`grant_target_use_permission`, `currentness_authority`, `infer_individual_state`) all **raise** with exact
reason codes rather than returning anything.

**No ranking — enforced structurally, not asserted:**

- binding material contains **no** rank / score / priority / preference / weight / best / first / latest /
  local field or value (proven by recursive value inspection)
- the admitted set is **unranked**, proven by **permutation invariance** of the binding replay identity
  across all 6 orderings of a 3-member candidate class — not by a self-declared boolean

---

## The F8 boundary, and the trap HQ208 named

Eligibility makes a source usable as a **source scope**. Nothing more.

- **conditioning** — refused; the binder exposes no conditioner constructor, and the court proves by **AST
  scan** that the module reads *no* conditioner or geometry attribute (the touched set must be empty)
- **geometry / distribution transformation** — F8 remains
  `EXACT_CONDITIONAL_LOOKUP__NO_SMOOTHING_INTERPOLATION_OR_EXTRAPOLATION`; the binder adds a **law-drift
  guard** that refuses if F8 ever reports a different `algorithm_id`
- **pooling**, **individual/actor inference** — refused
- `query`, `rule`, `evidence` reach the adopted evaluator **by identity**; the court asserts the caller's own
  `query.ref`, the same evidence object, and byte-identical `exact_geometry`

**The trap:** narrowing eligibility *can* change **which** pre-materialized slice F8 selects. That is output
**selection**, not output **transformation**. The court pins it directly — the same evidence yields identical
geometry and identical result state under both a wide and a narrowed binding.

---

## The distinction the commission insisted on

`NO_ADMITTED_SOURCE_IN_CANDIDATE_CLASS` is honoured only under COMPLETE coverage — and I **hardened** this
beyond the literal text. Exposing the set is *itself* an exhaustive claim, so `expose_unranked_admitted_source_set`
now requires COMPLETE coverage **in every binding mode**, not just the exhaustive one. Otherwise a caller could
bind a single-source binding over an INCOMPLETE class and then read back a partial set as if it were the
admissible set. The court pins that exact laundering attempt; it refuses. The narrow capability survives: one
known-admitted source can still be validated under INCOMPLETE.

Also preserved: applicability `NONCOMPARABLE` stays distinct from F8 evidence `NONCOMPARABLE` (both exercised
simultaneously); multiple admitted sources stay **separate source-indexed entries** with one provenance row
each, and cardinality is explicitly not a sample size.

---

## Qualification

| | result |
|---|---|
| new focused binding court | **72/72** |
| applicability court (unmodified) | 60/60 |
| F8 court (unmodified) | 13/13 |
| positioned-admission court | 3/3 |
| **aggregate** | **148 collected, 148 passed, 0 failed, 0 skipped** |

**Determinism:** three runs — `148 passed` with `PYTHONHASHSEED=0`, `0`, and `12345`. The third exists so
determinism is not an artifact of one lucky seed.

**Regression slice:** all 66 test files importing the touched/imported surface. Controlled before/after on
identical inputs, compared as **sorted sets** rather than aggregate counts:

```
baseline     78 failed · 1165 passed · 50 collection errors
post-change  78 failed · 1165 passed · 50 collection errors
new failures: []      new collection errors: []
```

**Zero regression.** The 78 failures and 50 collection errors are **pre-existing on this lineage** — dominated
by absent optional dependencies (`duckdb`) and missing fixtures — identical with and without my change. I
neither caused nor repaired them, and I make **no claim the wider surface is green**.

**Environment, truthfully:** the governed interpreter named by the commission is **absent on this host**, and
`c4c3-env` is gone too. Per the shared-store environment law I did **not** recreate one. All results come from a
disclosed, already-existing interpreter whose **14-package freeze is set-identical** to the governed
`01_ENVIRONMENT_LOCK.json`, `pyreadstat 1.3.6` held. Labelled **reconstructed-equivalent evidence, not governed
certification**. The binding is pure source-free logic over synthetic exact refs, so no semantic claim here
depends on the missing environment.

---

## I did not get it right first time — five defects, recorded

I am listing these because a reviewer should attack them first.

**Three real binder bugs:**

1. **Type bug** — compared an `ExactRef` against a `str`-keyed dict, so *every* positive admission was wrongly
   reported absent. Caught by the first smoke run.
2. **Authorisation-laundering path** — set exposure enforced COMPLETE coverage only in exhaustive mode (defect 3
   above). Caught by the court.
3. **Foreign exception leak** — delegated the coverage check to the adopted owner's private `_Refusal`, leaking
   a foreign type into my refusal surface. Now one typed surface, reason code preserved.

**Two test-quality defects — the same family as the GAP-3 problem I was trying to avoid:**

4. **My two write-terrain guards silently SKIPPED.** I computed the repo root as `parents[2]` instead of
   `parents[1]`, so they protected nothing while appearing to pass. I caught it by noticing an unexpected skip
   in an all-green run. **A test that skips while looking green is the same failure as a self-referential test.**
5. **Six wrong court assertions** (not code bugs): a defaulted `None` identity; two identically-built rules
   asserted to differ; an index-0 assumption over F8's *sorted* `replay_determinants`; a banned-substring scan
   that flagged the word "un**rank**ed" as "rank"; a `dir()`-based surface check that swept in merely-imported
   names; and a premise that a mislabelled receipt could be constructed at all — when the adopted owner already
   refuses to construct one. I rewrote that last case to assert the **stronger** real property.

---

## Court written to not be self-referential

The adopted review of the applicability owner (HQ207 GAP-3) showed a court iterating the *production
constant* cannot detect narrowing of it, and proves only that the *function* refuses its own list. So this
court:

- **pins 25 forbidden purposes as literals in the court file** — truncating `FORBIDDEN_BINDING_PURPOSES` makes
  the court **fail**, not silently collect fewer cases
- proves non-authorization by **value inspection of emitted data**, not by asserting the module's
  self-description
- proves "unranked" by **permutation invariance**, not by a self-declared flag
- pins the public API against `__all__`, and pins the *returning* surface apart from the *raising* surface

---

## C1 and F7 — genuinely not needed

I did not wait for either, imported neither, and claim no analytical, joint, multi-arity or positive temporal
result. The seam binds a **static exact-release source scope**: it computes no delta, builds no trajectory and
performs no composition, so neither C1 nor F7 lies on its path.
`TEMPORAL_COMPARABILITY_OR_PRESSURE` is a refused purpose.

---

## Referred to HQ

- **HQ207's court gaps in the applicability owner** (GAP-1…GAP-4) and its arithmetic error
  (`additional_courts_written` claimed 45; actually 32) are **not repaired here** — that owner is outside my
  write terrain. Its *mechanism* was independently verified sound by that review.
- The 78 pre-existing failures / 50 collection errors are out of scope.
- Which lifecycle authority may issue a currentness result is not adjudicated here; I only refuse to assert
  currency I was not given.

**Holds:** no raw source · no locator discovery · no warrant · no live C4 · no C7 · no actor/person work · no
ranking/selection · no pooling · no F8 geometry transformation · no self-adoption · no adopted owner modified ·
no clone · no broad fetch · sparse scope not widened beyond this seam and its courts · pushed only this branch.

`HQ210_HD_F8_SOURCE_SCOPE_BINDING_RETURNED__INDEPENDENT_REVIEW_REQUIRED`
