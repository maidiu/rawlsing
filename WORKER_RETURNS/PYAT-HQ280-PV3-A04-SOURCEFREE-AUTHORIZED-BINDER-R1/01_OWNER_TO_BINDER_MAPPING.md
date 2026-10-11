# A04 — Owner → binder mapping

Every stage below is an **already accepted Rawlsing owner**. The binder supplies
exact inputs and reads exact identities back. It replaces none of them.

| Commission requirement | Real owner used | Entry point | What the binder supplies | What the owner still decides |
|---|---|---|---|---|
| Governed projection | `pre553_carrier_execution` | `bind_governed_c11_projection(projection_fields)` | the **complete, exact** field set, no defaulting | whether the projection is valid at all |
| Runtime object catalog | `pre553_carrier_execution` | `RuntimeObjectCatalog(authorities, predicates, queries, discovery_authorities)` | nothing — it is **caller-issued INPUT** | authority closure via `validate_object_authority_closure` |
| Authority resolution | `pre553_empirical_objects` / `pre553_empirical_authority` | `catalog.authority_registry`, `AuthoritySnapshot.authority_ref` | a declared authority **identity string** | whether that authority exists and is exact |
| I03 requests | `pre553_route_b_production` | `I03ExecutionRequest(query_ref, predicate_ref)`, `.request_identity` | the exact declared `(query_ref, predicate_ref)` pairs | all I03 semantics, denominators, risk sets, typed negatives |
| I03 execution | `pre553_carrier_execution` → `pre553_empirical_query` | `CarrierNeutralResearchExecutor.execute_i03` | request identity only | query resolution, weighting, conditional arithmetic |
| I05 discovery authority | `pre553_empirical_objects` | `DiscoveryAuthority` (in the issued catalog) | the exact `discovery_authority_ref` | grammar, atoms, K/J, validation, frontier |
| I05 execution | `pre553_carrier_execution` → `pre553_discovery_exact` | `CarrierNeutralResearchExecutor.execute_i05` | the exact discovery authority ref | candidate evaluation, coverage claim, pruning |
| C11 repository | `pre553_source_backed_c11_facade` | `build_source_backed_c11_repository` via Route B | the physical source + projection | sealed `C11LogicalRelease`, replay manifest |
| Compositor | `pre553_route_b_production` | `execute_route_b_production(*, source, projection, runtime_catalog, i03_requests, discovery_authority_ref)` | the five exact inputs | object graph, typed-state receipt, replay receipt, dependency root |
| Batch units | `pre553_batch_runner` | `BatchUnitSpec(job_kind, job_ref, release_refs, semantic_input_refs)` | job kind, exact job ref, exact release ref | canonical unit identity, collision handling |
| Batch manifest | `pre553_batch_runner` | `BatchManifest(units)` | the unit tuple | canonical ordering, manifest hash |
| Batch execution | `pre553_batch_runner` | `BatchExecutionRunner(manifest, repository).run(executors=...)` | the executor **bindings** that call the real owner | attempt indices, retry, defer, receipt set, coverage state |
| Replay verification | `pre553_route_b_production` | `verify_route_b_replay_receipt(receipt)` | nothing | tamper detection, dependency root |

## Explicitly NOT used

No structural admission, no causal/structural truth, no learned-product
publication or current selection, no actor/V3 state, no field-forge release, no
adaptive discovery, no semantic PRE-MAIN rewrite. The binder imports none of
those modules; `test_binder_uses_only_existing_accepted_owners` asserts the
import surface.

## Direction of control

```
independently declared expected work (INPUT, hashed first)
        │
        ▼
   bind_expected_work()  ──► GovernedC11Projection | I03ExecutionRequest | JobPlan
        │
        ▼
   build_batch_manifest() ──► BatchManifest (exact sealed release ref)
        │
        ▼
   execute_bound_workload() ─► execute_route_b_production()   [REAL C11/I03/I05]
        │                    └► BatchExecutionRunner.run()   [REAL batch]
        ▼
   reconcile()  ── OUTER join  E vs J vs R vs C, typed, fail-closed
```

The arrow into `bind_expected_work` is the only place expectations enter, and it
happens **before** any owner runs. Nothing downstream can rewrite an
`expected_work_key`; a changed science yields a **new key** (successor), never
an in-place rewritten expectation.