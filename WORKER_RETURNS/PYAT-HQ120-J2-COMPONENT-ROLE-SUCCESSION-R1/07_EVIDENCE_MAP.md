# PYAT HQ120-J2 — EVIDENCE MAP

All current-tree evidence was read at commission head `a7ac40579cd5be11d4fdff3237bb00a3f6cc87a5` unless a different immutable historical experiment ref is explicitly named.

No raw survey source was opened.

## A. Commission

`WORKER_COMMISSIONS/PYAT-HQ120-J2-COMPONENT-ROLE-SUCCESSION-R1/00_COMMISSION.md`

Requires semantic succession rather than field resemblance and demands exact historical semantics, authority, mapping, producer, consumer and replay/provenance.

## B. Historical family-item role authority

### `data/ddm_build_copy/manifests/question_family_registry.yaml`

Observed governed family role groups include:

- `exception_case`;
- `elective_case`;
- `social_condition`;
- `family_size_condition`;
- `economic_condition`;
- `target_case`.

The same registry uses roles in:

- boundary rules;
- response-role rules;
- target-resolution rules.

The target-resolution basis explicitly names `question_family_registry.item_role_groups`.

### `data/ddm_build_copy/ddm_v550j_joint_patterns.py`

Relevant behavior:

- family item maps derive `item_role` from governed `item_role_groups`;
- `_resolve_family_item_semantics` resolves `item_role`;
- response-role fallback selection is role-scoped;
- target-resolution-rule selection is role-scoped;
- resolved item semantics carry target/permission consequences.

Finding:

`v550j_item_role` is governed family semantic information, not generic orchestration metadata.

## C. Historical V551J role and contribution semantics

### `data/ddm_build_copy/ddm_v551j_schema.py`

V2.2.3 component-index contract includes:

- `v550j_item_role`;
- `v551_evidence_role`;
- component authority/identity/status fields;
- `component_evidence_role`;
- `component_certification_contribution`;
- `component_v552_linkage_class`.

### `data/ddm_build_copy/ddm_v551j_packets.py`

Key logic:

- `V2_CONTEXT_ITEM_ROLES` identifies context/conditioning/metadata/administrative/nonrelation classes;
- `_evidence_role_status` distinguishes relation evidence, context evidence, unknown and missing;
- component builder chooses source item role from V551 evidence role -> item role -> semantic role;
- relation-like requires a matched component, non-context/nonrelation role and V551 relation-evidence permission;
- contribution mapping emits relation/context/special-or-missing/explained-nonrelation/blocked/unresolved;
- the identical contribution token is written to both `component_evidence_role` and `component_certification_contribution`;
- packet-status logic counts `relation_component`, counts context-like contribution states, blocks unresolved contribution, and requires at least two relation components.

Finding:

`component_certification_contribution` is a constitutive certification determinant.

## D. C4 information-conservation finding

### `data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/integration/G1A_C4R1_V550J_V551J_V552J_INFORMATION_CONSERVATION_RETURN.md`

C4R1 positively proved seven V551J->V552J->V553 loss gaps.

Gap 5 is:

`component roles and certification-contribution roles`.

The return states that the V551J component index includes V550J item roles, V551 evidence roles and certification contribution, while the actual reduced V552J/V553 path omitted them.

### `data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/13_G1A_RESIDUAL_ROUND_HQ_BANK_AND_SECOND_CLOSURE_ROUTING.md`

HQ banked C4R1's seven positive information-loss gaps, including role/certification contribution.

## E. C4R2A hostile conservation benchmark — historical experiment only

Immutable prototype commit inspected:

`f2c26d36c1f3411e325d7af49b63e8595b87f7e7`.

### `data/ddm_build_copy/ddm_v552j_handoff.py` at that ref

The prototype required each conserved component to carry:

- `component_id`;
- `item_order`;
- `component_contract_hash`;
- `v550j_item_role`;
- `component_evidence_role`;
- `component_certification_contribution`.

### `data/ddm_build_copy/ddm_v553_canonical_harmonization.py` at that ref

The consumer fail-closed validated the same component fields.

### `data/ddm_build_copy/test_c4r2a_v551j_v552j_v553_information_conservation.py` at that ref

Gap-5 test asserts exact V550J component roles and exact `relation_component` contribution tokens survive.

### Corrective status

`data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/14_VERKHOVOD_CORRECTIVE_STAY_AND_P10_RECLOSURE_REALIGNMENT.md`

Reclassifies C4R2A as non-authoritative future repair prototype. J2 therefore uses it only as a semantic conservation benchmark.

## F. Current common component-vector authority

### `rawlsing_next/pre553_component_authority_vector.py`

`ComponentAuthorityBinding` contains:

- component ID/ref;
- producer family;
- `role`;
- ordinal;
- multiplicity;
- authority state;
- authoritative value digest;
- value-authority ref;
- negative/limit refs.

The `role` field is only required to be a nonempty string.

`ComponentAuthorityVectorReceipt` adds exact authority-dimension contract, governed set, replay root, coverage/nonempty/unanimity proofs and scalarization disposition.

Finding:

the receipt is sufficient as an exact role-vector substrate, but `role` itself does not supply role authority.

### `rawlsing_next/tests/test_pre553_component_authority_vector.py`

Synthetic helper defaults to `role="MEMBER"`.

M4 integration passes component role into `participant_role` reference edges.

Finding:

the tests prove role-token carrier/reload integrity, not historical family-role semantic mapping.

## G. MX02 adoption history

### `.../N013_MX_DISCOVERY_AND_CONTRACTS/CORPUS/ORIGINAL/7e8b492772e6__RESULT.md`

MX02 R1 found existing carrier capacity but a missing common vector semantic receipt. It specifically noted V551J's `component_certification_contribution` as existing historical component capital.

### `.../N013_MX_DISCOVERY_AND_CONTRACTS/CORPUS/ORIGINAL/2b685053c782__RESULT.md`

MX02 R2 introduced `ComponentAuthorityVectorReceipt@1.0.0`.

It owns:

`VECTOR SUBJECT × AUTHORITY DIMENSION × GOVERNED COMPONENT SET × PROJECTION DECISION`.

It preserves producer refs, roles/order/multiplicity, authority state/value binding and replay.

It did not add a historical-role mapping producer.

### `data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/34_PREV3_WAVE1_R2_AND_AS3R3_CARDINALITY_ADOPTION.md`

Authority 34 adopts MX02 R2 common component-vector authority.

## H. Current I03

### `rawlsing_next/_pre553_query_common.py`

Target components carry:

- exact target ref;
- topology;
- domain;
- target-domain replay ref;
- topology authority;
- response-semantic authority;
- included states.

No governed family-item role or certification-contribution field exists.

### `rawlsing_next/_pre553_query_eval.py`

I03 preserves exact per-respondent multi-target configuration, order, risk/denominator membership and authority closure.

It does not derive family-item role or contribution classification.

## I. Current M1

### `rawlsing_next/pre553_learned_empirical_adjudication.py`

M1 generic jurisdiction:

`EXACT_I05_DISCOVERY_EVIDENCE + EXPLICIT_EXACT_FAMILY_RULE_BINDING -> LearnedEmpiricalDisposition@1.0.0`.

Relevant exact surfaces:

- `M1FamilyRuleBinding`;
- `M1PrerequisiteChannel`;
- `M1AdjudicationInputBundle`;
- `M1ValidatorRegistry`;
- `M1ValidatorContext`;
- determinant/explanation/replay receipt.

A binding can specify exact validator authority/parameters, prerequisite channels, source relations, measure/weight authority, coverage, output contract and replay.

`additional_dependency_refs` are included in dependency closure but are not themselves interpreted.

### `rawlsing_next/tests/test_pre553_learned_empirical_adjudication.py`

Tests prove exact family/rule dispatch, prerequisite blocking, authority closure, state conservation and deterministic replay.

They are synthetic; no current J-role-specific family validator was found.

Finding:

M1 is the correct generic adjudication jurisdiction but does not by itself close J2.

## J. Current lifecycle

### `PYAT_CONTROL_ROOM/17_HQD118_M01_AND_LEARNED_WORLD_OWNER_ADOPTION.md`
### `PYAT_CONTROL_ROOM/18_HQD119_I123_RUNTIME_INTEGRATION_AND_I4_GATE.md`

These separate M1 learned empirical adjudication from B5 lifecycle registration/publication/current selection.

Finding:

B5 is not the historical component-certification contribution owner.

## K. Current-code negative search

At the commission head, GitHub current-code search under `rawlsing_next` returned zero occurrences for:

- `v550j_item_role`;
- `component_certification_contribution`;
- `question_family_registry`;
- `item_role_groups`;
- `relation_component`.

Search also found no production callsite for `build_component_authority_vector_receipt` outside its module; the only direct use is bounded tests.

This is not proof that no possible successor can exist. It is positive evidence that the presently installed generic common receipt has not yet been wired as an exact historical role successor.

## L. Final adjudication

Two exact role-succession functions remain without the commission's required current mapping/producer/consumer proof.

Therefore:

`PYAT_HQ120_J2_BLOCKED__J_ROLE_OR_CERTIFICATION_FUNCTION_LACKS_CURRENT_OWNER_MAPPING_OR_RETIREMENT`.
