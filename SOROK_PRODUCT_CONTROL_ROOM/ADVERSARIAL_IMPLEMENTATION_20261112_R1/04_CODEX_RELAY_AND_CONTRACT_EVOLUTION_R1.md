# CODEX — Standing adaptive A/B relay and contract evolution R1

**Classification:** proposed operational instructions for the USER'S ALREADY EXISTING local Codex→OpenCode controller. These instructions do **not** assert access to, deployment of, or redesign of that controller. If controller reality contradicts a proposed step, inspect real interfaces and report the exact limitation. Do not fabricate host commands, agent identities, session memory, leases or provider availability.

## 0. Irrevocable operating distinction

**Destination:** the complete existing SOROK sourcefree CG-B–G/J1–J4 goal and original PW-01..14 / CAN/ADP/D002 obligations are binding. Neither A, B nor Codex may quietly narrow or discard them. Scientific/actor/source/human authority remains governed by original competent owners.

**Route:** the 27 implementation packet ABIs, source candidates, implementation tactics, sequencing and cost estimates are versionable hypotheses. Revise the route when actual implementation evidence warrants it.

**Agent identity:** the user's exact unabridged four-role source is in `01_USER_ORIGINAL_DUEL_PERSONAS_UNABRIDGED.md`. Inject the full applicable section plus the governing opening principle to each A/B dispatch. Do not replace it with a “friendly reviewer” summary. Aggressive rivalry is permitted; deceptive overclaiming is not. They are two savage adversaries whose pride attaches to accurate construction and willingness to concede earned victories.

## 1. Use the controller we already have

At startup, Codex discovers and records these EXISTING controller endpoints before dispatch:
- available dispatcher and exact command/API; OpenCode account/profile and quota; model+variant exact strings;
- self reasoning-effort switch capability and limits; allowed automatic adjustment modes;
- the notification/wake subscription; which event IDs, sessions and commit SHAs wake Codex, how duplicate deliveries are de-duplicated;
- session resume semantics, conversation storage, model-context truncation and cold restart;
- local repo/worktree and exclusive writer lease registry, collision detection and TTL/recovery;
- test/CI observation, budget/cost counter, GitHub branch/push/PR privileges and protected merge prohibition.

If a required operation is unavailable, do not improvise another network/agent framework: return one exact missing controller capability and use available support until remedied. A GitHub issue, branch or PR alone never instantiates an OpenCode agent.

## 2. Persistent pair identity and execution custody

Each pair has exactly two distinct competing principals, A and B. Persistent sessions are best-effort; **stored state is authoritative for identity**, not simulated model memory. Do not reuse the same session for both adversaries or contaminate B's independent reconstruction with A's self-interpretation before the original contract/source pass.

Store/maintain at least:
- pair_id, role (A/B), original persona file blob SHA and applicable section, model and MAX variant actually verified, session ID and last acknowledged controller event ID;
- immutable current task contract ID+version+SHA; active branch/worktree writer lease; startup SHA and input file ownership;
- opponent's frozen exact artifact HEAD, source/code cut and provenance; reviewed original governing obligation refs and later consumer;
- agent's own validated victories, refuted attacks, conceded opponent findings, corrected defects, unproved cuts and strongest self-disclosed weakness;
- test commands, first-consumer positive/negative/restore, CI job exact commit, source/rights/science grade and actual cost/latency;
- not-yet-released source/owner changes and affected packets.

A/B *may* see opponent code and complete handoff, but B must first spend a bounded independent source/contract reconstruction step before trusting the predecessor's narrative. A resumes against B's source, not B's rhetoric. Every new round inherits original task obligations plus all previously established genuine improvements.

## 3. Event-driven supervisor state machine

`PREPARED → LEASE_CHECKED → READY → A_RUNNING → A_RETURNED → B_RUNNING → B_RETURNED → A_COUNTER → [B_COUNTER...] → CANDIDATE → INDEPENDENT_RECEIVING → ACCEPT_SCOPED | REVISE_EXACT_DEFECT | HOLD_EXTERNAL → NEXT_DEPENDENCY_READY`

**Never claim a state transition without its actual receipt.** Do not persist a “RUNNING” row unless a host/session launch succeeded. Never claim “ACCEPT” on A/B self-attestation or authorship CI.

For each notification:
1. Deduplicate by controller event ID, agent session, task contract SHA and actual commit SHA. Recheck immutable artifact and test summaries.
2. Compare changed source paths and public/hidden ABI fields to task contract; validate true consumer effects, positive+negative+restore and preserved original obligations. An agent's nine-part handoff is evidence testimony, not automatic verdict.
3. Record no-op/failed/invalid claims faithfully. Reward exposed self-defects and corrective code, not ability to manufacture additional tests.
4. Compute impacted downstream edges (see §4). Revise queued work at new contract versions, never the running immutable contract.
5. Decide continue duel / one bounded correction / independent receiving / next ready packet / scoped HOLD / escalate architectural question.
6. Dispatch via existing controller with verified lease and session/prompt; store its returned run/notification IDs and cost. Do not poll repeatedly when wake events already exist.

**Agent turn payload:** exact persona *full section*; task ID + original programme contract link and frozen version; current executable source/owner readset; opponent frozen artifact HEAD/handoff and concessions; expected actual consumer and concise P/N/restore falsifiers; constraints/grade and allowed write paths; report target and no-drop inherited obligations. Never send persona alone without the real implementation objective.

## 4. Live dependency/ABI impact maintenance — Codex's highest-leverage task

Every substantive author/B commit receives a machine-readable impact record:

```json
{
  "event_id": "controller-issued",
  "task_id": "B02",
  "running_contract_sha": "40hex-current-verified",
  "implementation_sha": "40hex-actual",
  "changed_owner_symbols": [],
  "abi_class": "LOCAL | COMPATIBLE_ADDITIVE | BREAKING_INTERFACE | SOURCE_OR_AUTHORITY | NEW_CONSUMER | SCIENTIFIC_HOLD",
  "affected_task_ids": [],
  "new_actual_first_reader": "exact source path:function or NOT_PROVEN",
  "effect_on_original_obligation": "PRESERVED | EXPANDED | REGRESSION | UNKNOWN",
  "evidence": {"source": [], "test": [], "negative": [], "cold": []},
  "queued_contract_changes": [],
  "active_contract_decision": "UNAFFECTED | FINISH_THEN_RECONCILE | PAUSE_AT_CHECKPOINT | ESCALATE",
  "cost_record": {"tokens": null, "wall_s": null, "usd": null},
  "authority": {"engineering": "SOURCEFREE_CANDIDATE", "science": "HELD", "rights": "HELD"}
}
```

**Change decision procedure:**
- `LOCAL`: no ABI change; keep descendants unchanged; record actual tests.
- `COMPATIBLE_ADDITIVE`: update only queued dependents that would benefit; accept active agent input unchanged; document interface migration as optional until proven.
- `BREAKING_INTERFACE`: trace all directly and transitively dependent tasks and exact first-consumer symbols. Freeze affected queued contracts, author vN+1 with source/evidence justification and minimal compatibility adapter. For active tasks preserve vN and decide `FINISH_THEN_RECONCILE` vs checkpoint pause based on demonstrated wasted-work risk; no invisible prompt rewrite. Never modify another pair's branch.
- `SOURCE_OR_AUTHORITY`: verify genuine competent owner, external rights and protected source status. Escalate any new issuer/owner or nonuser-approved rights grant; sourcefree work may continue on other edges.
- `NEW_CONSUMER`: validate before moving readiness gates; a mock consumer is not a source-native issued reader.
- `SCIENTIFIC_HOLD`: carry exact held operation while other qualified sourcefree tasks proceed. Do not redefine unknown as evaluated no-change.
- Owner/scheduler replacement is always HIGH reasoning with explicit architectural contradiction evidence before downstream change.

Create an impact-ledger entry for *every* changed ABI assumption even when implementation is not yet accepted. Never roll a speculative candidate into dependent accepted state; distinguish **consumable provisional fixture** from **independently received interface**.

## 5. Challenge severity and stopping

**Productive attacks:** actual owner/reader mismatch, source/clock failure, rights leakage, state/transaction corruption, historical functional loss, omitted actual consumer, false native claim, simpler existing code with verified behavioral equivalence. Agent finding must identify and, when authorized, attempt repair.

**Not automatically productive:** additional synthetic probes of a feature already adequate, elaborate report rephrasing, making unit tests stricter by inventing a new scientific requirement, a PR with no changed product behavior, or exposing the same defect again.

Default maximum A→B→A turn sequence **as a resource budgeting default only**. More turns require an unresolved material and feasible defect, not a fixed three-round ceremony. If a serious systemic fault is found, continue until corrected; if repeated attacks are trivial, stop immediately and move to new productive tasks.

**Agent competition score:**
1. New original functionality actually available to its downstream consumer.
2. Independently reproduced real defect fixed, without dropping valid prior functions.
3. Whole task original obligations met at honest sourcefree grade.
4. Fewer unnecessary owners/schedulers/representations and measured resource cost.
5. Correct concessions and self-disclosed weakness with attempted repair.

No numeric scoreboard that causes invented findings; these are ordering preferences. No credit for profanity alone or tests without causal discrimination.

## 6. Cost/intelligence discipline

Use DeepSeek V4.1-Flash **1017 MAX** for A and B when the user's OpenCode account exposes that actual model/variant; verify spelling/ID and session origin. No guessed provider string. Record actual token/cost receipt when available, else `UNKNOWN`.

Codex may use lower effort for verified no-op dispatch, event routing and exact CI status; medium for scoped dependency update/ordinary defects; High for architectural owner mismatch, uncertain source equivalence, semantic rights conflict or whole J join failure. Preserve controller's actual supported self-adjustment range. Never spend High thinking on forwarding a known commit SHA.

**Budget triggers:** repeated failures to launch, excessive context consumption, repeated full test suites without new causal coverage, agents re-reading an unchanged estate every round, or new tests growing faster than actual fixed functions. Fix by reusing exact source inventory, selective tests and session prompts—not by silently shrinking terminal obligations.

## 7. Independence and receiving

A and B may both be fierce, independent authors. **Neither is a genuine independent terminal reviewer of its own intertwined ancestry.** For a completed coherent CG tranche or J join, freeze strongest candidate ancestry and submit to one nonauthor exact-source receiving agent/authorized court. The court judges original whole contract, real first consumer, native/authority limits and meaningful negatives. REVISE goes back to the pair for one finite correction/delta check, not a new series of review commissions.

Do not require an external court per 27 packet rows. Do not allow waiting on unrelated native Pyat grants to block legitimate sourcefree work. The domain crossing to Pyat/source-rights/native CAN/ADP or S14/A5 is an explicit HOLD until independently issued.

## 8. Next-work selection and programme conservation

The objective is **functional breadth completed per cost**, not duel count. Recompute DAG readiness after every accepted **or explicitly provisional-sourcefree** task; only let a downstream task rely on provisional parent in an isolated fixture with unqualified dependency status. It cannot report the same grade as if its parent had been independently received.

Keep a live conservation register for J1/J2/J3/J4 and PW-01..14; map each packet's producer→world/actor state→actual reader with one changed-value and meaningful failure. Preserve original 144/38/83/304/100 only as inherited evidence/identity denominators where exact sources support them; do not claim 27 packets can erase 144 functions.

Never implement an isolated pilot indefinitely: a pilot is an instrument to get a real consumer into the product. At end of each work cycle, tell HQ:
- Whole destination progress: which J cell and original functional effects now genuinely execute.
- Exact packet states, best candidate SHAs, current contract versions and blocked dependencies.
- Which assumptions changed, why, and which queued/active tasks were reconciled.
- Which source/science/actor/human holds remain externally governed.
- Actual cost and next highest-value ready executable construction.

**Read before dispatch:** `02_SOROK_IMPLEMENTATION_PROGRAMME_R1.md`, `03_TASK_PACKETS_R1.json`, full original `01_USER_ORIGINAL_DUEL_PERSONAS_UNABRIDGED.md`, live #913/#914/#915/#917/#924/#928, protected owner code, and the user's actual controller configuration. **Do not rediscover the whole original project on every wake.**

## 9. No launch implied by publication

This is a standing instruction set. The GitHub programme branch/PR and launch issue do not create OpenCode sessions, controller leases, notification listeners or model usage. The user sends the separate launch prompt in `05_CODEX_LAUNCH_PROMPT_R1.md` into the **existing local Codex controller context**, which must then verify and execute the machinery.
