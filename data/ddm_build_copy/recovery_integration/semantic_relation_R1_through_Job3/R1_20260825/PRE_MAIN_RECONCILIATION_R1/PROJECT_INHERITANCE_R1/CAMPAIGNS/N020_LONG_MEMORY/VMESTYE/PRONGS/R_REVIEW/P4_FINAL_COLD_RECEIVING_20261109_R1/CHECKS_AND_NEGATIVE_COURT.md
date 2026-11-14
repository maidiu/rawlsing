# ZL-P4R read-only checks and falsifier court

At candidate `d10602355c77564b2b6d50601ebba4fed4ac7d58`, the independent receiver fetched exact Git blobs through the authenticated GitHub connector and parsed TSVs in memory as literal tab-separated records. All checks are S0–S1; no project runner, CI, original respondent input, S2, S3 or native actor was executed. No installed code was modified.

| Table or sidecar | Rows | Width violations | Duplicate primary keys |
| --- | ---: | ---: | ---: |
| FUNCTION_ATLAS | 1,740 | 0 | 0 |
| RELATIONS | 8,503 | 0 | 0 |
| EVIDENCE | 2,720 | 0 | 0 |
| OPERATION_TRACES | 332 | 0 | 0 |
| CONSUMER_EDGES | 332 | 0 | 0 |
| AUTHORITY_APPLICATIONS | 370 | 0 | 0 |
| IMPLEMENTATIONS | 884 | 0 | 0 |
| DECISION_EVENTS | 884 | 0 | 0 |
| P0_LEFT_DISPOSITIONS | 6,125 | 0 | 0 |
| FULL_ID_ANTI_JOINS | 2,607 | 0 | 0 |
| CONFLICTS_AND_REPAIR_ORDER | 1,536 | 0 | 0 |
| SEAM_DEPENDENCIES | 82 | 0 | 0 |

Additional independent literal invariant checks: 332/332 operation producer-edge joins; 332/332 edge producer-operation joins; 332/332 current first-reader IDs unresolved; all 370 authority statuses lack `rule_applied_to_output=YES` and `negative_or_refusal_enforced=YES`; 883/884 implementations explicitly have `NOT_PROVED_CODE_SYMBOL`, one N10E protected code symbol; 82/82 seam predicates nonblank and original requiredness distribution 7/26/12/2/35; 2,607 source coverage rows split 1,962 exact P0 and 645 outside P0; 1,869 distinct matched P0 and 627 distinct non-P0; 6,125/6,125 P0 left dispositions nonempty with zero same-grain current proof; 1,536/1,536 conflict PKs unique; all 884 reciprocal status cells `NOT_REQUESTED_NOT_RECEIVED`. The 8,503 relations have 7,736 resolvable EVIDENCE IDs and 767 explicit sentinels (677 `UNRESOLVED`, 90 `UNRESOLVED_EVIDENCE`). These sentinels are not mistaken for affirmative source evidence.

### Independent schema failure

Protected `07_ATLAS_AND_RELATION_SCHEMA.md` permits 23 exact relation types and demands schema revision/migration for new kinds. Candidate `RELATIONS.tsv` has 4,841 rows in 11 additional kinds. By kind:

| Non-enumerated candidate relation type | Rows |
| --- | ---: |
| `CROSS_GENERATION_TYPED_UNJOIN` | 4,102 |
| `CANDIDATE_PRODUCER_EDGE__NOT_EXECUTION` | 332 |
| `SELF_STAGE_SOURCE_RETURN__NOT_SUCCESSION` | 318 |
| `DOCUMENTED_DEPENDENCY__ASTRA` | 33 |
| `DOCUMENTED_DEPENDENCY__FUNCTIONAL` | 14 |
| `DOCUMENTED_DEPENDENCY__OBSERVED` | 35 |
| `CANDIDATE_REQUIRED_FOR_SOROK_E001__OWNER_HELD` | 2 |
| `CROSS_PRONG_CANDIDATE_UNJOIN__NOT_SUCCESSION` | 2 |
| `CANDIDATE_IMPLEMENTATION_LABEL__SOURCE_STATIC` | 1 |
| `STATIC_CALL_AT_SHA__NO_EXECUTION` | 1 |
| `HISTORICAL_E001_IDENTITY_TO_SOROK_RECIPIENT_CANDIDATE__OWNER_HELD` | 1 |

These types are semantically helpful but not yet admitted under the canonical version. The P4 repair must **conserve** each old relation ID, source predicate, evidence, negative and held distinction, including the one historically versioned E001 bridge; no invalid types may enter protected as unreviewed schema extension.

### Ten bounded deliberate assertion violations

The reviewer created one altered in-memory record or list for each case and checked that the corresponding independently specified invariant reports failure. All **10/10** violations were detected by these local assertions. These are simple invariant probes, not a reproducible repository-wide mutation framework or native tests.

| Probe | Mutation | Expected refusal |
| --- | --- | --- |
| P4-N01 | Insert fake actual `consumer_operation_id` | No actual non-test consumer receipt |
| P4-N02 | Set source-held authority `rule_applied_to_output=YES` | No affirmative applied-rule witness |
| P4-N03 | Set source-held `negative_or_refusal_enforced=YES` | No affirmative current enforced refusal |
| P4-N04 | Erase literal IF predicate | Exact source predicate no-drop |
| P4-N05 | Promote an IF condition to MUST | Original source requiredness invariant |
| P4-N06 | Relabel R4 E001 identity bridge as `NATIVE_EXECUTED` | Explicit nonnative evidence ceiling |
| P4-N07 | Inject invented code symbol into unverified implementation | Typed `NOT_PROVED_CODE_SYMBOL` invariant |
| P4-N08 | Blank P0 left disposition | 6,125/6,125 explicit source fates |
| P4-N09 | Remove one conflict row | 1,536 source-negative/hold no-drop |
| P4-N10 | Assert a protected Pyat reciprocal adoption in candidate event | 884 owner-receiving cells still pending |

**Important:** this court found *new* admission deficits (relation-type migration; 73 inherited seed fates) even though the two specialized P3 reviews were correct at their narrower S0–S1 seams. That is a change of question, not a repudiation of their valid reviewed source-grain receipts. It has not established all semantic claims or all branch contents.
