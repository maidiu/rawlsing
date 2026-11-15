# DDM VOSKRES #1059 — R2 composed author return

**Candidate:** `docs/voskres1059-r2-composed-author-20261115`
**Frozen R1 input:** `819dc54c69633dd75b6d13ac0ee8c3bbfd624853`
**Original source pin:** `25830fe7462bb9e29bc4087e6ae14f3f84cec377`
**Modern cuts inspected:** spec `b9325f094b27d28c20006af9780a91b3254dcab8`; FORGE `3e0ed0794498506520ae62c997a5c852ac672061`
**Write scope used:** `WORKER_RETURNS/DDM_VOSKRES1059_R2/` only
**Grade:** `DOCUMENTARY_SOURCE_ONLY_CANDIDATE / NOT_ACCEPTED / G5_NOT_PERFORMED`
**Status:** `FROZEN_CANDIDATE_FOR_HQ_DISTINCT_REVIEW`

## 1. Custody and inputs read

Read the mandatory `sources/1059_METHODOLOGICAL_CORRECTION.md` (6890316242) plus frozen R1 A/B/HQ returns, their ledgers, reconciliations and source ledgers. Reused existing ZAK02/03/04 references and the banked G1A C4R1 V550J/V551J/V552J information-conservation return/crosswalk; no new A/B inventory, clone, archive extraction, broad ZAK census, raw data, test, CI, product edit or scientific execution was performed.

No A/B/HQ R1 file was edited. This pass added only the R2 files listed in `MANIFEST.json`.

## 2. G1 — canonical machine-cell corrections

`G1_CANONICAL_ACCOUNTING.tsv` records ten explicit supersessions, including:

1. **Not all-pairs O(k²):** V550 secondary scoring does one k-candidate scan, selects one primary by max(MI, Cramér's V, n), then evaluates at most k−1 remaining candidates against that primary (`ddm_v550_branching.py:209-265,269,276-289`). At k≤12 this is ≤11 candidate-vs-primary joint evaluations, not all pairs.
2. **Depth 3 is a default, not a universal cap:** `branch_nodes_rows(..., max_depth: int = 3)` and `--max-depth` default 3; recursion stops on depth/support/remaining-indicator/no-gain. `pure_or_near_pure` is a label, not the early-return test (`branching.py:372,391,397-399,419-425`; `build_determinicity_wave_shard_v550.py:856,1633`).
3. **Not existence-only resume:** the skip decision requires the complete marker, a readable nonempty `question_use_contract` parquet, a nonempty saved hash, and equality with the recomputed question-use-contract hash (`build_determinicity_repository_v550.py:963-992`; shard `:1509`). Scope limit is explicit: one table plus marker, not every checkpoint body/source version.

These are machine cells, not narrative caveats. The A/B first-pass files remain immutable and are superseded here only.

## 3. G2 — composed graph

`G2_COMPOSED_GRAPH.tsv` contains 21 edges for:

- ordinary `V550 → V551 → V552` (extraction/preparation, distributions, bridge lanes, adjudication/atoms/coverage, pressure/structural facts);
- joint `V550J → V551J → V552J → V553` (prepared substrate, same-person patterns, exact V551 atom matching, component/certification, producer-bound join, V553 canonical/probe consumption);
- explicit `551 → 551J` edge: V551 atoms are matched into components, while the **V551 conditional index is not an input to V551J**;
- explicit `552 → 552J` edge: V552 structural facts and temporal-key source index are verified inputs; V552 conditional determinicity is not an input;
- all inspected actual V553 inputs are listed separately in `G2_V553_INPUTS.tsv`: V552J input/handoff indexes, readiness, V552 structural/temporal indexes, authority overlays, thin readiness, harmonization sidecar, and upstream V551J provenance pointer (not dereferenced).

Key boundary found: V552J carries a reduced carrier. It does not load the V551J component index or same-grain component vectors; V553 canonical adapter does not dereference V551J. This is consistent with prior C4R1's seven information-loss gaps, which are cited as banked prior evidence rather than re-proved numerically.

## 4. G3 — one selected respondent-joint path

`G3_SELECTED_JOINT_PATH.md` reconstructs one concrete path:

`V550J same-person pattern → V551 directional atom → V551J certified joint packet → V552 structural pressure fact → V552J exact-scope join → V553 canonical/probe consumer`

It gives the exact input grain, computation/formula, output fields, scientific gain, loss/refusal, qualification and actual consumer at each stage. Critical numerical semantics:

- V550J pattern counts/probabilities/support use multiple explicit denominators; its `mutual_information` field is a scaled log-ratio, not joint MI.
- V551 atom promotion is restricted to the two direct distribution tables; derived determinicity is excluded.
- V552 pressure requires a unique positive respondent denominator and computes `Σ(normalized_weight × canonical_signed_component)` in [-1,1]; heterogeneous/absent denominator is unresolved, not renormalized.
- V552J ALLOW requires exact scope, semantic match threshold, certified lane, both producer permissions ALLOW, fact permission ALLOW and observed pressure; temporal field is never allowed.
- V553 canonical consumer verifies join/input/handoff equality and declared probe/temporal counts; temporal pressure remains `probe_only`, with `temporal_field_allowed=False`.

**Historical row status:** `NOT_AVAILABLE`. No V551J/V552J/V553 output row or positive-load run exists in authorized non-raw custody; prior C4R1 records 0/9 positive-load scopes and missing respondent substrate. The path is `SOURCE_EXECUTABLE`, not `HISTORICAL_EXECUTED`. No numeric historical count/score/id is invented.

## 5. G4 — old → FORGE and the conditional index

`G4_OLD_TO_FORGE.tsv` maps old mechanisms/products to modern actual products, first readers/call sites and evidence:

- old per-country/prepared reuse → modern `I03GroupedExecutionScope` + `execute_empirical_query`, with cold `DirectEstateI03Session` group refusal at the inspected cut;
- old direct distributions → modern exact marginal `EmpiricalFact`, consumed by `execute_empirical_query` and analytical composition;
- old indicator/secondary MI → modern exact arity-2 `GovernedDiagnosticProduct`, explicitly diagnostic-only and different grain;
- old recursive/outlier products → modern exact bounded discovery/I05 route, `COMPARE_UNKNOWN` for full product parity;
- old V550J/V551J/V552J/V553 joint products → modern exact joint facts + C1 composition are related, not same-grain; prior C4R1 seven gaps remain held;
- old checkpoint guard → modern batch/release receipts are related but not parity-proved.

`G4_CONDITIONAL_INDEX_TRACE.md` independently traces the V551 conditional index producer/eligibility, bridge metadata, V552 accept-but-unused socket, V551J non-ingestion, and prior PROGRAMMA `NO_CURRENT_MATCH_VERIFIED` row. Disposition: `HELD_LOCAL_UNCONSUMED_AUXILIARY_CAPABILITY_WITH_NO_PROVED_HISTORICAL_PRODUCER_OR_READER`. Local V552 non-use is **not** promoted to global loss; V551J existence is **not** treated as conservation; name/function similarity is **not** equivalence.

## 6. Self-critical held edges

`SELF_CRITICAL_HELD_EDGES.tsv` records 14 explicit holds, including: no historical execution row; no old runtime/cardinality; no causal proof that old sharing caused modern cost loss; old MI population mismatch and V550J MI mislabel; no modern same-grain V551 atom/J carrier; grouped cold estate not qualified; conditional index external-caller possibility remains `NOT_INSPECTED`; source inspection alone proves no functional conservation.

## 7. What is not claimed

No `ACCOUNTING_COMPLETE`; no functional-conservation execution; no historical-runtime superiority; no native/modern equivalence; no production adoption; no science/source right; no G5 acceptance; no protected merge; no CI/test/product change. This is one frozen documentary candidate for HQ intake and a distinct source-aware reviewer.

## 8. Publication note for HQ

The worktree already showed all tracked R1/root files as deleted (`git status` `D` entries) before this pass; this return did not delete or modify them. Because the worktree checkout is sparse/empty, **stage only `WORKER_RETURNS/DDM_VOSKRES1059_R2/`** when publishing; do not `git add -A`, which would commit pre-existing deletions of A/B/HQ R1 and root files. No git commit was made in this pass; HQ publishes if commit is unavailable to the author.

## 9. Next action

HQ terminal intake → distinct source-qualified adversarial G5 reviewer against this frozen candidate. One candidate, no self-G5, no new A/B survey, no additional discretionary hardening. Stop at accepted scope or exact reproducible defect/HOLD.
