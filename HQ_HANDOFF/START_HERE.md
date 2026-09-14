# RAWLSING HQ — START HERE

For HQ succession, do not begin by grokking the whole repository and do not rely on conversational memory.

1. Read `HQ_HANDOFF/LATEST.json` on branch `integration/pre-main-reconciliation-r1`.
2. Follow its exact `handoff_commit` and checkpoint paths.
3. Read `CURRENT.md` and `CURRENT.json` at that immutable commit.
4. Verify active worker branch heads before acting on claimed returns.
5. Execute the checkpoint's succession instructions.

Protocol:

`HQ_HANDOFF/PROTOCOL.md`

Canonical succession prompt:

> Become Rawlsing HQ. Read `HQ_HANDOFF/LATEST.json` on `integration/pre-main-reconciliation-r1`, verify and read the immutable checkpoint it names, then execute its succession instructions. Do not reconstruct state from conversational memory when the checkpoint supplies it.
