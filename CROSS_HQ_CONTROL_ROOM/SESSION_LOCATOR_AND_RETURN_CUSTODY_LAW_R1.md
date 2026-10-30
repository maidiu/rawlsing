# Mandatory cross-HQ worker session locator and return custody law — 2026-10-30

**USER-DIRECTED OPERATING REQUIREMENT — applies to PRE-MAIN, Pyat and Sorok HQ grokking, commissioning, dispatch, resumption, return intake and reviewer handoff.** This law is a staged process/control amendment until approved and merged into canonical PRE-MAIN; it does not confer original CAN/ADP/Pyat/SCI05/C8/C12 science/actor authority, change old commissions or authorize a merge.

## Problem and actual mechanism

The branch and Git SHA identify code, **not the human-operable chat/session that originally executed it**. Historical returns name OpenCode or macOS without saying which of two Macs or which app window, forcing searches through unrelated app windows/history. At every launch and return, record an **actual navigable operator locator** before the source becomes stale. Machines are **exactly** `oldMac` and `mainMac` as the user renamed them, plus `BROWSER` or `OTHER_VERIFIED` for a genuine non-Mac browser/cloud environment. Do not infer `oldMac` vs `mainMac` from macOS, x86_64, local paths, account, repository checkout or a model name. Browser has no Mac ownership unless the user verifies the launch host separately.

The persistent single entrypoint is `CROSS_HQ_CONTROL_ROOM/SESSION_LOCATORS.json`, plus one signed-by-reporting-agent/human **self-attested** manifest in each new `WORKER_RETURNS/<lane>/SESSION_LOCATOR.json`. Each commission must declare the intended row before dispatch in `WORKER_COMMISSIONS/<lane>/SESSION_LOCATOR_DISPATCH.json`. Those are **operational locators**, not immutable provider audit logs, security signatures, user identity attestation, external model/source authorization or permanent access to provider transcripts.

## Required dispatch fields — exact, no substitutions

- `commission_id`, `branch`, `sealed_commission_sha`, `status` = `SEALED_NOT_LAUNCHED | ACTIVE_VERIFIED | RETURNED | HOLD`.
- `device`: `oldMac | mainMac | BROWSER | OTHER_VERIFIED | UNKNOWN`; `device_evidence` describing whether confirmed by user, by local `scutil --get ComputerName`/`hostname` on the verified Mac, or unknown. Distinguish configured name from `hostname`; never silently rewrite old records.
- `agent_name` and `agent_id`: exact app agent/profile/worker name and identifier where the editor exposes it (such as OpenCode's selected agent, Codex agent/session profile, or a named Browser agent). Do not confuse agent with harness, provider, model, session, commission role or process. Set `UNKNOWN` if not exposed; `agent_role` captures actual selected agent mode if exposed, otherwise `UNKNOWN`.
- `harness`: **`Codex | OpenCode | DeepSeek-Harness | Browser | OTHER_VERIFIED | UNKNOWN`**. `model_provider`, `model_id`, `reasoning_effort_requested`, `reasoning_effort_verified` and `evidence_source` separate. A DeepSeek model within OpenCode is **OpenCode**, not automatically DeepSeek-Harness. An unexposed MAX selector is `UNVERIFIED`.
- `session_name`: exact app-visible conversation/session title, **operator supplied or verified in actual interface**; `session_id` and `session_url` when exposed, with `session_locator_type = APP_TITLE | APP_SESSION_ID | APP_URL | WORKTREE_AND_OPERATOR_NOTE | UNKNOWN`; do not invent app deep links, hidden provider IDs, ticket handles, or machine endpoints. A local `window_ordinal` or `workspace_name` may supplement a repeated title, but is not a globally unique ID.
- `worktree_path` (local only, diagnostic; never a shared-source authority claim), `editor_workspace`, `operating_account_label` (optional nonsensitive operator nickname, **no email/account ID/password/token**).
- `original_implementing_session` = exact known prior commission/session locator or `UNKNOWN`, `is_resumption`, `parent_session` if any, `reviewer_session` separate, `return_sha`, `return_directory`, `collected_at`, `confirmed_by` = `USER | WORKER | REVIEWER | UNVERIFIED`.
- Record `machine_claim` as **SELF_REPORTED** unless authenticated machine evidence actually exists. Do not pretend the Browser can inspect user's two Macs.

## Launch/resume loop — binding

1. **Before issue:** find the actual ORIGINAL implementing lane by exact branch+SHA from return/flight, then check `SESSION_LOCATORS.json` and original `SESSION_LOCATOR.json`. If present, quote `device / harness / session_name / session_id or URL / worktree / exact SHA` in the follow-up prompt. Decide whether to resume original implementing session or use independent reviewer; an independent review may never be silently routed into author session.
2. **Before user dispatch:** put `SESSION_LOCATOR_DISPATCH.json` in commission, with intended host/harness if selected, otherwise `UNKNOWN`; instructions direct the **operator** to rename the window before dispatch using a unique, searchable title such as `SOROK F2I | REVIEW | <short-branch> | oldMac | OpenCode`. Actual user-facing title/session id must be confirmed by operator; a proposed title is `suggested_session_name`, not observed `session_name`.
3. **At start:** worker asks/checks **once** for missing host or app title when it cannot inspect them; for a completed worker, return existing technical deliverable even if title remains unknown. Set `device` from local actual machine identity only when it matches user-renamed machine; otherwise `UNKNOWN` with observed raw value. Browser sets `BROWSER`, unless it is a local browser on a named Mac and that is actually verified. Capture original user-selected model/editor and effort status.
4. **At return:** write `SESSION_LOCATOR.json` on own return branch along with normal files. Include user-visible exact app title; self-attest whether title was inspected or supplied by operator. Record final remote SHA in subsequent **central registry intake**, not self-referentially in the file; if not known at file commit, set `return_sha: null` and include resolution method. Keep exact return branch and remote head externally verifiable.
5. **HQ intake:** direct-readback original return and original session manifest; append new locator row / supersession event to `SESSION_LOCATORS.json`. Never overwrite an old attribution; uncertainty is recorded. Pair every PRE-MAIN fan-in event with a `session_registry_id` or explicitly typed `HISTORICAL_SESSION_UNKNOWN`. Cross-HQ owner publishes only through its own authorized control/CAS path; source-return append does not adopt code.
6. **At grok/resumption:** enumerate **active/returned session indexes** for both `oldMac` and `mainMac`, plus Browser. Preserve actual app names separately from model, look up last implementing session before sending "use original session" instructions, and include locator in each copied prompt.
7. **Failure:** If operator cannot find the exact title/link, use branch/return SHA and `worktree_path` as an explicit fallback, never an invented locator; tag `SESSION_NOT_FOUND__REQUIRES_OPERATOR_CONFIRMATION`. Missing locator is a **dispatch-compliance defect** for NEW commissions; existing engineering evidence is not invalidated retroactively.

## Branch/CAS discipline and independent review

The registry is append-only **event-sourced**: newly observed or corrected facts append new `revision` for the same `commission_id`; historical rows remain. The latest valid row is selected by `revision`, not timestamp guessing. If the user's app UI renames a session, append the new exact title and preserve the older one as alias. Session identity is not source authority or cryptographic evidence. A worker may update its own return manifest only; **PRE-MAIN owner** updates canonical registry together with current flight/control intake via authorized CAS; preserve reviewer independence.

Log minimal access-safe identifiers. Never store login credentials, internal local service tokens, or transcript contents; operator may prefer a locally searchable session title over a private session URL. `UNKNOWN` permitted on historical evidence, but follow-up prompts must name it and request confirmation rather than pretending it is known.

## Machine-readable enforcement

`verify_session_locators.py` validates required fields, enumerations, same-commission ordered revisions, unique registry IDs, strict locator/confirmation enums, title/evidence consistency, no observed title from a suggested-only field, no unsafe guess that DeepSeek model implies DeepSeek-Harness, no mistaken user-confirmed machine from a generic macOS architecture, and no locator-issued source/adoption authority. When a previous registry snapshot or `--baseline-ref` is supplied, every historical row must remain an exact ordered prefix; rewriting, deleting or reordering a historical row is rejected. When a local Git repository is supplied, a non-null `return_sha` must exist as a commit; with `--require-sha` a missing/fake 40-hex SHA is rejected, and with `--require-sha-branch` the commit must be reachable from the declared branch. It is an **offline schema/custody consistency check**, not a machine-attestation mechanism. CI on the proposed PR should run `--selftest` and the G1–G6 unittest; PRE-MAIN required-check protection and original-owner progress CAS remain separate.

## Ready-to-copy mandatory header for ALL three HQs

```text
SESSION_CUSTODY (MANDATORY)
DEVICE: oldMac | mainMac | BROWSER | OTHER_VERIFIED | UNKNOWN
DEVICE_VERIFICATION: user-confirmed | local-machine-name-verified | self-reported | unverified
HARNESS: Codex | OpenCode | DeepSeek-Harness | Browser | OTHER_VERIFIED | UNKNOWN
AGENT_NAME / AGENT_ID / AGENT_ROLE: exact actual app agent/profile and mode | UNKNOWN
MODEL_ID: exact actual model; EFFORT_REQUESTED / EFFORT_VERIFIED separately
SESSION_NAME: exact app-visible title (verified/user-supplied) | UNKNOWN
SESSION_ID_OR_URL: exact app locator if available | UNKNOWN
SUGGESTED_SESSION_NAME: explicit searchable proposed title (NOT observed)
WORKTREE: local path if known | UNKNOWN
ORIGINAL_IMPLEMENTING_SESSION: same fields from exact prior author receipt | UNKNOWN
INDEPENDENT_REVIEWER_SESSION: different actual session | NOT_ASSIGNED
COMMISSION_SHA / RETURN_SHA: exact 40-hex or PENDING
NO_AUTONOMOUS_HARNESS_OR_MODEL_SWITCH: YES
```

All mandated 00C/00D/Pyat 13/HQ grok/independent source and adoption criteria remain in force. **This amendment repairs discoverability, not science.**
