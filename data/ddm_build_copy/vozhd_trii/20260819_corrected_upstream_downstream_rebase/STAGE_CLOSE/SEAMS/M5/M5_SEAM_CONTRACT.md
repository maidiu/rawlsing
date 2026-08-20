# M5 SEAM CONTRACT — M4 ResolvedStructuralContext -> V3 Structural Peer Prior

**Contract:** `M5_V3_STRUCTURAL_PEER_PRIOR_SEAM@1.0.0`  
**Authority:** `DISPOSITIVE_M5_STRUCTURAL_PEER_PRIOR_SEAM_ONLY`  
**Canonical contract-core SHA-256:** `54b9d262ec60ff8794f34d9caf68227275d272dc7d6b2254a9c84c996622d9f2`  
**Status:** `CLOSED`

## 1. Jurisdiction

This contract closes only the M5 seam between accepted M4/SCR5578 structural resolution and the accepted SCRV3 causal boundary.

It does not alter:

- V553/V554/V555/V556 producer semantics;
- V557 publication/governance semantics;
- V558 repository/resolver semantics;
- `ResolvedStructuralContext` semantics;
- `V3EmpiricalPossibilityInput` semantics;
- SCRV3 metabolism/read permissions;
- any V3 transition owner's actor-state semantics;
- V2/application semantics.

## 2. Three-type noncollapse

The following are distinct canonical classes:

| Class | Owner | Semantic identity | Authority ceiling |
|---|---|---|---|
| `ResolvedStructuralContext` | SCR5578/V558 | actual runtime `context_id` + `context_content_hash` under `SCR5578_RESOLVED_STRUCTURAL_CONTEXT@1.0.0` | structural context only; item-wise M4/V557/V558 permission |
| `V3EmpiricalPossibilityInput` | SCRV3 intake | `V3EPI:<input_content_hash>` under `V3EmpiricalPossibilityInput@1.1.0` | empirical possibility intake/read only under SCRV3 |
| `ActorCausalState` | named V3 semantic owners | V3-owned generated state/history identity | mutable only by accepted V3 transition authority |

No ID, hash, locator, checksum, scalar, vector or container may collapse these classes.

## 3. Structural peer machine binding

The required runtime structural type is:

`SCR5578_RESOLVED_STRUCTURAL_CONTEXT@1.0.0`.

Every actual consumption must validate an actual runtime instance. Stage-close authority cannot manufacture one.

Required top-level bindings are:

1. repository/query/policy;
2. resolution receipt;
3. resolved entries;
4. preserved negative entries;
5. deferred/unresolved entries;
6. every SelectionRecord ref/hash;
7. fidelity profile;
8. refresh metadata;
9. provenance;
10. exact context ID/hash.

Every resolved entry binds the resolution key, SelectionRecord ref, canonical producer family/object ID/hash, producer locator, resolver allowed uses and decision state.

### 3.1 M4 verification signature

The verifier is exactly:

`M4_TO_M5_RSC_MACHINE_SIGNATURE@1.0.0`.

Its canonical material is, in M4-governed canonical order:

```text
rsc_schema_id_version
rsc_context_id
rsc_context_content_hash
repository_bundle_id
repository_bundle_content_hash
context_query_id
context_query_hash
resolver_policy_id_version_hash
resolution_receipt_id
resolution_receipt_hash
resolved_entry_set_digest
preserved_negative_entry_set_digest
deferred_unresolved_entry_set_digest
selection_record_set_digest
coverage_fidelity_profile_id_hash
refresh_metadata_id_hash
provenance_root_digest
producer_binding_digest
permission_subset_proof_digest
reference_closure_digest
```

The signature is `SHA-256` over canonical JSON under the M4 handoff rules.

It is:

- a transport/verification checksum;
- not RSC semantic identity;
- not producer semantic identity;
- not permission;
- not actor state;
- not a substitute for the actual RSC instance.

V3 recomputes the signature from the actual runtime RSC values and requires exact equality with the transported signature.

## 4. Structural permission ceiling

For each selected root and every interpretation-critical dependency:

```text
resolver_allowed_uses ⊆ V557_allowed_uses ⊆ producer_allowed_uses
```

M5 cannot widen any set.

`ACTIVE_CAUSAL` is eligibility for structural context to be offered to an active-causal V3 use. It does not authorize mutation.

These never grant permission:

- repository presence;
- collection/global readiness;
- index hit;
- locator hit;
- dependency reachability;
- root permission inherited by a dependency;
- successful M4 checksum verification.

Missing/ambiguous permission fails closed.

## 5. Empirical peer independence

The empirical peer is separately typed as `V3EmpiricalPossibilityInput@1.1.0`.

Its current binding is:

- `V3_EMPIRICAL_POSSIBILITY_METABOLISM_AUTHORITY@1.1.0`;
- authority SHA-256 `e0cd3c8a4443c59b7e97cc151a7db9298310f7a7e766b593fb90968546d66939`;
- `SCRV3_READ_PERMISSION_MATRIX@2.0.0`;
- matrix SHA-256 `6a4227bb3df913b8564ba0d994ce5c2be81bf0f6e8d8b5a164ba546db59fa2d1`.

Current positive PSEPF actor-transition rows are **zero**.

The only current positive row is noncausal exact geometry dereference at the intake surface. No structural permission, M4 signature, RSC selection or repository state can substitute for a missing empirical permission.

## 6. Transition owner requirement declaration

Before a named V3 transition consumes either peer, it must bind `V3PeerPriorRequirementDeclaration@1.0.0` with:

```text
declaration_id
declaration_content_hash
transition_owner_authority_id
transition_owner_authority_version
transition_owner_authority_content_hash
transition_class
structural_peer_requirement
empirical_peer_requirement
structural_peer_operation_ref_or_NONE
empirical_read_permission_id_or_NONE
effective_time_rule_ref
causal_parent_rule_ref
```

Each peer requirement is exactly one of:

`REQUIRED | OPTIONAL_BY_EXACT_OWNER_RULE | NOT_USED`.

The two requirements are independent. There is no generic `BOTH_PRIORS_AVAILABLE => USE_BOTH` rule and no fallback from one denied/stale peer to the other.

This declaration validates a seam. It does not amend the transition owner's semantic contract.

## 7. Consumption receipt

Every attempted actual peer consumption emits `V3PeerPriorConsumptionReceipt@1.0.0` binding at least:

```text
receipt_id/hash
actor_id
causal_run_id
transition_id
transition_owner_authority_id/version/hash
transition_class
peer_requirement_declaration_ref/hash
decision_effective_time
rsc_context_id/hash_or_NONE
m4_signature_value_or_NONE
rsc_validation_result
structural_allowed_use_or_NONE
v3_epi_id/hash_or_NONE
empirical_read_receipt_refs/hashes
ordered_already_lawful_causal_parent_refs/hashes
rng_receipt_refs/hashes
pre_actor_state_hash
post_actor_state_hash
causal_effect_committed
integrity_state
```

Peer consultation provenance is separate from occurrence/witness/actor-fact and causal-parent authority.

## 8. RSC runtime validation state machine

Success:

`M5_RSC_VALIDATED_FOR_DECLARED_STRUCTURAL_PEER_USE`.

Fail-closed states include:

- `M5_RSC_RUNTIME_INSTANCE_MISSING`;
- `M5_RSC_SCHEMA_MISMATCH`;
- `M5_RSC_IDENTITY_OR_CONTENT_HASH_MISMATCH`;
- `M5_RSC_SIGNATURE_MISMATCH`;
- `M5_RSC_PRODUCER_BINDING_MISMATCH`;
- `M5_RSC_PERMISSION_PROOF_INVALID`;
- `M5_RSC_REFERENCE_CLOSURE_INVALID`;
- `M5_RSC_FORBIDDEN_REFERENCE_CLASS_PRESENT`;
- `M5_RSC_PROVENANCE_AUTHORITY_VIOLATION`.

Every failure causes `ZERO_STRUCTURAL_PEER_EFFECT` for the attempted consumption. No latest/fuzzy/raw-stage/network/LLM/random/default repair is permitted.

## 9. Reference and provenance firewall

The structural peer must preserve exact M4 producer identities and positive+negative interpretation-critical closure.

The structural repository/context may not semantically contain:

- PSEPF;
- `V3EmpiricalPossibilityInput`;
- `ActorComparatorReceipt`;
- rendered persona/expression.

Provenance demonstrates origin only. It never supplies source composition, sample pooling, respondent linkage, estimand equivalence, actor contradiction or V3 mutation authority.

## 10. Causal nonassignment

Neither peer directly creates:

- generated structural position;
- event/encounter/exposure;
- memory;
- belief;
- knowledge;
- relationship;
- action;
- response;
- persona;
- voice.

Specifically forbidden:

```text
RSC -> PSEPF
PSEPF -> generated structural position
RSC + EPI -> generic prior bag
RSC + EPI -> scalar/persona vector
source disagreement -> actor contradiction
```

Any actor-state effect must be owned by a separately accepted named V3 transition authority with independently lawful causal basis.

## 11. Currentness

Structural currentness and empirical currentness are independent.

A structural refresh/re-resolution does not imply empirical requery/rebind. An empirical requery/rebind does not imply structural refresh.

The same underlying actor fact change may be an independently authorized trigger on both seams, but each seam makes and receipts its own decision.

Committed transition receipts retain historical peer identities. No later refresh rewrites or launders committed history.

## 12. Divergence and replay

The seam must allow:

```text
same RSC + same EPI + same branch-point actor state
+ different lawful post-branch causal history
=> potentially different lawful developed states
```

It must also require:

```text
same exact authority/history/peer receipts/RNG receipts
=> deterministic exact-history replay
```

A deterministic finished-person mapping from priors is forbidden.

## 13. Scope ceiling

This contract creates no production code, runtime occurrence, broad topology change, new source-composition authority, new actor-state semantic, or new positive PSEPF actor-transition permission.

**Token:** `M5_ACCEPTED__V3_STRUCTURAL_PEER_PRIOR_SEAM_CLOSED`
