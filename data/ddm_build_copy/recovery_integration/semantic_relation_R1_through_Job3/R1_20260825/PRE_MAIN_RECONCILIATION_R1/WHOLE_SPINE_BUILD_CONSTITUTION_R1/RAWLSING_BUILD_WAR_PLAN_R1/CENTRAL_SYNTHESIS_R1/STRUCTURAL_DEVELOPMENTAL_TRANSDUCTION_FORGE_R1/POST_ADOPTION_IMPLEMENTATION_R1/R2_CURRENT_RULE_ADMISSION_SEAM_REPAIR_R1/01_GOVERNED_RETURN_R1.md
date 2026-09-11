# GOVERNED RETURN — SDTF R4 R2 CURRENT-RULE ADMISSION SEAM REPAIR R1

## Terminal

`SDTF_R4_R2_CURRENT_RULE_ADMISSION_SEAM_REPAIR_COMPLETE__READY_FOR_FRESH_INTEGRATION_REQUALIFICATION`

## Authorized grain

`SDTF_R4_R2_EXACT_R1_CURRENT_RULE_ADMISSION_CONSERVATION_REPAIR_R1_ONLY`

## Exact repair

The R1→R2 seam now requires exact R1 `MechanismRuleAuthorityBinding` admission before R2 may create `SUPPORTED_CURRENT` state. R2 calls the frozen R1 `require_current_rule_admission()` gate and separately requires exact equality between the R1 `rule_identity.ref` and the R2 application rule ref.

The former R2-only re-kind `MECHANISM_RULE_RECORD` is removed. `D1RuleApplicationRef.mechanism_rule_ref` is now exactly the canonical R1 `SDTF_R4_MECHANISM_RULE` ref constructed by the frozen R1 `MechanismRuleIdentity` law.

Every R2 application revision now conserves:
- the exact consumed R1 authority-binding ref;
- the exact current-admission ref when the revision is `SUPPORTED_CURRENT`;
- the exact canonical R1 mechanism-rule ref in revision semantic material.

Replay steps and replay receipt identity include the binding/admission provenance. Thus a current consequence cannot survive in deterministic replay material detached from the exact R1 admission that licensed it.

Direct hosting without R1 admission, with candidate/historical R1 binding, or with a current binding for a different exact rule identity fails closed before current state is hosted.

On redrive, absence of an exact current admission, a noncurrent binding, or an identity mismatch does not preserve or synthesize a current consequence and does not call the evaluator. R2 appends a `CLOSED_UNSUPPORTED` revision, removes the prior current output, preserves append-only history, and records supplied binding provenance when one exists. No opposite fact is synthesized.

## Contract disposition

The R2 hosting/replay contract is intentionally bumped from:

`SDTF_R4_D1_HOSTING_REPLAY_R1@1.0.0`

to:

`SDTF_R4_D1_HOSTING_REPLAY_R1@2.0.0`

This is a breaking semantic correction, not an additive compatibility claim: the old application identity encoded the wrong rule kind and the old API admitted authority-free current state.

A narrow seam sub-contract is also explicit:

`SDTF_R4_R2_CURRENT_RULE_ADMISSION_CONSERVATION_R1@1.0.0`

No R1 contract was changed.

## Exact identities

- commission tip: `f6c96200edd14dda924293e20f0c3cd7ce20a2ab`
- repair production commit: `2c559f81c5a2b0641dbbabc1ef168dffad46b4fa`
- governed evidence execution tip: `2d9c1dc2def3c515a1d10cc90434a79d261c273b`
- R2 production file: `rawlsing_next/sdtf_r4_d1_hosting_replay.py`
- repaired production blob: `7f5a2f677e60cd4d218737faa61140dddc55cc28`
- updated exact R2 regression suite blob: `cd4a3c0b81853205d825c6cd0b507c0ca971f850`
- focused hostile seam test blob: `aadc215c1561552461cf84df64243d0da60fb24e`

Frozen production identities preserved:
- R1 `rawlsing_next/sdtf_r4_mechanism_rule_authority_binding.py`: `c94997f5c7f2bbee9cd99c570554fd48c0f47556`
- R3 `rawlsing_next/sdtf_r4_witness_currentness.py`: `06c8a2259436e7209bad4e4b3f8c314b18446fe6`
- R4 `rawlsing_next/sdtf_r4_world_response_redrive.py`: `9964a24e25467fa53cc9f5529b6f40be9f11f53a`

## Governed execution

Workflow: `Rabochii Governed Bounded Court`
Run: `34584793057`

First clean execution, job `103216387780`:
- protocol self-tests: `20 passed`
- commissioned court: `35 passed`
- receipt artifact: `10193112341`
- artifact digest: `sha256:5d8f55ab962395ffe01405286c0c4291c560e1c9fa0f3f44dcce30fe1e8a318b`

Second clean execution, job `103216570316`:
- protocol self-tests: `20 passed`
- commissioned court: `35 passed`
- receipt artifact: `10193132980`
- artifact digest: `sha256:1c88e920f9bafbd880b1832d9c92d277422e9b8957856b4dbc39e3b7bb6dde52`

The commissioned court contains the focused hostile seam tests, the complete existing R2 hosting/replay regression suite, and the R1 mechanism-rule authority-binding suite.

## Boundaries preserved

No R1, R3, or R4 production candidate was modified. No rule was minted. No authority was selected. No calibration was chosen. No OBL062 closure or integration qualification was performed. R2 remains an admission consumer and hosting/replay adapter only.

## HQ disposition

The seam repair is producer-complete and ready for a fresh independent R1–R4 integration requalification. This return does not perform or substitute for that independent integration court.
