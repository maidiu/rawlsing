# G-SR08-R1 LiTS I — authority integration referral

Status: `REFERRAL_ONLY__VOZHD_CHETIRI_ADJUDICATION_REQUIRED__NO_CERTIFICATION_DECISION`

This referral does not decide whether the existing authority is sufficient and does not unlock C05-R2B. It packages the local continuation findings for Vozhd Chetiri.

## Relation to the assigned Vozhd task

The assigned task was to resume G-SR08-R1 at the exact frozen-decoder boundary, execute the previously unexecuted LiTS-I burden, and then continue through the source-specific `GovernedC11Projection`, validated C11 release/repository, and frozen-I03 parity gates. It expressly prohibited parser substitution, semantic redesign, promotion of `latin1`, invention of weight or ID authority, and C05-R2B launch.

This referral is therefore a continuation handoff at the projection-authority gate. It is not a replacement mission, a certification decision, or a request to reconstruct the authority corpus. The physical decoder burden ran as assigned. During preparation for the next assigned gate, existing LiTS authority layers were found outside the frozen worker runtime/package and require Vozhd Chetiri to determine whether they are accepted execution inputs and how their existing dispositions are packaged. Once adjudicated, the result can return to the same G-SR08-R1 task at source-specific projection construction.

## Source execution already completed

- source: `LiTS_I.dta`
- SHA-256: `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`
- shape: 29,002 rows × 1,198 variables = 34,744,396 physical events
- decoder: `decode_dta(source_path, encoding="latin1")`
- compatibility status: `COMPATIBILITY_EXECUTION_ONLY__NOT_SOURCE_TEXT_ENCODING_AUTHORITY`
- full physical replay: PASS; all-row and all-variable frontier preserved
- native `id`: 29,002 rows / 29,002 distinct values, retained separately from row ordinal
- `q105_12`: 29,002 system-missing cells retained
- `weight_0`, `weight_1`, `weight_2`: each 29,000 ordinary + 2 system-missing cells

## Existing authority inputs located

1. `Rawlsing_V550_Response_Option_Authority_SAV_Derived_R2_20260815/authority_inputs/lits_response_option_authority.csv`
   - SHA-256: `e696eb5084458cb5424a53f96c9461cdf8ec3da8e5eb47dc0a4458b413a2f867`
   - 1,842 LiTS-2006 value rows; `packet_authority_final` throughout
   - 284 `certified`; 1,558 `preserved_not_certified`
2. `Rawlsing_Full_Question_Relation_Authority_Final_R1_20260814/QSM_FULL_QUESTION_RELATION_AUTHORITY_FINAL_R1.csv`
   - SHA-256: `0f7fa1c0f579fd44ad44a7ccfc576166b5e8b49895e2822dfc916dff8d00ad13`
   - 1,198 LiTS-2006 variable rows
   - existing statuses include governed QSMv2 relation, governed non-directional, governed manual relation, and administrative dispositions
3. `Rawlsing_Full_Question_Relation_Authority_Final_R1_20260814/QSMV2_INTEGRATED_UNIT_AUTHORITY_3196_R1.csv`
   - SHA-256: `80af2ece8e8f9b669ef405ba2b506d68e8e36facc404609cc539b3419a5c48fb`
4. `joint_family_review_queue_recovered/review_only_registries/lits_question_family_registry.review_only.yaml`
   - SHA-256: `4107259ebe2012ddfa1ee9df8f42c0fbf6ba0fe35185980ca3d8f4d87b246592`
   - explicitly `status: review_only`, `execution_eligible: false`; requires adjudication before execution use
5. `_methodology_bundle_stage/data/ddm_build/reports/source_structure_audits/LiTS_2006_LiTS_I.yaml`
   - SHA-256: `f9068c2c3f76f6de16be5b30e44d501b164b33dc454dddc654112116ddcd3702`
   - records 1,198 source columns and 1,198 codebook rows

## Questions for Vozhd Chetiri

1. Are the listed LiTS-2006 QRA and response-option rows accepted as the source-specific inputs for this court?
2. May `preserved_not_certified` response rows be carried as raw/typed unresolved physical states, with no semantic promotion?
3. Should the review-only LiTS family registry be excluded, mechanically activated from existing authority, or separately adjudicated?
4. Which QRA dispositions become explicit C11 projection bindings, and which become explicit exclusions or typed unresolved states?
5. Is the resulting authority closure sufficient to construct and validate `GovernedC11Projection` for this LiTS-I court?

The four existing UNKNOWNs remain unchanged: intended source-text encoding; cross-release semantic equivalence; universal/default weight selection; and durable native-ID semantic identity beyond SHA plus row ordinal.

No new semantic authority, source bytes, carrier, runtime code, C11 release, repository, or I03 result is created by this referral.
