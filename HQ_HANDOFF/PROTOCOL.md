# RAWLSING HQ HANDOFF PROTOCOL

Status: `ADOPTED__CANONICAL_HQ_SUCCESSION_PROTOCOL_R1`

Schema: `RAWLSING_HQ_HANDOFF_PROTOCOL@1.0.0`

## Purpose

The repository, not conversational memory, is the authoritative HQ memory bus.

A new HQ chat should not reconstruct operative state by reading the whole repository, relying on prior-chat memory, or asking the user to paste a giant prompt. It should resolve one canonical pointer, read one immutable checkpoint packet, verify the exact referenced identities, and continue from that state.

## Canonical entrypoint

Read:

`HQ_HANDOFF/LATEST.json`

on branch:

`integration/pre-main-reconciliation-r1`

`LATEST.json` is a mutable pointer only. It is not semantic authority by itself.

It points to one immutable checkpoint directory:

`HQ_HANDOFF/checkpoints/<checkpoint_id>/`

and one exact checkpoint commit.

## Checkpoint packet

Every checkpoint MUST contain:

- `CURRENT.md` — compact human-readable operative state;
- `CURRENT.json` — machine-readable exact state.

The checkpoint may cite the append-only decision ledger:

`HQ_HANDOFF/DECISION_LEDGER.jsonl`

The checkpoint files at their checkpoint commit are immutable historical state. Later HQs create new checkpoint directories rather than rewriting prior checkpoints.

## Semantic PRE-MAIN vs handoff metadata

Handoff bookkeeping commits may advance the Git branch without changing Rawlsing semantics.

Every checkpoint therefore distinguishes:

- `semantic_pre_main_tip` — last commit whose contents represent the operative Rawlsing semantic/build state before the checkpoint bookkeeping;
- `checkpoint_commit` — supplied by `LATEST.json`, the exact immutable Git commit containing the checkpoint packet;
- current branch HEAD — may be later because `LATEST.json` itself is a mutable pointer.

A successor MUST NOT infer a semantic architecture change merely because branch HEAD is later than `semantic_pre_main_tip`.

## Source roles

### GitHub / repository

GitHub is the authoritative coordination substrate for:

- current HQ state;
- commissions and governed returns;
- adopted authority;
- executable code and exact blobs;
- blockers and competent owners;
- wake conditions;
- quarantines / supersession;
- integration state;
- next lawful work.

### Library

Library is the evidence/carrier warehouse for:

- survey carriers;
- codebooks and source documentation;
- PDFs/books;
- source corpora too large or inappropriate for Git.

A handoff MUST identify Library inputs by exact known identity whenever they matter. A successor should not broadly search Library merely because Library exists.

## Worker law

HQ succession and Rabochii execution are separate protocols.

For a commissioned worker, its branch-local `00_COMMISSION.md` remains authoritative. The worker should not need the full HQ checkpoint unless its commission explicitly binds it.

The ideal worker assignment remains as small as:

`you are <WORKER_ID>`

provided the current router/registry maps that ID to an exact branch and commission tip.

## Incoming HQ procedure

A new HQ MUST:

1. fetch `HQ_HANDOFF/LATEST.json` from `integration/pre-main-reconciliation-r1`;
2. read the exact checkpoint `CURRENT.md` and `CURRENT.json` at `LATEST.json.handoff_commit`;
3. verify the named active worker branches/tips before acting on any claimed return;
4. treat `CURRENT.json` exact refs as pointers, not substitutes for the underlying governed artifacts when detailed adjudication is required;
5. obey all constitutional laws and quarantine/supersession declarations in the checkpoint;
6. continue active lanes and wake only successors whose explicit gates are satisfied;
7. never reconstruct deprecated semantics merely because Git ancestry contains them;
8. after material HQ state changes, create a new immutable checkpoint and advance `LATEST.json`.

## Outgoing HQ procedure

Before succession, HQ SHOULD:

1. fan in all returns actually received;
2. perform any lawful HQ integration/adoption;
3. append material holdings to `DECISION_LEDGER.jsonl`;
4. create a new checkpoint directory with `CURRENT.md` and `CURRENT.json`;
5. commit the checkpoint;
6. update `HQ_HANDOFF/LATEST.json` to that checkpoint commit;
7. hand the next agent the one-line succession instruction.

## Decision ledger law

`HQ_HANDOFF/DECISION_LEDGER.jsonl` is append-only by semantic policy.

Each line is one JSON object with stable fields including:

- `decision_id`;
- `date`;
- `status`;
- `subject`;
- `holding`;
- `authority_refs`;
- `supersedes` when applicable;
- `wake_effect` when applicable.

Do not turn the ledger into a diary. Record decisions whose rediscovery would waste work or risk semantic regression.

## Minimal succession prompt

The canonical human handoff is:

> Become Rawlsing HQ. Read `HQ_HANDOFF/LATEST.json` on `integration/pre-main-reconciliation-r1`, verify and read the immutable checkpoint it names, then execute its succession instructions. Do not reconstruct state from conversational memory when the checkpoint supplies it.

Terminal:

`RAWLSING_HQ_HANDOFF_PROTOCOL_R1__ADOPTED`
