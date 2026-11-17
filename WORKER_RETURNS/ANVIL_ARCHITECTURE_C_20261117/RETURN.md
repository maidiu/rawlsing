# RETURN — distinct independent C on the frozen ANVIL architecture candidate

**Status:** `REVISE_EXACT_DEFECT`.
**Direction assessment:** the *conditional direction* is source-grounded and
conditionally competent; the *frozen package* is not coherent enough to accept
as-is. The defects are exact documentary/ABI defects, not a demand for native,
100k, original35 or production evidence.
**Candidate:** `98b8d261accfcc7834c86d3f0d52f23e4524f666`.
**Annotated tag:** `anvil-architecture-candidate-20261117-r1` = tag object
`ad73064f7a7fece32030075188d15dea84004c72`, peeling to `98b8d261…`.
**Branch:** `agent/anvil-architecture-independent-c-20261117-r1` at startup
`98b8d261…`. **Write scope:** `WORKER_RETURNS/ANVIL_ARCHITECTURE_C_20261117/`
only. **Product/protected scope:** read-only; no product edit, no schema or
evaluator change, no raw respondent read, no install, no native/100k benchmark,
no protected merge, no H1.

## 1. What was actually read and checked

- Protected currentness: canonical first-position OATH and full PROGRAMMA
  entrypoint at exact protected commit
  `31291d08179890852246c8742700e055168e9933` (PYAT CURRENT_PROGRESS rev10).
  The local protected snapshot
  `/Users/matthewsmith/Desktop/ANVIL_RABOCHII_EXECUTION_20261117/evidence/protected`
  was treated as a source-time snapshot, not promoted to live.
- Candidate: entire `RETURN.md`, `S1/S1_COMMON_FRAME.md`, `S1/FRAME.json`,
  `S1/FRAME_V2_ADDENDUM.json`, `S2_S3/FINAL_ARCHITECTURE.md`,
  `FINAL_DECISION.json`, `FINAL_OBLIGATION_CROSSWALK.tsv`,
  `SPECIALIST_ADJUDICATION.md`, resource/builder cards, guards, witness logs,
  and the 61-file manifest. Old provisional files were read only as preserved
  history.
- Both full specialist returns at exact commits:
  construction `f8c98027599b62069c03a269989075b4442f5138`;
  query `a5ea7fd9c6d8fdb4ba43d839bff900df4b60d89a`.
- Product code at `cea2d4d3009e9087d2267e9d1f53bec28b730dc7` and the actual
  first-consumer/prepared-session/Batch/writer symbols (exact pins in
  `SOURCE_CHECKS.tsv`).
- Source inventory and originals at exact pins: 118 mixed identities,
  `29 K1_CAP + 26 PYAT_PC + 14 P4R + 10 SEAM_B + 8 SEAM_S + 8 ANVIL_L +
  7 BOUNDARY + 16 TERMINAL`; 26 NOT_ADOPTED, 14 P4R held/pending; separate
  52/24/21 estate navigation-only; F26 exact hold. Original ZIP byte authority
  `526d835d64a98c886a8cbb159fb39f06af7c287ebe1029a93fbbfc9131072332`.
  Sourcebank `8523007…` was not used as byte authority.

Independent checks passed: tag/ref/remote identity; 61/61 manifest hashes;
base frame `44b17c…` / canonical digest `7e7bfb…`; v2 addendum
`aa170d89…`; product cut and protected head exact; product worktree clean
outside this review root; focused sourcefree tests 34 passed (3 prepared + 7
direct-estate + 24 saved-native first-consumer); structural guard 16/16 and
118/118. Those are sourcefree/structural grades only, not native/science/H1.

## 2. Verdict and blocking defects

### D1 — The final decision still says the mandatory specialist dependency is PENDING

`S2_S3/FINAL_DECISION.json` contains both:

- `specialist_consumption.status = "BOTH_RETURNS_RECEIVED_AND_ADJUDICATED"`;
- `specialist_dependency.status = "PENDING_TWO_FROZEN_SPECIALIST_RETURNS"`.

It also has `final_selection_frozen = true` while the
`specialist_dependency.adjudication_rule` says the final decision remains
unfrozen until both returns are adjudicated. The final `RETURN.md` and
`SPECIALIST_ADJUDICATION.md` say both are consumed. The frozen decision is
therefore internally contradictory about the very dependency that gates
freezing. `S2_S3/SPECIALIST_CONSUMPTION.md` repeats the stale PENDING status and
unchecked checklist and is included in the package manifest without a
supersession banner.

**Decisive correction:** update the final decision's specialist status to the
actual received/adjudicated state (or rename the old block to an explicitly
historical plan and make `specialist_consumption` controlling), remove or mark
`SPECIALIST_CONSUMPTION.md` as `SUPERSEDED_BY_FINAL`, and ensure the frozen
decision no longer contains a status that says it is not frozen.

### D2 — The final decision still describes the old SC-ESTATE selection, not the selected prepared-session-first design

The selected strategy says: prepared-session-first, conditional
one-journal/one-certificate, recovery repair, durable locator index **held**.
But `FINAL_DECISION.json` still contains, unchanged from the provisional
decision:

- `physical_architecture.name = "Single-certification canonical C11 estate +
  immutable derived access index"`;
- `physical_architecture` layers with `L2_INDEX` and per-row-group digests;
- implementation sequence step 4: "Add immutable derived selector/denominator
  index; prove cold open and 1/10/100 sourcefree reuse…" (unconditional);
- implementation sequence step 2: "Add write_direct_estate_from_certified_stream
  … one I02, no JSONL" (unconditional, although one-certificate is
  conditional);
- per-requirement candidate effects such as `REQ-RESOURCE-ECONOMICS`:
  "SC-ESTATE removes the second I02, … and per-session full scan";
  `REQ-PHYSICAL-WORKLOAD-1-10-100`: "The durable index and prepared session
  target 1/10/100"; `REQ-SOURCE-I02-REVOCATION`: "The index is bound…".

Those statements are not true of the selected design. Prepared-session-first
does **not** remove a fresh session's scan, does **not** remove the second I02
unconditionally, and the durable index is held. The guard passes because it
checks only the 16 base requirements and 118 identities; it does not check that
the final decision's architecture, sequence and per-requirement effects agree
with `single_selected_strategy`.

**Decisive correction:** regenerate the final decision from the final selected
design: either describe `physical_architecture` explicitly as the conditional
target if the durable index is later qualified, or replace it with the selected
prepared-session-first/conditional-construction architecture; make sequence
steps 2 and 4 explicitly conditional on their named gates; update the
per-requirement candidate effects. Re-run the guard and freeze.

### D3 — The v2 addendum is not covered by the 16/16 guard; removing it still PASSES

`S1/FRAME_V2_ADDENDUM.json` adds four PRESENT_HARD/FUTURE requirements:
`REQ-COST-LAYER-DECOMPOSITION`, `REQ-DERIVED-INDEX-BINDING`,
`REQ-EVIDENCE-OUTPUT-EXACT-IDENTITY`, `REQ-CONSTRUCTION-ATOMIC-RECOVERY`.
They are present in `FINAL_OBLIGATION_CROSSWALK.tsv` and in
`candidate_requirement_addendum_dispositions`, but the final guard reports
`covered: 16`, `requirement_total: 16`. I copied the final decision to this
review root, removed the entire v2 addendum block and its four dispositions,
and the unchanged accepted-instrument guard still returned
`PASS_LOCAL_INTEGRATED_DECISION_PENDING_C` with 16/16 and 118/118
(`RUNS/guard_omission_witness.txt`). The 16/16 guard cannot detect omission of
the four new requirements. This is the exact failure mode the mission asks
about: an addendum that is narrated but not guarded.

**Decisive correction:** extend the decision guard (or add a v2 guard) to cover
the 16 base + 4 addendum = 20 requirements, their dispositions, and their
crosswalk rows; record 20/20 and 118/118; then refreeze. The guard must also
check the specialist-dependency/selected-strategy consistency asserted in D1
and D2 so a stale provisional field cannot pass.

### D4 — Prepared-session-first does not fit the named first-consumer/Batch ABI as written

The selected handoff names `PreparedSavedC11Admission.open + prepared_i03` in
`SavedC11Admission.execute_i03` and `execute_saved_batch` per unit, with grade
`EXECUTED_SOURCEFREE_EXISTING_CODE`. The actual code:

- `pre553_saved_workload_integration.py::execute_saved_i03` and
  `execute_saved_i05` reject anything whose exact type is not
  `SavedC11Admission` (lines 42, 54);
- `execute_saved_batch` does the same (line 94);
- `pre553_batch_runner.py::BatchExecutionRunner.__init__` requires
  `type(repository) is SavedC11Admission` when `saved_mode=True` (line 406);
- `SavedC11Admission.execute_i03` delegates to
  `CarrierNeutralResearchExecutor`, which opens a fresh
  `DirectEstateI03Session` per call; `execute_i05` opens a fresh session too.
  Merely passing a `PreparedSavedC11Admission` through the existing wrappers
  therefore does not reuse the prepared session, even if the exact-type guard
  were relaxed.

A bounded witness in this root
(`WITNESS/test_prepared_abi.py`, 2 passed, `RUNS/prepared_abi_witness.txt`)
constructs the real sourcefree prepared admission and asserts that the named
`execute_saved_i03` path raises `SavedC11AdmissionError("exact
SavedC11Admission required")` and the named Batch runner raises
`BatchIntegrityError("repository must be accepted…")`. The direct prepared
3-test log is real, but it is not the named Batch/first-consumer path.

**Decisive correction:** add an explicit prepared-session-aware adapter (or a
narrow owner-approved protocol) and change the exact-type guards for the exact
prepared class; thread one prepared context through Batch units; test one
`_build` through the actual wrapper/Batch with four operations and exact
fact-ref parity. Until then, label the Batch/prepared handoff
`PROPOSED_NOT_WIRED`, not `EXECUTED_SOURCEFREE_EXISTING_CODE`.

### D5 — Preserved provisional artifacts are not unambiguously superseded

`S2_S3/SPECIALIST_CONSUMPTION.md` still says both returns are PENDING and has
unchecked completion boxes; `S2_S3/PROVISIONAL_STATUS.md` still says
`PROVISIONAL_PENDING_TWO_SPECIALIST_RETURNS`; `S2_S3/DECISION_GUARD.txt` is the
provisional guard output. All are inside the final package manifest. File names
`PROVISIONAL_*` help, but `SPECIALIST_CONSUMPTION.md` and the stale guard do not
carry a supersession marker. This is a documentary ambiguity, not a rejection
of preserving history.

**Decisive correction:** keep them, but add an explicit
`SUPERSEDED_BY_FINAL_...` header and keep them out of the final payload unless
the manifest labels them historical; or move them to an `ARCHIVE/` subdirectory
with the final manifest pointing only at final artifacts.

## 3. The strongest attack that failed

**Attack:** “Prepared-session-first merely moves work and silently changes
denominator, occurrence, routing, weight, negative or replay semantics.”

**Result: failed.** `PreparedI03Session.execute_i03` calls the same
`execute_empirical_query` with the same exact query/predicate/authority and
`group_scope=None`; `execute_i05` calls the same
`execute_exact_bounded_discovery`; `_build` is an index of locators, and the
canonical bodies/typed lanes are unchanged. The focused sourcefree run includes
the prepared 3-test file (3 of the 34 passed) and asserts exact fact-ref parity
for selected, F2, F4 and raw queries, one `_build` for four operations,
revocation refusal and condition mismatch refusal. The shared
session changes `S` (one index build) but not `Q`/`O` or the scientific
semantics. The candidate states this honestly, including N=1 neutrality and
fresh-process limitation.

Other attacks that did not become defects:

- **Construction certificate removal is not unconditional.** The final
  architecture gates it on full physical body/lane/selector proof against Q2
  and keeps the second-certificate fallback; the decision's implementation
  sequence is stale (D2), but the direction itself is conditional.
- **Recovery is not falsely claimed.** The candidate says atomic rename may
  clobber, requires a no-clobber claim/lease and typed orphan, and lists
  crash-injection proof as a remaining obligation. It does not claim the
  current target-before-manifest window is fixed.
- **Durable index is held, not declared a universal lower bound.** The 1.30 GB
  SQLite witness is cited as a current artifact, not as a proven minimum; the
  candidate requires a compact exact encoding, measurement and binding gate.
- **H/S/Q/O formulas are separated correctly.** `H+N(S+Q+O)`,
  `H+S+N(Q+O)`, `N(H+S+Q+O)` and `H+I+N(Q+O)` are distinguished; the
  1.69–1.70× four-op author report is not promoted to a 100-op asymptote.
- **The 30–50 MB/fact and 3–5 GB/100-fact evidence estimate is corrected** from
  the query specialist's original 15–25 MB/1.5–2.5 GB; it remains hypothetical.
- **No source→actor, opinion→power, fictional→observed or pairwise→joint edge**
  is introduced; the 13-family body and native evaluators are unchanged, and
  FF02/N9/N10W/SEAM/SOROK remain exact owner holds.
- **No protected adoption/H1 is claimed.** The product cut `cea2d4d` is not
  protected `31291`; the instrument 05e81747/review 21d39dfa/delivery f6073d92
  are preparation-only.

## 4. Whole-frame / new-requirement / specialist / first-consumer / no-loss coverage

| Area | Result |
|---|---|
| 16 base requirements | Present; guard 16/16; frame `44b17c…` |
| 4 v2 addendum requirements | Present in crosswalk and decision dispositions, **not guard-covered** (D3) |
| 118 identities | 118 exactly; 29/26/14/10/8/8/7/16; guard 118/118 |
| 26 PYAT-PC NOT_ADOPTED / 14 P4R held | Preserved; no promotion; SEP-52/24/21 navigation-only |
| F26 | `K1-CAP-24` / `P4R-R02` / `PYAT-PC-R11-21` exact hold |
| Both specialists | Exact SHAs read; construction favors durable index; query favors prepared-session-first; final adjudication is not a majority vote and is represented in `SPECIALIST_ADJUDICATION.md`; the final decision's stale PENDING field is D1 |
| First consumer | Direct prepared sourcefree tests pass; named Batch/first-consumer ABI still needs D4 wiring; NORMAL/resume owner holds remain |
| 13 families / true k≥3 / F2/F3/F4 / F6/F7 / FF01-FF02 / SEAM/SOROK | Body and native evaluators unchanged; downstream readers remain exact holds; no new rights |
| No-loss / replay | Exact fact/refs remain; prepared session adds no retained artifact; evidence set-ref sharing is a contract, not a current claim; cached fact never authoritative |
| Protected vs unmerged | `31291` protected currentness; `cea2d4d` product candidate unmerged; no protected acceptance |

## 5. Finite obligations and owner routing

1. **Integrated architect (same synthesis owner):** correct D1–D3/D5 in
   `FINAL_DECISION.json`, `FINAL_DECISION_GUARD.*`, and the stale provisional
   artifacts; refreeze the corrected candidate. No new campaign, no new
   specialist, no architecture redesign.
2. **S2-D saved admission owner + BatchExecutionRunner owner:** implement the
   prepared-session-aware wrapper/Batch path (D4); exact owner ACK for the
   shared Batch guard; one `_build` through the actual wrapper/Batch; four
   operations exact fact-ref parity; revocation/current refusal.
3. **S2-C/D physical writer owner:** keep the full physical proof and Q2
   certificate condition; implement the private stage/no-clobber claim/lease
   and crash-injection witness; fallback to the second certificate whenever the
   full family/selector proof does not survive.
4. **#1006 measured-cost owner + S04/I03 scientific owner:** H/S/Q/O measurement
   on one authorized real-width workload, 1/10/100 same-process and 10
   fresh-process; do not select the durable index before this.
5. **Competent H1/protected owner:** only after a corrected distinct-C
   acceptance; no protected merge or native/science/actor right from this
   review.

**Exact next coherent implementation handoff:** first refreeze the corrected
documentary package with a 20-requirement guard and consistent selected
strategy; then run the bounded sourcefree `execute_saved_batch` +
`PreparedI03Session` witness (one `_build`, four operations, exact parity,
revocation refusal); only then consider construction/recovery changes. Do not
start with the durable index or a native 100k run.

## 6. Own limits and non-claims

- I did not recensus all 141 crosswalk rows against every source original; I
  read the exact inventory, source pin manifests, K1/P4R samples, and both full
  specialist findings. No source-lineage defect was found in the sampled pins.
- I did not run the full test matrix, native/100k/6 GiB, original35, or a
  crash-injection suite. I ran 34 focused sourcefree tests, 2 bounded ABI
  witnesses and the structural guard.
- The ABI witness proves exact-type rejection; it does not prove a correctly
  wired prepared Batch path would fail.
- I did not authenticate the accepted instrument or its reviewer content; I
  treat 05e81747/21d39dfa/f6073d92 as preparation-only per mission.
- I did not independently verify the sourcebank `8523007…` two-hash caveat; I
  used the original ZIP `526d…` and the candidate's source pins.
- Return SHA is the final commit on this review branch; the payload manifest
  excludes itself. No H1, protected adoption, native/science/actor right or
  code acceptance is claimed.
