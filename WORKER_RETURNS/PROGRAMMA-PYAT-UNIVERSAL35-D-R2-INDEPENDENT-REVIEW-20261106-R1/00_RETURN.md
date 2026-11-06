# Universal35 D r2 — independent exact-frontier closure

**VERDICT: ACCEPT_SCOPED_ENGINEERING** at frozen D head `a31175cbd1371c599e2855e150ba3beb877c4ed4`.

- Code: `7b0ac186a8b0e27e26ebcc9c4d0e1f57f36597ae`
- Prior input: `017337a9e1edafcbcdbaf538eac9c2c91f7d0791`
- Prior F review read: `f2c477cee7535bad6103a5353f220a7eddd73a99`
- Actual D r2 return read: `WORKER_RETURNS/PROGRAMMA-PYAT-UNIVERSAL35-D-20261106-R1/02_R2_RETURN.md`
- Review branch: `codex/pyat-universal35-d-r2-frontier-review-20261106-r1`
- Published review head: the commit containing this directory; exact SHA reported in final delivery.

## FINDING

The observed R2 repair closes the F r1 extra-frontier acceptance. `bind_governed_frontier` rebuilds the explicit plan-derived inventory/policy/frontier, requires exact content-hash equality, compares operation `(op_id, material)` counters, and refuses extras, substitutions, duplicates and missing operations before compilation. Exact restore returns the baseline hash.

The intentional plan value/conditioner mutation with rebuilt inputs still changes real compilation, expected jobs and executed facts; exact restore returns the baseline facts/hash. The exact-frontier identity check therefore does not neuter genuine planned changes.

All35 accounting is concrete: 35 source rows, 20 explicit non-F1 frontier sources, 15 typed no-request rows, 991 frontier operations (21 eligible / 970 held-or-unknown), with all 35 retaining non-zero F1 paths and zero invented F2-F4 requests in the 15 no-request rows. Plan totals are 18,276 items / 18,413 slots / 18,467 operations. Route evidence is 676 qualified / 4,705 unknown / 249 unavailable, not 5,630 route-qualified.

Prior F ID/physical-code and unknown-route proofs remain covered by the unchanged identity test and the passing focused suite. Native wrapper direct read, default-3, arbitrary coordinate, synthetic ID/person unit remain explicit **HOLD**.

## GRADES

- **Exact frontier: PASS_SCOPED.** Extra, substituted material/identity, duplicate and missing supplied operations refused; exact restore succeeds.
- **Planned mutation: PASS_SCOPED.** Rebuilt plan mutation changes compilation, jobs and facts; restore exact.
- **All35 accounting: PASS_SCOPED.** 35/20/15, 991/21/970, 18,467/18,413/18,276, F1 retained, no invented requests.
- **Route labels: PASS_SCOPED.** 676/4,705/249; candidate raw 5,630 remains separate.
- **First consumer: PASS_SCOPED_COMPILER_BINDING.** `compile_governed_frontier` is reached only through the exact plan-derived frontier; native facts/FieldForge/science remain **NOT_RUN/HOLD**.

## LIMITS / PRESERVATION

- Tests: **8 passed** in 31.10s. No full-state 35 fixture floor, original 600s decode, A/C/E edit, guide/progress/controller/protected merge, or native/science/protected promotion.
- F prior `f2c477cee…` accepted ID and unknown-route subscopes are reused where the observed code path is unchanged.
- Native wrapper residuals remain HOLD: direct decode/read, `max_items=3` default, arbitrary coordinate fallback, synthetic original IDs/person unit, no empirical facts.
- DTA/original-scale and D 600s end-to-end remain **NOT_RUN**. Sourcefree configs do not establish those.
- No code repair by this reviewer. No original respondent rows/bytes or absolute source root in Git.
