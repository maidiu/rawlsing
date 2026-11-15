# ZAK1057-REVIEW-04 — F6M/F6P numeric meaning and the predecessor missing-share defect

**Review case ID:** `ZAK1057:R2:CASE:04`
**Reviewed family:** `G1A-FUNC-026` / F6M-F6P / I07 / N9 boundary (cross-references only; no new canonical T)
**Frozen return:** `ba20eeeea2243edd71febe0af0bc184d1cfeef1e::UNIFIED_LOG_R1/ZAK04S_CODEX_CAMPAIGN_R1`
**Verdict:** **REVISE_EXACT_DOCUMENTARY_DEFECT**
**Execution:** `NOT_RUN`; S0–S1 static source/documentary only.

## Claim under review

The return claims that the repaired F6M candidate is a real numerical partial-identification producer, F6P is its actual static consumer, I07 is a distinct permission guard rather than a numeric mixture, the protected N9 candidate is a synthetic progressive chain without F6M consumption, and a selected current F6 numeric receiver remains `NOT_PROVED`. It also claims a material alternative-cut difference: the predecessor adds the whole target-stratum share to uncovered when a present source is ineligible, while the repair uses proportional `missing_share`.

## What survives

1. **Repaired F6M output.** `1f1c72f883d0d7a6d11d7df8bad75c37d06c3ffa:WORKER_RETURNS/PYAT-R29-F6M-NATIVE-AUTHORITY-REPAIR-R1/candidate/rawlsing_next/pre553_heterogeneous_synthesis.py`, blob `2df811d76db258d98d89ffb43c830cb221ff9a7d`, `synthesize` L186, formula L307–L312, outputs L364, decision L380.
   - `planned = [s for s in sources if z in s["strata"]]`
   - `denom = sum(weights[s] for s in planned)`
   - `eligible_weight = sum(weights[s] for s in eligible)`
   - `missing_share = share * (1 - eligible_weight / denom) if denom else share`
   - `covered_share = share - missing_share`
   - `uncovered += missing_share`
   - Emits `covered_subprobability` and `uncovered_target_mass`; full distribution only when `uncovered == 0`; otherwise `PARTIAL_IDENTIFICATION_ONLY` / `NO_COMPLETE_TARGET_JOINT`.
2. **F6P static reader.** `016870e86913e6f7a811a51db6aba2d741bcfe58:WORKER_RETURNS/PYAT-R39-F6P-PARTIAL-BOUND-EVIDENCE-CONSUMER-R1/f6p_partial_bound_evidence_consumer.py`, blob `8fa992899293f454d7abded36831a4b4a362df8e`, `consume_f6m_evidence` L189. It imports F6M, verifies the bundle hash, checks `covered_sum + uncovered == 1` L235, rejects complete-with-uncovered, null-with-zero-uncovered, excluded-source-with-zero-uncovered L245, and prohibits model use. It is sourcefree/test-only, not a selected-world receiver.
3. **I07 is not the numeric producer.** `rawlsing_next/pre553_source_relations.py`, blob `5b67e3f98a5faf95a6c82700af2346fef6e306a5`, `guard_estimand_composition` L794–L834 returns `OperationGuardReceipt` after semantic-equivalence, overlap, and estimand-composition authority checks. It computes no mixture or uncovered mass.
4. **N9 candidate scope.** `rawlsing_next/pre553_n9_n10w_progressive_candidate.py`, blob `84d404147547767be8ecd4b6e1541f5fa3a8c8a2`, header and L60–L70: development-only synthetic 58-respondent A/B/C/Y progressive chain over N10E/C1/F8; no F6M import and no partial-bound shape. The historical header's broad “not implemented anywhere” statement is not fresh whole-machine evidence.
5. **World-serving alternative.** `pre553_universal_world_binding.py` blob `fdda8b2f887bd1fb7703bc5fb8ce1fefc52ca09d` and `pre553_evidence_world_consumer.py` blob `75ff3b9a73b1533c5fa6619e36577b69a4c65aed` consume R08 signed evidence, N10E slices, P41/sourcefree-world execution, and progressive conditioner prefixes. No F6/heterogeneous-synthesis/covered/uncovered token appears there or in `sourcefree_world/*.py`. Different input contract, not an omitted F6 receiver.
6. **Bounded F6 negative.** No protected `.py` hit for `covered_subprobability`, `uncovered_target_mass`, or `partial_identification`. This is not global absence.

## The defect

The return states:

> “The predecessor producer at `1428c2e9...` uses the older `uncovered += share` rule for a present-but-ineligible source; the repaired candidate ... replaces that with proportional `missing_share`.”

And in the case:

> “At L287 it adds the whole target stratum share to `uncovered` when a present source is ineligible (`uncovered += share`).”

The exact predecessor source is `1428c2e9:rawlsing_next/pre553_heterogeneous_synthesis.py`, blob `fc5e37fa5b2f0eb689593b42d95479d1327cb94c`, L284–L287:

```
denom = sum(weights[s["source_id"]] for s in eligible)
coverage[z] = { ... }
if not denom:
    uncovered += share
```

`denom` is the sum of weights of **eligible** sources. `uncovered += share` is inside `if not denom`, so it fires only when **no source is eligible** for that stratum. When some planned sources are ineligible but at least one is eligible, the predecessor sets `alpha = weights[sid] / denom` over survivors, renormalizes their weights to the full target share, and emits a complete distribution with zero uncovered mass. It does **not** add the whole target share for each present-but-ineligible source.

That is materially different from the stated trigger. The repair is still a real change: it computes `denom` over all **planned** sources, retains `missing_share` proportional to the ineligible planned weight, and adds it to `uncovered` instead of renormalizing it away. The downstream effect is important: the predecessor can produce a complete distribution while listing excluded sources, and F6P's `excluded-source-with-zero-uncovered` check would refuse that as `FALSE_FULL_COVERAGE`. The return’s broad conclusion (“material alternative-cut difference”) survives, but its factual description of the predecessor behavior and trigger does not.

A related reversal is in `MECHANISM_RECONCILIATION.tsv` edge `ZAK04S:MECH:R1:001`, `changed_mechanisms_and_semantics`: “Uncovered mass can be larger than repaired proportional rule.” For partial ineligibility, the predecessor’s uncovered mass is zero (it renormalizes onto survivors) while the repaired producer’s is positive; the repaired mass is the larger one. The predecessor is equal only in the all-ineligible/no-planned-source case. Correct the direction of that comparison as part of the same revision.

## Smallest exact revision

The same wrong predecessor claim is repeated across the 04 return. Correct it in all occurrences, not only the summary sentence:

- `00_RETURN.md` §1 (the “present-but-ineligible source” sentence) and §2.2 (the “when a source is ineligible” sentence).
- `CASES/ZAK04S_F6M_F6P_CURRENT_RECEIVER.md` §3 (the L287 sentence and the “an ineligible source contributes uncovered mass” refusal summary).
- `HUMAN_STORY.md` (the “handled an ineligible source by adding its whole target share” sentence).
- `DATA_SHAPES.tsv` rows `ZAK04S:SHAPE:R1:B_IN` and `ZAK04S:SHAPE:R1:A_IN` (“whole share of a present ineligible source goes to uncovered”).
- `OPERATION_TRACES.tsv` row `ZAK04S:OP:R1:BEFORE_A` (“add whole target stratum share ... when a present source is ineligible”; “any ineligible present stratum adds share directly”; “can overstate uncovered relative to repaired”).
- `MECHANISM_RECONCILIATION.tsv` edge `ZAK04S:MECH:R1:001` (both `historical_exact_behavior` and the reversed `changed_mechanisms_and_semantics`).
- `UNJOINS.tsv` row `ZAK04S:UNJOIN:R1:004` (the same present-but-ineligible premise).
- `EVIDENCE.tsv` row `ZAK04S:EV:R1:005` (the claim text).

The exact replacement wording is:

> When no source is eligible for a stratum, the predecessor adds the whole target-stratum share to `uncovered` (`if not denom: uncovered += share`). When some planned sources are ineligible but at least one is eligible, it renormalizes weights onto the eligible survivors, assigns no uncovered mass to the excluded present source, and may emit a complete distribution; F6P's excluded-source-with-zero-uncovered `FALSE_FULL_COVERAGE` check is the relevant downstream risk. The repaired candidate instead computes `denom` over all planned sources, retains proportional `missing_share = share * (1 - eligible_weight/denom)`, and adds that mass to `uncovered`.

Preserve all repaired-F6M, F6P, I07, N9, and bounded-negative findings unchanged.

## Secondary owner-facing observation (not an independent verdict trigger)

`F6M` lists a source with no table for a stratum in `excluded_sources` but does not include it in `planned`/`denom`, so it contributes no missing mass. `F6P._exclusions` (blob `8fa9928...`, L96–L111) collects every excluded source, and the `if exclusions and uncovered == 0` check (L240–L245) rejects it as `FALSE_FULL_COVERAGE`. A complete producer distribution can therefore be refused by its own static consumer when a source simply has no stratum table. This is not a contradiction in the return’s “F6P is a static reader” claim, but the owner should distinguish `NO_SOURCE_STRATUM` from `AGGREGATE_SUPPORT_OR_MASS_INSUFFICIENT` in the producer/consumer contract. Optional clarification.

## Verdict

**REVISE_EXACT_DOCUMENTARY_DEFECT** for lane 04. The defect is exact, bounded to the alternative-cut sentence, and does not reopen the accepted F6P/I07/N9/world findings. No runtime, scientific, or source authority is demanded.

## Evidence

`ZAK1057R2:EV:019`–`ZAK1057R2:EV:025`; searches `ZAK1057R2:S:012`–`S:016`; counterexamples `ZAK1057R2:CE:001` and `ZAK1057R2:CE:003`.
