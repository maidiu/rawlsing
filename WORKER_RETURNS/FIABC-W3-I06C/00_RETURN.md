# FIABC-W3-I06C — Lifecycle / Preserved-Work Accounting

Status: `COMPLETE__IMPLEMENTED__UNEXECUTED_BROWSER_QUALIFICATION_PENDING_FANIN`

Worker: `FIABC-W3-I06C`

Branch: `agent/rabochii-premain-fiabc-w3-i06c-lifecycle-accounting-r1`

Base: `agent/vozhd-premain-fiabc-wave2-fanin-r1@56697a27e94eb9603dfa412a15ab8f1feb819b0c`

Return path: `WORKER_RETURNS/FIABC-W3-I06C/`

## Holding

The lifecycle/preserved-work portion of Wave-3 IMP11 is implemented as a fail-closed accounting layer in:

- `rawlsing_next/fiabc_lifecycle_accounting.py`
- `tests/test_fiabc_lifecycle_accounting.py`

The implementation does not re-own I06A process isolation or I06B resource telemetry. It consumes normalized I06A isolation evidence and accepts I06B numeric lifecycle telemetry only after a candidate-specific lifecycle action has executed and passed the I06C action contract.

The central ordering is:

`I06A isolation binding -> exact lifecycle request -> actual candidate-state action -> I06C action validation -> I06B telemetry admission -> lifecycle accounting receipt`

No numeric lifecycle metric can be admitted before the action that supposedly produced it.

## Implemented lifecycle surface

The action contract covers:

- cold first realization/open;
- warm retained-state use;
- deletion/regeneration;
- source-release invalidation;
- authority/semantic invalidation;
- stale-state detection/recovery;
- corrupt-state detection/recovery;
- interruption recovery;
- fresh-process replay;
- audit/revalidation.

Every executed receipt binds:

- exact source ID and SHA-256;
- exact candidate and candidate-owner identity;
- exact frozen workload identity;
- exact authority-set identity;
- exact runtime binding;
- exact candidate state-scope identity;
- exact I06A process/root isolation receipt;
- actual action ID;
- pre/post candidate-state identities;
- governed operation ID;
- final governed terminal identity;
- I06B metric action/binding IDs.

Successful lifecycle actions must reproduce the expected governed terminal identity. Fresh-process replay additionally requires a distinct replay process token.

## Anti-surrogate enforcement

The implementation explicitly rejects:

- `FORMULA_DERIVED` recomputation as executed invalidation work;
- `LAW_HASH_ONLY` stale/corrupt evidence;
- `GENERIC_TEMP_FILE` interruption evidence;
- rebuild receipts without real deleted and regenerated candidate-owned objects plus lineage;
- warm-state claims where the retained state is absent or owned by another candidate;
- invalidation metrics whose numeric recomputation count differs from the actual recomputed-unit lineage;
- telemetry whose `action_id` or `binding_id` does not match the validated action;
- reserved lifecycle metric names attached to the wrong lifecycle action class.

This directly replaces the Wave-2 B03 defects represented by old S09-S14 surrogate logic without reimplementing the backend itself on this worker branch.

## Preserved-work law implemented

The accounting layer encodes the Wave-2 B03 preserved-work policies for the decisive categories:

- common upstream Lock/workload/oracle capital: candidate numeric cost `NOT_APPLICABLE`; candidate-local access remains separately chargeable when executed;
- P006 LiTS-A fresh first build: conditionally eligible field-by-field only after exact final workload/runtime/state/isolation/operation and metric-definition compatibility proof;
- P007 LiTS-B cacheless C11: semantic/identity evidence only, with numeric fields null;
- P008 older pre-P2 Candidate-A build: calibration only; never dispositive numeric P2 evidence;
- P009 authorized stop: preserves stop evidence; unreached metrics are `NOT_REACHED` and null.

The five HQ-facing dispositions are implemented exactly:

- `EXECUTED_NOW`
- `LAWFULLY_PRESERVED_MEASURED_WORK`
- `PRESERVED_SEMANTIC_EVIDENCE_WITHOUT_NUMERIC_TELEMETRY`
- `NOT_REACHED`
- `NOT_APPLICABLE`

No missing field is converted to zero.

## I06A / I06B integration seams

I06A target contract:

`ProcessIsolationReceipt`

Required facts are source, candidate, unique process token, candidate-root identity, fresh-process-for-cell and no cross-candidate reachable state. `ProcessIsolationReceipt.from_mapping()` is the mechanical adapter seam if I06A returns a mapping.

I06B target contract:

`TelemetryPort.record_completed_lifecycle_action(request, observation) -> Sequence[TelemetryMetric]`

Every measured metric must bind the validated lifecycle `action_id` and exact lifecycle `binding_id`. `CallableTelemetryAdapter` allows fan-in to wrap I06B's final concrete recorder without moving telemetry ownership into I06C.

I06C therefore remains independently fan-in-able even though I06A/I06B were not yet present on this branch when implementation began.

## Hostile tests added

The unittest suite encodes all required hostile cases, plus an additional observed-unit mismatch case and wrong-terminal replay case:

1. formula-derived recomputation cannot pass;
2. executed invalidation cannot report a recomputation number different from actually recomputed units;
3. law hashing cannot pass stale or corrupt exercise;
4. generic temporary-file manipulation cannot pass interruption recovery;
5. rebuild without deletion/regeneration fails;
6. warm use without valid retained candidate-owned state fails;
7. incompatible preserved state binding gets no numeric credit;
8. missing LiTS-B telemetry stays null, never zero;
9. an unreached stage emitting numeric telemetry fails;
10. Candidate-A preserved work cannot satisfy Candidate-B;
11. successful fresh replay reproduces the governed terminal identity;
12. fresh replay with the wrong terminal identity fails;
13. a reserved lifecycle metric cannot be attached to the wrong action class.

No measured P2X was run. No local-machine Codex was used. Tests were authored but not executed in this browser-only commission; the exact qualification protocol is in `04_TEST_AND_EXECUTION_PROTOCOL.md`.

## Scope exclusions

This worker does not:

- implement OS process spawning/isolation;
- implement CPU/RSS/I/O/scratch measurement;
- repair Candidate-C binding;
- materialize a parity oracle;
- reconcile the stopped ledger;
- run measured P2X;
- merge sibling work;
- create follow-on commissions.

## Terminal

`FIABC_W3_I06C_LIFECYCLE_AND_PRESERVED_WORK_ACCOUNTING_IMPLEMENTED__READY_FOR_FANIN`
