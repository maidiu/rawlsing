# EE-P2R6I RUNTIME-COMPATIBILITY CORRECTION — 2026-09-18

Status: `R6I_CANDIDATE_VERIFIED_BUT_NOT_R6A_RUNTIME_CONSUMABLE__ACTIVE_ADOPTION_SUPERSEDED__ZERO_ACTIVE_BINDINGS__SUCCESSOR_REPAIR_REQUIRED__P2X_HELD`

Decision:

`HQD-2026-09-18-058`

This decision supersedes the **active-runtime effect** of `HQD-2026-09-18-057` without deleting or rewriting the historical R6I evidence or the historical adoption decision.

## Trigger

After sealing HQD-057, HQ performed the required pre-A/B production-runtime compatibility check against the exact adopted R6A implementation:

`rawlsing_next/pre553_runtime_authority.py`

blob:

`2ddc591f2572983d18f8f3e8f81a33b80b3bca7b`

R6A accepts active concrete bindings only when:

- `schema == RELEASE_REALIZATION_BINDING@1.0.0`
- `typed_state == ACTIVE_POSITIVE`
- `binding_ref.content_hash == semantic_hash(identity_material)`
- `identity_material` satisfies the exact R5A `future_binding_required_fields` contract.

Exact R5A binding-schema authority:

`WORKER_RETURNS/EE-P2R5A/03_CONCRETE_REALIZATION_BINDING_SCHEMA.json`

schema ref hash:

`a1da1ea78dce423ea3520726d0477b058057482d67964056743e08389d9045a0`

## Exact incompatibility

R5A/R6A require 17 top-level `identity_material` fields:

- relation_authority_ref
- frozen_scope_anchor_ref
- source_artifact_sha256
- accepted_base_i02_release_ref
- accepted_base_replay_manifest_hash
- runtime_i02_release_ref
- runtime_candidate_projection_hash
- runtime_replay_manifest_ref
- runtime_m01_m18_coverage
- c11_repository_exact_resolution_receipt
- f02_extension_refs
- f02_authority_refs
- adopted_r4a_authority_refs
- selector_refs
- selector_truth_semantics
- respondent_binding_semantics
- f02_member_law

R6I candidate:

`fd4177eaddff07dc1e51a6f900c07f163965f996742b301932bbeb79a8690bb0`

places only these four required fields in its `identity_material` under the exact R5A/R6A names:

- relation_authority_ref
- frozen_scope_anchor_ref
- accepted_base_i02_release_ref
- runtime_i02_release_ref

It omits the other thirteen required R5A/R6A fields from `identity_material`.

Some omitted facts exist elsewhere in the R6I envelope, but under different names and/or structures:

- `source_sha256` instead of `source_artifact_sha256`
- `candidate_projection_identity` and proof-closure `runtime_candidate_projection_hash`
- `replay_manifest_ref` and proof-closure `runtime_replay_manifest_ref`
- M01-M18 closure hash rather than required complete coverage mapping
- `repository_resolution_evidence` rather than required exact-ref receipt
- F02 extension/authority/selector material in `extension_identity_set`
- R4A closure in proof material.

R6A does not read those alternate envelope locations when validating a concrete active binding.

Therefore the R6I candidate is:

`R6B_INTERNAL_VERIFIER_PASS__BUT_NOT_DIRECTLY_R5A_R6A_RUNTIME_CONSUMABLE`

This is a concrete producer/consumer contract mismatch.

It is not evidence that the relation semantics, R6L runtime release, F02 selector closure, R4A mixed-composition authority, or R6A runtime implementation are wrong.

## Corrective holding

The R6I candidate and its qualification remain preserved as governed evidence.

However, the active-runtime adoption of `fd4177e...` is superseded.

The candidate MUST NOT be supplied to R6A as an active positive binding.

Current active-positive-binding count for uniqueness key:

`659a8929df10b31da4c82eaf5a6b8bd74234b6f21430422beff186cab804fc16`

returns to:

`0`

Current corrective registry snapshot:

`HQ_HANDOFF/BINDING_REGISTRY_SNAPSHOTS/20260918T1820-0400.json`

snapshot hash:

`209cca7eb759c8fc2df265a0673d180f699381b164e80b88acfa5199438e2b56`

The historical zero snapshot and the superseded one-active snapshot remain immutable audit history.

## Required successor repair

The next Browser repair must align the concrete-binding issuer/verifier output with the already-adopted R5A/R6A runtime contract.

It must NOT weaken R6A.

It must NOT patch around the mismatch in A/B owners.

It must NOT remint F02 selectors or change R4A/R5A semantics.

The corrected candidate must have an `identity_material` that directly satisfies exact R5A `future_binding_required_fields`, and its proposed active runtime record must pass the exact R6A `Pre553RuntimeAuthoritySet.require_realized_release` path.

Because the identity material changes, the corrected binding will necessarily have a new deterministic binding hash.

The quarantined `fd4177e...` identity is not reused as the corrected binding.

## Wake graph

A/B owner-seam requalification is returned to dormant.

Backend fan-in remains dormant.

P2X remains held.

Next lawful work:

`R6B_TO_R6A_ACTIVE_BINDING_CONTRACT_ALIGNMENT_AND_REISSUANCE`

Terminal:

`R6I_ACTIVE_ADOPTION_SUPERSEDED__ZERO_ACTIVE_BINDINGS__RUNTIME_CONTRACT_ALIGNMENT_REQUIRED__P2X_HELD`
