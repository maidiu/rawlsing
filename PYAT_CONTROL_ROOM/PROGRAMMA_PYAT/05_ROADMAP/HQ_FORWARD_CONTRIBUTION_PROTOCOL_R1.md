# PYAT HQ — permanent direct maintenance of PROGRAMMA PYAT as the machine develops

**Corrected operational specification, 2026-11-03.** Supersedes the earlier proposal for a standalone “forward note” plus temporary PROGRAMMA receiver. PROGRAMMA is intended to become the live development representation used and **maintained directly by the appointed PYAT HQ**, after its finite construction phase and during all subsequent substantive Pyat work. The G1–G4/post-G4 record is the starting estate; **its component/seam grades are historical source-cut assessments**, not immutable statements about what Pyat will become.

This editorial-maintenance duty does not grant new original35 science, native data, N11/N12, Sorok actor rights, privileged code paths or protected merges. It operates under the existing HQ checkpoint/authority/decision protocols, not beside them.

## 1. The actual permanent responsibility

In each materially productive HQ cycle, two distinct representations must be advanced **together**:

**HQ operative authority and history**: worker return/reviewer/candidate/decision, code branch/commit, paired `PYAT_CONTROL_ROOM/CURRENT_PROGRESS.md/.json`, existing `HQ_HANDOFF` checkpoint when the operative state materially changes, and the existing append-only decision ledger where applicable. These establish what HQ **did, reviewed and lawfully adopted**.

**PROGRAMMA PYAT current map**: the existing `PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/05_ROADMAP/` sections, `COMPONENT_STATUS.jsonl` (62 guide organs/children), `CURRENT_SEAM_STATES.jsonl` (82 typed initial interfaces), `REMAINING_REAL_PYAT_WORK.md` (original GAP IDs plus additions), `FUNCTION_PARITY.jsonl`, `ASSET_LOCATOR.md`, `PREREQUISITES_AND_UNLOCKS.md` and `README.md`. These must reflect what Pyat **now possesses, actually connects, has accepted at which scope, and still needs**. They are not a second HQ progress board or authorization register.

**The same incumbent HQ owns both responsibilities. No separate “PROGRAMMA receiver” is required, permanently or after completion.** HQ may delegate factual source investigation and mechanical documentation edits, but cannot delegate its judgment of actual progress, owner/adoption/science status, cross-organ dependencies or truthful program-wide completion.

## 2. Coherent material transition: required direct write-through

On a coherent material change—**new function/code, recovered previous implementation, qualified test/review, genuine first reader/consumer, implementation or source-rights decision, accepted/adopted repair, incompatibility, refusal/negative, changed prerequisite or retired gap**—perform these steps as **part of closing that HQ transition**, not as an overnight-only handback:

1. **Identify affected PROGRAMMA coordinates.** Resolve `ROADMAP:Sxx` and child `ROADMAP:Sxx.y`, exact original `edge_id` and any `GAP-xxx`, historical `obligation_id`. If an actually new function has no existing ID, allocate a new typed identity linked to its parent, without renumbering the 782 original identities or inventing an alias.
2. **Append the evidence-linked transition** to `05_ROADMAP/HQ_DEVELOPMENT_TRANSITIONS.jsonl` (create on first real transition). This file is a thin append-only history of direct HQ actions **in PROGRAMMA**; it is not an approval ledger, scheduler or independent source authority. See minimum row below.
3. **Update the current affected representation, not merely the journal**:
   - **Component development** → affected records in `COMPONENT_STATUS.jsonl` and the relevant Sxx section page.
   - **Real producer → reader connection** → affected `CURRENT_SEAM_STATES.jsonl` record and neighboring section pages; `PLANNED_INTERFACES.jsonl` original MUST/IF/ALTERNATE requirements retain their intended authority unless competent architecture decision changes them.
   - **Function reused/new parity** → `FUNCTION_PARITY.jsonl` or a source-linked additive record, and `ASSET_LOCATOR.md`.
   - **Dependency unblocked or gap truly closed/changed** → `REMAINING_REAL_PYAT_WORK.md`, `PREREQUISITES_AND_UNLOCKS.md`, and affected section. Never simply delete a historical GAP or negative; append a dated later disposition referencing the exact old ID.
   - **Whole-course effect** → short `README.md` current-state/priority adjustment (not one paragraph for every test). State whether it changes actual source→V3 trajectory, else why the prerequisite matters.
4. **Publish the documentary changes on the incumbent HQ's authorized Git branch/PR within the same coherent transition.** Use existing owner review/CAS rules for protected destinations. When source-engineering and guide changes require separate branches, HQ carries out the guide update through its **own authorized documentation branch and ordinary Git integration**, preserving both exact commits. The update is not counted as current PROGRAMMA until its actual guide branch/approved target includes it. Keep pending documentation edits explicit instead of falsely claiming synchronization.
5. **Link both directions.** The ordinary HQ progress/motion/checkpoint cites the PROGRAMMA transition ID and guide commit; that transition cites the exact HQ motion/decision/reviewer/code source. On next HQ grok, reconcile these pointers if a prior guide update remained pending. Then choose the next productive work.

**No intermediary agent performs this transfer. It is the appointed HQ's persistent editorial obligation.**

## 3. Minimal transition record (example shape, not a new giant schema)

Each `HQ_DEVELOPMENT_TRANSITIONS.jsonl` line may use this stable small JSON object:

```json
{
  "transition_id": "PYAT-HQ-<existing-motion-or-return-id>",
  "observed_at_utc": "<actual ISO timestamp>",
  "kind": "IMPLEMENTATION|REVIEW|CONSUMER|ADOPTION|SCIENCE_AUTHORITY|NEGATIVE|RECOVERY|PREREQUISITE",
  "program_ids": ["ROADMAP:S05.2"],
  "edge_ids": ["<existing edge_id if applicable>"],
  "gap_ids": ["GAP-021"],
  "hq_motion_ref": "<exact existing HQ Git path@SHA>",
  "code_refs": [{"ref": "<commit>", "path": "<code path>", "symbol": "<actual function>"}],
  "review_ref": "<review Git ref or null>",
  "before": {"implementation": "SOURCEFREE_CANDIDATE", "consumer": "UNVERIFIED"},
  "after": {"implementation": "REVIEWED_SCOPED", "consumer": "REAL_FIRST_READER_AT_SOURCEFREE_SCOPE"},
  "authority_and_source_scope": "NO_ORIGINAL35_NATIVE_CLAIM; NO_PROTECTED_ADOPTION",
  "first_consumer": "<specific importing/calling function or NONE VERIFIED>",
  "remaining_dependency": "<exact smallest next missing piece and owner>",
  "guide_update": "SAME_COMMIT_FILE_CHANGE_OR_PENDING_AUTHORIZED_MERGE",
  "evidence_level": "DIRECT_CODE_AND_SCOPED_INDEPENDENT_REVIEW"
}
```

Use **actual** IDs and fields; this placeholder is not a claim that such an event occurred. Do not attempt to record the SHA of the commit currently being created inside that same commit; the SHA is subsequently available from Git history and can be cited by the next authorized HQ checkpoint. A transition with no materially changed behavior, reader, authority, adoption, source fact, or prerequisites needs no new row. No per-test/per-file/progress-tick spam.

## 4. Update the existing source-cut assessments without falsifying history

The G4 `COMPONENT_STATUS.jsonl` and `CURRENT_SEAM_STATES.jsonl` were authored from the G2/G3 historical evidence cuts. Their `source_identity`, `original_G2`, review references, old `current.status` and old negative findings **must stay referentially identifiable as judgments at those cuts**. Do not change 2026-11-02 source grades into retroactive 2026-11-03 successes.

For an affected record, add or advance a `latest_hq_observation` / `latest_scope_state` member containing **actual newer motion/commit, scope-specific implementation/review/adoption/native/first-reader status, remaining gap, and recorded date**. The inherited G4 status becomes `baseline_at_original_cut`, not false current truth. The append-only transition ledger retains the sequence. If no newer observation exists, continue to display the pinned source cut and its limits. An unmerged sourcefree candidate can be a positive **branch-candidate** while still not an adopted PRE-MAIN operation.

The 82 initial edge IDs and 62 initial guide component/child IDs remain stable; add justified new IDs when Pyat develops a real new component rather than concealing it. Preserve conditional and alternate edges and independent science/authority classifications. Recompute any summary from these scoped records; never infer a global readiness percentage from counts of files, tests or current guide pages.

## 5. What “Pyat coming up to completion” looks like in PROGRAMMA

For every function/organ/first-consumer edge, readers should see distinct evidence-backed dimensions:
- **Required function**: original product goal, scientific meaning and earliest prerequisite.
- **Existing implementation**: historical, current integrated, active branch-only, partial, absent at specified cut or unknown.
- **Working functional scope**: sourcefree fixture, selected actual first consumer, original native source-qualified operation, or no proof.
- **Independent judgment**: author test vs reviewer scoped PASS/REVISE/HOLD vs adoption at exact cut.
- **Authority/science**: permitted source, current owner and separately held/unissued decisions.
- **Next action**: the smallest build/reuse/connect/qualify/issuer step, and the downstream work it would unlock.

Thus a real improvement visibly changes `S05 child: reviewer accepted sourcefree M1→M2→B5` or `S10 edge: selected sourcefree first reader now proved` while leaving the original measured N9/N10W/N11 native gates held if not independently established. The guide answers **what is finished at which exact scope, what is still missing, and what advancing it buys**. That, not a decorative percentage bar, is the intended live completion picture.

## 6. Working safely during and after finite PROGRAMMA construction

**While SAT-M1–M5 and SAT-R or any other guide-construction agent is active:** Codex HQ continues its authorized engineering and produces **its own direct PROGRAMMA patch/transition record on a disjoint authorized HQ documentation branch**, not on the active worker's files. The HQ owns that patch; it is not entrusted to a “receiving worker.” At the next authorized guide update/merge, HQ itself reconciles exact commits with any concurrent guide edits and publishes its current state. Mark the guide target as pending until the actual merge. Never interrupt other workers.

**After PROGRAMMA's finite initial construction is done:** the incumbent Pyat HQ becomes the **ordinary, permanent maintainer** of its PROGRAMMA guide through authorized Git writes. There is no special receiving phase and no third management system. The same rules continue for months of work. If HQ succeeds in engineering but leaves the guide stale, that productive HQ cycle is **not fully documented** until the affected PROGRAMMA records are updated (without retroactively denying the engineering achievement). If guide state is pending because of an actual owner/protected merge restriction, state that plainly and reconcile on the next authorized custody opportunity.

**On every HQ resumption:** read authoritative checkpoint, current paired progress, and the guide's latest committed state and newest `HQ_DEVELOPMENT_TRANSITIONS.jsonl` entries; reconcile exact changes not yet reflected on either side. Never default to the original G4 evidence cut as if no later code exists.

## 7. Required correction to the overnight Codex Pyat HQ goal

> **BINDING PROGRAMMA LIVE-MAINTENANCE ADDENDUM.** As the appointed Pyat HQ, you are responsible for keeping PROGRAMMA PYAT **directly up to date** as you build, recover, connect, test, adjudicate and integrate Pyat. After each coherent material development transition, append an exact source-backed row to `PROGRAMMA_PYAT/05_ROADMAP/HQ_DEVELOPMENT_TRANSITIONS.jsonl`, and in the **same authorized documentary commit or associated HQ guide patch** update the affected `COMPONENT_STATUS.jsonl`, `CURRENT_SEAM_STATES.jsonl`, relevant Sxx page, original GAP disposition/dependency, and README where the whole-machine next step changes. Crosslink to the actual code/review/HQ decision cuts and preserve former states and scientific/source ceilings. Make a genuine current developer view, not merely a closing handoff note. Use ordinary protected owner/CAS rules for merges and existing checkpoint maintenance; do not claim the guide current until its update is actually published. You yourself maintain PROGRAMMA: **do not assign this to an imagined PROGRAMMA receiving worker or a new HQ.** When PROGRAMMA's initial construction is done, this becomes your normal continuing operating responsibility. Work productively in parallel with its current isolated workers without editing their active branches; retain any pending guide patch on your own authorized branch and reconcile it on actual authorized publication. No per-test bookkeeping, extra CI/daemon or scientific/actor/source rights implied.
