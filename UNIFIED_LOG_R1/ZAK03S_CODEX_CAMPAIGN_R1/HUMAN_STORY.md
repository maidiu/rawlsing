# HUMAN_STORY.md — What the old relation rule knew, and what the modern machine actually authorizes

**Boundary:** every modern statement below is about protected cut `6a5c12f04323d74001f9632063ec907f4fc4468e` and the explicitly named candidates. It is not a claim about the active PYAT machine globally, nor about unsearched branches or future deployments.

## The short version

The old F03 machine answered a narrow but consequential question: **may this exact source-specific question be used as directional relation evidence, only as context, not at all, or under a special certified exception?** It read a selected QSM authority row keyed by source family, wave, country, question and variable, then copied structural coordinates and set eligibility, pressure and review states. The answer was not a statistical result. It was a **permission-and-meaning decision** about what a later empirical bridge was allowed to represent.

The modern protected machine has three different authorization layers that can look similar from a distance:

1. **I03 empirical query** — may this exact query read this exact sealed C11 source release and produce this `EmpiricalFact`? It checks source/risk/authority fitness. A `TARGET_USE_PERMISSION` check is optional and, when declared, binds an exact target-use ref, authority and operation. It does **not** know about F03's six structural coordinates, directionality or QUC.
2. **I04 structural admission** — may this exact empirical fact be used for this exact **structural** target? This is much closer to F03 in vocabulary. It requires a named, content-addressed `StructuralAdmissionRule` with structural target identity, semantic identity, role/directionality semantics, predicate/target semantics, estimand/measure/temporal scope and negative authority. But the rule is **caller-supplied**. No protected code derives it from a selected QSM row.
3. **Issued-workload/Batch** — an external `CurrentDecisionResolver` admits a `NativeWorkload`, then the machine runs Route B, I03/I05 and Batch. It does not call I04. It records unit execution receipts, not structural meaning.

So the honest modern answer is: **the structural-admission vocabulary exists, but the selected F03/QSM-to-I04 binding and a real production first reader are not proved.**

## A worked before/after example

**Old (illustrative, not a sampled respondent record):** a V550 bridge row for source family GSS, wave 2010, country US, question `QX`, variable `Y` enters F03. The selected QSM row says the relation is directional. F03 copies the six structural coordinates, records polarity/reversal, marks `RELATION_EVIDENCE` certified and sets pressure eligibility. If the row instead says context-only, F03 clears the coordinates but retains contextual coverage. If it says administrative or blocked, F03 clears the coordinates, denies pressure and marks review. If the active registry has no matching row but a separate QUC row is certified, carries `RELATION_EVIDENCE`, is currently directional-eligible, is allowed as V551 relation evidence and has `structural_mapping_status=COMPLETE`, F03 preserves that qualified prior evidence. Change any one of those five conditions and the preservation branch fails.

**Modern:** the same source responses can become C11 `RespondentEvent` objects, then an I03 `EmpiricalFact` such as “the observed RAW share of `Y=1` in this risk set is …”. That fact may be true and useful. I03 does not thereby say the question is a directional structural relation. To get structural meaning, a caller must supply an I04 `StructuralAdmissionRule` with an exact structural target and a `TARGET_USE_PERMISSION` binding; I04 then returns `ADMITTED` or a typed nonpositive state. No protected path directly invokes I04, and no protected code binds the rule to the historical QSM row. A real non-test static receiver, `RouteObligation.from_structural_admission`, consumes the canonical admission receipt and derives route facts, but its own callers are tests only.

## Why the target-use flag is not the old rule

A modern reviewer could see `TARGET_USE_PERMISSION` and conclude “the old permission survived.” That is the exact false implication this round rejects.

- In I03, the target-use triple is optional. If the query grain omits it, I03 returns a fact without any target-use check. If present, it checks an exact `TARGET_USE_PERMISSION` snapshot for `EmpiricalFact@1.0.0`. It still has no structural target identity, no six-coordinate projection, no polarity/reversal and no QUC branch.
- In I04, `TARGET_USE_PERMISSION` is **necessary but not sufficient**. The rule also must bind a structural target, semantic identity, predicate/target semantics, role/directionality and negative authority. I04 can deny for missing structural admission authority even when a valid target-use permission exists.
- In C11, a `StructuralAdmissionReplayBinding` can be carried with state `NOT_APPLICABLE`. The carrier proves custody of a reference, not that an admission was positive.

## What changed physically

The physical source path is explicit and governed: decoded cells → `GovernedC11Projection` with caller-declared semantics and authority → validated `C11LogicalRelease` (`semantic_release_hash`, `source_release_manifest_hash`, public objects, internal records, M01–M18 coverage). The logical release, not the physical file, is what I03 reads. This is a real improvement in replay and custody. It does not create selected source-rule meaning. In the protected source-native adapter, the authority snapshots are `R56-TEST-ONLY-AUTH-*` at `TEST_ONLY_SOURCEFREE`, and `structural_replay` is `NOT_APPLICABLE`.

## What is genuinely reusable

- The I04 decision vocabulary and rule schema are a strong **structural-admission capital**: they name what a lawful structural use would require, including the negatives and compatibility fields.
- The C11 `StructuralAdmissionReplayBinding` is a usable **carrier** for an admission receipt once a real producer exists.
- The exact I03 source/risk/authority checks and typed negative facts are reusable as a lower-grade empirical layer.
- The old F03 branches remain a precise **oracle**: directional, context, administrative, blocked and QUC certified no-match. Any claimed successor should be tested against each positive and negative, not just a happy path.

## What is not proved

No selected QSM row/version is bound to a modern rule. No direct non-test invocation of I04 is proved; a real non-test receipt consumer exists, but its own callers are tests. No C11 `PRESENT` binding is proved to come from an `ADMITTED` evaluation. No I05/Batch receipt is proved to carry F03 structural meaning. The historical selected file and execution receipt remain unknown. These are open proof gaps, not a claim that the old function was globally lost.

## Case index

- [Current I04 structural-admission seam](CASES/ZAK03S_CASE_I04_STRUCTURAL_SEAM.md) — this round’s substantive case; linked to `ZAK03:T:0004`, not a new historical T.
- Prior R3 F03 case: `../ZAK03_SOURCE_AUTHORITY_RECON_R3/CASES/ZAK03_T_0004.md` — old selected-rule semantics and six child S mechanisms.
- Prior R3 cases T0001–T0014 remain the authoritative local cross-references; this round imports their identities without re-authoring them.
