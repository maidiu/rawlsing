# HQ SDTF R4 R2 CURRENT-RULE ADMISSION SEAM REPAIR ADOPTION R1

STATUS: `REPAIR_CANDIDATE_PASS_BANKED__FRESH_R1_R4_REQUALIFICATION_RELEASED`

Repair branch:
`agent/rabochii-hq-sdtf-r4-r2-current-rule-admission-seam-repair-r1`

Commission:
`f6c96200edd14dda924293e20f0c3cd7ce20a2ab`

Final repair return:
`5f57da82f281e361da8271326a511d81b6d61999`

Terminal:
`SDTF_R4_R2_CURRENT_RULE_ADMISSION_SEAM_REPAIR_COMPLETE__READY_FOR_FRESH_INTEGRATION_REQUALIFICATION`

Accepted candidate repair:
- R2 now consumes frozen R1 `require_current_rule_admission()` before `SUPPORTED_CURRENT` hosting;
- exact R1 rule ref kind `SDTF_R4_MECHANISM_RULE` is conserved end-to-end;
- exact consumed R1 authority-binding/current-admission provenance is embedded in application revision and replay identity;
- missing/noncurrent/mismatched admission closes unsupported current output fail-closed without evaluator invocation or opposite-fact synthesis.

Exact repaired R2 production blob:
`7f5a2f677e60cd4d218737faa61140dddc55cc28`

Updated R2 regression blob:
`cd4a3c0b81853205d825c6cd0b507c0ca971f850`

Focused seam hostile-test blob:
`aadc215c1561552461cf84df64243d0da60fb24e`

Contract disposition:
`SDTF_R4_D1_HOSTING_REPLAY_R1@2.0.0`
with narrow seam contract
`SDTF_R4_R2_CURRENT_RULE_ADMISSION_CONSERVATION_R1@1.0.0`.

Frozen R1/R3/R4 production identities remain unchanged. This HQ disposition accepts the producer repair only as the next exact candidate and releases a fresh independent full R1-R4 integration/conformance requalification. It does not runtime-adopt the assembled package yet.
