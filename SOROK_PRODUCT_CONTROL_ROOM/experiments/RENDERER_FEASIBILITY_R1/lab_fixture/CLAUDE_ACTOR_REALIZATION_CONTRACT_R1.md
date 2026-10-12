# RFA-05 — Claude-class actor realization contract (laboratory R1)

**Status:** one-shot proposed actor/world occurrence experiment, **not** canonical production V2/V3/PFF or an Anthropic API run. Hand-authored source: HAND_AUTHORED_LAB_SURROGATE_ONLY. Reconciled input schema: `SOROK_PRODUCT_CONTROL_ROOM/experiments/RENDERER_FEASIBILITY_R1/RFA_R_RECONCILIATION_R1/LABORATORY_TURN_TARGET_SCHEMA_R1.json@e65846bbb1c38a366d79b54bb89be47da0f8502e`.

## One-shot target and trust partition

One high-capability model call receives ONLY a compiled **actor-safe projection** from each RF file's `expression_action_constraints.value.actor_safe_projection` plus independently filtered actor-accessible world affordances and the exact user event. The evaluator has the complete canon, including objective falsehoods, actor-private material, hidden recruitment and scoring oracles; these are **not passed to the model wholesale**. The downstream user-phenomenal compositor is **out of scope**. In particular, the model must never receive the `status_and_provenance.value.evaluator_only_oracle` or `can008_recruitment.value.evaluator_only_hidden_causal_summary` as narration prompts.

The model shall **propose** a single bounded Nadia objective outward occurrence in one response with the exact `OBJECTIVE_OCCURRENCE_OUTPUT_SCHEMA_R1.json` shape. It must not claim that the candidate is already admitted. Silence or ordinary nonresponse is valid when compatible; a silence atom is not secretly narration. No verifier/rerender model loop is assumed. A deterministic/local laboratory admission gate may accept exact compatible atoms or reject/hold; this remains provisional under Sorok 101 versus CAN-022/ADP-019.

## Binding invariants

1. **Noncontradiction:** never contradict immutable seed, branch history, allowed current world or verified limits. Differentiate objective facts, actor beliefs and user assumptions.
2. **Reasonable extrapolability:** a small response must be plausibly from *this* Nadia, not just a generic agreeable adult. Prior ordinary episodes and context-specific organization matter.
3. **Relation specificity:** honor branch-private RF009 relationship incidents without retroactively editing precontact root, and preserve RF008/RF009 exact speech equivalence.
4. **Actor epistemic limits:** do not expose objective truth unknown to Nadia; no knowing the revised hall sign while not observing it; no P0 mind-reading; no third-party private mental contents.
5. **Lawful lying and error:** a knowing lie is not transformed into an innocent lapse or compulsory confession; sincerely believed error is not silently fixed by an omniscient narrator. Correct claims, false claims and withholding remain separate.
6. **No hidden-cause exposition:** causal organization can influence actions without visible tells, self-psychologizing or a narrator naming the hidden cause. No obligatory blush, twitch, hesitation or therapeutic insight.
7. **Exact speech identity:** the `SPEECH.content` bytes must be unchanged in prose quotation, in order, without adding extra speech; any mismatch is a hard failure. Speech represents **utterance**, not guaranteed propositional truth.
8. **Bounded time and matter:** at most thirty seconds and only listed objects/surfaces/capacities. Proposed previously latent particulars are marked `UNAUTHORIZED` or `DEFERRED` and are not rendered as facts.
9. **No invented biography/history:** no retrospective dates, promises, emotional revelations, events, relationships or skills absent from source facts.
10. **No user-phenomenal personalization:** render only outward Nadia action at the objective layer; never decide what P0 noticed, felt, imagined, heard or recognized. User attention cannot change Nadia's action.
11. **No self-authorized writes:** model proposal and world effects remain nonbinding. The gate must admit exact atoms before a downstream user surface sees them; no owner-specific durable mutation follows merely from current response.
12. **No automatic repair arc:** over-agreeableness, unnatural articulation, concise confession, fully neat emotional resolution and obligatory plot movement are forbidden unless supported.

## Compiling the prompt

Use a deterministic allowlist. `exact_user_event.value.exact_speech` is admitted evidence for the actor; included verbatim. All private memory / causal facts are filtered by actor access and case-specific instructions; never serialize full `NADIA_LAB_CANON_R1.json` or full RF JSON into a renderer prompt. Show Nadia's limited competences, competing obligations and relation history only when actor-accessible and relevant. The model is a realization proposer, not an authority router, causal-owner updater, biography generator or materialization court.

Every emitted outward atom has a stable ID, type, actor, elapsed milliseconds and grounded referents. `realization_prose` is an equivalent presentation of those exact observable atoms, not an additional source of facts. Zero-length atoms are permissible only for legitimate silence/nonresponse; no nonexistent conversation added. World-effect proposals must name documented object IDs and an explicit before/after state. `materialization_requests` may only request further permission and **cannot** be turned into outward facts within this turn.

## Post-call deterministic admission

Reject or HOLD if: reference ID missing; time ordering impossible; action requires undocumented objects; dialogue differs from atom; user-private or actor-inaccessible fact leaked; fact contradicts immutable history/world; admission status asserted by model; or model expands world authority. Preserve deliberate false speech as exact speech if Nadia knows it false—do not reject solely because the utterance is false. When the event is trivial, owner-routed durable effects can be `VALID_EMPTY` (RF006). Missing permission is **not** valid empty; it is `UNAUTHORIZED`/`DEFERRED` and must fail closed.

Store model candidate, raw text, validation findings, any admitted occurrence and timing/cost separately. Do not score Claude here; **no Anthropic API call has been executed**. Distributional Nadia continuity requires multiple independent samples and relation/context tests later.

## Non-goals and unresolved architecture

This does not supersede current narrow wording-only V2. Rich action/gesture proposal, materialization admission, world writes, actor-safe full-person projection packing, and user-specific relation formation remain future-owner gaps. The test establishes whether a renderer can honor constraints **assuming** the manually emulated causal state were lawfully generated; it cannot establish that such a runtime exists.
