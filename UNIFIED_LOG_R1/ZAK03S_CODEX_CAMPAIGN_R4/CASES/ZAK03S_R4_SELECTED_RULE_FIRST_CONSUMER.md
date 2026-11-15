# ZAK03S R4 case — selected-rule first-consumer boundary

**Case ID:** `ZAK03S:R4:CASE:SELECTED_QSM_FIRST_CONSUMER`
**Protected cut:** `6a5c12f04323d74001f9632063ec907f4fc4468e`
**Candidate cuts:** `ad17076c`; later `0d90c247`
**Status:** `DONE_AT_BOUNDED_SOURCE_CUT__NO_IMPORTING_BATCH_READER`

## Question

What selected historical QSM identity and meaning survives into the actual I03/I05 result, and what must Batch / the issued workload provide before they can consume that result?

## Finding

The selected QSM row is a **gate plus sibling binding receipt**. It does not become part of the I03/I05 empirical result.

### Candidate shape

`0d90c247:rawlsing_next/pre553_zak03s_selected_qsm_reader.py`, blob `d3c6c4e8a32398a3c4977ed287684bd95d058df3`:

- `SelectedQsmRequest` L75–L91: path, file SHA, row hash, authority version, rule id, source family/wave/country, var code, historical question id, native question ref, target-use triple.
- `SelectedQsmRouteResult` L94–L98: `route: RouteBProductionResult`; `binding_receipt: Mapping[str, Any]`.
- `_exact_selection` L114–L198: checks file SHA, row hash, version, rule id, question/var identity, source scope, unique same-code C11 response slot.
- `execute_selected_qsm_route_b` L201–L311: checks current permission triple in every I03 query, invokes `execute_route_b_production`, checks I03 facts and file stability, records binding receipt.
- Receipt L278–L310: QSM artifact/row/rule/resolution/lookup, source universe, native question, historical question/var, target-use triple, invoked producer, `selected_binding_first_importing_reader: "NOT_PROVED"`, `issued_batch_consumption_of_selected_qsm: False`, route/I03/I05 refs, `i05_historical_qsm_authority_established: False`, `original35_native_or_historical_production: False`.

### I03/I05 result shape

- `RouteBProductionResult`: `6a5c12f0:rawlsing_next/pre553_route_b_production.py`, blob `5b28d6c0c4f9bc032088cf660834ad574b8c8446`, L153–L164. No QSM field.
- `I03ExecutionRequest`: same file, L106–L130. Only `query_ref` and `predicate_ref`.
- `QueryExecutionResult`: `6a5c12f0:rawlsing_next/_pre553_query_common.py`, blob `40b1a9c974332db64d10b95d87682fd04be95063`, L105–L122. Only `query_ref`, `facts`, `source_scope_mode`, `release_refs`.
- `ExactBoundedDiscoveryResult`: `6a5c12f0:rawlsing_next/pre553_discovery_exact.py`, blob `1b82b6df993bf14afa5e78782d988cba6e76b668`, L127–L142. No QSM field.

### Exact counterexample

`0d90c247:rawlsing_next/tests/test_pre553_zak03s_selected_qsm_reader.py`, blob `5ef5ae473420dd314256898e44c10cb3b9821741`, L146–L184:

- Variant A and variant B are different QSM files/rows, with B `GOVERNED_CONTEXT_ONLY`.
- `other.route.i03_results[0].facts[0].ref == valid.route.i03_results[0].facts[0].ref` (L178): identical I03 fact identity.
- `binding_root` and `qsm_resolution` differ (L179–L180).
- `i05_historical_qsm_authority_established` is `False` (L162).

This proves the selected QSM row identity is not part of the I03 fact identity and that the I05 result is not QSM-qualified.

### Batch interface

`6a5c12f0:rawlsing_next/pre553_batch_runner.py`, blob `2d291600b9a10c56d9c6f6de7f7d619f6c52e829`:

- `JOB_KINDS = {"QUERY", "DISCOVERY"}` L23: no QSM kind.
- `BatchUnitSpec` L100–L151: `job_kind`, `job_ref`, `release_refs`, `semantic_input_refs`; all refs exact.
- `ExecutionOutcome` L215–L226: only result/provenance exact refs.
- `UnitExecutionReceipt` L242–L257: exact refs only.
- The candidate `binding_receipt` is a `Mapping` with a hex `binding_root`, not an `ExactRef` or canonical object. It cannot be a Batch semantic input or provenance ref without a new typed object/ref.

### Issued workload interface

`6a5c12f0:rawlsing_next/pre553_issued_workload.py`, blob `28174766f61a15f7296f575d615462d6410cfcb6`:

- `NativeWorkload` L188–L216: no QSM field; envelope closed over descriptor/projection/catalog/requests/discoveries/roots.
- `admit` L219–L261: compares envelope hash and `expected_jobs`; `IssuedWorkloadRecord` L85–L101 has no QSM field.
- `execute_issued_workload` L280–L367: calls `execute_route_b_production` directly (L312–L315), builds Batch units from requests (L324–L327), returns `NativeWorkloadResult` with no QSM binding (L264–L277).
- There is no selected-QSM parameter or call to `execute_selected_qsm_route_b`.

### Missing edge versus missing engine

The selected-QSM adapter, Route B, I03, I05, Batch, and issued-workload engines all exist. The missing piece is:

1. A typed exact ref/canonical object for the selected-QSM binding.
2. A field/sub-request in the issued-workload envelope, covered by the issuer hash and `expected_jobs`.
3. A call path that invokes the selected-QSM gate or accepts its result.
4. A Batch unit/result slot that preserves the binding as an exact ref or typed receipt.

This is a producer-to-consumer interface gap, not a missing engine or replacement requirement.

## Alternate consumer check

`6a5c12f0:rawlsing_next/pre553_learned_world_composition.py`, blob `adbcc3316920c708580097dfe9f5aef4c9ca82fb`:

- Imports `RouteBProductionResult` L50.
- Projects M01 replay-receipt identity and object-graph refs L740–L767.
- Accepts `m01_result` L1043–L1070, L1121–L1126.
- Contains no QSM reference. It consumes the inner route result, not the selected-QSM binding, and cannot recover the QSM row identity.

At `0d90c247`, `SelectedQsmRouteResult`/`execute_selected_qsm_route_b` have no non-test caller outside the defining module. At `6a5c12f0`, no protected Python source contains `SelectedQsm`, `selected_qsm`, or the candidate module name.

## Omission challenge

Could the binding receipt be passed as a Batch semantic input, ExecutionOutcome provenance, NativeWorkload envelope field, or precomputed issued-workload result? Source shape rejects each: no ExactRef, no Batch kind, closed envelope, no function parameter. The challenge survives bounded.

## Unresolved

- Runtime selected-QSM execution: `NOT_RUN`.
- Issued Batch consumption: `NOT_PROVED`; candidate explicitly false.
- Typed QSM binding ref/canonical object: absent.
- Issuer-envelope QSM field: absent.
- External/dynamic Batch or issued-workload callers: not inspected.
- Historical QSM semantic relation meaning beyond coverage eligibility: not carried into I03/I05.
- Adoption/integration: not claimed.
