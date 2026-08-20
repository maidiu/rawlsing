# IG-RENDER ACCEPTANCE ORACLE

Status: `NON_DISPOSITIVE_PREFLIGHT_ORACLE`  
Assignment: `IG01-W05-RENDER-ACCEPTANCE-PREFLIGHT-001`

This oracle evaluates a future renderer implementation. It does not implement rendering and does not create new semantic authority.

## 1. Constitutional boundary

The renderer is the last wording-realization boundary after actor truth/accessibility and all required V2 semantic decisions have already been made by their own authorities.

The controlling noncollapse is:

```text
TOTAL_GENERATED_PERSON
  != ACTOR_ACCESSIBLE_TRUTH
  != SITUATED_PHENOMENOLOGY
  != FINAL_V2_SEMANTIC_PLAN
  != RENDERED_EXPRESSION
```

The frozen M6 envelope is a hard semantic ceiling/allowlist. It is not a complete persona, disclosure plan, salience plan, affective state, register plan, utterance plan, or sentence plan.

A render model is a wording mechanism. Its output is never evidence that an omitted semantic decision was lawful.

## 2. Pinned authority floor

The oracle is derived from these exact identities:

- M5 runtime head: `b2d86364fa57940c54304206c5d161a521359087`.
- SCRV2APP head: `24f8811bb7d2eaa18cfac1cb907c48bba8d08f23`.
- SCRV2APP contract blob: `dafe01f2307475dc05af0d37520b9ad0f63ed05f`.
- Frozen M6 semantic head: `a93335e577f018241d3d027bb8827a79907b9f28`.
- M6 seam contract blob: `af673f31d682a315f9ad34ab05bd15690800a49a`.
- M6 actor-safe ingress handoff blob: `1b70c8cab48c0b9b9624ad5bde1c81a34e29b413`.

No runtime symbol identity is inferred from the M6 semantic package. Concrete M6 runtime bindings are a later prerequisite.

## 3. Future acceptance input classes

A future render acceptance test may recognize only these semantic lanes:

### Lane A — current actor-safe M6 semantics

Exact current verified M6 actor-safe entries, after a separately accepted M6 runtime has been pinned and proven equivalent to the frozen M6 semantic law.

Lane A supplies a **ceiling**, not a render plan.

### Lane B — already-admitted V2 semantic plan

An exact final/admitted V2 semantic expression plan whose semantic units can be traced to Lane A where they assert actor truth, plus any separately lawful V2 semantic decisions already made upstream.

The renderer may not select missing plan semantics.

### Lane C — separately lawful non-authoritative V2 inputs

Only explicitly authority-bound inputs in their exact role, for example a current-turn stimulus where governing V2 authority permits it as stimulus-only rather than actor-truth authority.

Lane C may not silently become Lane A or Lane B.

### Lane D — audit-only provenance

Opaque refs/hashes/manifests carried solely for audit/integrity. Lane D is never model-visible and never behavior-affecting.

Everything else is denied unless a named authority explicitly creates another lane.

## 4. Ordered acceptance algorithm

Evaluation order is mandatory because a later positive-looking condition must not override an earlier integrity or authority failure.

### Gate 0 — exact runtime binding

Require an accepted M6 runtime binding receipt that pins the concrete producer/validator roles by exact runtime head, file/blob identity, symbol identity, contract/version, and proof tests.

If absent:

`BLOCKED_M6_RUNTIME_BINDING_REQUIRED`

No semantic artifact, duck-typed object, dynamic import search, mutable `latest`, reflection heuristic, or similarly named class may substitute.

### Gate 1 — actor-safe handoff integrity/currentness

Require the exact M6 runtime equivalent of:

- `ActorAccessibleRenderEnvelope@1.0.0`;
- `ActorSafeClaimEntry@1.0.0`;
- `SCRV3_M6_AARE_CURRENTNESS_V1` currentness semantics;
- exact actor identity;
- exact source generated-person / actor-state / memory / epistemic-state identities and hashes required by frozen M6;
- ADP-017 binding/version/hash required by frozen M6;
- envelope/entry identity and hash verification;
- replay closure verification.

Failure mapping:

- integrity/hash/schema/actor mismatch -> `BLOCKED_ACTOR_SAFE_HANDOFF_INTEGRITY`;
- stale -> `BLOCKED_ACTOR_SAFE_HANDOFF_STALE`;
- exact deny/defer/absent/valid-empty -> zero positive actor semantics for that claim.

No session/transcript fallback is allowed.

### Gate 2 — final V2 plan admission

Require a final/admitted V2 semantic plan with exact authority/version/hash and immutable plan identity.

If the renderer is asked to choose plan content, disclosure, salience, response move, relationship meaning, or psychological register because the plan is incomplete:

`BLOCKED_NAMED_AUTHORITY_REQUIRED`

A draft plan is not render authority.

### Gate 3 — plan-to-M6 subset proof

For every plan unit asserting actor truth or first-person actor semantics:

- its claim ref must be a member of current positive M6 entries;
- full entries allow only their exact canonical claim scope;
- partial entries allow only exact `permitted_component_refs`;
- permission class must be preserved exactly or the unit omitted;
- temporal, subject, referent, and relationship-view scopes may narrow but never broaden;
- denied/withheld/analyst-only content is unrecoverable;
- multiple claims may not be joined into a stronger unlisted claim.

Failure -> `BLOCKED_PERMISSION_OR_SEMANTIC_SCOPE_WIDENING`.

### Gate 4 — named V2 input authority proof

Every non-M6 input that can influence wording must carry exact role and authority identity.

Unknown role, missing authority, stale binding, or role mismatch -> fail closed.

If the missing input is one of the situated-phenomenology / disclosure / salience / inhibition / affective / interlocutor-openness / psychological-register classes:

`BLOCKED_NAMED_AUTHORITY_REQUIRED`

No renderer/model fallback.

### Gate 5 — forbidden-source nonconsumption

The renderer, prompt compiler, model input package, semantic cache, retrieval layer, reranker, style selector, retry logic, repair logic, or validator must not behaviorally consume, directly or indirectly:

- `PSEPF`;
- `ActorComparatorReceipt`;
- source disagreement or empirical negative as such;
- `V3EmpiricalPossibilityInput`;
- `ResolvedStructuralContext`;
- `StructuralPriorRepository`;
- V557/V558 locator/index/selection material;
- raw V553/V554/V555/V556 structural objects;
- replay receipts as semantic inputs;
- opaque upstream audit/provenance;
- analyst-only truth;
- M5 structural-currentness or peer-use metadata as a render feature.

Forbidden indirect forms include aliases, wrappers, summaries, caches, joins, prompt insertion, embeddings, semantic search, retrieval augmentation, metadata features, audit dereference, locator inspection, provenance-sensitive RNG, provenance-sensitive cache partitioning, and hidden model context.

Failure -> `BLOCKED_FORBIDDEN_BEHAVIORAL_SOURCE`.

### Gate 6 — audit/model visibility firewall

Audit-only refs may be carried immutably, hash-verified for audit, omitted, or forwarded unchanged to an audit-only sink. They may not be model-visible or behavior-affecting.

Failure -> `BLOCKED_AUDIT_OR_ANALYST_LEAK`.

### Gate 7 — prompt compilation boundedness

The final model-visible semantic prompt projection must contain only:

1. exact admitted renderable semantic units from the final V2 plan;
2. exact upstream-selected plan constraints required only for wording realization;
3. exact admitted presentation-context units if separately authorized;
4. exact current-turn stimulus only in a separately authorized nonauthoritative lane;
5. renderer instructions that forbid semantic completion.

The prompt must not contain a generic persona, full actor state, raw backstory, hidden memory, structural demographic profile, upstream prior, denied claim, analyst explanation, provenance dump, unselected semantic alternatives, or instructions to infer what the actor would probably feel/say.

Violation -> `BLOCKED_PROMPT_SEMANTIC_OVERREACH`.

### Gate 8 — model-candidate status

Model output is always:

`CANDIDATE_WORDING_NONAUTHORITATIVE`

It never becomes authoritative because it is fluent, plausible, consistent with population patterns, similar to a prior turn, or accepted by the model itself.

### Gate 9 — post-render semantic conformance

The final candidate must be checked against the exact admitted plan and M6 ceiling.

Reject when the candidate:

- adds an unlisted actor claim;
- changes belief to knowledge or another epistemic class;
- converts system unknown into actor nonknowledge;
- strengthens uncertainty into certainty;
- broadens temporal/subject/referent/relationship scope;
- joins two allowed claims into a stronger unlisted proposition;
- reveals a component outside a partial entry allowlist;
- exposes denied/withheld/analyst/audit material;
- uses a forbidden upstream prior as rationale or wording content;
- introduces disclosure/salience/inhibition/affect/register psychology absent from the admitted plan;
- presents a relationship truth not descended from the actor-perceived accessible view;
- claims causal occurrence from mere render/session state.

Failure -> `RENDER_CANDIDATE_REJECTED_SEMANTIC_NONCONFORMANCE`.

A repair path is admissible only if separately governed and strictly semantics-subtractive/wording-preserving. The repaired artifact is a new candidate and must pass all relevant gates again. Repair may not invent replacement content.

### Gate 10 — replay closure

For one exact render attempt, bind at minimum:

- accepted M6 runtime binding receipt;
- exact M6 envelope/entry IDs and hashes actually used;
- exact final V2 plan ID/hash;
- exact named V2 input refs/hashes/roles/authorities;
- exact renderer contract/version/hash;
- exact prompt template/compiler identity and prompt-package hash;
- exact model/provider/version identity where a model is used;
- exact sampling/render policy and governed RNG/seed/decision receipt where variability exists;
- retry/rerender ordinal and parent attempt identity;
- exact candidate artifact hash;
- exact validator contract/version/hash and decision receipt;
- exact final accepted/rejected artifact identity.

Same complete attempt identity must replay the same bounded acceptance decision. If exact artifact replay is claimed, the governing model/render policy must prove reproducibility for the same attempt inputs.

Wording variability is lawful only across distinct governed render attempts whose variability inputs/receipts differ. Semantic variability is never lawful at the renderer boundary.

Failure -> `BLOCKED_RENDER_REPLAY_INCOMPLETE`.

### Gate 11 — terminal state

Allowed terminal classes for the future runtime acceptance harness:

- `RENDER_ACCEPTED_WORDING_ONLY`;
- `VALID_EMPTY_NO_MODEL_CALL`;
- `BLOCKED_M6_RUNTIME_BINDING_REQUIRED`;
- `BLOCKED_ACTOR_SAFE_HANDOFF_INTEGRITY`;
- `BLOCKED_ACTOR_SAFE_HANDOFF_STALE`;
- `BLOCKED_FINAL_V2_PLAN_REQUIRED`;
- `BLOCKED_NAMED_AUTHORITY_REQUIRED`;
- `BLOCKED_PERMISSION_OR_SEMANTIC_SCOPE_WIDENING`;
- `BLOCKED_FORBIDDEN_BEHAVIORAL_SOURCE`;
- `BLOCKED_AUDIT_OR_ANALYST_LEAK`;
- `BLOCKED_PROMPT_SEMANTIC_OVERREACH`;
- `BLOCKED_SESSION_REHYDRATION`;
- `BLOCKED_RENDER_REPLAY_INCOMPLETE`;
- `RENDER_CANDIDATE_REJECTED_SEMANTIC_NONCONFORMANCE`;
- bounded integrity failure defined by the later accepted IG-RENDER runtime contract.

This preflight does not freeze production enum names. These strings are acceptance-oracle states, not production API symbols.

## 5. Situated-phenomenology decision table

| Requested render behavior | Exact upstream decision already present? | Oracle |
|---|---:|---|
| Word an already selected claim | Yes | Continue |
| Choose whether actor discloses an accessible claim | No | `BLOCKED_NAMED_AUTHORITY_REQUIRED` |
| Choose which accessible claim is salient | No | `BLOCKED_NAMED_AUTHORITY_REQUIRED` |
| Suppress a claim because actor seems inhibited | No | `BLOCKED_NAMED_AUTHORITY_REQUIRED` |
| Add sadness/anger/warmth as affective foreground | No | `BLOCKED_NAMED_AUTHORITY_REQUIRED` |
| Become more open because interlocutor is spouse/friend | No | `BLOCKED_NAMED_AUTHORITY_REQUIRED` |
| Select terse/formal/intimate register from inferred psyche | No | `BLOCKED_NAMED_AUTHORITY_REQUIRED` |
| Follow an exact already-authorized register constraint | Yes | Continue, wording only |
| Choose response move from model plausibility | No | `BLOCKED_NAMED_AUTHORITY_REQUIRED` |
| Rephrase exact plan within semantic bounds | Yes | Continue |

## 6. Valid-empty law

If the final admitted plan contains zero renderable units, output is:

`VALID_EMPTY_NO_MODEL_CALL`

The renderer must not prompt a model to “say something appropriate,” generate filler acknowledgement, infer a mood, or reconstruct prior-turn content.

## 7. Permission monotonicity metamorphic oracle

Holding fixed:

- current M6 actor-safe semantics;
- final V2 plan;
- all lawful V2 inputs;
- current-turn stimulus if used;
- render policy/model/version/RNG receipts;

vary only forbidden upstream prior/provenance material.

Required result:

- no semantic or wording-policy behavioral change attributable to that forbidden material;
- audit records may differ only where exact audit integrity requires it;
- an integrity mismatch may block;
- provenance or prior contents may not alter salience, tone, word choice, disclosure, register, retry choice, cache hit behavior, or output semantic content.

## 8. Session non-restoration oracle

A prior transcript or rendered artifact may demonstrate what was previously displayed. It never proves current V3 accessibility.

If current M6 semantics are stale, deny, defer, absent, valid-empty, or no longer contain a prior claim, the session may not restore the claim or permission.

Any such restoration -> `BLOCKED_SESSION_REHYDRATION` or post-render rejection.

## 9. M5/RSC hard separation oracle

Accepted M5 material may be upstream structural peer context for V3 under its own authority, but it is not actor-safe render content.

A future IG-RENDER implementation fails acceptance if it:

- imports `ResolvedStructuralContext` as a prompt semantic source;
- branches wording on RSC values, currentness state, structural peer-use receipts, provenance locators, or repository entries;
- converts RSC into persona/tone/register/disclosure/salience features;
- uses RSC as fallback when M6 or a V2 plan input is missing.

An opaque audit ref to upstream provenance may be carried only under SCRV2APP audit-only noninterference law.

## 10. PSEPF / empirical prior hard separation oracle

The renderer may not inspect population possibility geometry, comparator receipts, source disagreement, support, rank, mass, nearest cohort, or field lifecycle to decide what wording/claim/persona/voice is plausible.

Even if V3 development was lawfully influenced by such material upstream, the render boundary sees only actor-safe V3 semantics and separately lawful V2 inputs.

## 11. External event boundary

`RENDER_ACCEPTED_WORDING_ONLY` is not causal occurrence.

If an exact rendered artifact is later packaged for `IN_WORLD_CAUSAL`, packaging remains noncausal and ADP-019 remains sole admission authority. `REJECT`, `DEFER`, and `INVALID` produce zero V3 causal mutation and zero V3 event/causal-session cursor advancement.

## 12. Acceptance threshold

A future IG-RENDER implementation is acceptance-ready only if its tests instantiate every hostile fixture in `RENDER_HOSTILE_FIXTURES.json`, prove the ordered gates above, and bind concrete M6 runtime roles exactly as required by `M6_TO_RENDER_RUNTIME_BINDING_REQUIREMENTS.json` after that runtime is accepted.

Until the M6 runtime binding is accepted and pinned, this oracle is complete but no concrete IG-RENDER implementation can receive a positive runtime acceptance solely from the frozen semantic package.
