# OBL059 R3 — INDEPENDENT BOUNDED REVIEW EVIDENCE R1

## Reviewer identity

Role: `RABOCHII_INDEPENDENT_REVIEWER_OBL059_R3_R1`

Review branch:
`agent/rabochii-subv-e-obl059-positive-applicability-r3-independent-review-r1`

Exact commission start:
`2eedd4456f7dfa61d266eb3efe938d406b96c9fd`

The reviewer is distinct from the R3 repair worker. No candidate repair was performed.

## Frozen target and governance

Frozen R3 candidate:
`4fdb897e8a089787d7407197fd49bbd1ef51f2ef`

Bound producer evidence execution:
`860078598cd1376c368177c51b183f651b9c8f45`

Known green producer run:
`34197429485`

Prospective campaign instruction/adjudication:
`c7f221d3c07453eebae36e448a52b2e7789ae13c`

Supplied adjudication tree:
`1fdf0ccf143942bf4b009c15cabfe2f5c41871e9`

Prior failure history consumed:

- R1 failed because malformed non-JSON required bindings reached unconditional receipt JSON hashing and escaped `TypeError`.
- R2 failed because its fallback recognized only one JSON error shape; mappings with `bytes` keys and circular lists still escaped.

## Independent matrix freeze

Matrix document:
`03_INDEPENDENT_REVIEW_MATRIX_R1.md`

Independent executable review:
`test_independent_review_r1.py`

Governed wrapper:
`rawlsing_next/tests/test_subv_e_obl059_positive_applicability_r3_independent_review_r1.py`

Frozen review/evidence execution SHA:
`8ab1409e9b94ca1a4fe7a762264eae2cf57e5efa`

Matrix blob SHA:
`51193379b880c7ff0e705fcf67693bf94954a490`

Court-spec blob SHA:
`56b0cf56f60acd27a54c3c18eb6f4948e621b917`

Court-spec SHA-256 recorded by governed receipt:
`c213aedf284b46233dffccbef2443dd0480a0b9d4238c31977eb4e74e70e4378`

The matrix was committed and frozen before governed execution. It is independently authored and is not the producer's 44-test court.

## Governed execution

Workflow: `Rabochii Governed Bounded Court`

Execution-only PR: `#286`

PR state after evidence capture: `CLOSED_UNMERGED`

Governed run:
`34199787501`

Job:
`101975718120`

Evidence execution SHA:
`8ab1409e9b94ca1a4fe7a762264eae2cf57e5efa`

PR synthetic merge SHA recorded by receipt:
`d8d3c42962c47850a599252b38c4d270a61b664b`

Artifact:
`10045333849`

Artifact name:
`rabochii-court-receipt-34199787501`

Artifact ZIP SHA-256, independently verified after download:
`a2ad8fbbd3a89c467104e70de5c3d9e0fac0752ca116cea48af96acc833fe3c0`

Governed receipt material:

```json
{
  "determinism_mode": "EXACT",
  "evidence_execution_sha": "8ab1409e9b94ca1a4fe7a762264eae2cf57e5efa",
  "exit_code": 1,
  "implementation": "CPython",
  "pr_synthetic_merge_sha": "d8d3c42962c47850a599252b38c4d270a61b664b",
  "python": "3.12.14",
  "result": "FAIL",
  "schema_id": "RABOCHII_BOUNDED_COURT_RECEIPT@1.0.0",
  "semantic_candidate_sha": "4fdb897e8a089787d7407197fd49bbd1ef51f2ef",
  "spec_sha256": "c213aedf284b46233dffccbef2443dd0480a0b9d4238c31977eb4e74e70e4378",
  "tests": [
    "rawlsing_next/tests/test_subv_e_obl059_positive_applicability_r3_independent_review_r1.py"
  ]
}
```

The protocol self-test and bounded-court spec validation both succeeded. The `Execute bounded court` step failed. Receipt upload succeeded.

## Smallest exact blocker

`BLOCKER__OBL059_R3_HOSTILE_MAPPING_PROJECTION_EXCEPTION_ESCAPES`

The current adjudication expressly requires objects with throwing mapping/iteration behavior when reachable by diagnostic projection and requires no uncaught projection exception after a required binding is already semantically malformed.

The frozen R3 code does not close that case. After `_diagnostic_safe` observes that a malformed required-binding `Mapping` is not directly JSON serializable, it delegates to `_project_json_safe`. The Mapping projection directly traverses `value.items()` without an exception boundary. The independent matrix supplies a copyable semantically malformed `Mapping` whose `items()` raises `TypeError("commissioned-hostile-mapping-items")`. That exception escapes the candidate's safe-receipt construction rather than producing a deterministic JSON-safe `NOT_DIRECTLY_APPLICABLE` receipt.

This is inside the commissioned malformed/non-JSON negative-receipt boundary; it is not the deliberate unrelated-programmer-error control. Therefore the governed FAIL is terminal under the decision law.

No broader repair claim is necessary to establish the failure.

## No-current-effect / no-repair attestation

`CANDIDATE_REPAIRED_BY_REVIEWER = NO`

`SECOND_REVIEWER_COMMISSIONED = NO`

`HQ_ADOPTION_CLAIMED = NO`

`PROJECT_CURRENT_POSITIVE_APPLICABILITY_CREATED = NO`

`PROJECT_CURRENT_OBL056_POSITIVE_ENTRY_INSTALLED = NO`

`OBL055_EXECUTED = NO`

`PROJECT_CURRENT_OEE_REALIZED = NO`

`ACTOR_CREATED_OR_ACTIVATED = NO`

`ADP008_PHASE_TRANSITION_EXECUTED = NO`

`ADP019_OCCURRENCE_ADMITTED = NO`

`CAUSAL_USE_PERMISSION_OWNED = NO`

`CONTACT_WITNESS_INDEPENDENCE_OWNED = NO`

`ENCOUNTER_CREATED = NO`

`AUTHORITY_INDEX_MUTATED = NO`
