# R125 — next commands and ordering (proposed, not executed)

No command below has been run by R125. They are the exact launch order once
current source/use and preimage grants are present. Do not run them as a
substitute for permission.

## 0. Rights/preimage gate

Required before any source factory call:

- exact `CurrentDecisionResolver` / `IssuedWorkloadRecord` for the selected
  scope, with source and scientific permission refs, host, purpose, source SHA,
  full envelope SHA, U/Epre roots, expected jobs, currentness, original wave and
  native universes;
- exact `NativePreimageBundle` / `NativeWorkload` (projection, catalog, I03
  requests, discovery authority, source factory ref);
- exact source edition/host/purpose and retention/export/revocation.

If absent, stop with the exact missing grant/preimage; do not read raw source.

## 1. Current-permission native pass (LiTS only when granted)

```sh
python3 -B WORKER_RETURNS/PYAT-R43-U43-ORIGINAL35-PROSPECTIVE-WORKLOAD-R1/repro/execute_permitted.py \
  --runtime <authenticated-current-u43-runtime> \
  --output WORKER_RETURNS/PYAT-R125-REPRESENTATIVE-ROUTE-B-LAUNCH-PACKET-R1/out/current_native_manifests.json
```

Without the authenticated runtime this emits zero executed original manifests
and the exact decision pointers; that is not a launch.

## 2. Accepted R03 native frontier execution

Use the exact accepted APIs (see `02_PRODUCER_TO_CONSUMER_BINDINGS.json`):

```python
from rawlsing_next.pre553_universal_workload import (
    compile_governed_frontier, execute_governed_frontier,
)
compilation = compile_governed_frontier(
    bundle=<exact-issued-NativePreimageBundle>,
    inventory=<exact-issued-SourceInventory>,
    policy=<exact-issued-GrammarPolicy>,
    frontier=<exact-issued-ScientificFrontier>,
    as_of=<authenticated-as-of>,
    host=<authenticated-host>,
    purpose=<authenticated-purpose>,
)
result = execute_governed_frontier(
    compilation=compilation,
    source_factory=<authenticated-source-factory>,
)
```

Expected nonrespondent outputs:

- `out/<scope>/governed_frontier_ledger.json`
- `out/<scope>/native_facts_and_receipts.json`
- `out/<scope>/anti_join_no_drop.json`
- `out/<scope>/artifact_manifest.sha256`

For a direct issued `NativeWorkload`, use
`pre553_issued_workload.execute_issued_workload` with the same admission/record
fields; no alternate compiler.

## 3. M1/M2/B5 learned artifact

```python
# exact M1 family binding + exact discovery/evidence refs
# exact M2 release core/publication binding
# exact B5 lifecycle register/publish/current selection
```

Outputs: `out/<scope>/learned_disposition.json`,
`out/<scope>/m2_release.json`, `out/<scope>/b5_current.json`.
No currentness may be minted by the consumer.

## 4. N10E/FF/V553+ consumer

```python
# evaluate_learned_world_consumer(...) on the exact admitted graph/consumer
# field_forge_conditional_support + GT12 admission where claim-family authorized
# m1_temporal_v554_admission_dedup only for an exact observed pair
# configure_progressive_world_context/progressive_world_view only if exact fit
```

Outputs: `out/<scope>/n10e_consumer.json`,
`out/<scope>/ff_or_v553_result.json`, `out/<scope>/consumer_receipt.json`.

If a relation/claim-family/temporal pair is absent, stop with typed refusal and
route to the exact scientific owner. Do not synthesize a probability, pair, or
cross-source joint.

## 5. Fixed acceptance replay

Run the same exact input as the positive; then mutate only the declared source/
role/risk/condition/release/preimage and assert the same consumer changes or
refuses; restore original and assert same positive. Cold replay in a fresh
process; preserve exact current/as-of and revocation.

## Planned routing

- C11/native production defect → R03/M01 owner.
- learned publication/reference/lifecycle → M2/B5 owner.
- FF/V553/world transformation → FF/temporal/world owner.
- source/role/design/U-Epre/science → source/scientific issuer and HQ.
- source/host/purpose/rights → data custodian + HQ/user authorization.
