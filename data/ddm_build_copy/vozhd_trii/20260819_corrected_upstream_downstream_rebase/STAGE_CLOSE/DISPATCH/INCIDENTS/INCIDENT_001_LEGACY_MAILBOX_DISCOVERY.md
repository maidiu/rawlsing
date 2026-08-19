# DISPATCH INCIDENT 001 — LEGACY CHAT COULD NOT DISCOVER CENTRAL MAILBOX

Status: `ROOT_CAUSE_CONFIRMED__PROTOCOL_CORRECTED`
Date: `2026-08-19`
Affected worker: `Worker #10 / CHAT-S5578C / most recent submitting agent M4_PREFLIGHT`
Issued assignment: `E02-W10-M4-FINAL-001`
New agent: `M4_FINAL`

## Observed failure

The user sent the legacy recycled chat the bare command `Check your next assignment.`

The worker inspected its old semantic/preflight folder `STAGE_CLOSE/SEAMS/M4/preflight/`, found no new HQ instruction file, inspected the likely successor M4 branch at the exact common base, and correctly refused to infer authority from branch naming alone.

## Root cause

The new central mailbox assignment existed correctly on `agent/vozhd-trii-stage-close-dispatch`, but the already-existing worker conversation had never been taught that branch/path. The dispatch design separated administrative state from semantic branches correctly but omitted the one-time discovery/bootstrap mechanism required to migrate legacy chats.

Therefore:

`ASSIGNMENT_EXISTS != LEGACY_CHAT_CAN_DISCOVER_ASSIGNMENT`

The failure was routing/discovery, not semantic assignment construction and not worker noncompliance.

## Corrective law

1. No administrative breadcrumb is written back onto an accepted semantic branch.
2. Every pre-mailbox legacy chat has `mailbox_bootstrap_state=REQUIRED` until it successfully consumes a central mailbox assignment.
3. While bootstrap is required, bare `Check your next assignment.` is forbidden as the user-facing launch message.
4. HQ must provide the dispatch branch, permanent chat ID, exact mailbox path, and current assignment ID in a one-time bridge message.
5. Repository evidence that the worker began/returned work on the named mission branch is required before HQ marks bootstrap `ACKNOWLEDGED`.
6. After acknowledgement, the economical bare command is lawful for that same continuing chat.
7. Any newly created worker chat after this protocol must receive its permanent chat ID and dispatch mailbox location in its initial launch order, so it begins life mailbox-aware rather than requiring later migration.

## Immediate repair

Worker #10 remains assigned to `M4_FINAL`; no assignment replacement is needed.

Its canonical mailbox is:
`data/ddm_build_copy/vozhd_trii/20260819_corrected_upstream_downstream_rebase/STAGE_CLOSE/DISPATCH/MAILBOXES/CHAT-S5578C/CURRENT.json`

on branch:
`agent/vozhd-trii-stage-close-dispatch`

Current assignment ID:
`E02-W10-M4-FINAL-001`

Worker #3 / `CHAT-SCRV3` is also marked bootstrap-required before its first central-mailbox launch.

No semantic branch was modified by this corrective action. Production implementation remains unauthorized. Broad topology remains unchanged.
