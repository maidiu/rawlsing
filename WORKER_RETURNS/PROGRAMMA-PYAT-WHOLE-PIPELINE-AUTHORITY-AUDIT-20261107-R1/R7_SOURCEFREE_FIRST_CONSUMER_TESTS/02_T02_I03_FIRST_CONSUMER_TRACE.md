# T02 - I03 TARGET-PLAN AUTHORITY FITNESS

## Fixture
- Synthetic TEST_ONLY sourcefree I03 fixture from `test_pre553_empirical_query._build_source("r7-t02", ...)`.
- Two respondents, both `Y=0`; one exact risk set; exact query grammar; baseline target topology/response authority is the positive `SOURCE_SEMANTICS_TOPOLOGY` snapshot.
- Baseline actual consumer: `_parse_target_plan` plus `execute_empirical_query`.
- Baseline fact: `SUPPORTED 2/2`, ref `urn:rawlsing:pre553:EmpiricalFact:sha256:9ddfed96d1f4bf4f8d448c0ffcbbf4fde28ac7eedec4b92b656a9d8f458cbcac`.

## Mutation
Only the target component `topology_authority_refs` and `response_semantic_authority_refs` were replaced with one bad snapshot. All event authority refs remained the legitimate positive source authority. All other grant and ref material was preserved.

## Results
| Mutation | `_parse_target_plan` | Actual downstream consumer |
|---|---|---|
| baseline | accepted | `SUPPORTED 2/2` |
| (a) `DENY` | refused: `Pre553AuthorityError` | `UNAVAILABLE 0/0` |
| (b) `ALLOW` wrong kind | accepted locally | `UNAVAILABLE 0/0` |
| (c) `ALLOW` wrong operation | accepted locally | `UNAVAILABLE 0/0` |
| (d) `ALLOW` wrong source scope | accepted locally | `UNAVAILABLE 0/0` |
| cold restore | accepted | `SUPPORTED 2/2`, baseline ref matched |

## Finding
`_pre553_query_common.py:351-355` checks only `typed_state == "ALLOW"`. Wrong-kind, wrong-operation, and wrong-scope `ALLOW` snapshots therefore pass the local target plan. That local gap is not independently sufficient: `_pre553_query_eval.py:184-190` requires the target authority ref to bind the matched C11 response event, and the target-only mutation does not put the bad ref into event authority closure. The actual consumer returns `UNAVAILABLE 0/0`, not governed positive output.

## Cross-test interaction
T02 is not a standalone bypass. It becomes reachable only after T01 has admitted the same bad authority into the event authority closure. In that T01 counterexample, the event binding check is satisfied by the already-admitted bad ref and the target plan's ALLOW-only check accepts it; the result is `SUPPORTED 2/2`.

## Verdict
`T02_NO_PATCH_ALONE`. Do not patch T02 alone as if it were an independently proven bypass. The C11 owner fix from T01 closes the demonstrated composition. A defense-in-depth I03 positive-fitness check remains reasonable and is proposed in `06_MINIMUM_OWNER_PATCH_ONLY_IF_REAL_BUG.md`.

No production edit was made in this commission.
