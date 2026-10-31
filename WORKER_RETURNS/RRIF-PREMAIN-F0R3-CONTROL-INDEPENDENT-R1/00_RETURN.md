# RRIF F0R3 — fresh independent PRE-MAIN fan-in control readiness review

**Verdict:** `RRIF_F0R3_CANDIDATE_ENGINEERING_ACCEPT_SCOPED__CURRENTNESS_HOLD__ENFORCEMENT_NOT_INSTALLED__SCIENCE_AUTHORITY_HOLD__NO_ADOPTION`

**Dispatch custody:** issue `#574` authorized SHA `696fbf97cc1f9bab16daf2e5a9f6a6800b449130`; exclusive worktree `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/rrif-574-exclusive-20261031`; local session branch `rrif-session-574-20261031`; HEAD and live remote branch both matched the dispatch SHA before work. The earlier pre-amendment provisional review was preserved and copied here; nothing was reset.

## FINDING

PR #519 live head is `59c9a7a4a4fae60d809c1ef545ff4e48906d0dd0`, matching the F0R3 cut. The F0R3 candidate validator (blob `2fc1c3c7ae6113d12b70abb655ff123a6ae9c895`, SHA-256 `ab26b3a014a16d5ec0f1c3edb5cfbbe284440b9a7a6580e4bd3631b971af1abb`) applies cleanly to the unchanged PR #519 validator `6fa0ce132e68f1fea7d67321129a2af2627a5d94` and passes independently on the actual current 32-event / 32-flight corpus:

- original validator: **13 witnesses**, and it admits N1–N4, N6, N7;
- candidate validator: **20 witnesses**, and rejects N1–N7;
- legal nonadopted `OWNER_ADOPTION_CANDIDATE` remains accepted by both with `adoption=false`;
- the old 13-witness pass is not transferred to the new bytes; the candidate is exercised against the exact current data.

The sourcefree engineering repair is real. It is not an installed control gate.

## Currentness and control findings

- **PR #519 is stale relative to current PRE-MAIN.** Its merge ref is `7abc24f2ec3884702d0bc41248ae13d7a367a6ae`, a merge of `59c9a7a4` into `299f41e97a43c67be9cc76a79fa49b48f4e12e54`. Current PRE-MAIN is `8e44ca9c751049d65e6def47600b5c073ee04b29` and **does not contain `CROSS_HQ_CONTROL_ROOM/BRANCH_FANIN` at all**. The reviewed PR must be rebased/merge-forwarded and re-locked to the current base before any fan-in.
- **Enforcement is not installed.** Live branch metadata reports `protected=false`; repository rulesets are `[]`; the required-status-check endpoint returns 403 to this credential. The receipt workflow is optional CI. A green PR run cannot block direct writes or unreviewed merge.
- **Seed is not owner-approved.** `00_FROZEN_INITIAL_SEED.json` is `4ffe5f95b84505431a928f7ef6d0e7b5931f63d8`, 11 events / 11 workers / 4 PRs, `owner_approval_status=PENDING`; no owner approval receipt or signature exists in PR #519.
- **No privileged verifier exists.** The offline validator cannot authenticate reviewer identity, source-owner grant, merged target, real first consumer, or paired progress. Those remain separate hard gates.
- **Sorok progress is still split.** Current PRE-MAIN Sorok MD opens at revision 36; its JSON parses revision 35. That is a separate rightful-owner CAS defect, not repaired here.
- **FIABC governed run 144/3 is separate.** F0R3 observed run 41082521136 with 3 identity/packaging failures. This review did not rerun it (Actions API 403); it remains a separate FIABC/Pyat owner classification, not a receipt-contract result.
- **F4 is divergent.** `9fb7caebc266f1e3a8315d87ff446d5db1634cc5` is not an ancestor of current PRE-MAIN and remains HELD. F4 must not proceed as a parallel control law; use the reviewed PR #519 head or abandon the old branch after an owner decision.
- **Current PR #519 CI green is old-suite green.** The run reported by F0R3 exercised 13 witnesses; it does not exercise N1–N4/N6/N7. The candidate's 20 witnesses were executed locally against the exact current data, not via a candidate PR CI run (workflow has no dispatch trigger).

## INTERPRETATION

The F0R3 patch closes the exact post-seed custody bypass classes at sourcefree test grain. It does not create repository protection, owner approval, independent review, reviewer identity, source grants, merged target proof, paired progress, or first-consumer acceptance.

A sourcefree validator is a guardrail. The current fan-in gate is not admissible until the administrator installs and reads back the required check and the rightful PRE-MAIN owner performs a protected CAS on an exact re-locked head.

## ACTION / OWNER

1. **PR #519 author:** rebase/merge-forward the reviewed control change onto current PRE-MAIN `8e44ca9c`, preserve the 32-event/32-flight corpus and exact candidate validator, and re-lock the new head.
2. **Independent reviewer:** hostile-review the exact patched validator and the re-locked PR head. This author cannot review or accept its own work; the prior F0/F0R2 authors cannot self-accept.
3. **Repository administrator:** install and read back a ruleset/branch protection requiring the exact `PRE-MAIN Branch Fan-in Receipt Integrity (sourcefree)` / `receipt-contract` check, independent approval, and no unauthorized bypass.
4. **Rightful PRE-MAIN owner:** approve the exact initial seed provenance (currently PENDING) and the re-locked head; then perform the protected merge/CAS.
5. **Authorized maintainer/owner:** authorize a separate privileged verifier for signed source/science grants, merged commit, real importing first consumer, and paired CURRENT_PROGRESS MD+JSON.
6. **Sorok incumbent:** reconcile MD36/JSON35 in one truthful paired revision.
7. **FIABC/Pyat owner:** classify the 144/3 failures against base and changed source; do not waive tests.
8. **HQ:** retire or re-cut F4; do not run a second competing control law.

## THREE COURTS

- **ENGINEERING:** `ACCEPT_SCOPED` for the F0R3 candidate at sourcefree validator/test grain. `HOLD` for currentness, patch re-lock, CI installation and protected merge.
- **SCIENTIFIC:** `HOLD` — no original CAN/ADP/SCI05/Pyat source, native person, or scientific issuer decision.
- **AUTHORITY:** `RED` — no owner seed approval, independent review acceptance, required check, privileged verifier, paired progress, or actual CAS. The candidate is not adopted.

## DONE / REMAINING / BLOCKERS / LARGEST MOVE / FLIGHT / DELTA

- **DONE:** live PR #519 head and merge base read; F0R3 patch applied and checked; current 32/32 data replayed; original 13 vs candidate 20 witnesses; N1–N7 reproduced; legal nonadopted candidate accepted; admin/seed/progress/F4 currentness read back.
- **REMAINING:** PR #519 rebase/merge-forward and re-lock; exact candidate review; owner seed approval; admin required-check install/readback; privileged verifier; Sorok pair; FIABC classification; F4 disposition; protected owner CAS.
- **BLOCKERS:** PR #519 merge ref is still based on `299f41e9`, not current `8e44ca9c`; current PRE-MAIN lacks the control files; `protected=false`; rulesets `[]`; seed `PENDING`; no privileged verifier; MD36/JSON35.
- **LARGEST MOVE:** one authorized maintainer transaction: re-lock the exact reviewed PR #519 head on current PRE-MAIN, install/read back the required check and independent approval, obtain seed approval and the privileged verifier, then protected CAS.
- **FLIGHT:** fresh independent review branch only; no PR #519, PRE-MAIN, F4, progress pair, source owner or active worker was modified.
- **DELTA:** the current head's old-suite green is distinguished from N1–N7; the candidate repair is independently reproduced; currentness and enforcement remain hard HOLDs.

No self-adoption. No model or harness switch. Exact return SHA is reported after push.
