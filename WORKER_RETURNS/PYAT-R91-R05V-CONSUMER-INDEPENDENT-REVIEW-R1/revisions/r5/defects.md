# R91 R05V R5 independent review — defects

## P1 — Coordinator/request cannot bind actual discovery/recursive/joint/E41 inputs

Location:
`rawlsing_next/pre553_learned_world_composition.py::NativeGraphSlot`,
`NativeGraphExecutionRequest`, `TrustedNativeGraphCoordinator.execute`.

`NativeGraphSlot` exposes only:
`slot_id, source_universe_ref, release_ref, producer_query_ref,
producer_predicate_ref, consumer_query_ref, model_rule_hash, producer_route`.

Missing High-decision associations: discovery result/receipt/frontier, recursive
handoff/lineage/root-parent, condition-value witness, target arity/topology/order,
M1 disposition, M2 release, B5 selection/currentness and E41 input. The
coordinator trusts an executor mapping and retains only composition identity
material; it cannot bind or prove the actual native inputs used.

Probes (`probes/test_r05v_r5_coordinator_gap.py`):

```text
slot_fields: 14 required actual-input fields missing
coordinator_inputs: discovery, recursive, handoff, lineage, frontier, E41,
  M1, M2, B5, currentness terms absent
actual_discovery_recursive_use_trusted_coordinator:
  both R5 actual tests call raw evaluate_learned_world_consumer without
  trusted_graph_reader
```

The R5 actual discovery/recursive/joint positives are raw compatibility-path
assertions, not the coordinator-owned full-graph custody required by the High
decision. The request cannot fix or retain the actual native inputs.

## P2 — Actual source/evidence sever and E41 discovery/recursive route unproven

R5 discovery/recursive severance changes only the requested predicate/ref; it
does not exercise actual source/native evidence change, a severed required
upstream dependency, or an actual E41 discovery/recursive result/receipt/route.
The High decision explicitly says wrong requested predicate/ref alone is not
enough.

## Missing function

1. Extend NativeGraphSlot/NativeGraphExecutionRequest with discovery result +
   receipt + frontier, recursive handoff + lineage/root-parent, condition-value
   witness, target arity/topology/order, M1/M2/B5/currentness and E41 input.
2. Coordinator executes actual owners from those inputs, validates before
   pinning, retains complete native input/output original, and serves through the
   fixed trusted reader; use it for actual discovery/recursive/joint positives.
3. Prove actual source/evidence and severed dependency change/refusal plus E41
   discovery/recursive route/receipt reconciliation with exact restore.

## Already-qualified partial

- Author 40/40; R1/R2/R3 probes 15/15; provider 43/43; C1 13/13.
- Actual AT10 discovery and AT11 recursive linkages to learned M1/M2/B5 and same
  N10E consumer are genuine native-object positives, but currently raw-path.
- Actual joint query arity 2; typed status/Z16 and R4 direct coordinator custody
  retained.
- Accepted R08/provider/evaluator bodies unchanged; R4 analytical custody change
  is inside the five-path grant.
