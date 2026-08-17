# Control Room Map

This file is the navigation surface for Vozhd Dva. A future Vozhd Dva chat should be able to orient from this file before reading deeper material.

## Command layer — whole-system context

Root files are Vozhd-Dva-facing and may refer to the whole project:

- `README.md` — mission and governing principles.
- `STRATEGY_AND_GATES.md` — execution strategy and gate sequence.
- `CONSTRAINTS_PRIORITIES.md` — scope, authority, economy, and anti-sprawl law.
- `CAPABILITY_MATRIX.md` — cross-stage capability requirements and vertical slices.
- `WORKSTREAMS_AND_DELEGATION.md` — current prongs and concurrency model.
- `LIVE_ITINERARY.md` — live sequence and near-term execution state.
- `state/CURRENT_STATE.md` — compact restart snapshot; update whenever project state materially changes.

## Prong spaces — bounded shared context

`prongs/` contains one directory per active prong. A prong may span multiple workers, but should contain only the external context necessary for that prong to remain synchronized with the whole system.

Each prong should state:

- objective;
- owned semantic/coding domain;
- required inputs;
- prohibited scope;
- dependencies on other prongs;
- outputs owed to integration;
- acceptance conditions.

## Rabochii cells — isolated delegated work

`rabochii/` contains one cell per worker assignment. Cells are task-local. A worker should not infer authority from neighboring cells.

A cell records:

- worker ID / branch;
- exact assignment;
- read set;
- write domain;
- issue/capability IDs owned;
- frozen external assumptions;
- deliverables;
- return/report format;
- status and terminal disposition.

Cross-cutting discoveries are returned to Vozhd Dva for integration; workers do not silently expand their own jurisdiction.

## Integration — synchronization across prongs

`integration/` is owned by Vozhd Dva. It records facts that must remain coherent across worker boundaries:

- dependency/synchronization ledger;
- interface changes;
- cross-prong blockers;
- merge/integration order;
- unresolved semantic collisions;
- accepted common contracts.

This is where local worker outputs become a coherent system.

## Review — Vozhd Dva assessment of returned work

`reviews/` contains Vozhd Dva's assessment of Rabochii outputs and PRs. Review state is separate from worker self-report.

A review should answer:

- Did the worker stay in scope?
- Did the work satisfy its assignment?
- Does it preserve upstream authority?
- Does it satisfy downstream consumers?
- Did it introduce semantic loss or a new cross-prong dependency?
- Is it ACCEPT / ACCEPT_WITH_FOLLOWUP / RETURN_FOR_FIX / REJECT / DEFER?

## State discipline

There must always be one compact current-state snapshot in `state/CURRENT_STATE.md`. Historical detail belongs in the relevant cell/prong/review, not in the restart snapshot.

When a worker result changes the system, Vozhd Dva updates, in order as needed:

1. worker review;
2. integration ledger;
3. affected prong state;
4. capability/strategy files if architecture changed;
5. `state/CURRENT_STATE.md`;
6. `LIVE_ITINERARY.md`.

The goal is that no future Vozhd Dva has to reconstruct the project from chat history or random PRs.
