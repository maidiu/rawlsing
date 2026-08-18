# Vozhd Trii — Pre-Change Discovery Control Surface

**Status:** `ACTIVE_RESEARCH_CONTROL__NO_ARCHITECTURAL_CHANGE_AUTHORIZED`  
**Branch:** `agent/vozhd-trii-prechange-discovery-control`  
**Branch base:** `0777a34e50221bde6801dbaca26c058a7350c9e8` (`main`, 2026-08-18 after PR #125)  
**Purpose:** preserve and operationalize the productive findings of the Vozhd Trii conversation before any V550–V552J redesign or deletion campaign begins.

This directory is the parent control room for the next Rawlsing discovery phase. It exists because several different kinds of evidence had become entangled in conversation: current production code, frozen VT3 archaeology, older design packs, live/public database schema, governing whole-machine law, and new observations about the V547–V549 lineage inside V550. The immediate task is to make those materials queryable, distinguish fact from inference, and define the questions that must be answered before architecture changes are proposed.

## Operating rule

**No production artifact, computation family, semantic lane, or historical capability is authorized for deletion, replacement, demotion, or promotion by this control surface.**

The working sequence is:

```text
preserve evidence
→ reconstruct actual capability genealogy
→ audit current behavior and data substrate
→ identify terminal semantic obligations
→ falsify assumptions
→ close discovery courts
→ only then design the recalibration
```

## Documents

1. [`00_FULL_MACHINE_VISION.md`](00_FULL_MACHINE_VISION.md) — rigorous statement of the complete Rawlsing destination against which all local optimization must be judged.
2. [`01_FINDINGS_LEDGER.md`](01_FINDINGS_LEDGER.md) — what has actually been established so far, with epistemic status and frozen/current separation.
3. [`02_RESOURCE_INDEX.md`](02_RESOURCE_INDEX.md) — repository paths, branches, governing law, historical packs, database schemas, and attachment hashes.
4. [`03_ASSUMPTION_AND_UNKNOWN_REGISTER.md`](03_ASSUMPTION_AND_UNKNOWN_REGISTER.md) — claims that remain assumptions, silent premises that could break a redesign, and questions the user may not have been explicitly tracking.
5. [`04_DISCOVERY_COURTS_REGISTER.md`](04_DISCOVERY_COURTS_REGISTER.md) — the finite set of deep-dive investigations to run before change design.
6. [`05_DECISION_PROTOCOL.md`](05_DECISION_PROTOCOL.md) — evidence hierarchy, closure rules, and the gate between discovery and architectural change.
7. [`06_FIRST_WAVE_LAUNCH_REGISTER.md`](06_FIRST_WAVE_LAUNCH_REGISTER.md) — exact sequencing, branch names, common law, and output contract for the first Rabochii discovery wave.
8. [`DISCOVERY_REGISTER.json`](DISCOVERY_REGISTER.json) — machine-readable workstream/dependency register.
9. [`evidence/HISTORICAL_DESIGN_EXTRACTS.md`](evidence/HISTORICAL_DESIGN_EXTRACTS.md) — exact key extracts from the historical V526c–V537 and Attitude Cloud packs, explicitly retained as genealogy evidence rather than current authority.
10. [`evidence/conversation_inputs/`](evidence/conversation_inputs/) — exact or hash-identified user-provided evidence snapshots and identity manifest used by this control surface.

## Two timelines must never be conflated

### Frozen archaeology timeline

The VT3 Conditional-Meaning Chamber adjudicated exact base:

`8c87f7725ba58202b5377c974548140420709fa9`

Its findings remain evidence about that frozen machine. The R00 synthesis lives on:

`agent/vozhd-trii-vt3-cm-r00-synthesis`

with R01–R11 on their named worker branches.

### Current production timeline

This control surface starts from current `main`:

`0777a34e50221bde6801dbaca26c058a7350c9e8`

That head includes merged PR #125, which installed the 18,518-row Final R1 full question-relation authority and migrated V550 runtime loading to it. Therefore every VT3 implementation claim must be rechecked before being described as current behavior.

## Central research correction now binding for the discovery phase

The VT3 chamber established that many broad V550 materializations are not proven canonical semantic objects. Subsequent archaeology established something different and equally important: **the capabilities that generate some of those artifacts descend from an older, deliberate empirical-discovery architecture and are still substantially implemented inside V550.**

The next phase must therefore distinguish:

```text
ARTIFACT PRESERVATION
!=
CAPABILITY PRESERVATION
```

A recursive tree, predictor summary, co-signature table, or attitude-cloud table may be replaceable as a stored artifact while the capability to discover historically meaningful heterogeneity, conjunctions, same-person cotravel, or position-conditioned response structure remains terminally necessary.

That distinction is the reason this control surface exists.
