# Self-critique and explicit holds

This court is deliberately narrow. The following limits are part of the result, not caveats to be waived.

## Measurement limits

1. **100, not 1,000, distinct cold operations.** The measured 100-op wall (51.93 s) linearly projects 519.3 s for 1,000 distinct cold operations, over the 300 s budget. The 1,000 figure is `EXTRAPOLATION_NOT_MEASURED`. The 1,000-repeat probe on the in-memory grouped path is explicitly `REPEAT_INVOCATIONS_NOT_DISTINCT_OPERATIONS` and is not a 1,000-distinct-operation claim. No 1,000 five-minute query was run.
2. **Synthetic 128-respondent estate, not original35.** The fixture is sourcefree and test-only. It is not a real country extract, not source rights, and not a bridge for #997. The country/wave/source shape (`SURVEY`, `US`, `W1`) is a fixture label, not scientific authority.
3. **Only 5 questions and a finite distinct-op space.** The 100 operations are 80 distinct condition/target cores plus 20 governed-weighted measure variants. The 20 variants are distinct estimands, but only 20/100 share an exact core; the other 80 do not. No `100` was inflated with identical jobs; repeat invocations are separately labelled.
4. **Not every routing state is on the saved estate.** The accepted #1006 fixture generates typed `MISSING` B, routed sparse `NOT_ELIGIBLE` D/MR, repeated MR and zero cells, but not `UNKNOWN` or `INAPPLICABLE` routing. The production special-state/zero-support test matrix passed (16 focused tests); this court does not claim those states were re-measured on the saved estate.
5. **Wall/CPU are contended.** Pre-timing load average was 4.52/4.41/3.95 on 16 CPUs; no other Rawlsing processes were observed. Three same-command in-memory grouped passes varied around 1.02×–1.26×. The cold 100-op wall was stable at ~51.9–52.2 s, but still ambient-contended. Do not present these as clean isolated performance claims. Core receipts, exact counters, fact hashes and guard messages are the strong evidence.
6. **Instrumentation changes overhead.** Session/row-group/object counters are runtime wrappers; they add some overhead and are not present in the native in-memory baseline. The cold counters are exact call counts, but the wall includes instrumentation.
7. **Compressed/uncompressed bytes are read-amplification proxies.** They are summed from Parquet row-group column-chunk metadata for each `read_row_group`; decompression itself was not separately timed. Intra-session row-group cache-hit counts are not instrumented; cross-operation reuse is zero by construction (new session per op).
8. **Process-tree RSS is effectively single-process.** No child processes were created by the probes; the process-tree peak equals the self max RSS. This is not a multi-process server measurement.
9. **No changed/restore on this 128 estate.** Exact cold/native parity and the state probe are measured; the accepted #1006 harness's changed/restore evidence is separate and not re-run. A future reader change must add changed/restore and mid-batch revocation.
10. **No independent G5.** This is author evidence. `G5_REVIEW_PENDING.md` lists the required distinct review. No self-acceptance.

## Authority and scope limits

11. **No production edit, no guard removal, no bypass.** Both cold grouped guards were exercised as refusals only. The direct index inspection was read-only and did not call the grouped cache. No production/tests file was edited.
12. **No #999 bodytruth successor.** The #999 S2-A native body-truth G5 is still pending. Any native reader/evaluator production change requires the accepted immutable successor plus the owner's exact file/symbol grant. This court is not that grant.
13. **No science/eligibility change, no original35, no governed QUERY issuance.** The 100 queries are TEST_ONLY sourcefree operations. J3's governed QUERY issuer remains separate. No source rights, no original35 inference, no science permission.
14. **No new index/store/engine, no full-object-first reopen.** The cold path builds no full `C11Repository` (tripwire 0) and does no whole-table read (0). The native in-memory `C11Repository` was built only as a parity oracle, not as a cold consumer or a grouped positive.
15. **No 100k/10k rerun.** Prior accepted #1006 same-estate 100k/10k locality/writer evidence is cited only as prior context. The three `_pre553_query_eval.py` respondent-sort candidate is not implemented or authorized; a `_respondent_family`-only grant would not authorize it.
16. **No protected merge, no #998 integration, no #1007 rights.** This return is a bounded performance/contract court, not product integration.

## What could falsify this return

- A cold saved grouped call that succeeds through a lawful public interface without the missing release/index identity contract, or a guard that is actually absent at the tested head.
- A 100-op cold/native mismatch, a fact/replay/release drift, or a collapsed `MISSING`/zero/`UNKNOWN`/`INAPPLICABLE` state.
- Evidence that the 100 query refs are not distinct, or that the 20 measure variants are counted as independent scientific claims without disclosure.
- A 1,000-distinct cold measurement inside the budget that contradicts the 519 s projection.
- A production/test edit or guard bypass in this return.
- A grouped in-memory result that is not exact or whose core receipts do not match the stated 80/20 or 64/20/16 counts.

If any of these occurs, this return should be `REVISE_EXACT_DEFECT` or `HOLD`, not accepted.
