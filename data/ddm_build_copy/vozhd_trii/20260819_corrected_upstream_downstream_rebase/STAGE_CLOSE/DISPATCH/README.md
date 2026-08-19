# VOZHD TRII STAGE-CLOSE DISPATCH PROTOCOL

Status: `ACTIVE_ADMINISTRATIVE_CONTROL_PLANE`
Semantic authority: `NONE`
Exact semantic common base: `baa257cb901ad8e5dc4d89faf2d81ea6f442ff8d`
Dispatch branch: `agent/vozhd-trii-stage-close-dispatch`

## Purpose

Preserve the economical command phrase `check your next assignment` without contaminating semantic worker branches, accepted result heads, seam packages, or stage contracts.

## Core separation law

Three identities MUST remain distinct:

1. `chat_id` — permanent identity of the already-open ChatGPT worker conversation. It never changes when the chat is recycled.
2. `assignment_id` — immutable administrative order issued to that chat. Each assignment has exactly one worker class, unit, mission branch, write root, authority set, output contract, and finite return-token set.
3. `semantic_result_identity` — the exact mission-branch result/head/blob(s) produced under an assignment. Administrative state is never part of this identity.

`chat_id != worker_role != unit != mission_branch != semantic_result_identity`.

## Stable worker-slot and user-facing addressing law

Each permanent chat also has one stable `worker_slot` number recorded in `MAILBOX_INDEX.json`. The slot does not change when the chat changes roles.

Every time HQ tells the user to send an already-open chat to its next assignment, the user-facing handoff MUST identify all four coordinates:

1. stable worker slot number;
2. permanent `chat_id`;
3. `most_recent_submitting_agent_id` — the unit/agent ID under which that chat most recently returned work to HQ;
4. new agent/unit ID being assigned.

Canonical display form:

`Worker #N — CHAT-... — most recent submitting agent OLD_ID -> new agent NEW_ID`

The user should be able to locate the correct open conversation from `OLD_ID` even when the permanent chat has already been recycled through multiple roles. HQ MUST NOT tell the user only `Worker #N` or only the new role when a recycled chat is being addressed.

The permanent chat ID does not change. What changes across assignments is the submitting agent/unit ID.

## Legacy-chat bootstrap law

The permanent-mailbox system was introduced after the current worker chats already existed. Therefore an existing chat that has never successfully consumed a mailbox assignment cannot discover the dispatch branch from its old semantic folder by the bare phrase `check your next assignment` alone.

For every permanent chat, dispatch state carries a `mailbox_bootstrap_state`.

Allowed values:

- `REQUIRED` — chat has not yet successfully consumed an assignment from the central dispatch mailbox;
- `ACKNOWLEDGED` — chat has successfully located and consumed its mailbox assignment at least once.

When `mailbox_bootstrap_state=REQUIRED`, HQ MUST give the user a one-time bridge message that explicitly names:

1. the dispatch branch `agent/vozhd-trii-stage-close-dispatch`;
2. the permanent `chat_id`;
3. the exact mailbox path `.../DISPATCH/MAILBOXES/<chat_id>/CURRENT.json`;
4. the exact `assignment_id` currently issued.

Canonical first-use message:

`Your assignment system has migrated. Read your permanent mailbox on branch agent/vozhd-trii-stage-close-dispatch at data/ddm_build_copy/vozhd_trii/20260819_corrected_upstream_downstream_rebase/STAGE_CLOSE/DISPATCH/MAILBOXES/<CHAT_ID>/CURRENT.json, then read the exact assignment it points to and execute it. Do not look for a new instruction file in your old semantic folder.`

A bare `Check your next assignment.` is valid ONLY after that chat's `mailbox_bootstrap_state=ACKNOWLEDGED`.

HQ marks a chat `ACKNOWLEDGED` only after repository evidence shows that the worker actually consumed the central assignment and began or returned work on the named mission branch. Merely sending the bridge message is not acknowledgement.

No bootstrap breadcrumb may be written to an old semantic branch. Bootstrap is user-to-chat routing plus central dispatch state only.

## Permanent mailbox law

Each open chat has one permanent mailbox under `DISPATCH/MAILBOXES/<chat_id>/`.

- `CURRENT.json` is the only mutable pointer for that chat.
- `ASSIGNMENTS/<assignment_id>.md` and `.json` are immutable once issued.
- `HISTORY.jsonl` is append-only administrative provenance when present.
- Workers NEVER write to the dispatch branch.
- HQ/Velikii Vozhd is the sole writer to dispatch state.

When the user says `check your next assignment`, the worker must:

1. identify its permanent `chat_id` from `MAILBOX_INDEX.json` or prior chat context;
2. read its mailbox `CURRENT.json` from this dispatch branch;
3. if `state=ISSUED`, read the exact immutable assignment artifact named there;
4. switch to the mission branch named by that assignment BEFORE writing;
5. write ONLY under the mission write root;
6. execute rather than returning readiness/status only;
7. return the exact finite token and exact semantic head requested by the assignment.

If `CURRENT.json` says `HOLD_FOR_COMMAND_REVIEW`, no new semantic work is authorized.

## Semantic branch hygiene

A semantic mission branch MUST contain only mission-authorized artifacts.

After a finite return is accepted or otherwise frozen:

- the semantic package is pinned by exact SHA/blob/content hashes;
- the semantic branch is IMMUTABLE;
- no `NEXT_ASSIGNMENT`, `00_NEW_ROLE_AND_TASK`, reassignment note, mailbox pointer, scheduling note, or other administrative file may be added;
- chat recycling occurs only through this dispatch branch;
- later dependencies read exact pinned semantic identities, never `latest` branch state.

Administrative commits are forbidden on semantic branches after this protocol takes effect.

## Assignment issue transaction

An assignment is not valid until all of the following exist in dispatch state:

1. immutable assignment file with unique `assignment_id`;
2. exact `chat_id` and stable `worker_slot`;
3. `most_recent_submitting_agent_id`;
4. explicit new worker class (`SUB-VOZHD`, `FLOATING_SPECIALIST`, `SEAM_BINDER`, `SEAM_PREFLIGHT_SPECIALIST`, `INSPECTORATE`, or later explicitly authorized class);
5. exact new agent/unit ID;
6. exact mission branch;
7. exact semantic launch base or exact branch-precondition check;
8. exact write root;
9. exact binding authorities by SHA/blob/hash wherever available;
10. explicit forbidden scope;
11. exact required outputs;
12. finite return-token set;
13. dependency/opening conditions;
14. `CURRENT.json` pointer updated to that immutable assignment.

No assignment may rely on prose such as `the latest accepted result` when an exact identity can be named.

## Return lifecycle

Dispatch state values:

- `HOLD_FOR_COMMAND_REVIEW`
- `ISSUED`
- `IN_PROGRESS_OBSERVED`
- `RETURNED_UNADJUDICATED`
- `ACCEPTED_FROZEN`
- `RETURN_FOR_HARMONIZATION`
- `REJECTED_NONCONFORMING`
- `SUPERSEDED`

A commit appearing on a mission branch proves only `IN_PROGRESS_OBSERVED`; it does not prove acceptance.

A finite token with wrong filenames, wrong output set, wrong branch/write root, missing required artifact, or unauthorized semantic amendment is `RETURNED_NONCONFORMING` unless HQ explicitly adjudicates a bounded exception. Substantive content may be retained as non-dispositive evidence without silently treating the exact-contract return as satisfied.

## Reassignment / recycling law

A completed chat may immediately receive another assignment, but only after:

1. its prior semantic result is pinned;
2. prior return disposition is recorded;
3. dependency gates for the new work are satisfied;
4. a new immutable assignment is issued in its permanent mailbox.

Recycling never changes the prior semantic branch and never changes the chat's permanent `chat_id` or stable `worker_slot`.

## Review-cycle law

HQ may run rapid recycle cycles, but the dispatch registry must declare a `review_epoch` and `recycle_budget`.

At the end of the declared budget:

- mailboxes go to `HOLD_FOR_COMMAND_REVIEW`;
- no further missions are issued;
- HQ performs cross-worker adjudication and semantic-pin reconciliation;
- only after the review/cleanup receipt is frozen may another dispatch epoch open.

Current dispatch epoch: `R03_STAGE_CLOSE_DISPATCH_EPOCH_02`.
Current initial issued missions: `M4_FINAL` and `SCRV3_M6_HANDOFF_LITERALIZATION`.
Planned dependency-following missions after accepted returns: `M5_FINAL`, `M6_FINAL`, then `POST_REVIEW_INSPECTORATE_RECLOSURE` after M4/M5/M6 acceptance.

## Legacy contamination cleanup

The earlier `00_NEW_ROLE_AND_TASK.md` mechanism is `LEGACY_SUPERSEDED` and MUST NOT be copied forward.

Cleanup is branch-specific and occurs only after provenance review. No destructive ref movement is authorized merely by detecting a legacy assignment file. Semantic provenance must be proved first.

## Production gate

This dispatch protocol authorizes no production implementation and changes no R03 broad topology.
