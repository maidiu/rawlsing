# R61 R03 pre-code API / expected-set / coverage contract

Status: frozen before the R03 code commit. Sourcefree TEST_ONLY only. Inherits
R61AN acceptance, R61AF R01 decision, U53A contracts and the qualified R01/R02
components. No original source/science, R04/R05, CI/prod/N11/N12/Sorok/J52W52.

## Recovery

- Exact issued module recovered from
  `9bbf9e0509411beb210331d28160324b005a784e` candidate
  `pre553_issued_workload.py` blob
  `31e84f49d624f5524906e9e7839d2873106f8249`, custody semantics unchanged.
- B49 binding recovered from
  `b5600da96358f8526471d635a1befa8daa3f098b`
  `pre553_native_workload_binding.py` blob
  `bc88720c2bbcf52a43b799526c7dade094ccd9f8`, adapted only to the current
  `NativePreimageBundle` (`projection.authority_snapshots`, weight-slot optional
  descriptor) and current owner imports.
- Unchanged owners reused: C11, Route B, I03, I05, Batch, recursive handoff,
  R01 retained campaign, R02 projection. No replacement engine.

## API

`rawlsing_next/pre553_universal_workload.py`:

- `compile_universal_workload(*, bundle, as_of, host, purpose, measure_kind="RAW")
  -> WorkloadCompilation`
  Derives operations from `bundle.administered` and the projection response
  domains. No source-specific operation list, no selected question names.
  Each operation gets a stable `urn:r03:op:` identity binding source digest,
  occurrence identity, item/value, measure and as-of. Construction failures are
  retained as `UNSUPPORTED_RUNTIME` with exact reason; never dropped.
- `execute_universal_workload(*, compilation, source_factory)
  -> UniversalWorkloadResult`
  Executes each compiled TEST_ONLY issued workload through exact recovered U43
  (`execute_test_only_workload` -> Batch/RouteB/I03/I05/C11). Returns native
  results, exact operation IDs, receipt/fact refs and typed failures.
  `anti_join()` checks exact expected operation IDs (no counts-only).
- `bind_recursive_execution(campaign, execution_ref) -> RecursiveWorkloadFragment`
  Reads exact retained R01 campaign snapshot/activation preimage. Returns exact
  operation/rule, receipt, handoff, fact and release refs without issuing or
  rerunning discovery.

## Independent expected set

Tests compute expected `(source_variable_code, response_value)` pairs directly
from `bundle.administered` + projection response slots, before comparing
`WorkloadCompilation.operations`. No candidate output defines the oracle.
Native facts/receipts are actual existing-owner objects, not mocked booleans.

## Coverage

Positive: rectangular SAV repeated-occasion bundle; valid DTA person bundle;
exact Batch receipts/facts/no-drop; R01 D3 recursive execution consumed by
reference. Negative: cross-unit DTA refusal; wrong source edition -> failures
with no executed IDs; mutation/count-preserving substitution/duplicates fail
anti-join; restore returns original fact refs. Cold/replay: deterministic
recompilation same content hash and facts; deeper custody remains R04.
