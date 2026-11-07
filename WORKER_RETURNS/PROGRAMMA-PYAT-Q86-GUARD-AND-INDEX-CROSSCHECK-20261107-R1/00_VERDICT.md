# R8 VERDICT

## Terminal disposition
`R8_Q86_SOURCE_IDENTITY_GUARD_IMPLEMENTED__TRUE_Q86_HASH_PRESERVED__NEGATIVES_REFUSED__R7_ACCEPTANCE_PENDING__NO_MERGE`

## Result
- The frozen FF producer now requires exact `QUESTION_IMPLEMENTATION` refs for Q86B conditioner and Q86A target from the existing `wave1_r5_q86_c11_projection.question_ref` source owner. It refuses unlike pairs, forged Q86-like object IDs, wrong identity hashes, and swapped roles before profile minting.
- The true frozen Q86 relation hash is preserved: `urn:rawlsing:field-forge:conditional-support:sha256:1ffdfe536adc01d35709521145b9c8057f589c20983f507d5ed6197c4ad27d19`, count-profile hash `49bf14eb4a2b7fbf8e79ea4c72d10f4027819381564f582242ef6e24fc14fb59`.
- Required negative outcomes are recorded in `01_IDENTITY_GUARD_PROOF_AND_NEGATIVES.md` and `R8_PROOF_TRACE.json`.
- Focused sourcefree tests: `140 passed in 117.78s`, exit `0`; C11/facade/query tests: `58 passed in 2.25s`, exit `0`.
- The 16-chain cross-check is in `02_INDEXED_16_CHAIN_CROSSCHECK.tsv`; the stage-specific generic-vs-canary answer is in `03_GENERIC_VS_CANARY_CURRENTNESS.md`.
- A generic Field Forge relation producer does **not** run alongside Q86 at a current protected stage. The generic path is current at PRE553 I03/I05, then stops at the unmerged/test-only GF1 candidate. This commission did not broaden into a generic FF implementation.

## Review gates
- R7 exact-head acceptance is still pending. PR #770 (`392de04e86202a2a80361a91808ef06fd34c1cc8`) has no independent review and its `governed-court` check failed on inherited tests; the R8 PR must not claim the R7 gate is accepted.
- R8 requires a separate nonauthor exact-head reviewer. No self-acceptance, protected merge, native/source issuer, S3, actor, or scientific promotion is claimed.
- The branch is isolated as required: `fix/pyat-r8-frozen-ff-q86-source-identity-guard-20261107-r1`.
- PR URL and final head SHA are recorded in `05_INDEPENDENT_REVIEW_REQUEST.md` and the PR review comment.

## Scope
Only the frozen producer and its tests/return evidence changed. The C to D bridge, D to M4 bridge, M1/M4/M5, permission ceilings, relation family/version, and source-specific canary data were not widened or generalized.
