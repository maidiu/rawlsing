# B01E — Exact batch-owner → durable-adapter mapping

Every row below names an **already accepted** owner. The adapter supplies
exact inputs and journals exact outputs. It replaces none of them.

| Commission requirement | Real owner used | Entry point | Adapter supplies | Owner still decides |
|---|---|---|---|---|
| Source-free workload | accepted test fixture | `test_pre553_route_b_production._fixture` (+ `missing_weight` variant) | nothing — fixture reused unchanged | all C11 semantics |
| C11 → Route B composition | `pre553_route_b_production` | `execute_route_b_production(*, source, projection, runtime_catalog, i03_requests, discovery_authority_ref)` | the five exact inputs | object graph, replay receipt, dependency root |
| Sealed release + executor | `pre553_carrier_execution` | `production.repository_binding.executor` (`execute_i03`, `execute_i05`) | nothing — executor is the owner's | query/discovery truth, typed facts |
| Batch units | `pre553_batch_runner` | `BatchUnitSpec(job_kind, job_ref, release_refs, semantic_input_refs)` | real query/discovery refs + real release ref + real predicate/authority refs | canonical unit identity |
| Batch manifest | `pre553_batch_runner` | `BatchManifest(units)` | the unit tuple | canonical ordering, manifest hash |
| Real execution | `pre553_batch_runner` | `BatchExecutionRunner(manifest, repository, prior_receipts).run(executors, max_units=1)` | caller-owned REAL executor bindings; per-unit throttle | receipt shape, contiguity law, no-retry-after-complete |
| Attempt accounting | `pre553_batch_runner` | `next_attempt_index(unit)`, `pending_units()` | reads only | contiguity, schedule order |
| Durable intent | B01D candidate (unchanged) | `record_intent`, `DurableCheckpointStore.save` | unit ref + runner-issued attempt index | digest, sequence, atomicity |
| Durable commit | B01D candidate (unchanged) | `record_commit`, `store.save` | the owner's REAL receipt | digest verification, intent-match law |
| Recovery classification | B01D candidate (unchanged) | `plan_recovery` (fail-closed) | nothing — never passes proofs for promotion | HELD vs committed vs never-started |
| Receipt rehydration | B01D candidate (unchanged) | `admit_receipts_for_resume` | nothing | digest-verified rebuild |
| Exclusive writing | B01D candidate (unchanged) | `ledger_lock` | lock scope per save | OS exclusion |
| Release resolution | `pre553_c11_repository` | `repository.resolve_release_exact(ref)` | exact refs | sealed release objects |
| Source fidelity (new) | `C11LogicalRelease.source_artifact_ref` | read `content_hash`, compare to declared `source_sha256` | the declared sha | the artifact binding |

## What the adapter adds (and only this)

1. **Session binding** (`open_session`): manifest identity + release
   resolution + source-sha check + pre-existing-checkpoint foreign check —
   all fail-fast, all fail-closed.
2. **Per-unit governed loop** (`run_to_completion`): intent → save → owner
   call → journal append → commit → save, with a checked head invariant
   (pending head must equal the intended unit) and stop-at-first-held/pinned
   semantics with explicit blocked-suffix reporting.
3. **Side-effect journal** (`b01e_side_effects.jsonl`): durable, fsync'd,
   per-execution records modelling externalization; the crash window
   (journaled-but-uncommitted) is observable and countable.
4. **Fresh-process recovery** (`recover`): load → plan → rehydrate → new
   runner → pending list → outer-join manifest reconciliation. Executes
   nothing.
5. **Explicit held guard** (`refuse_held_execution`): any non-runner driver
   path fails loudly on HELD units.

## What the adapter refuses to do (by construction)

- Execute a HELD unit through any path (skip + report; guard raises).
- Retry a DEFERRED/FAILED unit (B01D journal pins every COMMITTED record;
  the adapter reports `pinned_deferred` instead of working around it).
- Skip over a non-progressable schedule head (head-anchored owner
  scheduling; per-unit selection would need an owner entrypoint that does
  not exist — recorded as future work, never simulated).
- Admit a receipt without a durable intent→commit chain (saved vs
  simulated distinction).
- Promote on any caller proof (B01D repair inherited).

## Direction of control

```
accepted fixture ──► execute_route_b_production ──► release + executor
        │                                                    │
        ▼                                                    ▼
BatchManifest ──► open_session ──► run_to_completion ──► runner.run(1)/unit
        │            (bind+verify)      │ intent→call→journal→commit
        │                              ▼
        └────────► recover ──► plan → rehydrate → pending → reconcile
             (fresh process, durable state only; executes nothing)
```