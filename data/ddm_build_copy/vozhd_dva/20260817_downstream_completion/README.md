# Vozhd Dva — Downstream Completion Control Room

**Project:** Rawlsing V553→V558 semantic completion, V3/V2 rebuild, and app-ready vertical integration  
**Coordinator:** Vozhd Dva  
**Started:** 2026-08-17  
**Canonical implementation base:** current `main`

## Mission

Finish Rawlsing economically and at high quality by extending the best pipeline actually implemented in the repository. The immediate objective is to turn the existing V553–V558 thin/scaffolded downstream path into a semantically complete, vertically validated path that can support the redesigned V3/V2 runtime and a defensible app/resume artifact.

This directory is the live control plane for that execution. It records only the strategy, constraints, work decomposition, cross-stage requirements, decisions, and current itinerary needed to coordinate Rabochii work without semantic drift or duplicated redesign.

## Governing principles

1. `main` is the canonical implementation frontier. Older project material is evidence about intent only when a concrete ambiguity requires it.
2. V550–V552J are closed by default. Reopen only if a downstream failure proves an upstream interface defect that cannot lawfully be repaired downstream.
3. V553–V558 must be built with downstream needs visible. No stage is treated as independently finishable in a vacuum.
4. Every maximal architecture pass must read `TERMINAL_DEMAND_ENVELOPE.md` and `ARCHITECTURE_PASS_LAW.md`: workers see the complete Rawlsing machine but may architect only the bounded transformation their stage owns.
5. Work is organized by vertical semantic capability as well as by stage ownership.
6. Information loss across stage boundaries must be explicit and justified; silent semantic loss is a defect.
7. Enneagram-like attractor formation is part of the intended Rawlsing design. The task is to assign its proper stage responsibilities, not to reconsider its inclusion.
8. Architecture work is bounded: it exists to prevent rework and launch implementation, not to become a separate research program.
9. Scope discipline is mandatory. Anything that does not block a named vertical capability, horizontal qualification, V3/V2 integration, genealogy, or the app path is deferred.
10. Quality is evaluated end-to-end. A locally elegant stage that starves downstream consumers is not complete.
11. Economy matters: prefer the smallest mechanism that gives reliable coordination, traceability, and regression protection.

## Whole-picture / bounded-jurisdiction law

Architecture workers reason simultaneously from:
- the whole-system terminal destination;
- all lawful cumulative upstream material;
- the current stage's unique semantic jurisdiction;
- all downstream consequences.

Whole-system knowledge is used to prevent starvation, not to import later semantics early. Direct DAG reuse of earlier authoritative objects is preferred over forced serial republishing.

## Current entry condition

The active architecture path is under terminal-demand recalibration before V553 implementation. Existing S00/S00.5 and PRE-S01/PRE-S01.5 excavations remain evidence; their maximal architecture conclusions are being re-tested explicitly against the whole terminal system before implementation authority is restored.

## Files in this control room

- `TERMINAL_DEMAND_ENVELOPE.md` — explicit final Rawlsing demand.
- `ARCHITECTURE_PASS_LAW.md` — whole-picture / bounded-jurisdiction method and architecture checksum.
- `STRATEGY_AND_GATES.md` — execution phases and acceptance gates.
- `WORKSTREAMS_AND_DELEGATION.md` — parallel prongs, ownership, and Rabochii coordination.
- `CONSTRAINTS_PRIORITIES.md` — anti-sprawl rules, authority order, and decision priorities.
- `CAPABILITY_MATRIX.md` — cross-stage semantic requirements and vertical slices.
- `LIVE_ITINERARY.md` — current sequence, active work, blockers, and next launches.

## Completion target

A successful cycle ends with:

- semantically deepened V553–V558 contracts and implementations;
- explicit vertical continuity from V552J through V558;
- representative multi-wave and multi-source qualification;
- redesigned V3 consuming lawful structural priors and realizing actor-specific developmental orientation-to-strata, pressure-flow and attractor formation;
- historically constrained genealogy/household recursion;
- redesigned V2 rendering phenomenology/conversation without becoming causal authority;
- an app-facing path that can be demonstrated, explained, tested, and presented as a coherent engineering/research project.
