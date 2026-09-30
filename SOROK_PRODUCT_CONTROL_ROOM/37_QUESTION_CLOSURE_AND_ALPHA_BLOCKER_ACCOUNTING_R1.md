# Sorok — Question Closure and Alpha-Blocker Accounting R1

Status: `ACTIVE_PROGRESS_ACCOUNTING__CURRENT_THROUGH_Q_WORLD_001_CLOSURE`

Date: 2026-09-30

## 0. Governing accounting law

The raw number of entries in `QUESTIONS.jsonl` is a frontier census, not a remaining-work counter.

Progress is tracked by:
- `closure_state`;
- `blocking_stage`;
- `alpha_blocker`;
- exact resolution references.

One decision may constrain many questions and one question may require many decisions. Do not subtract decision count from question count.

## 1. Closure states

- `CLOSED_FOR_ALPHA`
- `PROVISIONALLY_ANSWERED`
- `NEEDS_PROTOTYPE`
- `NEEDS_ARCHITECTURE_ADJUDICATION`
- `OPEN_DISCOVERY`
- `DEFERRED_POST_ALPHA`

## 2. Blocking stages

- `ALPHA_SPEC` — product/Vozhd adjudication still required before alpha specification is clean.
- `ALPHA_IMPLEMENTATION` — architecture/owner/runtime work required before governed implementation.
- `ALPHA_VALIDATION` — buildable now; prototype evidence is needed.
- `POST_ALPHA` — intentionally later.
- `NONE` — no current alpha blocker.

`alpha_blocker=true` applies to ALPHA_SPEC and ALPHA_IMPLEMENTATION.

## 3. Exact current counts

Total surfaced questions: **113**.

By closure state:
- `CLOSED_FOR_ALPHA`: **8**
- `PROVISIONALLY_ANSWERED`: **23**
- `NEEDS_PROTOTYPE`: **24**
- `NEEDS_ARCHITECTURE_ADJUDICATION`: **44**
- `OPEN_DISCOVERY`: **8**
- `DEFERRED_POST_ALPHA`: **6**

By blocking stage:
- `ALPHA_SPEC`: **4**
- `ALPHA_IMPLEMENTATION`: **39**
- `ALPHA_VALIDATION`: **25**
- `POST_ALPHA`: **18**
- `NONE`: **27**

Broad alpha blockers remain **43**, split into:
- **4 product/spec blockers**;
- **39 implementation/architecture blockers**.

The conversational critical path is the four product/spec blockers, not the raw frontier count.

## 4. Current four ALPHA_SPEC blockers

### Q-ACCESS-001
What exact relational-access topology governs how the user becomes able to enter previously unavailable parts of the persona's life without scalar unlocks or guaranteed disclosure?

### Q-INVITEGRAPH-001
What exact residual invite-economy rules remain after the one-for-one warrant-coupled law: invite consumption on send/accept, decline/expiry/failure restoration, inviter visibility, abuse controls, seed-cohort/public-demand transition?

### Q-PRIV-001
What user data is required for longitudinal relational modeling, what should never be collected, and what deletion/export boundaries are required?

### Q-ALPHA-001
What evidence would falsify or support the proximal alpha theorem that a persistent, independently living generated person can become intrinsically worth knowing through accumulated relation rather than scores, scripted drama or novelty?

## 5. Q-WORLD-001 closure

`Q-WORLD-001` is now:

`PROVISIONALLY_ANSWERED / NONE / alpha_blocker=false`.

Controlling artifact:
- `51_Q_WORLD_001_PRESENT_WORLD_INGRESS_CONSTITUTION_R1.md`.

Core holding:
- bounded historical-present constraint layer, not digital twin;
- `REAL MACRO-HISTORICAL CONSTRAINT + SYNTHETIC MICRO-LIVED WORLD`;
- explicit external-anchor envelope;
- current/named public fact authority separated from learned-world prior;
- `NOT_YET_INGESTED_EXTERNAL_FACT != ABSENT_EXTERNAL_EVENT`;
- external occurrence, world admission, objective effect/exposure, actor access, uptake and durable effect remain noncollapsed;
- external relevance is objective dependency intersection, not user interest/newsworthiness/engagement value;
- curiosity may trigger checking but cannot condition truth;
- no silent retroactive rewrite after a late currentness collision.

Implementation successor:
- `Q-CURRENTINGRESS-001` — exact external-anchor, source/provenance, freshness/cache, dependency-routing, effective-time, causal-closure and late-collision contracts.

This successor is `ALPHA_IMPLEMENTATION`, not a reopened product blocker.

## 6. Other recently moved-out product blockers

- `Q-RETRY-001`: closed for alpha — no save branches; restart abandons continuity.
- `Q-LIFETOPO-001`: product direction answered; implementation remains.
- `Q-DISCLOSE-001`: product direction answered; implementation remains.
- `Q-ABSENCE-001`: no meaningful player autopilot; implementation remains.
- `Q-MSGTIME-001`: elastic-present default and cancellable/reschedulable pending rendezvous; implementation remains.

## 7. Validation interpretation

The 25 ALPHA_VALIDATION questions should generally be prototyped rather than debated into false precision.

Examples include:
- whether the primer works;
- whether first-contact curiosity emerges;
- whether reciprocal inquiry feels actor-owned;
- whether narrator salience is usable;
- whether control returns at the right grain;
- whether dual portal/message surfaces improve relational persistence.

## 8. Current critical path

1. `Q-ACCESS-001` — changing relational reach without unlock mechanics;
2. `Q-INVITEGRAPH-001` — residual one-for-one invitation constitution;
3. `Q-PRIV-001` — minimum data/deletion/export constitution;
4. `Q-ALPHA-001` — final proximal alpha falsification/evidence constitution.

Alpha evidence remains last because it should test the product actually specified, not an earlier abstraction.

## 9. Current interpretation

> **113 frontiers have been surfaced and preserved. Four still require product-level adjudication before the current alpha can be fully specified. Thirty-nine require architecture work before governed implementation. Twenty-five should be learned through prototype evidence rather than armchair design.**

That is the current progress signal.
