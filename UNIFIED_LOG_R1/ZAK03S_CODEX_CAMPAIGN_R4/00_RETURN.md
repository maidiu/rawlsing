# 00_RETURN — ZAK03 selected-rule first-consumer boundary (R4)

**Campaign:** ZAKONCHILOS / #1057
**Lane:** 03 selected current empirical
**Governing cut:** `cfae8c2550ffa364829e0df0df730c457621581d`
**Protected cut:** `6a5c12f04323d74001f9632063ec907f4fc4468e`
**Candidate cuts:** `ad17076cc95b9383ab3b28879f471026bcba9ff7`; later `0d90c2470b0b476dcb74ce157b706b10f8392f4f`
**Output root:** `UNIFIED_LOG_R1/ZAK03S_CODEX_CAMPAIGN_R4/`
**Execution:** `NOT_RUN`; S0–S1 static documentary source inspection only.
**Terminal status:** `DONE_AT_BOUNDED_SOURCE_CUT__SELECTED_QSM_IDENTITY_ONLY_IN_SIBLING_BINDING__NO_IMPORTING_BATCH_READER`

## Direct answer

### 1. What selected historical QSM identity and meaning survives into the I03/I05 result?

The selected QSM row is a **coverage/lineage gate and a sibling provenance receipt**, not an input that becomes part of the I03/I05 empirical result.

- `SelectedQsmRouteResult` has exactly two members: the actual `RouteBProductionResult` (`route`) and a separate plain-mapping `binding_receipt` (later candidate `0d90c247:rawlsing_next/pre553_zak03s_selected_qsm_reader.py`, blob `d3c6c4e8a32398a3c4977ed287684bd95d058df3`, L94–L98).
- `RouteBProductionResult` contains `source_identity`, `projection_binding_receipt`, `repository_binding`, `c11_release`, `i03_results`, `i05_result`, `object_graph`, `learned_empirical_execution_receipt`, `replay_receipt` (`6a5c12f0:rawlsing_next/pre553_route_b_production.py`, blob `5b28d6c0c4f9bc032088cf660834ad574b8c8446`, L153–L164). It has **no QSM field**.
- `I03ExecutionRequest` carries only `query_ref` and `predicate_ref` (same file, L106–L130). The QSM artifact SHA, row hash, rule id/version, resolution status, lookup key, and historical question id are not in the request.
- `QueryExecutionResult` carries only `query_ref`, `facts`, `source_scope_mode`, and `release_refs` (`6a5c12f0:rawlsing_next/_pre553_query_common.py`, blob `40b1a9c974332db64d10b95d87682fd04be95063`, L105–L122). It has **no QSM field**.
- `ExactBoundedDiscoveryResult` carries the discovery contract, authority/candidate/coverage refs, receipts, empirical facts, predicates, queries, valid-empty state, and replay ref (`6a5c12f0:rawlsing_next/pre553_discovery_exact.py`, blob `1b82b6df993bf14afa5e78782d988cba6e76b668`, L127–L142). It has **no QSM field**.
- The candidate test is the exact counterexample: two different selected QSM files/rows (variant A and variant B, one `GOVERNED_CONTEXT_ONLY`) produce **identical I03 fact refs**, while the sibling binding receipt and `binding_root` differ (`0d90c247:rawlsing_next/tests/test_pre553_zak03s_selected_qsm_reader.py`, blob `5ef5ae473420dd314256898e44c10cb3b9821741`, L146–L184, especially L178–L180).
- The later candidate records `i05_historical_qsm_authority_established: False` and `original35_native_or_historical_production: False` (reader L308–L309), and explicitly records `selected_binding_first_importing_reader: "NOT_PROVED"` and `issued_batch_consumption_of_selected_qsm: False` (L297–L300).

What actually survives into the I03/I05 computation is only:

1. The **native question/var coupling**: the selected QSM row's `question_id` must equal its `var_code` and the request's `historical_question_id`, and the projection must contain one C11 response slot whose native question ref equals the request's `native_question_ref` and whose slot name case-folds to the QSM row's `var_code` (reader L147–L159, L187–L197). The query target must equal that native question ref and the query universe must equal the single projection universe (L231–L247).
2. The **current target-use permission triple** in each I03 query's `requested_output_grain`, dependency refs, and authority refs (L248–L259).
3. The **historical coverage eligibility** (positive QSM disposition and coverage-only resolution status) as a pre-execution gate (L160–L172).

The QSM row's historical **semantic direction/relation meaning, artifact/row identity, rule id/version, resolution status, and lookup key do not enter the I03 facts or I05 result**. They are recorded only in the sibling `binding_receipt`. The test's A/B identical-fact result is the exact proof.

### 2. What Batch and the issued workload interfaces require before they can consume that result

**Batch (`6a5c12f0:rawlsing_next/pre553_batch_runner.py`, blob `2d291600b9a10c56d9c6f6de7f7d619f6c52e829`):**

- `JOB_KINDS = {"QUERY", "DISCOVERY"}` (L23). There is no QSM job kind.
- `BatchUnitSpec` carries `job_kind`, `job_ref`, `release_refs`, and `semantic_input_refs`; every ref must be an `ExactRef` (L100–L151; projection L85–L97).
- `ExecutionOutcome` carries only `result_refs` and `provenance_refs` (L215–L226).
- `UnitExecutionReceipt` carries exact unit/result/provenance refs only (L242–L257).
- The candidate `binding_receipt` is a plain `Mapping[str, Any]` with a `binding_root` 64-hex string, not an `ExactRef`, not a schema-typed canonical object, and not a `BatchUnitSpec` input (reader L278–L311).

So Batch would need a typed exact ref/canonical object for the selected-QSM binding before it could carry it as a `semantic_input_ref` or a receipt `provenance_ref`. It would still need a unit kind or explicit semantic-input convention that says what the QSM binding means to a QUERY/DISCOVERY unit.

**Issued workload (`6a5c12f0:rawlsing_next/pre553_issued_workload.py`, blob `28174766f61a15f7296f575d615462d6410cfcb6`):**

- `NativeWorkload` carries `decision_ref`, `source_factory_ref`, `descriptor`, `projection`, `catalog`, `requests: tuple[I03ExecutionRequest, ...]`, `discoveries`, `original_u_root`, `expected_frontier_root`, and optional `original_wave_identity` (L188–L216). There is no selected-QSM field.
- `NativeWorkload.envelope()` is a closed descriptor + projection/catalog/requests/discoveries/roots material (L201–L216); `admit()` requires `semantic_hash(workload.envelope()) == record.envelope_sha256` and checks `expected_jobs` from `operation_jobs(requests, discoveries)` (L247–L253; `operation_jobs` L63–L67). `IssuedWorkloadRecord` has no QSM field (L85–L101).
- `execute_issued_workload()` calls `execute_route_b_production` directly with `workload.requests` and `workload.discoveries` (L312–L315), never `execute_selected_qsm_route_b`. It builds Batch units from `workload.requests` with `(r.predicate_ref, workload.decision_ref)` as semantic inputs (L324–L327); there is no place for the selected-QSM binding.
- `NativeWorkloadResult` has routes, native outputs, manifest, receipts, output refs, envelope/decision/scope/summary, original-wave identity, and source SHA (L264–L277). It has no selected-QSM binding field.

So the issued workload would need: (a) a typed QSM-binding ref/object; (b) a QSM field or sub-request in the issued envelope, covered by the issuer's envelope hash and `expected_jobs`; (c) a call path that invokes the selected-QSM wrapper (or an equivalent gate) instead of directly calling Route B; and (d) a Batch/result representation that preserves the binding as an exact ref or a typed receipt. None exists at the inspected cuts.

### 3. Missing producer-to-consumer edge, not a missing engine

The engines exist and are concrete: the candidate selected-QSM adapter (`execute_selected_qsm_route_b`), the protected Route B compositor (`execute_route_b_production`), the protected I03/I05 execution owners, the protected Batch runner, and the protected issued-workload interface. The candidate adapter really invokes Route B and returns a real `RouteBProductionResult`; the I03/I05 results are real.

The missing piece is an **interface/provenance edge**: no typed exact identity for the selected-QSM binding, no issued-envelope field, no Batch unit/result slot, and no call path from the issued workload to the selected-QSM wrapper. That is a missing consumer edge, not a missing computation engine, a missing admission engine, or a replacement requirement. The later candidate itself records `selected_binding_first_importing_reader: "NOT_PROVED"` and `issued_batch_consumption_of_selected_qsm: False`.

## Material counterexample and alternate consumer

`6a5c12f0:rawlsing_next/pre553_learned_world_composition.py`, blob `adbcc3316920c708580097dfe9f5aef4c9ca82fb`, imports and consumes `RouteBProductionResult` (L50, L740–L767, L1043–L1070, L1121–L1126). It projects the M01 replay-receipt identity and the exact object-graph refs; it has no QSM import, no selected-QSM field, and cannot recover the selected QSM row identity from the route result. This is a real downstream consumer of the inner route result, and it confirms that the selected-QSM identity is not carried by that result.

At the later candidate, `SelectedQsmRouteResult` and `execute_selected_qsm_route_b` have no non-test caller outside their defining module; the only caller is the static test fixture. No protected Python source at `6a5c12f0` contains `SelectedQsm`, `selected_qsm`, or `pre553_zak03s_selected_qsm`.

## Bounded omission challenge

**Could the candidate binding receipt be passed to Batch or the issued workload without a new typed edge?**

Tested alternatives:

1. As a `BatchUnitSpec.semantic_input_ref`: refused by source shape. `semantic_input_refs` requires `ExactRef`; the binding receipt is a `Mapping` and its `binding_root` is a hex string, not an `ExactRef` (Batch L100–L151; reader L278–L311).
2. As an `ExecutionOutcome.provenance_ref`: refused for the same reason; `ExecutionOutcome` accepts only `ExactRef` tuples (Batch L215–L226).
3. As a `NativeWorkload` envelope field: refused by the closed envelope and issuer hash. `NativeWorkload` has no QSM field; `envelope()` is closed over descriptor/projection/catalog/requests/discoveries/roots; `admit()` compares its hash to the issued record (issued L188–L216, L247–L253).
4. As a precomputed route result passed to `execute_issued_workload`: refused by signature. The function accepts no selected-QSM result and recomputes `execute_route_b_production` from `workload.requests`/`workload.discoveries` (issued L280–L315).
5. As ordinary I03 query content: the query can carry the target-use triple and native question ref, but not the QSM artifact/row/rule identity; the test proves different QSM rows produce identical I03 facts (`0d90c247` test L146–L184).

The challenge survives bounded. The missing edge is a typed provenance/consumer contract, not an absent engine.

## Finite source coverage

Inspected directly:

- Candidate `ad17076c` and later `0d90c247` selected-QSM reader and static test.
- Protected `pre553_route_b_production.py`, `pre553_batch_runner.py`, `pre553_issued_workload.py`, `_pre553_query_common.py`, `pre553_discovery_exact.py`.
- Protected `pre553_learned_world_composition.py` as an immediate alternate consumer of `RouteBProductionResult`.
- Protected caller references for `execute_route_b_production`, `RouteBProductionResult`, `execute_issued_workload`, and Batch unit/receipt shapes.

Not inspected / held:

- Every external or dynamic caller of Batch/issued workload outside the named static search.
- Runtime execution of the candidate or the issued workload.
- Any new QSM-to-native-QVB mapping beyond the same-code rule.
- Adoption or integration of the candidate.

## Preserved prior work

The independently accepted round-two producer/provenance distinctions and the round-three review at `157b74ed3f55757a11d632dddca2b15703e687a7` are preserved by reference. This round does not reopen the I04 constructor search, does not assert selected-QSM→I04, and does not challenge the accepted I04/receiver findings.

## Runtime

- Start: `2026-11-15T00:43:51-0500` (`2026-11-15T05:43:51Z`).
- End/content freeze and elapsed: recorded in `RETURN_VERDICT.json`.
- Model context: `opencode-go/deepseek-v4.1-flash`; MAX/1017 variant and provider routing are not independently exposed by the local shell/config. No provider/model/account change; no subagents.
- Token usage, cost, and provider retries: `UNKNOWN` unless exposed below as `UNKNOWN`. No billing claim.

## Terminal sentence

**The selected historical QSM row is a coverage/lineage gate with a sibling binding receipt, not part of the I03/I05 empirical result; Batch and the issued workload have no typed QSM binding slot or call path; the missing piece is a producer-to-consumer interface edge, not a missing engine, and no implementation is authorized.**
