# SOROK V3 COURTS RX04 — INDEPENDENT HOSTILE REVIEW OF X04

**Review target:** `b609986a3f635de7b7581e763e76d3496ed9ad7e` (`agent/v3court-x04-scheduler-llm-event-r1`).
**Review startup:** `9a2753a1e9f76e9fcfa0c76dba49ed0e6cabf2a2` (`agent/v3court-review-rx04-secondwave-r1`).
**Review role:** independent I3 source/engineering reviewer; not X04 author, HQ, native mechanic issuer, production editor or self-reviewer.
**Surface:** OpenCode / DeepSeek V4.1-Flash MAX local S2; sourcefree original-code inspection. No provider/model call, no production or source edit, no native actor/rule/source grant.

**Overall:** `REVISE_PRECISE_WITH_ACCEPTED_SOURCE_FACTS`. X04's central source findings are largely correct and independently reproduced: 19 core / 20 configured steps, two event ledgers, premerged LLM deltas, fallback fabrication, age-band rupture outside the ledger, hidden derived writes, annotation leakage, and a one-call S48 transport with no 3–5 sequential batch. Four claims require precise correction, and two material reds were missed.

**Court verdicts**

- **ENGINEERING:** `ACCEPT_SCOPED_SOURCE_FACTS / REVISE_PRECISE / NEW_REDS`. The code and 77-test grouping are reproduced at the tested grain. Corrections: empty/parse paths do write a diagnostic state field; Pass-2 transport failure after mutation is not rolled back or marked cleanly; the "malheur" process severity is mapped to `micro`; the server does not call `render_year` again for non-LLM years (the final `run_and_print` re-render is a separate runner edge). New reds: no transactional rollback, and misleading `applied/clean` status after a Pass-2 callback exception.
- **SCIENCE:** `AGREE_SCOPED / HOLD_RULE_UNISSUED`. X04 correctly keeps fixed scoring weights, random surprise, LLM labels, delta templates, forced fallback and age rupture below empirical/native law. No human developmental rule, learning law or actor type is issued.
- **AUTHORITY:** `AGREE_SCOPED / NO_NATIVE_GRANT`. X04's no-native/no-production claim is correct. S48 is a current-test transport with an empty candidate source; it is not N11 or a complete C9/C12 person. No C8/C9/C11/C12/Pyat/CAN/ADP permission is inferred.

**Final independent status:** `RX04_REVISE_PRECISE__SOURCE_FACTS_CONFIRMED__EMPTY_DIAGNOSTIC_WRITE__NO_ROLLBACK__MALHEUR_SEVERITY_MISMATCH__SERVER_RERENDER_CLAIM_CORRECTED__NO_NATIVE_GRANT`.

## 1. Preflight, target and source identity

- X04 target remote tip verified exactly at `b609986a3f635de7b7581e763e76d3496ed9ad7e`.
- Review branch created at exact `9a2753a1e9f76e9fcfa0c76dba49ed0e6cabf2a2`; no duplicate RX04 worktree/session existed before this worktree was created. Sibling review branch names at the same startup are distinct reviews, not this reviewer.
- Source root `<USER_HOME>/Desktop/Rawlsing/Rawlsing_code_bundle_staging` verified; direct read-only inspection.
- X04's complete return and all nine M25/M27/M28/M29/M33/M34/M37/M38/M39 dossiers read at target SHA; the original X04 commission and second-wave intake, SYN01 R1, the four-review disposition and N11/user-settled controls read. The available local 00C/00E process references were read as qualification/review law, not semantic grants.
- Source file hashes in X04's table match direct local hashes for the inspected X04 files. S48 exact-cut blobs match `9fe0d066e4bf61ab6819a1f56e42d6d07956c2f7`: `session.py` `3de86536497999e7272cc1e4e703185356955088`, `sources.py` `90775a9a2b5793542b3e8e31734f929fdc8e0a12`, `product.py` `4561389bd8a68ab1c9c10aca6a60692be79a15c3`.
- Local staging zip `3f2c5ed9…` is not the TD-R05 archive `953c9149…`; archive-level exactness is not claimed. File-level identities control.
- Evidence identities are in `SOURCE_IDENTITIES.json`; test and probe receipts are in `TEST_MANIFEST.json` and `TEST_SOURCE_AND_LOGS/`.

## 2. Independent execution

| Evidence | Result |
|---|---|
| 64 V3 focused tests (architecture, step logic, sanity, LLM contract, metabolization, render/persona/prompt/structural surfaces) | **64 passed in 21.82s** |
| `test_distribution_smoke.py` (50 agents × 20 years) | **1 passed in 302.02s** |
| S48 exact-cut `tests/test_s48_one_call.py` at `9fe0d066…` | **12 passed in 13.58s** |
| **X04 grouping total** | **77 passed, 0 failed, 0 errors** |
| Independent source probe | Completed; `probe_rx04.json` |

X04's 65 old-V3 + 12 S48 = 77 grouping is independently reproduced. X04's `test_distribution_smoke` timing (152s) is environment-specific; this review observed 302.02s for the same single passing test, so the pass is confirmed but the timing is not. No full 150-test V3 suite was rerun; X04 correctly labels its 150/1 note as secondhand RX01 evidence.

**NOT_RUN:** live/provider LLM band, actual S48 product CLI/provider call, V2 conversation, current C44/S49/C9/C12 native person, official Astra K suite, raw surveys/respondents, production/native adoption. No scientific or native claim follows from green sourcefree tests.

## 3. Claim-by-claim hostile verdicts

### C1 — 19 core versus 20 configured steps: **AGREE_SCOPED**
`v3/v3_yearly_step_order.yaml` has **19** `core_steps` but **20** `steps`; the appended step is `active_magnets_update`. Independent probe reproduced both counts and the order. `run_one_year` executes the 20 configured steps, clamps, computes scheduled derived values, increments `year`/`age` after the steps, then runs pressure flow. `render_layer` is the 19th core step, before `active_magnets_update` and before age increment.

**Alternative / NO_CHANGE:** a 0-event year still increments age/year, runs all steps and pressure flow; it is not a lawful continuity/no-change interval. The old scheduler is a slow annual integrator, not an event/interval spine.

### C2 — 77 focused tests: **AGREE_SCOPED**
The 64-test V3 subset, the 1 distribution smoke test, and the 12 S48 tests all pass independently; the total is 77. X04's grouping and counts are correct. Timing differs (302s vs 152s) but is not a semantic discrepancy. X04's full-suite 150/1 note is secondhand and is not counted as an independent reproduction.

### C3 — LLM selected events are not in the canonical event ledger: **AGREE_SCOPED**
`run_llm_band_year` applies selected events through `apply_deltas_to_state` but never appends them to `state.events_this_year`. The probe with one selected practice event shows:
- `events_before == events_after == []`;
- `practice_stack.organizing` and `craft` changed 0→2;
- selected event only in `yearly_integrity.llm_band.selected_event_ids`;
- server `year_record["event_ledger"]` is the mechanical sampler list, while LLM selections are in `llm_band_ledger`.
This is a real two-ledger / absent-canonical-timeline defect. It is not repaired by the fact that mutation provenance exists inside the band.

### C4 — premerged deltas and no sequential event state: **AGREE_SCOPED**
`run_llm_band_year` computes `delta_from_event` for all selected events, calls `merge_deltas`, and applies one merged dict. `merge_deltas` sums capacity/alienation/coherence and merges lists; event 2 cannot read a state after event 1. The code has no event ordinal/source/access/interval and no per-event state transition. Reversing two events with the same additive deltas yields the same merged numeric result; changing an event label changes the delta template. This supports the X04 red, and RX02's earlier correction remains binding: old route values can alter later channel selection, but this is not a newly learned relation.

### C5 — fallback fabrication / no legitimate no-change: **AGREE_SCOPED, with a precise no-mutation correction**
- Empty raw response → `status="empty_response"` and no practice/domain/wound mutation; parse failure → `status="parse_failed"` and no such mutation.
- A syntactically valid packet with empty event and magnet lists reaches `parse_candidate_packet_with_fallback` and fabricates `fallback_ev_<year>_<age>` as a minor `practice` event. In the independent probe, that fallback produced `practice_stack.organizing/craft = 2`, wound changes, and `status="applied"`.
- If all candidates have scores but selection returns nothing, `run_llm_band_year` takes the first candidate; the empirical path is mostly a code fallback, not a lawful no-event admission.
- **Correction:** empty/parse paths are not literally state-nonmutating. They call `_set_llm_band_status`, which writes `state.yearly_integrity["llm_band"]`; that field is part of `BackboneState` and is included in `backbone_hash`. Independent probe: no practice/domain/wound change, but `backbone_hash` changed for both empty and parse-failure paths. X04's "no mutation" is correct only for model/psychological fields, not for the whole backbone/diagnostic state. No typed `NO_CHANGE` record is produced.
- **Correction:** the `no_candidates` branch is not reached for a parsed empty packet because the fallback has already added an event. X04 itself notes this, but its earlier phrase "no candidates returns unchanged" must not be used as if that branch were a live no-event path.

### C6 — age-band rupture outside the event ledger: **AGREE_SCOPED, with a missing severity correction**
`maybe_inject_rupture_at_band_age` uses age bands `{3:.60, 7:.70, 11:.65, 14:.60, 17:.55, 24:.45, 30:.30}` and module-global `random.random()/choices()`; it creates a shard/process and directly bumps wounds. Independent probe at age 3, seed 1:
- 1 shard, 1 process, `events_this_year=[]`;
- shard status `raw`, process status `raw`, `plasticity_years_left=2`;
- abandonment 50→58, fear 50→52.
X04 correctly calls this an age ritual outside the ledger.

**Precise omission:** `create_rupture_shard_from_event` maps intensity `"malheur"` (and `"minor"`) to process severity `"micro"`, while the age path passes original `"malheur"` to `update_wound_vector_from_rupture` (+15). Independent probe: malheur event → process severity `micro`, shard `raw`, `is_malheur(proc.severity)` false; direct malheur wound bump produces the larger wound effect. The normal LLM event path calls only `create_rupture_shard_from_event` and does **not** call the wound update. This is a source-level inconsistency X04 did not state. It strengthens the REPLACE disposition: the process severity and wound effect cannot both be trusted.

### C7 — derived computation writes persistent backbone fields: **AGREE_SCOPED**
`compute_all_derived` writes `state.metabolic_style` (`derived.py:322-334`) and `state.registers` (`:333-334`). Independent probe set `registers.inner_load=10`; after `compute_all_derived`, `inner_load=50.0` and `metabolic_style` was populated. `assert_no_derived_fields_in_backbone` checks only the fixed six-name `DERIVED_INDEX_NAMES`; `registers`/`metabolic_style` are missed. This is a real stored/derived ordering defect, not just a naming issue. It also means the "derived-only" claim cannot be accepted at face value.

### C8 — structural annotation can enter memory/previous scene: **AGREE_SCOPED for the leak; REVISE_PRECISE for the server re-render mechanism**
- Server non-LLM years call `render_year` once, then set `rendered_output.narrative_snapshot.scene` to `"Age X: health declined."` (or similar) when significant deltas exist. The annotation has no `[Structural year]` marker.
- `persona_sheet.real_scenes` filters only marker strings; the annotation passes into `MEMORIES`. Independent probe confirms `"Age 3: health declined."` appears in backstory.
- If `real_scenes` is empty, `elif scene` writes the current scene as `"Most recent memory"` even when it is a marker. Independent probe confirms `"[Structural year: no LLM scene rendered]"` appears as `"Most recent memory"`.
- `server._previous_scene` filters markers but not annotation text, so an annotation can be passed as `previous_scene` to a later Pass 2.
- `distill_memory` filters marker/stub patterns but not the annotation text.
- **Correction:** the server does **not** call `render_year` again for non-LLM years. `simulation.py:552` renders once, `:573–575` then sets the annotation, and the Pass-2 scene recovery at `:585` runs only when `llm_band_used`. The separate `v3/run_and_print.py:150–152` unconditionally re-renders after all years, so it can overwrite the final year's annotation; that is a runner edge, not a server non-LLM-year re-render. X04's broader "server/runner may render again for non-LLM years" must be narrowed.

### C9 — S48 one-call transport, empty candidate list and source/SCI05 holds: **AGREE_SCOPED**
Independent run of the exact S48 cut `9fe0d066…`: 12 passed in 13.58s. Source confirms `candidate_specs()=[]`, `eligible_candidate_ids()=[]`, and `issue_current_source` raises `S48Refusal(SOURCE_OWNER_HOLD, MISSING_FUNCTION)`. `run_turn` selects one current E1/C9 source, one product call, caches by source/hash/turn, and rejects non-current source. `admit_event` accepts at most one prospective candidate; empty allowed list → `SOURCE_OWNER_HOLD`; with a nonempty allowed list, empty prospective → `NO_PROSPECTIVE_PROPOSAL` and more than one → `UNRESOLVED`; nonempty self-account → `SCI05_HOLD`. S48 is a real one-call transport/refusal boundary, not the user-settled 3–5 sequential batch. X04's claim is correct at this grain.

### C10 — no current C9/C12 person or native grant: **AGREE_SCOPED**
No actual current C9/C12 person loop was run or traced. S48 is a current-test transport with empty candidate source; S49/S44 and prior current-source cuts are not current native person proof. The review does not infer a native actor/rule/source/C8/C9/C11/C12/Pyat permission. X04's HOLD is correct.

### C11 — direct render nonmutation versus later rendered-output feedback: **AGREE_SCOPED with exact fields; HOLD on rollback**
**Direct render:** independent probe confirmed `render_year(state, derived, config)` leaves `backbone_hash` unchanged and writes only `rendered_output`. The existing test and X04's claim are correct at this function grain.

**Later feedback:** independent source trace and probe confirm that a later `update_metabolization_and_plasticity_step` reads `state.rendered_output` through `_analyze_narrative_for_support_quality`, writes `state.narration_support`, and applies cluster deltas to `state.psychological_capacity` (and downstream biases). In the probe with a fixed `sensitivity_exposure` process, neutral prose → aperture 54 and warmth 20; warm prose → aperture 55 and warmth 22; coercive prose left aperture 54 with coercion 32. This is a real cross-mechanism path: direct render isolation is true, but rendered text later becomes a support signal for psychic capacity. The exact mutated fields are `narration_support.*`, `psychological_capacity.*`, and then stability/residue consumers; `rendered_output` itself is excluded from `backbone_hash`, which is why the immediate nonmutation test does not see it.

**Rollback/replay:** no rollback was located. `run_llm_band_year` applies all deltas before Pass 2; `render_year` catches a Pass-2 callback exception internally, writes a no-scene fallback, and returns without restoring state. Independent probe with a valid Pass 1 and a raising Pass 2 callback:
- selected practice event applied (organizing/craft 0→2; domain/wound/coherence changes);
- `llm_band.status="applied"`, `render_integrity=null`, i.e. not a clean failure status;
- state remains mutated after the failed render.
This is a **new red** and a `HOLD` for any claim that the band is transactional or replay/rollback-safe. X04 did not establish that claim; it must not be inferred from `render_year`'s direct nonmutation.

### C12 — 3–5 conditional batch, sequential realization, N+1 retrospective: **AGREE_SCOPED / HOLD**
X04's table is accurate: Pass 1 proposes 0–6 annual candidates; selection is at most 5 events (2 major + 2 minor + 1 surprise), plus 2 magnets; there is no 3–5 conditional event specification, no event order/interval/independent coactor realization, no per-event carry-forward, no N+1 first-half retrospective, and no ordinary-LLM-free intermediate sequence. S48 is one event/one call, not the batch. The user-settled N11 contract remains missing. This is a `HOLD` for implementation and `MISSING` for the batch producer, not a native NO_CHANGE.

### C13 — fixed route/value feedback versus learned relation: **AGREE_SCOPED**
The old code has fixed scoring/route arithmetic and a fixed topology/framework regime switch. It does not create a durable new learned relation edge. The RX02 correction is preserved: old route-value changes can alter later channel selection; grooves alone change conductance; neither is proof of a newly learned relation. S48's one-call source path is not evidence of such a relation.

### Per-dossier review matrix

| X04 dossier | Independent verdict | Precise qualification |
|---|---|---|
| M25 yearly ordered spine | **AGREE_SCOPED** | 19 core/20 steps, render timing and year/age increment confirmed. `run_and_print` runs its final band after all years, not after each `run_one_year`; this is a runner, not server-loop, timing. |
| M27 Pass 1 proposal | **AGREE_SCOPED** | Proposal-only boundary and premerged application confirmed; selected events absent from `events_this_year`. |
| M28 score/select/apply | **AGREE_SCOPED** | Exact weights/caps, no hard admissibility, unseeded surprise, merged application confirmed. |
| M29 Pass 2 render-only | **AGREE_SCOPED / REVISE** | Direct render nonmutation confirmed; Pass-2 callback exception after mutation is not rolled back and can be labelled `applied`/clean. |
| M33 mechanical sampler | **AGREE_SCOPED** | Deterministic 0–3 event serialization; no actor/access/coactor; zero-event year still ages. |
| M34 fallback | **AGREE_SCOPED / REVISE** | Fabricated practice event and no lawful no-change confirmed; empty/parse diagnostic write correction; fallback is not a no-event record. |
| M37 structural annotation | **AGREE_SCOPED / REVISE** | Annotation/marker memory leak confirmed; server non-LLM re-render claim corrected; final runner re-render can overwrite final annotation. |
| M38 derived schedule | **AGREE_SCOPED** | Fail-fast equality and hidden `registers`/`metabolic_style` writes confirmed. |
| M39 age rupture | **AGREE_SCOPED / REVISE** | Age/random/outside-ledger/direct-wound confirmed; malheur→micro severity and event-path wound omission added. |

## 4. Material corrections to X04

| ID | X04 statement | Independent correction | Severity |
|---|---|---|---|
| R1 | Empty/parse failure makes no mutation. | No practice/domain/wound mutation, but `_set_llm_band_status` writes `yearly_integrity.llm_band`; backbone hash changes. No typed `NO_CHANGE`. | `REVISE_PRECISE` |
| R2 | Fallback/no-selection behavior is a no-event/selection boundary. | Empty parsed packet fabricates a practice event and applies practice/wound deltas; `no_candidates` is unreachable after fallback. Fallback is not a lawful no-change. | `REVISE_PRECISE` |
| R3 | The server/runner may re-render non-LLM years and overwrite annotation. | Server non-LLM year renders once then annotates; no second server render. `run_and_print` final unconditional re-render can overwrite the final-year annotation. | `REVISE_PRECISE` |
| R4 | Age-band rupture creates a shard/process and direct wound. | True, but `"malheur"` becomes process severity `"micro"`; `is_malheur(proc.severity)` false; event path does not call wound update; only age path does. | `REVISE_PRECISE` |
| R5 | Render is direct-nonmutating; band is not render-only. | Direct render isolation true; band has no rollback and a Pass-2 callback exception is recorded as `applied`/`clean` after state mutation. | `NEW_RED` |
| R6 | 77 focused tests and 152s distribution. | 77 passed reproduced; distribution took 302s here. Timing is not semantic. | `AGREE_SCOPED / timing note` |
| R7 | Full V3 150/1 in RX01. | Correctly labelled secondhand by X04; not independently rerun. | `HOLD / not counted` |

## 5. Positive, lawful alternative/NO_CHANGE, and severed-edge cases

### Causal positive actually executed at sourcefree grain
- 19 core/20 configured steps execute in order.
- Direct `render_year` sets `rendered_output` and leaves the backbone hash unchanged.
- A selected LLM practice event mutates `practice_stack` and `domains`, while `state.events_this_year` remains empty; its ID appears only in `llm_band.selected_event_ids`.
- The S48 exact cut passes 12 source-owner/replay/one-call tests with no world mutation on a hold.

These are architecture/serialization positives, not native psychology.

### Lawful NO_CHANGE or external-support alternative
- Empty/parse Pass-1 returns do not mutate practice/domains/wounds, but they are **not** a typed no-change: `yearly_integrity` is written and no `NO_CHANGE` record exists.
- A valid no-event year still increments age/year and runs pressure flow; it is continuity of the annual clock, not a no-change psychological interval.
- S48's empty prospective / missing B source is a **source-owner hold**, not a positive event and not a lawful actor NO_CHANGE.
- A true external-support alternative would be a source-qualified care/support event that changes the actor through an owned transition; the old fallback practice event is not that alternative.

### Severed upstream edge / fault
- **Pass-2 failure after mutation:** remove/raise the Pass-2 callback after a valid selected event. The band still applies practice/domain/wound deltas and reports `applied`/`clean`; no rollback. This is a valid source-edge fault against any transactional/replay claim.
- **Selected LLM event ledger:** remove the selected event from `events_this_year`; the band still mutates state. The old canonical ledger has no event to sever or replay.
- **Rupture:** remove the age-band trigger; no shard/process/wound occurs. The presence of a shard depends on age/RNG, not an admitted event; the event path and age path also disagree on wound/severity.
- **Sequential batch:** reverse two selected events with the same additive deltas; `merge_deltas` yields the same numeric result. A true sequential system must produce a different event-2 read or NO_CHANGE; old code cannot.

## 6. Engineering, science and authority verdicts in detail

### ENGINEERING
`ACCEPT_SCOPED_SOURCE_FACTS / REVISE_PRECISE / NEW_REDS`.
- Source identities, line mappings, 77 focused tests, and independent probes are reproducible.
- Accepted source facts: 19/20, two ledgers, premerge, fallback, age rupture, derived writes, annotation leak, S48 one-call, direct render nonmutation.
- Corrections R1–R5 above.
- New red: no rollback/transaction after Pass-2 failure, and misleading `applied/clean` status. This is material because the commission asks for replay/rollback and because a failed render must not silently ratify psychic state.
- No current C9/C12 integration; no production code changed.

### SCIENCE
`AGREE_SCOPED / HOLD_RULE_UNISSUED`.
- X04's refusal to promote fixed weights, random surprise, LLM labels, fallback, age band, delta templates or narrative to developmental law is correct.
- No concrete event→actor-relative impression→recruitment→CAN011/CAN012 durable transition→later C9 semantic read is issued.
- The user-settled 3–5 batch and retrospective memory are requirements, not implemented science.
- Project-attached primary/contextual literature is not a numeric law; no primary text was re-read for this review. The RS boundary (motives from activity; plurality contingent; instruction can itself create an operation) remains binding.

### AUTHORITY
`AGREE_SCOPED / NO_NATIVE_GRANT`.
- X04 is read-only historical source + sourcefree tests.
- S48 is current-test transport with empty candidate source and explicit source/SCI05 holds; it is not a native C9/C12 person.
- No C8/C9/C11/C12/Pyat/CAN/ADP, source rights, production adoption or native rule issuance is granted or implied.
- The reviewer is not the author and does not self-adopt.

## 7. FINDING → INTERPRETATION → NEXT ACTION → ACCOUNTABLE OWNER

| ID | Finding | Interpretation | Next action | Owner |
|---|---|---|---|---|
| F1 | X04's 19/20, 77-test, two-ledger, premerge, fallback, derived-write, annotation, S48 findings are reproduced. | X04 is a sound source/work map at the accepted grain, not a current-person proof. | Retain as scoped source evidence; do not promote to native integration. | X04 author / HQ intake |
| F2 | Empty/parse writes only `yearly_integrity`, but changes backbone hash and creates no typed NO_CHANGE. | Diagnostics and actor no-change must be separated. | Add a typed no-change/diagnostic distinction; do not call hash-stable no-mutation. | C8/C9/V3 scheduler |
| F3 | Pass-2 callback failure after mutation leaves state changed with `status=applied`, `render_integrity=null`. | No transaction/rollback; failed render can ratify a psychic mutation. | Split proposal/realization/render transaction; rollback or mark mutation status before any render; add fault test. | C6/C8/C9/C12 |
| F4 | `"malheur"` maps to process `micro`; age path applies malheur wound; event path does not. | M39 severity/wound paths disagree; event and age rupture are not one causal operation. | Correct severity mapping or remove the age path; require admitted event parentage; add both-path tests. | CAN012/CAN011/ADP019 |
| F5 | Server annotation leak is real; server does not re-render non-LLM years; `run_and_print` final re-render can overwrite final annotation. | Correct the mechanism, retain the leak red. | Tag annotations; exclude from memory/previous scene; correct X04 claim; test server and runner separately. | persona/ADP016/C9 |
| F6 | S48 is a genuine one-call transport/refusal, no 3–5 batch or N+1. | Reuse transport; do not call it N11. | Build batch/interval/retrospective seam only under N11/C9/ADP016/017/SCI05. | S48/C9/ADP016/017/SCI05 |
| F7 | Selection has no hard admissibility; surprise/age use unseeded RNG; fallback fabricates. | Soft ranking/drama is not lawful event admission. | Hard admissibility, named RNG/ADP020, explicit no-event/no-change. | C8/C9/ADP020 |
| F8 | No current C9/C12 person, no independent B source, no native grant. | X04's HOLD/NO_NATIVE_GRANT is correct. | Keep native/product release held; obtain owner/source/rule/consumer. | incumbent C9/C12 + competent owners |

## 8. Limitations and self-limitations

- No live/provider LLM; no actual S48 product CLI provider call; no V2 conversation.
- No current S44/S49/C9/C12 native person; no official Astra K tests; no native CAN/ADP/Pyat/source grant.
- Full 150-test V3 suite not rerun; X04's secondhand RX01 note is not promoted.
- `test_distribution_smoke` timing differs (302s vs X04's 152s); only pass/fail is compared.
- The X04 probe is not retained by X04; this review therefore uses its own probe rather than treating X04's probe as independently reproducible.
- The direct source tree is the known local staging tree, not the TD-R05 archive; archive-level exactness is not claimed.
- The review does not accept any primary scientific claim; no primary literature was re-read.

## 9. Return identity and exact paths

- **Return content:** only `SOROK_PRODUCT_CONTROL_ROOM/V3_COURTS/REVIEW_COURTS/RETURNS/RX04/` additions: this review, source identities, test manifest, probe, test logs and test wrapper. No central atlas, sequencer, X04 card, source, production, CAN/ADP/Pyat, C9/C12 or PRE-MAIN edit.
- **Reviewer branch:** `agent/v3court-review-rx04-secondwave-r1`.
- **Review startup:** `9a2753a1e9f76e9fcfa0c76dba49ed0e6cabf2a2`.
- **Target:** `b609986a3f635de7b7581e763e76d3496ed9ad7e`.
- **Content commit:** `6278f5d265051bd887e26916d1cd361a4b85b2d0` (the 11-file RX04 evidence/review commit).
- **Final remote head:** the branch tip after the metadata-only publication commit, verified with `git ls-remote origin refs/heads/agent/v3court-review-rx04-secondwave-r1`; the exact readback SHA is reported in the final return. No self-referential SHA is embedded in this file.

**No self-adoption. No native grant. No production implementation. STOP.**
