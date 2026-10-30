# PRE-MAIN R4 / LOC2 — cross-HQ session registry G1–G6 repair

## Identity, custody and model

| Binding | Value |
|---|---|
| Repository | `maidiu/rawlsing` (private) |
| Repair branch | `agent/premain-r4-pr521-session-custody-six-negative-repair-20261030` |
| PRE-MAIN source anchor | `299f41e97a43c67be9cc76a79fa49b48f4e12e54` |
| PR521 source repaired | `f246eaddbeeb86677c3ae67a075390501e233f38` |
| Worktree | `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/loc2-r4-session-custody` |
| Host | macOS x86_64; `scutil --get ComputerName` = `mainMac`; hostname `MacBook-Pro.lan` |
| Harness / model | OpenCode; `opencode-go/deepseek-v4.1-flash`; session-store variant `max` |
| Session | title `BP4/C12 chain authenticity & writer compatibility`; id `ses_e727fe553ffechTREKfuiLPjDV`; agent/profile `build`; no model or harness switch |
| User-selected pair | Local OpenCode / DeepSeek V4.1-Flash MAX, explicitly selected by the user. The session store records variant `max`; the provider UI selector was not independently inspected. |
| Write scope | Candidate PR521 repair files plus `WORKER_RETURNS/LOC2-R4/**`; no canonical registry row write, PRE-MAIN/Pyat/Sorok mutation or draft-PR merge |

**Branch custody:** the branch point is the PR521 source `f246eadd…`; `299f41e9…` is its PRE-MAIN merge-base and remains untouched. The repair does not move, merge or adopt PRE-MAIN or PR521.

The original six witness tests and all six reviewer bypasses were reproduced on the exact PR521 source. The original verifier passes its six tests while accepting all six G1–G6 counterexamples. The repaired verifier rejects all six while retaining the original six and accepting legitimate appended revisions, including a faithful QF2 representation with no source authority.

## FINDING

1. **G1 — historical rewriting was undetected.** The original `check()` is stateless. It validates a single snapshot; it cannot know that a prior row was rewritten, deleted or reordered. The repair adds an exact ordered-prefix check against a supplied previous registry snapshot or `--baseline-ref`. Historical rows must remain byte-identical; new revisions append.
2. **G2 — a fabricated observed title was accepted.** The original only rejected `session_name == suggested_session_name` with `confirmed_by=UNVERIFIED`. A worker could set any fabricated `session_name` with `confirmed_by=WORKER`, any suggested title and no title evidence. The repair adds `session_name_evidence`, requires it for every observed title, rejects `SUGGESTED`/`UNKNOWN` as observed, and cross-checks title, locator type and locator status.
3. **G3 — an invalid locator type was accepted.** `session_locator_type` was not validated at all. The repair uses a strict enum and requires the field matching the type: title for `APP_TITLE`, session id for `APP_SESSION_ID`, URL for `APP_URL`, worktree/note for `WORKTREE_AND_OPERATOR_NOTE`, and no observed fields for `UNKNOWN`.
4. **G4 — a duplicated registry ID was accepted.** The original only checked `(commission_id, revision)`. The repair adds registry-ID uniqueness while retaining revision uniqueness and contiguity.
5. **G5 — a bogus confirmation authority was accepted.** `confirmed_by` was never validated. The repair requires the exact enum `USER | WORKER | REVIEWER | UNVERIFIED`; user confirmation needs direct evidence; reviewer confirmation needs reviewer readback; unverified rows cannot claim a machine or a returned status; workers cannot claim higher authority. Locator rows also cannot assert `source_authority`, `adoption`, `native_authority` or a source/merge grant.
6. **G6 — a forged valid-format SHA was accepted.** The original accepted any 40-hex `return_sha`. The repair adds local Git readback: a SHA must exist as a commit; with `--require-sha` a forged or missing SHA is rejected; with `--require-sha-branch` the commit must be reachable from the declared branch. Where no repository is available the verifier says HOLD, not PASS.

The repair also verifies the QF2 locator's actual `oldMac / Codex / Default / Review QF2 Sorok fan-in` session with `APP_SESSION_ID` `01a18e10-6391-7a52-8950-dec3073e1800`, while explicitly retaining `source_authority=false` and `adoption=false`.

## INTERPRETATION

The PR521 verifier was a useful schema check, not an append-only custody gate. Its six green tests and its six structural counterexamples can coexist because the tests do not exercise historical baselines, strict locator enums, title evidence, unique registry IDs, confirmer authority or real Git SHA readback. The repair closes those sourcefree consistency gaps. It still cannot authenticate a Mac name, a UI title, a user or a source owner; those remain operator/owner attestations. A valid locator is discoverability and provenance hygiene, not source authority.

## HQ ACTION

1. PR521 maintainer/owner reviews and adopts the exact patch at `f246eadd…` or the equivalent repair-branch blobs. Do not treat this return as owner adoption.
2. Cross-HQ registry owner runs the repaired verifier with a previous snapshot/baseline and appends the QF2 revision through its own authorized CAS; the worker does not write the canonical registry.
3. PRE-MAIN owner wires the repaired `--selftest`, the 21-test G1–G6 unittest and the baseline check as a required CI context; branch protection and original-owner CAS remain separate.
4. Operator confirms the actual `oldMac`/`mainMac` labels and app-visible session titles for rows still marked `SESSION_NOT_FOUND__REQUIRES_OPERATOR_CONFIRMATION`; preserve `UNKNOWN` where the evidence is genuinely absent.
5. Distinct control reviewer replays the exact repaired blobs and the before/after proof; original PRE-MAIN/Pyat/Sorok owners retain their own boundaries.

## OWNER

PR521 author/maintainer, Cross-HQ registry owner, original PRE-MAIN owner, Pyat/Sorok HQ grok owners, and the distinct independent control reviewer. The worker is not the reviewer and does not self-adopt.

## Three courts

| Court | Verdict | Basis |
|---|---|---|
| ENGINEERING | `PASS_SCOPED_SOURCEFREE_G1_G6_AND_APPEND_ONLY` | Original six PASS; six original bypasses reproduced; patched six rejected; 21/21 G1–G6 and valid-case tests pass; strict baseline + SHA + branch readback passes; QF2 representation accepted without authority |
| SCIENCE | `HOLD__NO_SOURCE_OR_PERSON_AUTHORITY` | This is registry/control integrity only. No native source, actor, world, person, Rule A/T, C11/C12 or scientific issuance. |
| AUTHORITY | `HOLD__NO_OWNER_CAS_OR_MERGE` | PR521 is draft/unmerged; no protected required check, owner CAS, source grant or first consumer is established. Repo write is a candidate, not adoption. |

## Exact before/after

| Test | Before (PR521 `f246eadd`) | After (repair) |
|---|---|---|
| Original verifier `--selftest` | `PASS 18 locators` + `PASS 6 adversarial locator integrity witnesses`, exit 0 | same six still pass, exit 0 |
| G1 historical rewrite | original check `[]` (bypass) | `row0:HISTORICAL_ROW_REWRITTEN` |
| G2 fabricated observed title | original check `[]` (bypass) | `SESSION_NAME_EVIDENCE_MISSING`, `NOT_FOUND_WITH_OBSERVED_FIELDS` |
| G3 invalid locator type | original check `[]` (bypass) | `LOCATOR_TYPE` |
| G4 duplicate registry ID | original check `[]` (bypass) | `DUPLICATE_REGISTRY_ID` |
| G5 bogus confirmation authority | original check `[]` (bypass) | `CONFIRMED_BY` |
| G6 forged valid-format SHA | original check `[]` (bypass) | `SHA_NOT_LOCAL` under strict local readback |
| G1 legitimate append | n/a | legal revision 2 and new commission revision 1 accepted, prefix preserved |
| QF2 representation | n/a | accepted with `source_authority=false`, `adoption=false` |
| New G1–G6 unittest | not present | `Ran 21 tests ... OK` |
| Strict canonical run | n/a | `PASS 18 locators` + `PASS append-only baseline prefix preserved`, exit 0 |

## First consumer and native production

First sourcefree consumer is the repaired verifier itself plus `test_session_locator_integrity_r2.py`; first control consumer is the Cross-HQ registry owner’s intake command. **No native production consumer, source authority, owner CAS or merge is proved.**

## DONE / REMAINING / CRITICAL BLOCKERS / LARGEST PRODUCTIVE MOVE / FLIGHT / DELTA

- **DONE:** reproduced original six; reproduced all six G1–G6 bypasses; implemented append-only baseline, strict locator/confirmation enums, title/evidence consistency, unique registry IDs, SHA readback, authority refusal; added 21 tests; verified QF2 representation; preserved historical UNKNOWN; ran strict canonical baseline/SHA/branch check.
- **REMAINING:** PR521 owner review/adoption; canonical registry append by Cross-HQ owner; required-check/branch protection; operator confirmation of unknown historical sessions; distinct reviewer; no source/production grant.
- **CRITICAL BLOCKERS:** no owner CAS or protected required check; PR521 draft; most historical rows still lack app-visible titles; this repair is offline self-attestation consistency, not machine or source authentication.
- **LARGEST PRODUCTIVE MOVE:** PR521 maintainer and Cross-HQ owner review the exact repaired blobs, then run the baseline/SHA command on the canonical registry and append QF2 revision 2 through authorized CAS.
- **FLIGHT:** sourcefree local Git/Python only; no PRE-MAIN/Pyat/Sorok mutation; no automatic draft-PR merge.
- **DELTA:** the six green witnesses can no longer coexist with G1–G6 false attribution in this candidate; historical rows are now append-only, locator/confirmer enums and title evidence are enforced, and a 40-hex SHA is no longer accepted without Git readback.

## STOP / HOLD

`PASS_SCOPED_SOURCEFREE__OWNER_CAS_AND_REQUIRED_CHECK_HELD__NO_MERGE`. The canonical registry was not modified by this worker. Missing or unavailable evidence stays `UNKNOWN`/HOLD, never invented.

## Artifacts

- `00_RETURN.md`
- `01_G1_G6_NEGATIVES_AND_VALID_CASES.json`
- `02_SESSION_REGISTRY_PATCH_AND_TESTS.md`
- `03_CROSS_HQ_OWNER_REVIEW_HANDOFF.md`
- `SESSION_LOCATOR.json`

Final remote SHA is reported externally after the ordinary push; a commit cannot contain its own final SHA.
