# 06 — Independent review request (Phase-1 measured checkpoint)

**Requested from:** independent reviewer distinct from this author-controller.
**Grade sought:** sourcefree Phase-1 measurement and bounded gap-selection review.
**Not sought:** protected merge, native/original35 science, actor/Sorok scope,
producer acceptance, or a claim that C4 is complete.
**Production diff:** none. No `rawlsing_next` file was changed. A bounded P2
implementation is **not yet authorized** and is not part of this review.

## Artifacts to review

- `00_RETURN.md`
- `01_BASELINE_CURRENT_CODE_ABI.md`
- `02_EXACT_COST_AND_MEMORY_RESULTS.jsonl`
- `03_SAME_FACT_GROUPED_AND_KWAY_PARITY.jsonl`
- `04_REPLAY_AND_AUTHORITY_INVALIDATION.md`
- `05_OPTION_MATRIX_AND_MINIMAL_DELTA.md`
- `tools/bench_common.py`, `tools/bench_worker.py`, `tools/run_phase1.py`,
  `tools/finalize_phase1.py`
- `results/commands.jsonl`, `results/repeat_summary.json`
- Raw scenario JSON and repeat JSON under the untracked checkout-local
  `.local-logs/pyat-l03-c4/` (not committed; referenced for re-run comparison).

## Required review questions

1. **First consumer / call graph.** Confirm the actual measured entry is
   `CarrierNeutralResearchExecutor.execute_i03` (`pre553_carrier_execution.py:427`)
   and that `execute_route_b_production` (`pre553_route_b_production.py:582`) and
   the issued/Batch/I05 path are correctly described. Flag any invented reader or
   contract edge.
2. **Baseline identity.** Confirm the base commit
   `8ffec40a6924848a49f95950aa9ce28c27ee3ec1`, the assigned branch, and the current
   presence of PR684/PR686/selector-v1 behavior. Confirm that the external
   selector-v1 qualification commit is not represented as this worker's own run.
3. **Exact facts and oracle.** Independently select a subset of the 52 baseline
   facts in `03_SAME_FACT_GROUPED_AND_KWAY_PARITY.jsonl` and check:
   - exact typed state;
   - exact raw numerator/denominator and complete cell projection;
   - exact weighted fractions where authorized;
   - exact risk/denominator member identity;
   - exact fact/replay refs;
   - agreement with the declared existing-fixture oracle and the scaled synthetic
     arithmetic.
   No checksum-only oracle was used.
4. **Sharing claim.** Verify the measured statement that index reuse already
   exists after the first operation (`_build_release_index` count 1 then 0) and
   that the residual cost is per-operation risk/routing, predicate, target, and
   weight work plus per-operation fact/replay/provenance construction. Confirm the
   61–78% “shareable component” range is a component share, not an achieved
   speedup, and that P2 is marked NOT_IMPLEMENTED.
5. **No unsupported sharing.** Check the release/universe/risk/authority/weight
   separation evidence: two releases → two indices; two universes → two indices;
   one release/universe with different risk sets → one source index but different
   risk/denominator sets and facts; nonpositive authority → typed refusal;
   missing weight → typed refusal. Confirm no cross-scope result sharing.
6. **Replay/authority negatives.** Re-run or inspect:
   identical replay refs, replay mismatch refusal, cached-index fault repair,
   missing-release binding refusal, typed direct-I03 source-scope refusal,
   authority DENY refusal. Confirm none is laundered into a positive fact.
7. **Accelerator behaviors.** Check HIT/DELETE/CORRUPT/STALE/REVOKED evidence and
   exact material parity. Confirm the review does **not** read this as a new
   default-cache authorization or a semantic authority grant.
8. **Measurement method.** Check that clean timings are separate from instrumented
   attribution, that instrumented overhead/run noise is disclosed including
   negative deltas, that Darwin `ru_maxrss` is treated as bytes and as a
   process high-water mark, and that cold-start includes synthetic fixture build.
9. **Scope and claims.** Confirm no original35, native source/science, human,
   actor/V3, Sorok, protected CAS, or complete-C4 claim is made; confirm no
   invented weights/routing/denominators; confirm the `NOT_ADMINISTERED` contract
   limitation is stated rather than fabricating an I03 state.
10. **Recommendation.** Accept, reject, or narrow the Phase-1 recommendation:
    smallest warranted P2 execution-local grouped AND-risk/target kernel; P3
    bitmap/posting index deferred/not run; P4 existing compact accelerator retained
    with no new default/retention change. The reviewer should state whether the
    measured evidence is sufficient for HQ to grant a bounded production diff, or
    whether an additional sourcefree measurement is required.

## Suggested independent commands

Use the verified runner and checkout-local TMPDIR/cache; do not install packages.

```sh
RUNNER=/tmp/rawlsing-oct28-p1r1/venv/bin/python
TMPDIR="$PWD/.local-logs/pyat-l03-c4/review-tmp" \
PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 \
"$RUNNER" -m pytest -q -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_empirical_query.py \
  rawlsing_next/tests/test_pre553_carrier_execution.py \
  rawlsing_next/tests/test_pre553_c11_execution_view.py \
  rawlsing_next/tests/test_pre553_query_frontier_hostile.py
```

Then inspect and selectively re-run:

```sh
"$RUNNER" WORKER_RETURNS/PROGRAMMA-PYAT-L03-C4-20261105-R1/tools/bench_worker.py \
  --scenario frontier \
  --output .local-logs/pyat-l03-c4/review-frontier.json

"$RUNNER" WORKER_RETURNS/PROGRAMMA-PYAT-L03-C4-20261105-R1/tools/bench_worker.py \
  --scenario invalidation \
  --output .local-logs/pyat-l03-c4/review-invalidation.json
```

For the scaled timing, use a fresh cache root with mode `0700` and run one scenario
at a time; do not parallelize timed cases:

```sh
mkdir -p .local-logs/pyat-l03-c4/review-cache && chmod 700 .local-logs/pyat-l03-c4/review-cache
TMPDIR="$PWD/.local-logs/pyat-l03-c4/review-tmp" \
RAWLSING_C11_ACCELERATOR_DIR="$PWD/.local-logs/pyat-l03-c4/review-cache" \
PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 \
"$RUNNER" WORKER_RETURNS/PROGRAMMA-PYAT-L03-C4-20261105-R1/tools/bench_worker.py \
  --scenario main --n 1000 --kind native --pass-mode clean --repeats 4 \
  --output .local-logs/pyat-l03-c4/review-main1000.json
```

## Expected independent verdict fields

- `BASELINE_IDENTITY`: PASS / REVISE / UNKNOWN
- `EXACT_FACT_ORACLE`: PASS / REVISE / UNKNOWN
- `INDEX_REUSE_AND_SHARING_GAP`: PASS / REVISE / UNKNOWN
- `REPLAY_AUTHORITY_NEGATIVES`: PASS / REVISE / UNKNOWN
- `CACHE_BEHAVIOR_ATTRIBUTION`: PASS / REVISE / UNKNOWN
- `NO_UNSUPPORTED_CROSS_SCOPE_SHARING`: PASS / REVISE / UNKNOWN
- `P2_RECOMMENDATION_SUFFICIENT_FOR_BOUNDED_DIFF`: YES / NO / NARROW
- `P3_P4_DISPOSITION`: CONFIRM_DEFER / REQUIRE_MORE / REVISE
- `SCOPE_CLAIM_SAFETY`: PASS / REVISE
- `NEXT_WORK`: `REUSE_ADAPT_P2` / `MORE_MEASUREMENT` / `NO_ACTION`
