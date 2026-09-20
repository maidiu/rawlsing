# FIABC-LM1-R1A — Fresh Rebuild Authority Adjudication

## Holding

FRESH_R5_REBUILD_AUTHORITY_NOT_YET_PROVED

No executable rebuild protocol is issued by this worker.

A fresh governed R5 is technically specifiable from the current repository contracts, but accepted execution law still forbids repeating the completed LiTS-A first-build. Technical sufficiency is not authority.

## Authority matrix

| Required item | Holding |
|---|---|
| canonical LiTS-I source SHA | PROVED: 7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09 |
| authoritative builder class | PROVED: R5CompactLongShardedBuilder |
| authoritative builder blob | PROVED at accepted Route-A authority: 92e364b31eaf27be1bca2081eff65f6ffb779c3d |
| current live R35 builder pointer | DEFECTIVE: freezes nonexistent 92e68693d72cbfcdd1c6d16e7f247ca3f60c8c55 |
| reader/version/config | PROVED at current R35 grain: pyreadstat 1.3.6; user_missing true; apply_value_formats false; encoding latin1; compatibility-execution-only |
| current LiTS projection | PROVED: 84361298ae702786a3fd1044bf619ffa4fe9ed2877040724386951e9c9d27872 |
| current expected learned product | PROVED: 47d36b1459c2458c480b58631d2c78af68be4dde44015a9220b09177b1eeb28d |
| current semantic replay hash | PROVED: 301735d4563314a0d7c133fa1afbb0ca57679b3fad887c66e77a909494779eb5 |
| current runtime catalog | PROVED: 5983d7d5c579b916ad46c1acf9e41c1c89b516a4e561a99b1d2b477bf5ad2d02 |
| current active binding | PROVED: a5f36a81843fe2ebab0b5cccb369ce76035f842b93e602613b8b9f3a81103308 |
| current runtime release | PROVED: 192926fabd9c9c3d40e43b1d7705ca2bcfe7f8d06e286be26d4b886d436df43f |
| Candidate-A owner blob | PROVED: d4915e7e6755ba1850756aebff72f982f73a332b |
| generic R35 parentage bundle machinery | PROVED |
| T4 charge treatment for newly executed build | PROVED: EXECUTED_NOW; candidate physical realization is chargeable C2 |
| historical derivative identity required as semantic prerequisite | NO generic R35 requirement demonstrated |
| authority to repeat completed LiTS-A first build | NOT PROVED; current T2 manifest explicitly forbids it |

## Exact rebuild-law blocker

WORKER_RETURNS/FIABC-T2/01_SIX_CELL_EXECUTION_MANIFEST.json contains:

NO_REPEAT_COMPLETED_LITS_A_FIRST_BUILD

and treats the preserved qualifying R5 first-build as a completed preparatory stage.

FIABC-T3 preserves the T2 six-cell capability set and contract. FIABC-T4 explicitly records t2_six_cell_manifest_preserved=true. FIABC-R35-I02 changes the provenance admission gate for the preserved carrier but says that if its first-build parentage receipt is absent, LiTS-A stops. It does not grant a repeat-build exception.

Therefore the missing authority item is an accepted, narrow succession that expressly authorizes replacement of the unparented preserved LiTS-A R5 and supersedes the no-repeat clause only for that replacement operation.

## Exact stale-pointer repair surface — record only, do not mutate here

The named owner commit 0b96b8de9aac774566f872cf0630ebd4ddeb70e6 contains the accepted R5 runtime files, but FIABC-R35-I02 froze five non-object Git IDs.

Required mechanical repair surface if separately adopted:

rawlsing_next/ee_p2x_darwin_stage_backend.py

- pre553_r5_codec.py:
  malformed 72f8e8a2b6b2330332030e3978077c11e38ec8db
  -> actual 72f8f3c03ed065e86fea4e76bb17f8e06c2bf540
- pre553_r5_compact_carrier.py:
  malformed 92e68693d72cbfcdd1c6d16e7f247ca3f60c8c55
  -> actual 92e364b31eaf27be1bca2081eff65f6ffb779c3d
- pre553_r5_model.py:
  malformed 62cea85788eb160796642ba09d9f0d41f987a3d43
  -> actual 62ce608829c3d9c2fb7c999aefe40188637edf80
- pre553_r5_seam.py:
  malformed cef346fca029fa920db16e83db908d466018f39e
  -> actual cef326ebbc40468428378f7fdbe76e4756179f39
- pre553_r5_single_pass_audit69.py:
  malformed ffb07a9d0bafbf685d27aa1161ce830bcfc810fc
  -> actual ffb063b93c86e215604eecb29a9545c7efdff399

Also update the mirrored builder expectation in:
tests/test_fiabc_derivative_parentage.py

from 92e68693d72cbfcdd1c6d16e7f247ca3f60c8c55
to 92e364b31eaf27be1bca2081eff65f6ffb779c3d.

No schema, source identity, Candidate-A semantic contract, runtime catalog identity, workload identity, or T4 accounting rule needs to change for that pointer repair.

## What a later rebuild authorization would have available

This section is evidence inventory only, not an executable protocol.

The accepted builder defaults at the authoritative implementation are:
- run_max_rows = 4096
- run_max_bytes = 4194304
- shard_max_rows = 16384
- shard_max_bytes = 16777216
- merge_fan_in = 8
- verified_spool_memory_bytes = 1048576

The R35 bundle machinery can bind a newly emitted physical_root_id to:
- canonical source verification;
- exact producer identity/blob/version;
- exact reader config;
- exact derivation operation BUILD_LITS_A_R5_FROM_CANONICAL_PHYSICAL_INCIDENCE;
- exact derivative class LITS_A_PRESERVED_R5_CARRIER;
- r5_root_metadata including carrier/schema/codec, logical digest, canonical row count, member inventory, build config, release identity and source artifact ref;
- scope/currentness/ownership determinants;
- source receipt identity, derivative receipt identity and bundle identity.

The current consumer environment contract names:
- RAWLSING_EE_P2X_LITS_A_R5_ROOT
- RAWLSING_EE_P2X_LITS_A_R5_PARENTAGE_RECEIPT
- RAWLSING_EE_P2X_LITS_A_R5_PARENTAGE_RECEIPT_IDENTITY

If a later accepted authority expressly permits the replacement build, the newly performed build would be accounted as EXECUTED_NOW. The old R5 may then be used only as comparison/replay evidence; it donates no numeric execution credit.

## Admission checks already available after any future lawful build

These checks are recorded as available mechanics, not permission to execute the build:
- verify the exact canonical source SHA before decode/build;
- verify exact pyreadstat/runtime reader config;
- require an absent target;
- verify emitted root and member inventory integrity;
- verify generic R35 source receipt, derivative receipt and bundle identities;
- assert the R5 embedded canonical source closes to LiTS-I;
- run tests/test_fiabc_derivative_parentage.py;
- run rawlsing_next/tests/test_fiabc_t4_live_accounting.py;
- run tests/test_fiabc_telemetry_semantics.py;
- run tests/test_fiabc_lifecycle_accounting.py;
- run rawlsing_next/tests/test_fiabc_t3_oracle_process_envelope.py;
- run rawlsing_next/tests/test_fiabc_w3_i06a_process_isolation.py;
- run rawlsing_next/tests/test_fiabc_t2_six_cell_execution_binding.py;
- run the local-court source-independent integration/receipt tests.

None of those checks substitutes for the missing rebuild authorization.

## Current action

STOP before local source access or rebuild.

Authority must first:
1. adopt the exact R35 runtime Git-pointer correction; and
2. explicitly supersede NO_REPEAT_COMPLETED_LITS_A_FIRST_BUILD for one governed replacement build whose output receives generic R35 parentage.

This worker does not issue that succession and does not create a follow-on commission.
