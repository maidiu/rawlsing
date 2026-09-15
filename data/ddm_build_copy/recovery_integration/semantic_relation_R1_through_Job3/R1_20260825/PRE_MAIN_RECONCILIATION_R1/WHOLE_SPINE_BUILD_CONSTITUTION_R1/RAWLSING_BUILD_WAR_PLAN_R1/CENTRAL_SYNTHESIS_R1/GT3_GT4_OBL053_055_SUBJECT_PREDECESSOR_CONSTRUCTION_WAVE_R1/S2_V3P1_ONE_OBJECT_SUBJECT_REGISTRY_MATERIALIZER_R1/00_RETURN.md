# GT3/GT4 S2 — OBL054 V3-P1 ONE-OBJECT OWNER-PRESERVING SUBJECT REGISTRY MATERIALIZER R1

## Terminal

`PASS__GT34_S2_OBL054_V3P1_ONE_OBJECT_OWNER_PRESERVING_SUBJECT_MATERIALIZER_GREEN__NO_SEMANTIC_AUTHORITY`

## Exact execution boundary

- repository: `maidiu/rawlsing`
- worker branch: `agent/rabochii-gt34-s2-obl054-v3p1-subject-registry-materializer-r1`
- exact working-ancestry start: `50cd903fbd6fdb4ed1dc248ab2ff5db9a2060733`
- immutable instruction ref: `50cd903fbd6fdb4ed1dc248ab2ff5db9a2060733`
- executed only: `WORKER S2 — OBL054 V3-P1 ONE-OBJECT OWNER-PRESERVING SUBJECT REGISTRY MATERIALIZER R1`
- profile: `BOUNDED_IMPLEMENTATION`
- semantic candidate SHA: `38257e57bd5e2d862edfcd1efb610c4d15774b37`
- evidence execution SHA: `e9df80b9b4aca29f7002257d8bf044fa21eef45e`
- draft PR: `#221`
- semantic authority created: NONE
- semantic authority adopted: NONE
- real first-canary subject materialized: NO
- actor identity/history created: NO
- encounter/contact/use/exposure created: NO
- comparator/PSEPF/metabolism/CAN-008/V2: NONE
- positive V3 actor mutation: NONE
- PRE-MAIN movement by this worker: NONE
- `main` movement by this worker: NONE

S2 did not consume S1 or S3 in-flight conclusions.

## Holding

The bounded V3-P1 substrate required by OBL054 is implemented and green at the exact one-object, owner-preserving grain.

It accepts only an already-lawful owner-bound nonactor semantic object. It verifies exact semantic-owner authority identity, exact semantic-object bytes/hash, exact evidence refs, exact provenance refs, and an exact owner-binding content hash before issuing any subject reference.

It emits only:

1. one deterministic content-addressed `subject_ref`; and
2. one deterministic content-addressed materialization receipt.

It does not parse, add, infer, normalize, reinterpret, classify, or transfer ownership of the semantic object.

The implementation is therefore an identity/materialization substrate, not a semantic owner.

## Exact implementation artifacts

Production module:

`rawlsing_next/gt34_s2_v3p1_subject_registry_materializer.py`

semantic-candidate blob:

`0ac1df8ef4c91b9004f3ffb8d00fefcadc2980cf`

Bounded tests:

`rawlsing_next/tests/test_gt34_s2_v3p1_subject_registry_materializer.py`

semantic-candidate blob:

`82be090227df24c4df8ab5d967bfb4ca99ba15a1`

Semantic-candidate tree:

`7075dbbfab83315dbdf90312f99eee988e0f6b49`

Semantic-candidate commit:

`38257e57bd5e2d862edfcd1efb610c4d15774b37`

Court spec:

`.rabochii/court_spec.json`

court-spec blob:

`5f38ac5460607780d676e835b8ac62ddb9a9b08b`

Exact evidence execution commit:

`e9df80b9b4aca29f7002257d8bf044fa21eef45e`

The court spec binds its `semantic_candidate_sha` to `38257e57bd5e2d862edfcd1efb610c4d15774b37`, so the evidence scaffolding commit cannot silently become semantic candidate law.

## Exact materializer identities

Materializer ID:

`GT34_V3P1_ONE_OBJECT_OWNER_PRESERVING_SUBJECT_REGISTRY_MATERIALIZER`

Version:

`1.0.0`

Subject-ref scheme:

`RAWLSING_V3_OWNER_PRESERVING_SUBJECT_REF_V1`

Ingress owner-binding schema:

`V3P1_OWNER_BOUND_SUBJECT_INGRESS_BINDING@1.0.0`

Receipt schema:

`V3P1_ONE_OBJECT_OWNER_PRESERVING_SUBJECT_MATERIALIZATION_RECEIPT@1.0.0`

These are implementation/transport identities only. None is a semantic authority ID.

## Exact input contract

`OwnerBoundSubjectInput` requires:

- `semantic_owner_authority_id`;
- `semantic_owner_authority_version`;
- `semantic_owner_authority_hash`;
- exact `semantic_object_ref`;
- immutable `semantic_object_bytes`;
- exact `evidence_refs`;
- exact `provenance_refs`;
- `owner_binding_content_hash`.

Before materialization, the implementation verifies:

1. every required owner field is exact/nonempty;
2. every hash is lowercase SHA-256;
3. semantic object bytes are nonempty;
4. `SHA256(semantic_object_bytes) == semantic_object_ref.sha256`;
5. evidence refs are exact and nonempty;
6. provenance refs are exact and nonempty;
7. duplicate exact refs fail closed;
8. the presented owner-binding content hash exactly recomputes from owner identity, semantic object ref, evidence refs and provenance refs.

Malformed, unknown/unbound-by-exact-input, or integrity-failing inputs produce `SubjectMaterializationError` and no subject ref.

## Deterministic subject identity law

The implementation uses canonical JSON and an explicit domain separator.

Conceptually:

`subject_ref_hash = SHA256(DOMAIN || canonical_json(owner + exact object ref + owner-binding hash + evidence refs + provenance refs))`

and:

`subject_ref = urn:rawlsing:v3:subject:sha256:<subject_ref_hash>`.

Identity does not consume:

- random UUID;
- wall clock;
- mutable latest;
- filesystem order;
- display label;
- geography;
- demographic inference;
- RNG;
- Q69B wording;
- clinic/hospital strings;
- structural-position inference;
- ADP-010 encounter semantics.

Evidence/provenance exact refs are canonically sorted solely for mechanical content addressing. Input iteration order is not semantic precedence or authority.

Changed semantic object material or changed owner identity changes the exact subject identity. A second distinct object cannot occupy the bounded one-object registry.

## Receipt identity law

The receipt body binds:

- receipt schema;
- exact resulting `subject_ref` and hash;
- materializer ID/version;
- semantic-owner authority ID/version/hash;
- exact semantic object ref/hash;
- exact owner-binding content hash;
- exact evidence refs;
- exact provenance refs;
- replay input hash;
- integrity state;
- `semantic_owner_transfer = false`;
- `semantic_fields_interpreted = false`.

Receipt identity is:

`receipt_hash = SHA256(RECEIPT_DOMAIN || canonical_json(receipt_body))`

and:

`receipt_id = urn:rawlsing:v3:subject-materialization-receipt:sha256:<receipt_hash>`.

Identical exact input is idempotent and returns the identical receipt.

## Semantic-owner preservation proof

The materializer never parses `semantic_object_bytes`.

It therefore cannot inspect or rewrite entity-family, facility-form, function, public/private status, clinic/hospital meaning, or any later classifier predicate.

The receipt carries the semantic owner's exact authority identity and the semantic object's exact ref/hash by reference.

It explicitly emits:

`semantic_owner_transfer = false`

and:

`semantic_fields_interpreted = false`.

No semantic fields from the opaque object are copied into the receipt.

Thus:

`SEMANTIC OWNER -> OBJECT TRUTH`

remains external to and upstream of:

`S2 MATERIALIZER -> CONTENT-ADDRESSED SUBJECT IDENTITY + RECEIPT`.

S2 cannot manufacture project truth by successful materialization.

## One-object ceiling

`OneObjectSubjectRegistry` has exactly one immutable slot.

Behavior:

- first valid owner-bound object -> materialize;
- exact duplicate -> return the identical receipt;
- second distinct object -> `OneObjectRegistryOccupiedError`.

This prevents the bounded implementation candidate from becoming an unrestricted general world-object registry.

Any later widening beyond this exact one-object substrate requires separate project authority/review.

## Synthetic fixture court only

All S2 positive tests use synthetic owner-bound fixtures only.

The primary synthetic object bytes are:

`{"fixture":"SYNTHETIC_NONACTOR_OBJECT_A","opaque_semantics":["alpha","beta"]}`

The fixture contains no Q69B, clinic, or hospital material and is not a generated-world project fact.

Exact synthetic test identity outputs:

- owner-binding content hash:
  `8871ded5a64c928ba1a84a4f5d1664c7a11464a65cb84e1dd26731add8c6b3c2`
- synthetic subject-ref hash:
  `2eebfb3405f9f0d696e35d1c6b23284a48aa1e472c9347aeec0638f289de2479`
- synthetic subject ref:
  `urn:rawlsing:v3:subject:sha256:2eebfb3405f9f0d696e35d1c6b23284a48aa1e472c9347aeec0638f289de2479`
- replay input hash:
  `b2adddc57e598500a7e72e1c2207acfe2ce2e8ca7ada3c07e57fe7df381bb297`
- synthetic receipt hash:
  `a789df704549b69d8372dac25a852c31d1cda2aa963c8b512730ae46527ac87e`
- synthetic receipt ID:
  `urn:rawlsing:v3:subject-materialization-receipt:sha256:a789df704549b69d8372dac25a852c31d1cda2aa963c8b512730ae46527ac87e`

These identities prove deterministic mechanics only.

They are explicitly **not** the real first-canary subject or receipt and must never be promoted as such.

## Tests / hostile boundary court

The S2 test module contains 20 bounded tests covering:

- synthetic-fixture-only boundary;
- deterministic cross-registry replay;
- duplicate idempotence;
- one-object occupancy;
- changed semantic input -> changed identity;
- changed semantic owner -> changed identity;
- ref iteration order non-authority;
- semantic-owner-transfer false;
- semantic-fields-interpreted false;
- absence of display-label/geography/wall-clock/UUID/RNG identity inputs;
- semantic object bytes/hash mismatch fail-closed;
- owner-binding hash mismatch fail-closed;
- malformed/empty owner/evidence/provenance/object inputs fail-closed;
- duplicate exact evidence-ref rejection;
- exact receipt owner/object/evidence/provenance/replay binding;
- implementation identity not labeled as semantic authority.

No test fixture creates actor history, encounter, exposure, comparator, PSEPF, metabolism, CAN-008 effect or V2 authority.

## Governed bounded court

Draft PR:

`#221`

Workflow:

`Rabochii Governed Bounded Court`

Run:

`34016836165`

Job:

`101441974170`

Exact checked-out evidence execution SHA:

`e9df80b9b4aca29f7002257d8bf044fa21eef45e`

Court result:

`PASS`

Job conclusion:

`success`

Protocol self-test:

`20 passed in 0.11s`

Court-spec validation:

`PASS`

S2 bounded test execution:

`20 passed in 0.13s`

Court receipt artifact:

- artifact ID: `9984156110`
- artifact name: `rabochii-court-receipt-34016836165`
- artifact digest: `sha256:f503bdb428dfca9a32b0d8b33fc3bb35f435a09caffa86ed4c19ca3498583c91`

Exact court receipt:

- schema: `RABOCHII_BOUNDED_COURT_RECEIPT@1.0.0`
- result: `PASS`
- exit code: `0`
- semantic candidate SHA: `38257e57bd5e2d862edfcd1efb610c4d15774b37`
- evidence execution SHA: `e9df80b9b4aca29f7002257d8bf044fa21eef45e`
- PR synthetic merge SHA: `1dc9c1207802cb0c9e1656b7bbbe7abf92433e75`
- Python: `3.12.14`
- implementation: `CPython`
- determinism mode: `EXACT`
- court spec SHA-256: `84f5a10c563df4694c5539bf344f19c030d6dc226bb18fa6f8037449f66f6902`

## Historical archive check

The inherited old V3-P1 launch register names:

`Rawlsing_code_bundle_staging.zip`

with governed expected SHA-256:

`953c9149bd03877206e3cb440d1f4db35dea6473af30b97fd23b7e76c6fc0086`.

No matching governed archive bytes are committed in the current repository.

A connected Library object with that filename was materialized and directly hashed before use. It was:

- bytes: `21,967,177`
- entries: `9,808`
- computed SHA-256:
  `3f2c5ed925273153a4f300f75e54524729f0b4fef9974957be1f3cd887c91289`

This is **not** the governed archive and was rejected as historical implementation evidence.

S2 therefore did not preserve/adapt any behavior from those mismatching bytes.

The implementation candidate is grounded instead in accepted/current project law and current repository execution conventions, including:

- post-R OBL052 HQ disposition;
- R2 seam preflight;
- RA-R00 V3-P1/IMP-008 packet law;
- V3-P1 W3 fixture boundary;
- accepted ADP-007 deterministic generated identity/provenance law;
- accepted ADP-015 generated-entity ownership pattern;
- accepted CAN-006 producer-preserving exact-ref/replay pattern;
- current Rabochii governed-court protocol.

No historical archive content is promoted to authority.

## No-semantic-widening court

The candidate proves only:

`ALREADY OWNER-BOUND ONE OBJECT`

->

`DETERMINISTIC SUBJECT REF + MATERIALIZATION RECEIPT`.

It does not prove or own:

- what the object is;
- whether it is a facility;
- whether it is public;
- whether it is a clinic or hospital;
- `SUBJECT_IS_PUBLIC_CLINIC_OR_HOSPITAL`;
- actor contact/use;
- ADP-010 AVAILABLE/OPPORTUNITY/ENCOUNTER/EXPOSURE;
- Q69B response or meaning;
- comparator truth;
- PSEPF;
- metabolism;
- CAN-008;
- actor psychology/state;
- V2 output.

Therefore adoption of this implementation at its exact grain would not itself create a general semantic world-object authority.

## OBL054 disposition

`OBL054 = IMPLEMENTATION_CANDIDATE_GREEN__AWAITING_HQ_REVIEW_ADOPTION`

S2 does not self-adopt and does not close OBL054 project-wide.

The candidate is ready for HQ hostile review/adoption at exactly the one-object owner-preserving materialization grain.

OBL052 remains blocked until the independently owned OBL053 semantic/evidence side exists and the necessary predecessor pieces are adopted/combined under HQ authority.

No real first-canary subject may be materialized from this synthetic court.

## Final

No semantic authority was created.

No semantic owner was transferred.

No real first-canary subject was materialized.

No positive actor/V3 causal event was created.

Terminal:

`PASS__GT34_S2_OBL054_V3P1_ONE_OBJECT_OWNER_PRESERVING_SUBJECT_MATERIALIZER_GREEN__NO_SEMANTIC_AUTHORITY`

The terminal branch tip is the commit containing this return artifact.
