# 00_RETURN — J02

Status: **PASS**

Branch: `agent/rabochii-prev3-w8-j02-source-state-target-disposition-r1`

Commission tip: `decaa46fe285ad22b6e8f9d1c54eb98be21cf02a`

Grain executed: `PREV3_EMPIRICAL_SOURCE_STATE_TO_PRODUCT_TARGET_DISPOSITION_CONTRACT_R1_ONLY`

## Governed return

J02 freezes the reusable objective-world contract:

`RAW_SOURCE_STATE -> SOURCE_LOCAL_GOVERNED_STATE -> PRODUCT_TARGET_DISPOSITION -> DENOMINATOR_RESOLUTION_CHECK -> EMPIRICAL_RESULT`

The universal layer never interprets a raw numeric/string token. It consumes exact content-addressed source-local semantic authority (`SOURCE_SEMANTICS_TOPOLOGY`), exact product/target-domain authority (`TARGET_USE_PERMISSION`), exact pre-query denominator/risk-set authority (`ROUTING_RISK_SET`), and exact replay authority (`REPLAY_PROTOCOL`).

The minimum lawful source-local classes are `SOURCE_SUBSTANTIVE`, `TYPED_MISSING_NONRESPONSE`, `SOURCE_NOT_APPLICABLE_OR_INELIGIBLE`, `SOURCE_SPECIFIC_SPECIAL`, and `SOURCE_UNKNOWN`. These are authority outcomes only; they are not universal meanings of native codes.

The minimum product dispositions are `TARGET_MEMBER`, `RESOLVED_NON_TARGET`, `TYPED_MISSING_NONRESPONSE`, `NOT_APPLICABLE_OR_INELIGIBLE`, `AUTHORIZED_PREQUERY_EXCLUSION`, and `UNRESOLVED`.

For a denominator member, only `TARGET_MEMBER` and `RESOLVED_NON_TARGET` count as resolved. Therefore a substantive state outside the requested target can be resolved only when exact target-domain authority supplies the resolved-complement binding. Typed missing/nonresponse and not-applicable/ineligible response states do not self-delete the denominator and do not become resolved merely by being typed. `SOURCE_SPECIFIC_SPECIAL` and `SOURCE_UNKNOWN` fail closed to `UNRESOLVED` in this universal layer.

Denominator membership is independent of target membership. The only denominator-removal path is an exact `PREQUERY_EXCLUDED` decision under the frozen `ROUTING_RISK_SET` authority, exact risk-set ref, exact eligibility basis ref, and `PRE_QUERY` phase. A target disposition cannot retroactively exclude a denominator member. The frozen `expected_record_ids` set must be accounted for exactly once, preventing post-outcome deletion by omission.

`EMPIRICAL_RESULT` is emitted only when `raw_resolved_target_support == raw_denominator_support` and the unresolved-member set is empty. Source-state bindings, target-disposition bindings, the query envelope, denominator ledger, gate, and result are SHA-256 replay identified over canonical material.

## Accepted-law anchors used

- `rawlsing_next/_pre553_query_eval.py` — blob `e2d91984541df7c692a1b2f32370500838a2a000`
- `rawlsing_next/_pre553_query_common.py` — blob `6b38b0b749961358b65b31871a8cd5ca4a98fe77`
- `rawlsing_next/pre553_empirical_objects.py` — blob `a61365b994e5c3c50de0f598fcf40e90abf757b6`
- `rawlsing_next/pre553_empirical_authority.py` — blob `c824bcf17257c0318e86497fc12ee31101bb6daf`

These anchors supply the accepted PRE553 separation of routing/risk-set authority from response semantics, exact authority identity law, fail-closed resolution behavior, and deterministic semantic identity law. J02 does not add source-specific meaning to them.

## Exact return artifacts

- `tools/prev3_source_state_target_disposition.py` — blob `062b0c56d754cacfbd2464a733af001e7661f5b2`
- `evidence/fixtures/prev3_source_state_target_disposition_fixture.json` — blob `e438cf7df36017504712a57bc4e33943ef8e03e1`
- `evidence/selftest/prev3_source_state_target_disposition_contract.py` — blob `39b69dd644723a3d20ff1a10b014d686efe79062`
- `evidence/receipts/PREV3_EMPIRICAL_SOURCE_STATE_TO_PRODUCT_TARGET_DISPOSITION_CONTRACT_R1.json` — blob `275f6291a7813f0ce1a6fe723a8a891a56eba185`
- `evidence/validation/prev3/PREV3_EMPIRICAL_SOURCE_STATE_TO_PRODUCT_TARGET_DISPOSITION_CONTRACT_R1.md` — blob `5fb003c245232da7bb42a25942bf41a5901f2b7b`
- `WORKER_COMMISSIONS/J02/01_CONTRACT_SCHEMA.json` (this commission directory) — blob `a4d916a553b6c5039c57ea8607a15c5ac2df5c47`

## Tests

Executed before repository materialization:

`python3 evidence/selftest/prev3_source_state_target_disposition_contract.py`

Result: **17/17 checks PASS**. Exact check identities are frozen in the receipt. They cover resolved target/complement accounting, identical raw-code divergence under source-local authority, source-special fail-closed behavior, typed missing/nonresponse behavior, not-applicable denominator behavior, exact pre-query exclusion, prohibition of post-data denominator deletion, target-domain substitution rejection, complete accounting, prevention of universal promotion of source-specific specials, exact source/risk authority identity, deterministic replay identity, and absence of a native-code table in production logic.

`python3 -m py_compile tools/prev3_source_state_target_disposition.py evidence/selftest/prev3_source_state_target_disposition_contract.py`

Result: **PASS**.

## Bounds

No source-specific code table. No survey-family assumption. No native numeric code receives universal meaning. No learned positive empirical execution was performed. No structural/causal/person-state promotion was introduced. PRE-V3 remains objective-world only. OBL063 semantics are not revived.

## Successor gate

**HQ must reconcile J02 with the separate J03 source-local semantic-authority return before any learned positive re-execution.** J03 may provide competent source-local meanings; it does not authorize changing this generic denominator/target-disposition accounting law. J02 alone authorizes no source-specific positive execution.
