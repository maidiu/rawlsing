# S03 — GENERIC R4 BATCH RULE-ENVELOPE INTAKE / CONSTRUCTOR CONTRACT R1

Repository: `maidiu/rawlsing`
Branch: `agent/rabochii-prev3-w17-s03-generic-r4-batch-envelope-contract-r1`
Commission base: `8306aab9a3174f65c611f8157530307dabaf539c`

Exact grain:
`SDTF_R4_GENERIC_BATCH_RULE_ENVELOPE_INTAKE_AND_CONSTRUCTOR_CONTRACT_R1_ONLY`

Library: `NO`

## Mission

Consume adopted generic R4 binding contract `SDTF_R4_MECHANISM_RULE_AUTHORITY_BINDING_R1@1.0.0` and adopted R03 complete 28-row residual matrix as the canary-derived requirement inventory.

Derive a GENERIC, candidate-agnostic batch intake/constructor contract that can accept many mechanism-rule candidates without re-inventing architecture per candidate.

M10-M01 is a conformance fixture only. Do not encode Wright-specific semantics into generic fields or defaults.

Required contract must:
- expose all external constructor determinants required by the adopted R4 contract;
- represent exact refs, typed missing/blocker/N-A/candidate/current states without silent fallback;
- preserve six authority-role bindings and value-mode/calibration branching;
- preserve rule-currentness separation;
- distinguish candidate payload from generic contract/schema;
- define deterministic canonicalization/content-addressing/replay law;
- define batch row/candidate identity and per-candidate result/receipt form;
- permit parallel closure of independent requirement packages while keeping final current-selection serial;
- forbid latest/default/fuzzy selectors and silent N/A inference;
- support future source families/candidates without M10-specific codepaths.

## Required output

A governed contract/schema artifact plus a short return explaining:
- generic fields;
- candidate-specific fields;
- batch execution semantics;
- failure/blocker semantics;
- whether existing R4 runtime implementation can consume this contract directly or needs a separately authorized generic adapter implementation.

PASS at this grain freezes the generic interface only. It does NOT implement or mint any concrete mechanism rule.

## Hard forbiddens

No M10-M01 concrete rule body.
No rule CURRENT_ACCEPTED.
No new authority issuance.
No position repair/materialization.
No topology.
No V3/person state.
No OBL063.
No Library.
No MAIN/PRE-MAIN mutation.
Do not consume S01/S02 provisional output.

Work through PASS or the smallest exact blocker, commit governed return, and report final tip/artifact identities.
