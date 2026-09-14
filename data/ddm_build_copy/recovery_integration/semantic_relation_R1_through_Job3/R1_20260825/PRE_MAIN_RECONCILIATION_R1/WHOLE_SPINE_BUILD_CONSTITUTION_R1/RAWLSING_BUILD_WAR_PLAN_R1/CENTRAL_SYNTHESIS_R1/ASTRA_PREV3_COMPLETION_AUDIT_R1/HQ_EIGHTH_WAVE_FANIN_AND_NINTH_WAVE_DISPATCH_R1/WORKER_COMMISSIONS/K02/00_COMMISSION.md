# K02 COMMISSION — SOURCE-STATE → TARGET-DISPOSITION PRODUCTION INTEGRATION R1

Repository: `maidiu/rawlsing`
Branch: `agent/rabochii-prev3-w9-k02-source-state-target-production-integration-r1`
Commission parent / J02 return: `4c86fb44d06e27763b004dbd3181271cfb83efc1`
HQ authority: `a93e3717d9bea1857937a3fa278a933283948acc`

Execute only:
`PREV3_SOURCE_AGNOSTIC_SOURCE_STATE_TO_PRODUCT_TARGET_DISPOSITION_PRODUCTION_INTEGRATION_R1_ONLY`

Mission:
Productionize J02's reusable contract in the current PRE553 empirical-query seam:
`RAW_SOURCE_STATE -> SOURCE_LOCAL_GOVERNED_STATE -> PRODUCT_TARGET_DISPOSITION -> DENOMINATOR_RESOLUTION_CHECK -> EMPIRICAL_RESULT`.

Requirements:
- raw native numeric/string values remain opaque;
- source-local semantic authority is explicit/content-addressed;
- target-domain authority is explicit/content-addressed;
- denominator/risk-set authority remains distinct and frozen pre-outcome;
- no post-outcome denominator deletion;
- exact accounting of all expected record ids;
- unresolved source/target authority fails closed;
- deterministic replay identity covers source-state, target-disposition, denominator ledger, gate and result.

This is generic production integration only. DO NOT consume J03 LiTS-specific meanings as implementation constants. No source-family/native-code table may appear in generic production logic.

PASS requires implementation + targeted regression/self-test at the exact generic contract ceiling, or the smallest exact blocker. This lane does not independently qualify itself for HQ integration and does not execute the LiTS learned workload.

No structural/causal/person-state promotion. PRE-V3 objective-world only. No OBL063 revival.

Commit governed return and report final tip, production blobs, tests and replay identities.