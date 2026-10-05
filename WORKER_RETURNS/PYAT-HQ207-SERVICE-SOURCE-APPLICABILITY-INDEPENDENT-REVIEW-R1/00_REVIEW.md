# PYAT HQ207 — service-source applicability independent hostile review — R1

**Disposition:** `ACCEPT_SERVICE_SOURCE_APPLICABILITY__SOURCE_FREE_FORM`

**Terminal:** `HQ207_SERVICE_SOURCE_APPLICABILITY_REVIEW_RETURNED__HQ_ADJUDICATION_REQUIRED`

Review branch: `agent/reviewer-pyat-hq207-hc-r1`
Commissioned startup SHA: `01cda2106139fc4de2594229526a1b3ff1163bbf` — **verified equal**
Exact base: `cfe648bd462ddf6fc1252182c5e784ec43bf4405` · Candidate: `e7d3598494472a9aea7dd2c69f6aacb11585905c`
Ratified derivation: `6c0d4739dc56a957a8bdd2512b24756cf466511b`
`SPARSE_REQUIRED` honored — no clone, no full worktree, **no code modified**.

---

## Verdict

The candidate faithfully implements
`ADMISSIBLE_SET_ONLY__RANKING_AND_SELECTION_NOT_AUTHORIZED`. **All eight attacked areas pass.**
No material defect, no overreach, no qualification failure. **60 collected, 60 passed** in the
governed interpreter on a clean first run.

## A — request key: exact and complete

All ten `REQUEST_KEY_COMPONENTS` are mandatory; omitting any one is refused with the typed outer
refusal (never defaulted, inferred or surfaced as a Python `TypeError` — the candidate discloses it
found and fixed exactly that defect). Thirteen forbidden smuggling names (ranking, score, weight,
preference, evidence, pooling, currentness, permission_grant, sample_size, selected, best, linkage,
backfill) are all refused before construction.

All mutable/fuzzy selectors (`LATEST`, `latest`, `DEFAULT`, `FUZZY`, `NEAREST`,
`SEMVER_FALLBACK`) are refused — the `.upper()` call matters and makes the check case-insensitive
in both directions. Unknown components, empty tuples, and permission-ref/grant confusion are
refused; `target_use_permission_refs` is declared **bound input, not a grant**.

## B/C — state separation and coverage honesty

The module defines its own decision, receipt **and** state families and explicitly refuses to alias
`SOURCE_UNIVERSE_RELATION_STATE`, `EMPIRICAL_FACT_STATE`, `AUTHORITY_STATE` or
`STRUCTURAL_ADMISSION_STATE`. Precedence puts `INTEGRITY_FAILURE` first and `ADMITTED` **last**.

Coverage is `COMPLETE` **iff every** candidate holds a terminal decision. I attacked every route —
unresolved candidate, missing authority, conflicting authority, integrity failure, broadened class,
narrowed class, out-of-class authority — and **none produced COMPLETE**. Critically,
**`NO_ADMITTED_SOURCE_IN_CANDIDATE_CLASS` is unreachable under INCOMPLETE**, enforced twice: the
resolver only sets it inside the `coverage == COMPLETE` branch, and the receipt's own
`__post_init__` independently refuses it under `POST_COVERAGE_LAW`.

## D — the unranked set holds

Three `ADMITTED` sources stay an **unranked set of separate source-indexed entries**. I measured
**1 distinct replay identity** across all 6 candidate-order permutations *and* all 6
authority-record permutations. Every named hidden-ordering attack is absent: no first-source-wins,
no ordering preference, no score, rank, priority, locality preference, release-recency preference or
implicit fallback order. Absence of authority yields `MISSING_APPLICABILITY_AUTHORITY` and forces
INCOMPLETE rather than falling through.

## E — power noncollapse

I called `assert_receipt_does_not_authorize` for **all 14** forbidden purposes against a real
receipt containing an `ADMITTED` source: **14/14 refused**, including pooling, selection, ranking,
priority, semantic equivalence, respondent linkage, overlap/nonduplication, estimand composition,
backfill, currentness, target-use grant, F8 geometry/distribution transform, individual inference
and actor/person state. Every `may_*` flag is `False` for **every** decision — including on
`ADMITTED` for rank/select, pooling, F8 conditioning, geometry transform and individual inference.

## F/G — evidence distinction, replay and provenance

In a single receipt, a bound-negative source renders `NOT_APPLICABLE` while authority-less sources
render `MISSING_AUTHORITY` — **absence of evidence is never converted into evidence of
inapplicability**. No receipt key carries an evidence value, and the court *structurally* AST-proves
the resolver reads no forbidden evidence field. Replay is deterministic under permutation, the
request identity is stable and determinant-sensitive, positive decisions carry exact admission
provenance, and negative decisions preserve exact basis while being refused if they carry admission
provenance.

## H — court quality and regression

**60 collected, 60 passed** (`0.22s`, exit 0) in the governed R7 interpreter. All **15**
commissioned hostile cases are present, and the load-bearing ones drive the real resolver and
assert on resulting receipts or raised refusals — including a genuinely structural
evidence-noninterference proof. The change is **purely additive: 8 added paths, 0 modified** — no
pre-existing production or test file is touched.

## Three corrections to my own work — recorded

1. I first measured **6** distinct replay identities under permutation and nearly recorded a
   determinism defect. **My bug**: the probe tuple included the builtin `id()`. Corrected: **1**.
2. I first flagged hidden rank/score/priority/weight and evidence/support fields by **substring**
   scan. Value inspection showed every hit is a negation *declaration* flag set to `True`. Corrected:
   no such value-carrying field exists.
3. I labelled version `Mixed` an anomalous accepted selector. The check uppercases first, so `Mixed`
   is correctly an ordinary exact version. **My label was wrong.**

Notably, the candidate discloses that one of *its* three found court bugs was the same
substring-matching trap I fell into twice — its disclosure is credible and the fix direction
matches what I had to apply.

## Scope limitations

I did not run a broad repo-wide regression slice; I relied on the additive-only diff (8 added, 0
modified), the focused court, and an import/name-collision check. And the receipt is an immutable
dataclass, so a caller who ignored `assert_receipt_does_not_authorize` could read `as_dict()`
directly — a caller-misconduct boundary, not an authority the module issues.

## Holds observed

No code modified; no source access; no locator discovery; no warrant issuance; no live C4; no
self-adoption. This accepts a **source-free synthetic form** — it establishes machinery only and
authorises no real-world structural claim.
