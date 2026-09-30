# Sorok — Question Closure and Alpha-Blocker Accounting R1

Status: `ACTIVE_PROGRESS_ACCOUNTING__REPLACES_RAW_QUESTION_COUNT_AS_PROGRESS_SIGNAL`

Date: 2026-09-30

## 0. Why this exists

The raw count of entries in `QUESTIONS.jsonl` is a **frontier census**, not a remaining-work counter.

A question may remain historically present even after strong provisional decisions constrain it, because later prototype or architecture work may still reopen or sharpen it.

Likewise, one decision may constrain several questions and one question may require several decisions.

Therefore:

`QUESTION_COUNT - DECISION_COUNT`

has no valid progress meaning.

---

## 1. New closure states

Every question now carries `closure_state`:

- `CLOSED_FOR_ALPHA` — sufficiently settled that it does not require further product adjudication for the alpha;
- `PROVISIONALLY_ANSWERED` — strong current answer exists; reopen only on contradictory prototype/research/architecture evidence;
- `NEEDS_PROTOTYPE` — conceptual direction exists but must be tested through concrete interaction/UI behavior;
- `NEEDS_ARCHITECTURE_ADJUDICATION` — product direction exists or is bounded enough, but exact owner/schema/runtime placement remains unresolved;
- `OPEN_DISCOVERY` — genuinely unresolved product/design question;
- `DEFERRED_POST_ALPHA` — intentionally postponed beyond the core alpha.

Legacy `status=OPEN/DEFERRED` remains for historical compatibility but MUST NOT be used as the progress measure.

---

## 2. New blocking stages

Every question now also carries `blocking_stage`:

- `ALPHA_SPEC` — user/product-design adjudication still needed before the alpha can be specified cleanly;
- `ALPHA_IMPLEMENTATION` — exact architecture/owner/runtime work needed before governed implementation;
- `ALPHA_VALIDATION` — does not block building; must be tested to know whether alpha thesis works;
- `POST_ALPHA` — explicitly not needed to establish the first alpha;
- `NONE` — sufficiently answered for current alpha purposes.

`alpha_blocker=true` only for `ALPHA_SPEC` and `ALPHA_IMPLEMENTATION`.

---

## 3. Exact current counts

Total surfaced questions: **109**.

By closure state:
- `CLOSED_FOR_ALPHA`: **8**
- `PROVISIONALLY_ANSWERED`: **20**
- `NEEDS_PROTOTYPE`: **22**
- `NEEDS_ARCHITECTURE_ADJUDICATION`: **42**
- `OPEN_DISCOVERY`: **11**
- `DEFERRED_POST_ALPHA`: **6**

By blocking stage:
- `ALPHA_SPEC`: **7**
- `ALPHA_IMPLEMENTATION`: **35**
- `ALPHA_VALIDATION`: **23**
- `POST_ALPHA`: **18**
- `NONE`: **26**

Current total alpha blockers in the broad sense: **42**.

But this splits critically into:

> **7 product/spec questions that Vozhd + user still need to adjudicate**

and

> **35 implementation/architecture questions that should largely be handled after product semantics are sufficiently fixed.**

Thus the meaningful current conversational progress number is **8**, not 103, 94 or 9.

---

## 4. Current seven ALPHA_SPEC blockers

### Q-WORLD-001
What present-world/current-event ingestion and admission law keeps persona life coupled to the historical present without equating external occurrence with actor exposure, knowledge or effect?

### Q-MSGTIME-001
What asynchronous time law governs message delivery, reply timing and life advancement outside portal scenes without requiring continuous wall-clock coupling or making the persona feel always available?

### Q-ACCESS-001
What exact relational-access topology governs how the user becomes able to enter previously unavailable parts of the persona's life without scalar unlocks or guaranteed disclosure?

### Q-INVITEGRAPH-001
What exact invite economy—seed cohort, invite scarcity, inviter disclosure, note semantics and later outbound-invite eligibility—lets Rawlsing grow person-to-person without status capture or referral spam?

### Q-PRIV-001
What user data is required for longitudinal relational modeling, what should never be collected, and what deletion/export boundaries are required?

### Q-ABSENCE-001
What bounded background/autopilot continuity, if any, may represent the portaled user's ordinary existence while the real user is away without fabricating relational agency?

### Q-ALPHA-001
What evidence would falsify or support the core alpha theorem that earned relationship with an unchosen persona is compelling and spiritually productive?

### Newly moved out of ALPHA_SPEC
- `Q-RETRY-001`: CLOSED_FOR_ALPHA — no user save slots/branch reloads; restart loses continuity/people.
- `Q-LIFETOPO-001`: PROVISIONALLY_ANSWERED / ALPHA_IMPLEMENTATION — independent present life generated from V3/world state with computable→flesh→computable feedback.
- `Q-DISCLOSE-001`: PROVISIONALLY_ANSWERED / ALPHA_IMPLEMENTATION — actor-owned event-time disclosure from relational tension/cathexis rather than trust threshold.

## 5. What the 35 implementation blockers mean

These are not thirty-five new conceptual conversations the user must personally answer.

They are mostly exact architecture questions such as:
- V3/CAN-008/PFF/V2 ownership;
- player participant binding;
- memory and promotion;
- perception packets;
- world completion;
- assertion provenance;
- resource envelope;
- relation facts;
- portal binding;
- actor agendas;
- object/action state;
- expression separation.

Many will collapse or become straightforward once the eight product-spec blockers are settled.

Therefore do not treat `29` as a queue to discuss sequentially with the user.

---

## 6. What the 22 validation questions mean

These are things that should be **prototyped rather than debated to death**.

Examples include:
- whether the primer works;
- whether first-contact curiosity emerges;
- whether dual interfaces improve the experience;
- whether narrator salience feels usable;
- whether scene framing gives enough information;
- whether control returns at the right moments;
- whether persona reciprocity feels actor-owned;
- whether early relational rewards are palpable.

These should generate test fixtures and prototypes, not endless pre-implementation ontology.

---

## 7. Progress rule going forward

Whenever a new question is added, it MUST receive:
- `closure_state`;
- `blocking_stage`;
- `alpha_blocker`;
- `resolution_refs` when an existing artifact/decision already constrains it.

Question-count growth by itself must never again be presented as regression or remaining-work growth.

Progress reports should instead say:

> `ALPHA_SPEC blockers: N`
> `ALPHA_IMPLEMENTATION blockers: N`
> `ALPHA_VALIDATION questions: N`
> `POST_ALPHA / NONE: N`

---

## 8. Current critical path

The seven ALPHA_SPEC blockers are not equally urgent.

Current recommended order:

1. `Q-WORLD-001` + `Q-MSGTIME-001` — jointly settle present coupling and outside-portal time;
2. `Q-ACCESS-001` — changing relational reach without unlock metaphysics;
3. `Q-INVITEGRAPH-001` — initial person-to-person distribution;
4. `Q-PRIV-001` — minimum data/deletion/export constitution;
5. `Q-ALPHA-001` — final falsification/evidence constitution once the product shell is concrete enough to test.

Why put alpha evidence last among the six?

Because the falsification criteria should test the product we actually define, not an earlier abstraction of it.

---

## 9. Interpretation

The system is no longer:

> 103 questions remain.

It is:

> **109 frontiers have been surfaced and preserved. Seven still require product-level adjudication before the current alpha can be fully specified. Thirty-five more require architecture work before governed implementation. Twenty-three should be learned by prototyping, not armchair design.**

This is the current canonical progress interpretation.