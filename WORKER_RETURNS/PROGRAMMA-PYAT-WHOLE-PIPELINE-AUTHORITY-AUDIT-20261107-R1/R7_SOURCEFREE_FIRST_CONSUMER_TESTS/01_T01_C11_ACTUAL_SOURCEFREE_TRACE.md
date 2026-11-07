# T01 - C11 NONCANONICAL QUESTION AUTHORITY FITNESS

## Fixture
- Synthetic TEST_ONLY sourcefree C11 fixture from `test_pre553_source_backed_c11_facade._fixture("r7-t01")`.
- Target `Y` is substantive for all three synthetic respondents; its risk set has two exact members. Baseline query therefore resolves `2/2`.
- Baseline authority is the fixture's positive `SOURCE_SEMANTICS_TOPOLOGY` snapshot used by every `QuestionVariableBinding.semantic_authority_ref` and `topology_authority_ref`, and by each `ResponseSlotRule.question_binding`.
- Baseline actual consumer: `execute_source_backed_empirical_query`, which builds `validate_c11_source_release` output and executes `execute_empirical_query`.
- Baseline fact: `SUPPORTED`, numerator `2`, denominator `2`, ref `urn:rawlsing:pre553:EmpiricalFact:sha256:00cc5e59bbe4ee5eb89729aa0713f5a72fe3bbd8656b75f1ea28166a752f100b`.

## Mutation
Only the question semantic/topology refs and their mirrored response-slot question bindings were replaced with one synthetic authority snapshot. The bad snapshot was added to projection authority snapshots and required refs. The surrounding release, manifest, respondents, replay, namespace, risk set, and query grammar stayed intact.

For each ALLOW variant, the query target refs were then generated from the accepted bad question authority refs, as a real consumer targeting that binding would do. A separate positive-target control kept the original positive target authority refs.

## Results
| Mutation | C11 release | First consumer with bad refs | Positive-target control |
|---|---|---|---|
| baseline | accepted | `SUPPORTED 2/2` | `SUPPORTED 2/2` |
| (a) `DENY` same kind/family | accepted | `UNAVAILABLE 0/0` | `UNAVAILABLE 0/0` |
| (b) `ALLOW` wrong kind `ROUTING_RISK_SET` | accepted | `SUPPORTED 2/2` | `UNAVAILABLE 0/0` |
| (c) `ALLOW` same kind, wrong operation | accepted | `SUPPORTED 2/2` | `UNAVAILABLE 0/0` |
| (d) `ALLOW` same kind, wrong source universe scope | accepted | `SUPPORTED 2/2` | `UNAVAILABLE 0/0` |
| cold restore | accepted | `SUPPORTED 2/2` | `SUPPORTED 2/2` |

Exact bad-ref fact refs:
- (b) wrong kind: `urn:rawlsing:pre553:EmpiricalFact:sha256:e931f6a38467e406fe562f64417ea613f0721ec50573e352bb0e1f82eb137327`
- (c) wrong operation: `urn:rawlsing:pre553:EmpiricalFact:sha256:e072a0d52a00528258361c7ddd5e31664ce2b8185a2990ec13ff1fa2dd492837`
- (d) wrong scope: `urn:rawlsing:pre553:EmpiricalFact:sha256:f5438214b46dab8fb323338071932254c303606c15f26c21ca15bece33e8e551`
- cold restore matched the baseline ref: `true`.

## Finding
`pre553_c11_ingest.py:644-659` resolves every noncanonical question semantic/topology ref but applies `require_positive_authority` only to a canonical mapping ref. Consequently a noncanonical `QuestionVariableBinding` can carry a positive-but-wrong-kind, wrong-operation, or wrong-scope authority into the C11 release and into respondent-event authority closure.

The first actual consumer then emits a governed positive fact when the query target uses those same accepted refs. The downstream event check only tests ref presence at `_pre553_query_eval.py:184-190`; it does not re-check kind, operation, or source scope. The positive-target control confirms the event guard is not bypassed by the question mutation alone: it refuses when events carry only the bad ref while the target names the positive source authority.

This is a real first-consumer authority-fitness defect in the synthetic sourcefree path. It is not a claim that historical native R5 data was affected.

## Minimum repair
Primary owner: C11 ingest (`pre553_c11_ingest.py`, `_validate_question_authorities`). Apply exact positive fitness to each noncanonical question semantic/topology snapshot, including kind, public object family, and exact source-universe scope. The I03 target plan should add the same positive fitness as defense in depth. Exact proposed repair and test additions are in `06_MINIMUM_OWNER_PATCH_ONLY_IF_REAL_BUG.md`.

No production edit was made in this commission.
