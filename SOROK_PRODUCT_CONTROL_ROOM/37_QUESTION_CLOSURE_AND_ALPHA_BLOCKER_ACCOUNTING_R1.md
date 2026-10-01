# Sorok — Question Closure and Alpha-Blocker Accounting R1

Status: `ACTIVE_PROGRESS_ACCOUNTING__CURRENT_THROUGH_Q_ACCESS_001_CLOSURE`

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

Total surfaced questions: **115**.

By closure state:
- `CLOSED_FOR_ALPHA`: **8**
- `PROVISIONALLY_ANSWERED`: **24**
- `NEEDS_PROTOTYPE`: **24**
- `NEEDS_ARCHITECTURE_ADJUDICATION`: **46**
- `OPEN_DISCOVERY`: **7**
- `DEFERRED_POST_ALPHA`: **6**

By blocking stage:
- `ALPHA_SPEC`: **3**
- `ALPHA_IMPLEMENTATION`: **41**
- `ALPHA_VALIDATION`: **25**
- `POST_ALPHA`: **18**
- `NONE`: **28**

Broad alpha blockers are now **44**, split into:
- **3 product/spec blockers**;
- **41 implementation/architecture blockers**.

The conversational critical path is the three product/spec blockers, not the raw frontier count.

## 4. Current three ALPHA_SPEC blockers

### Q-INVITEGRAPH-001
What exact residual invite-economy rules remain after the one-for-one warrant-coupled law: invite consumption on send/accept, decline/expiry/failure restoration, inviter visibility, abuse controls, seed-cohort/public-demand transition?

### Q-PRIV-001
What user data is required for longitudinal relational modeling, what should never be collected, and what deletion/export boundaries are required?

### Q-ALPHA-001
What evidence would falsify or support the proximal alpha theorem that a persistent, independently living generated person can become intrinsically worth knowing through accumulated relation rather than scores, scripted drama or novelty?

## 5. Recently closed product blockers

### Q-WORLD-001
`PROVISIONALLY_ANSWERED / NONE`.

Controlling artifact:
- `51_Q_WORLD_001_PRESENT_WORLD_INGRESS_CONSTITUTION_R1.md`.

Implementation successor:
- `Q-CURRENTINGRESS-001`.

### Q-ACCESS-001
`PROVISIONALLY_ANSWERED / NONE`.

Controlling artifact:
- `52_Q_ACCESS_001_RELATIONAL_REACHABILITY_TOPOLOGY_R1.md`.

Core holding:
- sparse typed access/reachability topology, not scalar relationship level;
- route-specific target/mode/basis/controller/scope/conditions/time/revocability/dependencies/provenance;
- route existence, permission, opportunity and realization remain distinct;
- access, disclosure and knowledge remain distinct;
- domain-specific, asymmetric and nonmonotonic;
- third-party/institutional controller firewall;
- historically formed / causally established access rather than morally earned access;
- no access meter or domain-unlock UX.

Implementation successor:
- `Q-ACCESSIMPL-001`.

These successors are `ALPHA_IMPLEMENTATION`, not reopened product blockers.

### Q-RELSIGN-001
New implementation frontier created by the access-semantic refinement.

It asks how counterpart-specific relational meaning packets are generated from developmental relational grammar, role/relation-class priors, models of particular others, dyadic history/conventions, network context and concrete surface acts, while preserving competing interpretations and governed durable promotion.

Controlling artifact:
- `53_DIFFERENTIAL_RELATIONAL_MEANING_GENERATION_R1.md`.

This is `ALPHA_IMPLEMENTATION`, not a reopened ALPHA_SPEC blocker.

## 6. Other moved-out product blockers

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
- whether invitation events feel caused rather than rewarded;
- whether narrator salience is usable;
- whether control returns at the right grain;
- whether dual portal/message surfaces improve relational persistence.

## 8. Current critical path

1. `Q-INVITEGRAPH-001` — residual one-for-one invitation constitution;
2. `Q-PRIV-001` — minimum data/deletion/export constitution;
3. `Q-ALPHA-001` — final proximal alpha falsification/evidence constitution.

Alpha evidence remains last because it should test the product actually specified, not an earlier abstraction.

## 9. Current interpretation

> **115 frontiers have been surfaced and preserved. Three still require product-level adjudication before the current alpha can be fully specified. Forty-one require architecture work before governed implementation. Twenty-five should be learned through prototype evidence rather than armchair design.**

That is the current progress signal.
