# PYAT HQ188-A — OpenCode dispatcher/runtime fail-closed repair — R1

Repository: `maidiu/rawlsing`

Role: **RABOCHII / LOCAL-MACHINE IMPLEMENTER — SPACE BUNNY**

Exact base: `6820160533859cf8dd283d10c043947dfe1dd5d4`

Branch: `agent/rabochii-pyat-hq188-a-opencode-dispatcher-runtime-repair-r1`

Return directory: `WORKER_RETURNS/PYAT-HQ188-A-OPENCODE-DISPATCHER-RUNTIME-REPAIR-R1/`

## Mission

Repair the currently shipped Space Bunny/OpenCode dispatcher/runtime so it can later be independently qualified for bounded unattended source-free orchestration. This is an implementation lane, not an acceptance or adoption lane.

Read first, at the exact base:
- `PYAT_CONTROL_ROOM/SPACE_BUNNY_OPENCODE_R1/CURRENT_HANDOFF.md`
- `PYAT_CONTROL_ROOM/SPACE_BUNNY_OPENCODE_R1/REVIEWS/HQ181_187_AUDIT_20261003/REVIEW.md`
- `PYAT_CONTROL_ROOM/SPACE_BUNNY_OPENCODE_R1/REVIEWS/HQ181_187_AUDIT_20261003/REPAIR_PLAN.md`
- `PYAT_CONTROL_ROOM/SPACE_BUNNY_OPENCODE_R1/REVIEWS/HQ181_187_AUDIT_20261003/probe-results.json`
- `PYAT_CONTROL_ROOM/SPACE_BUNNY_OPENCODE_R1/REVIEWS/HQ181_187_AUDIT_20261003/reproduce-probes.mjs`

The audit disposition is binding input: the historical 23-pass/1-skip helper record is **not** end-to-end dispatcher qualification.

## Allowed write terrain

Implementation:
- `PYAT_CONTROL_ROOM/SPACE_BUNNY_OPENCODE_R1/runtime/**`

Repair tests/evidence:
- `PYAT_CONTROL_ROOM/SPACE_BUNNY_OPENCODE_R1/ACTIVATION_RETURNS/OPS-02-03-REPAIR-R1/**`
- your return directory above

Do not edit:
- `rawlsing_next/**`
- raw survey/source storage
- `HQ_HANDOFF/**`
- historical OPS-01/02/03/04 return bytes
- prior checkpoints/returns
- any production-semantic authority artifact

## Required implementation properties

### A. Fail-closed immutable task binding
A runnable task must persist and validate enough information to reconstruct the exact commission without conversational memory:
- task ID / attempt / sequence;
- role;
- exact base commit;
- isolated worktree;
- allowed write terrain;
- frozen acceptance inputs;
- commission path and immutable commission identity;
- model and reasoning variant as separate fields;
- session/process receipt once launched.

Reject missing, placeholder, `UNBOUND`, malformed, or non-full required identities. Do not treat two absent identities as equality.

### B. State-transition and acceptance discipline
Do not allow an arbitrary appended `ACCEPTED` event to manufacture accepted state.

Acceptance/publication state must require an explicit, structurally valid HQ adjudication/decision receipt bound to the exact candidate and review. The worker may implement and test this machinery with fixtures; the worker **may not issue real HQ authority**.

A review must bind the immutable candidate it reviewed and carry a recognized approving/nonapproving disposition. A materially changed candidate invalidates the old review.

### C. Git-derived publication gate
Do not trust caller-supplied changed-path arrays or two strings standing in for repository state.

For any publication eligibility helper:
- resolve exact candidate/base/expected-parent from Git;
- derive changed paths from Git;
- enforce allowed terrain from the task binding;
- validate candidate↔review↔HQ-decision identity;
- fail closed on missing objects/fields;
- check the actual remote expected parent immediately before any publication operation.

Implement/test this in disposable Git fixtures. **Do not publish this worker branch into control.**

### D. Durable event store, recovery, and concurrency
The store must not silently discard malformed/torn event records. Preserve or surface corruption as a blocking recovery state.

Persist enough immutable task/session information for restart recovery.

Make duplicate submission idempotent **before** capacity accounting.

Eliminate the current read-then-append race with a single enforced writer or equivalent transaction/locking discipline appropriate to this local runtime.

Demonstrate that restart reconstructs the exact task/session state rather than merely a state label.

### E. Actual process lifecycle and return notification
A launch is not qualified by constructing argv.

Bind:
- observed launch receipt;
- process/session identity;
- running transition;
- completion/exit result;
- candidate return identity;
- delivery back to HQ/runtime queue.

A worker completion must become observable to HQ without requiring the user to copy a chat message.

Interrupted launch/restart must reconcile honestly rather than invent success.

### F. OpenCode invocation correctness
On the actual operating host, inspect the installed OpenCode CLI/config and distinguish:
- `--model provider/model`
- `--variant <reasoning variant>`

Do **not** guess a provider/model ID.

The selected Space Bunny model and selected reasoning variant must be demonstrably the ones launched.

Deliver actual commission contents using the installed CLI's supported mechanism (for example `--file` if supported); passing only a pathname as ordinary prompt text is insufficient unless you prove that installed-version behavior loads the file.

Record the installed CLI version/help evidence used.

Do not rewrite global user configuration unnecessarily.

## Mandatory pre/post negative cases

Reproduce the audit's failures against the pre-repair implementation, then show they fail closed after repair:

1. literal `UNBOUND` commission/acceptance;
2. missing candidate identities in publication gate;
3. duplicate submission at full capacity;
4. corrupt/truncated event log;
5. restart with queue record missing reconstructive bindings;
6. arbitrary ACCEPTED event;
7. Q08-style wrong-state result map;
8. argv-only launch without evidence of actual model/commission execution.

Also add at minimum:
- review for candidate A presented against candidate B;
- non-full/empty Git identity;
- write outside declared terrain;
- stale expected remote parent;
- two genuine fixture processes racing submission/publication;
- interrupted launch then restart;
- worker completes but return delivery is missing;
- unavailable Python reported truthfully rather than hardcoded PASS.

Use disposable source-free fixture repositories and fake source directories only. Do not touch real raw storage.

## Positive end-to-end proving sequence

After unit/negative repair tests, run an actual source-free fixture workflow with:
- two fixture workers in distinct temporary worktrees;
- one separate fixture reviewer in a third worktree;
- exact commissions delivered as file content;
- durable session/process receipts;
- completion delivered back to HQ queue;
- restart/recovery between at least one lifecycle stage;
- candidate-changing-after-review invalidation;
- competing-publication expected-parent reconciliation against an actual disposable Git remote.

The worker may use Space Bunny for these fixture processes if that is the actual configured local surface. Do not claim process/OS isolation unless actually demonstrated.

## Required return packet

Return at least:
- `00_RETURN.md`
- `01_DIFF_AND_TERRAIN.json`
- `02_PRE_POST_NEGATIVE_CASES.json`
- `03_END_TO_END_FIXTURE_RUN.json`
- `04_RECOVERY_CONCURRENCY_EVIDENCE.json`
- `05_OPENCODE_MODEL_VARIANT_BINDING.json`
- `06_LIMITATIONS_AND_UNQUALIFIED_CAPABILITIES.json`
- `07_FINAL_DISPOSITION.json`

Final disposition must be one of:
- `CANDIDATE_READY_FOR_INDEPENDENT_ACCEPTANCE`
- `MATERIAL_REPAIR_INCOMPLETE`
- `HOST_CAPABILITY_BLOCKED`

Do **not** return `ADOPTED`, `QUALIFIED`, or `PASS_FOR_AUTONOMOUS_PUBLICATION`. Independent hostile acceptance is mandatory after this candidate freezes.

## Hard holds

Zero raw-source access.
Zero source locator discovery.
Zero warrant issuance.
Zero live C4.
Zero production-semantic mutation.
Zero C7 or actor implementation.
Zero self-adoption.
Zero control-branch publication.

Terminal on success:
`HQ188_A_DISPATCHER_REPAIR_CANDIDATE_RETURNED__INDEPENDENT_ACCEPTANCE_REQUIRED`
