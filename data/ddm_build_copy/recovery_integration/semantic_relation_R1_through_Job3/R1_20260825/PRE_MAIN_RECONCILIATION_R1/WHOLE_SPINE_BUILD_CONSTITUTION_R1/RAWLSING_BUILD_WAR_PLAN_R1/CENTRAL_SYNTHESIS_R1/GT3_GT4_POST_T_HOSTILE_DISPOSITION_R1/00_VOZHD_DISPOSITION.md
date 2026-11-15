# GT3/GT4 POST-T HOSTILE DISPOSITION R1

Repository: `maidiu/rawlsing`

HQ disposition basis before these records:

`fc428e35b9f161b1ffba0646d38b0bce3c846c12`

`main` remains unchanged at:

`b53f8843092e776fb83ec584399641f5f2fc3de3`

## Terminal HQ disposition

`ADOPTED__GT34_OBL053_ONE_OBJECT_NONACTOR_SUBJECT_ENTITY_SEMANTIC_AUTHORITY__EXACT_CONSTITUTIVE_GRAIN`

`FAIL_BANKED__GT34_OBL054_S2_OWNER_AUTHENTICATION_AND_ONE_OBJECT_SCOPE_DEFECTS__BOUNDED_REPAIR_REQUIRED`

`FAIL_BANKED__GT34_OBL055_S3_AUTHENTICATION_AND_REPLAY_INTEGRITY_GAPS__BOUNDED_REPAIR_REQUIRED`

`POSITIVE_V3_EXECUTION = NOT_AUTHORIZED`

## T1 / OBL053

Independent hostile terminal:

`PASS__GT34_T1_OBL053_S1_ONE_OBJECT_SEMANTIC_AUTHORITY_LAWFUL_FOR_BOUNDED_ADOPTION`

Worker evidence tip:

`29770c954fa375d40d4e0d71583645544b92e61c`

Hostile evidence commit:

`38878d78222fd5945896c3252d8a43ebe1d2529b`

T1 independently recomputed and matched all four S1 semantic hashes and found the candidate lawful only under its exact constitutive generated-world reading.

HQ therefore adopts exactly:

- authority: `GT34_OBL053_ONE_OBJECT_NONACTOR_SUBJECT_ENTITY_SEMANTIC_AUTHORITY@1.0.0`
- authority semantic hash: `e024220dfd21bd2544f86dd9ceec332b42115ff55afdc94183811d2ed52924ed`
- admitted frozen generation-seed hash: `b20687b91e0a7a9cc64a96e229e58244041d54b4ea9c73a182b2f9da0cd2ef53`
- exact prospective/current-at-semantic-grain object hash: `d9647033de698e38e16001984580e1e0af3ba30c362acf3258aef3b78070cb53`
- exact object ID: `urn:rawlsing:gt34:generated-nonactor-subject-semantic-object:sha256:d9647033de698e38e16001984580e1e0af3ba30c362acf3258aef3b78070cb53`
- generated-fact provenance/integrity receipt hash: `1561942f1fe4fc43b248c61be866c0bc459773b7c6dbb8e393e13b064cdacce0`

The adopted objective entity facts at exactly this one-object generated-world grain are:

- `entity_family = NONACTOR_FACILITY`
- `facility_domain = HEALTHCARE_DELIVERY`
- `facility_form = CLINIC`
- `facility_function = OUTPATIENT_HEALTHCARE_SERVICE_DELIVERY`
- `ownership_status = PUBLIC_SECTOR`

These facts are constituted by the exact adopted generated-world rule + frozen seed. They are **not** empirical observations and the receipt is not independent empirical corroboration.

The adoption does not emit:

`SUBJECT_IS_PUBLIC_CLINIC_OR_HOSPITAL`.

That proposition remains separately owned by OBL048.

The adoption also does not create a V3 `subject_ref`; OBL054 remains required for owner-preserving materialization.

### OBL053 closure

`OBL053 = CLOSED_AT_EXACT_ONE_OBJECT_CONSTITUTIVE_SEMANTIC_GRAIN`

No second seed/object, general facility ontology, arbitrary caller object, empirical-world claim, actor/contact/use/encounter/exposure, Q69B semantic borrowing, classifier, comparator, PSEPF, metabolism, CAN-008, V2 or positive-V3 authority is adopted.

## T2 / OBL054

Independent hostile terminal:

`FAIL__GT34_T2_OBL054_S2_OWNER_AUTHENTICATION_FAIL_OPEN_AND_ONE_OBJECT_SCOPE_ESCAPE_PROVED`

Target S2 remains not adopted.

T2 proved two exact defects:

1. the caller can self-certify an arbitrary semantic owner by recomputing S2's owner-binding checksum;
2. the claimed one-object ceiling is bypassable through the exported stateless materializer or a fresh registry instance.

The reusable S2 properties remain:

- deterministic content addressing;
- semantic opacity;
- owner identity transport;
- no semantic-owner transfer;
- replay stability for exact inputs.

The minimum repair must:

- authenticate ownership against an independently accepted authority/adoption root that the caller cannot mint;
- bind the exact adopted S1 authority/object to one immutable content-addressed one-object permit/scope;
- require that permit for every materialization path;
- make exact duplicate use idempotent;
- reject every distinct object under the V1 permit regardless of registry re-instantiation;
- remove or gate the unrestricted stateless materialization path;
- preserve zero semantic interpretation/transfer.

`OBL054 = RETURN_REQUIRED__BOUNDED_REPAIR`.

## T3 / OBL055

Independent hostile terminal:

`FAIL__GT34_T3_OBL055_S3_ADP010_V3P5_EXECUTOR_AUTHENTICATION_AND_REPLAY_INTEGRITY_GAPS`

Target S3 remains not adopted.

T3 proved the bounded executor's transition shape is largely correct but authentication/replay is insufficient for a real canary. Exact defects include:

- subject ingress shaped but not mutually authenticated;
- exact ADP-008 phase-state ref not replay/identity-bound;
- applicability authority signature not bound;
- contact witness authority/independence not authenticated;
- co-location can be laundered through caller relabeling;
- `validate_record()` cannot reconstruct and verify replay bindings;
- required ADP-010 authority/registry/rule hash provenance not enforced;
- `source_candidate_id` not derived/validated.

`OBL055 = RETURN_REQUIRED__BOUNDED_REPAIR`.

For project hygiene, OBL055 repair should consume the final adopted OBL054 materializer identity/receipt law rather than repair subject-ingress authentication against an in-flight materializer schema.

Therefore the immediate semantic critical path is:

`OBL054 repair -> hostile PASS -> HQ adoption -> exact real subject materialization -> OBL052 closure`

After OBL054 is adopted, OBL055 repair may bind the exact adopted materializer contract. After OBL052 closes, OBL048 classifier work may proceed.

At that point OBL048 and OBL055 can proceed in parallel.

No positive V3 execution is authorized by this disposition.
