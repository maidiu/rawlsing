# Control plane

This directory is the executable operating layer for Rawlsing/DDM/V5. It indexes governing authority and accepted execution; it is not a semantic-authority source.

## Start here

```bash
python3 control_plane/rawlsingctl.py verify --tier repo
python3 control_plane/rawlsingctl.py status
python3 control_plane/rawlsingctl.py next
```

Current R1 frontier is `V552_REACCEPTANCE`, because the accepted Phase-D successor receipt closed the Phase-D gate without starting V552+.

## Files

- `authority_registry.json` — pinned authority/provenance references.
- `current.json` — tiny mutable active pointer.
- `pipeline_graph.json` — typed stage/ownership/execution graph.
- `courts.json` — run scopes, acceptance predicates, and claim ceilings.
- `change_policy.json` — change classes and revalidation rules.
- `regression_catalog.json` — failures that may never silently return.
- `repair_stack.json` — governing 25-item posture, kept separate from stage readiness.
- `obligations.json` — append-only successor/technical obligations.
- `receipts/` — immutable privacy-safe accepted execution receipts.
- `worker_task_contract.md` — required worker state-machine discipline.
- `rawlsingctl.py` — stdlib-only status/verify/next/impact/court/task CLI.

## Maintenance law

Do not hand-edit a narrative to make the project look green.

Advance `current.json` only after an accepted immutable receipt exists. If a receipt is superseded, add a successor receipt and move the pointer. Never rewrite the old receipt.
