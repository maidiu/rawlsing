# State, succession and communication

[Start](README.md) · [Task board](data/task_board.json) · [Task template](templates/task_assignment.template.json)

## Repository is the durable bus

HQ maintains one active task board, exact commissions, returns, reviews, decision records and handoff checkpoints. Conversation messages point to those objects. No critical conclusion should depend on a vanished browser chat or a worker's memory.

The packet's `data/task_board.json` is an initial snapshot, not a live claim of dispatch. On activation HQ copies/versions it into its active operational state and fills owner/session, branch, base SHA, precise terrain, reviewer, runtime and fixture freeze. Each update includes a monotonic revision and prior digest. Do not let multiple agents independently overwrite the shared board; HQ is sole writer or uses explicit compare-and-swap tooling.

## Task state machine

PLANNED → READY → ISSUED → RUNNING → RETURNED → UNDER_REVIEW → CHANGES_REQUIRED or ACCEPTED_SCOPED → INTEGRATED_QUALIFIED.

Alternative states: BLOCKED_CAPABILITY, BLOCKED_AUTHORITY, BLOCKED_CUSTODY, AWAITING_ASTRA, SUPERSEDED_WITH_LINEAGE, CANCELLED_BY_HQ. Record exact reason and unaffected work. READY requires competent inputs, actual owner/reviewer, supported execution surface and frozen write boundary; a placeholder row cannot become RUNNING by timestamp alone. ACCEPTED_SCOPED is not global F-gate completion.

Each task record identifies parent commission, required and conditional dependencies, allowed library mode, source policy, baseline, implementation/output refs, proof grade, remaining scope and next action. Use null for unreached implementation/test/source metrics. Source_reads=0 is allowed only with an actual access account, not as a substitute for unknown.

## Messages

- HQ → worker: goal, exact refs, allowed actions, output/acceptance, review and stop/escalation conditions.
- Worker → HQ: a material return/blocker with exact artifact refs and requested decision; no narrative diary.
- Reviewer → HQ: exact findings/approval and reproduced evidence at the reviewed SHA.
- HQ → Astra: the compact decision packet from the escalation protocol, only when a trigger or Omega boundary applies.

Use supported dispatch/messaging tools only within user-authorized orchestration. If the browser cannot create/message agents, HQ supplies a complete prompt plus the target model/role and input links for user-mediated launch. It does not attempt to automate ChatGPT UI to bypass that limitation. Do not claim messages sent or jobs running before actual acknowledgements.

## Recovery and drift

At continuation, resolve LATEST and the immutable checkpoint; verify its manifest; reconcile named active branch heads. Unchanged ref means no observed Git movement, not a live process. Valid later worker returns remain pending until adjudicated. Unexplained movement is quarantined. Recover existing task/branch state and preserved logs before considering a new run; do not restart broad audits.

When HQ context becomes too large, seal a concise handoff containing adopted changes, active exact tasks, unresolved decisions and next lawful actions. The successor reads that packet and named live edges, not the full project again. Seal material adoption/integration/commission changes under `HQ_HANDOFF/PROTOCOL.md`; previous checkpoints remain immutable.

## Checkpoint and authority accounting

Control branch HEAD, immutable handoff commit, semantic PRE-MAIN, implementation commit, fixture/oracle identity and source identity are separate fields. Append durable decisions to the ledger. Bind CURRENT.md/CURRENT.json blobs in a new manifest, commit the checkpoint, update LATEST to that exact commit, and refetch/verify. Never embed a commit hash in content that determines the same commit. A plan delivery or checkpoint update is not a proof upgrade.
