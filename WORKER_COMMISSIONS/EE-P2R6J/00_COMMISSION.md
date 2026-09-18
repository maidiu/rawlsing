# EE-P2R6J — R6B→R6A ACTIVE BINDING CONTRACT ALIGNMENT + CORRECTED CANDIDATE ISSUANCE

Repository: `maidiu/rawlsing`

## Execution surface

**BROWSER**

## Library access

**NO**

Do not access Library files, LiTS/WVS carriers, source bytes, empirical outcomes, or performance measurements.

Exact branch:

`agent/rabochii-prev3-ee-p2r6j-r6b-r6a-binding-contract-alignment-r1`

Exact base:

`3f382e6abd6c4f6f2271440041be27ceaf4900ee`

This exact base is the adopted EE-P2R6A production runtime implementation. Do not replace or weaken it.

Before doing anything else, resolve live canonical HQ through:

`HQ_HANDOFF/LATEST.json`

and verify its immutable checkpoint packet.

At commission time the sealed checkpoint is:

`20260918T1820-0400`

with immutable handoff:

`da2bdbfbd4746ab1bb81b0790ec48270fdf78885`

Controlling decision:

`HQD-2026-09-18-058`

Read:

`HQ_HANDOFF/EE_P2R6I_RUNTIME_COMPATIBILITY_CORRECTION_20260918.md`

prospectively from the immutable handoff above.

## Trigger

EE-P2R6I produced an internally verified R6B binding candidate:

`fd4177eaddff07dc1e51a6f900c07f163965f996742b301932bbeb79a8690bb0`

at return head:

`f1941fc7e9291a17860475dc14edc9ef1bc32eff`

The R6I candidate passed the refreshed R6B issuer/verifier chain.

However HQ independently proved after return that it is **not directly consumable by the adopted R6A production runtime**.

Exact R6A production runtime authority module:

`rawlsing_next/pre553_runtime_authority.py`

Git blob:

`2ddc591f2572983d18f8f3e8f81a33b80b3bca7b`

Exact R5A concrete binding schema authority:

`WORKER_RETURNS/EE-P2R5A/03_CONCRETE_REALIZATION_BINDING_SCHEMA.json`

schema ref/content hash:

`a1da1ea78dce423ea3520726d0477b058057482d67964056743e08389d9045a0`

R6A accepts concrete active bindings only when:

- `schema == RELEASE_REALIZATION_BINDING@1.0.0`
- `typed_state == ACTIVE_POSITIVE`
- `binding_ref.content_hash == semantic_hash(identity_material)`
- `identity_material` satisfies the exact R5A `future_binding_required_fields` contract.

The R5A contract requires 17 exact top-level identity-material fields.

R6I puts only 4 of those 17 under the exact required names inside `identity_material`; the rest are in `proof_closure`, `extension_identity_set`, or alternate-name fields.

Thus the old candidate is quarantined.

It is **not** an active binding.

Current active-positive-binding count is again `0`.

## Current exact binding-registry snapshot

Path:

`HQ_HANDOFF/BINDING_REGISTRY_SNAPSHOTS/20260918T1820-0400.json`

Snapshot hash:

`209cca7eb759c8fc2df265a0673d180f699381b164e80b88acfa5199438e2b56`

Exact uniqueness key:

`659a8929df10b31da4c82eaf5a6b8bd74234b6f21430422beff186cab804fc16`

Active positive binding count:

`0`

The quarantined R6I candidate is preserved only as evidence.

## Mission

Repair only the producer/consumer contract seam between the R6B-style candidate and the adopted R5A/R6A concrete runtime-binding contract.

Issue exactly one **new deterministic corrected binding candidate** whose proposed active binding record is directly consumable by the exact adopted R6A production runtime.

Do not alter R6A semantics.

Do not patch Candidate A/B.

Do not wake A/B.

Do not execute BE1 or P2X.

The corrected candidate remains inactive until HQ adopts it.

## Exact required R5A/R6A identity material

The corrected binding `identity_material` must contain the exact R5A `future_binding_required_fields` surface under the exact required names and structures.

Prefer **exactly** these 17 top-level fields, with no alternate-name shadow fields:

1. `relation_authority_ref`
2. `frozen_scope_anchor_ref`
3. `source_artifact_sha256`
4. `accepted_base_i02_release_ref`
5. `accepted_base_replay_manifest_hash`
6. `runtime_i02_release_ref`
7. `runtime_candidate_projection_hash`
8. `runtime_replay_manifest_ref`
9. `runtime_m01_m18_coverage`
10. `c11_repository_exact_resolution_receipt`
11. `f02_extension_refs`
12. `f02_authority_refs`
13. `adopted_r4a_authority_refs`
14. `selector_refs`
15. `selector_truth_semantics`
16. `respondent_binding_semantics`
17. `f02_member_law`

The resulting binding identity is:

`SHA256_CANONICAL(corrected_identity_material)`

This will produce a new binding hash.

Do **not** reuse `fd4177e...`.

## Exact field sources

Use adopted authority only.

### Relation / scope / source / base

From adopted R5A authority and R6L evidence:

- relation authority hash:
  `9da19997168612891f59012e69674bac59fbee417d9b30b003171f3074168bf5`
- frozen scope:
  `bf305bf3f169d66954be4f39cc602880fddea6083b5bee9c0212938355cd5297`
- source SHA:
  `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`
- accepted base release:
  `e6c954538fa1830820120465a10a6d065b8a18d1e6b7b08d3f863b0917741e26`
- accepted base replay:
  `6bfe9862abd6f373309ff6f8868f8871948bb9ed397906d880cda6776941a1dd`

### Runtime I02 target

Adopted R6L return:

`1e0a22b6e8b4d25e1b40a0b915bb497369d72b6c`

Runtime release:

`LITS1-I02-F02-SUCCESSOR-7cac43e2ca5b31cb-bf305bf3f169d669`

content hash:

`192926fabd9c9c3d40e43b1d7705ca2bcfe7f8d06e286be26d4b886d436df43f`

Runtime candidate projection hash:

`23912633a23318d22bad0da08027867031320331d8d436d944e9c0b21eb086eb`

Runtime replay-manifest ref content hash:

`30c168fbdf8425b23cbf2a2b2d2c9ab56f3438851f52e3562510089f1d381a08`

Use the exact `runtime_m01_m18_coverage` mapping from:

`WORKER_RETURNS/EE-P2R6L/RUN_OUTPUT/successor_release_receipt.json`

Do not replace the coverage map with a closure hash.

For:

`c11_repository_exact_resolution_receipt`

use the exact runtime release ref shape expected by the adopted R6A production validator and its qualification precedent. Do not substitute the larger R6I repository-resolution evidence object if the production validator expects an ExactRef.

### F02 extension refs

Use the exact **R5A binding-schema structure**, not the R6I `extension_identity_set` structure.

R5A expects q310/q311 question/slot/routing/state values in the exact hash-only shape declared by:

`future_binding_required_fields.f02_extension_refs`

Do not put full ExactRef objects where the R5A schema requires hashes.

### F02 authority refs

Use exact adopted mappings from R5A/F02.

### R4A authority refs

Use the exact R5A-required hash map:

- respondent_binding:
  `3ef0317887f6910838636d3816237a81d5a56b38e07595c8cc1f7c5e7f1fae74`
- mixed_grammar:
  `0d7cfaac1d63cd438d29b109b590cb828805bd113fc37759a6f6f4c88d3c8f55`
- derived_predicate:
  `225e4b80390500451834ea784d955465eb9f145a4cd1f798dace51f3a6d3baa4`
- aggregate:
  `b87c387f9d222c83106c8d47d369af44f5c5368b274fd85e7a08b12c20d49cae`

### Six selector refs

Use the exact ordered R5A list:

1. `c9a0c8106d457bba7e3f3f5abb7ee7fb98482bd86af629d860e4a904ad58456a`
2. `78dbd1a899fe43ac2e2ca6985ea0eccb086989fa2c4315fa518524e7ba94a6df`
3. `c4d2dd827326b6ff29f3c02382c36fa33c47c6227bfbf8c8053c11e1089923ca`
4. `69dc59f79014a7c17190ca658e193a004e167c322c7f713f4540882fb980feb8`
5. `f63d6121776500912342ab377178a15fcf6fabf7071864f4f413d95babb43849`
6. `a6494153b4defeb13e1658b73eead7c5df6e25847708c770dad5f42142492c7d`

### Exact semantic strings

Use the exact R5A strings without normalization or paraphrase:

`selector_truth_semantics`:

`survey_response_EQ__TRUE_IFF_SAME_ROW_GOVERNED_EVENT_HAS_EXACT_NATIVE_VALUE__MISSING_FALSE__NO_ORDERING_DISTANCE`

`respondent_binding_semantics`:

`EXACT_SOURCE_ROW_REPLAY_WITHIN_SAME_LITS1_RELEASE__REFINES_EXACT_SAME_RESPONDENT_ONLY_WITHIN_EXACT_BOUND_SCOPE`

`f02_member_law`:

`EXACT_BASE_RELEASE_MEMBERS_UNCHANGED_BY_REFERENCE_UNION_GOVERNED_Q310_Q311_EXTENSION`

## Exact R6A production qualification

This commission is based on the adopted R6A production runtime head.

Do not qualify against a copied alternate implementation if the production module can be imported directly.

The PASS court must directly exercise:

`Pre553RuntimeAuthoritySet`

from the exact production blob:

`2ddc591f2572983d18f8f3e8f81a33b80b3bca7b`

### Proposed active runtime record

Construct a proposed active record from the corrected candidate:

- `schema = RELEASE_REALIZATION_BINDING@1.0.0`
- `typed_state = ACTIVE_POSITIVE`
- `binding_ref.kind = ReleaseRealizationBinding@1.0.0`
- `binding_ref.content_hash = semantic_hash(corrected_identity_material)`
- exact deterministic object_id derived from that hash
- `identity_material = corrected_identity_material`

This active record is a **qualification projection only** until HQ adopts the corrected candidate.

Do not claim it is active authority in the repository.

### Required direct runtime proof

Using the exact adopted R4A/R5A authority files and an exact repository representation of the adopted R6L runtime release, prove:

`Pre553RuntimeAuthoritySet.require_realized_release(frozen_scope, repository=exact_repository, runtime_release_ref=exact_runtime_ref)`

returns exactly the adopted R6L runtime release when the proposed corrected active record is the sole active binding.

The court must also prove:

- zero binding fails closed;
- multiple corrected active bindings fail closed;
- quarantined R6I candidate `fd4177e...` is not accepted as a production active binding;
- changed source SHA fails;
- changed runtime ref fails;
- changed replay ref fails;
- incomplete M01-M18 coverage fails;
- changed selector/F02/R4A required material fails;
- no latest/default/fuzzy/nearest lookup is introduced.

If exact R6L repository reconstruction cannot lawfully be achieved from already-adopted repository artifacts without source/carrier access, STOP with the smallest exact blocker instead of substituting a fake repository.

## R6I relation/proof preservation

The corrected candidate may carry a separate proof envelope outside `identity_material` preserving:

- zero-binding snapshot provenance;
- R6I/R6L replay and ZIP evidence;
- R6B relation semantics;
- R4A/R5A proof closure;
- quarantined predecessor candidate ref.

Those proof fields must not contaminate the exact R5A identity-material contract.

## Exact current uniqueness authority

Use:

`HQ_HANDOFF/BINDING_REGISTRY_SNAPSHOTS/20260918T1820-0400.json`

snapshot hash:

`209cca7eb759c8fc2df265a0673d180f699381b164e80b88acfa5199438e2b56`

active count:

`0`

Confirm live HQ has not adopted a later competing binding before issuance.

## Required outputs

Write only under:

`WORKER_RETURNS/EE-P2R6J/`

At minimum:

1. `00_RETURN.md`
2. `01_STATIC_R6I_R6A_CONTRACT_MISMATCH_PROOF.json`
3. `02_CORRECTED_BINDING_ISSUER.py`
4. `03_CORRECTED_RUNTIME_BINDING_CANDIDATE.json`
5. `04_PROPOSED_ACTIVE_RUNTIME_BINDING_RECORD.json`
6. `05_R6A_PRODUCTION_RUNTIME_VERIFICATION_RECEIPT.json`
7. `06_BROWSER_QUALIFICATION_RECEIPT.json`

Vendor exact immutable support under `SUPPORT/` only as required.

Do not mutate production R6A files.

## PASS terminal

`EE_P2R6J_PASS__R5A_R6A_RUNTIME_COMPATIBLE_CONCRETE_BINDING_CANDIDATE_ISSUED__PRODUCTION_RUNTIME_VERIFIED__INACTIVE_PENDING_HQ_ADOPTION`

PASS wakes HQ adjudication only.

A/B remains dormant until HQ adopts the corrected binding.

## BLOCK terminal

`EE_P2R6J_BLOCK__<EXACT_FIRST_CONTRACT_ALIGNMENT_OR_PRODUCTION_RUNTIME_VERIFICATION_FAILURE>`

## Hard forbidden

- no Library access;
- no LiTS/WVS carrier access;
- no source rerun;
- no empirical outcome/performance access;
- no production R6A weakening;
- no candidate A/B modification or qualification;
- no BE1 or P2X;
- no Candidate-C repair;
- no selector remint;
- no R4A/R5A semantic redesign;
- no D02/F02 workload mutation;
- no Lock1/Lock2 mutation;
- no MAIN or semantic PRE-MAIN mutation;
- no rebase;
- no replacement branch;
- no reuse of quarantined `fd4177e...` as the corrected binding identity.

Run governed Browser qualification.

Commit and push the exact branch.

Return PASS/BLOCK, final tip, corrected candidate hash/ref, proposed active-record hash/ref, exact R6A runtime-verification disposition, qualification run/job/artifact identities, and wake.

Return to HQ.
