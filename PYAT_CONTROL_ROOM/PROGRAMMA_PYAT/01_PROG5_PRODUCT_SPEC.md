# PROG5 — THE PYAT DEVELOPMENT ROADMAP: PRODUCT SPECIFICATION
**User-directed scope clarified 2026-11-02.** This document specifies the *guide for finishing Pyat*, not the Pyat source-to-world engine itself. It supplements (does not replace) [00_PROGRAMMA_PYAT.md](00_PROGRAMMA_PYAT.md), the inherited [Programma Rawlsing constitution](../../CROSS_HQ_CONTROL_ROOM/PROGRAMMA/00_PROGRAMMA_RAWLSING.md) and all existing source/science/HQ authority.

## 1. Purpose and completion
**One accessible, durable, source-exact, navigable map of the ENTIRE Pyat development undertaking, from governed source to the PRE-V3→V3 gate.** A fresh development agent should find, within minutes: (1) what the whole project is intended to become; (2) where a component fits; (3) every relevant existing design/vision/plan/implementation/test/review/source asset; (4) the strongest existing expression of its needed functionality, even if historical/unadopted; (5) the actual current implementation and its development state; (6) which upstream/downstream/authority connections exist and their state; (7) exact unmet prerequisites, residuals, and what to work on without duplicating earlier work.

**PROG5 DONE** = a useful guide to Pyat, not a beautiful new system. It is NOT a second Pyat HQ, new code engine, autonomous scheduler, scientific model, agent platform, long-running ingestion service, replacement for existing progress ledgers, or prerequisite to doing actual Pyat development forever. Once first assembled and checked, ordinary workers update the few affected entries as they make progress.

**Permanent home:** `PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/` within `integration/pre-main-reconciliation-r1`. The guide may *reference* code/branches elsewhere, but should not migrate or modify original code. “All in one place” refers to a single **finding aid and interrelated roadmap**, not physical copying of historical source, survey bytes or executable assets. Scope is Pyat through its V3 gate; Sorok is represented only at its necessary receiving-interface boundary.

## 2. What an agent can navigate
**Whole-project view:** intended pipeline; major organs; all nested plans; current/reviewed/historical status; highest-impact missing functions and unresolved boundaries.
**Section and subsection view:** parent(s), purpose, required behavior, finer requirements, relevant original roadmap/vision citations, interfaces and sources.
**Asset view:** exact file/path/branch/commit/blob, document/Library identity when available, age/succession, kind (idea, specification, architecture, current code, historical implementation, test, review, decision, negative), relevant components (many-to-many), strongest preserved useful function, adopted/nonadopted distinction.
**Connections:** upstream input, downstream receiver, conditional prerequisite, alternative implementation, scientific/authority precondition, producer→consumer contract. Each connection has **state**, evidence, and the exact missing interface/validation if unfinished.
**Remaining work:** small concrete unmet actions and prerequisites, not speculative implementation advice or bureaucratic green/yellow theater. Navigable backward: “X requires Y; Y requires Z,” with conditional and alternative edges carefully marked.

We need both **top-down** (end goal→functions→assets/unfinished requirements) and **bottom-up** (asset/current symbol→function/requirements→consumers→end goal) discovery.

## 3. Small, legible records — no schema cathedral
**Asset entry (reference, not a copy):** stable asset ID; kind; human title; exact location and immutable Git ref/blob or Library identifier; source-era / currentness; what capability or obligation it illuminates; links to component IDs; whether inspected or only reported; limitations. Historical old code may be *stronger for one function* than current integrated code while remaining unadopted. Preserve both.
**Component entry:** stable component ID; names/aliases, all parent/membership plan IDs; purpose and expected behavior; original and latest architectural sources; linked current code + best historical alternatives; fine-grained development status; evidence of actual consumer; missing subrequirements; corresponding source/authority obligations; incoming/outgoing seam IDs; practical next actions. Never infer a child's completion from its parent.
**Seam/prerequisite entry:** from/to component IDs; kind (requires, conditioned-on, alternate route, consumes, issues authority); required behavior/shape; state such as VERIFIED_WORKING_AT_EXACT_SCOPE, PARTIAL/INCOMPATIBLE, MISSING, HELD_AUTHORITY, NOT_APPLICABLE_PROVED or UNKNOWN; exact evidence and next missing part. **GREEN must mean tested at the stated consumer and scope**, never “has an import” or “architecturally planned.” Conditional edges remain conditional.
**Section overview:** what it accomplishes, contents, interfaces with other sections, major missing/under-developed areas, links to every child and inherited roadmap.

Exact status dimensions may be simplified for human reading but must not collapse **planned/spec'd/code-present/tested/current-integrated/real-consumer/native-source-qualified** into one PASS. Lawful refusal, untested, historical-only, and unknown are distinct.

## 4. Required coverage and traceability
- **Vision and full intended architecture:** latest Astra's N0–N13 (including N8E/N8S, N10E/N10W), F1–F8; the 101 task classes and G/S/P/Q/L/F/T/W/A registers; original V550/J, Dva/Trii/Chetiri, Long Memory and FF, N11/N12 receiving gate. Link overlapping plans instead of picking one and deleting the other.
- **Whole historical and current estate:** main, PRE-MAIN, relevant unintegrated branches and RRIF fate records, source inheritance, source configurations/real permissions, project and Library documents, reviews, negatives, tests, accepted owners and current first consumers.
- **Non-orphan condition:** every known materially relevant asset is linked to one or more components OR resides in an explicit UNPLACED/UNVERIFIED register with a reason and precise discovery request. No blind 845-branch recensus; reuse RRIF and prior archival source registries.
- **No ghost completion:** representation 20/35 != native source permission; 1,890 matrix cells != admissible original operations; P1 840 synthetic manifests != executable original work; sourcefree route/fixture tests != original native measured consumer; strongest old code != current accepted code. Preserve existing documented scope.
- **Currentness:** freeze the cut and allow human updates. Changed implementation/review/source? Update the affected entry and seams, with source link and date. No daemon, new event platform, auto orchestration or mandatory live refresh.

## 5. Form and usability
**Default form**: straightforward Markdown overview/section/component pages + small JSON/JSONL reference/index tables when needed for searching and consistency. Reuse W1-H's already tested reference in the **control-room directory**, moving/adjusting only what is actually useful. The existing Astra atlas includes a self-contained `index.html`; reuse its navigation and content where it helps rather than writing another frontend. More software is never an automatic deliverable. Human-readable browsability is required; elaborate interactive visualization is not.

**Every entry must link sources and neighbors**: a reader should not have to infer code symbols from prose, reconstruct commit history, or consult seven incompatible reports unaided.

## 6. Project boundaries and stop rules
- **No new Pyat empirical code, source-native operation, U/Epre scientific issuance, N11/N12 acceptance, Sorok actor grant, or PRE-MAIN production behavior** arises from prog5 mapping.
- **No separate project-management hierarchy, duplicated flight board, meta-review loop, perpetual gap hunting, database/graph service/daemon or recurrent research fleet.**
- Do not demand all historical artifacts be exhaustively read at full depth if indexed trustworthy inventories plus precise focal source inspection suffice; do not abandon material historical functions behind “old branch” labels.
- Do not stop Pyat actual development waiting for every roadmap nicety. When the guide is usable and unresolved physical-source requests have exact identifiers, **finish prog5 and use it**.
- Revisit roadmap structure only if a concrete wrong/missing architectural organ or broken navigational answer demonstrates the need.

**Product acceptance (human practical):** an unfamiliar qualified Pyat agent can locate C11, Field Forge, F6/F7, original35 workload, N9/N10W, N11/V3 seam, inspect each one's exact current and best historical work, identify missing subfunctions and adjacent seam states, and navigate their prerequisites without repeating archaeology. A few finite correction passes, then **DONE**.

## 7. Related governing source material
- [Finite work course](02_PROG5_FINITE_BUILD_COURSE.md)
- [GitHub-first evidence sources and existing work](03_PROG5_EXISTING_WORK_AND_SOURCE_QUEUE.md)
- [Provisional source→V3 gate roadmap](04_PROG5_ROUGH_SPINE.md)
- [Astra development atlas](../ASTRA_PYAT_INTEGRATED_DEVELOPMENT_ATLAS_R1/README.md)
- [Whole-Machine work register](../WHOLE_MACHINE_COMPLETION_R1/GLOBAL_WORK_REGISTER.md)
- [Critical all35 workload seam](../WHOLE_MACHINE_COMPLETION_R1/AUTOMATED_WORKLOAD_CONSTRUCTION_CRITICAL_GATE.md)
