# G1A-FUNC-012 — conditional producer present; file loader present; structural value reader absent

Historical exact cut `25830fe7462bb9e29bc4087e6ae14f3f84cec377`: producer `ddm_v551_conditional.py` blob `359665297677553a33556ce65c2e3d76b60b2cc1`; compiler `compile_v552_structural_ddm.py` blob `0f9a28749ed5858a4814ec8e8fa6b53000f343de`; structural builder blob `0df56d70cb3880dee723df00aea2207acd525260`. Modern I03 `pre553_empirical_query.py` blob `b72b469e6646b88e4e2ed4dbbf0f3c209557fd69` at `6a5c12f04323d74001f9632063ec907f4fc4468e`. Original identity retained; no new T. Evidence R3:EV:012:*.

## Historical input → transformations → output

**Input:** V551 bridge row keyed by `source,wave,canonical_wave,country_code,question_id,var_code,source_row_hash` and carrying `bridge_evidence_lane`, `v551_conditional_determinicity_eligible`, `question_use_contract_joined`, `source_structure_fields_joined`, `support_status`, `n_unweighted`, `response_direction`, `response_intensity`. Source L95–155/L157–235.

**Predicates and algorithm:** source-table priority and keys sort rows; wrong `bridge_evidence_lane` (must be `derived_determinicity`), missing eligibility, missing question-use join, missing source-structure join, insufficient support and duplicate exact conditional key each produce an exclusion row with `gate_name,exclusion_reason,sample_source_row_hash`. Eligible rows get hash-based `conditional_id`, support and directionality statuses, response fields and `compiler_status` (populated or insufficient_directionality). Two distinct typed outputs: conditional index and V551 atom exclusion audit. R3:EV:012:OLD_OUT/:OLD_GATES.

## Illustration (source-branch only; NOT executed)

For a row `source="A",wave="W",question_id="q",var_code="v",bridge_evidence_lane="derived_determinicity",v551_conditional_determinicity_eligible=True,question_use_contract_joined=True,source_structure_fields_joined=True,support_status="sufficient_support",source_row_hash="h"`, with remaining expected fields present, the old code adds a conditional index row. Change only `question_use_contract_joined=False` -> exclusion `question_use_contract_not_joined`; repeat the same source/wave/question/row-hash -> duplicate audit. This code-level example does not make the data source-native.

## Precise first reader: split invocation from meaning

`compile_v552_run` L299–309 accepts an optional parquet, requires canonical path, reads DataFrame and passes it to `build_v552_structural_outputs`. Thus **there is a real loader/argument edge and a possible file-open/validation failure**. But `build_v552_structural_outputs` L253–259 builds pressure from *V551 atoms + coverage/adjudication*, never reads `conditional_determinicity`, and creates `conditional_determinicity_status_audit` as an empty schema. Therefore the old conditional **value** has no proven V552 structural effect even when successfully loaded. See R3:EV:012:LOAD/:NO_READ. The Trii D11 report is an *auditor of this absence*, not the first scientific consumer of conditional values.

## Modern and intermediate comparison

Modern I03 receives an exact C11 release, governed query and predicate and emits an `EmpiricalFact` or typed negative. It is a different denominator, source/authority contract and output, not the same as a V551 derived-determinicity auxiliary index or proof of V552 causal use. Trii D11 §5.1, §6 and §8 also nominates other apparently stranded functions (unary position conditional, V548/V549 branch/cotravel, V550 clouds, V550J respondent membership); those belong in omission countersearch with source-specific inherited IDs, not folded into this case or pronounced globally absent.

## Disposition

Producer: located. Loader: located. Material V552 conditional reader/effect: not proved; code actually ignores value. Current analogue: partial/different. Scientific/authority succession: unknown. Smallest next *read-only* research: cross-repo source search for any other semantic consumer of `conditional_determinicity_index`, then trace exact denominator and actual first reader; do not engineer a substitute. See R3:GAP:012:*.
