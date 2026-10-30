# PREMAIN R4 F0R4 — current-head twenty-witness validator qualification

**Overall:** `PASS_SCOPED__TWENTY_WITNESS_CANDIDATE_QUALIFIED__OLD_13_CI_NOT_EQUIVALENT__SCIENTIFIC_HOLD__AUTHORITY_RED`.
The F0R3 candidate validator (`2fc1c3c7...`) was independently executed against the actual frozen control data: the sealed `342164...` 19/19 cut and the live PR #519 `59c9a7a4...` 32/32 cut. It rejects all 20 expected mutation witnesses and accepts only the legitimate nonadopted `OWNER_ADOPTION_CANDIDATE`. The old PR #519 CI remains a 13-witness success and is not promoted to a 20-witness proof. This is a sourcefree engineering qualification, not an independent review, adoption, science grant or authority CAS.

**Repository:** `maidiu/rawlsing` (PRIVATE)
**Branch:** `agent/premain-r4-f0r3-candidate-20-witness-ci-source-repair-20261030`
**Source base:** `299f41e97a43c67be9cc76a79fa49b48f4e12e54`
**Live PR #519 head re-locked:** `59c9a7a4a4fae60d809c1ef545ff4e48906d0dd0`
**F0R3 author return:** `3057b2f5b87f04ff1737d88356edfe3568e1745f`
**F0R3I independent return:** `8f85ded9a62ed2ec64386ab91fef4399e84c30a1`
**Original F0 return:** `e5089b7da29d3c290ad1447f7b7a45cc81f0eb6e`
**QF2 STOP return:** `a93db6bce4832270cf29727233dbfbc5f0312395`

**Session:** `mainMac` verified by `scutil`; OpenCode `1.18.34`; model `opencode-go/deepseek-v4.1-flash`; local session variant `max`; actual continued session title `F0R3 postseed authority bypass repairs` (`ses_e72807b76ffeufLz4gsp3C6yVQ`); agent `build`. This is the same OpenCode session that authored F0R3, now executing F0R4 in a new isolated worktree. It is **not** an independent review of F0R3; a new source-qualified I2 reviewer remains required. Full manifest: `SESSION_LOCATOR.json`.

## Exact source and candidate identity

| Surface | Git blob |
|---|---|
| PR519 original validator at sealed and live cuts | `6fa0ce132e68f1fea7d67321129a2af2627a5d94` |
| F0R3 candidate validator | `2fc1c3c7ae6113d12b70abb655ff123a6ae9c895` |
| F0R3 candidate patch | `424d87370b0e5fdfad13705335558eff37be9257` |
| Frozen initial seed | `4ffe5f95b84505431a928f7ef6d0e7b5931f63d8` |
| Sealed event log / flight (`342164...`) | `2b899397bdac9c2e92d4db295278743e2499eca9` / `7c20af660ce6c323e99f5dd038abf4c4ac3b5891` |
| Live current event log / flight (`59c9a7a4...`) | `60fd8e26b3d8c4bd66f27900b82c9359cf4ad652` / `9306df304a8f12029c8daacb2eb97c9fcb58df56` |
| Receipt workflow | `ce1ef40b5f2568c52a44d1ddc01a98647f3bf322` |

The patch applies cleanly to the exact `6fa0ce...` source and produces exactly `2fc1c3...`; `git apply --check` and `git apply` both exit 0 in the isolated check tree. The seed, event log, flight register and workflow are unchanged by the candidate.

## What was executed

**Candidate validator, current 32/32 source:**

```text
python3 verify_branch_fanin.py --selftest --baseline-ref 299f41e97a43c67be9cc76a79fa49b48f4e12e54
# exit 0
# PASS sourcefree record integrity: 32 events and 32 flights; NO ADOPTION ALLOWED
# PASS: 20 mutation witnesses rejected + valid nonadopted owner-candidate stage
```

**Candidate validator, sealed 19/19 source:** same command in the sealed snapshot, exit 0; `19 events and 19 flights`; 20 witnesses; legal nonadopted candidate.

**Independent twenty-witness harness** (does not call the validator's own selftest):

| Data cut | Candidate result | Original `6fa0ce...` result |
|---|---|---|
| Current `59c9a7a4...` 32/32 | 20/20 expected rejections; legal candidate accepted; exit 0 | 13/13 original expected rejections; `N1,N2,N3,N4,N6,N7` admitted; `N5` rejected only by the old flight-SHA mismatch, not by the new append check; exit 0 report-only |
| Sealed `342164...` 19/19 | 20/20 expected rejections; legal candidate accepted; exit 0 | same old-13 behavior and six admissions |

The original validator never emits `APPEND_REUSES_PRIOR_IMMUTABLE_SHA`; its `N5` rejection is an incidental `FLIGHT_LOG_EXACT_SOURCE_MISMATCH`. The candidate rejects `N5` with the intended append-reuse error. The old live CI success (`run 41082520979`, job `124155062531`) is therefore **not** evidence of N1–N7 coverage.

**Candidate CI source:** `WORKER_RETURNS/F0R4-R4/candidate/ci/run_f0r4_ci.sh` runs both snapshots and both harness invocations, checks `PASS: 20 mutation witnesses` and `"all_expected": true`, and exits 0. The existing receipt workflow already invokes the validator's selftest; when the exact validator patch is applied, it exercises the 20-witness suite. No workflow YAML change is required for the count, but the owner must apply the validator patch and obtain a real CI run at the exact patched head.

**Seed/current prefix:** direct comparison confirms the frozen seed's first 11 events, 11 workers and 4 PRs equal the first rows of the live 32/32/5 control data. This is byte-level prefix equality of parsed records, not owner approval. `owner_approval_status` remains `PENDING`.

## FINDING → INTERPRETATION → ACTION → OWNER

| FINDING | INTERPRETATION | ACTION | OWNER |
|---|---|---|---|
| Candidate rejects all 20 W1–W5, B1–B8, N1–N7 and accepts only the legal nonadopted candidate on the current 32/32 cut; sealed 19/19 also passes 20/20. | The 20-witness candidate is source-qualified and independently executed; the old 13-case CI is weaker and cannot be inherited. | Preserve exact results; obtain distinct independent review of the patched live SHA; do not merge from this return. | PR519 control author, new source-qualified reviewer, authorized maintainer. |
| `N1,N2,N3,N4,N6,N7` are admitted by the old `6fa0ce...` validator on the same 32/32 data; `N5` is rejected only incidentally by an old flight mismatch. | The live green receipt job does not cover the new post-seed custody families. | Apply the exact validator patch in an owner-authorized branch and run the 20-witness CI at the exact patched head. | PR519 author/CI and repository administrator. |
| Seed is frozen at `4ffe5f...`, 11/11/4, `PENDING`; live data is 32/32/5 with exact seed prefix. | Prefix equality is not owner approval or protected historical enforcement. | Original seed owner must approve provenance; administrator must provide protected required-check readback. | Original PRE-MAIN seed owner + repository administrator. |
| PRE-MAIN remains `protected=false`, rulesets `0`, required-check endpoint `404`; receipt workflow is optional. | A green optional run does not enforce fan-in. | Install and read back the exact required `receipt-contract` check, independent review and no-bypass rules. | Repository administrator + incumbent PRE-MAIN maintainer. |
| Live governed CI remains 3 failed / 144 passed; Sorok MD36 vs JSON35; QF2 STOP at `a93db6...`; F4 at `9fb7...` STOP. | These are separate owner/authority blockers, not repaired by the validator candidate. | Keep visible; no test weakening; original owners classify/reconcile; no F4/QF2 activation. | FIABC/Pyat, Sorok, QF2/F4 owners, incumbent HQ. |

## Three courts

- **ENGINEERING: `PASS_SCOPED` for the exact 20-witness candidate source and executed current/sealed data.** The candidate is independently runnable, patch-applies cleanly, and passes 20/20 plus legal nonadoption. `HOLD` for adoption/independent review and for claiming the old live CI is 20-witness CI.
- **SCIENTIFIC: `HOLD`.** Sourcefree control code and synthetic fixtures only; no native CAN/ADP/SCI05/Pyat actor, world, acquisition, person or production consumer.
- **AUTHORITY: `RED/HOLD`.** Seed owner approval `PENDING`, no protected required check, no independent review of the exact patched live SHA, no owner CAS and no first real consumer. Optional CI and a branch name grant nothing.

## DONE / REMAINING / CRITICAL BLOCKERS / LARGEST PRODUCTIVE MOVE / FLIGHT / DELTA

- **DONE:** exact source/seed/log/flight/workflow re-lock; patch apply check; 20-witness candidate execution at sealed 19/19 and live 32/32; separate original 13 vs new 7 demonstration; legal nonadopted candidate accepted; seed prefix check; candidate CI script exit 0; current PR/CI/protection/progress/QF2/F4 state read.
- **REMAINING:** distinct source-qualified review of the exact patched live SHA; owner-authorized patch application and real required CI run; administrator protection readback; original seed owner approval; FIABC/Pyat classification; Sorok paired progress; owner CAS/first consumer; no F4/QF2 activation.
- **CRITICAL BLOCKERS:** old 13-case CI is not 20-witness proof; seed `PENDING`; target unprotected; no required check; no independent review; governed 3 failures; Sorok MD36/JSON35; QF2/F4 STOP.
- **LARGEST PRODUCTIVE MOVE:** owner-authorized application of the exact validator patch and a real required 20-witness CI run at the patched live head, followed by distinct source review and administrator protection readback.
- **FLIGHT:** no PR #519, PR #521, PRE-MAIN/main, QF2/F4, original source or other active worker was modified. No model/harness switch. Only this own return tree and isolated candidate/evidence were written.
- **DELTA:** the F0R3 candidate's 20 witnesses are no longer only author-reported; they are independently executed at the exact current 32/32 and sealed 19/19 cuts, while the old 13-witness CI is explicitly separated and not inherited.

## No self-approval

This F0R4 execution is the same OpenCode session that authored the F0R3 candidate. It is a fresh source-qualified execution, not an independent review of the candidate. A distinct source-qualified I2 reviewer must review the exact patched live SHA and this return. No merge, protection change, PRE-MAIN write, F4/QF2 activation or self-adoption occurred.

**Push readback:** the exact immutable remote SHA is reported in the final HQ message after `git push` and `git ls-remote`; it is not embedded in its own committed files. The worktree was clean at commit time.
