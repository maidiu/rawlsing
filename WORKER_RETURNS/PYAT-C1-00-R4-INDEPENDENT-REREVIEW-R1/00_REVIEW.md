# PYAT C1-00 — R4 independent contract / oracle rereview — R1

Disposition: `APPROVE_AT_DECLARED_GRAIN`

Terminal: `C1_00_R4_INDEPENDENT_REREVIEW_COMPLETE__HQ_ADJUDICATION_REQUIRED`

Reviewed head:
`233a91d7cb7789a8e338405abdfef15a5a8ee764`

Reviewer commission:
`bcaa43885dafaa9391a4466620eb41a0e570eebb`

Implementation baseline / owner reference:
`b3b2fa13049513078c301a1f6574b661fcf390c5`

This is **C1-00 documentary contract/oracle approval only**. It does not implement, execute, or authorize C1-01. HQ must separately freeze the exact accepted contract/oracle/write allowlist before issuing C1-01.

No raw survey source was accessed. No production code or production tests were edited. No semantic, comparability, pooling, model, or survey authority was created.

## 1. Scope and diff

The exact R4 compare

`4482f28e436a6ef48e66f9aefda40d354c3866f5`
→
`233a91d7cb7789a8e338405abdfef15a5a8ee764`

is seven commits ahead and zero behind.

Exactly seven files changed:

- four files under `WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R4/**`;
- `analytical_contract.md`;
- `fixture_oracle_manifest.json`;
- `worker_return.json`;

with the latter three under the allowed current C1 packet directory.

No production path, test-owner path, historical R2/R3 correction directory, or prior reviewer directory changed.

The current worker `changed_blobs` list accurately names the three current-C1 packet files changed by R4. The R4 blob manifest separately records the R4 return artifacts.

## 2. A — exact value-bearing condition relation: PASS

I independently recomputed the canonical SHA-256 identities for all frozen subject-condition preimages, producer predicate-leaf preimages, pairing-ground-truth objects, and the witness schema.

All reproduce exactly.

Decision-critical hostile:

- subject: `POSITION_P1`;
- producer leaf: `POSITION_EQ_P2`;
- same empirical semantic ref: **yes**;
- same exact value: **no**;
- frozen pairing relation for that cross-pair: **none**.

The frozen witness law therefore rejects the pair before slice construction.

P1 and P2 subject preimages also hash differently despite sharing the same semantic question ref, so same conditioner/semantic id does not collapse exact value identity.

Pairing/witness substitution is likewise fail-closed: the witness requires the exact pairing-ground-truth ref to name the exact subject-preimage + producer-leaf pair, and requires exact subject/leaf value equality.

No contract step relies on label equality in place of canonical preimage identity. SHA-256 collision resistance remains the same identity-system assumption used throughout PRE553; C1 introduces no weaker shortcut.

**Disposition A: PASS.**

## 3. B — complete synthetic authority freeze / owner-native scope: PASS

Independent recomputation:

- AT07 `EmpiricalUniverse@1.0.0` hash:
  `ca5ee1320b1c0e0685eccb6585b35c1e74094516802545bde42fa11191ea43c2`
- corrected `C1-AT07-QUERY` AuthorityRef content hash:
  `b59ef578314515268fa7b280a8480b4c95c80c9cfd831c39c2bfc4214b6fd767`
- corrected query `AuthoritySnapshot@1.0.0` outer object hash:
  `ddce68bad384945dbec3da9413f915cc968147fb06ba9562aaa4a63ffdbb5724`

All reproduce.

Current I03 owner law independently confirms why the R3 repair is necessary and sufficient at the frozen narrow path:

- `_require_exact_i03_authority_fitness` requires `PREDICATE_GRAMMAR`;
- it requires the exact query operation;
- it requires all three families `EmpiricalPredicate`, `EmpiricalQuerySpec`, and `EmpiricalFact`;
- it passes the exact source-universe ref to `require_positive_authority`;
- `require_positive_authority` checks `scope_envelope["source_universe_refs"]` by exact canonical containment.

The corrected authority contains exactly the frozen AT07 universe in `source_universe_refs`.

Removing the source scope, or replacing it with a different universe ref, fails closed. The repair does not invent a target-use or predicate/risk owner grant for this narrow query path.

A downstream identity check also survives: substituting the old R2 query AuthorityRef into the forward evidence authority closure changes the evidence hash from

`fe5cd778...546f5`

to independently recomputed

`72ea7a3240e2360917aa5617941b93ea08c604f62110298838d2b94c8b94c847`.

One owner-law nuance is explicit: the C1 query AuthorityRef content hash is a frozen **synthetic fixture preimage identity**. Current `AuthoritySnapshot` validation accepts the exact supplied AuthorityRef and validates kind/state/scope; it does not itself derive this C1 fixture hash from the snapshot fields. That is not a defect at the declared source-free oracle grain because the full canonical fixture preimage and expected hash are frozen separately and the owner-use fitness is independently checked.

**Disposition B: PASS.**

## 4. C — owner-native UNKNOWN_CURRENTNESS fixture: PASS

I did not trust either historical candidate hash.

Using the exact frozen R3 fixture refs and the actual B5 owner law:

`SelectionKey.semantic_projection()`
→ `semantic_hash`
→ `_record_ref("SELECTION_KEY", ...)`

with `consumer_context_partition_ref=None`, the canonical projection is 728 UTF-8 bytes and hashes to:

`53683ac6353055af69af9f2d5cb93d889ccc5338b6aa915990c6a541ad942cb6`.

Therefore that is the exact owner-native key.

The competing hash

`a0c54c568eee1351a67ecfee43c297e82aba509daf4bce6932b5ae7331ca03cd`

does not match the exact frozen semantic projection and is stale/wrong for this fixture.

The current packet uses `53683ac...` as the active AT14 `selection_key_ref`.

Every current-packet occurrence of `a0c54c...` is explicitly non-authoritative:

- stale/wrong explanatory prose in `analytical_contract.md`;
- `stale_wrong_ref` in `fixture_oracle_manifest.json`;
- `stale_wrong_selection_key_ref` in `worker_return.json`.

The reachable owner-native UNKNOWN witness is also correct:

1. `LearnedProductLifecycleExecutor.selection_key(...)` registers the exact key;
2. no current-selection or no-current receipt is established;
3. `current_selection_receipt_ref(selection_key.ref)` finds no selection-index ref;
4. it raises exact `LearnedProductLifecycleError("UNKNOWN_CURRENTNESS")`.

This remains distinct from:

- `NO_CURRENT`;
- `CONFLICTING_CURRENT_SELECTION`;
- `EXPLICIT_UNKNOWN_UNVISITED`;
- `UNRESOLVED`;
- `UNAVAILABLE`.

**Disposition C: PASS.**

## 5. D — exact PossibilitySliceEvidence projection / noncircular identity: PASS

Independent recomputation reproduces the projection-schema hash:

`c00e038dd2c1177bfc7842f12febef7b3e30b92bc421df244e2a8e3c4a20b17a`.

The R3 evidence identity law is noncircular:

`C1_POSITIONED_SUBJECT_SLICE_EVIDENCE_PREIMAGE@1`

contains every identity-bearing field of the current `PossibilitySliceEvidence` payload except `evidence_ref` itself, plus the contract/schema discriminator.

Independent evidence hashes reproduce exactly:

- forward `POSITION=P1`:
  `fe5cd7783ac84f0298fb7f56a621d7b0e494bd9348d080dc68ceee09abb546f5`
- reverse `ANSWER=yes`:
  `b54201c8ba8743922e51627e621cc4f3d1c563a43b70167a0720fbb0028ccf72`

`raw_support` is exactly the conditioned raw denominator in both frozen AT07 directions:

- forward: `60`;
- reverse: `62`.

Independent hostile mutations all reidentify the forward evidence:

- denominator-member substitution while preserving visible 54/60 arithmetic;
- cell-geometry mutation from 6/60 to 5/60;
- fixture pairing/comparability AuthorityRef substitution.

The independent hostile hashes need not equal the worker's mutation receipts; the point of the rereview was to test identity sensitivity without trusting the worker mutation recipe. All three produce distinct evidence identities.

**Disposition D: PASS.**

## 6. E — determinant / replay / invalidation closure: PASS

The current direct determinant closure explicitly contains:

- condition-value witness ref/hash;
- subject-condition preimage refs;
- producer predicate leaf refs/projections;
- pairing-ground-truth refs;
- risk-set member refs;
- denominator-member refs;
- constructed `PossibilitySliceEvidence.evidence_ref`;
- the slice projection-schema hash;
- the non-self-referential evidence preimage identity material;
- the owner-native source-scoped query AuthorityRef.

The full fresh-process replay contract explicitly requires:

- witness material/ref;
- subject-condition preimage material/ref;
- producer leaf projection/ref;
- pairing-ground-truth material/ref;
- synthetic authority preimages/refs;
- slice projection-schema hash.

It explicitly states that omission of relation inputs cannot earn
`FULL_COMPOSITION_FRESH_PROCESS_RECOMPUTE`.

The relation-only mutation oracle remains correct: changing the relation/witness determinant while producer counts and unrelated determinants remain fixed must reidentify the direct composed result. Existing B5 selective invalidation applies only if that composed family is already lifecycle-governed; C1 does not impose B5 on a competent direct empirical route merely to satisfy the fixture.

**Disposition E: PASS.**

## 7. Packet-wide self-consistency

The complete current packet now has one active exact UNKNOWN_CURRENTNESS SelectionKey identity.

Historical R2/R3 evidence remains immutable rather than silently rewritten.

The current packet does not claim C1-01 execution. It records no runtime execution and no candidate product output.

Real-source subject↔survey comparability remains external/typed blocked; none of the synthetic fixture objects are promoted into real-source semantic authority.

Previously accepted holdings remain intact:

- exact source/release identity;
- target topology/domain/component identity;
- exact risk/eligibility/denominator/member custody;
- RAW vs governed-weighted separation;
- recursive immediate-parent and full-coverage distinction;
- replay-grade separation;
- direct vs learned/adjudicated anti-bypass law;
- AT07 54/60 forward and 54/62 reverse;
- narrow future C1-01 write terrain.

## 8. Final disposition

All five mandatory classes A–E pass at the declared documentary C1-00 grain.

No typed residual or escalation is warranted by this packet.

`APPROVE_AT_DECLARED_GRAIN`

This approval means only that the **C1-00 contract/oracle packet is exact enough for HQ adjudication of a future C1-01 freeze**.

C1-01 remains:

- unimplemented;
- unexecuted;
- unauthorized by this reviewer.

HQ must separately freeze the exact accepted contract/oracle/write allowlist before issuing C1-01.

`C1_00_R4_INDEPENDENT_REREVIEW_COMPLETE__HQ_ADJUDICATION_REQUIRED`
