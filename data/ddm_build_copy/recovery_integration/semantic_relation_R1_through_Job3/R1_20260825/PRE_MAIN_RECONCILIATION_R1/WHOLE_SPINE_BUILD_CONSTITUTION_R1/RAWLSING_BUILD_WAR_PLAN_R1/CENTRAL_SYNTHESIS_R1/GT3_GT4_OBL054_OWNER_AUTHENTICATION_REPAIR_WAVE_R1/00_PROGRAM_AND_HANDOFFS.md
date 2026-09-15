# GT3/GT4 OBL054 OWNER AUTHENTICATION / ONE-OBJECT SCOPE REPAIR WAVE R1

Repository: `maidiu/rawlsing`

Commissioning authority: VOZHD / grounded project decision.

Canonical commissioning basis before this instruction commit:

`ef46f615db1cb11ededc4afd8e3b4aeca95e0bf4`

Current project state:

- OBL053 is HQ-adopted and CLOSED at exact one-object constitutive semantic grain.
- OBL054 is RETURN_REQUIRED after T2 hostile FAIL.
- OBL052 is blocked only on OBL054.
- OBL055 is intentionally blocked on OBL054 so S3 repair can bind the final adopted materializer contract.
- OBL048 is blocked on OBL052.
- positive V3 execution remains forbidden.

## Immutable OBL053 trust anchor

HQ adoption artifact:

`data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/GT3_GT4_POST_T_HOSTILE_DISPOSITION_R1/01_OBL053_HQ_ADOPTION.json`

Exact Git blob:

`286ff7b851e920ff2760082d8b2fb194560ab127`

Exact adopted owner:

- authority ID: `GT34_OBL053_ONE_OBJECT_NONACTOR_SUBJECT_ENTITY_SEMANTIC_AUTHORITY`
- authority version: `1.0.0`
- authority semantic hash: `e024220dfd21bd2544f86dd9ceec332b42115ff55afdc94183811d2ed52924ed`

Exact adopted semantic object:

- object ID: `urn:rawlsing:gt34:generated-nonactor-subject-semantic-object:sha256:d9647033de698e38e16001984580e1e0af3ba30c362acf3258aef3b78070cb53`
- object content hash: `d9647033de698e38e16001984580e1e0af3ba30c362acf3258aef3b78070cb53`
- generated-fact provenance/integrity receipt hash: `1561942f1fe4fc43b248c61be866c0bc459773b7c6dbb8e393e13b064cdacce0`

No other owner or object is admitted for this repair.

## Target failed candidate

S2 semantic candidate:

`38257e57bd5e2d862edfcd1efb610c4d15774b37`

Original evidence execution:

`e9df80b9b4aca29f7002257d8bf044fa21eef45e`

Original governed court:

`34016836165`

Production module:

`rawlsing_next/gt34_s2_v3p1_subject_registry_materializer.py`

T2 hostile terminal:

`FAIL__GT34_T2_OBL054_S2_OWNER_AUTHENTICATION_FAIL_OPEN_AND_ONE_OBJECT_SCOPE_ESCAPE_PROVED`

T2 return:

`.../GT3_GT4_OBL053_055_INDEPENDENT_HOSTILE_REVIEW_WAVE_R1/T2_S2_V3P1_MATERIALIZER_HOSTILE_AUDIT_R1/00_RETURN.md`

T2 hostile evidence run:

`34018861625`

T2 proved:

1. caller-supplied owner identity can self-certify through S2's own checksum;
2. the one-object ceiling is bypassable through the exported stateless materializer and fresh registry instances.

The deterministic identity, semantic opacity and no-owner-transfer design are otherwise reusable.

---

# WORKER U1 — OBL054 S2 OWNER AUTHENTICATION + ONE-OBJECT SCOPE REPAIR R1

Profile:

`BOUNDED_REPAIR_AND_GOVERNED_COURT`

Mission:

Repair only the two exact T2 defects while preserving S2's already-good deterministic/content-addressed, semantic-opaque, owner-preserving behavior.

Do not redesign V3-P1.

Do not build a generic authority registry.

Do not create new entity semantics.

Do not materialize a second object.

## Required repair architecture

### A. Accepted-owner authentication must terminate in the immutable HQ root

The repaired materializer must not accept arbitrary owner ID/version/hash merely because a caller can recompute a matching checksum.

Every successful V1 materialization must mechanically prove that the presented owner/object package equals the exact currently admitted OBL053 trust anchor above.

At minimum validate exact equality to:

- HQ adoption artifact blob `286ff7b851e920ff2760082d8b2fb194560ab127`;
- authority ID/version/hash;
- semantic object ID/hash;
- generated-fact provenance/integrity receipt hash.

The caller may present these values, but cannot substitute different values and still succeed.

The materializer's accepted-root logic must be part of the implementation candidate itself, not a caller-created arbitrary registry/capability that can be instantiated with fake authority roots.

The existing owner-binding content hash may remain as transport/integrity material.

It must not be treated as proof that the owner is accepted.

### B. One-object scope must be an immutable permit invariant, not mutable instance memory

Define the smallest deterministic one-object materialization permit/scope necessary for V1.

The permit must name exactly:

- the OBL053 HQ adoption root;
- the exact admitted authority ID/version/hash;
- the exact semantic object ID/hash;
- the exact generated-fact provenance/integrity receipt hash;
- the S2 materializer ID/version;
- a one-object cardinality ceiling.

The permit must itself be deterministic/content-addressed.

Every public materialization path, including any stateless helper, must require and validate the same permit.

A new Python registry instance must not create new permission.

Therefore:

- exact admitted object + exact permit -> lawful deterministic candidate materialization;
- exact duplicate -> identical `subject_ref` / receipt;
- any distinct owner -> fail closed;
- any distinct semantic object -> fail closed;
- any altered adoption root -> fail closed;
- any altered objective-evidence receipt identity -> fail closed;
- second object attempt under a fresh registry -> fail closed;
- direct stateless call for another object -> fail closed.

Per-instance occupancy may remain as a local convenience but may not be the authority boundary.

### C. Semantic opacity remains mandatory

The materializer must not parse, infer, normalize or reinterpret the semantic object's facility facts.

It may authenticate the exact semantic-object identity/hash and accepted-owner/adoption root.

It must not emit:

- facility form/domain/function;
- public/private status;
- `SUBJECT_IS_PUBLIC_CLINIC_OR_HOSPITAL`;
- actor/contact/use/encounter/exposure;
- Q69B semantics.

`semantic_owner_transfer = false` must remain mechanically true.

## Identity / replay requirement

If the exact permit/adoption-root material changes the subject-ref or receipt identity law, that is allowed and expected if required for authenticated replay.

Do not preserve an old hash merely for cosmetic compatibility.

Document the exact new identity law.

Every field required for owner authentication and one-object scope must be directly or transitively committed by the exact content-addressed permit/ref/receipt chain.

## Testing requirements

Preserve the historical S2 and T2 audit artifacts unchanged.

Do not edit T2's hostile audit return/evidence to make the repair look green.

Create new U1 repair/regression tests that re-run the **attack cases** T2 identified with repaired expectations:

- fake owner self-certification must reject;
- arbitrary owner with self-consistent checksum must reject;
- second object via stateless helper must reject;
- second object via fresh registry instance must reject;
- adoption-root mutation must reject;
- semantic-object mutation must reject;
- objective-evidence-receipt mutation must reject;
- permit mutation must reject;
- exact duplicate accepted input remains idempotent;
- semantic bytes remain opaque;
- ref/provenance input ordering remains mechanically deterministic;
- no UUID/wall-clock/filesystem/display-label semantic input;
- no semantic-owner transfer.

Also run the still-applicable original S2 deterministic/opacity tests.

If original tests encode the vulnerable ability to materialize arbitrary synthetic owners/objects, preserve those historical tests as evidence and add a new repaired test surface rather than weakening the attack history. Clearly document which historical tests are no longer valid under the repaired accepted-root contract and why.

## Real subject boundary

Because OBL053 is now adopted, U1 may compute the **prospective exact output** for the real adopted semantic object under the repaired permit.

But U1 must mark it:

`CANDIDATE_MATERIALIZATION_OUTPUT__NOT_PROJECT_CURRENT_UNTIL_HQ_ADOPTS_REPAIRED_OBL054_AND_EXECUTES_MATERIALIZATION_ACT`.

U1 does not close OBL052.

U1 does not self-adopt OBL054.

## Governed court

Run the Rabochii governed bounded court on the exact repaired semantic candidate/evidence execution.

Persist exact:

- repaired semantic candidate SHA;
- evidence execution SHA;
- run ID;
- job ID;
- court receipt/spec identity;
- repaired permit identity/hash;
- prospective real subject-ref hash/ref;
- prospective materialization receipt hash/ID;
- exact target module/tests;
- no-semantic-widening proof.

Remove temporary branch-specific court spec after the evidence run if repo convention requires.

## Required return

Path:

`.../GT3_GT4_OBL054_OWNER_AUTHENTICATION_REPAIR_WAVE_R1/U1_S2_OWNER_AUTHENTICATION_ONE_OBJECT_SCOPE_REPAIR_R1/00_RETURN.md`

Preferred PASS terminal:

`PASS__GT34_U1_OBL054_S2_OWNER_AUTHENTICATION_AND_ONE_OBJECT_SCOPE_REPAIRED__NO_ADOPTION`

A PASS means only:

- repaired OBL054 candidate is ready for independent hostile review;
- prospective real subject identity may be known;
- no project-current V3 `subject_ref` exists yet.

If the exact repair cannot be made without broader authority, return the smallest precise BLOCKED/FAIL.

## Forbidden

Do not:

- move PRE-MAIN;
- move `main`;
- adopt OBL054;
- close OBL052;
- define OBL048 classifier;
- repair S3/OBL055;
- create or assert ADP-010 ENCOUNTER;
- create comparator/PSEPF/metabolism/CAN-008/V2/positive-V3 authority;
- broaden the exact one-object permit into a generic owner/object registry.
