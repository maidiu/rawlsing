# Special questions — exact answers

## 1. Is PRE553_STRUCTURAL_ADMISSION_RULE@1.0.0 still sufficient/current for relations permitted by current Field Forge R2?

**No as a universal Field Forge relation grammar; yes inside its own direct structural-admission jurisdiction.**

`pre553_structural_admission.py` is physically current and tested. Its rule is generic over exact EmpiricalFact/Query/authority inputs and can lawfully produce `StructuralEmpiricalAdmission` or typed refusal under exact P06 authority.

But HQD-115 names it a **compatibility structural-admission implementation**, and the adopted GT12 actor-independent Field Forge path explicitly bypasses I04/P06. Current Field Forge relations have their own semantic owner and relation-admission owner.

FF02 classification:

`NOT_REQUIRED_UNDER_CURRENT_FF02_GRAIN`

Do not delete it; do not promote it to universal FF ownership.

## 2. Which exact relation object represents a currently admitted actor-independent relation?

Current GT12 relation:

- class: `ExactConditionalSupportProfile`
- family: `EXACT_CONDITIONAL_SUPPORT_PROFILE_WITHIN_SCOPE@1.0.0`
- semantic owner: `FIELD_FORGE_ACTOR_INDEPENDENT_RELATION_OWNER`
- current adopted content hash:
  `1ffdfe536adc01d35709521145b9c8057f589c20983f507d5ed6197c4ad27d19`
- deterministic object ID:
  `urn:rawlsing:field-forge:conditional-support:sha256:1ffdfe536adc01d35709521145b9c8057f589c20983f507d5ed6197c4ad27d19`

The exact admission object is `Prev3FieldForgeRelationAdmission` under `PREV3_FIELD_FORGE_RELATION_ADMISSION@1.0.0`; it preserves the relation ref/owner and does not become the relation's semantic owner.

## 3. Can current code represent typed refusal without manufacturing a positive structural object?

**Yes.**

Current relation producer/admission/M1 preparation code all preserve nonpositive states. Nonpositive admission receives no positive permission. Blocked GT2 relation objects cannot carry a positive conditional-count profile.

For a new LiTS family, the **downstream refusal representation is already sufficient**; what is missing is the claim-specific upstream relation/refusal producer/admission instantiation.

## 4. Can exact current EmpiricalFact/query/predicate/authority refs be dereferenced directly?

**Yes.**

The final LiTS checkpoint v3 retains complete current canonical object preimages and verifies constructor re-materialization/source-free replay. FF02 readiness is:

`FF02_READY__NO_SOURCE_REOPEN_REQUIRED`

Exact inventory: 60 facts, 63 queries, 35 predicates, 24 authority snapshots, 50 discovery receipts, one discovery authority, one universe, 225 exact refs.

No older compact product or ASTRA summary is required.

## 5. Is field_forge_conditional_support.py generic enough for LiTS current objects?

**No.**

It is exact and robust, but deliberately frozen to the historical/current GT2 canary:

- Q86B conditioner;
- Q86A target;
- Afrobarometer R5;
- one universe;
- RAW/unweighted;
- two-target complete domain;
- frozen role/order semantics.

Passing arbitrary LiTS objects into it would be semantic coercion, not reuse.

## 6. Which GT2/GT12 parts are reusable current implementation versus proof precedent?

Reusable implementation law:

- exact object dereference and identity verification;
- Field Forge relation owner distinct from PREV3 admission owner;
- exact relation/admission refs;
- role/order/scope/risk conservation;
- permission narrowing;
- typed refusal conservation;
- exact authority/provenance/replay closure;
- reference-preserving admitted-relation envelope.

Canary-specific / proof precedent:

- Q86 conditional-support semantics;
- Afrobarometer source/risk identities;
- GT2 admission authority;
- GT12 C->D bridge;
- GT12 permission translation;
- `STRUCTURAL_MEDIATION_INPUT` unless separately authorized;
- V554/V557/V558 CONTEXT descent as mandatory topology.

## 7. Does current relation admission require a target-use token whose name risks overclaim?

**Yes.**

The GT2 relation-admission path and relation M1 compatibility path require:

`STRUCTURAL_MEDIATION_INPUT`

That is safe only under exact claim-specific authority. Field Forge R2 explicitly denies an automatic dependence/coexistence -> mediation inference.

For LiTS FF02, reuse is forbidden unless FF02-A/HQ separately authorizes mediation semantics.

## 8. What is the smallest implementation gap if FF02-A admits one or more relation families?

A bounded **LiTS claim-specific relation/admission adapter**.

It does not need a new architecture. It must:

- consume exact retained LiTS objects source-free;
- validate exactly the approved relation family;
- emit a positive actor-independent relation or exact typed refusal;
- preserve exact scope/risk/authority/provenance/replay;
- bind the exact claim-specific admission authority;
- emit/replay the existing PREV3 relation-admission envelope if positive;
- use only an actually authorized target-use token.

Classification:

`CLAIM_SPECIFIC_EXTENSION_REQUIRED`

No gap is being fixed in this worker.
