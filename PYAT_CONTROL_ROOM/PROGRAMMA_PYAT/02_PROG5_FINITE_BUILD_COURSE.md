# PROG5 — FINITE CONSTRUCTION COURSE AND PRIORITIES
**Course agreed 2026-11-02.** Scope is the roadmap *about* Pyat, not engineering the Pyat engine. Read [the product contract](01_PROG5_PRODUCT_SPEC.md) and [existing estate](03_PROG5_EXISTING_WORK_AND_SOURCE_QUEUE.md).

## The fixed order of work
**GitHub-wide source reconnaissance + latest vision → first complete rough source-to-V3-gate spine → index the GitHub assets → supplement Library → specific mainMac gap requests only if evidenced → attach assets and resolve functional placement → actual completion/dependency/seam sweep → practical usability/correction → stop.**

Do NOT invert this by trying to mark every historical item DONE/RED before the whole rough spine exists. The initial scan is reconnaissance of material and chronology, not final adoption or detailed architectural arbitration. Keep an asset record even if its place is initially uncertain.

## Cycle I — scan GitHub, pick the best spine, draw the entire outline
### I-A. Broad scan: what exists and where
Search `main`, live `integration/pre-main-reconciliation-r1`, current Pyat code and control-room, the inherited `data/ddm_build_copy/` estate, relevant Dva/Trii/Chetiri/Long Memory/Field Forge/Verkhovod/EE/PRE-V3 docs and code, W1-A–H, and the **already completed** RRIF branch/function dispositions. Inspect a source's exact path, real branch, SHA, type, old/current grade and references to other material. Use Git trees and existing inherited indexes for breadth, then source reads for high-value functions. Duplicate paths and historical copies are tracked as versions, not counted as distinct capabilities.

**First input is GitHub.** Library is second pass. mainMac is not searched speculatively. User supplies selected OpenCode/Codex local agents only when we can name a missing path/function/asset class and cite the Git/Library document that implies its existence.

Deliver: `GITHUB_ASSET_REGISTER` in a simple stable searchable format, `UNVERIFIED_OR_UNAVAILABLE_REFERENCES` with reason, and observed Git/branch cuts. No source folder relocation.

### I-B. Select the *present best* engineering/vision spine
Read the latest governing Pyat vision, Astra's `report/D_CANONICAL_ARCHITECTURE_SPINE.md`, `PROGRAM.md`, `DEPENDENCY_DAG.md`, `data/nodes.json`, `report/N_OBJECTIVE_PRE_V3_MAP.md`, `report/Y_FINAL_ORDERED_PROGRAM.md`, whole-machine G/S/P/Q/L/F/T/W/A, 101 task classes, 35 source estate, current PRE-MAIN relevant code/consumers and newer source-exact findings. Treat older original V550–V558 staging as inherited *functionality/vision*, not mandatory current pipeline seriality. Cross-check current/accepted versions versus historically stronger but nonadopted functions.
Deliver: rationale for chosen current spine, competing/overlapping plans crosswalk, explicit currentness/uncertainty, not a replacement of valid inherited plans.

### I-C. Write the entire rough roadmap (before exhaustive anchoring)
Populate all major domains from governed 35-source inventory and scientific semantics, C11/Route B/automatic F1–F4, learned-world, Field Forge, F6/F7, objective PRE-V3, N9/N10E/N10W/F8, N11/N12 V3 gate. Decompose into real major subsections and expected interfaces with exact inherited IDs and citations. At this stage **rough whole-machine coverage matters more than perfect local detail**; tag edges `PLANNED_OR_UNCHECKED` where their current implementation is not yet established.
Deliver: navigable table of contents, major section pages, subsection headings, preliminary edge inventory and missing-organ list. A section may say “existence/consumer unknown”; it must not simply vanish.

**Cycle I exit:** an unfamiliar agent can navigate the complete intended source-to-gate architecture from major program to meaningful subsection without hunting through multiple incompatible plan trees. The GitHub asset inventory exists separately for later precise attachment. If this is not true, do not declare an assembled spine.

## Cycle II — attach all found assets, exhaust accessible sources, close *specific* missing-source requests
### II-A. Anchor every known GitHub asset to the spine
For each plan/section/function, attach actual current code symbols, historically stronger alternate implementations (with retained specific useful functionality), original vision/planning versions, tests/reviews/negative receipts, source/authority docs, first consumer links and any identified branch/version. An asset can belong to multiple components. If its place is ambiguous, show candidate memberships and retain it in an unplaced register. Do not silently infer semantics or label-based aliases.

Start with W1-A–G's 656 architecture records / 623 distinct component IDs, 28 current realization rows, 37 seam rows, 35 source rows, 22 HQ/currentness rows, 29 selected historical variants and F's graph contract; W1-H already reconciles 1,048 raw return rows with 12 cross-lane adjudications, but 164 assertions lack grounded stable joins. These are baseline inputs **not a complete code census**.

### II-B. Library only after GitHub-first coverage
Browse relevant `/Rawlsing/` folders (including `PYAT HQ`, `FIELD_FORGE_R2`, `DDM_HANDOFFS`, `Evidence`, source-authority and orientation material) and other specifically referenced Library items. Index Library documents by stable identifier/name/date and match to spine. Prefer exact comparable content to duplicate stale transcript dumps. Preserve unique vision and code references.
Deliver: library delta of *additional* relevant sources, duplicates/copies and gap candidates.

### II-C. Request mainMac retrieval only where evidence justifies it
For each apparently missing asset, record: exact citation in Git/Library that indicates it existed; expected filename/path/branch/archive/role if known; why material to a named function; what Git and Library checks ruled out; which local repository/archive/directories to search; expected return format and minimal code/hash proof. Request one bounded source-finding local worker batch for these *named* assets, not “search every drive for everything.” If no credible missing local evidence remains, explicitly skip the local cycle.

Deliver: referenced assets anchored; list of genuine unresolved/missing physical assets and specific retrieval instructions; no default assumption that every old branch/file needs to be restored.

**Cycle II exit:** every known material asset from these sources is linked to a named function/plan OR accounted for in an explicit exceptions register. Historical-only useful functions are visible beside current code even when their old implementations will never be reused. No demand to eliminate honest UNKNOWN.

## Cycle III — completion, prereqs and seams; final usability court; DONE
### III-A. Completion sweep by major organ and nested function
For each component determine: intended behavior and proof, latest current integrated code vs candidate/historical alternative, missing functionality, architectural specification state, test/review and source/authority grade, first actual downstream consumer. Do not mark a full system green because a sourcefree unit test passed. Preserve any old method that current code has not fully reexpressed.

### III-B. Dependency/connection sweep
Document “**to implement X, prerequisite Y must exist**” and, where warranted, Y's own missing Z. Mark mandatory vs conditional vs one-of-several, with input/output or owner scope. For every significant adjacent/interacting system record **each seam's state** (working at exact scope, partial, incompatible, absent, held by method/authority, or unknown), supporting source, and specific repair/qualification required. Draw only justified, source-backed edges; all unverified prospective edges are labeled proposed, never green.
Deliver: nested roadmap and functional prerequisite map, seam board, actual gaps/underdeveloped items, no unsupported completion percentage.

### III-C. Practical stranger-agent check, correct and stop
Give a fresh competent Pyat agent substantive development questions: locate complete C11/Route B implementation and outstanding original35 U/Epre seam; best Field Forge/F6/F7 historical vs current methods and missing consumers; explain N9/N10W and N11/V3 conditional requirements; navigate Dva/Trii/Chetiri/Long Memory reuse; trace any X→Y→Z prerequisite both ways. Have the agent follow the actual linked files and read the actual code/spec, rather than merely accept the roadmap author's conclusion. Fix concrete wrong/missing links or dependency claims. Publish a concise README/entry point, exact coverage and exceptions, and retire PROG5 *construction*.
**Cycle III exit:** guide works for real next Pyat tasks; prominent coverage known; no known unaccounted material assets, or precisely named unresolved ones; major edges and missing work visible. Stop improving the guide on abstract perfection grounds.

## Work priority and minimal organization
1. **Highest:** whole-machine scope and best current spine. Missing a major organ is worse than an imperfect local status.
2. **Next:** full, verifiable asset anchoring, especially historical functionality current code lacks and likely source/consumer losses.
3. **Then:** precise completion and prerequisite/edge states, highest-impact missing connections.
4. **Only if justified:** source-specific Library or mainMac retrieval where an indexed document indicates a concrete gap.
5. **Finally:** a short independent agent-usage check and corrections.

Reuse W1-H's working reference as a convenience, but do not spend a cycle designing another graph schema, database, CI court, scheduler or UI. Astra already has a self-contained static navigator; basic Markdown + links is acceptable. Work can be done by a few long, productive commissions; split only when source breadth demonstrably requires independent parallel coverage. The user explicitly chooses model/editor/harness. No commission launch is implied by this plan.

## Revision and maintenance after DONE
A later Pyat worker should append/update the few affected assets, component states, prerequisite links, and seam state as part of its normal return. Cross-link actual new code SHA, reviewer and consumer; no automatic watch loop or new central controller. Escalate to reopening the guide only for a demonstrated missing major area or repeatedly unanswerable developer question.

## Anti-inflation and acceptance
No planning a planning system, no ontology grand redesign, no endless extra audits, no default source-native execution, no 845-branch recensus, no graph database, no continuous ingest automation, no demand for full historical archival reading when proven inventories suffice, and **no delay of legitimate ongoing Pyat engine development waiting on this roadmap**.
Reference: [product spec](01_PROG5_PRODUCT_SPEC.md); [provisional spine](04_PROG5_ROUGH_SPINE.md); [estate/status](03_PROG5_EXISTING_WORK_AND_SOURCE_QUEUE.md).
