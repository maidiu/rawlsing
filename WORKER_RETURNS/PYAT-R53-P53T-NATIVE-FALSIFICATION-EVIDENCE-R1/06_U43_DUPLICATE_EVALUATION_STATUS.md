# U43 — DUPLICATE DISCOVERY EVALUATION STATUS

**Source:** issued workload blob `31e84f49d624f5524906e9e7839d2873106f8249`, materialized at `tests/_pinned/u43/pre553_issued_workload.py`, SHA256 `8a420647ec32e1e6935e2b359c0c6e3cab1f802be59c3861a8ba2393b3351ac6`.
**Call sites:** Route B surface `pre553_issued_workload.py:300-303`; Batch DISCOVERY unit `:308-309`; actual `execute_i05` in the Batch executor `:321`; runner invocation `:331-333`.

## Actual observed control flow

`tests/test_u43_duplicate.py` imports the pinned U43 module under an isolated name and replaces only the external owners with spies:

- `admit` returns a fixed admission record.
- `execute_route_b_production` is a spy.
- `build_source_backed_c11_repository` returns a minimal release.
- `CarrierNeutralResearchExecutor` is a spy executor.
- `BatchExecutionRunner` is a spy scheduler that invokes the actual U43 `execute()` closure for each manifest unit.

The inspected U43 `execute_issued_workload()` itself is unchanged. One issued discovery ref is supplied.

Observed call sequence:

```
ROUTE_B_SURFACE  DiscoveryAuthority|urn:test:disc|cccc...
BATCH_SURFACE   DiscoveryAuthority|urn:test:disc|cccc...
```

Both surfaces receive the same exact `DiscoveryAuthority` ref. The first is the Route B production call; the second is the Batch `execute_i05(discovery_authority_ref=unit.job_ref)` call. This reproduces the duplicated **entry surface** on the same issued operation.

Grade: `REPRODUCED_ISOLATED_HELPER__MOCKED_U43_OWNERS`.

## Positive control — prior receipt ingress refusal

With `prior_receipts=(object(),)`, the actual U43 code raises:

```
WorkloadAdmissionError: RESTORE_THROUGH_EXISTING_ISSUED_FACT_RECEIPT_CUSTODY_REQUIRED
```

before either spy surface is called. The current refusal of caller-supplied prior receipts is correct at this boundary.

## What is not proved

- Actual `BatchExecutionRunner` scheduling, receipt creation, replay, or prior-receipt custody.
- Whether the Route B call and the Batch call both commit the same semantic fact/receipt, or only duplicate CPU.
- Whether an object graph, unique receipt identity, checkpoint, or data value is corrupted.
- Whether a real issued workload would reach both sites with the same discovery under a real resolver/catalog.
- Whether duplicate execution is semantically legitimate for this workload.

The B53R "possible duplicate CPU vs receipt/data corruption" question remains open. No path was deleted, no repair proposed, and no production U43 behavior was changed.

## Why this is not native

The U43 module's native owners (`execute_route_b_production`, C11 source-backed repository, `CarrierNeutralResearchExecutor`, `BatchExecutionRunner`) were not executed. The test measures the control flow of U43's own function with synthetic owner surfaces. It does not establish native Batch or source behavior. A later test must use the actual owners, an actual issued workload, and an authenticated cold/replay path.
