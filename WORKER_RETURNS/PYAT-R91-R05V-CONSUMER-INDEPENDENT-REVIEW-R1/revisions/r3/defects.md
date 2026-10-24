# R91 R05V R3 independent review — defects

## P1 — Graph provenance is metadata-consistent, not native-evidence-validated

Location:
`rawlsing_next/pre553_learned_world_composition.py::_authoritative_graph`,
`evaluate_learned_world_consumer`.

R3 checks component topology arity/components, joint count/order, route labels,
duplicate hashes and E41 type/membership/consumer hash. It does not reconcile
these fields to actual native owner receipts/frontier/lineage/root-parent or
actual component results. Internally consistent invented metadata still passes.

Independent probes (`probes/test_r05v_r3_actual_graph_gap.py`):

```text
forged_joint_topology:
  one actual composition; target topology arity=2 with two copied components;
  joint_component_count=2 -> EXACT_SUPPORTED, joint=2; no second actual result

forged_discovery_route:
  actual direct composition relabelled I05 discovery with forged receipt/frontier
  -> EXACT_SUPPORTED; forged ref echoed

forged_recursive_route:
  actual direct composition relabelled MX01R2 recursive with forged
  handoff/lineage -> EXACT_SUPPORTED; forged refs echoed

actual_type_e41_forged_route:
  real EmpiricalPossibilitySliceExtensionResult with route changed to
  EXT_ROUTE_DISCOVERY -> EXACT_SUPPORTED; forged route echoed
```

The two-direct-component positive and the status-disagreement typed result pass.
The author's two-component test uses two distinct DIRECT compositions; no actual
joint/discovery/recursive product is exercised. The author return explicitly
admits no actual discovery/recursive C1 linkage.

### Missing function/dependency

- Reconcile topology/joint count/order, discovery receipt/frontier, recursive
  parent/handoff/lineage/root-parent, source/operation and product currentness
  with actual native owner objects/results; do not trust internally consistent
  component metadata.
- Validate the E41 extension route against the actual component route and the
  discovery/recursive evidence it claims; a real-type extension with a forged
  route must refuse.
- If actual discovery/recursive C1 linkage to the same learned disposition is
  unavailable in the existing five-path owners/fixtures, name the exact native
  fixture/caller dependency. Do not fabricate labels or claim support.

## P2 — False exact status: fixed

R2's producer-SUPPORTED / analytical-ZERO_SUPPORT false exact case now returns
`LEARNED_CONSUMER_ZERO_SUPPORT` with denominator 0/cells and no exact support.
The status-disagreement probe passes.

## P3 — Duplicate definition block: fixed

Only one `__all__` and one active `NativeProductGraph`/`LearnedWorldConsumerResult`/
`evaluate_learned_world_consumer` remain.

## Retained partial capability

- Author 37/37; R05V R1 exact probes 4/4; R2 exact probes 5/5; provider 43/43;
  analytical composition 13/13.
- Actual M01/M1/M2/C1/N10E positive, two distinct direct compositions, direct
  E41, typed Z16/status cases; accepted owners unchanged.
