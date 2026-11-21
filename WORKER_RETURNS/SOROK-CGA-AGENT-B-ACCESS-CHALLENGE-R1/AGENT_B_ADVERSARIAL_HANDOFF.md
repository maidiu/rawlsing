# SOROK CG-A — Agent B constructive counterstrike and adversarial handoff

**Status:** Agent B authored **SOURCEFREE_TEST_ONLY** corrective candidate, not acceptance, independent scientific issuance, human approval, or protected merge.  
**Original whole commission:** [#913](https://github.com/maidiu/rawlsing/issues/913), with single independent receiving [#914](https://github.com/maidiu/rawlsing/issues/914).  
**Agent A baseline:** [PR #917](https://github.com/maidiu/rawlsing/pull/917), exact challenged head `384d4a4ac4973b83187d9a1e160f6d085d6aae19`, itself based on [original CG-A author #915](https://github.com/maidiu/rawlsing/pull/915) `8248711fb8ba4ac07c0b0e6e7dfc4decce9352b7`.  
**Agent B revised artifact:** [PR #924](https://github.com/maidiu/rawlsing/pull/924), independent branch `review/sorok-cga-agent-b-access-qualification-20261112-r1`, code/test cut **`659cdcd82d4b7d60583122d43b2d4f427eef3ccf`**. The exact final PR HEAD MUST be read back after this documentary commit; only those source code/test bytes at the cited cut have entered the verification run.  
**CI evidence for that cut:** [GitHub Actions #43162492337](https://github.com/maidiu/rawlsing/actions/runs/43162492337). Inspect live status; do not presume final success from a green first step.

## 1. Exact revised artifact / immutable custody

- `WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/situated.py`: new `current_p3_actor_access(...)` and replacement of unqualified context-nonempty boolean with an exact current-evidence predicate when calling `qualified_p3_read`.
- `WORKER_RETURNS/SOROK-CGA-CAUSAL-BRIDGE-R1/test_bridge.py`: preserve all five first-agent positive and negative integration tests; correct one overbroad quiet-interval expectation and add `test_old_and_forged_sensory_cues_do_not_authorize_p3_activation`.
- This handoff file is documentary. No P3 `PsycheStore`, `test_rules`, `projections.activate`, P2 world writer, `BatchEngine`, `RecursionCycle`, P4 user/actor rights, source registries, Pyat original35 or protected PRE-MAIN changed.

**Comparison base:** exactly PR #917 head `384d4a4...`; do not compare only against original `#915` and inadvertently erase Agent A's repaired activation/contradiction/source checks. PR #924 must remain a child PR against #917 until a qualified receiver chooses otherwise.

## 2. Independently verified predecessor strengths

1. Agent A correctly identified the earlier `MEDIATOR{room:kitchen}` proof as synthetic psychological store mechanics, not a lawful world-owned home resource.
2. Agent A kept the P3 actor-state sidecar read-only at the P6 consumer; material/P6 writes remain under existing event/world owner.
3. Agent A repaired a real initial bug: raw B1 modes cannot be handed to P6 without existing `p3.projections.activate`, source registry check, time, role/relation and contradiction screening.
4. A *committed sourcefree outward cue* can give the injected P6 interpreter a bounded P3 readset, and the ordinary world writer can commit actor speech conditionally; same-world sever/restore distinguishes the sourcefree effect.
5. PR #917's [Actions #43160250903](https://github.com/maidiu/rawlsing/actions/runs/43160250903) passed 11 selected tests on prior exact code cut `38ecf93c7b1ad6c57a5c420d753eaeac6bb643f4`. Both final-head CI checks for `384d4a4...` were separately observed `success` before this counterstrike. Neither is independent semantic receiving.

These are earned scoped engineering strengths, not native CAN/ADP psychogenesis or actual independent parenting.

## 3. Exact defect established in the original bridge

Agent A's `situated.reconsider` calculated:

```python
actor_observed = bool(
    packet["recent_self_actions"] or cues or packet["recent_speech"]
)
```

But `recent_self_actions(session)` and `recent_speech(session)` are **near-term historical context buffers**. They are not limited to the currently admitted P6 interval. A preceding MOVE, REPAIR or perceived SPEECH can remain present during a later quiet WAIT even when no qualified current activity has occurred. `p3.projections._activation` uses `actor_observed` as a sourcefree access predicate for B1 mediators with `requires_actor_access: True`. Therefore historical context presence was being promoted into a *new observation/activation warrant*. A model could receive an eligible mediator merely because Nadia had perceived some earlier unrelated act. This is not a problem of scientific numeric coefficients; it is a source-access category error.

There is a second connected attack surface: a `receipt["outward_cue"]` in `situated.reconsider` was previously admitted into the P3 observation boolean without rechecking the event's exact committed `event_id/hash/clock`, the P6 sensory candidate and the current checkpointed conditions. A forged or replayed sourcefree cue could thus satisfy that coarse boolean if an untrusted caller passed a forged receipt. The normal `run_p6` code gets its cue from the sourcefree outward writer; the strengthened read boundary additionally checks the witness itself.

## 4. Correction implemented and why narrower is better

`current_p3_actor_access(session, interval, world, house, packet)` now separates the data used for *context* from what can be counted as *fresh access evidence*:

- A P6 outward cue must identify a committed world event with exact hash and timestamp, lie within the current stated interval, and equal the **rederived** `outward.sensory_candidate(event, world, house)` under current checkpointed sensory conditions.
- An actor-perceived encounter cue must bind an existing committed event and actual actor perception.
- A self-action must remain an actor-perceived and world-held self action *and* be strictly later than the current interval start; previous-context rows are retained in the packet but no longer unlock P3 activation.
- Accessible speech must bind a world SPEECH event and actual actor perception, also strictly later than the current interval start.
- No matching present evidence yields `actor_observed=False`; existing P3 `projections.activate` still decides eligible/inhibited/unknown/contradiction. This does not produce an ADP memory, durable trait or universal causal trigger matching law.

This is a narrow reuse-first change. No second scheduler or owner state, no added trait writer, no simulated mother, no widening of native authority.

## 5. Causal proof and preservation results

**Exact commands executed by GitHub Actions on the code/test cut:**

```sh
python -B -m pytest -q -p no:cacheprovider WORKER_RETURNS/SOROK-CGA-CAUSAL-BRIDGE-R1/test_bridge.py
python -B -m pytest -q -p no:cacheprovider \
    WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests/test_p3_vertical_slice.py::test_primary_actual_formation_read_later_and_no_mediator_control \
    WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests/test_p3_vertical_slice.py::test_h_cold_reopen_idempotent_replay_and_source_restore
python -B -m pytest -q -p no:cacheprovider WORKER_RETURNS/SOROK-P4-FIRST-FULL-MPC-R1/test_response.py::test_performed_speech_reads_real_prior_p3_formation
python -B -m pytest -q -p no:cacheprovider WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/test_house.py::test_outward_conduct_supplies_only_qualified_cues
python -B -m pytest -q -p no:cacheprovider WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/test_house.py::test_silent_interval_reconsiders_and_commits_only_admitted_speech
```

- **Positive:** the existing committed `APPROACH` sensory cue remains a source-qualified access case. Later injected sourcefree decision + actual P6 actor SPEECH remains admissible under actual world-writing mechanics.
- **Negative:** a quiet WAIT with inherited near-term self action/speech, but no newly qualified present evidence, now gets `NO_QUALIFIED_P3_CANDIDATES` rather than automatic old-mediator recruitment. The old context remains in the P6 situated packet and can still guide ordinary interpretation.
- **Forgery:** an exact-world event with a tampered event hash cannot qualify a sourcefree cue.
- **Stale replay:** a once-real `APPROACH` cue cannot be replayed into a subsequent interval to manufacture present actor observation.
- **Restoration:** the previous sourcefree positive/no-history and exact same-checkpoint bridge-sever/restoration tests are retained unchanged; when the actual present cue and reader are restored, so is the original positive behavior.
- **Regression scope:** inherited P3 cold and source restore, P4 historical first reader, P6 sensory and situated-time tests remain scheduled on the same CI run, with each outcome to be read from the run rather than assumed.

A passing CI stage establishes the code did what those test assertions check; it does not by itself prove human psychological validity, scientifically matched trigger semantics, or native actor rights.

## 6. Challenges investigated and rejected

- **“Every old self-action should count because duration matters.”** False at the access boundary. Duration makes history relevant context; it does not retroactively turn an older event into the actor's new perception. Old context is deliberately preserved in the packet.
- **“The entire P3 activation algorithm should be replaced.”** Unsupported. Its role/relation/obligation/source logic and contradiction screen are useful existing machinery; the defective input was the caller's coarse boolean. The correction preserves that machinery.
- **“The sourcefree test interpreter makes all behavior illusory.”** Too broad. The test interpreter's choice is stipulated, but the sourcefree readset's effects on the actual P6 admission and world event are executable and counterfactually testable. Claim no more.
- **“Building a second full parent/world scheduler would fix this.”** No. It would multiply owners and fail the specific witness-provenance problem.
- **“Any near-term context is equivalent to conscious memory.”** False, and neither implementation claims native memory issuance.

## 7. New attack surfaces / consequences

- The `current_p3_actor_access` predicate is still **evidence eligibility**, not project/counterpart-specific stimulus-to-mediator matching. An arbitrary *legitimate* current cue could activate a prior B1 sourcefree mediator if the existing rule selectors otherwise admit it. This is the strongest remaining semantic risk, and cannot be solved by inventing a native law.
- Binding some actor self-actions to `> interval.start` excludes same-clock un-cued self actions. This is deliberately conservative but should be challenged in future non-fixture actor-supporting contexts. An exact current-operation event receipt would be a better provenance primitive if available.
- A non-fixture P5 encounter cue qualifies through an actual perception stream; corroborating its original recipient/eligibility proof and source version should be audited if it is extended beyond this sourcefree scene.
- Calling the internal `qualified_p3_read(..., actor_observed=True)` directly remains a caller-trust surface; the corrected P6 production call uses the verified helper. A future public API must enforce the source proof at the trust boundary rather than rely on convention.
- Harder process-crash windows between P6 speech world admission and outer P4 turn receipt recovery are not newly proven here. Existing inherited crash coverage must be applied before claiming a durable end-to-end actor action product.

## 8. Surviving disagreements and honest authority grade

**Engineering:** sourcefree actor-access provenance repair, building on Agent A's actual P3→P6 injected-reader seam. If [Actions #43162492337](https://github.com/maidiu/rawlsing/actions/runs/43162492337) ultimately passes, receive at `S2_SOURCEFREE_TEST_ONLY_CANDIDATE`, pending one substantive independent review and PR merge decision. If a stage fails, `REVISE_EXACT_DEFECT`; do not assert blanket pass.

**Science:** original CAN008 Rule A, CAN011 Rule T, ADP016/017 formation, native psychogenesis, causal mediator-to-current-event matching, Pyat source and original35 issuance remain `HELD`. An engineered access predicate is not a new personality science rule.

**Authority:** no C12 native actor, respondent/source rights, human A5 permission, independently appointed review acceptance or protected merge. This branch does not modify Pyat or original-program denominators.

**Product:** no independent parent, materially dated household, rolling years or genuine generated root. Those belong to CG-B/C/D/E; they must not be demanded as acceptance of this bounded CG-A repair.

## 9. Challenge back to Agent A

Attempt to defeat this result **by a superior lawful construction**, not by merely finding a false positive in a toy interpreter:

1. Can you demonstrate a same-world case where a source-authentic current `APPROACH` or current actor-perceived speech is **irrelevant** to a previously acquired mediator, yet our use of `actor_observed=True` still recruits that mediator and changes P6 conduct? Then implement the smallest existing-owner source qualification that prevents the mismatch, without fabricating a universal psychological trigger law.
2. Find an accepted P4/P3 consumer that renders this P6 bridge redundant. If the old path can actually fulfill the same P6 situated/actor first-consumer function more simply, replace the new bridge and show positive/negative/restore parity.
3. Falsify the strict interval gate against an actor-performed self-action at the interval boundary that is genuinely part of the **same admitted operation**, and propose a source receipt or operation ID binding better than timestamp guesswork.
4. Attack crash/replay after `session.product.say` but before P4 outer receipt persistence; demonstrate whether original idempotence genuinely conserves world speech and P3 readset custody under that failure, not merely whether an isolated test stays green.

Do not demand that CG-A produce independent mothers, a real dated home or native rules: they are the next explicitly selected construction tranches. A sourcefree improvement should close at its earned grade while the product program advances.

**This return is a challenge, not its own acceptance certificate.**
