# Rank-1 Native V550 Cloud Gate Diagnostic

## Conclusion

The zero-row native V550 surfaces are caused by a semantic/contract eligibility gate, not by a missing respondent intersection and not by a missing response-map join.

The exact LiTS II / SE prepared substrate contains 900 respondents for each requested variable and 838 respondents with both governed non-missing values. The V550 output nevertheless contains only zero-row schemas for `branch_relation_co_signature`, `branch_co_signature`, and `question_response_attitude_cloud`.

The QUC rows entering the builder have all native empirical-use flags disabled. The builder therefore has no lawful anchor or feature from which to construct a cloud or co-signature.

## Exact observed state

Source artifact:

`/tmp/successor_run/lits_ii_retry_result_1_min/v550/shard_runs/lits_ii_successor_retry_rank1_min/LiTS_II_SE/core/question_use_contract.parquet`

| Variable | Semantic role | Directionality status | Current directional atom eligible | Relation co-signature | Cloud anchor | Cloud feature | Eligibility status |
|---|---|---:|---:|---:|---:|---:|---|
| `q305_1` | `STRUCTURAL_CONTEXT` | `NOT_APPLICABLE` | `false` | `false` | `false` | `false` | `PENDING` / `NOT_CERTIFIED` |
| `q306c` | `RELATION_EVIDENCE` | `CERTIFIED` | `false` | `false` | `false` | `false` | `PENDING` / `NOT_CERTIFIED` |

The two rows were response-map matched in the audit surface: `q305_1` has 9 effective rows (8 substantive, 1 special), and `q306c` has 3 effective rows (2 substantive, 1 special). The absence is therefore not caused by the response-option map failing to resolve values.

## Builder gate

The native V550 implementation consumes QUC authority fields and gates the lawful surfaces through:

- `allowed_as_branch_relation_cosignature`;
- `allowed_as_attitude_cloud_anchor`;
- `allowed_as_attitude_cloud_feature`.

The QUC construction clears those native empirical-use flags when `current_directional_atom_eligible` is false or the directionality/semantic contract is incomplete. This is why healthy respondent co-travel does not become empirical relation evidence automatically.

## Supporting audit evidence

`bridge/response_semantics_audit.csv` contains 748 diagnostic rows classified as `derived_determinicity`, not direct relation evidence. Their failed gates include `derived_determinicity_not_direct_relation_evidence`, `non_substantive_or_missing_response`, `review_required_not_relation_evidence`, and `numeric_only_label_requires_numeric_scale_family`.

`bridge/direct_relation_response_eligibility_audit.csv` is empty: no row passed the direct relation-response eligibility boundary.

`bridge/bridge_exclusion_reason_by_lane.csv` reports 748 derived-determinicity rows excluded as not direct relation evidence, 60 position-context rows excluded as non-substantive or missing response, and 9 position-context rows excluded as review-required rather than relation evidence.

`audit/cloud_exclusion_audit.parquet` is empty because no candidate reached the cloud constructor. This is an upstream eligibility absence, not a downstream cloud-computation failure.

## Root classification

```text
ROOT: QUC authority eligibility / contract completeness gate
NOT: respondent substrate absence
NOT: same-respondent join failure
NOT: response-option map absence
NOT: V550J registry failure
NOT: downstream V551/V552 behavior
```

For `q305_1`, the behavior is expected under current authority: it is explicitly structural context/ranked-choice topology and must not be treated as directional relation evidence.

For `q306c`, the current installed QUC is conservative: its source-level directionality surface says `CERTIFIED`, but the QUC still records response-semantics authority review required, structural mapping pending, low semantic confidence, and `current_directional_atom_eligible = false`. The builder correctly honors the QUC result rather than the looser upstream overlay row.

## What would be required to proceed

This is not safely fixed by enabling cloud flags or changing the respondent join. Governing authority would need to resolve the `q306c` QUC contract conflict: complete or confirm response-semantics authority, complete structural mapping, establish a current directional eligibility decision with provenance, regenerate the QUC, and rerun the bounded V550 scope.

`q305_1` should remain structural context unless a separate authoritative decision changes its role. It should not be promoted merely to create the rank-1 pair.

No semantic decision was made by this diagnostic.
