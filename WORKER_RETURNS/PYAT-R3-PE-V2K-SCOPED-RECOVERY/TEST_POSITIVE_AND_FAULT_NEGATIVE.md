# PE / V2K positive and fault-negative receipts

**Sourcefree only.** No original survey/response, native source, actor/world permission, production source or PRE-MAIN mutation was used. Tests were run in isolated extracted trees; no arbitrary branch executable or production merge was performed.

## PE — original source (e61a26ce, blob `58484f4c...`)

| Court | Command | Actual result |
|---|---|---|
| Author suite | `PYTHONPATH=. PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q rawlsing_next/tests/test_postastra_pe_generic_world_possibility.py` | **21 passed**, exit 0 |
| Independent strict | `HQ297_EXACT_PE_ROOT=<exact-tree> ... pytest -q rawlsing_next/tests/test_hq297_k9k10_sc0_pe_independent.py` | **4 passed / 9 failed**, exit 1 |

The 9 independent failures include `test_strict_reverse_scoped_issuer_forgery_must_refuse` and eight strict SC0 value-bearing/schema failures. The nine failures are preserved, not xfailed.

## PE — repaired candidate (candidate blob `31de8f21...`)

The candidate changes only the serve role-reversal competence boundary: a non-null caller `AuthorityRef` is no longer sufficient; the exact `TARGET_USE_PERMISSION` snapshot must be present in the issuer registry, positively scoped to `REVERSE_TARGET_VALUE_TO_SUBJECT`, target use and denominator/risk set. `_auth` remains shape normalization only. Typed/schema helpers are unchanged.

| Court | Command | Actual result |
|---|---|---|
| Author suite | same author command with the repaired candidate on `PYTHONPATH` and the exact reversal authority registered in the sourcefree fixture; the registration patch is `candidate/PE_TEST_FIXTURE_AUTHORITY.patch` | **21 passed**, exit 0 |
| Independent strict, repaired candidate | same 13 assertions; only the test's module-blob pin changed from `58484f4c...` to repaired `31de8f21...` | **5 passed / 8 failed**, exit 1 |
| Candidate competence test | `pytest -q tests/test_pe_reversed_issuer_repair.py` | **2 passed**, exit 0 |

The repaired independent run proves the reversed-issuer forgery is now refused. The remaining 8 failures are the strict SC0 value-bearing/schema requirements that the whole PE contract does not implement (`clocks`, `scoped_status_rows`, `structural_publication_refresh_receipt`, `n9_values_read_receipt`, `generic_consumers`, N9/F2/AH strata). They are **not** silently repaired or xfailed. Engineering verdict for the whole PE contract remains **RED/HOLD**; the `_auth` negative is closed at its exact scope.

## V2K — exact historical dependency restored

V2K original tip `694fb450...`; source blob `e3ef9a24...`. The branch alone cannot collect because it lacks:

- `pre553_original_workload_contract_v2_candidate.py` `08bb75c4...`
- `pre553_original_workload_binder_candidate.py` `7d8b3902...`
- `pre553_v2_durable_consumer_integration_candidate.py` `dc146e92...`
- `pre553_original_workload_v2_verifier_candidate.py` `996c8e90...`
- `pre553_batch_durable_checkpoint_candidate.py` `719c8d87...`
- dependency test helpers `test_pre553_original_workload_contract_v2_candidate.py` `0b9f1add...` and `test_pre553_v2_durable_consumer_integration_candidate.py` `3218f280...`

These exact blobs were restored only in the isolated test tree, not transplanted into current source. The exact `PV_RETURN` oracle directory was extracted from `694fb450`.

| Court | Actual result |
|---|---|
| Four V2K suites (`test_hq295...`, `test_hq294...actual_scope`, `test_hq294...identity_court`, `test_postastra_pv_v2k_independent.py`) | **63 passed**, exit 0 |
| `test_hq295_v2k_original_identity_successor.py` alone (24 candidate suite) | **24 passed** |
| Exact dependency/owner suites (`test_pre553_original_workload_contract_v2_candidate.py` + `test_pre553_v2_durable_consumer_integration_candidate.py`) | **50 passed / 1 failed**, exit 1 |
| Without restored dependency | **collection error**, exit 2: `ModuleNotFoundError: pre553_original_workload_contract_v2_candidate` |

The single dependency-suite failure is `test_no_accepted_owner_modifications`: it checks `git diff` of `pre553_route_b_production.py` against historical commit `0f8c6d08...` in the current tree, which is not the exact historical worktree. It is a source-cut/environment check, not a V2K semantic failure. The reported **111 owner-test aggregate** is not available as one exact suite at this branch cut; 50 exact dependency tests were available, with that one source-cut check failing. No claim of 111/111 is made.

## Negative dependency-severance tests

`tests/test_v2k_dependency_severance.py`:

- current `pre553_issued_workload.py` does **not** expose `V2ExpectedWorkDeclaration`, `v2_bind_semantic_to_dispatch` or `V2_SCHEMA_VERSION`;
- blocking the exact historical dependency makes V2K import fail closed.

Result with a combined current-ABI + V2K-source tree: **2 passed**, exit 0.

## Not run / unavailable

- Full SC0 K9 8/K10 28 strict court: **NOT_REACHED**.
- 111-test V2K owner aggregate as a single exact suite: **NOT_AVAILABLE_AT_THIS_CUT**.
- Native source/U/E, original scientific rule, N9/N10W operative world, actor/person, PRE-MAIN integration: **NOT_RUN / NOT_ISSUED**.
- No failing assertion was skipped, xfailed, or replaced to obtain green.
