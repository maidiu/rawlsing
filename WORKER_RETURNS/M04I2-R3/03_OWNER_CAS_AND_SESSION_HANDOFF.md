# M04I2 — owner CAS, original-source and session handoff

**Date:** 2026-10-30
**Repository:** `maidiu/rawlsing`
**Review branch:** `review/sorok-r3-m04-claim-ancestry-independent-replay-20261030`
**Sealed commission:** `187fdd11963163dab03c7b061e20067ea1f99134`
**Target original return:** `2309a73bcea1572f6545d5b26027ddc608bee271`
**Candidate reviewed:** patched `claim_provenance.py` blob `5ba929f51870b111ca54ca87fdf97338e4295625`
**Verdict:** `REVISE_EXACT_CANDIDATE__THREE_JOURNALED_RED_CLASSES_CLOSED__RESIDUAL_UNJOURNALED_ADP017_BYPASS__SCIENCE_HOLD__AUTHORITY_HOLD`

## 1. What the owner may and may not infer

- The M04 patch closes the three journaled provenance classes at the frozen-test grain: 51/51 fresh and 587/587 inherited in two cold reconstructions, with the original 10 failures reproduced before the patch.
- The patch does **not** close the unjournaled ADP017 terminal route. A direct unjournaled `SUPERSEDE_EXACT_RECORD` after a journaled revocation restores accessible BELIEF and the patched read boundary accepts `REROUTE` while the journal remains at 2 entries and the state has 3 transitions.
- The nine historical CAN3 failures remain nine separate originals; they are not repaired, reclassified, counted in the 51 or 587, or evidence for the unjournaled route.
- The work is sourcefree TEST_ONLY. No native CAN3/ADP/Pyat science, canonical C9 production compatibility, source grant, owner CAS or canonical merge is established.
- A green test count, a matching source blob, or a filled report does not confer authority.

## 2. Required correction before any acceptance

The original M03/M04 author must add a **positive journal-coverage/terminality check**, not only the existing journaled-ancestry check. At minimum:

1. Every terminal transition consumed for a selected claim must have exactly one matching `ADP017_COMMIT` journal entry.
2. The journal entry's recorded transition ID, `before`/pre-state, recorded post-state set hash and owner-state `after` must match the terminal transition and current owner state.
3. Any `ctx.epistemic_transitions` entry without a matching journal entry must be rejected before consumption.
4. New frozen tests must cover the direct unjournaled `SUPERSEDE_EXACT_RECORD` route and the unjournaled forged-pre-state route; the existing 51 and 587 must remain unchanged.
5. The correction must be re-run in a fresh cold reconstruction and returned at a new exact SHA for a distinct independent review. This reviewer does not author or accept that correction.

The original M04 author's own Limits section already states the unjournaled route is covered only to the extent exercised by the frozen tests. This review confirms that the current 51 do not exercise it and that the read boundary accepts it.

## 3. Original owner and CAN3 issuer gates

| Gate | Required decision | Accountable owner |
|---|---|---|
| M03/M04 sourcefree repair | Accept, revise or reject the exact candidate after the unjournaled route is corrected; no verbal promise | Original M03/M04 author and original M04 reviewer |
| Original CAN3 nine | Keep the nine historical failures as separate original source-cut RED; decide separate court | Original CAN3 issuer/owner |
| Canonical C9/CAN3 compatibility | Do not infer from test-only overlay; require original source/owner and first real consumer evidence | M03/M04/CAN008/ADP016/ADP017 and canonical C9 owners |
| Scientific claim | Keep HOLD; no native actor/world/practice/person claim | Original CAN/ADP/Pyat/SCI05 source owners |
| Owner CAS / fan-in | Hold until corrected exact SHA, distinct review, owner approval and protected path | Authorized PRE-MAIN maintainer and original owner |
| QF2 | Do not start on this review; QF2 preconditions are not met | Incumbent HQ / authorized maintainer |

**Canonical C9 compatibility:** `NOT_ESTABLISHED__SOURCEFREE_TEST_ONLY_OVERLAY`. The M04 target changes only return artifacts; no original CAN3/ADP/C9 source is modified. The patch is compatible with the reconstructed TEST_ONLY M01/M02/M03 harness (51/51 and 587/587), not with canonical C9 production.

## 4. Owner CAS sequence after a corrected candidate

1. Re-lock the original M04 return and the corrected candidate at exact SHAs.
2. Confirm the corrected patch closes the unjournaled direct and forged-pre-state routes with new frozen tests, and still passes 587/587 + 51/51 + the same nine historical failures.
3. Obtain a distinct source-qualified independent review of the corrected exact bytes. The author of this review is not that reviewer.
4. Obtain original M03/M04 author and original M04 reviewer disposition; obtain original CAN3 issuer disposition for the nine; do not collapse those roles.
5. Confirm no canonical source, science, actor or production grant is implied by test success.
6. Only an authorized PRE-MAIN maintainer may perform an owner CAS through the protected path, after required-check and independent-review protections are read back. No merge, force-push or PRE-MAIN mutation is made by this reviewer.
7. Record the actual merged SHA and first real consumer only after they exist. Do not predict a future merge hash inside a pre-merge ledger.

## 5. Session custody and handoff

**Observed session:** OpenCode `1.18.34`; model provider `opencode-go`; model `deepseek-v4.1-flash`; local session variant `max`; device `mainMac` verified by `scutil --get ComputerName=mainMac`; agent name `build`; agent ID not exposed. The actual OpenCode session title is the continued `F0R3 postseed authority bypass repairs` (`ses_e72807b76ffeufLz4gsp3C6yVQ`), not the suggested M04I2 title. The suggested title was not applied; this is a dispatch-compliance note, not a reason to reject the engineering evidence. Full manifest: `WORKER_RETURNS/M04I2-R3/SESSION_LOCATOR.json`.

**Original implementing session:** central registry row `HISTORICAL-SOROK-M04-R1`; exact author SHA `2309a73bcea1572f6545d5b26027ddc608bee271`; device/session `UNKNOWN`; no invented link. The original M04 reviewer is `3a993abcc0a9f6bd3a1bb003d298d293be199ea6`.

**Central registry intake:** the PRE-MAIN owner should append the following row to `CROSS_HQ_CONTROL_ROOM/SESSION_LOCATORS.json` after the return push and fill `return_sha` with the exact remote SHA. This worker did not mutate the central registry.

```json
{
  "registry_id": "M04I2-R3-INDEPENDENT-REPLAY-20261030",
  "revision": 1,
  "commission_id": "M04I2",
  "branch": "review/sorok-r3-m04-claim-ancestry-independent-replay-20261030",
  "sealed_commission_sha": "187fdd11963163dab03c7b061e20067ea1f99134",
  "status": "RETURNED",
  "device": "mainMac",
  "device_evidence": "LOCAL_MACHINE_NAME_VERIFIED: scutil --get ComputerName=mainMac; LocalHostName=mainMac; macOS 13.2.1 build 22D68",
  "harness": "OpenCode",
  "model_provider": "opencode-go",
  "model_id": "deepseek-v4.1-flash",
  "reasoning_effort_requested": "MAX",
  "reasoning_effort_verified": "LOCAL_SESSION_DB_MODEL_VARIANT_MAX__PROVIDER_SIDE_EFFORT_UNVERIFIED",
  "session_name": "F0R3 postseed authority bypass repairs",
  "suggested_session_name": "RAWLSING M04I2 | M04 independent journaled-provenance ancestry | mainMac | OpenCode",
  "session_id": "ses_e72807b76ffeufLz4gsp3C6yVQ",
  "session_url": null,
  "session_locator_type": "APP_SESSION_ID",
  "worktree_path": "/Users/matthewsmith/Desktop/Rawlsing_Worktrees/m04i2-review-20261030-r1",
  "editor_workspace": "/Users/matthewsmith/Desktop/Rawlsing_Worktrees/m04i2-review-20261030-r1",
  "original_implementing_session": "HISTORICAL-SOROK-M04-R1",
  "is_resumption": "NO",
  "parent_session": null,
  "reviewer_session": "ses_e72807b76ffeufLz4gsp3C6yVQ",
  "return_sha": null,
  "return_directory": "WORKER_RETURNS/M04I2-R3",
  "collected_at": "2026-10-30",
  "confirmed_by": "WORKER",
  "machine_claim": "SELF_REPORTED__LOCAL_SCUTIL_COMPUTERNAME_MAINMAC",
  "locator_status": "SESSION_ID_FOUND__ACTUAL_TITLE_CONTINUED_FROM_F0R3__M04I2_RENAME_NOT_CONFIRMED"
}
```

## 6. No self-adoption and nonclaims

This document is not an acceptance, merge authorization, source grant, scientific decision, owner CAS, or QF2 start. The reviewer has not modified the original M04 return, original M03/M04 branches, canonical PRE-MAIN/main, PR514/516/519/521, QF2, native source, or any other active worker. The candidate is held for correction and re-review. The only rendered verdict is the independent engineering/scientific/authority result in `00_INDEPENDENT_M04_VERDICT.md`.
