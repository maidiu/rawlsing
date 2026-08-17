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

## Schematic transformation layer — what each stage actually does to upstream reality

`schematics/` is the pre-implementation reasoning layer for the transformation chain.

Its unit of analysis is the seam:

`upstream authority → lawful intake → stage-specific operation → enriched output → downstream requirement`

Contents:
- `schematics/TRANSFORMATION_METHOD.md` — canonical forward/backward reasoning method;
- `schematics/BOUNDARY_SESSION_TEMPLATE.md` — required breakout-session format;
- `schematics/SESSION_INDEX.md` — ordered seams from V552J→V553 through V3→V2;
- `schematics/boundaries/` — isolated seam workspaces;
- `schematics/synthesis/` — Vozhd-only reconciliation and accepted seam rulings.

Schematic workers may reason beyond their seam only enough to understand upstream authority and downstream need. They do not acquire implementation jurisdiction. Worker-local proposals become system law only after Vozhd synthesis.

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

Schematic synthesis rulings feed this layer before implementation workers are launched against shared seams.

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

There must always be one compact current-state snapshot in `state/CURRENT_STATE.md`. Historical detail belongs in the relevant cell/prong/review/schematic session, not in the restart snapshot.

When a worker result changes the system, Vozhd Dva updates, in order as needed:
1. worker review;
2. schematic boundary workspace if the result changes a transformation seam;
3. Vozhd schematic synthesis/ruling;
4. integration ledger;
5. affected prong state;
6. capability/strategy files if architecture changed;
7. `state/CURRENT_STATE.md`;
8. `LIVE_ITINERARY.md`.

Implementation packets must cite the accepted local seam ruling where one exists. The goal is that no future Vozhd Dva has to reconstruct the project from chat history or random PRs.
