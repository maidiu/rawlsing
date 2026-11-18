# R3 G1–G5 RECHECK — same distinct C

**Verdict: `REVISE_EXACT_CONSEQUENTIAL_GAP`.**
**Target:** `b567ceee8291b4927004dfc4b5b109ae29ba0294`, author branch
`agent/anvil-r3-downstream-accommodation-20261117-r1`.
**Predecessor:** `c548ef10bc2276cbe6016a53b8a39b9728cbc922`; prior C
`e4cda70a66af241297c230362a61b03e77bb13bc`; product `cea2d4d…` unchanged;
protected `5d387a9…` rev11 unchanged.
**Package:** 8/8 manifest payload hashes; 10 capability rows; 27 ledger entries;
old 22 entries preserved exactly; 5 new entries 023–027.

**Scope:** stage-sensitive conceptual accommodation and research custody only.
No native/100k, product implementation, source/science/actor authority,
protected adoption or H1.

## Per-G disposition

| Gap | Disposition | Basis |
|---|---|---|
| **G1** FF01-2/FF01-k split | **MOSTLY RESOLVED; one exact-contract gap** | Old `ExactConditionalSupportProfile` claim is retracted in `R3-RES-023`; corrected §5.4 correctly keeps FF01-2 as fixed Q86B→Q86A two-participant count/no-ratio, and proposes FF01-k with roles/order/direction/risk/weights/coverage/typed states/owner-held ratio. But `R3_FIELD_AND_ADAPTER_CONTRACT.md` has no exact FF01-k field/receipt/consumer schema; the decision gives categories. Add the exact table; method/eligibility/ratio can remain owner-held. |
| **G2** C11/external/absent source map | **PARTIALLY RESOLVED** | Exact C11 field map is now correct: `QuestionVariableBinding` has no option/form/routing content; `EmpiricalUniverse` has `respondent_namespace`, not household/PSU/strata; `WeightMeasureFact` has design/estimand authority refs, not variance; `EmpiricalFact` has method/state, not numeric interval. But the “external source/codebook/design artifact by exact identity” route has no concrete artifact type, ref kind, lookup/join from native ref/version/source lineage, authority/current, scope, permission or refusal protocol. Product search finds no external codebook resolver. Add the external-artifact contract or mark external lookup `UNPROVEN_HOLD`; do not grade those fields conceptually accommodated until specified. |
| **G3** research refs | **RESOLVED** | 27 ledger entries; old 22 preserved exactly; new 023–027 have corrections/retractions; 24 refs in decision, 23 in capability table, 10 in falsifiers all resolve to existing IDs. The architecture is no longer parallel to the ledger. `R3_FIELD_AND_ADAPTER_CONTRACT.md` has no R3-RES refs; add 024/025/026 when next edited. |
| **G4** exact views/adapter | **NOT RESOLVED** | See exact counterexamples below. Identity keys include state; `SelectionMembership` is count-only despite full-fact membership needs; bounded-RAM claim does not account for full universe/routing/denominator cost. |
| **G5** F6 design variance/PSU/strata | **RESOLVED** | Corrected §5.3, R3-CAP-03 and R3-CAP-08 explicitly state C11 has design/estimand authority refs and universe/frame labels only; PSU/strata/replicate weights/design variance and numeric uncertainty are external F6 inputs or typed absent. |

## G4 exact counterexamples

**G4-A — state in identity key.** `R3_FIELD_AND_ADAPTER_CONTRACT.md` §2.3–2.6
(lines 44–70) puts `response_state`, `applicability_state`/`routing_state`,
`coordinate_state` and `weight_state` into the identity keys. Two records for
the same stable event/coordinate/weight identity that disagree on state then
have different keys and are not refused as duplicates/contradictions. The
actual evaluator catches routing state conflicts and weight multiplicity, but
that is evaluator behavior, not the proposed view contract; the contract itself
does not establish the required refusal. **Correction:** separate stable
identity keys from mutable state/value content; refuse conflicting content for
one identity unless an exact version/authority distinguishes it.

**G4-B — count-only selection membership.** The contract line 107 defines
`SelectionMembership (candidate refs + nonselected count)`; the corrected
decision §3.3 says complement counts. The actual `_build_fact` requires
`risk_set_member_refs=evaluation.risk_members` and
`denominator_member_refs=evaluation.denominator_members`, and
`_evaluate_index_group` appends every respondent’s exact ref after routing/
denominator evaluation. A count-only reusable selection object cannot supply the
full nonselected membership needed for exact facts. **Correction:**
`SelectionMembership` must carry exact ordered risk/denominator member refs, or
the adapter must always materialize the full `_ReleaseIndex` membership; counts
are diagnostic only.

**G4-C — bounded selected row groups vs full risk/denominator.** The contract
says “Disk/RAM bounded by selected partition/row groups” (lines 125–129) while
requiring the full risk population/nonselected members. `_ReleaseIndex` carries
full respondents/events/routing/weights and `_evaluate_index_group` evaluates
every respondent. A selected-row-group view cannot both bound RAM to selected
rows and expose complete universe/routing/denominator membership without a
qualified full membership index or full routing/weight scan. The contract does
say “No Q-reduction claim before measurement,” but still declares bounded RAM.
**Correction:** separate selected page reads from the full universe/routing/
denominator membership cost; state the full cost or require a qualified compact
index; no bounded-RAM/Q claim for full-domain facts without measurement.

## What is genuinely settled

- 13-family canonical body retained; no new body/database/psychology.
- Prepared-session-first within process; conditional one-journal/source-derived
  Q2 with full physical proof and second-certificate fallback; conditional
  recovery; durable index held; v1 fact/replay ABI retained.
- Native F1–F4, true same-person k≥3, F2 direction-specific bases, F3
  minority/recursive; FF01-2 vs FF01-k separation; F6/F7 external; FF02/N9/
  SEAM/SOROK owner boundaries; no source→actor/opinion→power/fictional→observed
  promotion.
- 26 NOT_ADOPTED / 14 HELD / F26 / separate 52/24/21 preserved.
- Research ledger 27 entries, old 22 exact, new corrections/retractions,
  sources/grades/counterarguments/negatives/cross-refs/reuse; G3 linkage now
  present in decision/table/falsifiers.

## Remaining conditional extensions / owner proofs

- exact FF01-k field/receipt/consumer schema; method/eligibility/ratio/weighted
  estimand owner-held;
- external source/codebook/design artifact lookup/scope/refusal contract;
- exact state/value-separated view keys and conflict refusal;
- full member-ref `SelectionMembership` or full `_ReleaseIndex`;
- full universe/routing/denominator cost accounting for selected views;
- durable index H/S/Q/O; Batch prepared adapter; Q2 full proof; recovery crash
  injection; FF02 material power, F7 comparability, N9/N10W, SEAM encounter,
  SOROK actor; original35/native rights; 100k/6 GiB/1–10/100.

## Research custody

G3 now passes at sampled scope: 27 stable entries, old 22 exact, new 023–027
with explicit retraction/correction, all architecture refs resolve. The field/
adapter contract itself has no R3-RES refs; add 024/025/026. No sampled
fabricated execution or false native grade found.

## Strongest failed attacks

The corrected split does refuse the former false FF01 k>2/reverse claim; the
exact C11 field map correctly distinguishes absent/external source meanings;
the G3 linkage is real; the G5 external F6 boundary is explicit. The remaining
G4 issues are concrete view-contract defects, not a demand for implementation
or native evidence.

## Limits

- Source-lineage inspection is sampled, not exhaustive.
- No native/100k, product test matrix, new sourcefree experiment, instrument
  authentication or external reviewer/science authentication.
- Static schema/code/contract findings are decisive; no author patch.
- No H1, protected adoption, source/science/actor/native or performance
  acceptance is claimed.

**Return SHA:** final commit on this review branch; original review `e4cda70a…`
and prior R2/C roots preserved unchanged.
