# SV3A Exact Input Contract — `V3EmpiricalPossibilityInput`

**Contract:** `SV3A_V3_EMPIRICAL_POSSIBILITY_INPUT_LIFECYCLE@1.0.0`  
**Authority class:** non-dispositive specialist recommendation to SCRV3  
**Broad lane:** `PSEPF -> V3EmpiricalPossibilityInput -> V3`

## 1. Contract purpose

`V3EmpiricalPossibilityInput` is the smallest boundary object that lets V3 consume an exact PSEPF without copying it and without confusing empirical possibility with realized actor state.

Its functions are limited to:

- exact immutable root binding and dereference integrity;
- exact subject/binding consistency;
- V3-side lifecycle/freshness classification under external authority;
- lossless preservation of source-component states;
- replay-verification bookkeeping;
- typed provenance visibility;
- carriage of opaque separately-owned metabolism and refresh/requery authority bindings when available.

It does **not** own PSEPF geometry, empirical source composition, generated-position semantics, causal transition authority, actor state, or refresh scheduling.

## 2. Canonical envelope

The following field groups are required.

### 2.1 Wrapper identity

- `input_schema_id = V3_EMPIRICAL_POSSIBILITY_INPUT`
- `input_schema_version`
- `input_id`
- `input_hash`

`input_id` is a boundary identity, not an empirical or actor-semantic identity. It MUST be a deterministic function of the canonical identity-bearing fields in this contract. Wall clock, process ID, filesystem order, session ID, randomness, mutable latest pointers and storage paths MUST NOT participate.

### 2.2 Exact PSEPF root binding

`psepf_root_ref` MUST contain or exactly dereference:

- `psepf_object_id`;
- `psepf_content_hash`;
- `psepf_schema_id`;
- `psepf_schema_version`;
- exact producer/authority ID, version and hash sufficient to interpret that PSEPF;
- immutable material locator or exact packaged content-addressed resolution contract sufficient to recover the complete PSEPF and its interpretation-critical closure.

A PSEPF ID/hash whose content is unavailable or whose authority/schema binding cannot be verified is not a valid root.

### 2.3 Generation-subject/binding consistency

The wrapper MUST carry the exact subject/binding reference required by the accepted PSEPF/V3 boundary to prove that the PSEPF is being offered to the same generated subject for which it was produced. The minimum form is:

- `generation_subject_ref` or exact accepted equivalent;
- exact content/hash binding when the governing subject/binding contract supplies one.

This field is an **identity-consistency reference only**. It does not create class, sect, party, household, family, institution, occupation, belief, identity or any other generated position.

Subject mismatch is `INVALID_FAIL_CLOSED`; fuzzy or descriptive matching is forbidden.

### 2.4 Effective-time basis

The wrapper MUST carry exact references sufficient to identify the effective-time/lifecycle basis under which the PSEPF was generated and is being presented to V3:

- `effective_time_basis_refs`;
- exact lifecycle authority/ref governing the freshness classification;
- per-component effective-time refs where source components differ and the PSEPF contract makes those differences material.

The wrapper MUST NOT invent an observation interval from a point time, replace producer time with ingest time, or use hidden wall clock as semantic effective time.

### 2.5 Complete source-component manifest

`source_components[]` is required and MUST contain exactly one manifest entry for every PSEPF source component required by the accepted PSEPF contract. Each entry minimally contains:

- `component_id` — exact producer/PSEPF component identity;
- `component_ref` and `component_content_hash`;
- exact `source_universe_ref` and hash or equivalent source-universe identity binding;
- `component_state` from the SV3A boundary state vocabulary;
- `producer_state_subtype` and exact authority/negative/support refs whenever the upstream producer distinguishes a more precise state;
- applicable `comparability_or_negative_refs`;
- applicable `component_effective_time_basis_refs`;
- applicable externally-produced refresh metadata refs.

The component manifest is a **state/address manifest**, not a field payload. It MUST NOT copy cells, masses, modes, marginals or distributions.

### 2.6 Lifecycle dimensions

The wrapper MUST carry these orthogonal dimensions:

- `freshness_state` plus exact `freshness_authority_ref` and `freshness_basis_refs`;
- `refresh_requirement_state` plus exact external `refresh_authority_ref`/basis when bound;
- `replay_verification_state` plus exact replay binding refs;
- `envelope_integrity_state`.

No one dimension substitutes for another. In particular, `FRESH` is not permission and `VALID` is not support.

### 2.7 Provenance

`provenance_refs[]` MAY expose exact typed provenance references required to audit PSEPF production, including ActorComparatorReceipt and ReplayReceipt references.

Boundary rules:

- ActorComparatorReceipt = provenance only;
- ReplayReceipt = replay/audit only;
- DiscoveryResultReceipt = audit/provenance only unless a separate accepted authority gives it another role outside this contract;
- provenance reachability never creates source composition, causal permission or actor facts.

### 2.8 Opaque separate-authority bindings

The wrapper MAY carry exact opaque bindings to separately accepted authorities:

- `metabolism_authority_binding`;
- `refresh_requery_authority_binding`.

Each binding, when present, MUST be exact ID/version/hash. SV3A defines no permission from their presence and no fallback when absent. The unbound state remains explicit.

## 3. Exact dereference closure

A valid wrapper MUST permit deterministic recovery of the complete PSEPF semantics without wrapper copies. At minimum the dereference chain must recover, where present under the accepted PSEPF contract:

- full exact J-way state space;
- every governed cell and exact mass/support representation;
- all minority and multimodal structure without top-k truncation;
- exact source-indexed components;
- source universe identities;
- support, low-support, observed-zero, zero-support/unsupported and valid-empty distinctions as the producer defines them;
- negative, noncomparability, unknown and conflict states;
- comparator/provenance closure needed to verify production without promoting it to actor state;
- exact generation/effective-time/lifecycle bindings;
- exact schema/authority/version/hash closure needed to interpret the field historically.

If any interpretation-critical required object resolves to zero targets, multiple incompatible targets, mismatched hash/version/schema, mutable latest, fuzzy rematch, or unavailable content, the wrapper is `INVALID_FAIL_CLOSED`.

## 4. Source component state vocabulary

SV3A freezes the boundary-level minimum vocabulary:

- `POSITIVE`
- `UNSUPPORTED`
- `VALID_EMPTY`
- `NONCOMPARABLE`
- `UNKNOWN`
- `CONFLICT`
- `INTEGRITY_FAILURE`

This vocabulary is a boundary projection only. Where the producer distinguishes `LOW_SUPPORT`, `OBSERVED_ZERO`, `ZERO_SUPPORT`, a named negative subtype, or another interpretation-critical state, the wrapper MUST retain the exact producer subtype and refs; it may not erase that distinction by mapping everything to the coarser boundary label.

No global wrapper support state may be computed by majority, averaging, maximum mass, winner source, latest source, confidence score, or file order.

## 5. Permission law

`V3EmpiricalPossibilityInput` is an **admissible evidence envelope**, not an authorization to mutate an actor.

Therefore:

- wrapper presence grants zero causal permission;
- `FRESH` grants zero causal permission;
- `POSITIVE` source components grant zero causal permission by themselves;
- replay verification grants zero causal permission;
- comparator provenance grants zero causal permission;
- a metabolism authority binding must be separately accepted and interpreted by SCRV3's final metabolism/read-permission law.

SV3A does not define whether stale fields may be read causally, how masses may condition a transition, how RNG interacts with field geometry, or what developmental state variables exist.

## 6. Forbidden fields and transformations

The wrapper MUST NOT contain or generate:

### Duplicate PSEPF content

- modal/cell arrays;
- field masses or probability vectors;
- top-k modes;
- marginals;
- dominant mode;
- summarized or truncated J-way geometry;
- pooled source distribution;
- copied comparator snapshot payload when an exact ref is sufficient.

### Actor-state promotion

- actor belief or belief probability;
- actor response or response probability;
- actor identity/affiliation;
- actor memory/knowledge;
- actor psyche/personality/trait;
- actor biography/event/history;
- realized generated position;
- direct `actor_state` fields derived from PSEPF;
- a modal cell ID or mass relabelled as any of the above.

### Illicit authority

- wrapper-created `causal_allowed=true`;
- wrapper-created source pooling/equivalence/linkage authority;
- mutable `latest/current/default` semantic pointer;
- fuzzy/nearest/embedding/LLM matching;
- raw-stage/network fallback;
- wrapper-created refresh schedule;
- wrapper-created generated-position inference.

## 7. Canonical hashing

`input_hash` MUST bind canonical representations of:

- wrapper schema ID/version;
- exact PSEPF root tuple and authority binding;
- exact generation-subject/binding ref;
- effective-time basis refs;
- the complete ordered-by-canonical-key source-component manifest, while preserving any producer-declared semantic order inside a component reference;
- freshness/refresh/replay/integrity states and their exact authority/basis refs;
- identity-bearing provenance and opaque authority bindings.

The hash MUST exclude volatile transport metadata, observed wall clock, filesystem enumeration order, cache state, process/thread order and display labels.

Any identity-bearing change yields a new wrapper identity/hash; in-place mutation under the same ID is forbidden.

## 8. SCR5578 seam

This contract is independently frozen and requires no `ResolvedStructuralContext` field to be embedded in the PSEPF wrapper.

SCRV3 later receives from SCR5578/M5 the exact accepted structural peer-prior input signature, including the exact `ResolvedStructuralContext` identity/hash and the immutable V558 repository/query/resolution bindings required to verify it. That peer input remains a separate channel. Combining it with PSEPF inside one convenience payload must not collapse provenance, authority, lifecycle or causal-read jurisdiction.
