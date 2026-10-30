# F0R4 — administrator, seed, progress, QF2/F4 and owner-CAS handoff

**Date:** 2026-10-30
**Repository:** `maidiu/rawlsing`
**Branch:** `agent/premain-r4-f0r3-candidate-20-witness-ci-source-repair-20261030`
**Source base:** `299f41e97a43c67be9cc76a79fa49b48f4e12e54`
**Live PR #519 head re-locked:** `59c9a7a4a4fae60d809c1ef545ff4e48906d0dd0`
**Candidate validator:** `2fc1c3c7ae6113d12b70abb655ff123a6ae9c895`
**F0R4 engineering result:** `PASS_SCOPED__20_WITNESS_CANDIDATE_QUALIFIED__OLD_13_CI_NOT_EQUIVALENT`

## 1. Actual current state

| Surface | Observation | Meaning |
|---|---|---|
| PR #519 | open, draft, unmerged; head `59c9a7a4...`; base `299f41e9...`; mergeable true; mergeable_state unstable; submitted review list empty | Candidate patch is not applied. No current-head 20-witness hosted run exists. |
| Receipt CI | run `41082520979`, job `124155062531`, success; stdout 32 events/32 flights and `PASS: 13 mutation witnesses` | Old 13-witness suite; **not** F0R4 20-witness proof. |
| Governed CI | run `41082521136`, 3 failed / 144 passed; same FIABC identity/packaging assertions | Separate original-owner RED; no test weakening. |
| PRE-MAIN protection | `protected=false`; rulesets `0`; required-status endpoint `404 Branch not protected` | Optional CI only; no enforced required check. |
| Frozen seed | blob `4ffe5f95...`; `owner_approval_status=PENDING`; 11 events/11 workers/4 PRs | Prefix-verified but not owner-approved. |
| Live control data | 32 events/32 workers/5 PRs; event blob `60fd8e26...`; flight blob `9306df30...` | Seed prefix equality verified; no owner approval. |
| Sorok progress | MD revision 36 blob `fd6ce005...`; JSON revision 35 blob `c7fb05d8...` | Paired CAS split; rightful Sorok owner must reconcile. |
| QF2 | branch head `a93db6bce4832270cf29727233dbfbc5f0312395`; return `STOP_QF2...NOT_MERGED` | QF2 remains STOP / not launched. |
| F4 | branch head `9fb7caebc266f1e3a8315d87ff446d5db1634cc5`; issued conditional cut | F4 remains STOP / not activated. |
| F0R3I review | `8f85ded9a62ed2ec64386ab91fef4399e84c30a1`; candidate runtime HOLD, authority RED, PR521 REVISE, F4/QF2 STOP | This F0R4 closes the missing independent Python execution, not the independent review. |

## 2. Optional versus required

**Optional today and insufficient:**

- green optional receipt CI on the old 13-witness validator;
- a local candidate script exit 0;
- a branch name, PR title, filled JSON field, or source blob hash;
- a report claiming protection.

**Required and not performed by this worker:**

1. **PR #519 control author/CI:** apply only the exact validator patch `424d8737...` in an owner-authorized branch, not via unauthorized direct PR #519 mutation, and obtain a real hosted run at the exact patched SHA. The existing workflow command already exercises the validator selftest; after the patch it prints the 20-witness result. No workflow YAML change is required for the count.
2. **Distinct source-qualified reviewer:** review the exact patched live SHA, validator source, seed/log/flight/workflow blobs and the 20-witness receipts. This F0R4 executor is the same OpenCode session that authored F0R3; it is not that independent reviewer.
3. **Repository administrator:** protect the authorized PRE-MAIN target with a real required `receipt-contract` check, independent review and no unauthorized bypass/force-push. Read back `protected=true`, exact required context, review rule and bypass list. A green optional run is not enforcement.
4. **Original PRE-MAIN seed owner:** approve the exact 11/11/4 seed provenance. `PENDING` is a hard stop for adoption.
5. **FIABC/Pyat original owners:** classify and repair the three governed failures with exact source/negative evidence; do not weaken or reclassify them.
6. **Sorok rightful owner:** reconcile MD36/JSON35 in one truthful paired CAS revision. Do not edit Pyat reports without the Pyat owner.
7. **Privileged verifier / authorized maintainer:** authenticate the real merged target, owner grant, actual first consumer, current paired progress and repository protection. The offline validator cannot.
8. **QF2/F4 owners:** remain STOP. A validator 20-witness pass and the QF2 STOP return do not satisfy QF2/F4 preconditions.

## 3. Owner CAS sequence after exact patched CI

1. Re-lock PR #519 and the authorized PRE-MAIN target.
2. Apply only the validator patch in an owner-authorized branch; verify result blob `2fc1c3...`.
3. Run the exact 20-witness CI at the patched head. Require 32 events/32 flights, 20 expected rejections, legal nonadopted candidate, and exit 0. Do not accept the old 13-witness run as a substitute.
4. Obtain distinct source-qualified review of the exact patched SHA and this F0R4 receipt.
5. Obtain original seed owner approval; read back required-check/protection; obtain FIABC/Pyat and Sorok dispositions.
6. Only the authorized maintainer may merge through the protected path. Record the actual merged SHA and first real consumer only after they exist; do not pre-embed a future merge hash in a pre-merge ledger.
7. Any head, validator, seed, workflow or target movement after review invalidates the receipt; re-lock and rerun.

Abort/HOLD if: PR #519 or target moves; patch conflicts; 20-witness CI is not run at the exact patched head; seed remains `PENDING`; required check is absent; independent review is missing; Sorok/Pyat remain split; FIABC failures are unclassified; or any attempt is made to treat a branch name, optional CI, or filled field as authority.

## 4. Session handoff and independence limit

- Device: `mainMac`, verified by `scutil --get ComputerName=mainMac` and `LocalHostName=mainMac`; macOS 13.2.1 build 22D68.
- Harness: OpenCode `1.18.34`; model `opencode-go/deepseek-v4.1-flash`; local session variant `max`; provider-side effort `UNVERIFIED`.
- Agent: `build`; agent ID not exposed. Task role: independent I2 bounded control-code engineer/F0R4 executor, not F0R3I reviewer, maintainer, administrator or own reviewer.
- Actual session: title `F0R3 postseed authority bypass repairs`, ID `ses_e72807b76ffeufLz4gsp3C6yVQ`; it was not renamed to the suggested F0R4 title.
- Worktree: `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/f0r4-20w-20261030-r1`.
- Original implementing session: the F0R3 author return `3057b2f5...` was produced from this same OpenCode session on `mainMac`. F0R4 is a fresh source-qualified execution in a new worktree, **not** an independent review of F0R3. `SESSION_LOCATOR.json` records this explicitly.
- New reviewer session: **NOT_ASSIGNED**. A separate source-qualified I2 reviewer is required after this return.

## 5. Nonclaims

This document is not a protection change, merge authorization, owner CAS, source/science grant, independent review or QF2/F4 activation. The worker has not modified PR #519, PR #521, PRE-MAIN/main, QF2/F4, original source, or any other active worker. The only engineering claim is the exact sourcefree 20-witness candidate qualification in `00_RETURN.md` and `02_VALIDATOR_PATCH_AND_CI_RECEIPTS.md`.
