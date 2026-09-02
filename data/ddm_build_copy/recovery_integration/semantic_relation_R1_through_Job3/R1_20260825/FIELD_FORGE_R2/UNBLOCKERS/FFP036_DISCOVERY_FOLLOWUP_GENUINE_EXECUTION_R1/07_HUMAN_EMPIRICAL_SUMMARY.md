# FFP036 — DISCOVERY-TO-FOLLOWUP GENUINE EXECUTION R1

Status: `PASS__DISCOVERY_FOLLOWUP_GENUINE_EXECUTION_COMPLETE__FROZEN_W0_W5_EVIDENCE_BANKED__NO_ARCHITECTURE_VERDICT`

Exact starting HEAD: `b7798a9bc48582e341309610c218aadce4355ea2`. Immutable handoff `ad2db7ece75fb6c2cd89260f8a70a153734895c9` was instruction evidence only. The frozen FFIF014 court was not redesigned or mutated.

## Frozen execution

The court executed the complete frozen `DISCOVERY_TO_FOLLOWUP_LINKAGE_MINIMUM@1` Q1 relation: 62,609 exact predicates over the 19,210-respondent Afrobarometer R5 risk set, stratified by the frozen 11-token `COUNTRY_ALPHA3` domain. The normalized target contains exactly **688,699** predicate-country cells.

All mandatory input hashes matched before target output, including the risk set, response facts, exposure facts, deterministic roster gzip, and canonical uncompressed roster. All 153,680 eight-variable exposure pairs on the risk set were `EXPOSED__PROVED`, with zero country-attachment mismatches.

## Exact result bank

The canonical target semantic SHA-256 is `0746052037bf815f953c4a0e06094350d3fcbd7557c782513b212c8667a9b6df` over 134,174,630 uncompressed canonical TSV bytes. It contains **259,991 `OBSERVED_POSITIVE`** cells and **428,708 `OBSERVED_ZERO`** cells. Every one of the 62,609 predicates satisfies `sum_country(country_support) == original_support`; no cell was dropped and all zero cells remain explicit.

ORACLE-A / W1 direct upstream re-query was executed without any FIELD-FORGE-local stored predicate/respondent membership table. A cold repeated W1 run was byte-for-byte identical. ORACLE-B / W5 independently constructed the full eight-state same-unit surface plus country and marginalized 4,600 full-profile-country groups; it reproduced the exact same canonical target hash.

W4 explicitly materialized 4,898,550 predicate/respondent memberships during execution and regenerated the same target hash with zero membership/support failures. W3 materialized the post-target Q1 sufficient statistic and independently reconstructed the same target hash. W2, constrained to predicate identity plus original support only, returns `UNDEFINED_FOR_OBJECT` for AS06 rather than fabricating a country joint relation. W0 can serve the cached final assertion but remains replay-incomplete for AS07. W6 remained excluded.

## Evidence banking

The canonical oracle target, W5 full-state surface, and W3 Q1 sufficient statistic were banked under `/Rawlsing/FIELD_FORGE_R2/FFP036_DISCOVERY_FOLLOWUP_GENUINE_EXECUTION_R1/` and then cold-rematerialized; all three were byte-identical to the executed local outputs.

## Ceiling

This worker records a bounded mechanical evidence vector only. W1 exact PASS supplies the frozen counterexample candidate contemplated by FFIF014: this Q1 result can be regenerated from exact producer-owned facts without FIELD-FORGE-local stored predicate membership. This worker does **not** issue the semantic architecture ruling, CVCR, COCR, arbitrary-future sufficiency, universal physical architecture, or terminal FIELD FORGE synthesis. W3 remains Q1-only; W4/W5 exactness does not promote persistence.

Terminal: `PASS__DISCOVERY_FOLLOWUP_GENUINE_EXECUTION_COMPLETE__FROZEN_W0_W5_EVIDENCE_BANKED__NO_ARCHITECTURE_VERDICT`
