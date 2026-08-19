# ActorAccessibleRenderEnvelope Exact Contract — SCRV3 M6 Literalization

**Assignment:** `E02-W03-SCRV3-M6LIT-001`  
**Authority:** `NARROW_SCRV3_OWNED_INTERFACE_COMPLETION_ONLY`  
**Semantic launch base:** `baa257cb901ad8e5dc4d89faf2d81ea6f442ff8d`  
**Mission branch:** `agent/vozhd-trii-dr-r03-seam-v3-m6-handoff-literalization`  
**Contract:** `SCRV3_M6_ACTOR_ACCESSIBLE_RENDER_ENVELOPE_LITERALIZATION@1.0.0`  
**Contract canonical SHA-256:** `b3ec651c22dedcb58f4be8e8a0b4148a4b2df26dbd61fc12bdc352c00cf3aaf3`  
**Result:** `SCRV3_M6_HANDOFF_LITERALIZATION_COMPLETE`

This contract literalizes the already-accepted ADP-017 actor-safe expression boundary. It creates no new belief, memory, knowledge, relationship, disclosure, affect, salience, or phenomenology semantics.

## Exact handoff

Positive V3→V2 handoff: `ActorAccessibleRenderEnvelope@1.0.0`.  
Entry type: `ActorSafeClaimEntry@1.0.0`.

Envelope fields remain exactly the ADP-017 fields: `envelope_id`, `envelope_schema_version`, `actor_id`, `as_of_causal_time`, `source_generated_person_record_hash`, `source_actor_state_hash`, `source_memory_state_hash`, `source_epistemic_state_hash`, `adp017_authority_version`, `adp017_authority_hash`, `allowed_claim_entries`, `explicit_denial_refs`, `opaque_provenance_refs`, `envelope_hash`, `integrity_state`.

ADP-017 binds exactly to version `1.0.0`, blob `git-blob-sha1:eece4f3f2f3f9288ab9bbc645dc81e20a99e1280`, accepted commit `614775fa05c5d904adff4b53f353637b869e6842`.

## Deterministic identity

Canonicalization profile: `SCRV3_M6_CANONICAL_JSON_V1`: UTF-8, Unicode NFC, recursively sorted object keys, no insignificant whitespace, canonical integer form, and deterministic sorting only for arrays explicitly declared set-like. Producer-owned semantic order stays behind exact immutable ref/hash.

Entry domain-separator bytes, UTF-8 hex:

`5241574c53494e470053435256335f4d36004163746f7253616665436c61696d456e74727900312e302e3000`

Envelope domain-separator bytes, UTF-8 hex:

`5241574c53494e470053435256335f4d36004163746f7241636365737369626c6552656e646572456e76656c6f706500312e302e3000`

`entry_hash = SHA256(entry-domain-bytes || UTF8(canonical_json(entry_core)))`.

Envelope identity-bearing fields are all required envelope fields except `envelope_id` and `envelope_hash`.

`envelope_hash = SHA256(envelope-domain-bytes || UTF8(canonical_json(envelope_core)))`.

`envelope_id = "AARE:" + envelope_hash`.

Opaque audit refs are identity-bearing for exact audit/replay identity while remaining behaviorally inert.

## Actor/source snapshot

All actor-bound semantic records bind one exact `actor_id`.

`as_of_causal_time` is the V3 causal time at which the generated-person record, actor state, ADP-016 memory state, and ADP-017 epistemic/accessibility/permission state are co-valid. It is never wall-clock time.

The four source hashes are immutable content hashes for that snapshot. Actor mismatch, authority mismatch, missing/unverifiable source hashes, or a same-time competing hash is `INTEGRITY_FAILURE`.

## Currentness

Predicate: `SCRV3_M6_AARE_CURRENTNESS_V1`.

A verified envelope remains current at a later causal time only while all four bound source hashes and the exact ADP-017 binding still match. Causal time may advance without staling the envelope when no bound semantic source state changes.

At a later causal time, any bound source-hash change yields `STALE_RENDER_ENVELOPE`. Relevant generated-person, actor-state, ADP-016 memory/accessibility, ADP-017 stance/accessibility/permission, or actor-perceived-view changes must alter at least one bound hash; failure to do so is producer integrity failure.

A stale envelope can remain historically replay-valid but has zero current behavioral authority.

## Positive, partial, denied, deferred

`allowed_claim_entries` is a positive semantic allowlist only.

- `CLAIM_ACCESSIBLE` requires one of the four positive `PERMIT_FIRST_PERSON_*` classes and an empty `permitted_component_refs`; empty means the exact whole canonical claim only.
- `CLAIM_PARTIALLY_ACCESSIBLE` requires one of the four positive classes and a nonempty exact `permitted_component_refs`; only those components are positive.

Denied/deferred claims are represented only as `ActorSafeNonrenderableDecisionRef@1.0.0` control refs. They carry exact claim/permission-record identity but no claim payload and are non-dereferenceable by V2's behavioral lane.

`CLAIM_INACCESSIBLE` maps to `DENY_FIRST_PERSON_CLAIM`. `CLAIM_ACCESS_UNKNOWN` maps to `DEFER_MISSING_AUTHORITY`. The ADP-017 `NO_GOVERNED_STANCE → DENY` rule is represented only when the exact permission record proves that basis; its serialized accessibility state remains one of ADP-017's actual four states.

System missing authority never becomes actor nonknowledge or uncertainty.

## First-person permission vocabulary

Exactly:

`PERMIT_FIRST_PERSON_KNOWLEDGE`, `PERMIT_FIRST_PERSON_BELIEF`, `PERMIT_FIRST_PERSON_UNCERTAINTY`, `PERMIT_FIRST_PERSON_NONKNOWLEDGE`, `DENY_FIRST_PERSON_CLAIM`, `DEFER_MISSING_AUTHORITY`.

V2 may omit or narrow scope; it may not substitute permission class, widen scope, join hidden claims, or rehydrate withdrawn access.

## Relationship views and components

`actor_perceived_view_refs` may contain only same-actor actor-perceived relationship views already lawful and accessible under V3. Objective relationship/household/genealogy truth is forbidden as a substitute.

Partial accessibility stays component-scoped to exact `permitted_component_refs`.

## Opaque provenance

`OpaqueAuditRef@1.0.0` contains only `role`, `audit_role`, `opaque_ref_id`, `opaque_ref_hash`. `role` is exactly `AUDIT_ONLY_REF`.

It is never model-visible, behaviorally dereferenceable, parseable, joined, searched, ranked, embedded, feature-extracted, or used for behavioral cache/routing/style decisions.

Raw PSEPF, comparator receipts, source disagreement, `V3EmpiricalPossibilityInput`, `ResolvedStructuralContext`, structural repository/resolver objects, raw V553–V556 objects, `ReplayReceipt`, and other upstream provenance have zero behavioral authority. Upstream material may be reachable only behind an opaque audit ref through an audit-only sink.

## Replay closure

`SCRV3_M6_AARE_REPLAY_CLOSURE@1.0.0` is an external audit-only content-addressed manifest. Replay-closure domain-separator bytes, UTF-8 hex:

`5241574c53494e470053435256335f4d3600414152455f5245504c41595f434c4f5355524500312e302e3000`

The envelope must carry exactly one opaque ref with `audit_role = ENVELOPE_REPLAY_CLOSURE_ROOT`.

The closure binds the accepted ADP-017 replay material: causal/generated-fact state refs, ADP-016 memory objects/transitions, canonical claims, epistemic effects/transitions, permission records, owning rules, actor checkpoints, exact causal-parent sequence, actor-perceived views, source hashes, entry hashes and deny/defer hashes.

Replay must reproduce exact entries, permissions, envelope hash and envelope ID. Missing/mismatched replay material is `INTEGRITY_FAILURE`; heuristic reconstruction is forbidden. `ReplayReceipt`, if reachable behind the closure, remains audit-only.

## Receiver terminal mapping

Integrity failure and stale status dominate claim-level states and have no fallback.

For a current verified envelope, each requested claim maps to full-ready, partial-ready, explicit-deny, defer-missing-authority, or absent-with-no-inference. A current verified envelope with zero positive entries is `VALID_EMPTY_NO_RENDERABLE_ACTOR_CLAIMS`; valid empty does not authorize fabrication.

See `TERMINAL_STATE_MAPPING.csv`.

## Non-jurisdiction

This literalization does not create disclosure willingness, situational salience, conversational inhibition, affective foregrounding, interlocutor-specific openness, V2 phenomenological variability, or new actor-state semantics. It does not reopen SCRV3 empirical causality, PSEPF metabolism, RSC integration, broad topology, or production implementation.
