# Control Room Map

This file is the navigation surface for Vozhd Dva. A future Vozhd Dva chat should be able to orient from this file before reading deeper material.

## Command layer — whole-system context

Root files are Vozhd-Dva-facing and may refer to the whole project:

- `VOZHD_DVA_HANDOFF.md` — **read first in a fresh Vozhd Dva chat**; operating identity, doctrine, current campaign context, review law, worker-coordination law and exact restart/next-action protocol.
- `RAWLSING_GOVERNING_SPIRIT.md` — **binding interpretive law for ambiguity and design choice**; the project/spiritual manifesto that states the anthropology, causality, freedom/alienation/identification logic, Absolute-Horizon poles, anti-reduction law, and engineering tie-break principles. It governs choices only after explicit source/semantic authority and closed jurisdiction are satisfied; it never authorizes invention or architecture drift.
- `README.md` — mission and governing principles.
- `TERMINAL_DEMAND_ENVELOPE.md` — explicit finished-system demand lens: nine strata, inter-pressure, mediation, orientation-to-strata, Absolute Horizon, pressure-flow, attractors, V3 causality, genealogy, V2 and epistemic separation.
- `ARCHITECTURE_PASS_LAW.md` — formal whole-picture / bounded-jurisdiction law for every maximal architecture pass; defines four simultaneous views, disposition taxonomy, architecture checksum, no-starvation and no-bloat tests.
- `STRATEGY_AND_GATES.md` — execution strategy and gate sequence.
- `CONSTRAINTS_PRIORITIES.md` — scope, authority, economy, and anti-sprawl law.
- `CAPABILITY_MATRIX.md` — cross-stage capability requirements and vertical slices.
- `WORKSTREAMS_AND_DELEGATION.md` — current prongs and concurrency model.
- `LIVE_ITINERARY.md` — live sequence and near-term execution state.
- `state/CURRENT_STATE.md` — compact restart snapshot; this overrides stale status details in the longer handoff whenever project state changes.

The authority hierarchy is:

`explicit source semantics / accepted semantic authority`
`→ closed architecture and stage jurisdiction`
`→ RAWLSING_GOVERNING_SPIRIT.md for lawful ambiguity / tie-breaking`
`→ implementation convenience`.

The governing spirit is therefore mandatory context whenever a worker or Vozhd must choose among multiple otherwise-lawful designs. It is not itself empirical evidence, a missing-rule substitute, a new ontology, or permission to move meaning across settled jurisdictions.

The terminal envelope and architecture-pass law do not make every stage own the whole system. They force architecture workers to understand the complete machine while proving their local stage neither starves later capabilities nor pre-instantiates downstream semantics.

## Schematic transformation layer — what each stage actually does to upstream reality

`schematics/` is the pre-implementation reasoning layer for the transformation chain.

Its unit of analysis is the seam:

`upstream authority → lawful intake → stage-specific operation → enriched output → downstream requirement`

Contents:
- `schematics/TRANSFORMATION_METHOD.md` — canonical forward/backward reasoning method;
- `schematics/BOUNDARY_SESSION_TEMPLATE.md` — required breakout-session format;
- `schematics/SESSION_INDEX.md` — ordered seams from V552J→V553 through V3→V2;
- `schematics/boundaries/` — isolated seam workspaces;
- `schematics/synthesis/` — Vozhd-only reconciliation and accepted seam rulings;
- `schematics/recalibration/` — architecture-imagination reruns that test already excavated stages against the explicit terminal demand envelope without repeating unnecessary code archaeology.

Schematic workers may reason beyond their seam only enough to understand upstream authority and downstream need. Maximal architecture workers must additionally work backward from `TERMINAL_DEMAND_ENVELOPE.md` under `ARCHITECTURE_PASS_LAW.md`. They do not acquire implementation jurisdiction. Worker-local proposals become system law only after Vozhd synthesis.

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
- Does it satisfy the applicable terminal-demand obligations under the whole-picture/bounded-jurisdiction law?
- Where explicit law leaves a genuine design choice, is the choice faithful to `RAWLSING_GOVERNING_SPIRIT.md`?
- Did it move downstream semantics into the current stage merely because the worker knew the whole system?
- Did it introduce semantic loss or a new cross-prong dependency?
- Is it ACCEPT / ACCEPT_WITH_FOLLOWUP / RETURN_FOR_FIX / REJECT / DEFER?

If the disposition is `RETURN_FOR_FIX`, Vozhd must tell the user immediately and provide the exact paste-ready continuation prompt in that same response.

## State discipline

There must always be one compact current-state snapshot in `state/CURRENT_STATE.md`. Historical detail belongs in the relevant cell/prong/review/schematic session, not in the restart snapshot.

When a worker result changes the system, Vozhd Dva updates, in order as needed:
1. worker review;
2. schematic boundary/recalibration workspace if the result changes a transformation or terminal-demand sufficiency;
3. Vozhd schematic synthesis/ruling;
4. integration ledger;
5. affected prong state;
6. capability/strategy/terminal-demand/method files if architecture changed;
7. `state/CURRENT_STATE.md`;
8. `LIVE_ITINERARY.md`;
9. `VOZHD_DVA_HANDOFF.md` only when the durable operating doctrine or major campaign topology changes; do not rewrite it for ordinary status churn.

Implementation packets must cite the accepted local seam ruling and the applicable terminal-demand-ready architecture snapshot. When implementation or authority law leaves more than one lawful mechanism, packets must also use `RAWLSING_GOVERNING_SPIRIT.md` as the interpretive tie-break. The goal is that no future Vozhd Dva has to reconstruct the project from chat history or random PRs.
