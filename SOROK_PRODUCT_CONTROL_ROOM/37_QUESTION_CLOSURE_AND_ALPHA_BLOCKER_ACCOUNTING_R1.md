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

Total surfaced questions: **103**.

By closure state:
- `CLOSED_FOR_ALPHA`: **8**
- `PROVISIONALLY_ANSWERED`: **18**
- `NEEDS_PROTOTYPE`: **21**
- `NEEDS_ARCHITECTURE_ADJUDICATION`: **38**
- `OPEN_DISCOVERY`: **12**
- `DEFERRED_POST_ALPHA`: **6**

By blocking stage:
- `ALPHA_SPEC`: **8**
- `ALPHA_IMPLEMENTATION`: **29**
- `ALPHA_VALIDATION`: **22**
- `POST_ALPHA`: **18**
- `NONE`: **26**

Current total alpha blockers in the broad sense: **37**.

But this splits critically into:

> **8 product/spec questions that Vozhd + user still need to adjudicate**

and

> **29 implementation/architecture questions that should largely be handled after product semantics are sufficiently fixed.**

Thus the meaningful current conversational progress number is **8**, not 103, 94 or 9.

---

## 4. Current eight ALPHA_SPEC blockers

### Q-ALPHA-001
What evidence would falsify or support the core alpha theorem that earned relationship with an unchosen persona is compelling and spiritually productive?

### Q-PRIV-001
What user data is required for longitudinal relational modeling, what should never be collected, and what deletion/export boundaries are required?

### Q-RETRY-001
What undo/retry/save semantics, if any, preserve contingency and consequence without making experimentation punitive or allowing cost-free optimization across every relational branch?

### Q-LIFETOPO-001
What minimum independent life-domain model—work, family, religion/community, interests, projects, other relationships—supports a person whose life remains causally active whether or not the user is present?

### Q-ACCESS-001
What exact relational-access topology governs how the user becomes able to enter previously unavailable parts of the persona's life without scalar unlocks or guaranteed disclosure?

### Q-DISCLOSE-001
What governs persona disclosure, withholding, refusal, evasion and later reinterpretation so conversation remains actor-owned rather than exposition delivery?

### Q-INVITEGRAPH-001
What exact invite economy—seed cohort, invite scarcity, inviter disclosure, note semantics and later outbound-invite eligibility—lets Rawlsing grow person-to-person without status capture or referral spam?

### Q-MSGTIME-001
What asynchronous time law governs message delivery, reply timing and life advancement outside portal scenes without requiring continuous wall-clock coupling or making the persona feel always available?

---

## 5. What the 29 implementation blockers mean

These are not twenty-nine new conceptual conversations the user must personally answer.

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

The eight ALPHA_SPEC blockers are not equally urgent.

Current recommended order:

1. `Q-MSGTIME-001` — outside-portal time/message law;
2. `Q-LIFETOPO-001` — minimum independent life that exists between encounters;
3. `Q-DISCLOSE-001` — actor-owned conversation/disclosure mechanics;
4. `Q-ACCESS-001` — how relational reach changes without lore unlocking;
5. `Q-RETRY-001` — continuity / reset / branching semantics;
6. `Q-INVITEGRAPH-001` — initial person-to-person distribution rules;
7. `Q-PRIV-001` — minimum data / deletion / inspection boundaries;
8. `Q-ALPHA-001` — final falsification/evidence constitution after the product shell is concrete enough to test.

Why put alpha evidence last among the eight?

Because the falsification criteria should test the product we actually define, not an earlier abstraction of it.

---

## 9. Interpretation

The system is no longer:

> 103 questions remain.

It is:

> **103 frontiers have been surfaced and preserved. Eight still require product-level adjudication before the current alpha can be fully specified. Twenty-nine more require architecture work before governed implementation. Twenty-two should be learned by prototyping, not armchair design.**

This is the current canonical progress interpretation.