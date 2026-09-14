# PRE-V3 empirical source-state to product-target-disposition contract R1

## Result

PASS at producer/self-test level for the J02 grain `PREV3_EMPIRICAL_SOURCE_STATE_TO_PRODUCT_TARGET_DISPOSITION_CONTRACT_R1_ONLY`.

The reusable objective-world path is explicit and mechanically gated:

`RAW_SOURCE_STATE -> SOURCE_LOCAL_GOVERNED_STATE -> PRODUCT_TARGET_DISPOSITION -> DENOMINATOR_RESOLUTION_CHECK -> EMPIRICAL_RESULT`

The implementation treats every raw native value as opaque. It never assigns semantic meaning from a number or string token. Source meaning is accepted only through an exact content-addressed `SOURCE_SEMANTICS_TOPOLOGY` authority ref already frozen in the query envelope; target membership is accepted only through an exact `TARGET_USE_PERMISSION` authority ref and exact target-domain ref; denominator membership is accepted only through exact `ROUTING_RISK_SET` authority and a `PRE_QUERY` eligibility binding.

## Minimum lawful state space

The source-local layer can carry `SOURCE_SUBSTANTIVE`, `TYPED_MISSING_NONRESPONSE`, `SOURCE_NOT_APPLICABLE_OR_INELIGIBLE`, `SOURCE_SPECIFIC_SPECIAL`, or `SOURCE_UNKNOWN`. These labels are authority outcomes; they are not interpretations of raw codes.

The product layer can carry `TARGET_MEMBER`, `RESOLVED_NON_TARGET`, `TYPED_MISSING_NONRESPONSE`, `NOT_APPLICABLE_OR_INELIGIBLE`, `AUTHORIZED_PREQUERY_EXCLUSION`, or `UNRESOLVED`.

Only `TARGET_MEMBER` and `RESOLVED_NON_TARGET` resolve a denominator member. A typed missing/nonresponse state or a not-applicable/ineligible response state does not, by itself, remove that record from the denominator and does not count as resolved. `SOURCE_SPECIFIC_SPECIAL` and `SOURCE_UNKNOWN` fail closed to `UNRESOLVED` in the universal layer.

## Denominator law

Denominator membership and target membership are independent decisions. The frozen query envelope declares the complete expected record-id set before outcome binding. Every expected record must be accounted for exactly once.

The only denominator-removal path is `PREQUERY_EXCLUDED`, bound to the exact frozen `ROUTING_RISK_SET` authority, exact risk-set ref, exact routing/eligibility basis ref, and phase `PRE_QUERY`. A product target disposition cannot convert a denominator member into an exclusion. Therefore post-data denominator deletion, recoding, target expansion, or semantic substitution is rejected rather than repaired.

For denominator members, the gate computes both `raw_denominator_support` and `raw_resolved_target_support`. `EMPIRICAL_RESULT` is emitted only when they are equal and no member is unresolved. This preserves the accepted PRE553/I03 fail-closed denominator-resolution invariant.

## Identity and replay

Source-state bindings, target-disposition bindings, the denominator ledger, gate, and result all receive SHA-256 identities over canonical semantic material. The query envelope includes exact source-semantic, target-use, routing/risk-set, replay-protocol, target-domain, and risk-set identities. Reordering input records leaves gate and result hashes unchanged.

## Hostile proofs

The self-test contains 17 passing checks. It proves that the same raw numeric token can have different governed source-local meanings and different target dispositions; a source-specific special fails closed; typed missing/nonresponse and not-applicable states remain unresolved denominator members unless separate pre-query eligibility authority excludes them; post-data deletion and target-domain substitution are rejected; incomplete accounting is rejected; exact source/risk authority identities are enforced; and deterministic replay hashes are stable.

Commands used on the authored artifacts:

```text
python3 evidence/selftest/prev3_source_state_target_disposition_contract.py
python3 -m py_compile tools/prev3_source_state_target_disposition.py evidence/selftest/prev3_source_state_target_disposition_contract.py
```

Both passed locally before repository materialization.

## Bounds and successor gate

No source-specific table, survey-family assumption, numeric-code meaning, learned positive empirical execution, structural/causal/person-state promotion, PRE-V3/V3 boundary weakening, or OBL063 revival is introduced.

This is producer/self-tested only. HQ must reconcile this generic contract with the separate source-local semantic-authority lane before any later learned positive re-execution. A source-local lane may supply exact meanings; it may not change this generic denominator/target accounting law.
