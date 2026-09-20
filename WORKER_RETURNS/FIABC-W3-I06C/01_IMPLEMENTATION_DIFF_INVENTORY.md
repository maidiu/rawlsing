# FIABC-W3-I06C — Implementation Diff Inventory

Base: `56697a27e94eb9603dfa412a15ab8f1feb819b0c`

Branch: `agent/rabochii-premain-fiabc-w3-i06c-lifecycle-accounting-r1`

## Production code

### `rawlsing_next/fiabc_lifecycle_accounting.py`

New bounded lifecycle/accounting module.

Implemented structures:

- `LifecycleAction` for the ten governed lifecycle actions.
- `AccountingDisposition` with the five required HQ-facing dispositions.
- `MetricState` preserving measured/null/not-reached/not-applicable distinctions.
- `ProcessIsolationReceipt` as the I06A normalization/validation seam.
- `LifecycleBinding` binding source, candidate, owner, workload, authority, runtime, candidate state and expected terminal identity.
- `LifecycleActionRequest` binding one lifecycle obligation to the exact governed operation.
- `ActionObservation` carrying actual candidate-state event evidence.
- `TelemetryMetric` as the I06B normalization seam with action/binding provenance.
- `LifecycleAccountingReceipt` as the final executed/preserved/not-reached/not-applicable record.
- `PreservedWorkPolicy`, `PreservedReceiptEvidence` and `PreservedCompatibilityProof`.

Implemented execution/adjudication functions:

- `execute_lifecycle_action`
- `typed_unreached_receipt`
- `typed_not_applicable_receipt`
- `build_lits_a_preserved_receipt`
- `build_lits_b_semantic_only_receipt`
- `adjudicate_preserved_work`
- `receipt_as_dict`

Implemented integration adapters:

- `CallableLifecycleActionAdapter`
- `CallableTelemetryAdapter`
- `ProcessIsolationReceipt.from_mapping`

Implemented fail-closed action checks:

- no formula-derived lifecycle evidence;
- no law-hash-only stale/corrupt evidence;
- no generic temporary-file interruption evidence;
- actual deletion and regeneration plus lineage for rebuild;
- candidate-owned retained-state proof for warm use;
- exact governed invalidation trigger and actual invalidated/recomputed unit lists;
- actual stale determinant change plus detection/recovery;
- actual candidate-state corruption plus detection/recovery;
- interruption of the governed candidate operation, not an unrelated file;
- separate process token for fresh replay;
- exact governed audit primitive;
- final terminal-identity reproduction after successful action;
- telemetry action/binding identity equality;
- observed recomputation-unit count equality.

## Tests

### `tests/test_fiabc_lifecycle_accounting.py`

New stdlib `unittest` hostile suite.

Coverage:

- formula-assigned recomputation units rejected;
- numeric invalidation count cannot exceed/replace observed recomputed unit lineage;
- law-string/hash stale/corrupt surrogates rejected;
- generic temp-file interruption surrogate rejected;
- deletion/regeneration without candidate-state action rejected;
- invalid warm retained state rejected;
- incompatible preserved-state binding receives no numeric credit;
- missing preserved LiTS-B telemetry remains null;
- unreached lifecycle stage cannot emit numeric metrics;
- Candidate-A preserved work cannot satisfy Candidate-B;
- fresh process replay requires terminal identity reproduction;
- wrong-terminal replay rejected.

## Return package

Added:

- `WORKER_RETURNS/FIABC-W3-I06C/00_RETURN.md`
- `WORKER_RETURNS/FIABC-W3-I06C/01_IMPLEMENTATION_DIFF_INVENTORY.md`
- `WORKER_RETURNS/FIABC-W3-I06C/02_LIFECYCLE_ACTION_CONTRACT.md`
- `WORKER_RETURNS/FIABC-W3-I06C/03_PRESERVED_WORK_ACCOUNTING_LEDGER.csv`
- `WORKER_RETURNS/FIABC-W3-I06C/04_TEST_AND_EXECUTION_PROTOCOL.md`
- `WORKER_RETURNS/FIABC-W3-I06C/RETURN.json`

## Deliberately untouched

No existing production backend, source semantics, candidate identity, court authority, P2X stopped ledger or measured receipt was modified on this branch.

The historical `rawlsing_next/ee_p2x_darwin_stage_backend.py@617c9c9...` was inspected as evidence of the S09-S16 defects but is not present on the Wave-2 fan-in base and was not recreated wholesale here. Fan-in should bind its actual candidate-state operations to this module rather than importing the historical surrogate lifecycle handlers.

No merge was performed.
