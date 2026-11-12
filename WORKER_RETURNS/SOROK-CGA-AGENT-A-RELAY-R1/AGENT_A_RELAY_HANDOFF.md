# CG-A adversarial relay — Agent A constructive counterstrike against Agent B

## Identity and immutable code custody

- Original whole CG-A: [Issue #913](https://github.com/maidiu/rawlsing/issues/913); one independent receiving: [Issue #914](https://github.com/maidiu/rawlsing/issues/914). The original four duties remain `CGA-P3-ABI`, `CGA-POSITIVE-CAPITAL`, `CGA-COLD-LATER-READ`, `CGA-CGB-CD-CONTRACT`.
- Initial author [PR #915](https://github.com/maidiu/rawlsing/pull/915) `8248711fb8ba4ac07c0b0e6e7dfc4decce9352b7`; Agent A [#917](https://github.com/maidiu/rawlsing/pull/917) `384d4a4ac4973b83187d9a1e160f6d085d6aae19`; Agent B's valid counterstrike [#924](https://github.com/maidiu/rawlsing/pull/924) **final** `0213c844b26a8e69afeea6e499fea46e13444c69`. Agent B's final-head CI was reported successful [#43162941345](https://github.com/maidiu/rawlsing/actions/runs/43162941345).
- This round's private writer branch: `review/sorok-cga-agent-a-relay-20261112-r1`, created **from the exact B final HEAD**, not rewriting B's branch or PR. Substantive code/test cut: `618950bdf1a4c53aacb9a0eba7a6c06b744911d6`. Final resulting PR HEAD must be independently checked at receiving.
- Changed paths at code cut: `WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/situated.py`; `WORKER_RETURNS/SOROK-CGA-AGENT-A-RELAY-R1/test_cue_issuer.py`; `.github/workflows/sorok-cga-agent-a-relay-r1.yml`. This handoff is an additive documentation change, not a test-code modification.
- Sourcefree S2 only, no protected merge, no replacement owner, no native psych rule or respondent/human permission.

## 1. Agent B's genuine victories — preserved verbatim in semantics

Agent B proved that the old `bool(recent_self_actions or cues or recent_speech)` promoted historical context into fresh actor access. B also proved that a once-authentic sensory candidate must not be replayed as a new current one. Both corrections remain in this branch: actor-local interval qualification, real event identity, rederived `outward.sensory_candidate`, ordinary context retained without automatic activation, and existing P3 `test_rules._check_sources` / `projections.activate` eligibility/contradiction semantics. Agent B's six bridge tests are unchanged, not removed to manufacture a passing result.

## 2. A false *completion claim*, not a false diagnosis

B described its remaining actor-access condition as source-checked current evidence. For nonfixture cues its exact code nevertheless accepted an event by actor-perceived `event_id` plus caller-supplied `modality` / `channels`; `event_hash` was optional. A committed actor-perceived event is **not** proof that anybody issued the *claimed sensory cue*. A forged `AUDITORY` row attached to a real world event, never produced by P6 sensory/encounter code, returned `True`. [Reproduced RED in CI #43164818810](https://github.com/maidiu/rawlsing/actions/runs/43164818810): `test_world_real_perceived_event_cannot_become_forged_sensory_cue` failed `assert True is False`. This does not invalidate B's authenticated outward-cue protection; it shows that the nonfixture fallback bypassed it.

B's surviving diagnosis of missing scientific cue-to-specific-mediator matching is **valid**. The corrected current-provenance guard is a necessary condition, not sufficient psychological science.

## 3. New defects and causal consequence

**(A) Nonfixture sensory claim laundering.** The perceived-event plus modality shortcut admitted fabricated access even with no `P6_MOVEMENT_EVIDENCE` producer and no full receipt. It could hand sourcefree B1 modes to the model via `actor_observed=True`.

**(B) Operation lineage absence.** Even a legitimately rederived outward cue was checked against *world state*, not the just-executed P6 operation's `receipt.performed` plus its `P6_HOUSE_CONDUCT` episode. A stale or transplanted cue at an ambiguous timestamp remained a caller-trust surface.

**(C) Forged recent context.** Prior self-action or speech source readers were used to construct packets, but the helper itself could be invoked with modified rows pointing to real event IDs. It did not compare those rows against its original actor-local source reader.

**(D) Missing world half of activation evidence.** The P3 readset held historical mediator record hashes and context hash, but a downstream forensic reader could not see *which present world event* warranted the current actor access boolean. That is a real transitive source/readset gap, distinct from relevance matching.

**(E) Outer receipt crash window.** `run_p4.act` durably writes `ledger.pending` before conduct, and actor speech may commit before `ledger.turns` is persisted. It cannot be declared a completed exactly-once turn solely because request_id deduplication exists on completed turns.

## 4. Construction implemented

1. **Delete the unverified nonfixture cue shortcut**. For a sourcefree P6 outward sensory candidate, require `cue == source_receipt.outward_cue`, `source_receipt.performed == session.event(event_id)`, true actor/user/clock/event hash, `sensory_candidate` rederivation against actual checkpointed house, and a recorded `P6_HOUSE_CONDUCT` parent for that event/operation. `P6_MOVEMENT_EVIDENCE@1` with `HOLD_ACTOR_REGISTRATION_OWNER_MISSING` does **not** confer actor-observation authority just because visual eligibility was listed.
2. **Keep exact actor-source readers**. A current self-action or speech row must equal a row re-emitted by `recent_self_actions(session)` or `recent_speech(session)` at that same read cut. Registered perceptions are compared by exact `(event_id,clock)`, not event ID alone. Strict `>interval.start` on prior-context rows remains B's conservative rule.
3. **Separate historical and present readsets and persist the private causal receipt**. Keep `P3.readset` as B1 mediator hashes; add `sourcefree_p3.actor_access_evidence` with `(event_id, event_hash, clock, issuer basis, SOURCEFREE_TEST_ONLY)` and `sourcefree_p3.world_readset` with actual current world event hash. The parent P6 packet hash binds both. More importantly, `reconsider` also returns `receipt["situated"]["sourcefree_p3_receipt"]`: root/branch/clock, pre-action world-state hash, P3 activation context hash, distinct P3 and world readsets, and exact source evidence. Cold reopen verifies this readset against the world event and P3 store, while public surface rendering excludes the private receipt. `stimulus_to_mediator_relevance=UNISSUED_NATIVE_RULE` explicitly blocks an interpretation of this engineering warrant as native Rule T/CAN/ADP psychological equivalence.
4. **Fault-inject the dangerous crash window**. `test_crash_after_world_speech_commit_holds_retry_without_duplication` raises *after* the actual P6 actor speech is admitted but before P4 outer receipt persistence, then confirms the pending guard refuses retry and no second world speech or P3 write appears. This is fail-stop evidence, NOT successful reconciliation.

## 5. Regressions / negatives / execution

From an isolated checkout of the exact immutable code cut `618950bdf1a4c53aacb9a0eba7a6c06b744911d6`:

```sh
python3 -m pip install pytest
python3 -B -m pytest -q -p no:cacheprovider WORKER_RETURNS/SOROK-CGA-AGENT-A-RELAY-R1/test_cue_issuer.py
python3 -B -m pytest -q -p no:cacheprovider WORKER_RETURNS/SOROK-CGA-CAUSAL-BRIDGE-R1/test_bridge.py
python3 -B -m pytest -q -p no:cacheprovider WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests/test_p3_vertical_slice.py::test_primary_actual_formation_read_later_and_no_mediator_control WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests/test_p3_vertical_slice.py::test_h_cold_reopen_idempotent_replay_and_source_restore
python3 -B -m pytest -q -p no:cacheprovider WORKER_RETURNS/SOROK-P4-FIRST-FULL-MPC-R1/test_response.py::test_performed_speech_reads_real_prior_p3_formation
python3 -B -m pytest -q -p no:cacheprovider WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/test_house.py::test_outward_conduct_supplies_only_qualified_cues WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/test_house.py::test_silent_interval_reconsiders_and_commits_only_admitted_speech
```

The first complete code cut `58687a7ed865f8a8809e278b981e73cac94b057d` passed all 17 selected tests in [GitHub Actions #43166066244](https://github.com/maidiu/rawlsing/actions/runs/43166066244) (5 new + 6 B bridge + 2 P3 + 1 P4 + 3 P6). The later change persists the private first-consumer receipt and asserts cold-reopened issuer identity; **verify its separate exact-code/head run** before promoting that stronger claim. The source and test diff after that cut is bounded to the private receipt and corresponding provenance assertions. Baseline B CI was green at its separately frozen HEAD. The initial RED source-real forged-cue test is a real pre-fix execution, not an invented hypothetical. Do not confuse passing authored CI with an independent reviewer identity.

## 6. Original CG-A obligations conserved

- `CGA-P3-ABI`: no P2/P3 root/actor/clock/registry change, no second scheduler or new writer. The bridge retains identical P3 activation semantics.
- `CGA-POSITIVE-CAPITAL`: B1 remains TEST_ONLY. Previous exact historical 23-row matrix custody (21 inspectable tuples) is not reclassified. Historical B3A/HQ300/M01/C9RI source values are NOT silently imported or proclaimed native.
- `CGA-COLD-LATER-READ`: authentic world cue + exact P3 mediator can still reach actual P6 situated consumer at sourcefree grade; same-world read-edge severance and source-severance negatives retained; newly source-bound world activation witness distinguishes present event from old mediator. Actual P4 deterministic speech response remains the existing source-specific B1 consumer.
- `CGA-CGB-CD-CONTRACT`: P2/P6 material truth and speech stay with world owner, P3 psyche records remain actor-sidecar TEST_ONLY; no new batch engine, mother actor, calendar or source authority issued.

## 7. Unfulfilled requirements, authority ceilings and precise reasons

- **Meaning relevance:** An exact valid present `APPROACH` event can still activate an old mediator under the B1 generic `requires_actor_access` predicate even though no native rule proves this event relevant to that particular historical mediator. We **did not invent a relevance rule** to cover it. Recording `UNISSUED_NATIVE_RULE` is honest evidence hygiene, not a behavioral exclusion mechanism. Actual native Rule T/ADP and a material situation-to-mediator crosswalk remain needed.
- **Direct internal caller:** `qualified_p3_read(actor_observed=True)` may still be called by code with raw owner access, bypassing the P6 proof helper. This is a trust-boundary design risk for future public interfaces; current P6 path is qualified.
- **Crash reconciliation:** Confirmed fail-stop and absence of duplicate actor speech on retry, but `P4_PENDING_OPERATION_REQUIRES_RECONCILIATION` can leave the foreground blocked. A safe repair needs a transitive, complete P4 turn reconstruction protocol including after-state/foreground witness/public output; clearing pending blindly would lose causal history or double-act. None is claimed here.
- **Same-clock current self actions:** B's strict `> interval.start` holds ambiguous same-clock self-actions. This relay repairs current *outward* operation provenance with event/episode/receipt, but no generalized S46 parent receipt for all other same-clock acts.
- **Full product:** No independent parent, dated material home, child-perceived mother speech, CG-B/C/D/E function, C12 generated root, operated S14/A5 rights, original CAN008/011 or ADP016/017 issuer, Pyat scientific permission, or protected PRE-MAIN merge.

## 8. Alternatives rejected and challenge returned

- **Trust `event_id`+modality:** disproved in RED CI; a true world event does not issue its own auditory cue.
- **Treat every perceived event as a B1 trigger:** conflates present source-qualified perception with specific historical plan relevance; B already showed stale evidence is wrong.
- **Invent a universal stimulus-mediator matching psychology:** unavailable native source/authority and contrary to reuse-first instruction. Use exact world/readset provenance as a lawful precursor, not fiction.
- **Replace P4/P3 source-specific B1 path:** existing `read_response` already constrains speech `request_edge` and original event perception and has an inherited green test. There is no evidence the optional P6 bridge supersedes it.
- **Clear a crash `pending` flag and retry:** risks duplicate speech and false receipt. Fail-stop is preferable to ungrounded auto-heal until genuine world/ledger reconciliation is constructed.
- **New person/world scheduler:** duplicates P2 owner and accepted BatchEngine/RecursionCycle, does not solve source-issuer tampering.

**Best next adversarial attack:** produce an independently authenticated *current* but irrelevant cue and trace a B1 mode into a sourcefree P6 model's action; prove or build a lawful narrower same-task binding. Then attack same-clock receipt/replay under an authentic but different operation and the internal direct-boolean P3 caller. No reviewer is authorized to promote this branch into protected adoption merely because these tests pass.

**Disposition:** construction delivered on isolated child branch, S2 SOURCEFREE candidate **pending final-head executable verification and separate #914 receiving**. Never self-APPROVE; do not merge protected branches.
