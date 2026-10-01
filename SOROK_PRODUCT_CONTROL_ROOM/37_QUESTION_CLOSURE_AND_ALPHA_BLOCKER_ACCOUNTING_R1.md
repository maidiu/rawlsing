# Sorok — Question Closure and Alpha-Blocker Accounting R1

Status: `ACTIVE_PROGRESS_ACCOUNTING__CURRENT_THROUGH_Q_PRIV_001_CLOSURE`

Date: 2026-10-01

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

Total surfaced questions: **117**.

By closure state:
- `CLOSED_FOR_ALPHA`: **8**
- `PROVISIONALLY_ANSWERED`: **26**
- `NEEDS_PROTOTYPE`: **24**
- `NEEDS_ARCHITECTURE_ADJUDICATION`: **48**
- `OPEN_DISCOVERY`: **5**
- `DEFERRED_POST_ALPHA`: **6**

By blocking stage:
- `ALPHA_SPEC`: **1**
- `ALPHA_IMPLEMENTATION`: **43**
- `ALPHA_VALIDATION`: **25**
- `POST_ALPHA`: **18**
- `NONE`: **30**

Broad alpha blockers remain **44**, split into:
- **1 product/spec blocker**;
- **43 implementation/architecture blockers**.

The conversational critical path is now the single remaining product/spec blocker, not the raw frontier count.

## 4. Current ALPHA_SPEC blocker

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

### Q-INVITEGRAPH-001
`PROVISIONALLY_ANSWERED / NONE`.

Controlling artifact:
- `57_Q_INVITEGRAPH_001_ONE_FOR_ONE_HUMAN_INVITATION_CONSTITUTION_R1.md`.

Core holding:
- one invitation is one deliberate human designation, not one successful conversion;
- deliberate credential commitment spends the invitation before recipient acceptance;
- decline, ignoring, abandonment and existing access do not refund;
- system technical failure may repair credentials only inside the same invitation identity;
- revocation does not create a new recipient-cycling entitlement;
- human-carried single-use credential remains the alpha delivery default;
- no built-in personal note is required for alpha;
- inviter receives no invitee conversion/activity surveillance;
- human invite provenance does not connect synthetic worlds;
- seed/public admission routes remain truthful and non-prestigious.

Implementation successor:
- `Q-INVITEIMPL-001`.

Validation remains:
- `Q-INVITEDELIVERY-001`;
- `Q-HUMANINVITE-001`.

This is no longer an `ALPHA_SPEC` blocker.

### Q-PRIV-001
`PROVISIONALLY_ANSWERED / NONE`.

Controlling artifact:
- `58_Q_PRIV_001_USER_DATA_PRAXIS_DELETION_EXPORT_CONSTITUTION_R1.md`.

Core holding:
- preserve relationship history while minimizing the external-human dossier;
- zero-profile default;
- purpose-bound optional user facts;
- external human / participant state / supplied facts / event history / actor-local models / system praxis hypotheses remain distinct;
- sensitive traits are not silently inferred as truth;
- actor-local models remain actor-scoped and do not become global reputation;
- praxis/relationship data does not feed advertising, growth targeting, pricing or public reputation;
- reflection/user-model data can be deleted/disabled separately from causal relationship memory;
- canonical history deletion deletes/resets the continuity rather than silently retconning it;
- inspect/export user-governed facts and system-user-model data while preserving actor-private opacity.

Implementation successor:
- `Q-PRIVIMPL-001`.

This is no longer an `ALPHA_SPEC` blocker.

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

1. `Q-ALPHA-001` — final proximal alpha falsification/evidence constitution.

Alpha evidence remains last because it should test the product actually specified, not an earlier abstraction.

## 9. Current interpretation

> **117 frontiers have been surfaced and preserved. One still requires product-level adjudication before the current alpha can be fully specified. Forty-three require architecture work before governed implementation. Twenty-five should be learned through prototype evidence rather than armchair design.**

That is the current progress signal.
