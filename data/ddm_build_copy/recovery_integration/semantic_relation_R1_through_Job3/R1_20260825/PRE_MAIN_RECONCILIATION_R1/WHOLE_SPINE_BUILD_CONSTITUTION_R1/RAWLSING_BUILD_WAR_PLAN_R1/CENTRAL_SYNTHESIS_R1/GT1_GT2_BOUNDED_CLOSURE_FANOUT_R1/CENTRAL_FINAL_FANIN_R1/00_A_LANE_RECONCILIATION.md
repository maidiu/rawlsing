# GT12 CENTRAL FINAL FAN-IN R1 — A-LANE RECONCILIATION

## Status

`PASS__GT12_A_LANE_RECONCILED_FOR_FINAL_FANIN`

## Common substrate

Both positive empirical workers descend from terminal A1:

- A1 terminal: `2753d1abbcb702e9260f4ab60c528748fb28c7d2`
- exact C11 release: `C11LogicalRelease / R5_GT12_Q86A_Q86B_FROZEN`
- release hash: `8315b104a94ae985a3ee3d77c8c365d5fcef6b6cb51a606df5bf141434668295`
- replay manifest hash: `c80d08ca9a5bb4814bdca3c0c21cb4c708da32840d6459b190cca206c3e3b4aa`
- empirical-universe hash: `4dc56730f5c3b06838cc8a6116e0f4c78662b76d75b578918f7207cea3902dd1`
- source rows preserved: `51,587`
- exact claim members: `19,210`

## GT1

Worker A2 terminal: `eb625ef51a99d9661d90e9ac3e496b00f7e9032a`

Terminal: `PASS__REAL_GT1_SUPPORTED_19210__DETERMINISTIC_REPLAY`

- claim: `GT1_R5_Q86A_RAW_UNARY_EXACT_RISK_SET@1`
- state: `SUPPORTED`
- denominator: `19,210`
- query hash: `aeac560d90bd504ce488d63227f812ff2f8613d8a0570a0b6cdcae0b72658aba`
- fact hash: `6fbd00cc6d0086f686a310857647f0aa0e6076d0be5a46ed3d2a8fe13a0a8baf`
- deterministic replay: exact equality

## GT2

Worker A3 terminal: `843fd5ae70c578226f96ffa6c0a220493360c856`

Terminal: `PASS__REAL_GT2_SUPPORTED_19210__DETERMINISTIC_REPLAY`

- claim: `GT2_R5_Q86A_X_Q86B_RAW_JOINT_EXACT_RISK_SET@1`
- semantic order: `Q86B -> Q86A`
- CONDITIONER: `Q86B`
- TARGET: `Q86A`
- state: `SUPPORTED`
- denominator: `19,210`
- query hash: `e91970c161736113201a3e9880034f8d088099aad67300a5aa689b7a08200670`
- fact hash: `7bdb8752df31905a737d1a21c2ada61fe0c64d9cb4db17ea9bb748a1cf25b27f`
- replay hash: `10c4c50af557fe92866c6033a424ba2ab56847400bf9f970e6666612f435cae0`
- deterministic replay: exact equality

## Parallel production-code reconciliation

A2 and A3 both independently repaired the same genuine-scale `DERIVED_BRANCH_COHORT` performance defect in `rawlsing_next/_pre553_query_predicate.py`.

Central selects A2's production implementation as the integrated implementation because it compiles exact derived-cohort membership once per verified predicate AST and threads the resulting immutable mapping through execution. The cache is execution-local and nonauthoritative.

A3's alternative module-level identity cache is not integrated. A3 remains authoritative execution evidence for the genuine GT2 fact/replay because its exact source/release/universe/query/fact/authority identities and hostile matrix are banked on immutable worker terminal `843fd5ae70c578226f96ffa6c0a220493360c856`.

`EXECUTION_EVIDENCE_ACCEPTANCE != PRODUCTION_PATCH_ACCEPTANCE`.

No GT2 semantic result depends on a meaning change between the two performance implementations; both are expressly nonsemantic cohort-membership caching over the same exact membership identity. Final central regressions must nevertheless execute GT2 through the selected integrated A2 predicate implementation before adoption.

## Downstream selected workers

- Closure B: `a4c6e57d628c94cf1a6cda9e149371d230dacd62`
- Closure C: `24eccabda8a15ad885ece71351b8464e68eebda3`
- Closure D audit packet: `5ce9b13285f5ac42297e01a21e8dba4026c0a5ac`

No PRE-MAIN or `main` movement is authorized by this receipt.
