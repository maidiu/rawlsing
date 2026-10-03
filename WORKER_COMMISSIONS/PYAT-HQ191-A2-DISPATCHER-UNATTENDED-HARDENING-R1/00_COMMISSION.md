# PYAT HQ191-A2 — Dispatcher unattended hardening after hostile review — R1

Repository: `maidiu/rawlsing`

Role: **RABOCHII / LOCAL-MACHINE IMPLEMENTER — SPACE BUNNY**

Branch:
`agent/rabochii-pyat-hq191-a2-dispatcher-unattended-hardening-r1`

Exact implementation base:
`c782b455d492e47d39d54274f24829d36e8e0077`

The exact commissioned startup SHA is supplied by HQ after this commission commit is published.

Return directory:
`WORKER_RETURNS/PYAT-HQ191-A2-DISPATCHER-UNATTENDED-HARDENING-R1/`

## Mission

Repair the exact hostile-review findings against the now-adopted **supervised-only** dispatcher base.

Governing review:
`agent/reviewer-pyat-hq190-a-dispatcher-hostile-acceptance-r1 @ 1aae86c831ead4f9cd5ca97b39c081322fe2d9bd`

Current dispatcher blob at base:
`f3067208f7a8b8ffc159bdc41c25309e9a14b5cb`

Do not rewrite the architecture. Preserve the fail-closed identity/terrain/adjudication gates that the reviewer accepted.

## Mandatory startup

Fetch origin, verify this exact worker branch equals the startup SHA HQ supplies, use an isolated clean worktree, no blind pull, stop on mismatch.

## Required repairs

### MR-1 — atomic admission
Deduplication, slot-capacity decision and QUEUED append must occur in **one writer-lock transaction**.

Acceptance:
- use the reviewer's minimal counterexample and independent new stress;
- N >> cap processes;
- many repeated trials;
- admitted tasks must never exceed cap;
- duplicate task submission remains idempotent.

A single lucky trial is insufficient.

### MR-2 — un-droppable state transitions
Fix event identity/sequence law so QUEUED → RUNNING → RETURNED cannot be silently swallowed because a state reuses a sequence.

Preferred:
- one monotonic per-task/attempt sequence allocator under the writer lock; or
- another design that proves legitimate different states cannot dedup accidentally.

Do not merely append `state` to a key if that creates replay ambiguity elsewhere without addressing sequence ownership.

### MR-3 — no blanket `--auto`
Replace blanket OpenCode `--auto` for unattended fixture execution with a scoped permission mechanism.

On the installed OpenCode version, inspect actual supported permission/config surfaces rather than guessing.

Acceptance:
- authorized fixture write succeeds;
- out-of-terrain write is denied **by runtime/tool permission before write**, not merely rejected later by Git terrain validation;
- dangerous unrelated tool/file access is denied where the role does not require it;
- no global user configuration is destructively rewritten.

If installed OpenCode cannot express sufficient scoped permissions, return that limitation rather than hiding it behind `--auto`.

### MR-4 — process containment
The prior review found no OS/process containment.

Determine the minimum practical local containment compatible with the operating Mac:
- OS user/ACL separation;
- sandbox profile;
- or another host-enforced boundary.

Do not claim worktree separation is containment.

If genuine OS-level containment cannot be implemented without disproportionate/unsafe machine changes, preserve it as a limitation and target a lower capability ceiling.

### MR-5 — commission delivery integrity
The `--file` channel may render content as faux tool-call blocks.

Build a robust authoritative instruction-delivery protocol that:
- binds exact commission bytes;
- clearly frames them as governing instructions;
- treats nested tool-call-looking text inside the commission as data, not a second authority source;
- is exercised with adversarial benign fixture commissions.

Do not trust a hash alone to solve interpretation.

### MR-6 — lock/durability hardening
- stale lock reclaim must not reclaim a verified live writer merely because mtime is old;
- fsync the containing state directory where required for creation durability;
- test interrupted/crash-like recovery as far as safely possible.

## Full regression

Re-run the accepted gates from HQ188-A plus reviewer-authored cases:
- missing/placeholder identities;
- commission drift;
- review/candidate/adjudication mismatch;
- arbitrary ACCEPTED;
- Git-derived terrain;
- stale expected parent;
- corruption/torn log;
- duplicate submission;
- capacity stress;
- state-transition preservation;
- return delivery/recovery.

Use real OpenCode fixture processes where needed and source-free fake repos only.

## Allowed write terrain

- `PYAT_CONTROL_ROOM/SPACE_BUNNY_OPENCODE_R1/runtime/**`
- `PYAT_CONTROL_ROOM/SPACE_BUNNY_OPENCODE_R1/ACTIVATION_RETURNS/OPS-02-03-HARDENING-R2/**`
- `WORKER_RETURNS/PYAT-HQ191-A2-DISPATCHER-UNATTENDED-HARDENING-R1/**`

Do not touch production, sources, warrant, HQ_HANDOFF, historical returns.

## Return dispositions

Exactly one:
- `CANDIDATE_READY_FOR_UNATTENDED_HOSTILE_REVIEW`
- `SUPERVISED_MULTILANE_REPAIR_READY__UNATTENDED_STILL_BLOCKED`
- `MATERIAL_HARDENING_INCOMPLETE`
- `HOST_CAPABILITY_BLOCKED`

Do not self-qualify. Any claim beyond the current supervised ceiling requires independent hostile review.

## Return law

Commit the stable substantive result; push branch; re-fetch and verify.

Artifacts record substantive result SHA only. Report pushed branch tip out-of-band; do not chase self-reference.

Terminal:
`HQ191_A2_DISPATCHER_HARDENING_RETURNED__HQ_REVIEW_REQUIRED`

## Holds

Zero raw sources, locators, warrant, live C4, C7 or actor work.
