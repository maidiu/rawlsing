# GT3/GT4 T2 — OBL054 S2 V3-P1 OWNER-PRESERVING MATERIALIZER HOSTILE AUDIT R1

## Terminal

`FAIL__GT34_T2_OBL054_S2_OWNER_AUTHENTICATION_FAIL_OPEN_AND_ONE_OBJECT_SCOPE_ESCAPE_PROVED`

## Exact review boundary

- repository: `maidiu/rawlsing`
- worker branch: `agent/rabochii-gt34-t2-obl054-s2-v3p1-materializer-hostile-audit-r1`
- exact working-ancestry start: `d7c5f2270bdc2bdb78c347dd1c9b9c67205dd635`
- immutable instruction ref: `146eb938a568ae8b8c853b502860c29491956372`
- executed only: `WORKER T2 — OBL054 S2 V3-P1 OWNER-PRESERVING MATERIALIZER HOSTILE AUDIT R1`
- target semantic candidate: `38257e57bd5e2d862edfcd1efb610c4d15774b37`
- target evidence execution: `e9df80b9b4aca29f7002257d8bf044fa21eef45e`
- target original court: `34016836165`
- S2 candidate modified: NO
- authority adopted: NO
- real first-canary subject materialized: NO
- PRE-MAIN moved: NO
- `main` moved: NO

T2 did not consume T1 or T3 in-flight conclusions.

## Disposition

S2 is **not lawful for bounded adoption in its current form**.

The hostile audit confirms several important S2 properties are genuinely correct, but proves two exact fail-open defects at the required OBL054 grain:

1. owner authentication is not actually enforced; and
2. the claimed one-object V1 ceiling is bypassable.

Therefore:

`OBL054 S2 CANDIDATE = FAIL_HOSTILE_REVIEW__RETURN_FOR_BOUNDED_REPAIR`.

This is not a rejection of the V3-P1 owner-preserving materialization design. It is a bounded implementation defect requiring repair before adoption.

## 1. Exact semantic-candidate / evidence separation — PASS

Independent comparison proves:

`50cd903fbd6fdb4ed1dc248ab2ff5db9a2060733`

-> semantic candidate

`38257e57bd5e2d862edfcd1efb610c4d15774b37`

adds exactly:

- `rawlsing_next/gt34_s2_v3p1_subject_registry_materializer.py`
- `rawlsing_next/tests/test_gt34_s2_v3p1_subject_registry_materializer.py`

and then:

`38257e57bd5e2d862edfcd1efb610c4d15774b37`

-> evidence execution

`e9df80b9b4aca29f7002257d8bf044fa21eef45e`

adds only:

- `.rabochii/court_spec.json`.

Exact target blobs on the banked review base remain identical to the semantic candidate:

- module blob: `0ac1df8ef4c91b9004f3ffb8d00fefcadc2980cf`
- S2 tests blob: `82be090227df24c4df8ab5d967bfb4ca99ba15a1`.

T2 did not modify either target blob.

## 2. Original S2 governed court — independently verified PASS

Target court:

- run: `34016836165`
- job: `101441974170`
- workflow: `Rabochii Governed Bounded Court`
- exact checkout: `e9df80b9b4aca29f7002257d8bf044fa21eef45e`
- target semantic candidate in court spec: `38257e57bd5e2d862edfcd1efb610c4d15774b37`
- protocol self-test: `20 passed`
- S2 court: `20 passed`
- run conclusion: `success`.

The original court is real and correctly tied to S2's evidence execution SHA.

Its success is insufficient because the hostile defects below were not tested.

## 3. Independent hostile court

T2 added only an independent hostile test/court surface:

`rawlsing_next/tests/test_gt34_t2_s2_materializer_hostile_audit.py`

plus the bounded court spec.

Authoritative corrected hostile execution:

- evidence execution SHA: `a2d60a01f19af7b1d5c01284dd0f21f24173f112`
- draft PR: `#225`
- run: `34018861625`
- job: `101447609008`
- exact checkout: `a2d60a01f19af7b1d5c01284dd0f21f24173f112`
- protocol self-test: `20 passed in 0.09s`
- hostile audit tests: `12 passed in 0.11s`
- court result: `PASS`
- job conclusion: `success`
- court spec semantic candidate: `38257e57bd5e2d862edfcd1efb610c4d15774b37`
- court receipt spec SHA-256: `0465b3846b7bad56c06752ce99cd69fe41138c458f9e89b4325645f8641106ba`
- receipt artifact ID: `9984802086`
- receipt artifact digest: `sha256:c9b7877e6074090e9e25c099d872aad06703e0c3e8c7d119411cd76a4b12453a`.

The court PASS means **the hostile assertions succeeded**. It does not mean the target candidate passed hostile review.

A prior T2 run `34018821436` failed only because the independent recomputation helper attempted to sort Python dict objects directly. That harness error was corrected without modifying S2. It carries no candidate disposition.

## 4. Positive controls — S2 properties that survived attack

The hostile court independently confirms:

- exact canonical content-addressing is deterministic;
- independent recomputation matches S2's owner-binding, subject-ref, replay and receipt identity laws;
- owner authority/hash mutation changes identity when the binding is recomputed;
- semantic-object bytes/ref mismatch fails closed;
- evidence/provenance iteration order is canonicalized mechanically and creates no precedence;
- exact duplicate input is idempotent;
- a **single existing** `OneObjectSubjectRegistry` rejects a second distinct object;
- semantic object bytes are opaque to the materializer;
- clinic/public-like bytes are not copied into the receipt as materializer truth;
- `semantic_owner_transfer = false` is mechanically emitted by code;
- `semantic_fields_interpreted = false` is mechanically emitted by code;
- no UUID, wall clock, display label, filesystem order or environment state participates in the declared input identity;
- no replay nondeterminism was found.

T2 found **no hidden semantic parser or classifier** inside S2.

The failure is narrower.

## 5. DEFECT T2-D01 — owner authentication fails open

S2's input requires:

- semantic-owner authority ID;
- version;
- content hash;
- semantic object ref/hash;
- evidence refs;
- provenance refs;
- owner-binding content hash.

But the implementation does not independently establish that the named semantic owner is accepted, competent, or owns this object.

`validated_owner_binding_hash()` only recomputes:

`SHA256(domain || canonical_json(caller-supplied owner/object/evidence/provenance fields))`.

The public helper:

`compute_owner_binding_content_hash(...)`

allows the same caller to compute exactly the checksum that the materializer later treats as verified ownership integrity.

There is no required:

- accepted authority snapshot;
- authority-registry membership proof;
- adoption receipt;
- competence/object-family scope proof;
- independently owned object-binding receipt;
- fixed accepted-authority root/capability.

### Hostile proof

T2 fabricated:

- owner ID: `HOSTILE_UNREGISTERED_OWNER`
- owner version: `999.999.999`
- owner hash: `919de30f5fa6cb6f5ccce0b6fae1f1d19ec7e8568c778411d4bc4c399f741475`

and arbitrary exact object/evidence/provenance refs.

Using only S2's public helper, T2 computed a self-consistent binding and called:

`materialize_owner_bound_subject(...)`.

S2 emitted a content-addressed subject ref with:

`integrity_state = VERIFIED_OWNER_BOUND_INPUT`.

No accepted semantic owner existed.

For hostile object A, independent recomputation produced:

- owner binding:
  `6a876ed1da686e63dd66f538ba8a5db08abe5f8f8c9bd3f1e947cebfc2026611`
- subject-ref hash:
  `d5726284b313c9ddb7bbf396c00e1b8ae7ec4a3f0d05a7caa63d67a50dc20204`
- replay hash:
  `19333d2631c53d9534014103b202cc4aca0551cf0a74cb04385801cac16ad939`
- receipt hash:
  `aa764f27b2b53fba7f6c49471377dbf5dbfa23fd5abd8aa00507acd05a2ceb29`.

This violates the S2 requirement that unknown/unowned input fail before ref emission.

The owner-binding hash is a useful integrity checksum, but it is **not an ownership authentication proof**.

## 6. DEFECT T2-D02 — one-object scope is bypassable

S2's `OneObjectSubjectRegistry` rejects a second distinct object only inside one already-instantiated Python object.

The claimed one-object V1 ceiling is not enforced at the materializer/adoption scope.

Two independent escapes are green in the hostile court.

### Escape A — exported stateless materializer

The module publicly exports:

`materialize_owner_bound_subject`.

Calling it for hostile object A and then hostile object B emits two distinct subject refs and two distinct receipts.

Object B independently recomputes to:

- owner binding:
  `113951066cae94b1039019d232159a31fb3340d4a017330e75f481c65a4e7e56`
- subject-ref hash:
  `d4256803e4300b62af837c7ec8d01b74c48264a5589274681761472bce57fb89`
- replay hash:
  `0552067d4a0b9971e15341b551351eb027133a08a44453ea0d04c04c6d183eb1`
- receipt hash:
  `0e992191b039464eb4b4aefeb47aabfef81ba8e8de3b4645cad6aac18c944702`.

So the free function itself is an unrestricted multi-object mechanical materializer.

### Escape B — registry re-instantiation

Two new `OneObjectSubjectRegistry()` instances may independently materialize A and B.

The one-object guard is therefore per-instance mutable memory, not a V1 contract invariant.

This violates the hostile-review requirements that:

- a second distinct object be impossible at the V1 grain; and
- the implementation not silently widen beyond the one-object substrate.

## 7. Synthetic-fixture promotion attack

S2 does not parse semantic bytes; that part is correct.

However, D01 + D02 together allow arbitrary/synthetic bytes to be paired with fabricated real-looking owner/ref material and emitted as normal-looking content-addressed subject refs.

That means synthetic-fixture nonpromotion currently depends only on external discipline.

This is **not** a third semantic-parser defect. It is a direct consequence of:

`OWNER AUTHENTICATION FAIL-OPEN + ONE-OBJECT SCOPE ESCAPE`.

## 8. semantic-owner-transfer=false assessment

This field is not merely decorative in the narrow sense that S2 never rewrites owner identity into a materializer-owned semantic authority.

The code preserves the supplied owner ID/version/hash and never emits semantic object fields as its own truth.

So:

`semantic_owner_transfer = false`

is mechanically true **for whatever owner identity the caller supplies**.

The defect is prior:

S2 does not prove that the supplied owner is a lawful owner at all.

Thus:

`NO OWNER TRANSFER`

does not rescue:

`NO OWNER AUTHENTICATION`.

## 9. Smallest exact repair requirement

Do not add semantic ontology or classifier logic.

Repair only the failed materialization grain.

### R2-1 — independently authenticated owner binding

Require one independently verifiable accepted-owner authority snapshot/capability that binds at minimum:

- exact semantic owner authority ID/version/content hash;
- accepted/adopted authority identity;
- governed object family/scope;
- exact semantic object ref/hash or exact bounded owner-object binding;
- exact evidence/provenance lineage required by that owner;
- integrity/currentness state.

The materializer must validate this proof against an accepted authority root/registry/capability that the caller cannot satisfy merely by recomputing S2's own checksum.

`owner_binding_content_hash` may remain as transport integrity.

It may not itself constitute owner authentication.

### R2-2 — make one-object cardinality a scope invariant

Bind V1 materialization to one immutable content-addressed **one-object materialization permit/scope** naming the exact expected owner-bound semantic object ref/hash.

Then:

- exact duplicate under the same permit -> idempotent;
- any distinct object under that permit -> fail closed;
- constructing another Python registry instance -> does not create a new permission;
- direct stateless materialization without the permit -> impossible.

Remove the unrestricted exported free-materialization path or make it require and validate the same exact one-object permit.

This repair creates no entity semantics.

It creates no classifier, encounter, PSEPF, metabolism, CAN-008, V2 or positive actor authority.

## 10. Adoption readiness

`S2 / OBL054 = NOT READY FOR HQ ADOPTION`.

Exact reason:

`OWNER_AUTHENTICATION_FAIL_OPEN + ONE_OBJECT_SCOPE_ESCAPE`.

The identity algorithm, receipt content-addressing, semantic opacity and no-transfer direction are reusable.

The candidate requires bounded repair and another hostile review before adoption.

OBL052 therefore remains blocked on a lawfully repaired/adopted OBL054 plus its independently owned OBL053 predecessor.

## Persisted independent evidence

Machine-readable audit evidence:

`.../T2_S2_V3P1_MATERIALIZER_HOSTILE_AUDIT_R1/01_HOSTILE_AUDIT_EVIDENCE.json`

Independent hostile tests:

`rawlsing_next/tests/test_gt34_t2_s2_materializer_hostile_audit.py`

## Final

No S2 candidate code was modified.

No authority was adopted.

No real first-canary subject was materialized.

Terminal:

`FAIL__GT34_T2_OBL054_S2_OWNER_AUTHENTICATION_FAIL_OPEN_AND_ONE_OBJECT_SCOPE_ESCAPE_PROVED`
