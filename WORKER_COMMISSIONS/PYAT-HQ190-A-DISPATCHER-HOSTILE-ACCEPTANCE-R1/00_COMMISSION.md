# PYAT HQ190-A — Dispatcher/runtime hostile independent acceptance — R1

Repository: `maidiu/rawlsing`

Role: **HOSTILE INDEPENDENT REVIEWER / LOCAL-MACHINE RUNTIME ACCEPTANCE**

Preferred reviewer: **DeepSeek V4.1 Flash**, using the locally available provider/model identifier and reasoning variant actually selected at launch. Record the exact observed identifier; do not invent one.

Review target branch:
`agent/rabochii-pyat-hq188-a-opencode-dispatcher-runtime-repair-r1`

Exact returned remote tip to review:
`f522af5a7a01432159830dfbf26325c0e320adaf`

Substantive implementation/evidence candidate:
`5f9a93af1cc98d75d392794534484e41248efb5f`

Repaired dispatcher blob:
`f3067208f7a8b8ffc159bdc41c25309e9a14b5cb`

Commissioned repair base:
`ff7a06694b0391471b8e1223b2f881b3288f529e`

Review branch:
`agent/reviewer-pyat-hq190-a-dispatcher-hostile-acceptance-r1`

Return directory:
`WORKER_RETURNS/PYAT-HQ190-A-DISPATCHER-HOSTILE-ACCEPTANCE-R1/`

## Mission

Assume the HQ188-A repair is still unsafe or overclaimed. Try to break it.

This is not a style review and not a request to improve unrelated code. Determine whether the exact returned candidate satisfies the commissioned fail-closed/runtime claims, whether its evidence is non-vacuous, and what capability ceiling is actually justified.

The reviewer must remain independent: do not edit the worker candidate, do not repair it in place, and do not accept the worker's own harness as authoritative merely because it passes.

## Mandatory GitHub startup

The authoritative review commission is on GitHub.

Before review work:
1. `git fetch origin`.
2. Do not use blind `git pull`.
3. Resolve the exact review branch and verify it equals the commissioned startup SHA supplied in HQ's launch directive.
4. Resolve the exact target worker tip `f522af5a7a01432159830dfbf26325c0e320adaf`.
5. Verify `5f9a93af1cc98d75d392794534484e41248efb5f` is an ancestor of that target and that the dispatcher blob at both is exactly `f3067208f7a8b8ffc159bdc41c25309e9a14b5cb`.
6. Use an isolated review worktree.
7. Stop before testing if any identity differs.

The worker's three post-candidate commits are return-bookkeeping only if and only if Git proves that they modify no implementation/evidence other than the final-disposition bookkeeping file. Verify this independently.

## Read first

- HQ188-A commission and its startup/return protocol
- the complete HQ188-A return packet
- the October 3 publication/runtime audit:
  `PYAT_CONTROL_ROOM/SPACE_BUNNY_OPENCODE_R1/REVIEWS/HQ181_187_AUDIT_20261003/REVIEW.md`
- the audit repair plan and reproduced probes
- the repaired dispatcher source and worker harnesses

Do not infer acceptance from worker prose.

## Review stance

Attack claims with independently constructed cases. Reuse worker fixtures only as evidence inputs or for reproduction; important acceptance gates need reviewer-authored adversarial cases.

A failure must identify:
- violated acceptance property;
- exact evidence;
- scope;
- minimum repair needed.

Do not demand unrelated polish or a different architecture without a concrete failure.

## Mandatory attacks

### 1. Immutable task and commission binding
Try:
- missing/empty/non-full identities;
- literal placeholders such as `UNBOUND`;
- valid-shape but wrong identities;
- commission file changed after task construction;
- wrong base/candidate/worktree combination;
- symlink/canonical-path ambiguity;
- same missing value on both sides.

Verify rejection occurs for the correct reason, not because an earlier unrelated validator masks the intended gate.

### 2. Candidate/review/adjudication binding
Attempt to:
- apply review A to candidate B;
- mutate candidate after review;
- inject an arbitrary `ACCEPTED` event;
- omit review or HQ decision identity;
- use an unrecognized disposition;
- replay a valid receipt against another task.

Verify no path reaches accepted/publication state without the exact review and HQ adjudication relationship.

### 3. Git-derived terrain and publication
In disposable repositories/remotes:
- alter caller-supplied path metadata and confirm it has no authority;
- make an out-of-terrain change;
- move the expected remote parent after validation but before publication;
- create competing publications;
- test branch/path ambiguity;
- test candidate/base objects that exist but are not related as claimed.

The decisive evidence must come from Git, not fixture-provided assertions.

### 4. Persistence, corruption, recovery and races
Independently attack:
- truncated JSONL;
- malformed middle record;
- duplicate event/task identity;
- restart before launch;
- restart while process is running if safely reproducible;
- restart after process exit but before return delivery;
- duplicate submission at full capacity;
- simultaneous submissions from distinct OS processes;
- process death during append/lock ownership;
- stale lock behavior.

Determine exactly what is and is not crash-consistent. Do not turn local fsync into a transactional-store claim.

### 5. Lifecycle and HQ delivery
Verify with real local processes that:
- launched process identity is observed;
- exit does not itself become RETURNED;
- a return requires the required candidate identity;
- the completion becomes visible through the intended HQ inbox/queue without chat-copy intervention;
- restart reconstructs enough immutable bindings to continue honestly;
- missing return delivery stays missing rather than being inferred from process exit.

### 6. OpenCode invocation semantics
Independently inspect the installed CLI and actual execution.

Confirm or refute:
- model and reasoning variant are separate;
- actual launched values match task bindings;
- actual commission bytes are what the model receives;
- the worker's `--file` ordering fix works;
- help/stdout/stderr handling is truthful.

Do not treat CLI help text alone as proof of runtime behavior.

### 7. The three load-bearing limitations
These are mandatory hostile targets.

#### L2 — `--auto`
The worker reports that positive E2E required blanket `--auto`, and without it writes were rejected.

Determine whether this makes the candidate **unacceptable for unattended operation** absent a scoped permission profile. In disposable fixtures, test whether a commissioned agent under the actual invocation can perform actions outside its intended terrain or classes of tools once `--auto` is enabled.

Do not touch real sources or user data. Use fake repos/files only.

#### L1 — no containment
Determine what the dispatcher itself enforces versus what exists only as prompt/commission law. No OS/process isolation was demonstrated. Do not credit distinct worktrees/pids as containment.

#### L4 — `--file` instruction integrity
The worker reports attached commission content renders as faux tool-call blocks and a fixture agent identified it as injection-like.

Construct adversarial benign fixture commission files containing nested instruction-looking/tool-call-looking text. Determine whether the agent reliably treats the authenticated commission as governing instructions or whether the delivery mechanism creates ambiguity/injection risk.

A Git blob identity proves bytes, not interpretation.

### 8. Worker evidence/harness integrity
Independently re-run or inspect enough to establish whether:
- all 8 audit defects were truly reproduced pre-repair;
- 16/16 post-repair cases test the intended gates rather than masked/vacuous failures;
- E2E evidence corresponds to actual processes/commits;
- race results have correct denominators;
- no out-of-terrain tracked artifact remains;
- `rawlsing_next/**` and `HQ_HANDOFF/**` are untouched.

Pay special attention to the worker's admitted history of catching vacuous/mis-targeted probes.

## Acceptance question

Do **not** ask only whether the code is "better."

Answer separately:

1. Is the implementation mechanically improved and fail-closed relative to the audited prototype?
2. Is it safe/qualified for **unattended source-free orchestration** under the intended two-worker/reviewer topology?
3. If not, is it still an acceptable supervised repair base with an explicit capability ceiling?
4. What is the minimal next repair that would change the answer?

## Allowed review dispositions

Exactly one:

- `ACCEPT_FOR_UNATTENDED_SOURCE_FREE_ORCHESTRATION`
- `ACCEPT_AS_SUPERVISED_REPAIR_BASE__UNATTENDED_NOT_QUALIFIED`
- `CHANGES_REQUIRED_BEFORE_ADOPTION`
- `MATERIAL_COUNTEREXAMPLE__REPAIR_CLAIM_UNSOUND`

An acceptance must state its exact capability ceiling.

## Write terrain

Write only:
`WORKER_RETURNS/PYAT-HQ190-A-DISPATCHER-HOSTILE-ACCEPTANCE-R1/**`

Temporary disposable fixture repositories/worktrees may exist outside the repository and must not contain real source data.

Do not modify:
- the worker candidate;
- `rawlsing_next/**`;
- `HQ_HANDOFF/**`;
- any historical return;
- source/warrant artifacts.

## Required return packet

At minimum:
- `00_REVIEW.md`
- `01_TARGET_IDENTITY_AND_TERRAIN.json`
- `02_INDEPENDENT_NEGATIVE_CASES.json`
- `03_RUNTIME_E2E_AND_LIFECYCLE.json`
- `04_AUTO_PERMISSION_AND_CONTAINMENT_ATTACK.json`
- `05_COMMISSION_DELIVERY_INTEGRITY_ATTACK.json`
- `06_WORKER_EVIDENCE_CROSSCHECK.json`
- `07_CAPABILITY_CEILING_AND_MINIMUM_REPAIR.json`
- `08_FINAL_DISPOSITION.json`

## Return-to-HQ law

Commit the complete review to the review branch and push it to `origin`. Re-fetch and verify the remote branch equals local HEAD.

The return artifacts must record the stable reviewed target SHA and the substantive review-result commit if useful. They are **not required to embed their own enclosing branch-tip SHA**. The exact pushed review-tip SHA is reported in the completion message and will be independently resolved by HQ. Do not create an infinite self-referential SHA-record chain.

Do not merge into control or self-adopt.

## Hard holds

Zero raw-source access.
Zero locator discovery.
Zero warrant issuance.
Zero live C4.
Zero production-semantic mutation.
Zero C7/actor work.

Terminal:
`HQ190_A_DISPATCHER_HOSTILE_ACCEPTANCE_RETURNED__HQ_ADJUDICATION_REQUIRED`
