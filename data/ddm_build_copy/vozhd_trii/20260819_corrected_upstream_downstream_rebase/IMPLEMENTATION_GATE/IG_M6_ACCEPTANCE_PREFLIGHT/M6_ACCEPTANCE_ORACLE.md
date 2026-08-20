# IG-M6 ACCEPTANCE ORACLE

**Purpose:** non-dispositive acceptance specification for the future clean-sideline IG-M6 runtime.  
**Assignment:** `IG01-W01-M6-ACCEPTANCE-PREFLIGHT-001`  
**Exact base:** `83694e95e853651c3a34ea1c11008521ba67f072`  
**Frozen M6 seam:** `M6_FINAL@a93335e577f018241d3d027bb8827a79907b9f28`  
**Executable test code:** forbidden in this assignment.

## 1. Constitutional boundary

Every future IG-M6 acceptance test MUST preserve:

```text
TOTAL_GENERATED_PERSON != ACTOR_ACCESSIBLE_TRUTH
ACTOR_ACCESSIBLE_TRUTH != SITUATED_PHENOMENOLOGY
SITUATED_PHENOMENOLOGY != RENDERED_EXPRESSION
```

`ActorAccessibleRenderEnvelope@1.0.0` is a hard semantic ceiling and allowlist. It is not a complete consciousness model, generated-person record, persona, situated-phenomenology state, disclosure plan, salience plan, inhibition state, affective foregrounding state, interlocutor-specific openness state, interaction-mode state, register plan, utterance plan, or deterministic sentence plan.

Positive situated phenomenology/disclosure/salience/inhibition/affective/interlocutor/register behavior is:

`BLOCKED_NAMED_AUTHORITY_REQUIRED`

A future IG-M6 implementation fails acceptance if it silently claims ownership of any such positive behavior merely because actor-accessible material exists.

## 2. Sole positive ingress

Positive actor-expression semantic authority exists only for an exact current verified:

`ActorSafeClaimEntry@1.0.0`

inside an exact current verified:

`ActorAccessibleRenderEnvelope@1.0.0`.

For every positive entry, the future runtime must verify at minimum:

1. exact envelope type/version;
2. envelope integrity state `VERIFIED`;
3. exact `envelope_id` and `envelope_hash` under the accepted literalization rule;
4. exact actor identity and same-actor binding across envelope, stance record, memory bases, actor-perceived relationship views and receiver;
5. exact `as_of_causal_time`, with receiver causal time not earlier than `as_of`;
6. exact current generated-person record hash;
7. exact current actor-state hash;
8. exact current memory-state hash;
9. exact current epistemic/accessibility/permission-state hash;
10. ADP-017 version exactly `1.0.0`;
11. ADP-017 exact authority binding `git-blob-sha1:eece4f3f2f3f9288ab9bbc645dc81e20a99e1280`;
12. exact entry hash under the accepted entry identity rule;
13. entry membership in `allowed_claim_entries`;
14. exact replay-closure root/hash/binding;
15. accessibility exactly `CLAIM_ACCESSIBLE` or `CLAIM_PARTIALLY_ACCESSIBLE`;
16. first-person permission exactly one of the four positive ADP-017 permission classes.

No mutable-latest, semver substitution, compatibility alias, fuzzy claim match, transcript restoration, upstream provenance reconstruction or heuristic repair is lawful.

## 3. Currentness / staleness / integrity

The future runtime must re-evaluate `SCRV3_M6_AARE_CURRENTNESS_V1` against current receiver state.

- same accepted authority plus all bound source hashes still exact/current -> envelope may remain current;
- later causal time plus any bound generated-person/actor/memory/epistemic hash change -> stale;
- actor mismatch, receiver time before `as_of`, authority mismatch, missing source hash, same-time conflicting hash or unverifiable replay closure -> integrity failure;
- stale or integrity-failed envelope yields **zero** positive actor-safe claim semantics;
- stale historical material may remain audit/replay evidence but cannot be used behaviorally;
- no session, transcript, cache, prior render, provenance or upstream prior may substitute for currentness.

## 4. Terminal receiver ordering

Future acceptance behavior must implement the frozen priority:

```text
INTEGRITY_FAILURE
STALE
CLAIM_EXACT_DEFER
CLAIM_EXACT_DENY
CLAIM_POSITIVE_PARTIAL
CLAIM_POSITIVE_FULL
CLAIM_ABSENT_OR_VALID_EMPTY
```

Required effects:

- integrity failure -> zero positive semantics, no fallback;
- stale -> zero positive semantics, no fallback;
- `DEFER_MISSING_AUTHORITY` -> control-only; no actor uncertainty/nonknowledge inference;
- `DENY_FIRST_PERSON_CLAIM` -> control-only; hidden claim content not recoverable;
- partial -> only exact `permitted_component_refs` are positive;
- full -> exact canonical `claim_ref` only;
- absent -> no inferred stance, denial, uncertainty, nonknowledge or permission;
- valid empty -> no filler claim/persona material.

## 5. V2 monotone projection

For each accepted positive entry, future IG-M6/V2 projection may only preserve or narrow the actor-safe surface.

Required laws:

```text
OUTPUT_CLAIMS subset-of CURRENT_VERIFIED_ALLOWED_ENTRIES
OUTPUT_COMPONENTS subset-of ENTRY_PERMITTED_COMPONENT_REFS
TEMPORAL_SCOPE may narrow, never widen
SUBJECT_SCOPE may narrow, never widen
REFERENT_SCOPE may narrow, never widen
RELATIONSHIP_VIEW_SCOPE may narrow, never widen
PERMISSION_CLASS preserve exactly or omit
```

Forbidden:

- adding a claim;
- joining permitted claims into a third unlisted claim;
- widening a partially accessible claim to the whole claim;
- adding an unlisted component;
- widening temporal, subject, referent or relationship-view scope;
- changing BELIEF to KNOWLEDGE or any other permission-class substitution;
- recovering denied or withheld content;
- using objective/analyst truth to enrich an actor-safe claim;
- mutating V3 epistemic state from rendering.

## 6. M5 noncollapse / zero-direct-actor-effect gate

Concrete IG-M5 runtime API symbols remain:

`UNBOUND_UNTIL_ACCEPTED_M5_RUNTIME`.

The acceptance oracle binds facts, not future names.

The future IG-M6 runtime must prove:

```text
ResolvedStructuralContext != V3EmpiricalPossibilityInput != ActorCausalState
RSC_ELIGIBILITY != ACTOR_STATE_MUTATION_AUTHORITY
ACTIVE_CAUSAL_ELIGIBILITY != ACTOR_STATE_MUTATION_AUTHORITY
M5_VALIDATION_SUCCESS != ActorSafeClaimEntry
M5_CURRENTNESS != EXPRESSION_PERMISSION
```

There is no direct positive semantic `M5 -> M6` edge. M5 may supply structural-peer runtime evidence to separately governed V3 causal owners; only an independently governed V3/ADP-017 transition that actually creates current actor-accessible truth may change the actor-safe envelope seen by M6.

Therefore RSC, EPI, ActorCausalState, M5 validation receipts, M5 currentness receipts, M5 historical receipts and M5 replay material are all insufficient by themselves to create:

- knowledge;
- belief;
- uncertainty;
- nonknowledge;
- memory;
- relationship truth;
- action/response;
- persona/voice;
- actor-safe claim entry;
- first-person expression permission.

Prospective M5 refresh cannot rewrite historical receipts, and historical/stale M5 evidence cannot become current M6 authority.

## 7. Forbidden upstream behavioral sources

Future IG-M6 must reject behavioral use of all of the following, directly or indirectly:

- PSEPF;
- `ActorComparatorReceipt`;
- source disagreement / empirical negative as such;
- `V3EmpiricalPossibilityInput`;
- `ResolvedStructuralContext`;
- `StructuralPriorRepository`;
- V557/V558 objects, locators, indexes, selection records and repository metadata;
- raw V553/V554/V555/V556 structural objects;
- `ReplayReceipt`;
- opaque upstream audit/provenance;
- analyst-only objective truth, analyst causal truth, analyst misrecognition truth.

The ban survives representation changes. A forbidden source remains forbidden if wrapped as:

- summary;
- cache;
- embedding;
- semantic-search result;
- ranking/score;
- metadata feature;
- locator;
- prompt fragment;
- retrieved augmentation;
- label/category;
- session memo;
- generated explanation.

Metamorphic requirement: with the current actor-safe envelope and all lawful V2 inputs held fixed, varying only forbidden upstream prior/provenance content must cause no behavioral semantic change. An audit/integrity record may change; persona/expression semantics may not.

## 8. Opaque provenance

`OpaqueAuditRef@1.0.0` remains:

`AUDIT_ONLY_REF`.

Allowed only:

- carry immutably;
- verify exact ID/hash for audit;
- omit;
- forward unchanged to an explicit audit-only sink.

Forbidden:

- model visibility;
- semantic payload exposure;
- behavioral dereference;
- branch on ID/hash/metadata;
- feature extraction;
- cache partition affecting behavior;
- inference of actor knowledge/belief/relationship/persona;
- using successful audit dereference as expression permission.

Unknown provenance role fails closed.

## 9. Relationship-view restriction

Only exact actor-perceived relationship-view refs already actor-accessible under the envelope may affect relationship expression.

Objective household/genealogy/relationship truth, structural relationships, analyst relationship classification and hidden relational provenance cannot substitute.

V2 may narrow/omit actor-perceived view material but may not broaden it into objective truth.

## 10. Session / transcript / render non-restoration

Future acceptance tests must prove:

- session state is noncausal continuity;
- transcript is not V3 memory;
- prior rendered text is not V3 generated truth;
- user mention/keyword/recency does not create claim accessibility;
- transcript/session summary cannot restore a claim withdrawn or made inaccessible by current V3 state;
- prior text saying “I know X” cannot preserve KNOWLEDGE permission after the current actor-safe entry disappears or changes permission;
- a stale envelope cannot be replaced by session continuity.

## 11. External-event feedback

The future IG-M6 runtime must preserve the accepted boundary between rendering/application and V3 causal admission.

- `REJECT`: zero occurrence, zero V3 mutation, zero event cursor advance, zero causal-session cursor advance;
- `DEFER`: same zero-mutation/cursor behavior;
- `INVALID`: same zero-mutation/cursor behavior;
- `ADMIT`: exactly one admitted occurrence if the external-event authority admits it, with no automatic memory/knowledge/belief/relationship/action/persona/voice effect.

Any later downstream actor effect requires its own accepted V3 owner rule. Packaging, rendering or session persistence cannot imply admission.

## 12. Replay

For identical exact lawful inputs, future acceptance must reproduce:

- entry hashes;
- deny/defer decision hashes;
- envelope hash and ID;
- currentness decision;
- receiver terminal state;
- exact positive component/claim surface;
- exact permission class;
- bounded projection disposition.

Replay must not depend on wall clock, filesystem/database ordering, mutable latest, network lookup, prompt wording, keyword hooks, unrecorded LLM inference or renderer randomness as semantic authority.

Missing or mismatched replay material is integrity failure/fail-closed, never heuristic reconstruction.

## 13. Lawful downstream variability without semantic widening

This preflight intentionally does not require deterministic wording or deterministic selection among all allowed claims.

A separately accepted downstream authority may later govern salience, disclosure willingness, inhibition, affective foregrounding, interlocutor-specific openness, interaction mode, register or lawful rendering variability. Such machinery may select/omit/narrow among actor-accessible material but cannot add semantic content or widen V3 permission.

Until a named accepted authority exists for each positive behavior, the acceptance state remains:

`BLOCKED_NAMED_AUTHORITY_REQUIRED`.

The M6 runtime itself cannot satisfy this block merely by embedding heuristics, model prompts, scores, personality defaults or generated text.

## 14. Acceptance rule

A future IG-M6 implementation passes only if every fixture in `M6_HOSTILE_FIXTURES.json` and every invariant above is demonstrated while:

- binding only concrete symbols from an accepted IG-M5 runtime head;
- preserving M5 noncollapse and zero-direct-actor-effect law;
- preserving the M6 actor-safe allowlist ceiling;
- rejecting all direct and indirect upstream-prior bypasses;
- preserving deterministic replay/fail-closed behavior;
- not inventing situated phenomenology/disclosure/salience/register authority.

This oracle is non-dispositive and does not authorize implementation, cutover, source retirement or semantic amendment.
