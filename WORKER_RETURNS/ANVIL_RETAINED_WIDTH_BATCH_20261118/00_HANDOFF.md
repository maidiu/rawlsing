# Retained WIDTH128 actual prepared Batch

## Verdict

**PASS** — one actual `execute_saved_batch` on the sealed retained 128x600 WIDTH128 estate completed two distinct F2 operations in one prepared session, with full manifest coverage and exact receipt/fact refs matching the earlier qualified direct baseline.

This is reuse of the existing sealed WIDTH128 estate. No new estate, partial build, baseline rerun, benchmark pair, product edit, original source, or multi-country execution was used.

## Exact scope

- Fixture: `PYAT-1006-WIDTH128-600-20261118`
- Respondents/width: `128` respondents, `600` question bindings
- Manifest: `4d9604dc886ff9655ad25941fdcad2e412d18de4ab07c813524068c1dad09eea`
- Exact code snapshot: `aee95429609c372564e996c2d3d3eb30e9253cbf`
- Own repaired driver: `a716c208d16fa1e4dbc75e705bd4ab5df26f40cb`
- Earlier qualified baseline: `MEASUREMENT_PREP/WORKER_RETURNS/ANVIL_ROUTING_MATCHED_RUNNER_20261118/RUN_aee95429609c/baseline.json`
- One synthetic source-wave-country context: `SYNTHETIC_SINGLE_SOURCE_WAVE_COUNTRY_WIDTH128`; multi-country execution: **false**

## Preflight

`PRECHECK.json` records:

- exact WIDTH128 manifest and baseline manifest equality;
- exact I02/release pins;
- exact forward/reverse query and predicate refs matching the earlier qualified baseline;
- runtime catalog counts: 7 authorities, 5 predicates, 8 queries;
- exact current callback `width_current_scope.authorize`, which compares the runtime roots to the independently held WIDTH128 `ExternalI02Roots` (no permissive fallback);
- free space before execution: **48,008,728,576 bytes** (above 8 GiB).

## Actual run

One child process ran `full_width_batch_driver.py` using one actual
`execute_saved_batch` call over the existing catalog and sealed contract.

- Batch status: `COMPLETED`
- Coverage: `FULL_MANIFEST_COVERAGE`
- Units: 2 total, 2 completed, 0 failed, 0 deferred, 0 pending
- Prepared session builds: **1** (`session_scope.one_prepared_session=true`)
- Operations: distinct `f2_forward_raw` and `f2_reverse_raw` query/predicate refs
- Receipt/output refs: exact facts `ef761588...` (forward) and `516f4f0...` (reverse), matching the qualified direct baseline
- Provenance/replay: each completed receipt carries its unit/query/release/executor closure and the admission replay identity; operation-level full fact replay is not carried by Batch receipts
- Full fact payload and denominator/cell comparison: **NOT_CARRIED_BY_BATCH_RECEIPT**, left to the existing direct artifact/I03 API
- Runtime caps: child wall **47.815 s**, peak process-tree RSS **148,971,520 B**, peak scratch **323,143,200 B**; all below 240 s/6 GiB/4 GiB
- No retry after a started Batch failure; no Batch retry occurred.

## Artifacts

- `run_retained_width_batch.py` — preflight, exact provider/catalog construction, one-child supervisor with process-group termination and caps
- `width_current_scope.py` — exact test-only current callback
- `sealed_contract.json`, `runtime_catalog.json` — exact materialized inputs
- `PRECHECK.json` — exact refs/pins/catalog/free-space preflight
- `BATCH_RESULT.json`, `child.stdout.txt`, `child.stderr.txt` — actual result and raw child output
- `CAPS.json`, `VERDICT.json`, `run.stdout.txt` — raw caps/verdict
- `RECEIPTS.json` — compact exact operation/receipt summary
- `COMMANDS.md` — exact reproduction commands

No full-payload-in-Batch, multi-country, original/source, protected, production, or benchmark claim is made.
