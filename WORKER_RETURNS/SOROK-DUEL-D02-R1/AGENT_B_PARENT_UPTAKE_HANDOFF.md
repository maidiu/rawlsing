# SOROK D02/D03 Agent B — parent uptake and incremental period counterstrike

**Task chain:** `D02` bounded counterstrike + `D03` sourcefree immediate speech uptake. `D04` seam only.
**Status:** D02 current-clock selector remains `IN_PROGRESS_PREREQUISITE_HELD` (incremental current period implemented; historical/interleaving/P4-live-root not). D03 is a bounded sourcefree adapter over actual C04 standalone speech/child uptake; it is **not** D04, native CAN-008, or a normal P4/P6 C04 integration.
**Programme:** #939 / PR #938 at `08a323b490df4e2ddd0dca7f8b3cd394dfe17e0a`.
**Frozen composition:** `6c6a8afa14e8cb197c5db23257e8171a448bc944` (A D02 `cef8f53b...`/code `d82d2ac...` + Pair1 A `7663067...` + Pair3 B `1510d83...`).
**Same A return:** `cef8f53b404e8c5fc124bec2649ed44cba679556`; A D02 code `d82d2ac28331215ba2caa0ae2d152cce3266bef5`.
**Branch:** `codex/sorok-duel-d02-b-parent-uptake-20261112-r1`.
**B code cut:** `658354e2621e55a0e9d673fae429aaf568f92608`.
**Final artifact:** the branch HEAD containing this handoff and the B impact records. No remote/protected push.

## 0. Independent reconstruction before A

From the five frozen programme files and D02/D03/D04 packets:

- D02 is a thin read-only situated-field projection over actual P2/Pyat/actor owners. A changed material fact or eligible actor observation must change the real sourcefree decision input/options; stale source/clock, unobserved parent private state and portal gaze must not enter Nadia's readset; same-state restore must reproduce the eligible readset/hash. D02 depends D01/B02/C01, but B02 history/interleaving and C01 acceptance are separate.
- D03 must consume actual admitted parent speech and actual Nadia perception, not a caller boolean or handmade utterance. Same outward speech under two established prior organizations must change allowed immediate responses with no forced memory. Omitted receipt, altered speaker or severed event must hold/refuse/remove recruitment without erasing the parent's prior choice. Parent hidden reason/cash/period/portal knowledge must not enter Nadia's readset. Durable formation is distinct and cannot be written by retrospective prose or experimental response. D04 is dependency-held.
- The sourcefree `vertical:project`/`vertical:counterpart` is not the registered mother. A speaker/relation transfer requires an explicit sourcefree scope, not relabeling legacy B1 records. C04 is a candidate source; the normal P4/P6 C04 consumer under Pair3 repair is not accepted here.
- Full Library conceptual/operational sources remain NOT_INSPECTED locally; no contents are asserted.

## 1. Exact artifact and provenance

| Path | SHA-256 |
|---|---|
| `p3/situated_context.py` | `38bc881627ad74bd95be8530de8e4ab386815adbc4501f283398d70dc9d34dee` |
| `p3/immediate_uptake.py` | `0329e85d1cabb7194c2c2dcc93cb77756bac657299ee27c1c30af711e2108982` |
| `INTEGRATION_CONTRACT.md` | `b3a1a4991940734daff1ce695c040d2131b1414e08d32cf5d309ac64668485ad` |
| D02 `tests/test_d02_b_two_event_uptake.py` | `2395a9f7458d1f4f6ee1fb7c50bf98c16cb5d2a7210742ac1afda2dc25b37de2` |
| D02 `D02_B02_INGRESS_CONTRACT_B.md` | `57a1140fba0d50210479e01227b02c2ee02cc71428ac9b8a6827e1df4987f82a` |
| D03 `tests/test_d03_immediate_uptake.py` | `0448c6077bb351720202ac750c27eea556ce60464bd636748e80302f5bf41f48` |
| D03 `tests/d03_support.py` | `1bb438f2f6b4cc1d6f3e27c5761d48f57984762da021136df4c066b63f9d55ee` |
| D03 `D03_D04_SEAM.md` | `b624c243251796745dc4320ea59fc35aaa546b74ed9d85a4e3a73890729e1b29` |
| B02 `historical_period.py` (input) | `d1d4171af95f4d87fa9e174159cde46270d12331c728c4462251b488b0cb49c7` |
| C04 `parent_speech.py` (input) | `31e5fad79dfeda71b4632074b3e2df635121eb532bb44ba6303f8459c52d01b0` |
| C01 `supporting_actor.py` (input) | `35e43d8c924d6ea30b4376ef8bed4a8af5b68dd81d636e1cf9033da4320b9c5a` |
| B03/P6 `house.py` (input) | `6c892ea7525bc608ccd332dce9ee5ea7dc25397092f9c2db9ef44bd4e17d3436` |
| D01 relay `p3_owner.py` | `81be18dae3c4c5d9d79f68ee7146be13055a24c4b63bb54019b8ce9d3931b44b` |
| D01 relay `state_store.py` | `fc878ce928d9aca305166bfd1b24f4f5c31923b9479f6d47ac4a0bd54402589a` |
| S45 `projection.py` (input) | `6e7771000b0d50abcdc990192a2d834171640371e6e814694a918eb9286386fd` |

Commands/receipts:

```sh
python3 -B -m pytest -q -p no:cacheprovider WORKER_RETURNS/SOROK-DUEL-D02-R1/tests/
python3 -B -m pytest -q -p no:cacheprovider WORKER_RETURNS/SOROK-DUEL-D03-R1/tests/
python3 -B -m pytest -q -p no:cacheprovider WORKER_RETURNS/SOROK-DUEL-D01-R1/tests/
python3 -B -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests/test_state_store.py \
  WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests/test_rules.py \
  WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests/test_projections.py \
  WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests/test_p3_owner.py \
  WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests/test_p3_goal_residuals.py
```

Receipts: D02 all **22 passed in 927.85 s** (`D02/evidence/d02_b_parent_uptake_all.log`); D02 focused two-event **2 passed in 8.55 s** (`D02/evidence/d02_b_two_event_final.log`); D03 **7 passed in 75.09 s** (`D03/evidence/d03_b_immediate_uptake.log`); D01 **15 passed in 89.66 s**; P3 selected regression **77 passed, 1 skipped in 53.88 s** (`D03/evidence/`).

Only `p3/situated_context.py`/`p3/immediate_uptake.py`, D02/D03 tests/artifacts/evidence and the optional P3 contract section were written. P2/material/period/B01–B05, parent_activity/decision/speech/supporting, P4/P6/run_p4/run_p6, world writer, other-pair files, guides/workflows/Pyat/global/protected were not edited.

## 2. A's valid work, conceded

- **D02-B1/B2/B3/B4/B5/B6 repairs are real.** Event-time selection, normalized access hashes, event/current co-presence separation, the D02 source closure, pending refusal and the read-boundary correction are preserved. I did not reopen them.
- **Acquired-state contribution is genuine.** Exact scoped `PsycheStore.query` + existing `projections.activate` over a sealed later plan, no caller `actor_observed`/eligible override, bounded modes/hashes/withheld/active-latent contradictions, unchanged store head, and real recognized/imposed histories delivering different modes to the provider input and later P3 response. I preserve it.
- **Scope separation is correct.** The acquired record scope remains the sourcefree vertical project/counterpart; it is not relabeled as the registered mother. Parent private state remains unread.
- **B02 is source-present.** The current-period ingress is actual; the global “B02 unbuilt” claim is stale at this composition. Full historical/interleaving/P4-live-root claims still need separate evidence.
- **D01 relay deletion/record-list and actual-owner verify are correct.** No D01 retention round is reopened.

## 3. Defects/gaps established

### D02-B8 — Prior-perception activation was not qualified by the actual later speech receipt

A's `_activation_context` derives `actor_observed` from the selected **prior** perception. The actual later P3 owner rechecks its own event access, but a caller/provider carrying A's acquired eligible modes could treat them as proof that Nadia heard a later parent speech even when the C04 child receipt is absent.

B's actual two-event evidence: on a fresh P3 root with prior records, the D02 acquired state is `ELIGIBLE`/`joint_check` and `actor_observed=true` from the prior event; the actual parent speech is committed while the child is elsewhere, so `read_child_uptake` is `NOT_PERCEIVED`. B's D03 actual-speech consumer returns `HELD_NOT_PERCEIVED`, no modes/streams, no text/event read, no activation context, unchanged store head; the parent prior decision remains `READ`. This is the required two-event boundary: prior organization is not new-event hearing. Test: `D02/tests/test_d02_b_two_event_uptake.py`.

### D02-B9 — Period ingress used the older anchor/read_material_period path, not actual incremental period_progress

A mapped the current clock to a date by private anchor-date arithmetic and read `read_material_period`; it did not consume the actual incremental `period_progress` currentness/coverage/remaining API now present. In the tested cases the date matched, but the ingress omitted the actual progress state and could not demonstrate that the date came from the incremental reader rather than a parallel derivation.

B now selects the current declared period, reads `period_progress`, requires its clock/period to match, uses `progress.current_date`, then `read_material_period` must return the same logical tick. `period_progress` status/currentness/coverage/remaining and exact source symbols are in the body/readset. The declared S46 tick-day basis is still checked; no workshop tick becomes a year. Tests: `test_current_period_uses_incremental_progress_fields` and A's existing period test.

### D02-B10 — The period source pin did not name the incremental reader

A's `period_source` symbol list named `read_material_period`/`p3_interval_span`/`read_period_plan` but not `period_progress`. B pins the actual incremental symbol and updates the optional B02 ingress addendum; the A contract remains as historical testimony, and the B addendum is the current pointer.

### D03-B1 — No D03 immediate-uptake consumer existed

A's D02 acquired state is a prior-organization read, not a speech response. There was no actual C04 speech -> Nadia-qualified uptake -> existing P3 response-rule consumer, no omitted-receipt/altered-speaker/severed-event response court, and no explicit durable-formation hold. B implements that bounded consumer.

## 4. Corrections implemented

- **D02 period:** `_period_ingress` uses `period_progress`; body/readset includes progress; `period_source` includes the symbol; `D02_B02_INGRESS_CONTRACT_B.md`; `B02_INGRESS.contract_doc` points to the B addendum. Current-only; historical/interleaving/P4 live root unchanged/held.
- **D02 two-event proof:** actual unobserved C04 speech after prior acquired modes; D03 holds; test.
- **D03 module `p3/immediate_uptake.py`:**
  - actual `read_child_uptake` + actual writer receipt, C01 public speaker registration, no caller boolean/handmade utterance;
  - public-only speech scope; hidden reason/decision/period/cash/portal not read; self-only parent receipt refuses `D03_PRIVATE_INPUT`;
  - local sealed P3 plan-scope validation; existing `PsycheStore.query` + `projections.activate` + existing response rule descriptor; `actor_observed=true` only from the actual child speech receipt; `material_eligible=None` and material feasibility separate;
  - bounded eligible modes/streams/withheld/contradictions; no new rule/owner/store;
  - `durable_formation = MISSING_RULE`, no writes, store head before/after equal, target candidate null;
  - exact D03 source closure (P3 owner pins + immediate_uptake + parent_speech + supporting_actor + S45 projection + p3 init), expected-closure refusal, optional expected speaker binding;
  - actual same-speech recognized/imposed roots yield joint_check/private_check; unobserved speech holds; altered/private/severed speech refuses/holds without erasing parent decision; material-infeasible parent decision does not suppress the immediate sourcefree candidates;
  - D03 output is accepted as the existing `RecursionCycle` provider context, and the actual later P3 response streams match the D03 mode/record hash.
- **D04 seam:** `D03_D04_SEAM.md` only; no D04 target/owner/writer.
- **Optional `INTEGRATION_CONTRACT.md`:** D03 API/limits and incremental B02 period addendum; A's earlier optional section preserved.

## 5. Proof of improvement / preservation

- D02 all 22 passed; focused two-event 2 passed; D03 7 passed; D01 15; P3 77/1.
- Same actual speech event ID/hash/text under two P3 histories: D03 modes `joint_check` vs `private_check`; streams and record hashes differ; actual P3 later responses match; store head count unchanged; no durable record.
- Unobserved speech: D02 prior acquired `ELIGIBLE`, C04 child uptake `NOT_PERCEIVED`, D03 `HELD_NOT_PERCEIVED`, no modes/text/event, parent decision `READ`.
- Hidden/private: `HIDDEN` absent; self-only parent receipt refused; no cash/period/decision/portal fields in D03 readset.
- Period: incremental `period_progress` current date/clock, B02 source symbol; A's current-period test and B's progress test pass.
- Preserved: A's D01 repairs; A's D02 event/access/source/acquired gains; B's prior D02 tests; no P2/house/supporting/P4/P6 edits.
- Cost: D02 927.85 s + D03 75.09 s + D01 89.66 s + P3 53.88 s = 1146.48 s observed; tokens/USD `UNKNOWN`.

## 6. Concessions, refutations, self-attack

- **Conceded:** A's acquired-state read, D02 event/access/source closure repairs, D01 deletion/actual-owner repair, and B02 source presence.
- **Not a refutation of A's acquired read:** A's acquired modes are valid prior organization. The defect/gap is treating them as later-event hearing; B gates the actual D03 speech response on the C04 child receipt.
- **Refuted as sufficient:** A's older age anchor/private date derivation for the actual incremental period API; replaced by `period_progress.current_date` with matching clock/period.
- **Refuted as sufficient:** signifying the B02 period source without the `period_progress` symbol; repaired.
- **Bounded:** A's provider transport is not actor cognition; B retains that boundary. The D03 provider/later P3 test proves input/read consistency, not native cognition.
- **Bounded:** A's source closure is file-level; B's D03 closure is selected-file-level, not whole S47/P2 or a Byzantine root.
- **Own attack:** local D03 plan validation duplicates D02's plan-scope validation; it is sourcefree and exact for the P3 plan, but a future unified helper would reduce duplication. It does not import or relabel the B1 counterpart.
- **Own attack:** D03's immediate response stream construction is an adapter over the existing response rule descriptor/activation, not a call to `P3Owner._effect` (which requires a focal P3 event and would mislabel a parent speech). The later actual P3 response test confirms the same organization produces the same mode/record. This is the honest boundary.

## 7. New attack surfaces

- D03 uses the standalone C04 writer/child-uptake seam, not the normal P4/P6 C04 consumer under Pair3's repair. Do not infer a live P6 join or normal user scene.
- D03 source closure is exact for immediate_uptake/parent_speech/supporting_actor/S45 projection/P3 pins; it does not pin the C04 writer's parent_activity/decision transitively, because they are not read by this adapter.
- D03 accepts any registered `parent` role speaker unless `expected_speaker_actor_id` is supplied. Callers must bind the actual parent when speaker identity matters; the altered-speaker test covers tampered receipts/expectation.
- D03's immediate candidate modes are prior-organization modes, not a speech-specific semantic rule. Do not claim the same text selects the mode; the actual child receipt gates the response, and the prior organization supplies the modes.
- D03 reads P3 records through the existing store and checks unchanged head; it does not verify the whole P3 chain beyond the owner's inherited D01 actual-owner construction.
- D02 period read uses `period_progress` but does not materialize or apply P3 interleaving; historical/as-of and live P4/P6 period joins remain held.
- B02 source hash at this composition is `d1d417...`; A's earlier contract source hash `78e...` is historical. Use the B addendum/current `period_source` output.
- No native/rights/actor/human/protected acceptance; full D02/D03 independent receiving remains separate.

## 8. Surviving disagreements

- **D03 rule boundary:** adapter over existing activation/response descriptor vs a future shared `test_rules`/P3 helper. The parent speech is not a focal P3 event; relabeling it would be false. If A can provide a unified sourcefree helper without mislabeling the speaker, use it.
- **D02 acquired provider hint:** D02 prior modes are legitimate prior organization. D03 gates actual speech; a provider that ignores the actual child receipt would still misuse any context. The recipient boundary is explicit; stronger provider-side enforcement is a downstream design question.
- **C04 normal P4/P6 consumer:** Pair3 SAME A's parent-lock/normal child experience repair is not in this composition/acceptance; D03's standalone seam is exact but not the live house join.
- **Period:** incremental current period is qualified; historical B02 split, midperiod P3 interleaving, later actor decision and cold multi-period replay remain unbuilt. `materialize_to` is not invoked because D02 is current-state read-only.
- **D04:** exact seam prepared; no target rule/writer/B05 qualification. Do not mark D04 READY.
- **Source closure:** file-level exact; no hash arms race or whole-repo pin.

## 9. Challenge to same A

1. **Break D03 with an actual second-parent speech.** Create a second registered parent/decision/speech with the same text; show whether `expected_speaker_actor_id` + actual receipt prevents cross-speaker recruitment. If a sourcefree speaker-relation rule is required, implement it explicitly without renaming the B1 counterpart.
2. **Break the two-event boundary.** Find a legitimate actual provider/proposal path where D02 prior acquired modes enter an unobserved parent speech response despite D03's child-receipt gate. Fix it at the actual consumer, not by removing prior organization.
3. **Break the immediate-response adapter.** Show that an existing P3 response helper can be called without mislabeling the parent speech as a focal P3 event, or demonstrate a semantic speech rule that D03 must add. Preserve MISSING_RULE/durable no-write.
4. **Break the period incremental path.** Use actual B02 `period_progress`/`materialize_to` with a midperiod employment change, non-day-aligned clock, outside period and cold replay; show whether D02's current-only read still matches the actual period and whether the P3 interval seam is truly consumed by a later actor decision.
5. **Attack the C04/P6 seam.** Implement the normal Pair3 C04 child consumer/P6 join and show the same actual uptake reaches the D03 input; do not claim the standalone seam is the live house.
6. **Prepare D04 concretely.** Consume D03's exact fields and add one authorized sourcefree target/recruiter rule with B05 qualification; do not use option labels or immediate modes as durable memory.
7. **No D01 retention re-litigation.** The deletion/actual-owner repair remains adequate.

## 10. Limits

- D02 remains `IN_PROGRESS_PREREQUISITE_HELD`; full historical B02, P3 interleaving, final C01/B03/B04/B05 and live P4/P6 join are not accepted.
- D03 is a sourcefree standalone C04-to-P3 immediate-uptake adapter; not D04, not native CAN-008, not a normal P4/P6 child-experience consumer, not a finished J join.
- C04/Pair3, C01, B02, B04/B05 are candidate inputs; their separate running contracts are not rewritten.
- No new scheduler/store/owner/rule/world writer; no parent private reason/cash/period/portal in Nadia readset.
- Source closure is exact-file selected, not a Byzantine authenticated root; old-code roots require fresh fixtures.
- Token/USD `UNKNOWN`; wall times are pytest observations.
- No protected merge, native science, actor/human/source rights or independent acceptance.
