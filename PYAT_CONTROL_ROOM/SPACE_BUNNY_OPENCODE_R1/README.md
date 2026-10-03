# Space Bunny / OpenCode — Pyat HQ

Status: **REMOTE_MACHINE_HANDOFF_CURRENT__HQ187_CONTINUATION__C4_HOLD_PRESERVED**.

This is the control-room home for Space Bunny HQ in OpenCode. Start with [HQ_START_HERE.md](HQ_START_HERE.md). It contains the complete launch instruction and ordered first actions. You do not need the conversation that produced this packet.

The user requested this subsection so Space Bunny can be directed here and know what to do. This selects the OpenCode workflow; activation has since progressed as recorded in CURRENT_HANDOFF. It supersedes Browser Economy's default routing for that activation; it does not adopt C4, issue a source warrant, authorize actor work, or expand any existing implementation commission.

## Current continuation — read before the original activation sequence

Read [CURRENT_HANDOFF.md](CURRENT_HANDOFF.md) first. Activation and the independent re-check have progressed through HQ187; preserve completed work. It supplies the exact current continuation, published C1 evidence, later HQ187 qualifications, multi-agent handoffs and the path to the next external decision. Original activation steps below apply only to missing or unqualified capabilities on the actual host. No chat-only instruction is required.

## Supporting packet read order

1. [HQ start instruction](HQ_START_HERE.md).
2. Live `HQ_HANDOFF/LATEST.json` and its immutable checkpoint/manifest under `HQ_HANDOFF/PROTOCOL.md`.
3. [Activation runbook](ACTIVATION_RUNBOOK.md) and [first task plan](FIRST_TASKS.json).
4. [Operating design](OPERATING_DESIGN.md), especially Git ownership, quality controls and scheduling.
5. [C4 reconciliation docket](C4_RECONCILIATION_DOCKET.md) when ready to prepare that decision.
6. [Forward program](FORWARD_PROGRAM.md) for the path through C9/C10.

Roles: [HQ](roles/hq.md), [worker](roles/worker.md), [reviewer](roles/reviewer.md), [source runner](roles/source-runner.md). These are prompt sources, not installed agents. Templates: [commission](templates/COMMISSION.md), [task](templates/TASK.json), [event](templates/EVENT.json), [return](templates/RETURN.json), [decision claims](templates/DECISION_CLAIMS.md).

## Original delivery record — current operational state is in CURRENT_HANDOFF

Delivered: instructions, role prompts, exact comparison references, staged activation tasks, templates, operating design, and a packet-integrity verifier. Not yet installed or qualified: OpenCode role configuration, dispatcher, permission isolation, integration service, live queue and background wake-up. No agent was launched by delivery.

Run `python3 scripts/verify_packet.py` from this directory to verify the delivered packet. Verification reads only packet files. A PASS establishes packet integrity, not operational readiness or permission enforcement.

`FIRST_TASKS.json` is an activation plan, **not a live task board**. Do not mark it running because a session exists. Materialized tasks require exact bindings and durable session/result records. Do not dispatch the stale revision-29 browser task board.

## One prompt for the user

> Act as Pyat HQ in OpenCode using Space Bunny. Read PYAT_CONTROL_ROOM/SPACE_BUNNY_OPENCODE_R1/HQ_START_HERE.md on integration/pre-main-reconciliation-r1 in maidiu/rawlsing. Read CURRENT_HANDOFF.md first, reconcile the live checkpoint and resume the existing HQ workflow without repeating completed setup or review. Preserve existing work and all C4/source/semantic/actor gates. Continue already-authorized work without making me relay routine agent messages. Report the first operational result and any exact decision that genuinely requires me.

## Authority and state

Preparation baseline: `fe1b2729b0f9f1ff18044c2f655b74784e001217`, HQ182. This is a historical reference, never an assertion that HEAD cannot advance. The delivery checkpoint records this packet without adopting the C4 review or certifying that the old frontier is current. Reconcile live state before selecting work.

The repository/checkpoint is durable accepted memory. OpenCode sessions and the dispatcher queue are operational tools. Worker claims and messages are pending evidence until reviewed and adjudicated.

