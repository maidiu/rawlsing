# RAWLSING HQ HANDOFF PROTOCOL

Status: `ADOPTED__CANONICAL_HQ_SUCCESSION_PROTOCOL_R2`

Schema: `RAWLSING_HQ_HANDOFF_PROTOCOL@1.1.0`

## Purpose

The repository, not conversational memory, is the authoritative HQ memory bus. A new HQ resolves one canonical pointer, reads one immutable checkpoint packet, reconciles only the live edges explicitly named by that checkpoint, and continues from that state.

## Canonical entrypoint

Read `HQ_HANDOFF/LATEST.json` on `integration/pre-main-reconciliation-r1`.

`LATEST.json` is a mutable pointer only. It points to one immutable checkpoint directory `HQ_HANDOFF/checkpoints/<checkpoint_id>/` and one exact handoff commit.

## Checkpoint packet

Every checkpoint MUST contain:

- `CURRENT.md` — compact human-readable operative state;
- `CURRENT.json` — machine-readable exact operative state;
- `MANIFEST.json` — packet manifest binding checkpoint ID, semantic PRE-MAIN tip, exact file paths, and immutable Git blob identities for `CURRENT.md` and `CURRENT.json`. SHA-256 content digests may additionally be recorded when independently available.

Every checkpoint MUST carry a stable `checkpoint_id`. `LATEST.json.handoff_commit` is the authoritative Git snapshot containing the immutable packet. Do not attempt to embed a commit SHA inside a file whose contents determine that same commit SHA.

Prior checkpoint directories are immutable historical state. Never rewrite them.

## Semantic PRE-MAIN vs handoff metadata

Every checkpoint distinguishes `semantic_pre_main_tip`, `LATEST.json.handoff_commit`, and current control-branch HEAD. A successor MUST NOT infer semantic architecture change merely because branch HEAD is later than `semantic_pre_main_tip`.

## Temporal reconciliation law

The checkpoint is the **last sealed HQ authority**, not a command to ignore later authorized worker movement.

Mandatory categories:

1. `SEALED_CHECKPOINT_AUTHORITY` — state already adjudicated/adopted by HQ.
2. `POST_CHECKPOINT_PENDING_RETURN` — a checkpoint-named active worker branch advanced after checkpoint cut with a governed return awaiting HQ adjudication. New pending HQ input: neither inherited authority nor ignorable history.
3. `UNAUTHORIZED_POST_CHECKPOINT_MOVEMENT` — branch movement that does not satisfy its governed return/lineage protocol. Do not consume it as authority.

Incoming reconciliation:

1. load the immutable checkpoint as last sealed authority;
2. verify every named active worker branch against its recorded commission tip / observed head;
3. unchanged means still active;
4. advanced means inspect only enough governed return lineage to classify it;
5. valid return -> `POST_CHECKPOINT_PENDING_RETURN`, adjudicate/fan in normally;
6. invalid/unexplained movement -> `UNAUTHORIZED_POST_CHECKPOINT_MOVEMENT`, do not consume;
7. only after HQ adjudication may operative state change and a successor checkpoint be minted.

Never silently treat post-checkpoint output as adopted authority.

## Active-worker checkpoint law

Every `CURRENT.json.active_workers[]` entry MUST include:

- `id`, `branch`, `commission_tip`, `observed_head_at_checkpoint`, `grain`;
- `library_access`;
- `pass_wake`;
- `blocker_effect`;
- `hard_forbidden`.

Normal succession should not require reopening worker commissions merely to know what their return means.

## Dependency / wake-graph law

Material downstream gates MUST be explicit in `CURRENT.json.dependency_graph`, including status, prerequisites, wake effect, and prohibited early actions. Do not invent an automatic wake where none is encoded.

## Source roles

GitHub/repository is authoritative for HQ state, commissions/returns, adopted/superseded/quarantined authority, code/blobs, semantic owners, blockers, wake conditions, integration state, and next lawful work.

Library is the evidence/carrier warehouse. Library evidence does not self-authorize Rawlsing semantics.

## Library permission modes

Normalize active-worker Library permissions to exactly:

- `NO` — no Library use authorized by current commission;
- `EXACT_ONLY` — only explicitly listed file IDs/versions/purposes;
- `ESCALATION_ONLY` — only after an exact named trigger and within explicitly bounded scope.

If a commission requires a blocker when repo-bound evidence is insufficient, checkpoint mode is `NO`, not inferred search permission.

## Major negative-authority summaries

Preserve every material defect slot needed to stop rediscovery or semantic laundering. Do not omit a source/channel/receiver defect merely for compactness.

## Candidate-status summaries

For material candidates distinguish producer existence, independent qualification, execution blocker, downstream authorization, and next wake.

## Worker law

HQ succession and Rabochii execution are separate protocols. A worker's branch-local `00_COMMISSION.md` remains authoritative for its bounded grain.

## Incoming HQ procedure

A new HQ MUST:

1. fetch `LATEST.json`;
2. read `CURRENT.md`, `CURRENT.json`, and `MANIFEST.json` at `LATEST.json.handoff_commit`;
3. verify checkpoint ID/path consistency and manifest Git blob identities;
4. establish checkpoint as `SEALED_CHECKPOINT_AUTHORITY`;
5. reconcile named active workers under the temporal law;
6. obey constitutional/quarantine/supersession declarations;
7. wake only explicitly satisfied gates;
8. never reconstruct deprecated semantics from ancestry;
9. after every material HQ state change update durable decisions as needed, create a new immutable checkpoint, advance `LATEST.json`, and verify before sealing.

## Material HQ state change

Includes authority adoption/rejection/supersession/quarantine; qualified code integration; fan-in changing blocker/wake graph; active-lane commissioning/cancellation/completion/replacement; new canonical world/release/root identity; opening/closing a project-critical execution gate; or any durable decision whose absence could cause duplicated work, revived rejected semantics, missed work, or unlawful action.

Mere commentary, exploratory reads, and non-operative observations do not require a checkpoint.

## Outgoing HQ procedure

1. fan in returns actually received;
2. perform lawful adoption/integration;
3. append durable decisions as needed;
4. create new `CURRENT.md` and `CURRENT.json`;
5. fetch their immutable Git blob identities and create `MANIFEST.json` binding them;
6. commit the packet;
7. update `LATEST.json` to the exact packet commit/path set;
8. re-resolve `LATEST.json` and verify checkpoint identity/manifest blob bindings before sealing.

A handoff is stale if material operative state changed after the checkpoint named by `LATEST.json`.

## Decision ledger law

`HQ_HANDOFF/DECISION_LEDGER.jsonl` is append-only by semantic policy. Record durable decisions, not diary entries.

## Fidelity diagnostics

`HQ_HANDOFF/FIDELITY_DIAGNOSTIC.md` is the canonical read-only succession test. `repository reads beyond checkpoint` is a quality metric. Ordinary succession target: `LATEST + immutable checkpoint packet + named active branch heads`; deeper reads should normally be required only to adjudicate actual new returns.

## Minimal succession prompt

> Become Rawlsing HQ. Read `HQ_HANDOFF/LATEST.json` on `integration/pre-main-reconciliation-r1`, verify the immutable checkpoint packet it names, establish it as the last sealed HQ authority, reconcile only its named live worker edges under the post-checkpoint return law, then execute its succession instructions. Do not reconstruct state from conversational memory when the checkpoint supplies it. After every material HQ state change, update durable decisions as needed, create a new immutable checkpoint, advance `HQ_HANDOFF/LATEST.json`, and verify the pointer before considering that transition sealed.

Terminal:

`RAWLSING_HQ_HANDOFF_PROTOCOL_R2__ADOPTED`
