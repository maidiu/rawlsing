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

## Permanent mailbox law

Each open chat has one permanent mailbox under `DISPATCH/MAILBOXES/<chat_id>/`.

- `CURRENT.json` is the only mutable pointer for that chat.
- `ASSIGNMENTS/<assignment_id>.md` and `.json` are immutable once issued.
- `HISTORY.jsonl` is append-only administrative provenance.
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

An assignment is not valid until all of the following exist atomically in dispatch state:

1. immutable assignment file with unique `assignment_id`;
2. exact `chat_id`;
3. explicit worker class (`SUB-VOZHD`, `FLOATING_SPECIALIST`, `SEAM_BINDER`, `SEAM_PREFLIGHT_SPECIALIST`, `INSPECTORATE`, or later explicitly authorized class);
4. exact mission branch;
5. exact semantic launch base or exact branch-precondition check;
6. exact write root;
7. exact binding authorities by SHA/blob/hash wherever available;
8. explicit forbidden scope;
9. exact required outputs;
10. finite return-token set;
11. dependency/opening conditions;
12. `CURRENT.json` pointer updated to that immutable assignment.

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

Recycling never changes the prior semantic branch and never changes the chat's permanent `chat_id`.

## Review-cycle law

HQ may run rapid recycle cycles, but the dispatch registry must declare a `review_epoch` and `recycle_budget`.

At the end of the declared budget:

- mailboxes go to `HOLD_FOR_COMMAND_REVIEW`;
- no further missions are issued;
- HQ performs cross-worker adjudication and semantic-pin reconciliation;
- only after the review/cleanup receipt is frozen may another dispatch epoch open.

Current epoch is frozen for command review.

## Legacy contamination cleanup

The earlier `00_NEW_ROLE_AND_TASK.md` mechanism is `LEGACY_SUPERSEDED`.

It MUST NOT be copied forward.

Cleanup is branch-specific and occurs only after provenance review:

- pure admin-only tail after a frozen semantic head -> branch may be reset to frozen semantic head after the assignment is archived here;
- later legitimate semantic amendments before an admin tail -> adjudicate and pin the lawful semantic amendment head first, then remove only the admin tail;
- admin content interleaved with later substantive commits -> do not blind-reset; reconstruct or explicitly grandfather/pin the semantic package before branch normalization.

No destructive ref movement is authorized merely by detecting a legacy assignment file. Semantic provenance must be proved first.

## Production gate

This dispatch protocol authorizes no production implementation and changes no R03 broad topology.
