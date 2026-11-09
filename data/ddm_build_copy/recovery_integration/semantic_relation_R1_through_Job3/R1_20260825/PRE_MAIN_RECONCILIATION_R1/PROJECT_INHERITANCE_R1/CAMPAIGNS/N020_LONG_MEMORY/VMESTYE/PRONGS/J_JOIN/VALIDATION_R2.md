# VMESTYE ZL-15 — candidate graph integrity and negative-proof receipt

**Court:** authenticated GitHub code/data retrieval and in-memory deterministic JavaScript TSV parsing. **Not** the Python project S2 validator, source-native S3, original35 data execution, scientific issuers or independent hostile reviewing.

## S0–S1 checks actually executed

| Machine artifact | Rows | Key-width failures | Duplicate primary IDs |
| --- | ---: | ---: | ---: |
| DATA/FUNCTION_ATLAS.tsv | 1,740 | 0 | 0 |
| DATA/RELATIONS.tsv | 3,662 | 0 | 0 |
| DATA/OPERATION_TRACES.tsv | 332 | 0 | 0 |
| DATA/AUTHORITY_APPLICATIONS.tsv | 370 | 0 | 0 |
| DATA/EVIDENCE.tsv | 2,718 | 0 | 0 |
| DATA/IMPLEMENTATIONS.tsv | 884 | 0 | 0 |
| DATA/CONSUMER_EDGES.tsv | 332 | 0 | 0 |
| DATA/DECISION_EVENTS.tsv | 884 | 0 | 0 |
| J_JOIN/FULL_ID_ANTI_JOINS.tsv | 2,607 | 0 | 0 |
| J_JOIN/CONFLICTS_AND_REPAIR_ORDER.tsv | 1,536 | 0 | 0 |
| J_JOIN/P0_EXACT_JOIN_AUDIT.tsv | 2,607 | 0 | 0 |
| J_JOIN/SOURCE_PROOF_RECEIPTS.tsv | 13 | 0 | 0 |
| J_JOIN/HISTORICAL_AUTHORITY_58_INDEX.tsv | 58 | 0 | 0 |

**Prong-level conservation checks:** all 13 R5-accepted heads accounted (ZL02–ZL14); 884 `FINDINGS`, 332 `OPERATION_TRACES`, 370 `AUTHORITY_USE`, 2,718 `EVIDENCE`, 2,607 `COVERAGE`, 1,536 `UNJOINS` from exact receipt table; row width validated, no cross-prong local-ID collision. Source `(prong, local)` identifiers were explicitly namespaced in R2 because R1 collapsed distinct `F01`-type keys.

**Original P0 bytes:** 6,125 unique five-tuples at `CONTROL/P0_RETURN_AND_BRANCH_CENSUS.tsv` blob `65c1bbe4a602341c5caacca2d58dced31a23f382`. Recomputed exact tuple match of **every** 2,607 coverage row. 1,962 observations / 1,869 distinct exact P0; 645 observations / 627 distinct outside P0; 88 P0 identities recur across prongs (93 repeated observations); zero P0 ambiguity and zero mismatched census IDs. Full per-row receipt: `P0_EXACT_JOIN_AUDIT.tsv`.

**Graph relational checks:** 332 producer edges reference present candidate operation IDs; all 332 operative `function_ids` reference existing atlas IDs; all 370 authority rows reference atlas IDs; all 884 implementation rows and 884 decision events reference atlas IDs. All decision events remain S0–S1 candidate admissions. 3,662 unique edges comprise `ASSIGNED_TO 1312`, `REQUIRES_AUTHORITY 452`, `HELD_BY 1868`, `ALIAS_OF 30`. No fabricated `APPLIES_RULE`, `PRODUCES` or `CONSUMED_BY` edge. 44 LMX / 30 LMQ / 29 F29 / 58 AR indexed at their **different** record grains.

**Negative checks:** all 332 candidate actual-consumer cells = `NOT_PROVED_NON_TEST`; all 332 actual-call-site cells = `NOT_PROVED`; all 332 consumer statuses = `OPEN_PROOF_GAP`. All 370 authority grades are `R5_DOCUMENTARY_ONLY__...`; 10 `rule_selected_for_scope=YES` are documentary **selection reports**, not effect. Zero `rule_applied_to_output=YES` and zero `negative_or_refusal_enforced=YES`. No original/native S3 or qualified project-runner S2 was performed.

## Known limits (not passes)

These validations establish internal **documentary** consistency and exact ID conservation, not acceptance of every source interpretation. Particularly unresolved: actual first readers and source-native/issuer rights; D05-F06/F11; FIABC 144 reported PASS / 3 FAIL; 49 ZL12 GAP different-commit aliases; original J losses; sourcefree-vs-protected status of stranded branches; S01–S11 IF edges; actual Sorok and N10 downstream read. The original 6,125 P0 row corpus is preserved without expansion by the 627 outside-P0 identities.

**Status:** `VALIDATED_S0_S1_IN_MEMORY__INDEPENDENT_#815_#816_REQUIRED`. No project CI tests, S2, S3, source owner, reviewer, or protected merge claimed. Exact candidate SHA is resolved from the PR and issue return receipt rather than self-embedded.
