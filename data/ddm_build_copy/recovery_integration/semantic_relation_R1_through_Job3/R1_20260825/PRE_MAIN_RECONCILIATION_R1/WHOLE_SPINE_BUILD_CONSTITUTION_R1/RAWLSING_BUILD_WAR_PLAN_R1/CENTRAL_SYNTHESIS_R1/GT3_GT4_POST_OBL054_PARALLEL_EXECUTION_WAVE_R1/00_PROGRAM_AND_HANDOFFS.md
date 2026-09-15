# GT3/GT4 POST-OBL054 PARALLEL EXECUTION WAVE R1

Repository: `maidiu/rawlsing`

Canonical commissioning basis before this instruction commit:

`72e6debeccd6f7cf6d63b18756985e2433848bf7`

## Campaign state

OBL053 is CLOSED at corrected one-object semantic authority grain.

OBL054 is CLOSED at corrected owner-authenticated one-object materializer grain.

Current OBL054 HQ adoption artifact:

`../GT3_GT4_OBL054_CORRECTED_MATERIALIZER_HQ_ADOPTION_R1/01_OBL054_CORRECTED_MATERIALIZER_HQ_ADOPTION.json`

blob:

`fc46d377dafa5b2c4e274d702e7f26268aa429cb`

Adopted materializer:

`GT34_V3P1_CORRECTED_OWNER_AUTHENTICATED_ONE_OBJECT_SUBJECT_MATERIALIZER@2.0.0`

module:

`rawlsing_next/gt34_u2_v3p1_authenticated_subject_materializer.py`

module blob:

`b0cb39a9a975381f3f3b4a03e7e435b2932e89b9`

Accepted-root hash:

`1563a1661d3e0a76e6781633f1b590147e26ab21014674bbe732f68cef6acfa8`

Exact one-object permit hash:

`3eeea2dcfa0a70f1a5b6ce15d41d9f83d84e39ecde816896150fff21e77573dc`

Corrected OBL053 semantic-object hash:

`9a5fbe9a7c272cb2a60e425f09b206f0d25dd2d95caa07028bdb021130c32547`

Two independent lanes are now lawful.

They may run in parallel.

Neither worker may consume the other worker's in-flight conclusion.

## Context-discipline law

Do not recursively ingest the whole project.

Each worker should read:

1. this commissioning file;
2. the exact lane-specific artifacts named in its section;
3. only directly referenced code/tests needed to execute that lane.

Do not load unrelated historical waves, broad handoffs, or whole-project state unless a named artifact is missing or directly contradictory.

Return discovered contradictions to HQ rather than expanding scope.

---

# WORKER W1 — OBL052 EXACT FIRST-CANARY SUBJECT_REF MATERIALIZATION R1

Profile:

`BOUNDED_CURRENT_EXECUTION_AND_GOVERNED_PROOF`

## Read only the minimum lane-A set

Required:

1. this file;
2. `../GT3_GT4_OBL054_CORRECTED_MATERIALIZER_HQ_ADOPTION_R1/00_VOZHD_DISPOSITION.md`;
3. `../GT3_GT4_OBL054_CORRECTED_MATERIALIZER_HQ_ADOPTION_R1/01_OBL054_CORRECTED_MATERIALIZER_HQ_ADOPTION.json`;
4. `../GT3_GT4_OBL053_HASH_GRAPH_INTEGRITY_REPAIR_WAVE_R1/V1_OBL053_HASH_GRAPH_INTEGRITY_REPAIR_R1/01_REPAIRED_HASH_GRAPH_CANDIDATE.json`;
5. `rawlsing_next/gt34_u2_v3p1_authenticated_subject_materializer.py`;
6. U2/U3 tests only as needed to verify the adopted materializer contract.

Do not read the OBL055/T3 lane unless a direct shared-contract contradiction appears.

## Mission

Execute exactly one current production materialization of the already-adopted corrected OBL053 semantic object through the already-adopted OBL054 materializer.

This is execution under adopted authority.

It is not authority creation.

## Exact object bytes

Take exactly:

`prospective_semantic_object.semantic_projection`

from the repaired OBL053 candidate.

Canonicalize using the declared content-addressing law:

- lexicographically sorted mapping keys;
- compact comma/colon separators;
- UTF-8;
- Unicode preserved without ASCII escaping;
- ordered sequences preserved.

The resulting bytes MUST SHA-256 to:

`9a5fbe9a7c272cb2a60e425f09b206f0d25dd2d95caa07028bdb021130c32547`

If not, stop and return FAIL.

Do not alter the semantic projection.

## Materialization law

Use the adopted U2 production path and exact current constants.

Construct the exact `OwnerBoundSubjectInput` for the corrected OBL053 object using:

- current OBL053 semantic-owner ID/version/hash;
- exact current semantic-object ref;
- exact canonical semantic-object bytes;
- `CURRENT_EVIDENCE_REFS`;
- `CURRENT_PROVENANCE_REFS`;
- mechanical `compute_owner_binding_content_hash(...)`.

Materialize only with:

`CURRENT_ONE_OBJECT_MATERIALIZATION_PERMIT`.

Do not use the private shadow path.

Do not construct an alternate root or permit.

## Required persisted output

Persist a machine-readable current materialization artifact containing at minimum:

- materializer ID/version;
- OBL054 HQ adoption artifact blob;
- accepted-root hash;
- permit ID/hash;
- exact OBL053 semantic-object ID/hash;
- exact owner ID/version/hash;
- exact subject_ref;
- subject_ref_hash;
- exact production receipt ID/hash;
- full production receipt wire representation;
- evidence refs;
- provenance refs;
- replay input hash;
- proof that semantic_owner_transfer = false;
- proof that semantic_fields_interpreted = false;
- explicit statement that no classifier/contact/encounter/exposure assertion follows.

Do not persist semantic-object bytes redundantly if the exact canonical source artifact + hash is sufficient.

## Required governed proof

Create an executable bounded court proving at minimum:

1. canonical OBL053 object bytes reproduce exact object hash;
2. exact adopted root/permit validate;
3. production materialization succeeds;
4. independently recomputed subject-ref identity equals persisted subject_ref;
5. independently recomputed production receipt hash equals persisted receipt hash;
6. exact replay produces byte-for-data-model identical receipt;
7. fresh registry instance with exact same input returns same receipt/ref;
8. any one-bit/object-byte mutation fails;
9. any owner/object/evidence/provenance mutation fails;
10. historical OBL053 root fails;
11. alternate/second object fails under current permit;
12. shadow path is not used and shadow receipt cannot satisfy persisted production artifact;
13. persisted receipt is bound to adoption blob/root/permit;
14. semantic object fields are not interpreted by materializer;
15. no classifier proposition is emitted;
16. no actor/contact/use/encounter/exposure is emitted;
17. no comparator/PSEPF/metabolism/CAN-008/V2/positive-V3 authority is created;
18. repository contains exactly one current first-canary materialization artifact for this execution lane.

## OBL052 closure ceiling

Preferred terminal:

`PASS__GT34_W1_OBL052_FIRST_CANARY_SUBJECT_REF_MATERIALIZED__HQ_CLOSURE_READY`

Worker PASS means:

- the exact current subject_ref + production receipt now exist;
- the execution is mechanically proven and idempotent;
- OBL052 is ready for HQ closure.

Worker does not itself change central obligation ledgers.

Worker does not define OBL048.

Worker does not assert `SUBJECT_IS_PUBLIC_CLINIC_OR_HOSPITAL`.

Worker does not invoke ADP-010.

Worker does not assert contact, encounter or exposure.

## Required return

`.../GT3_GT4_POST_OBL054_PARALLEL_EXECUTION_WAVE_R1/W1_OBL052_FIRST_CANARY_SUBJECT_MATERIALIZATION_R1/00_RETURN.md`

Persist machine-readable evidence beside the return.

---

# WORKER W2 — OBL055 S3 ADP-010 AUTHENTICATION + REPLAY REPAIR R1

Profile:

`BOUNDED_IMPLEMENTATION_REPAIR_AND_GOVERNED_COURT`

## Read only the minimum lane-B set

Required:

1. this file;
2. `../GT3_GT4_OBL053_055_INDEPENDENT_HOSTILE_REVIEW_WAVE_R1/T3_S3_ADP010_V3P5_EXECUTOR_HOSTILE_AUDIT_R1/00_RETURN.md`;
3. its `01_HOSTILE_AUDIT_EVIDENCE.json`;
4. original S3 target module `rawlsing_next/v3_adp010_oee_executor.py`;
5. original S3 tests;
6. T3 hostile tests;
7. OBL054 HQ adoption disposition + JSON;
8. adopted U2 materializer module only to learn the exact current subject-ingress/materialization-receipt contract;
9. accepted ADP-010 / ADP-008 / ADP-020 authority artifacts named by T3 only as required.

Do not read the OBL052/W1 lane unless a direct shared-contract contradiction appears.

Do not wait for W1.

W2 repairs a generic executor authentication contract against adopted OBL054; it does not need W1's in-flight current subject_ref to implement that contract.

## Historical target

Original S3 semantic candidate:

`5bed04b83f0dc61e500da26130892e46ce9c86ff`

Original evidence execution:

`c70808c993b7e236e5535a03e22fe89cc3759d1e`

Target module historical blob:

`cd6e978eea25384482ef2ab75547b8d33bcc4fb7`

Historical S3 is not adopted.

Preserve its exact historical evidence.

## Mission

Construct the smallest lawful successor that closes exactly T3's authentication/replay defects while preserving the sound S3 transition semantics.

Do not redesign ADP-010.

Preserve:

- AVAILABLE -> OPPORTUNITY -> ENCOUNTER sequencing;
- exact parent actor/subject continuity;
- ZERO_DRAW core-v1 stochastic behavior;
- no hidden RNG;
- no EXPOSURE API;
- no broader actor mutation;
- deterministic canonical identity;
- existing rejection of direct insufficient witness classes.

## Required repair set

Close all T3 adoption blockers:

1. **subject ingress authentication**
   - authenticate one mutually bound chain containing:
     - subject_ref;
     - semantic owner ID/version/hash;
     - semantic object identity;
     - OBL054 materializer ID/version;
     - OBL054 adoption/root/permit identity;
     - exact materialization receipt identity/content;
     - exact causal-use permission;
     - exact provenance;
   - caller-shaped strings/refs alone cannot establish ingress.

2. **ADP-008 phase-state authentication**
   - authenticate exact phase-state record/receipt;
   - bind exact state ref/hash and accepted authority/registry identity into candidate replay.

3. **positive applicability authentication**
   - authenticate exact owning authority;
   - bind authority ID/version/content hash + receipt identity into replay.

4. **contact-occurrence witness authentication**
   - require separately competent witness authority/receipt;
   - authenticate independence proof;
   - bind witness authority identity + receipt + independence proof into replay.

5. **anti-laundering**
   - co-location/co-presence/proximity/shared endpoint/structural target/institution class remain insufficient regardless of caller relabeling/wrapping.

6. **accepted provenance**
   - require exact accepted ADP-010 authority/registry/rule-hash provenance under existing law.

7. **source candidate identity**
   - derive and validate `source_candidate_id` from exact candidate material.

8. **reconstructible replay**
   - persist enough exact candidate material/refs to recompute `source_candidate_replay_hash`.

9. **record validation completeness**
   - every mutable record field must be directly identity-bound or transitively committed by a replay hash that `validate_record()` actually recomputes.

10. **historical hostile closure**
    - original S3 court plus every T3 hostile probe must pass against the successor.

## OBL054 binding

The successor must recognize as current only the adopted materializer contract rooted in:

- OBL054 adoption artifact blob:
  `fc46d377dafa5b2c4e274d702e7f26268aa429cb`;
- materializer:
  `GT34_V3P1_CORRECTED_OWNER_AUTHENTICATED_ONE_OBJECT_SUBJECT_MATERIALIZER@2.0.0`;
- accepted-root hash:
  `1563a1661d3e0a76e6781633f1b590147e26ab21014674bbe732f68cef6acfa8`;
- permit hash:
  `3eeea2dcfa0a70f1a5b6ce15d41d9f83d84e39ecde816896150fff21e77573dc`.

Historical S2/U1 or historical invalid OBL053 roots must not authenticate subject ingress.

## Successor identity

Prefer a distinct successor implementation identity/version rather than silently turning the failed historical S3 candidate into current authority.

Preserve API compatibility only where lawful.

If an in-place module-path repair is technically necessary, explicitly preserve historical S3 by exact candidate SHA/blob and explain why the current implementation identity cannot be confused with the failed candidate.

## Test fixtures

Synthetic fixtures may be used to test generic accepted-contract mechanics.

They must be explicitly noncurrent test fixtures.

Do not materialize or persist W1's current first-canary subject.

Do not claim a synthetic OEE record is current canary truth.

## Court

Run a governed bounded court containing:

- original S3 tests;
- all T3 hostile probes;
- new repair-specific tests needed to prove exact OBL054 binding and replay validation.

The semantic candidate SHA must identify the commit containing the complete successor implementation + tests before transient court configuration.

## PASS ceiling

Preferred terminal:

`PASS__GT34_W2_OBL055_S3_AUTHENTICATION_REPLAY_REPAIRED__NO_ADOPTION`

PASS means only:

- exact T3 defects are repaired in candidate form;
- original sound S3 behavior is preserved;
- candidate is ready for independent hostile review.

Worker does not adopt OBL055.

Worker does not invoke current first-canary OEE.

Worker does not create EXPOSURE.

Worker does not create comparator/PSEPF/metabolism/CAN-008/V2/positive-V3 authority.

## FAIL rule

Return FAIL if a T3 hostile attack still succeeds or if closing it requires semantic authority beyond the accepted ADP-010/008/020 + adopted OBL054 contracts.

## Required return

`.../GT3_GT4_POST_OBL054_PARALLEL_EXECUTION_WAVE_R1/W2_OBL055_S3_AUTHENTICATION_REPLAY_REPAIR_R1/00_RETURN.md`

Persist machine-readable evidence beside the return.

---

# HQ fan-in law

W1 and W2 are independent parallel workers.

HQ may adjudicate either return as soon as it arrives.

Do not wait for both if one lane finishes first.

If W1 passes first:

`W1 -> HQ OBL052 closure -> immediately commission OBL048 classifier lane`

without waiting for W2.

If W2 passes first:

`W2 -> bank candidate -> immediately commission independent OBL055 hostile audit`

without waiting for W1.

This asynchronous fan-in is deliberate and is the propulsion strategy for this phase.

Neither worker may move central, PRE-MAIN or main.
