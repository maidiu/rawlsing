# Proposed implementation and falsification contract R1 — not adopted

**Status:** `SCHEMA_SKETCH_AND_QUALIFICATION_TEST_BANK__NOT_EXECUTED`. No new semantic authority, registered effect, production admission, numeric selection policy, or mandate to call an LLM.

## Two separately typed results of ONE API invocation

**Input:** exact `ContextBundleRef` for `S[n]` and `H[n]`: actor-safe event ledger, past state, memory/accessibility permissions, current objective material ecology, household/independent persons and source use rights. Input separates analyst causal detail from first-person renderable truth. No raw surveys, objective demographic prior→personal memory or unverifiable nested person-private fields.

**Output A: `RetrospectiveRenderProposal`** includes `interval_id`, `causal_checkpoint_ref`, `allowed_fact_refs`, `allowed_actor_memory_refs`, `text_or_scene_fragments`, `uncertainties`, `surface_inventions_only`, and `render_provenance`. It is an immutable `RENDERED_EXPRESSION_NONCAUSAL` proposal and cannot write an actor memory, event, relationship, inferred feeling, selected belief or fact. A later in-world artifact would require entirely separate ADP019 interaction admission.

**Output B: `ProspectiveEventProposalPacket`** includes `horizon`, exact input `checkpoint_ref`, `candidates[]`, `eligible_participant_refs`, optional explicitly proposed new-entity constructors, `possible_relevance_domains`, `prerequisite_claims`, `source_scope_refs`, `uncertainty`, `model_version`, `prompt_hash`, `sampling_metadata`. Each `candidate` is `LLM_PROPOSAL_NONCAUSAL`, not an admission, personal affect, guaranteed external witness or author-committed trajectory. All candidate set/rule/source hashes and owner decisions are recorded independently.

**One-call contamination hazard:** Co-producing A and B in a single autoregressive model pass does NOT guarantee semantic independence. B may reuse a name or invented event from A even when the schema separates them; future anticipation may likewise contaminate A's retrospective description. Thus mandatory source-backed ref checks, fact and psyche claim validators, prompt ordering and cross-field independence tests are more important than merely naming two JSON keys. For a grounded retrospective fact, require exact V3 owner-backed fact refs; new surface color remains ungrounded/surface-only or must be stripped. A future proposal referencing render-only inventions must DENY or undergo a separately issued new-entity/event route. No self-proposal authorizes its own source.

## Inside each interval: event-time loop, not annual aggregate delta

At each time trigger, ordered by actual causality and event/source clocks:
1. `context = re_resolve(world, actor_position, now)` with all required Pyat/SDTF source, permission, applicability, effective/published/observed/actor-exposure distinctions. UNKNOWN is not ABSENT and feasible is not known/attempted.
2. Validate remaining proposed event prerequisites against **current** actor/world/other-actor state; an invalid future candidate is not forced, and no LLM-authorized fallback may produce a fabricated event.
3. Competent independent event owner accepts or refuses the exact objective event/witness. Speaker performed action, actor listening/exposure and actor's interpretation remain separate. Actor-specific practical options can be computed without any psychic selection or narrative.
4. Competent CAN008 event-time rule yields lawful candidate response/effect/refusal; CAN011, ADP016/017 or independent world/relationship owners **separately** qualify and commit durable effects. A no-change can leave actor causal state identical while separate audit receipts are recorded.
5. Continuous slow-process integration advances under the governed hybrid scheduler between events; transition/event/ledger/checkpoint hashes persist and are cold replayable. Earlier objective events and other people's independent histories cannot be retroactively edited.
6. At a material disruption, invalidate affected future proposals, then permit an explicitly policy-governed extra proposal call if qualified and beneficial. A new proposal cannot retcon elapsed time; no automatic re-roll until a desired plot appears.

`possible_relevance_domains` are *questions for the actual existing actor causal mechanisms*, not direct axes to increment. No fixed trauma vs healing, recognition vs constraint, demographic→belief, ennea-type-at-birth or universal route-to-desire rule. Changing only an analyst label must not flip the material developmental outcome. Future accepted uptake/learning must rest on a separately tested explicit scientific rule, not an LLM-selected `effects` field.

## Minimum sourcefree comparative experiment (future commission, not yet performed)

Use a fixed constructed world, two independently materialized actors/parents with distinct prior witnessed activity, identical relevant demographics/structural prior, common seeded potential encounters and a second independent person able to refuse. At least 3 events within a one-year interval: one event that changes actual practicability, one event that can only be decided after that change, one event with genuinely unaffected/valid-empty possibility. Include ordinary positive/nontraumatic life: a new activity, friendship, material opportunity, successful project and/or move. Never force an event count or psychological change merely to complete the fixture.

**Three arms with identical actor/source/rule/seed inputs, and identical owner eligibility:**
- `ONE_CALL_COMBINED`: two typed outputs from one model call; processing and next call after real V3 computation.
- `TWO_CALL_BASELINE`: proposal and render in separate calls under the same owner rules; test whether one call reduces overhead without corrupting content.
- `PURE_FIXED_PACKET`: same proposal/render shape, controlled deterministic sourcefree fixtures, no provider call, to independently validate contracts and cold replay.

**Evaluation measures**: actor/world exact replay and provenance; cross-output hallucination contamination; rate of admitted, refused, invalidated and valid-empty events; different lawful histories producing different possible actions without label-only dependence; independent-other refusal; correct first-person knowledge filtering; no pre-event future leakage; source/currentness coverage; cold restart; time and provider cost, including total tokens and output quality. Compare at several interval cadences (annual and six-/three-month where warranted), not by assuming more calls are scientifically better.

**Adversarial invariants to execute:**
- R01: a retrospective invented teacher name becomes a proposed later encounter → reject unsupported referent, no actor/world event.
- R02: an invented betrayal in retrospective prose attempts to update resentment → reject.
- R03: changed render wording only leaves exact V3 causal hash/next admitted event invariant; source-free prospective packets compared under pinned inputs (under stochastic LLM, test provenance and empirical rate, not false byte equality).
- R04: event 1 move invalidates a geographically impossible later encounter; no forced replacement.
- R05: event 1 successful practice genuinely changes capabilities available at event 2 **only under independently admitted scientific update rule**; otherwise DEFER not imaginary learning.
- R06: candidate no-event or all rejected → lawful empty interval and continuing background time, no fallback event.
- R07: at same observed words, different witnessed parent/child practice histories produce distinct evidence/recruitment sets, not mandatory emotions.
- R08: identical practice/interaction, cosmetic `recognized_plan` label changed → no authoritative psyche change.
- R09: change history while maintaining actor demographics/country prior → cannot infer identical response solely from demographics; without rule, evidence changes but psychological choice stays UNKNOWN.
- R10: speaker performed speech without listening exposure → child cannot automatically know or believe it.
- R11: independent other changes project/refuses → child cannot authorize other's consent/interaction, including desired romance.
- R12: externally witnessed adoption of a habit followed by contradictory conscious appraisal → preserve separate channels, no forced cognitive harmony.
- R13: last-year narrative cannot influence earlier event clocks or be retroactively called witnessed.
- R14: use mismatch in source, missing actor position or missing probability authority → fail closed/DEFER; no cohort prior projected as person probability.
- R15: original immutable event/personal prestate and independently computed next checkpoint cold replay after process restart exactly.
- R16: model emits unauthorized `CAN011_UPDATE` / `ADP016_MEMORY` field → reject without effect.
- R17: combined call worse at cross-output contamination versus separate-call control → retain two-call fallback; performance/price alone cannot override science.

Every case must report machine `PASS/RED/NOT_APPLICABLE`, actual imported modules, owning rule, evidence grade and remaining claim ceiling. A passing mock must not be called an independent native CAN008 positive, Pyat source qualification or human behavioral validation.

## Research → decision gate

Implement **no new psychology** here. First perform the sourcefree scheduler/JSON schema and contamination differential while HQ330 finishes B3 independent X3/S3 and M2 M4/next I2. The B3 engine's future legitimately issued CAN008/CAN011/ADP016/017 rules plug in only after source/owner acceptance; if they are absent, return explicit valid-empty/deferred. Any comparison using a paid model needs explicit provider/access permission, version capture and measured budget. Production PREMAIN/CURRENT, survey sources and actor/signer registries are not touched.

**Important:** The objective is preserving the original *two logical roles*, not forcing a `two-call` physical runtime. A genuine output-quality or provenance regression is grounds to restore separate calls, use a dual-branch prompt or issue narrower adaptive calls. Do not canonize a cost optimization ahead of scientific verification.
