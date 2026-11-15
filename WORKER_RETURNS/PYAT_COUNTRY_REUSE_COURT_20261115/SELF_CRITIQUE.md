# Self-critique and explicit holds

This court is deliberately narrow. The following limits are part of the result, not caveats to be waived. The independent G5 `c5a71fcc59a45aa470720159a334ae57f365de11` accepted the measurement at sourcefree scope and returned `REVISE_EXACT_DEFECT` for the earlier handoff; this file is part of the corrected documentary handoff, not self-acceptance.

## Measurement limits

1. **100, not 1,000, distinct cold operations.** The author's 100-op wall (51.929 s) linearly projects **519.29 s** for 1,000 distinct cold operations; the independent review's 65.661 s projects **656.61 s**. Both are `EXTRAPOLATION_NOT_MEASURED` and over the 300 s budget. The 1,000-repeat probe on the in-memory grouped path is explicitly `REPEAT_INVOCATIONS_NOT_DISTINCT_OPERATIONS` and is not a 1,000-distinct-operation claim. No 1,000 five-minute query was run.
2. **Synthetic 128-respondent estate, not original35.** The fixture is sourcefree and test-only. It is not a real country extract, not source rights, and not a bridge for #997. The country/wave/source shape (`SURVEY`, `US`, `W1`) is a fixture label, not scientific authority.
3. **Only 5 questions and a finite distinct-op space.** The 100 operations are 80 distinct condition/target cores plus 20 governed-weighted measure variants. The 20 variants are distinct estimands, but only 20/100 share an exact core; the other 80 do not. No `100` was inflated with identical jobs; repeat invocations are separately labelled.
4. **Not every routing state is on the saved estate.** The accepted #1006 fixture generates typed `MISSING` B, routed sparse `NOT_ELIGIBLE` D/MR, repeated MR and zero cells, but not `UNKNOWN` or `INAPPLICABLE` routing. The production special-state/zero-support test matrix passed (16 focused tests author and review); this court does not claim those states were re-measured on the saved estate.
5. **Wall/CPU are contended; there is no stable throughput constant.** The author's one frozen pass was 51.929 s cold and 1.021× grouped; the independent review's one pass was 65.661 s cold and 1.199× grouped under lower preflight load with identical facts/counters. The author's earlier “three passes / stable ~51.9–52.2 s” sentence was unfrozen and is withdrawn. Do not present these as clean isolated performance claims. Core receipts, exact counters, fact hashes and guard messages are the strong evidence.
6. **Instrumentation changes overhead.** Session/row-group/object counters are runtime wrappers; they add some overhead and are not present in the native in-memory baseline. The cold counters are exact call counts, but the wall includes instrumentation. The `_build` share (~12.3–12.4%) is instrumentation-inclusive, not a full phase time decomposition.
7. **Compressed/uncompressed bytes are metadata-sum proxies.** They are summed from Parquet row-group column-chunk metadata for each `read_row_group`; they are not physical I/O counts or decompression timings. Page cache/filesystem behavior is not instrumented. Intra-session row-group cache-hit counts are not instrumented; cross-operation reuse is zero by construction (new session per op).
8. **Process-tree RSS is an inference, not a sampled tree high-water.** The code sets `max(before tree snapshot, after tree snapshot, self ru_maxrss)`. No child processes were created by the probes. In the author data the tree sample (137,236,480 B) differs from self `ru_maxrss` (136,503,296 B) by 733,184 B; they are not equal. The review pass had equality, but that is not a general invariant.
9. **Object materialization counts are native work, not tripwires.** The 94,068 family and 29,343 event `_object_from_row` calls are actual evaluation materializations. The real negative tripwires are `C11Repository.__init__` = 0 and `pq.read_table` = 0. The cold path materializes row-level family/event objects as expected; that is not a full-object-first reopen.
10. **Source-open is INAPPLICABLE, not a measured zero.** The fixture is synthetic/sourcefree; the cold path reads the saved Parquet estate. There is no original source file to open, so source-open is not a tripwire. The real tripwires are the two above.
11. **No changed/restore on this 128 estate.** Exact cold/native parity and the state probe are measured; the accepted #1006 harness's changed/restore evidence is separate and not re-run. A future reader change must add changed/restore and mid-batch revocation.
12. **Measurement acceptance is not broader qualification.** The independent review accepted the sourcefree measurement. It did **not** grant production, security, science, original35, J3/new governed QUERY issuer, optimized-engine, protected-merge or #998 integration acceptance.

## Handoff and authority limits

13. **B is a hypothesis, not a measured candidate.** There is no B implementation, B patch or B A/B run in the frozen evidence. The court measured the cold-cost target that motivates B. A bounded owner-approved B measurement is required before any gain claim or production choice. The earlier claim that B was a measured candidate is withdrawn.
14. **#999 chronology is corrected.** The native repair `ce7704253f6a2381310c3eb2c7412a2d85c5596c`, accepted at `c18b7e087d5d5b178ed5acc92f9c82250a1743de`, was created after this author started and is **not adopted** in the `9d96a9c…` measurement cut. The old baseline is a valid-fixture benchmark only, not adversarial security qualification of the accepted successor. Any J1/B production work must adopt/qualify the accepted successor under the owner's exact reader/evaluator/file grant; it must not wait for a new #999 acceptance.
15. **No production edit, no guard removal, no bypass.** Both cold grouped guards were exercised as refusals only. The direct index inspection was read-only and did not call the grouped cache. No production/tests file was edited.
16. **No science/eligibility change, no original35, no governed QUERY issuance.** The 100 queries are TEST_ONLY sourcefree operations. J3's governed QUERY issuer remains separate. No source rights, no original35 inference, no science permission.
17. **No new index/store/engine, no full-object-first reopen.** The cold path builds no full `C11Repository` (tripwire 0) and does no whole-table read (0). The native in-memory `C11Repository` was built only as a parity oracle, not as a cold consumer or a grouped positive.
18. **No 100k/10k rerun.** Prior accepted #1006 same-estate 100k/10k locality/writer evidence is cited only as prior context. The three `_pre553_query_eval.py` respondent-sort candidate is not implemented or authorized; a `_respondent_family`-only grant would not authorize it.
19. **No protected merge, no #998 integration, no #1007 rights.** This return is a bounded performance/contract court, not product integration.

## What could falsify this return

- A cold saved grouped call that succeeds through a lawful public interface without the missing release/index identity contract, or a guard that is actually absent at the tested head.
- A 100-op cold/native mismatch, a fact/replay/release drift, or a collapsed `MISSING`/zero/`UNKNOWN`/`INAPPLICABLE` state.
- Evidence that the 100 query refs are not distinct, or that the 20 measure variants are counted as independent scientific claims without disclosure.
- A 1,000-distinct cold measurement inside the budget that contradicts the 519.29/656.61 s projections.
- A production/test edit or guard bypass in this return.
- A grouped in-memory result that is not exact or whose core receipts do not match the stated 80/20 or 64/20/16 counts.
- A B performance claim without a B implementation/run and a bounded owner-approved measurement.

If any of these occurs, this return should be `REVISE_EXACT_DEFECT` or `HOLD`, not accepted.
