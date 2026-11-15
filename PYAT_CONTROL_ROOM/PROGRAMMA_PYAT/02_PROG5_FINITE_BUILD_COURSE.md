# PROG5 — FINITE CONSTRUCTION COURSE AND PRIORITIES
**Course agreed 2026-11-02.** Scope is the roadmap *about* Pyat, not engineering the Pyat engine. Read [the product contract](01_PROG5_PRODUCT_SPEC.md) and [existing estate](03_PROG5_EXISTING_WORK_AND_SOURCE_QUEUE.md).

## The fixed order of work
**GitHub-wide source reconnaissance + latest vision → first complete rough source-to-V3-gate spine → anchor and reconcile GitHub assets → complete the GitHub-based development-state/dependency/seam sweep → THEN (only if useful) targeted Library supplementation → THEN (only if evidence warrants) named mainMac retrieval → final practical usability/correction → stop.**

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

## Cycle II — attach and reconcile GitHub assets against the complete rough spine
### II-A. Anchor every known GitHub asset to the spine
For each plan/section/function, attach actual current code symbols, historically stronger alternate implementations (with retained specific useful functionality), original vision/planning versions, tests/reviews/negative receipts, source/authority docs, first consumer links and any identified branch/version. An asset can belong to multiple components. If its place is ambiguous, show candidate memberships and retain it in an unplaced register. Do not silently infer semantics or label-based aliases.

Start with W1-A–G's 656 architecture records / 623 distinct component IDs, 28 current realization rows, 37 seam rows, 35 source rows, 22 HQ/currentness rows, 29 selected historical variants and F's graph contract; W1-H already reconciles 1,048 raw return rows with 12 cross-lane adjudications, but 164 assertions lack grounded stable joins. These are baseline inputs **not a complete code census**.

### II-B. Close the GitHub asset-to-component attachment
Follow references from each inspected asset into the first complete spine; reconcile versions/aliases, old functions not matched by current code, reviews and first consumers. Retain explicit UNPLACED/UNVERIFIED evidence items. Do not use the absence of a Library copy as an excuse to defer a GitHub component whose code and spec are already accessible.

**Cycle II exit:** all materially relevant GitHub assets in scope are linked to a named function/plan OR accounted for in an explicit GitHub exceptions register. Historical-only useful functions are visible beside current code even when their old implementations will never be reused. Library and mainMac remain intentionally deferred; their absence is not a blocker to a complete GitHub-based roadmap.

## Cycle III — complete the GitHub-based development-state, prerequisite and seam sweep
### III-A. Completion sweep by major organ and nested function
For each component determine: intended behavior and proof, latest current integrated code vs candidate/historical alternative, missing functionality, architectural specification state, test/review and source/authority grade, first actual downstream consumer. Do not mark a full system green because a sourcefree unit test passed. Preserve any old method that current code has not fully reexpressed.

### III-B. Dependency/connection sweep
Document “**to implement X, prerequisite Y must exist**” and, where warranted, Y's own missing Z. Mark mandatory vs conditional vs one-of-several, with input/output or owner scope. For every significant adjacent/interacting system record **each seam's state** (working at exact scope, partial, incompatible, absent, held by method/authority, or unknown), supporting source, and specific repair/qualification required. Draw only justified, source-backed edges; all unverified prospective edges are labeled proposed, never green.
Deliver: nested roadmap and functional prerequisite map, seam board, actual gaps/underdeveloped items, no unsupported completion percentage.

### III-C. Finish the GitHub roadmap before broadening sources
Write the actual whole/section/subsection overviews, current and historical code/state, prerequisite chains and seam board, linked to their exact GitHub source identities. Perform a bounded GitHub-only navigation check: C11/Route B, original35 U/Epre, Field Forge/F6/F7, N9/N10W/N11/V3, Dva/Trii/Chetiri/Long Memory and a real X→Y→Z requirement. Correct concrete omissions. List only *evidence-backed* Library/mainMac candidates; do not begin those searches in this cycle.

**Cycle III exit:** an agent can navigate a largely complete, useful Pyat roadmap using GitHub alone; major parts and seams are present and the remaining GitHub uncertainties are explicit. The roadmap must not defer its own completion until Library or local work. Library/local is an optional late supplement, not the default next phase.

## Optional late supplement — ONLY AFTER Cycles I–III are substantially complete
**Library delta:** inspect referenced /Rawlsing/ collections ONLY when a GitHub document, unanchored function or unresolved design/implementation discrepancy gives a concrete reason. Index stable Library identifiers and unique assets; skip redundant transcript dumps and do not repeat GitHub history.
**mainMac targeted retrieval:** if GitHub and any warranted Library lookups still point to named missing material, issue a short retrieval ledger: `GAP_ID | component | exact referring document | expected asset | GitHub/Library exclusion | material relevance | proposed narrow local search`. Ask user to select local Codex/OpenCode agent for those specific searches only. No general hard-drive trawling.
**Final usability closeout:** read a representative set of component/asset/seam/prerequisite entries, correct any newly proven gap, publish the guide and stop. If optional sources add nothing material, do not run a new cycle.

## Work priority and minimal organization
1. **Highest:** whole-machine scope and best current spine. Missing a major organ is worse than an imperfect local status.
2. **Next:** full, verifiable asset anchoring, especially historical functionality current code lacks and likely source/consumer losses.
3. **Then:** precise completion and prerequisite/edge states, highest-impact missing connections.
4. **Only AFTER the GitHub-based guide is substantially complete, if justified:** narrowly referenced Library or mainMac retrieval.
5. **Finally:** a short practical agent-usage check and corrections.

Reuse W1-H's working reference as a convenience, but do not spend a cycle designing another graph schema, database, CI court, scheduler or UI. Astra already has a self-contained static navigator; basic Markdown + links is acceptable. A few productive GitHub-only commissions may run in parallel by distinct source territory, followed by one roadmap builder. The user explicitly chooses model/editor/harness. No commission launch is implied by this plan.

## Revision and maintenance after DONE
A later Pyat worker should append/update the few affected assets, component states, prerequisite links, and seam state as part of its normal return. Cross-link actual new code SHA, reviewer and consumer; no automatic watch loop or new central controller. Escalate to reopening the guide only for a demonstrated missing major area or repeatedly unanswerable developer question.

## Anti-inflation and acceptance
No planning a planning system, no ontology grand redesign, no endless extra audits, no default source-native execution, no 845-branch recensus, no graph database, no continuous ingest automation, no demand for full historical archival reading when proven inventories suffice, and **no delay of legitimate ongoing Pyat engine development waiting on this roadmap**.
Reference: [product spec](01_PROG5_PRODUCT_SPEC.md); [provisional spine](04_PROG5_ROUGH_SPINE.md); [estate/status](03_PROG5_EXISTING_WORK_AND_SOURCE_QUEUE.md).
