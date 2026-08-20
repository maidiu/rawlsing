# M6 — Exact V3 → V2 actor-safe expression seam contract

**Contract:** `M6_V3_TO_V2_ACTOR_SAFE_EXPRESSION_SEAM@1.0.0`  
**Authority:** `DISPOSITIVE_M6_V3_TO_V2_EXPRESSION_SEAM_ONLY`  
**Broad topology:** unchanged  
**Production implementation:** not authorized

## 1. Jurisdiction and constitutional noncollapse

M6 binds the accepted V3 actor-accessible truth handoff to the accepted V2/application expression firewall. It owns only the cross-stage admission and non-widening seam.

The hard noncollapse is:

```text
TOTAL_GENERATED_PERSON != ACTOR_ACCESSIBLE_TRUTH
ACTOR_ACCESSIBLE_TRUTH != SITUATED_PHENOMENOLOGY
SITUATED_PHENOMENOLOGY != RENDERED_EXPRESSION
```

`ActorAccessibleRenderEnvelope@1.0.0` is therefore an allowlist/semantic ceiling. It is not a complete generated person, persona, consciousness, situated phenomenology, salience plan, disclosure-willingness plan, inhibition state, affective-foregrounding state, interaction mode, register, or utterance/sentence plan.

Separately governed V2 mechanisms may lawfully decide whether, when, in what order, and in what wording/register to express allowed material. That freedom is downstream selection/narrowing only.

## 2. Sole positive ingress law

A positive V2 actor-expression semantic unit exists iff all of the following verify exactly:

```text
envelope.type == ActorAccessibleRenderEnvelope@1.0.0
envelope.integrity_state == VERIFIED
SCRV3_M6_AARE_CURRENTNESS_V1(envelope, receiver_state) == CURRENT
exact actor binding verifies
exact generated-person/actor/memory/epistemic source hashes verify
receiver causal time is not before envelope.as_of_causal_time
ADP-017 version == 1.0.0
ADP-017 hash == git-blob-sha1:eece4f3f2f3f9288ab9bbc645dc81e20a99e1280
envelope id/hash verifies under the accepted literalization contract
replay-closure root/hash/binding verifies
entry.type == ActorSafeClaimEntry@1.0.0
entry hash verifies and entry is enumerated in envelope.allowed_claim_entries
entry.accessibility_state in {CLAIM_ACCESSIBLE, CLAIM_PARTIALLY_ACCESSIBLE}
entry.first_person_permission in {
  PERMIT_FIRST_PERSON_KNOWLEDGE,
  PERMIT_FIRST_PERSON_BELIEF,
  PERMIT_FIRST_PERSON_UNCERTAINTY,
  PERMIT_FIRST_PERSON_NONKNOWLEDGE
}
```

No other object, payload, wrapper, locator, summary, cache, provenance path, analyst state, session state, or rendered text is positive actor-expression authority.

## 3. Currentness and integrity precede semantics

Receiver evaluation begins with integrity and currentness. A same-time mismatch, actor mismatch, source-hash mismatch, authority mismatch, missing replay closure, unverifiable hash, receiver time before `as_of_causal_time`, or other literalization integrity failure yields:

`BLOCKED_HANDOFF_INTEGRITY_FAILURE`

A historically verified envelope whose relevant bound source hash changed at a later causal time yields:

`BLOCKED_STALE_ACTOR_SAFE_HANDOFF`

Both states expose **zero positive actor-safe claim semantics**. Historical validity may remain audit/replay truth; it is not current behavioral input.

Session/transcript state, previous render output, user mention, keyword hit, latest object, analyst truth, or upstream provenance cannot restore the old permission.

## 4. Terminal receiver order

The exact receiver order is:

```text
INTEGRITY_FAILURE
-> STALE
-> CLAIM_EXACT_DEFER
-> CLAIM_EXACT_DENY
-> CLAIM_POSITIVE_PARTIAL
-> CLAIM_POSITIVE_FULL
-> CLAIM_ABSENT / VALID_EMPTY
```

Effects:

- `DEFER_MISSING_AUTHORITY`: control-only, zero positive claim semantics. System missing authority is not actor uncertainty/nonknowledge.
- `DENY_FIRST_PERSON_CLAIM`: control-only, zero positive claim semantics. Denied/withheld semantic content is not recoverable.
- `CLAIM_PARTIALLY_ACCESSIBLE`: only exact nonempty `permitted_component_refs` are positive.
- `CLAIM_ACCESSIBLE`: the exact canonical `claim_ref` is positive; `permitted_component_refs` is empty by contract.
- no positive entry and no exact deny/defer ref: no inferred knowledge, belief, uncertainty, nonknowledge, denial, or permission.
- valid empty envelope: zero renderable actor claims; no filler.

## 5. V2 monotone projection law

For every accepted positive entry:

```text
V2_claims ⊆ V3_allowed_claim_entries
V2_components ⊆ V3_permitted_components
V2_temporal_scope ⊆ V3_temporal_scope
V2_subject_scope ⊆ V3_subject_scope
V2_referent_scope ⊆ V3_referent_scope
V2_relationship_view_scope ⊆ V3_actor_perceived_view_scope
V2_permission_class == supplied_permission_class
```

V2 may omit a claim or narrow its lawful scope. It may not:

- add an unlisted claim;
- join two or more permitted claims/components into an unlisted semantic claim;
- widen component, temporal, subject, referent, or relationship-view scope;
- upgrade, downgrade, relabel, or otherwise substitute the supplied first-person permission class;
- recover denied/withheld content;
- infer a stance from absence;
- mutate V3 actor state.

Rendering may vary wording only inside the admitted semantic plan established by separately governed V2 rules.

## 6. Relationship truth boundary

`actor_perceived_view_refs` may carry only exact same-actor relationship views already generated and actor-accessible under V3 authority.

Objective household, genealogy, relationship, structural, or analyst truth is not a substitute. If objective truth differs from the actor-perceived view, V2 expresses only the lawful actor-safe view unless a separate V3 transition later changes actor access.

## 7. Opaque provenance firewall

`OpaqueAuditRef@1.0.0` has role `AUDIT_ONLY_REF`.

Allowed operations:

```text
CARRY_IMMUTABLY
VERIFY_EXACT_ID_OR_HASH_FOR_AUDIT
OMIT
FORWARD_UNCHANGED_TO_EXPLICIT_AUDIT_ONLY_SINK
```

Forbidden in the behavioral/model-visible lane:

```text
DEREFERENCE
READ_OR_PARSE_PAYLOAD
SEMANTIC_SEARCH
EMBED
SUMMARIZE
JOIN
RANK_OR_SCORE
FEATURE_EXTRACT
BRANCH_ON_ID_HASH_OR_METADATA
PROMPT_INSERT
SELECT_SALIENCE
SELECT_REGISTER_OR_VOICE
SELECT_RESPONSE_MOVE
INFER_RELATIONSHIP
INFER_EPISTEMIC_STATE
INFER_UNCERTAINTY
BEHAVIOR_AFFECTING_CACHE_OR_PARTITION
```

Exact audit verification never grants expression permission. Holding lawful actor-safe semantics fixed, changing only opaque provenance must produce no behavioral semantic change.

## 8. Upstream-prior exclusion

The following are denied as direct or indirect behavioral authority, including through aliases, wrappers, summaries, caches, locators, embeddings, prompt material, metadata, audit dereference, or joined derivatives:

- PSEPF;
- `ActorComparatorReceipt`;
- source disagreement/empirical negatives as such;
- `V3EmpiricalPossibilityInput`;
- `ResolvedStructuralContext`;
- `StructuralPriorRepository`;
- V557/V558 records, locators, indexes and selection records;
- raw V553/V554/V555/V556 structural objects;
- `ReplayReceipt`;
- opaque upstream audit/provenance;
- analyst-only objective truth, causal explanation or misrecognition relation.

A lawful actor-accessible V3 claim may of course concern empirical/structural subject matter after V3 has independently created the actor stance/accessibility/permission. That does not expose the upstream prior itself.

## 9. Session/application noncausality

Transcript, session summary, cached render plan, previous model output, and application persistence are noncausal continuity surfaces. They cannot:

- create V3 memory or epistemic stance;
- restore a withdrawn/inaccessible/stale claim;
- substitute for a current envelope;
- widen a permission;
- turn prior rendered text into current actor truth.

## 10. External-event feedback

The accepted V2/application event boundary remains:

- `ADMIT`: create exactly one admitted occurrence if ADP-019 admits it. The package/V2 state is not causal authority, and no downstream memory/knowledge/belief/relationship effect is implied.
- `REJECT`: zero occurrence, zero V3 causal mutation, zero V3 event/casual-session cursor advance.
- `DEFER`: same zero-mutation/cursor behavior until its named blocker changes for the same immutable proposal.
- `INVALID`: same zero-mutation/cursor behavior.

Any actor-state consequence after `ADMIT` requires the separate V3 owner/rule that governs that consequence.

## 11. Replay

Exact replay binds the accepted literalization contract, exact ADP-017 authority, actor, causal time, four source-state hashes, claim/stance/accessibility/permission data, actor-perceived views, entry/decision hashes, and replay closure.

Identical lawful inputs reproduce:

- active actor-safe entry/decision identities;
- envelope id/hash;
- currentness/terminal receiver state;
- exact bounded semantic permission surface.

Wall clock, filesystem order, mutable latest, unrecorded lookup, transcript summary, prompt wording, keyword hooks, unrecorded LLM interpretation, or renderer randomness cannot reconstruct missing semantic authority.

## 12. Closure

All commanded M6 proofs pass. No accepted SCRV3 or SCRV2APP contract requires modification, no broad edge changes, and no production code is authorized.

`M6_ACCEPTED__V2_ACTOR_SAFE_EXPRESSION_SEAM_CLOSED`
