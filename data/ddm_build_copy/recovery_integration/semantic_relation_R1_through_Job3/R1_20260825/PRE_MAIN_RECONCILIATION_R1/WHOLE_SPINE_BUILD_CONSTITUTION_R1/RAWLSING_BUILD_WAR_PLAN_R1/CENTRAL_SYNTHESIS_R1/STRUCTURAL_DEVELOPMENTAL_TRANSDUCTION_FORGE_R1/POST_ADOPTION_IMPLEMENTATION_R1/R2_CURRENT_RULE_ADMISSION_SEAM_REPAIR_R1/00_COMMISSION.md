# COMMISSION — SDTF R4 R2 CURRENT-RULE ADMISSION SEAM REPAIR R1

Repository: `maidiu/rawlsing`

Branch:
`agent/rabochii-hq-sdtf-r4-r2-current-rule-admission-seam-repair-r1`

Exact repair base:
`ef087753d4adda452312ba30057b2ae07d3714c4`

HQ blocker adoption:
`87f2ebbfc7f07595a26d975de7a269e5b9f37e95`

Fresh court blocker return:
`4b60c9931899e4b993b52029dfa60bc6c27843f4`

Exact blocker:
`R1_R2_CURRENT_RULE_ADMISSION_AND_EXACT_RULE_IDENTITY_CHAIN_NOT_CONSERVED`

Authorized grain:
`SDTF_R4_R2_EXACT_R1_CURRENT_RULE_ADMISSION_CONSERVATION_REPAIR_R1_ONLY`

## Mission

Repair only the R1 -> R2 admission-consumer seam so that no R2 rule application may become or remain `SUPPORTED_CURRENT`, expose a current consequence, or be redriven as current unless the exact R1 governed mechanism-rule admission has been consumed, validated and conserved.

R1 already owns the authority/currentness decision. Do not duplicate or reinterpret it.

The exact R1 production identity is frozen:
`rawlsing_next/sdtf_r4_mechanism_rule_authority_binding.py`
blob `c94997f5c7f2bbee9cd99c570554fd48c0f47556`

The R2 candidate to repair is:
`rawlsing_next/sdtf_r4_d1_hosting_replay.py`
blob `66ffd2e1df9ab81970af9264f27de1f449752064`

The exact hostile proof established that R2 currently accepts raw `rule_id / rule_version / rule_hash`, reconstructs `MECHANISM_RULE_RECORD`, and can create current application/consequence state without an R1 `MechanismRuleAuthorityBinding`, `require_current_rule_admission()`, or exact rule-current-selection evidence.

## Required repair law

At minimum:

1. R2 current hosting must require exact R1 current-rule admission proof, not a caller promise.
2. The exact R1 rule identity must be conserved across R2; do not reconstruct a semantically different `ExactRef.kind` and call it equivalent.
3. The R1 admission/binding identity or semantically equivalent exact content-addressed proof must survive into the R2 application/revision provenance and deterministic replay material.
4. Current hosting must fail closed when the R1 rule is candidate, historical-noncurrent, missing current-selection evidence, authority-incomplete, or otherwise not accepted by `require_current_rule_admission()`.
5. Redrive must not preserve/create current outputs through a rule whose exact R1 current admission is absent or no longer current.
6. Historical application/revision provenance must remain preserved; lack of current admission must not synthesize an opposite fact.
7. Determinant-scoped invalidation, reverse dependency, replay determinism, history preservation and same-context self-ancestry law from R2 must remain intact.
8. Existing R1, R3 and R4 candidate production files are immutable in this grain.

## Explicit prohibitions

- no mechanism-rule minting;
- no rule-owner or authority selection;
- no causal-use permission inference;
- no calibration choice;
- no R4 semantic redesign;
- no changes to K1-K4 witness semantics;
- no world-response changes;
- no OBL062 closure;
- no concrete actor facts;
- no HQ/main mutation;
- no integration qualification by this producer.

## Required focused proof

Add focused tests proving at least:

- the exact hostile no-R1-admission path is now rejected;
- exact R1 current admission permits lawful current R2 hosting;
- exact identity is conserved rather than re-kinded;
- candidate/noncurrent/missing-selection R1 admission fails closed;
- replay/application provenance includes the exact admission identity;
- redrive cannot use an unadmitted/noncurrent rule to maintain current output;
- prior R2 dependency/invalidation/replay/self-ancestry invariants remain green.

Run the exact R2 focused suite plus the smallest R1-focused checks required to prove the seam. Do not claim full R1-R4 qualification.

## PASS

`SDTF_R4_R2_CURRENT_RULE_ADMISSION_SEAM_REPAIR_COMPLETE__READY_FOR_FRESH_INTEGRATION_REQUALIFICATION`

## BLOCKER

`SDTF_R4_R2_CURRENT_RULE_ADMISSION_SEAM_REPAIR__EXACT_BLOCKER_PROVED`

Commit the exact implementation, focused tests and governed return. Report final branch tip, production/test blobs, contract/version disposition and PASS or exact blocker.