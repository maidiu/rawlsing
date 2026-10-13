# RAWLSING HQ — START HERE

For HQ succession, do not begin by grokking the whole repository and do not rely on conversational memory.

1. Read `HQ_HANDOFF/LATEST.json` on branch `integration/pre-main-reconciliation-r1`.
2. Follow its exact `handoff_commit` and checkpoint paths.
3. At that immutable commit read `CURRENT.md`, `CURRENT.json`, and `MANIFEST.json`; verify checkpoint identity and packet digests.
4. Establish that checkpoint as `SEALED_CHECKPOINT_AUTHORITY` — the last state already adjudicated by HQ.
5. Verify each checkpoint-named active worker branch.
6. If a named branch advanced after checkpoint cut, do **not** ignore it and do **not** silently adopt it. Inspect the governed return lineage and classify it as either `POST_CHECKPOINT_PENDING_RETURN` or `UNAUTHORIZED_POST_CHECKPOINT_MOVEMENT`.
7. Adjudicate valid pending returns normally, then execute the checkpoint succession instructions.
8. After every material HQ state change, append durable decisions as needed, create a new immutable checkpoint, advance `HQ_HANDOFF/LATEST.json`, and verify the pointer/packet before treating the transition as sealed.

Temporal law:

`SEALED_CHECKPOINT_AUTHORITY != POST_CHECKPOINT_PENDING_RETURN != UNAUTHORIZED_POST_CHECKPOINT_MOVEMENT`

A post-checkpoint worker return is new pending HQ input. It is neither inherited authority nor ignorable history.

Library permission modes in checkpoint state are exact: `NO`, `EXACT_ONLY`, or `ESCALATION_ONLY`. Do not interpret missing/ambiguous permission as broad Library search authority.

Protocol:

`HQ_HANDOFF/PROTOCOL.md`

Canonical succession prompt:

> Become Rawlsing HQ. Read `HQ_HANDOFF/LATEST.json` on `integration/pre-main-reconciliation-r1`, verify the immutable checkpoint packet it names, establish it as the last sealed HQ authority, reconcile only its named live worker edges under the post-checkpoint return law, then execute its succession instructions. Do not reconstruct state from conversational memory when the checkpoint supplies it. After every material HQ state change, update durable decisions as needed, create a new immutable checkpoint, advance `HQ_HANDOFF/LATEST.json`, and verify the pointer before considering that transition sealed.
