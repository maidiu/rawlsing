# SRC16 I03 -> I05/Batch trace

Isolated TEST_ONLY receiving evidence for the exact unresolved native I03
output described in `ANVIL_SRC16_SHARED_SQLITE_FREE_RUNNER_20261119`.

- base: `1f8b61b81`
- source: existing sourcefree prepared-saved fixture and existing native owners
- no original source, config, grant, private artifact, or running process used
- no product file modified

## First observable discrepancy

The native I03 facts are `UNRESOLVED`; the existing I05 path emits one receipt
with:

- `coverage_state = EVALUATED_MISSING_OR_CONFLICTING_AUTHORITY`
- `typed_state = COVERAGE_LIMITED`

This is the `_terminal_fact_class` and `_evaluate_candidate` mapping in
`rawlsing_next/pre553_discovery_exact.py`: `UNRESOLVED` is collapsed with
`UNAVAILABLE` before terminal selection.

A valid-empty frontier in the same fixture is distinct:
`EVALUATED_VALID_EMPTY` / `VALID_EMPTY`. Positive I03 support is `SUPPORTED`.
A revoked current authority raises the existing `DirectEstateError`.

## Batch

The actual saved Batch path (`execute_saved_batch`) returns `COMPLETED` for
all three units. The discovery result refs are `DiscoveryResultReceipt` refs,
not empirical facts; the Batch receipt has no typed fact state. The normal
Batch result therefore is operational completion, not a false completed fact.

A completed prior receipt is accepted without comparing it to an exact native
output. Replacing every prior `result_refs` entry with an unrelated exact ref
still yields three `COMPLETED` receipts and `FULL_MANIFEST_COVERAGE`, with no
native execution. The prior-cache consistency guard exists in the issued path
(`_validate_prior_cache`) but is not applied by `execute_saved_batch`.

## I05 unresolved repair — isolated RED/GREEN

`I05_UNRESOLVED_REPAIR.patch` is the exact one-file patch for
`rawlsing_next/pre553_discovery_exact.py`. It is not applied to the product
tree.

- RED: `EVALUATED_MISSING_OR_CONFLICTING_AUTHORITY` / `COVERAGE_LIMITED`
- GREEN: `EVALUATED_UNRESOLVED` / `COVERAGE_LIMITED`
- native fact states remain `UNRESOLVED`
- valid empty remains `EVALUATED_VALID_EMPTY` / `VALID_EMPTY`
- positive I03 remains `SUPPORTED`, denominator 8
- revoked authority remains `DirectEstateError`

`EVALUATED_UNRESOLVED` is an existing caller lane in
`pre553_analytical_state_and_route.py`; no new state is invented. The existing
typed lane remains `COVERAGE_LIMITED`.

The separate Batch prior-receipt issue is not modified here. No Batch owner
code or evidence is changed.

## Prior narrow fix note

The earlier suggested Batch fix is intentionally not in this patch; the Batch
owner lane remains separate.

Run:

```bash
PYTHONPATH=/Users/matthewsmith/Desktop/ANVIL_ENGINEERING_EXECUTION_20261117/IMPLEMENTER \
python3 WORKER_RETURNS/ANVIL_SRC16_I03_I05_BATCH_TRACE_20261119/trace_i03_i05_batch.py
```
