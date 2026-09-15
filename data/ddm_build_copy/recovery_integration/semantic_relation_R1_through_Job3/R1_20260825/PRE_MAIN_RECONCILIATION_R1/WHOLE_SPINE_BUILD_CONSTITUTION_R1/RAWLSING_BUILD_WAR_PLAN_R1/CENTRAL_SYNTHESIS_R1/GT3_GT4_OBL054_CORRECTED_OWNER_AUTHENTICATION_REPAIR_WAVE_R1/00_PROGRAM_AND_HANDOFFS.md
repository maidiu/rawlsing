# GT3/GT4 OBL054 CORRECTED OWNER-AUTHENTICATION REPAIR WAVE R1

Repository: `maidiu/rawlsing`

Canonical commissioning basis before this instruction commit:

`61c0656eed94076cdc25d1d716b34fba8cb4498d`

Current corrected OBL053 HQ disposition:

`../GT3_GT4_OBL053_REPAIRED_HASH_GRAPH_HQ_ADOPTION_R1/00_VOZHD_DISPOSITION.md`

Fresh exact OBL053 adoption artifact blob:

`f561765bad4fdad2bbf4591f35fe7f81f8486428`

Current exact OBL053 identities:

- authority ID:
  `GT34_OBL053_ONE_OBJECT_NONACTOR_SUBJECT_ENTITY_SEMANTIC_AUTHORITY`
- authority version:
  `1.0.0`
- authority hash:
  `867962094705ce13a33b0acfc81918b930dca6ae6d7c22e8094cc1d95bc41b29`
- admitted generation-seed hash:
  `b20687b91e0a7a9cc64a96e229e58244041d54b4ea9c73a182b2f9da0cd2ef53`
- semantic object ID:
  `urn:rawlsing:gt34:generated-nonactor-subject-semantic-object:sha256:9a5fbe9a7c272cb2a60e425f09b206f0d25dd2d95caa07028bdb021130c32547`
- semantic object hash:
  `9a5fbe9a7c272cb2a60e425f09b206f0d25dd2d95caa07028bdb021130c32547`
- objective-evidence receipt hash:
  `153ff1cd67e27b435cb6ffa4127047802eb06edcc6dab7072cedf9cb3ede7d6c`

Historical S2 semantic candidate:

`38257e57bd5e2d862edfcd1efb610c4d15774b37`

Historical S2 module:

`rawlsing_next/gt34_s2_v3p1_subject_registry_materializer.py`

Historical T2 hostile return:

`../GT3_GT4_OBL053_055_INDEPENDENT_HOSTILE_REVIEW_WAVE_R1/T2_S2_V3P1_MATERIALIZER_HOSTILE_AUDIT_R1/00_RETURN.md`

Historical T2 terminal:

`FAIL__GT34_T2_OBL054_S2_OWNER_AUTHENTICATION_FAIL_OPEN_AND_ONE_OBJECT_SCOPE_ESCAPE_PROVED`

## Historical-branch preservation

The old pristine worker branch:

`agent/rabochii-gt34-u1-obl054-s2-owner-auth-one-object-scope-repair-r1`

was commissioned against historical adoption blob `286ff7...`, whose identity chain was later invalidated.

Do not repurpose or move U1.

This wave is a fresh successor commission.

## Current obligation state

`OBL053 = CLOSED`

`OBL054 = RETURN_REQUIRED`

`OBL052 = BLOCKED_ON_OBL054`

`OBL055 = BLOCKED_ON_OBL054`

No V3 `subject_ref` currently exists.

---

# WORKER U2 — OBL054 S2 CORRECTED OWNER-AUTHENTICATION + ONE-OBJECT PERMIT REPAIR R1

Profile:

`BOUNDED_IMPLEMENTATION_REPAIR_AND_GOVERNED_COURT`

## Mission

Construct the smallest lawful successor to historical S2 that closes exactly T2-D01 and T2-D02 against the fresh corrected OBL053 trust root.

Preserve:

- deterministic content-addressed subject identity;
- semantic object opacity;
- owner-preserving direction;
- exact evidence/provenance binding;
- no semantic field interpretation;
- no actor/contact/use/encounter/exposure authority;
- no classifier authority;
- no positive V3 execution.

Do not modify historical S2/T2 artifacts merely to make their old tests look green.

Create a successor implementation surface with a distinct materializer identity/version.

## T2-D01 closure — independently rooted owner authentication

The adopted successor must not accept caller-selected owner/object authority merely because the caller can compute a checksum.

Require an immutable accepted-owner/materialization root whose exact content is fixed by the fresh HQ adoption above.

At minimum the accepted root / permit must bind:

- fresh adoption artifact blob `f561765bad4fdad2bbf4591f35fe7f81f8486428`;
- exact authority ID/version/hash;
- exact admitted generation-seed hash;
- exact semantic object ID/hash;
- exact objective-evidence receipt hash;
- exact evidence/provenance lineage used by materialization;
- explicit currentness/adoption state;
- exact one-object cardinality.

A forged permit for a different owner/object must fail even if its own checksum is internally self-consistent.

The old `owner_binding_content_hash` concept may remain as transport/integrity binding.

It may never be the authentication primitive.

The historical adoption blob `286ff7b851e920ff2760082d8b2fb194560ab127` must fail current-root validation.

Historical invalid authority/object/receipt hashes must fail.

## T2-D02 closure — immutable one-object permit scope

Create one immutable content-addressed V1 materialization permit naming only the exact corrected OBL053 semantic object.

Every materialization path must require and validate that permit.

Required law:

- exact duplicate materialization under the permit -> deterministic/idempotent;
- direct stateless materialization without the permit -> impossible;
- same permit + distinct object -> fail closed before subject_ref emission;
- newly constructed registry instance + same exact object -> same subject_ref/receipt;
- newly constructed registry instance + distinct object -> fail closed;
- caller-created alternate permit for a second object -> fail current-root validation;
- no Python object instantiation may manufacture additional cardinality authority.

## Successor/historical separation

Do not delete historical S2.

Do not claim historical S2 itself passed T2.

The successor should have a distinct implementation identity so downstream adoption can authenticate the repaired surface rather than accidentally treating historical S2 as current.

Historical S2 may be used as design/reference material only.

## Exact evidence/provenance contract

Define one explicit implementation-level exact evidence/provenance contract for the corrected OBL053 object without interpreting its semantic fields.

The contract should bind at least:

- corrected OBL053 objective-evidence receipt hash;
- corrected OBL053 generation-seed hash;
- corrected OBL053 semantic-owner authority hash.

Ref IDs may be mechanical/content-addressed implementation identifiers.

They must not create semantic facts.

## Subject identity law

Preserve the useful historical S2 direction:

`semantic owner + exact semantic object + exact evidence/provenance -> deterministic subject_ref`

The semantic object bytes remain opaque.

No materializer code may parse or branch on:

- entity_family;
- facility_domain;
- facility_form;
- facility_function;
- ownership_status;
- labels/names;
- Q69B;
- ADP-010;
- actor state.

The repair may add adoption-root/permit authentication to the receipt.

If subject_ref identity itself changes from historical S2, the return must justify exactly why and show no semantic widening.

Prefer stable subject identity with stronger authenticated receipt if possible.

## Required hostile closure cases

Executable governed tests must prove at minimum:

1. exact corrected permit/root validates;
2. historical adoption blob is rejected;
3. historical invalid authority/object hashes are rejected;
4. unregistered/hostile owner self-binding attack fails;
5. caller-generated alternate permit for hostile owner/object fails;
6. stateless materialization without a valid permit is impossible;
7. same valid permit cannot emit a second distinct object;
8. multiple registry instances do not create new object permission;
9. exact duplicate input is deterministic/idempotent;
10. object bytes/ref mismatch fails;
11. evidence/provenance mutation fails permit/root validation;
12. permit/adoption root is bound into the materialization receipt;
13. semantic object bytes remain opaque and are not re-emitted as materializer truth;
14. semantic_owner_transfer remains false;
15. semantic_fields_interpreted remains false;
16. no UUID/wall-clock/display-label/environment input participates;
17. no classifier/actor/encounter/comparator/PSEPF/metabolism/CAN-008/V2/positive-V3 authority is created.

## Court requirement

Use the governed bounded court.

The semantic candidate SHA must identify the commit containing the successor implementation + tests before adding the transient court spec.

Record exact semantic candidate, evidence execution SHA, run, job, test count, receipt artifact ID/digest.

Remove transient court spec after evidence is persisted.

## Adoption ceiling

U2 may return a repaired OBL054 candidate only.

U2 does not adopt OBL054.

U2 does not materialize the real first-canary `subject_ref`.

U2 does not close OBL052.

After U2 PASS:

1. bank candidate;
2. independent hostile review;
3. only hostile PASS permits fresh OBL054 HQ adoption;
4. only after adoption may the exact real OBL053 object be materialized to close OBL052.

## Required return

`.../GT3_GT4_OBL054_CORRECTED_OWNER_AUTHENTICATION_REPAIR_WAVE_R1/U2_OBL054_CORRECTED_OWNER_AUTH_ONE_OBJECT_REPAIR_R1/00_RETURN.md`

Preferred terminal:

`PASS__GT34_U2_OBL054_CORRECTED_OWNER_AUTH_AND_ONE_OBJECT_PERMIT_REPAIRED__NO_ADOPTION`

## Forbidden

Do not:

- move `main`;
- move PRE-MAIN from the worker;
- move/repurpose old U1;
- edit historical S2/T2 evidence to erase the failure;
- use historical adoption blob `286ff7...` as current root;
- interpret OBL053 semantic fields;
- emit real first-canary `subject_ref`;
- close OBL052;
- repair OBL055;
- define OBL048;
- create positive comparator/PSEPF/metabolism/CAN-008/V2/V3 authority.
