# Rabochii Worker Packet Template

Every delegated assignment should instantiate this template. Sections may be shortened, but none should be omitted without a reason.

## Identity

- Worker ID:
- Branch:
- Prong:
- Capability / issue IDs:
- Base ref / SHA:

## Mission

State the concrete job in 2–5 sentences and explain why it exists in the end-to-end Rawlsing path.

## System position

Describe only the relevant local chain, for example:

`V552J canonical handoff → V553 temporal semantics → V554 consumer requirements`

Explain what the worker's output must preserve for the next consumer.

## Canonical read set

List exact files/contracts/tests to read first, in order. Do not tell workers to “familiarize yourself with the repo” when a bounded read set can be supplied.

## Frozen external facts

List decisions that bind the worker and are not open for redesign in this assignment.

Examples:

- current `main` is canonical;
- V550–V552J remain closed unless a proven interface defect requires escalation;
- Enneagram-like attractor formation is a designed Rawlsing capability;
- stage boundaries and provenance restrictions relevant to this lane.

## Upstream contract

Specify the exact admissible upstream artifacts, meanings, statuses, and authority assumptions.

## Downstream obligations

Specify what downstream consumers need from this work. This is mandatory even when the worker has no write access downstream.

For each obligation where useful:

- consumer;
- required semantic information;
- information that must not be collapsed;
- uncertainty/provenance requirements;
- relevant vertical slice.

## Known hazards / active findings

List only relevant issue IDs, deferred risks, historical failures, or misleading shadow paths.

## Write domain

Exact files/directories/functions/schema families the worker owns.

## Prohibited scope

List neighboring domains the worker must not modify or semantically decide.

## Required work

Numbered implementation/audit tasks with terminal criteria.

## Acceptance tests / evidence

State the minimum evidence Vozhd Dva will require to accept the work:

- focused unit/contract tests;
- fixture behavior;
- producer/consumer continuity;
- no-loss invariants;
- provenance/forbidden-inference checks;
- any required real-data smoke.

## Cross-cutting discovery protocol

If the worker discovers that correct completion requires changes outside the write domain:

1. do not invent downstream/upstream semantics;
2. record the exact dependency and evidence;
3. complete all lawful in-domain work;
4. return `PARTIAL_AWAITING_CROSS_HOOK` or another explicitly assigned terminal state;
5. identify the affected prong/capability/interface for Vozhd Dva synchronization.

## Deliverables

List exact files/artifacts/PR/report expected.

## Return report

The terminal report must include:

- status;
- branch / commit / PR;
- files changed;
- capability / issue dispositions;
- tests run and results;
- downstream obligations satisfied;
- unresolved cross-hooks;
- semantic/interface changes that other workers must now know;
- recommended Vozhd Dva integration action.
