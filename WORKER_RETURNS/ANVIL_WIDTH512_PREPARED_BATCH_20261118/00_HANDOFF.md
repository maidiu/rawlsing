# WIDTH512 prepared Batch qualification

## Verdict

**PASS — one actual sourcefree prepared Batch on the sealed WIDTH512 estate.**

- Estate: `PYAT-1006-WIDTH512-600-20261118`, **512 respondents × 600 questions**
- Manifest: `984814f820fea4eba983f5f1fd4ce02c3e45371e879e2e9c910dcdd0f0b4b348`
- Accepted code snapshot: `aee95429609c372564e996c2d3d3eb30e9253cbf`
- Existing driver: `a716c208d16fa1e4dbc75e705bd4ab5df26f40cb`
- Owner harness start: `61642f98be5c10f22a4b117a8cc759c33a0c41ba`
- Runtime catalog: derived from the existing WIDTH512 fixture/query provider; 7 authorities, 5 predicates, 8 queries.

This is reuse of the sealed artifact only. No new estate, partial build, governed source, science, protected write, product edit, paired benchmark, or retry after native start.

## Actual execution

- One `execute_saved_batch` call on the retained artifact
- Fresh child process, exactly one authenticated prepared `_build`
- Batch: `COMPLETED`, `FULL_MANIFEST_COVERAGE`, 2 total / 2 completed / 0 failed / 0 deferred / 0 pending
- Distinct forward/reverse F2 query and predicate identities derived from WIDTH512
- Receipts:
  - forward receipt `PRE553BatchExecutionReceipt@1.0.0|…:3fdb2c3c66d6aaf824ace68545e191ce07403d8b1ee076a86ebdd9d8a98e7a97`
  - reverse receipt `PRE553BatchExecutionReceipt@1.0.0|…:734003f6ff849023065973af02c92b37de9791427e11365aeb0f2ffa5078cb19`
- Result refs (exact Batch receipt content):
  - forward `EmpiricalFact@1.0.0|…:2d873efea3d535877adc0d682df1ba777e873fc0fb50929aec973e7958ffd071|…`
  - reverse `EmpiricalFact@1.0.0|…:6326a2f135fc1e6b804c1f531085797dab66115a7b4d6a83b6c75259f0260ed3|…`
- Exact query/predicate refs and receipt refs are in `BATCH_RESULT.json` and `RECEIPTS.json`.

`baseline_status` is **NOT_AVAILABLE**: no WIDTH512 direct baseline or retained WIDTH512 fact oracle was provided, and I did not run another heavy oracle or reuse WIDTH128 operation IDs/results. Receipt refs are exact; full content is not independently verified by a WIDTH512 oracle and is not carried in Batch receipts. Full payload/denominator comparison remains explicitly unavailable from Batch.

## Caps and gates

- Child wall: **197.351 s** / 600 s
- Peak process-tree RSS: **192,561,152 B** / 6 GiB
- Peak scratch: **1,292,461,600 B** / 4 GiB
- Free space before start: **44,735,545,344 B** / ≥8 GiB
- No competing WIDTH512 writer/heavy process detected at preflight
- Process-group termination armed; no abort and no retry after native start.

## Exact preflight

- Manifest SHA-256 equals the contract and its 14 member hashes verify
- Manifest I02, release, and family counts equal the contract
- Exact external I02/release pins recorded
- Single synthetic source-wave-country context; multi-country execution **false**
- Exact current callback compares runtime roots against the independently held WIDTH512 `ExternalI02Roots`; no permissive fallback
- Query/predicate refs are distinct and derived from WIDTH512, not WIDTH128

## Evidence

- `run_width512_batch.py` — exact preflight, catalog materialization, one-child supervisor and caps
- `width512_current_scope.py` — exact current callback
- `sealed_contract.json`, `runtime_catalog.json`
- `PRECHECK.json`, `BATCH_RESULT.json`, `RECEIPTS.json`, `CAPS.json`, `VERDICT.json`
- `child.stdout.txt`, `child.stderr.txt`, `run.stdout.txt`, `COMMANDS.md`, `MANIFEST.json`

No full-payload-in-Batch, WIDTH512 content-oracle, multi-country, production, or benchmark claim is made.
