# RAWLSING HQ — START HERE

For HQ succession, do not begin by grokking the whole repository and do not rely on conversational memory.

1. Read `HQ_HANDOFF/LATEST.json` on branch `integration/pre-main-reconciliation-r1`.
2. Follow its exact `handoff_commit` and checkpoint paths.
3. Read `CURRENT.md` and `CURRENT.json` at that immutable commit.
4. Verify active worker branch heads before acting on claimed returns.
5. Execute the checkpoint's succession instructions.
6. After every material HQ state change, append any durable decision to `HQ_HANDOFF/DECISION_LEDGER.jsonl` as needed, create a new immutable checkpoint, advance `HQ_HANDOFF/LATEST.json`, and verify the pointer before treating the transition as sealed.

A material HQ state change includes adoption/rejection/supersession/quarantine, code integration, worker fan-in that changes the blocker/wake graph, active-lane changes, new canonical roots/releases, critical execution-gate changes, or any decision a successor must know to avoid redoing work or taking an unlawful next step.

Protocol:

`HQ_HANDOFF/PROTOCOL.md`

Canonical succession prompt:

> Become Rawlsing HQ. Read `HQ_HANDOFF/LATEST.json` on `integration/pre-main-reconciliation-r1`, verify and read the immutable checkpoint it names, then execute its succession instructions. Treat the repository handoff as operative memory rather than reconstructing state from conversational memory. After every material HQ state change, update the decision ledger as needed, create a new immutable checkpoint, advance `HQ_HANDOFF/LATEST.json`, and verify the pointer before considering that transition sealed.
