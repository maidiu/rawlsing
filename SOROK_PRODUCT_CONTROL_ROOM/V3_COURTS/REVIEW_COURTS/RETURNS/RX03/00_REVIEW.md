# RX03 — independent hostile review of X03 second-wave source court

**Reviewer branch:** `agent/v3court-review-rx03-secondwave-r1`  
**Sealed startup:** `9a2753a1e9f76e9fcfa0c76dba49ed0e6cabf2a2`  
**Pinned target:** `e81dd633b419d35619014bdf99f894ad4f98c5a5` (`agent/v3court-x03-development-topology-r1`)  
**Role:** independent I3 original-source reviewer; not X03 author, Sorok HQ, native semantic issuer, production editor or own reviewer.  
**Surface / model:** local macOS OpenCode / DeepSeek V4.1-Flash selected session; S2 sourcefree historical inspection; no model/provider switch and no LLM/provider call.  
**Source:** `/Users/matthewsmith/Desktop/Rawlsing/Rawlsing_code_bundle_staging`, read-only.  
**Terminal:** `RX03_SECOND_WAVE_REVIEW__X03_ENGINEERING_ACCEPT_SCOPED_WITH_PRECISE_CORRECTIONS__SCIENCE_HOLD_RULE_UNISSUED__AUTHORITY_NO_NATIVE_GRANT__CURRENT_C9_C12_HOLD`.

---

## 0. Preflight, independence and custody

- The review branch was created from the exact sealed startup `9a2753a1e9f76e9fcfa0c76dba49ed0e6cabf2a2`; the pinned X03 target is `e81dd633b419d35619014bdf99f894ad4f98c5a5`. Both were verified against the local Git object store and the remote target before review.
- A dedicated isolated worktree (`rx03-wt`) was created from the sealed startup. No duplicate RX03 worktree or active RX03 session was found. The author's `x03-wt` was not modified.
- Historical source at the user-confirmed path was read directly and read-only. No source copy was exported.
- No raw respondent/survey data, LLM/person generation, current S39–S52/C9/C12/Pyat run, production edit, native rule/source grant, atlas/sequencer write or other worker branch was used or changed.
- X03's 35 declared source files were independently hashed: **35/35 exact**. The S50-selected manifest was independently checked: **31/31 exact**. The local staging ZIP is `3f2c5ed925273153a4f300f75e54524729f0b4fef9974957be1f3cd887c91289`; TD-R05's archive is `953c9149bd03877206e3cb440d1f4db35dea6473af30b97fd23b7e76c6fc0086`. **Whole-archive identity is not claimed; file-level identity controls.**
- X03's 71 focused tests were independently reproduced: **71 passed in 16.96s** (X03 reports 71 in 14.55s; count matches, timing differs). The full `v3/tests` suite was **not run by RX03**; X03's timed attempt stopped after 15 collected tests at 180s and is correctly not counted as a pass or failure.
- X03's `probe_x03.py` was rerun independently. The general observations reproduced, with the precise corrections in §3.5 and §3.6.
- **Review independence:** no X03 dossier was modified; this return is evidence, not adoption. HQ, the competent owners and a later independent reviewer retain disposition.

---

## 1. Claim verdict matrix

**Status vocabulary:** `AGREE_SCOPED` = exact at the named sourcefree/documentary grain; `REVISE_PRECISE` = core finding survives but the stated evidence, wording or receipt is wrong; `HOLD` = not established at the required authority or native grain.

| # | X03 substantive claim | Verdict | Independent evidence / correction |
|---|---|---|---|
| C01 | X03 source identities are exact (35 files; S50 31/31); archive ZIP mismatch is not identity | **AGREE_SCOPED** | 35/35 SHA-256 exact; 31/31 S50 exact; local ZIP vs TD-R05 mismatch confirmed. |
| C02 | 71 focused historical tests passed; full-suite timed attempt is not a pass/fail | **AGREE_SCOPED** | 71 passed in 16.96s; full suite NOT_RUN by RX03; X03's withholding is correct. |
| C03 | M09 `update_cracks` is event-delta only; no spawn/activation/decay/reactivation; most `cracks_rules` are dead | **AGREE_SCOPED** | `cracks.py:15-61` reads only `intensify_range`; no lifecycle writes. |
| C04 | M09 placeholders are substantive hidden state and contribute to crack load; Pass 1 hides placeholder types | **AGREE_SCOPED** | `invariants.py:253-274`; `derived.py:166-199`; `llm_contract.py:604-615`. Default state gets 2 active placeholders. |
| C05 | M09 cracks are seeded from religion/SES/minority/age; some origin years are future-dated | **AGREE_SCOPED** | `seed_frameworks.py:193-250,303-353`; child probe gives four cracks, three active; origin 2002/2004 for an age-8 2000 persona. |
| C06 | M11 acute/chronic operator is real and changes capacity | **AGREE_SCOPED** | `frameworks.py:33-102`; synthetic weight 100 gives binding 51.5, 53.0, 51.5 on acute/acute/chronic. |
| C07 | M11 frameworks are age/demographic recipes; adult tenure is already chronic; domains ignore frameworks/practices | **AGREE_SCOPED** | `seed_frameworks.py:54-186`; adult 40 middle/dominant tenures 34/32; `domains.py:50-56` reads only event deltas; high/low probe identical. |
| C08 | M11 `enforce_framework_caps` does not enforce active-count `max_active=6` | **REVISE_PRECISE** | `enforce_framework_caps` (`frameworks.py:104-119`) indeed only moves weight<5 to dormant. But `assert_frameworks_limits` (`invariants.py:163-174`) is a year-end fail-fast check; the correct statement is “no cap/selection in the cap function; an assert can fail, not cap.” |
| C09 | M13 practices are seeded from SES/age/religiosity and mutated by labels/magnets/routed charge; domains ignore practices | **AGREE_SCOPED** | `practices.py:19-40`; `identity_to_backbone.py:374-405`; `delta_templates.py:161-219`; `flow.py:500-541`; `domains.py:50-56`. Child/adult practice values reproduced. |
| C10 | M14 topology hysteresis and one-step boundary/reversal gate are real | **AGREE_SCOPED** | `topology.py:14-99`; `boundary.py:20-80`; two-call transition and repression-75 reversal reproduced. |
| C11 | M14 is a global enum/scalar regime, not a newly learned relation edge; no focused topology/boundary test | **AGREE_SCOPED** | No relation-edge creation found; no focused test calls `update_loop_topology`/`update_solidarity_boundary`; architecture test only checks step order. |
| C12 | M16 strivings are age/proxy-map spawned; support/feasibility/momentum are unnamed random; five runs differ | **AGREE_SCOPED** | `striving_objects.py:63-70,82-124,127-213`; `update_striving_step` passes no RNG; five independent age-14 runs gave different object/value sets. |
| C13 | M16 exact five object sets listed in the dossier (meaning/eros; beauty/belonging; belonging/eros; justice/eros; beauty/justice) | **REVISE_PRECISE** | Those exact sets are not in X03's own `probe_x03.json` (which shows Peer/Justice, Art/Justice, Justice/Eros, Art/Peer, Eros/Justice) and are not reproducible; independent runs differ. Nonreplayability is the stable finding; the listed sets are a run-dependent receipt. |
| C14 | M16 retirement occurred “only at seed 1, not seed 0” | **REVISE_PRECISE** | X03's own probe JSON `retire_seed_scan` retires at seeds 1, 3, 4 (remaining count 1,0,1,0,0,1). Independent rerun is identical. The seed-1-only wording is false; random retirement is real. |
| C15 | M16 `setdefault(hopeful)`, no event/activity input, inactive objects removed, retired history dropped | **AGREE_SCOPED** | `striving_objects.py:242-272`; no `events_this_year` read; active-list deletion at `:239`. |
| C16 | M18 event path creates shard/process without wound update; age-band path calls both creation and wound update | **AGREE_SCOPED** | `delta_templates.py:331-358`; `metabolization_effects.py:273-332`. Probe: create-only wounds unchanged; direct malheur wound 50→69. |
| C17 | M18 severity mapping contradicts wound path; malheur becomes process micro; malheur multiplier unreachable in generated path | **AGREE_SCOPED** | `metabolization_effects.py:38` maps non-major/shock to micro; `is_malheur` requires malheur or major+status_shock+isolation; yearly call does not pass those. |
| C18 | M18 age-band rupture uses hardcoded ages and global RNG; 14/20 seeds inject at age 14 | **AGREE_SCOPED** | `metabolization_effects.py:273-332`; independent probe 14/20; modes vary. |
| C19 | M18 persona reads nonexistent `metabolization_mode` in two places, so “that branch is always false” | **REVISE_PRECISE** | `persona_sheet.py:275` still emits the unresolved-rupture voice note for `raw/narrativized/sealed`; only the mode text is missing. `persona_sheet.py:754` (`_sacred_ruptured`) is the branch that is always false. |
| C20 | M19 process status never leaves `raw`; `working/provisionally_narrated/integrated/sealed/chronic` have no producer; narrators/IRR/meanings/counters never update | **AGREE_SCOPED** | Source search found no status/narrator/IRR/meaning/counter writers; three probe years remain raw with plasticity 3→0. |
| C21 | M19 cluster deltas and `downstream_biases` accumulate for raw/working even after plasticity 0; biases have no consumer | **AGREE_SCOPED** | `metabolization_effects.py:558-583`; no consumer search hit for `downstream_biases`. Exact bias keys/values are mode-dependent. |
| C22 | M19 exact bias accumulation “betrayal_expectancy 2→4→6 and reality_tolerance −1→−2→−3” | **REVISE_PRECISE** | Accumulation is real, but the exact values are one random-mode/cluster draw. Independent run with mode `collapse` produced betrayal 2→4→6, reality −2→−4→−6, plus attachment_guarding 2→4→6. These are receipts, not stable constants. |
| C23 | M19 rendered narrative is causally wired into narration_support and later psyche; warm scene raises warmth/aperture | **AGREE_SCOPED** | Exact edge is next-year `update_metabolization_and_plasticity_step` (`metabolization_effects.py:541-575`), not `render_year`. Targeted probe: warm/raw aperture 55 vs neutral/raw 54; no-process path unchanged; severed reader removes difference. |
| C24 | M19 malheur multiplier unreachable; second rupture overwrites plasticity window; stability drain active only as holding/manual | **AGREE_SCOPED** | `create` maps malheur to micro; second rupture replaces `plasticity_window` 3→2; `stability_inertia.py:17-83` only drains integration/IRR/sealed for statuses not generated. |
| C25 | Old step order overstates actual inputs (domains/frameworks/practices/narrators) | **AGREE_SCOPED** | `domains.py:50-56` and `practices.py:19-40` read only events; `striving_objects` reads age/baseline; metabolization reads rendered text, not narrators. |
| C26 | No current same-person C9/C12 semantic consumer is proved; current integration `UNTRACED` | **AGREE_SCOPED** | RC static review `ddea75634c05bf89cf752da3813d17437b805767` and X03 both find no qualified same-person CAN011→later CAN008 read. X03 does not overclaim. |
| C27 | CAN_012/CAN_011/CAN_010/ADP_007 are documentary authority evidence; no native grant | **AGREE_SCOPED / AUTHORITY HOLD** | CAN_012 rejects age/global RNG/direct wound/rendered prose; CAN_011 rejects demographic seeds; ADP_007 rejects demographic destiny. They are documentary, not a production/native grant. |
| C28 | M09/M11/M13/M14/M16/M18/M19 overall `PARTIAL_WRONG_MEANING` | **AGREE_SCOPED** | Each has at least a real carrier/arithmetic; the required actor-relative formation/transition/consumer is absent or wrong. Not a percentage and not a native law. |
| C29 | Proposed typed interfaces/operators are candidate only | **HOLD** | They are conceptual proposals; no competent issuer has issued them. X03 correctly labels them nonissuing. |
| C30 | X03's no-production/no-self-adoption claim | **AGREE_SCOPED** | No source/production file changed in the reviewed target; reviewer also made no source edit. |

---

## 2. What is genuinely established

### 2.1 Source/test identity

The historical source review is real. 35/35 declared files match byte-for-byte and 31/31 S50 selected files match. The reviewed X03 target has a coherent source map and the 71 focused tests are reproducible. The archive-level caveat is correct and must remain: the local re-zip is not the TD-R05 archive; file-level identity is the evidence.

### 2.2 Real retained machinery

The review confirms these are real source affordances, not merely names:

- **M09:** typed crack carrier, bounded event deltas, persistence, JSON, Pass-1/persona surfaces, degraded placeholder diagnostics.
- **M11:** framework persistence, acute/chronic operator, bounded per-field capacity/psych effect, dormancy record.
- **M13:** practice scalar carrier, bounded event deltas, downstream derived/persona/pressure-flow use.
- **M14:** two-year topology hysteresis with persistent counters and reset; one-step boundary motion with reversal gate; bounded coherence deltas.
- **M16:** persistent object identity, exact `striving_object_id` event seam, active/retired distinction, gift/disruption targeting.
- **M18:** typed shard/process carrier, event-to-shard seam, bounded wound increment via the age path.
- **M19:** persistent process carrier, raw/working cluster arithmetic, holding drain, JSON persistence, plasticity decrement.
- **Cross-mechanism:** the old code has fixed scalar/enum regime switches and some value-mediated route effects. They are not new learned relation edges.

### 2.3 Real defects confirmed

- M09 placeholder cracks are inserted as real active objects; Pass 1 hides them but `compute_metabolic_style` still includes them.
- M09 demographic/age seeding and future origin years are real.
- M11 frameworks are age/class/religion recipes; adult tenure is already chronic; domains ignore frameworks and practices.
- M13 practices are seeded before activity; labels/magnets/routed charge mutate them; no object/support/loss record.
- M14 topology/boundary are global enum/scalar transitions; no relation edge; boundary accepts event labels without actor access.
- M16 age/proxy spawn and unnamed RNG are real; no actual activity/support/recognition input; retired history is dropped.
- M18 age-band global RNG; severity/malheur mismatch; event path vs age path disagree; statuses/meanings stay empty.
- M19 statuses never transition; IRR/narrators/meanings/counters never update; cluster effects continue; malheur unreachable; second rupture overwrites the window; rendered prose is a causal input.
- Step-order descriptions overstate actual reads in domains/practices/strivings/metabolization.

---

## 3. Detailed corrections and falsifications

### 3.1 The 71-test receipt is accepted, the full-suite attempt is correctly not a pass

Independent command and result:

```text
RAWLSING_STAGING_ROOT=<source> PYTHONDONTWRITEBYTECODE=1 python3 -B \
  <X03>/TEST_SOURCE_AND_LOGS/run_v3_tests.py \
  v3/tests/test_metabolization_effects.py v3/tests/test_step_logic.py \
  v3/tests/test_v5_framework_dormancy.py v3/tests/test_invariants.py \
  v3/tests/test_wave4.py v3/tests/test_architecture_invariants.py \
  v3/tests/test_step_sanity.py v3/tests/test_llm_contract.py \
  v3/tests/test_v5_baseline_load.py v3/tests/test_v5_alienation.py
=> 71 passed in 16.96s
```

The tests establish historical source presence/arithmetic at their tested grain. They do **not** cover the central semantic claims: rupture admission, metabolization status/IRR/narrator transitions, framework acquisition, practice acquisition/support/loss, striving activity dependence, topology/boundary value cases, or current C9/C12. X03 says this correctly.

The full-suite attempt is a **NOT_COMPLETED** record, not a failure or a pass. RX03 did not run it. No claim of full-suite health is made.

### 3.2 M09 and M11: the carriers and fixed operators are real; the acquisition/lifecycle stories are not

**M09.** `update_cracks` (`v3/systems/cracks.py:25-61`) reads `events_this_year` and the `intensify_range` maximum only. `Crack.active` is written by `seed_cracks_from_identity` and `ensure_min_cracks`, not by the annual step. The default adult gets two active `placeholder` cracks (`invariants.py:253-274`); `compute_metabolic_style` includes all cracks in `crack_load` (`derived.py:180-181`), while `llm_contract.py:604-615` hides placeholders. The demographic seeder (`seed_frameworks.py:193-250,303-353`) creates cracks from religion/SES/minority/age and can produce a future `origin_year`. These are source facts.

**M11.** The acute/chronic operator is real (`frameworks.py:33-102`); a weight-100 framework with `half_life_years=2` produced binding 51.5, 53.0, 51.5 across three calls. The frames themselves are identity recipes with age-derived tenure (`seed_frameworks.py:54-186,257-300`); an adult 40 middle/dominant persona enters with tenures 34/32 and is already chronic. `update_domains` ignores frameworks and practices (`domains.py:50-56`); a high/low probe produced identical domains. `enforce_framework_caps` does not enforce `max_active=6`; `assert_frameworks_limits` exists as a year-end fail-fast (`invariants.py:163-174`). The proper wording is “no cap/selection in the cap function; a later assert can fail rather than cap.”

**M13.** Practice seeds and label/route mutations are real (`identity_to_backbone.py:374-405`; `delta_templates.py:161-219`; `flow.py:500-541`). The child/adult seed values reproduced exactly. There is no object, support, repetition, transfer or loss record; `update_domains` ignores practices. The scalar is not evidence of ability or enacted practice.

### 3.3 M14 and M16: fixed regime switches are not learned relations; two receipt corrections

**M14.** The two-call topology transition and one-step boundary reversal are real (`topology.py:14-99`; `boundary.py:20-80`). They are fixed scalar/enum transitions. There is no relation-edge creation, no cross-link, no actor-access receipt for an event-requested boundary, and no focused behavior test. `update_loop_topology` ignores event `loop_topology` hints. This confirms X03's distinction between a fixed regime switch and a newly learned relation.

Additional source defect not emphasized by X03: `_boundary_index` returns `2` for an unknown/corrupt boundary (`boundary.py:13-17`), silently treating it as `in_group`; `update_loop_topology` defaults an invalid current topology to `self_contained` (`topology.py:71`). These are hidden defaults, not observed actor states.

**M16.** The age/proxy spawn and unnamed RNG are real. `update_striving_step` calls `update_existing_objects` and `spawn_striving_objects_for_age` without an RNG (`striving_objects.py:242-272`); both create unnamed `random.Random()`. Five independent age-14 runs produced different object/value sets. This is nonreplayable from state.

**Precise corrections:**
- X03's exact five sets (meaning/eros; beauty/belonging; belonging/eros; justice/eros; beauty/justice) are not the sets in its own `probe_x03.json` and are not reproducible. The stable finding is “different object/value sets across runs,” not those literal labels.
- X03's “retired only at seed 1” is false. Its own `retire_seed_scan` and the independent rerun show remaining counts `[1,0,1,0,0,1]` for seeds 0..5, i.e. retirement at seeds 1, 3 and 4. Random retirement is real; the receipt is wrong.

### 3.4 M18 and M19: rupture admission and metabolization lifecycle are not implemented

**M18.** The event path creates a shard/process with status `raw` and does not touch the wound vector (`delta_templates.py:331-358`). The age path calls creation and `update_wound_vector_from_rupture` (`metabolization_effects.py:273-332`). A malheur-intensity event produces a process with severity `micro` because creation maps every non-major/shock intensity to micro (`:38`); the direct malheur wound bump changed abandonment 50→69, while create-only left wounds unchanged. The age path uses global `random.random/choices`; 14/20 seeds injected at age 14, with modes varying. No admission rule, exact parent, pre-state hash, actor basis or rule receipt is present.

**Correction:** X03 says persona reads nonexistent `metabolization_mode` “in two places, so that branch is always false.” Precisely, `persona_sheet.py:275` still emits the unresolved-rupture voice note (it only omits the mode text); `persona_sheet.py:754` (`_sacred_ruptured`) is the always-false branch. The display defect survives in narrower form.

**M19.** Creation sets `raw` and plasticity 1–3; the yearly step (`metabolization_effects.py:521-599`) decrements plasticity but never status. No source writer was found for `working/provisionally_narrated/integrated/sealed/chronic`. `narrators` is created empty and never populated; `intrusive_return_rate` is set at creation and never updated; `intrusive_return_rate_prev` stays 50; `meaning_attempts`, `provisional_frame`, `reactivation_triggers`, `sealed_candidate_years`, `post_plasticity_years`, and `start_plasticity_years` have no source producer. `downstream_biases` is written but no consumer was found.

Cluster deltas and biases are applied to `raw/working` processes regardless of plasticity; after three years the probe remains raw with plasticity 0. The exact bias values are mode-dependent; X03's 2→4→6 and −1→−2→−3 are one draw. Independent `collapse` mode produced betrayal 2→4→6, reality −2→−4→−6, plus attachment_guarding 2→4→6. The accumulation claim is stable; the exact numeric receipt is not.

`stability_inertia_dissipation` can drain holding, and a manually integrated status produces a larger drain (20→14.7735 vs raw 19.88675), but no generated process reaches integration; IRR-drop and sealed leak are inert on generated state. The malheur multiplier is not reachable through the generated path: creation maps malheur to micro, and the yearly call does not pass the `status_shock`/`isolation_spike` flags.

### 3.5 The urgent narrator-to-psyche edge

This is the most important finding and it survives independent challenge, with a precise boundary:

1. `render_year` itself is immediately nonmutating. After `compute_all_derived`, `render_year` leaves the backbone hash unchanged and writes only `rendered_output` (`render/phenomenology.py:55-156`; `test_architecture_invariants.py:51-67`). **AGREE** with X03's immediate-render distinction.
2. In the **next year**, `update_metabolization_and_plasticity_step` reads the persisted previous `state.rendered_output` (`metabolization_effects.py:541-575`), calls `_analyze_narrative_for_support_quality` (`:445-518`), which counts warm/coercive/accuracy words, and writes `state.narration_support`.
3. That `narration_support` then modulates `compute_metabolization_delta` (`:358-424`) and changes `state.psychological_capacity` and `downstream_biases` for `raw/working` processes. It is also used at creation for mode sampling (`:91-122`, `:187`).
4. At sourcefree grain, warm vs neutral rendered prose with one raw process produced warmth 30 vs 20 and aperture 55 vs 54. With no process, both remained at 50/50 psychological capacity; the narrator text alone did not change capacity. With `_analyze_narrative_for_support_quality` monkeypatched to constant `(50,50,50)`, warm and neutral both produced aperture 54; the difference disappeared.

**Verdict:** `AGREE_SCOPED` that the source has a narrator-text-to-psyche causal edge. **REVISE_PRECISE:** it is not inside `render_year`; it is a next-year read, requires a `raw/working` process, and the "narrator" is LLM prose keyword statistics, not an actual narrator/support record. This violates the source's stated render-only intent and CAN-012's `rendered narrative keyword -> NarrationSupport` `REMOVE_REJECT` disposition.

**Legally admissible alternative:** if a narration or story is itself an actor-accessible care/relationship event, it must be admitted as an exact generated/admitted V3 event with source/parent/permission; support must come from actual narrator/relationship/practice refs. Otherwise the rendered text should be noncausal. The old keyword counter is not a lawful substitute.

### 3.6 RNG, replay and the exact receipts

- `maybe_inject_rupture_at_band_age` uses module-global `random.random/choices` (`metabolization_effects.py:273-332`).
- `create_rupture_shard_from_event` calls `_sample_mode_from_priors_and_support(..., state.narration_support)` with no RNG; the helper creates `random.Random()` (`:91-122`). The same state can produce different modes.
- `update_striving_step` passes no RNG to `update_existing_objects` or `spawn_striving_objects_for_age`; both create `random.Random()` (`striving_objects.py:216-272`).
- Five age-14 strivings runs differ; retirement seed scan is `[1,0,1,0,0,1]` remaining for seeds 0..5. This is source nonreplayability, not merely test-only randomness.
- X03's exact object sets and “seed-1-only” retirement wording are **not** stable receipts. The nonreplayability finding is stable.

### 3.7 Current consumer and authority

X03 says current integration is `UNTRACED`; RX03 agrees. RC's static review (`ddea75634c05bf89cf752da3813d17437b805767`) remains the current-consumer evidence: S42 default-path synthetic predicates, S49 empty natural B root/controlled `PRIOR_B_REFUSAL`, S48 one-call transport, S52 withheld, no qualified same-person CAN011 formation → later CAN008 semantic value read. X03 does not promote any historical fixture to current personhood. No native source/actor/C8/C9/C11/C12/Pyat grant is implied.

The CAN-012/CAN-011/CAN-010/ADP_007 authority records are correctly used as documentary dispositions. CAN-012 explicitly rejects age-band/global RNG, direct wound mutation and rendered-text support; CAN-011 rejects demographic-to-psyche seeds and placeholder minimums; ADP_007 rejects demographic destiny/midpoint defaults. These are not production adoption or current native issuance.

---

## 4. Positive, NO_CHANGE/alternative and severed-edge evidence

### 4.1 Causal positive (sourcefree, historical)

- **Framework operator:** synthetic weight-100 framework, half-life 2: binding 51.5 → 53.0 → 51.5 (acute → chronic). This is a real fixed operator, not a learned relation.
- **Topology hysteresis:** `self_contained` with network 60/organizing 60: counter 1 then `reciprocal` on call 2.
- **Narrator edge:** raw process + warm prose → aperture 55; same state + neutral → 54. This is a real source-to-psyche edge at historical sourcefree grain.

### 4.2 Lawful NO_CHANGE / external-support alternative

- **No process:** warm vs neutral rendered prose with no `metabolization_process` left psychological capacity at 50/50/50/50/50. The narrator signal changed but there was no metabolization target. This is a **sourcefree no-target no-change boundary**, not a native CAN012 `NO_CHANGE`; a competent owner must issue the latter.
- **External support alternative:** if a later change is caused by actual support from a caregiver or institution, that is not proof of an internal metabolization transition. The correct system must be able to represent “support changed, process unchanged” and “process changed under exact rule” separately. X03's proposed NO_CHANGE cases are conceptually correct but not native-run.

### 4.3 Severed upstream fault (tested, sourcefree)

- **Exact edge:** `_analyze_narrative_for_support_quality` in `update_metabolization_and_plasticity_step`.
- **Intervention:** monkeypatch the function to constant `(50,50,50)` for both warm and neutral scenes.
- **Result:** both conditions produced aperture 54; the warm-vs-neutral difference disappeared while the raw process and state were otherwise fixed.
- **Label:** sourcefree severed **reader** fault, not a production fault injection and not a native E1→E2 semantic consumer. It falsifies the claim that the difference under warm prose is independent of the narrator reader; it does not establish a human law.

A true same-person C9/C12 positive/NO_CHANGE/severed-edge remains **NOT_RUN**; the proposed design is in §6.

---

## 5. Three separate court verdicts

### 5.1 ENGINEERING

**`ACCEPT_SCOPED_WITH_PRECISE_CORRECTIONS`.**

- 35/35 declared source hashes exact; 31/31 S50 selected exact; 71 focused tests reproduced; X03 source map and major behavior claims largely correct.
- Real retained: M09/M11/M13 carriers and bounded arithmetic; M11 acute/chronic; M14 hysteresis/boundary; M16 object identity/event targeting; M18 event-to-shard seam; M19 process carrier and holding drain.
- REDs confirmed: placeholders/demographic seeds; no crack/framework/practice/striving lifecycle; age/proxy strivings; global/unnamed RNG; rupture severity/path inconsistency; empty metabolization statuses/IRR/narrators; rendered-text psyche causality; no focused topology/boundary/metabolization tests; step-order overstatement.
- Corrections required: M16 exact sets/retirement receipt; M18 persona branch wording; M19 exact bias receipt; M11 active-count nuance; M14 hidden invalid-value defaults.
- **Current integration: UNTRACED; no C9/C12 consumer executed.**

### 5.2 SCIENCE

**`HOLD / RULE_UNISSUED`.**

- X03's conceptual differential is accepted as a source-grounded requirement, not an empirical law.
- No coefficient, age bracket, mode prior, status ladder, plasticity window, malheur multiplier, inertia drain, retirement probability or operator scale is promoted.
- Competing accounts remain: historically formed context-sensitive organization; current situated response without durable state; narrative/analyst description; plural/contradictory organization. The old code cannot distinguish them.
- The narrator-to-psyche edge is a real source mechanism but not evidence that narrated care should become causal. The lawful alternative is exact admitted events/support refs, not keyword counts.
- No native same-person semantic read, no actor-access memory, no empirical validation.

### 5.3 AUTHORITY

**`NO_NATIVE_GRANT / CURRENT C9-C12 HOLD`.**

- Original V3 is historical read-only evidence. No native actor/source/rule/CAN/ADP/Pyat/C8/C9/C11/C12 permission is used or inferred.
- CAN_012/CAN_011/CAN_010/ADP_007 are documentary dispositions, not a production grant. X03 correctly does not issue or implement.
- Current S39–S52/C9/C12/Pyat status remains outside this review; RC's static consumer hold is incorporated, not overridden.
- No production implementation, source edit, atlas/sequencer write, PR merge or self-adoption.

---

## 6. Proposed first real same-person test (design only, NOT_RUN)

**Inputs:** one actor with an exact admitted CAN-012 rupture, a `raw` process, exact later support/narrator refs, an independent later E2, and a current C9 readset. The test must vary only the actual support/narrator edge, not the rendered prose.

**Positive:** the actor receives actual later support from an exact caregiver/practice/narrator; a CAN-012 rule establishes a `WORKING`/`PROVISIONAL_ORGANIZATION`/`INTEGRATED_WITH_RESIDUE` transition; a later same-person C9 semantic read differs in the scoped relation/meaning.

**Lawful NO_CHANGE:** no exact later parent/support/rule; the process remains `RAW`; C9 reads the same semantic values; the result is a `NO_CHANGE` receipt under an issued rule, not `HELD_MISSING_RULE`.

**Severed upstream fault:** sever only the actual support/narrator→process edge (not the world, actor, E2 or current C9 code); the process must remain `RAW` and C9 must not show the earned difference. Restoring the edge must restore the consequence in replay.

**Alternative:** external support changes the actor's feasible action without any internal process transition; C9 may differ for that external reason. The system must label the cause, not attribute it to metabolization.

**Required owners:** CAN012 for rupture admission/transition; ADP020 for named RNG; ADP021 for cadence; ADP016/017 for memory/access; C9/C12 for same-person semantic read; independent reviewer. X03/RX03 do not issue these.

---

## 7. FINDING → INTERPRETATION → NEXT ACTION → ACCOUNTABLE OWNER

| Finding | Interpretation | Next action | Owner |
|---|---|---|---|
| X03 source map and 71 tests largely reproduce; 35/35 hashes exact | Engineering evidence is credible at historical sourcefree grain | Preserve X03 as scoped evidence; correct the four precise receipts before disposition | X03 author / HQ intake |
| M16 exact object sets and “seed-1-only” retirement are wrong | Receipt error, not a mechanism reversal; nonreplayability is real | Correct the dossier text to “different sets across runs” and “retirement at seeds 1,3,4” | X03 author / reviewer |
| M18 persona mode branch overstatement | The unresolved-rupture note still emits; `_sacred_ruptured` is the always-false branch | Correct wording; do not claim the entire persona branch is dead | X03 author |
| M19 exact bias numbers are mode-dependent | Accumulation is real; exact numeric receipt is not stable | Replace exact constants with “mode-dependent accumulation” and cite independent example | X03 author / reviewer |
| M11 “no active-count enforcement” is overbroad | `enforce_framework_caps` lacks cap; `assert_frameworks_limits` fails at year end | Correct to “no cap/selection; year-end assert can fail” | X03 author |
| M09 placeholders/demographic seeds; no tension lifecycle | Carrier is real, causal operation is missing/wrong | Remove placeholders/seeds; create event-parented tension lifecycle under CAN011/ADP015 | CAN011/ADP015; source owner |
| M11 frameworks are age/demographic recipes; domains ignore them | Operator real; acquisition/use/target missing | Create acquisition/use/scope/conflict/reactivation and real target consumer under CAN011/CAN010 | CAN011/CAN010; C9/C12 |
| M13 practices are seeds/labels/routes, not activity | Scalar is not ability or support | Create enacted practice record with object/support/loss under CAN011/ADP015 + SDTF/ADP | CAN011/ADP015; SDTF/ADP |
| M14 topology/boundary are fixed scalar/enum switches | Hysteresis technique real; relation/configuration missing | Preserve hysteresis; create scoped relation/configuration records under CAN011/ADP015/CAN008 | CAN011/ADP015; CAN008 |
| M16 age/proxy/random strivings and retirement | Object identity real; formation/support/history missing | Create activity/object/recognition/support formation under CAN010/CAN011; preserve retired history | CAN010/CAN011/ADP015 |
| M18 age-band/global RNG; severity/path mismatch; empty status | Rupture admission is not implemented | Create CAN012 admission with exact parents/pre-state/basis/rule; separate wound/target effects; named RNG | CAN012/ADP019/ADP020 |
| M19 statuses/IRR/narrators never update; prose causality | Process carrier real; multi-year lifecycle absent | Create CAN012 transition/NO_CHANGE with actual support refs; remove prose scoring and annual auto-accumulation | CAN012/ADP020/021/016/017 |
| Current same-person C9/C12 consumer not proved | Historical source is not current person integration | Build E1→CAN008→CAN011→later CAN008 semantic read; independent B; source/actor rights | C9/C12 + CAN/ADP + Pyat |

---

## 8. Review limits and required future reviewer

### 8.1 Limits

- RX03 did not run the full V3 suite; the focused 71-test subset is the historical execution evidence. No full-suite PASS/FAIL is claimed.
- RX03 did not run current S39–S52/C9/C12/Pyat or any native person; the current-consumer hold is documentary/static from RC and X03.
- No primary scientific literature was re-read. The science court is a source-grounded differential, not an empirical validation.
- No raw respondent data, LLM/V2 run, source copy export or production change.
- The narrator probe is a sourcefree keyword/probe result, not a human developmental experiment; the no-process path is not a native `NO_CHANGE`.

### 8.2 Required future reviewer

An independent I2/I3 reviewer distinct from X03 and RX03 must review this return at the immutable return SHA. That reviewer must specifically:

1. reproduce the 35/35 identity and 71-test result;
2. correct or confirm the M16 retirement/object-set receipt and M18 persona-mode wording;
3. reproduce the narrator positive/no-process/severed-reader case;
4. inspect the absence of status/IRR/narrator producers;
5. inspect M11 active-count nuance and M14 invalid-value defaults;
6. verify the CAN_012/CAN_011/CAN_010/ADP_007 documentary use without inferring a production grant;
7. keep current C9/C12/native claims under separate owner authority.

Then competent owners must separately issue/withhold: CAN-012 rupture/metabolization transitions; CAN-011 framework/practice/crack/relation states; CAN-010 need/striving; ADP-020 named randomness; ADP-021 cadence; ADP-016/017 memory/access; C9/C12 and Pyat native rights. **No reviewer may turn this return into native law.**

---

## 9. Artifacts, provenance and remote verification

**Review artifacts:**

- `REVIEW_COURTS/RETURNS/RX03/00_REVIEW.md` (this file)
- `REVIEW_COURTS/RETURNS/RX03/INDEPENDENT_EVIDENCE.json`
- `REVIEW_COURTS/RETURNS/RX03/LOCAL_PROBES.md`
- `REVIEW_COURTS/RETURNS/RX03/REMOTE_READBACK.json` (added after push)

**Review target:** `e81dd633b419d35619014bdf99f894ad4f98c5a5`. **Sealed startup:** `9a2753a1e9f76e9fcfa0c76dba49ed0e6cabf2a2`. **Branch:** `agent/v3court-review-rx03-secondwave-r1`. **Final reviewer commit and exact remote readback:** reported in the handoff after commit/push; this file does not embed its own future SHA. No self-adoption, no production implementation, no original-source modification.
