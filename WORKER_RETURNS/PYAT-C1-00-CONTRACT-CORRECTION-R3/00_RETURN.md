# PYAT C1-00 — contract / oracle correction — R3 return

Status: `C1_00_R3_CORRECTIONS_READY_FOR_INDEPENDENT_REREVIEW`

Terminal: `C1_00_R3_CORRECTIONS_READY_FOR_INDEPENDENT_REREVIEW`

Assigned branch:
`agent/rabochii-pyat-hq126-c1-00-contract-correction-r3`

Commission tip:
`e50bc716cf0fd017081e351a5803d3da61a00a38`

Exact base / independent R2 rereview head:
`959d5d8cd4e8f96732e6809030c946751ba5da67`

R2 reviewed worker return:
`a94649020346383e9d9cd18cc2b5a448e0a09ad7`

Implementation baseline remains:
`b3b2fa13049513078c301a1f6574b661fcf390c5`

This is a bounded documentary correction only. C1-01 was not implemented or executed. No production code or production test was edited. Raw survey source reads: **0**. No real-source semantic, comparability, model, pooling or survey authority was created.

## 1. Three reviewed residuals corrected

### B — owner-native synthetic authority scope

R3 freezes the exact synthetic AT07 `EmpiricalUniverse@1.0.0` before the source-scoped query authority:

`ca5ee1320b1c0e0685eccb6585b35c1e74094516802545bde42fa11191ea43c2`

The exact source-free C11 release identity is:

`C11LogicalRelease | REL-c1-at07 | 8afa807cc06a3a10e660d13bbd831f4f758ae829e835a454c62831bfd8f4d939`

The R2 `C1-AT07-QUERY` authority is changed only by adding the current-owner-native exact source scope:

`scope_envelope.source_universe_refs = [<exact frozen AT07 universe ref>]`

Corrected AuthorityRef:

`C1-AT07-QUERY | 1.0.0 | b59ef578314515268fa7b280a8480b4c95c80c9cfd831c39c2bfc4214b6fd767`

The frozen owner check is against current I03 blob
`03facecf70890bfd13b80418620d274cbcd69d02`
and authority owner blob
`ca65a7fd4d52f0c44447434559b1d09412e7aa39`.

The exact source-universe containment, state, kind, operation and required object-family checks all evaluate true in the documentary recomputation. No unrelated source/target/predicate scope field was invented.

Frozen material:
`02_OWNER_NATIVE_AUTHORITY_SCOPE_FREEZE.json`.

### C — reachable B5 UNKNOWN_CURRENTNESS fixture

R3 supersedes the unreachable R2 witness path with the actual current owner route.

Owner:
`rawlsing_next.pre553_learned_product_lifecycle.LearnedProductLifecycleExecutor`
blob:
`a11c9eb73abab9be118ef4f0b6e325e676059f27`

Fixture:

1. instantiate a fresh executor;
2. register the exact frozen SelectionKey using `executor.selection_key(...)`;
3. establish neither a current selection nor a no-current receipt;
4. call `executor.current_selection_receipt_ref(selection_key.ref)`;
5. require exact `LearnedProductLifecycleError("UNKNOWN_CURRENTNESS")`.

Frozen SelectionKey hash:

`a0c54c568eee1351a67ecfee43c297e82aba509daf4bce6932b5ae7331ca03cd`

`resolve_selection_exact` with a fabricated receipt is explicitly forbidden as the UNKNOWN witness.

`UNKNOWN_CURRENTNESS` remains distinct from `NO_CURRENT`, `CONFLICTING_CURRENT_SELECTION`, adaptive `EXPLICIT_UNKNOWN_UNVISITED`, `UNRESOLVED`, and `UNAVAILABLE`.

Frozen material:
`03_UNKNOWN_CURRENTNESS_FIXTURE.json`.

### D — noncircular PossibilitySliceEvidence identity

R2's exact `C1_POSSIBILITY_SLICE_GEOMETRY@1` and
`raw_support = EmpiricalFact.raw_denominator_support`
remain unchanged.

R3 freezes the evidence identity preimage as:

`C1_POSITIONED_SUBJECT_SLICE_EVIDENCE_PREIMAGE@1`

containing every identity-bearing evidence field except `evidence_ref` itself:

- schema;
- contract id;
- source universe ref;
- release ref;
- target ref;
- retained conditioner ids;
- evidence state;
- exact geometry;
- raw support;
- uncertainty state;
- canonical provenance refs;
- canonical authority refs.

Identity law:

`digest = sha256(canonical_json(exact_nonselfreferential_preimage))`

Expected source-free AT07 evidence hashes:

- forward POSITION=P1: `fe5cd7783ac84f0298fb7f56a621d7b0e494bd9348d080dc68ceee09abb546f5`;
- reverse ANSWER=yes: `b54201c8ba8743922e51627e621cc4f3d1c563a43b70167a0720fbb0028ccf72`.

Hostile forward mutations independently recompute to distinct identities:

- different exact denominator member with same visible 54/60:
  `f3f33cc8ae6404ea2d463641e42a9a537db577099a1edbee97929f96735ca37f`;
- changed geometry cell:
  `b6ee0bce50141576f9e186fb92cf1f0d038354b4f3e40509df58fb09142c57b0`;
- changed relation/pairing authority propagated through witness/provenance/authority material:
  `08c73ee366f7368408459fc3df3d0e81f589b1da12cf86aa0567d2684507fa72`.

Frozen material:
`04_EVIDENCE_IDENTITY_PREIMAGE.json`.

## 2. Bookkeeping correction

The superseding current C1 worker return now lists only C1 packet files actually modified by R3.

`family_binding_manifest.json` was not modified by R3 and remains at accepted blob:

`cb430c1eb8ccc1f9f94ba0e9e241807c971b228a`

It is therefore no longer falsely listed as a changed blob.

## 3. Accepted corrections and holdings preserved

R3 leaves the independently accepted R2 A correction unchanged:

- exact value-bearing subject-condition preimages;
- exact producer predicate-leaf preimages;
- exact pairing-ground-truth refs;
- P1-subject/P2-producer mismatch rejection before slice construction.

R3 also leaves the independently accepted R2 E correction unchanged:

- relation/witness/preimage/predicate-leaf/pairing refs remain mandatory composition determinants;
- full fresh-process recomputation requires the relation material;
- relation-only mutation reidentifies;
- existing B5 selective invalidation remains conditional on lifecycle-governed families.

Previously accepted holdings remain unweakened:

- exact source universe + release identity;
- target topology/domain/component identity;
- risk/eligibility/denominator/member identity;
- RAW versus governed-weighted measure/design/estimand identity;
- recursive immediate-parent ancestry;
- positive handoff versus full coverage;
- replay-grade separation;
- direct versus learned/adjudicated anti-bypass law;
- AT07 arithmetic;
- narrow future C1-01 write terrain.

## 4. Deterministic recomputation

`05_RECOMPUTATION_RECEIPT.json` records independent documentary hash recomputation using PRE553 canonical JSON rules.

All frozen checks pass:

- SHA-256 implementation self-test;
- exact AT07 universe ref;
- corrected C1-AT07-QUERY AuthorityRef;
- exact AT07 C11 release;
- forward evidence ref;
- reverse evidence ref;
- denominator-member hostile reidentification;
- geometry hostile reidentification;
- relation/pairing-authority hostile reidentification.

AT07 arithmetic remains:

- forward: `54/60 = 9/10`;
- reverse: `54/62 = 27/31`.

No C1 candidate output was used.

## 5. Exact updated current C1 packet blobs

| artifact | R3 blob |
|---|---|
| `WORKER_RETURNS/PYAT-C1-GENERIC-ANALYTICAL-COMPOSITION-R1/analytical_contract.md` | `978658b4d143f16ab113158f91658fb7ea61266f` |
| `WORKER_RETURNS/PYAT-C1-GENERIC-ANALYTICAL-COMPOSITION-R1/fixture_oracle_manifest.json` | `d27e51c8f8fb32c305507669f91fc84030b599da` |
| `WORKER_RETURNS/PYAT-C1-GENERIC-ANALYTICAL-COMPOSITION-R1/analytical_products.json` | `e29e1d5d99fcb14331b45297f32491d91711f0f2` |
| `WORKER_RETURNS/PYAT-C1-GENERIC-ANALYTICAL-COMPOSITION-R1/hostile_case_receipts.json` | `3a393b1e457d9e59f2061ff63df0e0674b2c61d1` |
| `WORKER_RETURNS/PYAT-C1-GENERIC-ANALYTICAL-COMPOSITION-R1/producer_consumer_trace.json` | `c3165b0fc9323999c426f0ec4056c4c7d4b6f1bd` |
| `WORKER_RETURNS/PYAT-C1-GENERIC-ANALYTICAL-COMPOSITION-R1/replay_and_dependency_receipt.json` | `553f6c0dc8de43b60ac0132089c86aff7f339f5f` |
| `WORKER_RETURNS/PYAT-C1-GENERIC-ANALYTICAL-COMPOSITION-R1/worker_return.json` | `963cd4c14a3fe827d3a460bbf5e51d1962ab9eea` |

Unchanged accepted artifact:

| artifact | unchanged blob |
|---|---|
| `WORKER_RETURNS/PYAT-C1-GENERIC-ANALYTICAL-COMPOSITION-R1/family_binding_manifest.json` | `cb430c1eb8ccc1f9f94ba0e9e241807c971b228a` |

## 6. R3 correction artifact blobs before this return file

| artifact | blob |
|---|---|
| `01_CORRECTION_MATRIX.json` | `3ef369801d7114f3892a79afb9dbfe35a80484d5` |
| `02_OWNER_NATIVE_AUTHORITY_SCOPE_FREEZE.json` | `5d1583dc31c837282ea40448285109a31bb1db41` |
| `03_UNKNOWN_CURRENTNESS_FIXTURE.json` | `b7b3bd4ca919432c0d638ed880080ae7c0956d53` |
| `04_EVIDENCE_IDENTITY_PREIMAGE.json` | `1d1e9eddeebf7e1f26189355dc06e71bf70a367f` |
| `05_RECOMPUTATION_RECEIPT.json` | `f30ddb95ba3e4896dad0d378e6a25a6df25240d4` |

## 7. Proof / execution grade

Proof grade:

`STATIC_INSPECTION + DETERMINISTIC DOCUMENTARY HASH/ORACLE FREEZE`

C1-01 execution: **none**.

Production code/test edits: **none**.

Raw survey source access: **0**.

Real-source semantic/comparability/model/pooling/survey authority created: **none**.

Requested next action:

`FRESH_INDEPENDENT_REREVIEW_OF_EXACT_R3_BRANCH_TIP_ONLY`

C1-01 remains blocked until that rereview accepts the exact R3 packet and HQ separately adjudicates/freezes C1-01.

`C1_00_R3_CORRECTIONS_READY_FOR_INDEPENDENT_REREVIEW`
