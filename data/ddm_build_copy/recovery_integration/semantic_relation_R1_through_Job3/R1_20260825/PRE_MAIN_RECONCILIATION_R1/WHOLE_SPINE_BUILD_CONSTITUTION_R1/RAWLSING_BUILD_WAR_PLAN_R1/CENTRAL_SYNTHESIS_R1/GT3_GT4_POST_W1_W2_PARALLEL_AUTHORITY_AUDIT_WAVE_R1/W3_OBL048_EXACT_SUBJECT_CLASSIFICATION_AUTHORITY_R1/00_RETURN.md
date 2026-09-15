# GT3/GT4 W3 — OBL048 EXACT FIRST-CANARY SUBJECT CLASSIFICATION AUTHORITY / PROPOSITION R1

## Terminal

`PASS__GT34_W3_OBL048_EXACT_SUBJECT_CLASSIFICATION_AUTHORITY_CANDIDATE_GREEN__NO_ADOPTION`

## Exact execution boundary

- repository: `maidiu/rawlsing`
- worker branch: `agent/rabochii-gt34-w3-obl048-exact-subject-classification-authority-r1`
- exact working-ancestry start / commissioning ref: `8e45a995eb6b1e8132075f99124c22d48c6e61ad`
- profile: `SEMANTIC_AUTHORITY`
- frozen semantic candidate: `01645806c98b8a83070389e5375e2b7fde781c6a`
- OBL048 adopted by W3: **NO**
- W4 lane consumed: **NO**
- central / PRE-MAIN / main moved: **NO**

## Candidate disposition

W3 defines exactly one bounded semantic authority and one exact proposition candidate for the current first-canary subject.

Classification authority:

`GT34_OBL048_EXACT_FIRST_CANARY_SUBJECT_CLASSIFICATION_AUTHORITY@1.0.0`

Authority content hash:

`a0cd9714145ea4c7edd862b2a0dfdd50c2912c5ae2de598632dbe6fd2bc62794`

Exact proposition:

`SUBJECT_IS_PUBLIC_CLINIC_OR_HOSPITAL`

Proposition content hash:

`90c69c1d6f548214ae4c33f3aceac76e78b083d5b03218fcf4139f3922e3ea11`

Proposition ID:

`urn:rawlsing:gt34:obl048:exact-first-canary-subject-classification-proposition:sha256:90c69c1d6f548214ae4c33f3aceac76e78b083d5b03218fcf4139f3922e3ea11`

This is a candidate only. Independent hostile review and HQ adoption are still required.

## Exact current subject binding

Subject ref:

`urn:rawlsing:v3:subject:sha256:a0d7805874dc8449fa81770254a59accde050871aed13501902502e317273f33`

Subject-ref hash:

`a0d7805874dc8449fa81770254a59accde050871aed13501902502e317273f33`

W1 production materialization receipt:

`urn:rawlsing:v3:authenticated-subject-materialization-receipt:sha256:e8bb714f46a12dd1643e71a0e4a209ba3f7253be9d350d212b696146da11807f`

Receipt hash:

`e8bb714f46a12dd1643e71a0e4a209ba3f7253be9d350d212b696146da11807f`

## Exact semantic basis

The proposition is bound only to the already-authoritative exact OBL053 object/evidence chain:

- semantic object:
  `urn:rawlsing:gt34:generated-nonactor-subject-semantic-object:sha256:9a5fbe9a7c272cb2a60e425f09b206f0d25dd2d95caa07028bdb021130c32547`
- semantic-object hash:
  `9a5fbe9a7c272cb2a60e425f09b206f0d25dd2d95caa07028bdb021130c32547`
- semantic owner:
  `GT34_OBL053_ONE_OBJECT_NONACTOR_SUBJECT_ENTITY_SEMANTIC_AUTHORITY@1.0.0`
- semantic-owner hash:
  `867962094705ce13a33b0acfc81918b930dca6ae6d7c22e8094cc1d95bc41b29`
- objective-evidence receipt hash:
  `153ff1cd67e27b435cb6ffa4127047802eb06edcc6dab7072cedf9cb3ede7d6c`
- repaired Q1 requirement:
  `GT34_ADP010_Q69B_PUBLIC_CLINIC_SUBJECT_SEMANTIC_REQUIREMENT@1.1.0`
- Q1 requirement hash:
  `219fe6714efbcda30b6d9ea69cec6b99f3fe86a92c43ae7122a68e404f795fca`

Exact objective facts consumed:

```text
entity_family      = NONACTOR_FACILITY
facility_domain    = HEALTHCARE_DELIVERY
facility_form      = CLINIC
facility_function  = OUTPATIENT_HEALTHCARE_SERVICE_DELIVERY
ownership_status   = PUBLIC_SECTOR
```

At this exact one-subject grain, the positive rule requires a nonactor facility, healthcare-delivery domain, facility form CLINIC or HOSPITAL, public-sector ownership, and exact authentication of the current object/owner/evidence/materialization chain.

The current exact object satisfies that rule with `CLINIC + PUBLIC_SECTOR`.

No lexical label, Q69B wording, co-location, structural position, or category similarity is used.

## Minimality / authority ceiling

The candidate is intentionally not a runtime ontology or generic facility classifier.

It owns only:

`SUBJECT_IS_PUBLIC_CLINIC_OR_HOSPITAL`

for the one exact current subject ref above.

It does not assert or imply:

- actor contact;
- actor use;
- actor encounter;
- actor exposure;
- medicine/supplies problem;
- awareness/belief/memory/response;
- Q69B response/history;
- comparator result;
- PSEPF;
- metabolism;
- CAN-008;
- V2;
- positive-V3 actor mutation;
- classification of a second subject;
- a general facility ontology.

ADP-010 was not invoked or modified.

## Governed proof

Final governed execution:

- semantic candidate SHA:
  `01645806c98b8a83070389e5375e2b7fde781c6a`
- evidence execution / exact checkout:
  `3efb73af8bcba84f1b0fd1c77ebc2fd6c61aaa88`
- workflow:
  `Rabochii Governed Bounded Court`
- run:
  `34054644018`
- job:
  `101544191263`
- protocol self-test:
  `20 passed in 0.13s`
- W3 bounded proof:
  `15 passed in 0.67s`
- conclusion:
  `success`
- receipt artifact ID:
  `9995582801`
- receipt artifact digest:
  `sha256:185619abb0a8cd6dd578256227e2fa3a0d16042ec6cc455094146c08ae446f97`

The authority and proposition artifact blobs are identical at the frozen semantic candidate and the final evidence execution:

- authority blob:
  `a0be5530a3fab5a0b18746750ff461b0e7ff2d91`
- proposition blob:
  `c8c9ec0d708acfe864beede72c062b13b5aa0f58`

The candidate-to-evidence delta contains only:

1. transient governed court configuration; and
2. a proof-only validator shape assertion.

No semantic artifact changed.

## Preserved red evidence

The first authoritative court is preserved rather than erased:

- evidence execution:
  `08afac57be1d0944a18c3f744177432ccdc05557`
- run/job:
  `34054591749 / 101544028993`
- result:
  `1 failed, 14 passed`
- artifact ID:
  `9995567678`
- artifact digest:
  `sha256:94076de03c7880861b5c6c8f16976bf6facd602543a29dff174103f630d8eadc`

Exact failure class:

`TEST_FAILURE__HARNESS_ASSERTION_TYPE_DEFECT`

The lexical-label negative probe correctly failed closed but raised `KeyError` before the harness's expected `AssertionError`. W3 added one strict classification-basis shape assertion. No authority/proposition artifact changed.

## Proof matrix

Final court proves:

1. exact current chain yields the positive proposition;
2. authority/proposition hashes independently recompute;
3. subject-ref mutation fails;
4. materialization-receipt mutation fails;
5. semantic object/owner/evidence mutation fails;
6. non-CLINIC/HOSPITAL form fails;
7. non-public ownership fails;
8. lexical clinic/hospital labels without objective evidence fail;
9. second subject fails;
10. contact/use/encounter fields are absent and rejected from proposition shape;
11. exact Q1 requirement hash is bound;
12. replay is exact/idempotent;
13. no broader authority is emitted.

## Persisted artifacts

Authority candidate:

`data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/GT3_GT4_POST_W1_W2_PARALLEL_AUTHORITY_AUDIT_WAVE_R1/W3_OBL048_EXACT_SUBJECT_CLASSIFICATION_AUTHORITY_R1/01_EXACT_SUBJECT_CLASSIFICATION_AUTHORITY_CANDIDATE.json`

Proposition candidate:

`data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/GT3_GT4_POST_W1_W2_PARALLEL_AUTHORITY_AUDIT_WAVE_R1/W3_OBL048_EXACT_SUBJECT_CLASSIFICATION_AUTHORITY_R1/02_EXACT_SUBJECT_CLASSIFICATION_PROPOSITION_CANDIDATE.json`

Machine-readable governed evidence:

`data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/GT3_GT4_POST_W1_W2_PARALLEL_AUTHORITY_AUDIT_WAVE_R1/W3_OBL048_EXACT_SUBJECT_CLASSIFICATION_AUTHORITY_R1/03_GOVERNED_CLASSIFICATION_EVIDENCE.json`

Focused proof:

`rawlsing_next/tests/test_gt34_w3_obl048_exact_subject_classification.py`

## Closure ceiling

W3 has reached its frozen terminal.

The next lawful project action is an **independent OBL048 hostile review** of this exact candidate. W3 does not perform that review and does not self-adopt.

## Final

`PASS__GT34_W3_OBL048_EXACT_SUBJECT_CLASSIFICATION_AUTHORITY_CANDIDATE_GREEN__NO_ADOPTION`
