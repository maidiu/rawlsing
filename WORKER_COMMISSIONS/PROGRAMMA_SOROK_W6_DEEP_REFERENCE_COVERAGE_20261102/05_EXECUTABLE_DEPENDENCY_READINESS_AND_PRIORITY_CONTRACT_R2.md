# W6-R2 — EXECUTABLE DEPENDENCY, READINESS, PRIORITY AND JOINT-WORK CONTRACT
**User clarification (2026-11-02): priority is not merely tracing relationships but using grounded prerequisite facts to determine WHAT CAN/MUST BE WORKED ON NEXT, WHY, and WHICH ITEMS MUST BE TACKLED TOGETHER.** This supersedes any W6-R1 framing that stops at describing a graph or listing its edges.

## Desired end-to-end answer

Given a sought outcome or missing component X, the guide should answer:

1. In order to **KNOW / SPECIFY** X correctly, what exact evidence, science decisions, architecture decisions, authoritative sources, product choices or interface contracts Y/Z are prerequisites, and which are completed?
2. In order to **BUILD** X, what existing capabilities, permissioned sources, upstream artifacts/interfaces and implementation prerequisites are required?
3. In order to **INTEGRATE / VERIFY / ACCEPT** X at the claimed scope, what downstream consumers, contracts, reproducible tests, independent reviews, source-owner grants and human-product evidence are required?
4. Recurse through every unsatisfied *material* prerequisite to reach an **already qualified completion witness**, a **concrete actionable work leaf**, an **owner-held decision**, or a **precisely identified unknown source**. Do not leave a generic noun such as "C9 science" as a terminal node if the source can identify the actual Rule A/Rule T decision and receiving code/owner.
5. Reverse the paths to identify what finishing each currently incomplete leaf actually makes possible, which other gates remain unsatisfied, and whether it would unlock one or several important terminal objectives.
6. Derive a practical **WORK-NOW view**: which work packages are unblocked and runnable; which are ready for *specification* but not implementation; which are held by owner/science; which require another result or alternative choice; and which form genuine mutually dependent co-design packages. Show WHY the recommended order exists.

**Automatic discernment** means the status and ordering can be reproducibly derived from simple linked records; it does not mean automated dispatch, invented authority, a graph server, a UI, or an autonomous project manager.

## Distinguish what must exist from what is merely related

Each prerequisite is a requirement for a **target component at a specified phase/evidence grade**, not an undifferentiated arrow between two general SP sections. Distinguish:

- `NEED_TO_KNOW`: X cannot be validly *specified/understood* until evidence/science/owner determination Y is complete. **This may be a legitimate first actionable research/decision work item**.
- `NEED_TO_BUILD`: implementation of X requires an actual specified, typed, available artifact/decision/function Y. Do not require fully built downstream product just to begin sourcefree design.
- `NEED_TO_INTEGRATE`: producer/consumer, schema, identity/root, permission, cold/persistence or compatibility must align; a "named consumer" is not an actual import.
- `NEED_TO_VERIFY`: scope-limited test witness, independent review, owner approval or native/human acceptance necessary for a specific claim. An author test or sourcefree PASS is insufficient for another grade.
- `UNLOCKS`: derived reverse outcome from qualifying a predecessor; never claim it makes the whole downstream component DONE when other predecessors remain.
- `CONTEXT_ONLY`, `CONTAINS`, `SUPERSEDES`: navigation/provenance, explicitly NOT blockages.
- Logical group `ALL_OF` for genuine AND requirements, `ANY_OF` for legitimate alternatives and `IF` for an explicit predicate/claim scope; one valid ANY alternative can suffice for that group without satisfying unrelated ALL requirements. A choice requiring owner consent remains OWNER_HELD until granted.

A target can be READY_TO_SPECIFY while BLOCKED_TO_BUILD; BUILD_IMPLEMENTED at sourcefree grade while BLOCKED_TO_NATIVE_INTEGRATE; REVIEWED_SCOPED while NOT_HUMAN_ACCEPTED. **There is no unqualified global DONE flag**. Keep separate `REPORTED`, `DIRECT_SOURCE_INSPECTED`, `AUTHOR_TESTED`, `INDEPENDENT_REVIEWED`, `OWNER_ADOPTED`, `NATIVE_VERIFIED`, `HUMAN_VALIDATED` claims.

## Minimal common record form — use existing 06–13 IDs and simple structured files

Represent an item as a stable original identifier when possible, otherwise a bounded `LOCAL_GUIDE` suffix under the original component, with:
- `target_id`, `stage` (KNOW / SPECIFY / BUILD / INTEGRATE / VERIFY / ACCEPT), `claim_scope`, `owner`, `status_at_cut`, `exact_completion_witness_or_none`, `source_cut`, `required_action`, `downstream_objectives`.
- `gate_id`, `target_id@stage`, `logic` ALL_OF/ANY_OF/IF, `predicate` if relevant, `member_requirements` (each stable `source_id@required_stage`), `source_claim` (immutable commit/path/section/line where possible), `evidence_grade`, `unknown_or_owner_hold`.
- A seam/consumer work item references its `producer`, typed output/contract/schema/root, exact actual `consumer` (or NONE_VERIFIED), accepted/reported tests, failure/version scope, and the `gate_id` it satisfies or blocks.
- A `work_package` references its affected item IDs, expected concrete deliverable, acceptance/test/owner proof, prerequisite gates, choice of alternatives where needed, and reverse unlocks. No new permanent ticket manager.

Keep existing W3 `D-C*` and `E001–E022` unchanged as **parent anchors**, with deeply typed linked *child* records where justified. Do not create another independent canonical graph; these are candidate additions to existing 08/09 and section pages, potentially JSONL generated from common entries.

## Deterministic work-now derivation

Given a chosen terminal outcome T or selected program/workstream scope:
1. Trace its referenced prerequisite groups through every material unsatisfied predecessor, honoring AND/ANY/IF. A prerequisite counts as satisfied ONLY at the explicitly required stage, permission and accepted evidence grade.
2. Mark `SATISFIED_AT_SCOPED_CUT` on proven leaves; `UNSATISFIED`, `OWNER_HELD`, `SOURCE_UNKNOWN`, `CONTESTED` or `ALTERNATIVE_DECISION_REQUIRED` elsewhere. Unknown is NOT green.
3. The first unsatisfied leaf that has all *its* own valid prerequisites satisfied is `READY_NOW` (or `READY_TO_SPECIFY` if only the knowledge/design phase is runnable). If required source/decision is owner-held, show `OWNER_ACTION_READY` as a separate legitimate work queue, **not** a coder-ready task. If access/currentness is missing, first work is the exact evidence retrieval/decision, not speculative implementation.
4. Compute downstream unlocks from reverse references. `UNLOCKS_NEXT_STAGE` and `UNLOCKS_CONDITIONALLY` must show remaining unmet gates; don't declare a downstream target fully buildable based on just one fulfilled ancestor.
5. Detect directed prerequisite cycles and return the **strongly connected group** / mutual dependency set. A *genuine co-design loop* should yield a single explicit **JOINT_WORK_PACKAGE** with cross-interface contract, participating owners, coordinated deliverables, a provisional shared interface to break execution deadlock, acceptance conditions and what work inside the set can run in parallel. An impossible or unsupported circular prerequisite becomes `DESIGN_CYCLE_NEEDS_RESOLUTION` with a specific architecture/owner decision; never pretend a cycle is resolved merely by grouping it.
6. If there are independent ready leaves, expose them as parallel work with separate owners and proofs. Never serialize them because they share a distant product ancestor.
7. Produce a small source-derived `WORK_NOW`/priority list:
   - terminal objective(s) served and actual blockers removed;
   - whether each package is READY, SPECIFY_FIRST, OWNER_ACTION, JOINT, BLOCKED, or NEEDS_EVIDENCE;
   - number/names of *material* downstream capabilities affected (informative, not an automatic importance score);
   - logical bottleneck/unique predecessor vs one optional variant;
   - existing reusable code/source that can make it cheaper and any actual known cost/time/owner constraints;
   - a plain reasoned priority band/order rather than a fabricated single numeric critical-path or descendant-score rank.
8. Re-evaluate the work-now view whenever a genuine Sorok completion/owner decision changes a prerequisite. No automatic monitoring or dispatch is required; an agent can derive from linked JSONL/Markdown and optionally a tiny static validator/renderer if genuinely helpful.

**A ranked list alone is NOT sufficient.** The dependency and maturity evidence must explain the ordering, expose alternative paths, and permit re-prioritizing under different declared terminal goals. Critical path length cannot be asserted without defensible durations/capacity; differentiate "logical bottleneck" from measured schedule.

## Acceptance questions — must be answered with actual references, not hypothetical nodes

- Given Sorok A5, what *smallest currently executable* work is available toward it? Which requirements remain upstream in C12, S11, S14, S15 and S5; which can proceed separately, and which depend on an owner grant?
- For C12 native, traverse through C10, C9, C8, C4 and C11 and their deeper prerequisites. Distinguish WHAT WE MUST FIRST KNOW (source law/Rule A/Rule T/NO_CHANGE, owner schema) from WHAT WE CAN BUILD NOW (specific sourcefree code or compatibility proof) and what cannot be native claimed.
- For a C9 writer→C12 reader candidate mismatch, what exact version/schema/root/ACK/anchor choices must precede implementation or testing, and is there a joint owner/consumer decision package? Don't label an old candidate mismatch a failing adopted native importer.
- For V3 M29/M25 and nine R6 unwired families, where does already existing source reduce work instead of creating fresh BUILD tasks?
- For S5/S13/S14, what research/normative/privacy/economic SPECIFICATION work is ready despite native C12 blockage, and what operational verification needs that specification?
- For at least one *real, sourced* mutual dependency, can the record identify co-design package and work split? If source evidence does not prove a mutual cycle, state `NO_VERIFIED_CYCLE` rather than inventing one.
- When one leaf becomes independently reviewed or owner-adopted, can a second agent update that exact leaf and reproducibly change the next ready work without rebuilding the map?
- Can an unfamiliar agent name the **most consequential feasible next work** for a declared goal, identify independent parallel opportunities and expose uncertainty, using no broad reread of all historical Sorok sources?

## Cross-worker duties

**W6-A** must make source/asset dispositions useful as *evidence that a prerequisite or completed function ALREADY EXISTS*: cite exact item IDs and proven completion grades; identify candidate missing scientific/owner receipts rather than only attaching assets to sections.

**W6-B** is accountable for the typed **knowledge/build/integrate/verify dependency hierarchy**, logically derived ready/blocked/joint packages, and a defensible work-now prioritization view. W6-B must not merely return more AND/OR prose chains.

**W6-C** is accountable for binding those dependencies to real producer→artifact→consumer seam witnesses, required missing consumers, actual current version/compatibility, acceptance and the *specific gate* each contract blocks/unlocks.

**Future fan-in** must merge all three into existing PROGRAMMA 06–13 so an agent can ask "what should we work on?" and get an evidence-derived answer. Preserve W4/W5 limited PASS and original owner/source boundaries; test new non-W4 examples and an actual readiness/priority recomputation.

**Guardrail:** maximum evidence-grounded execution utility, not a maximal graph database. Use simple records and clear referenced text; no autonomous workflow product, new controller, repeated W1 fleet or false DONE promotion.
