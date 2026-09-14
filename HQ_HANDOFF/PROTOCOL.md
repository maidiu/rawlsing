# RAWLSING HQ HANDOFF PROTOCOL

Status: `ADOPTED__CANONICAL_HQ_SUCCESSION_PROTOCOL_R2`

Schema: `RAWLSING_HQ_HANDOFF_PROTOCOL@1.1.0`

## Purpose

The repository, not conversational memory, is the authoritative HQ memory bus.

A new HQ chat should resolve one canonical pointer, read one immutable checkpoint packet, reconcile only the live edges explicitly named by that checkpoint, and continue from that state. It should not reconstruct operative state by grokking the whole repository, relying on prior-chat memory, or asking the user to act as a sync bus.

## Canonical entrypoint

Read `HQ_HANDOFF/LATEST.json` on branch `integration/pre-main-reconciliation-r1`.

`LATEST.json` is a mutable pointer only. It is not semantic authority by itself. It points to one immutable checkpoint directory `HQ_HANDOFF/checkpoints/<checkpoint_id>/` and one exact handoff commit.

## Checkpoint packet

Every checkpoint MUST contain:

- `CURRENT.md` — compact human-readable operative state;
- `CURRENT.json` — machine-readable exact operative state;
- `MANIFEST.json` — packet manifest binding checkpoint ID, semantic PRE-MAIN tip, file paths, and SHA-256 digests of `CURRENT.md` and `CURRENT.json`.

Every checkpoint MUST carry a stable `checkpoint_id`. `LATEST.json.handoff_commit` is the authoritative Git snapshot containing the immutable packet. Do not try to embed a commit SHA inside a file whose contents determine that commit SHA.

Prior checkpoint directories are immutable historical state. Never rewrite them. Create a new checkpoint directory for every material HQ transition.

## Semantic PRE-MAIN vs handoff metadata

Every checkpoint distinguishes:

- `semantic_pre_main_tip` — last commit representing operative Rawlsing semantic/build state before handoff bookkeeping;
- `handoff_commit` — supplied by `LATEST.json`, exact immutable Git commit containing the checkpoint packet;
- current control-branch HEAD — may be later because handoff bookkeeping and later worker movement can occur.

A successor MUST NOT infer semantic architecture change merely because branch HEAD is later than `semantic_pre_main_tip`.

## Temporal reconciliation law

The checkpoint is the **last sealed HQ authority**, not a command to ignore later authorized worker movement.

Three categories are mandatory:

1. `SEALED_CHECKPOINT_AUTHORITY` — state already adjudicated/adopted by HQ in the immutable checkpoint.
2. `POST_CHECKPOINT_PENDING_RETURN` — a checkpoint-named active worker branch has advanced after checkpoint cut with a governed return that is awaiting HQ adjudication. This is new pending HQ input: neither inherited authority nor ignorable history.
3. `UNAUTHORIZED_POST_CHECKPOINT_MOVEMENT` — a named active worker branch advanced without satisfying its governed return/lineage protocol. Do not consume it as authority.

Incoming HQ reconciliation procedure:

1. load the immutable checkpoint and establish it as the last sealed HQ authority;
2. verify every active worker branch named by the checkpoint against its recorded commission tip / observed head;
3. if unchanged, leave the worker active;
4. if advanced, inspect only the governed return lineage necessary to classify the movement;
5. classify a valid return as `POST_CHECKPOINT_PENDING_RETURN` and adjudicate/fan it in normally;
6. classify invalid/unexplained movement as `UNAUTHORIZED_POST_CHECKPOINT_MOVEMENT` and do not consume it;
7. only after HQ adjudication may operative state change and a successor checkpoint be minted.

Never silently treat a post-checkpoint worker return as already adopted authority.

## Active-worker checkpoint law

Every `CURRENT.json.active_workers[]` entry MUST include at minimum:

- `id`;
- `branch`;
- `commission_tip`;
- `observed_head_at_checkpoint`;
- `grain`;
- `library_access`;
- `pass_wake`;
- `blocker_effect`;
- `hard_forbidden`.

This should make normal succession possible without reopening worker commissions merely to understand what their return would mean.

## Dependency / wake-graph law

Material downstream gates MUST be represented explicitly in `CURRENT.json.dependency_graph` rather than distributed only across historical returns.

Each dependency node should state:

- current status;
- conjunctive/disjunctive prerequisites;
- wake effect;
- prohibited early actions.

A successor must not invent an automatic wake where the checkpoint does not encode one.

## Source roles

### GitHub / repository

GitHub is authoritative for current HQ state, commissions, governed returns, adopted/superseded/quarantined authority, executable code/blobs, competent semantic owners, blockers, wake conditions, integration state, and next lawful work.

### Library

Library is the evidence/carrier warehouse for survey carriers, codebooks/source documentation, PDFs/books, and source corpora inappropriate for Git. Library evidence does not self-authorize Rawlsing semantics.

## Library permission modes

Avoid ambiguous `NO_BY_DEFAULT` language in checkpoint state. Normalize every active worker to one of:

- `NO` — no Library use authorized by the current commission;
- `EXACT_ONLY` — only explicitly listed file IDs/versions/purposes may be consumed;
- `ESCALATION_ONLY` — Library access is permitted only after an exact named trigger and only within the explicitly bounded scope recorded in the checkpoint/commission.

If a commission says to return a blocker when repo-bound evidence is insufficient, its checkpoint Library mode is `NO`, not an inferred invitation to search Library.

## Major negative-authority summaries

When a closed/rejected route has multiple independent defects, `CURRENT.json` MUST preserve all material slots needed to prevent rediscovery or semantic laundering. Do not compact a three-slot failure into only one or two slots if the omitted slot would require archaeology to recover.

## Candidate-status summaries

For material candidates, compact checkpoint state should distinguish producer existence from independent qualification and downstream authorization. Example fields may include `producer_status`, `independent_qualification`, `execution_blocker`, `downstream_authorized`, and `next_wake`.

## Worker law

HQ succession and Rabochii execution are separate protocols. A commissioned worker's branch-local `00_COMMISSION.md` remains authoritative for its bounded grain. Workers should not need the full HQ checkpoint unless their commission explicitly binds it.

## Incoming HQ procedure

A new HQ MUST:

1. fetch `HQ_HANDOFF/LATEST.json` from `integration/pre-main-reconciliation-r1`;
2. read `CURRENT.md`, `CURRENT.json`, and `MANIFEST.json` at `LATEST.json.handoff_commit`;
3. verify manifest digests and checkpoint identity;
4. establish the checkpoint as `SEALED_CHECKPOINT_AUTHORITY`;
5. reconcile named active worker branches under the temporal reconciliation law;
6. obey constitutional laws and quarantine/supersession declarations;
7. continue active lanes and wake only successors whose encoded gates are satisfied;
8. never reconstruct deprecated semantics merely because Git ancestry contains them;
9. after every material HQ state change, update durable decisions as needed, create a new immutable checkpoint, advance `LATEST.json`, and verify it before treating the transition as sealed.

## Material HQ state change

Includes at minimum authority adoption/rejection/supersession/quarantine; integration of qualified production/runtime code; worker fan-in changing blocker/wake graph; commissioning/cancellation/completion/replacement changing successor action; new canonical world/release/root identity; opening/closing a project-critical execution gate; or any durable decision whose absence could cause duplicated work, revived rejected semantics, a missed active lane, or an unlawful next action.

Mere commentary, exploratory reads, and non-operative observations do not require a checkpoint.

## Outgoing HQ procedure

Before succession, HQ MUST ensure current operative state is checkpointed:

1. fan in returns actually received;
2. perform lawful HQ adoption/integration;
3. append material holdings to `DECISION_LEDGER.jsonl` as needed;
4. create new checkpoint `CURRENT.md` and `CURRENT.json`;
5. compute their SHA-256 digests and create `MANIFEST.json`;
6. commit the immutable packet;
7. update `LATEST.json` to that exact commit/path set;
8. re-resolve `LATEST.json`, read the packet from the pinned commit, and verify identity/digests before sealing the transition.

A handoff is stale if material operative state has changed since the checkpoint named by `LATEST.json`.

## Decision ledger law

`HQ_HANDOFF/DECISION_LEDGER.jsonl` is append-only by semantic policy. Record durable decisions whose rediscovery would waste work or risk semantic regression; do not turn it into a diary.

## Fidelity diagnostics

`HQ_HANDOFF/FIDELITY_DIAGNOSTIC.md` is the canonical read-only succession test. Its `repository reads beyond checkpoint` section is a quality metric: normal succession should approach `LATEST + checkpoint packet + named active branch heads`, with deeper reads needed only to adjudicate actual new returns.

## Minimal succession prompt

> Become Rawlsing HQ. Read `HQ_HANDOFF/LATEST.json` on `integration/pre-main-reconciliation-r1`, verify the immutable checkpoint packet it names, establish it as the last sealed HQ authority, reconcile only its named live worker edges under the post-checkpoint return law, then execute its succession instructions. Do not reconstruct state from conversational memory when the checkpoint supplies it. After every material HQ state change, update durable decisions as needed, create a new immutable checkpoint, advance `HQ_HANDOFF/LATEST.json`, and verify the pointer before considering that transition sealed.

Terminal:

`RAWLSING_HQ_HANDOFF_PROTOCOL_R2__ADOPTED`
