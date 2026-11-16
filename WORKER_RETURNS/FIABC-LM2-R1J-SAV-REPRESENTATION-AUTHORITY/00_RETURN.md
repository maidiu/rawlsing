# FIABC-LM2-R1J — WVS7 SAV Decoder Representation Authority Recovery

Status: `PASS`

Terminal:

`FIABC_LM2_R1J_SAV_REPRESENTATION_AUTHORITY_PASS__EXACT_Q291_PHYSICAL_NATIVE_BRIDGE_AUTHORIZED__R6S_BINDING_REISSUED__LOCK2_PRESERVED__READY_FOR_R15_R16_RETRY`

Version-parity decision:

`REPRESENTATION_EQUIVALENCE_PROVED__R1G_CARRIER_ADMISSIBLE`

## Holding

The missing A→B premise is now independently proved and narrowly authorized.

For the exact WVS7 source SHA `2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d`, accepted physical metadata proves Q291G5 ordinal 388 and Q291P5 ordinal 394 are SAV numeric variables exposed by ReadStat as `double` with storage width 8 and SPSS display format `F3.0`. The exact tagged pyreadstat 1.3.2 and 1.3.6 stacks both route SAV numeric cells through ReadStat's C-double lane and then through pyreadstat's `READSTAT_TYPE_DOUBLE -> np.float64` path. With `user_missing=True`, SPSS defined-missing numeric values are converted through that same numeric path rather than replaced by NaN; system missing remains separate. With `apply_value_formats=False`, labels are not substituted for values.

This supplies a representation statement only:

`SAV native numeric code/state N -> ReadStat double -> pyreadstat float64 physical material -> exact R5 float64 token/key`.

It does not derive source semantics from raw values. EE-R6A/P2F2 remains the authority for native response meaning/state; R1E remains the authority only for native substantive code -> program token.

## Q291 type premise

Browser-accessible accepted Rawlsing physical evidence already closes the declared-type premise:

- Q291G5: ordinal 388, `storage_type="double"`, storage width 8, `F3.0`, missing range -5..-1.
- Q291P5: ordinal 394, `storage_type="double"`, storage width 8, `F3.0`, missing range -5..-1.

The R1I structural preimage's `storage_type=null` is downstream information loss in the structural materializer, not absence of the accepted source metadata. No local metadata verification is required.

## Narrow authority and R6S repair

A new authority kind `PHYSICAL_NATIVE_REPRESENTATION_BINDING` was introduced rather than overloading `SOURCE_SEMANTICS_TOPOLOGY`.

Representation authority hash: `63543411892d8d30fb5670a39714a3dc115145e3f054a7017a325dab1c6cf053`  
Representation snapshot: `e23ec7451d150597799bbd9049cdab45339e647694a9ccfacb2e53aaf09b609b`  
Reissued response-binding identity: `f225e6289b553ab221902c95c1b416bbd01fb722efcc77c909e239d4ee02e87b`  
Reissued projection authority: `5e793e2fe255d0a0ef6dd405f4bd4c7df125c2d6fb23bd464a0f77d65cb1fcdf`  
Reissued projection snapshot: `540914a3ddf3b0349720fd81de49b1a88f194929adf1ea5506718af94e65c0d2`  
Reissued projection identity: `f400c804fea9b526f25eac823138ecb30e10efaad3207c4578661f684adee665`

R6S now constructs Q291 physical response keys from the exact authorized float64 representation table. It does not add generic numeric coercion to C11. Substantive and special native semantics remain unchanged; special states remain noncanonical; system missing remains the separate None/system-missing key; R1E remains unchanged.

## Conserved boundary

Unchanged: source SHA, frozen Q291 carrier `1aea888d8d576fc8606d56dd7a3b1a552411b8f8126ea27a54c36ff6d551dd7e`, structural preimage `151907b3163959d0eb5ebb020fa5253d33447362420e465600035744112fe5bc`, accepted physical expectation `9845c24da0c03adb4dfd65118b7c8c39a60a30337f33cc4177ffc6c848d02390`, EE-R6A/P2F2 source semantics `c7336ce479b8625b71e33743a05e43525c387dd50e4be1bb7af313667f9c341f`, R1E mapping authority `76e63b2af0bf0b9a53319a74d2ded099c9ac175de99935d0741ac52f68086670` and snapshot `0e98540cf6c4a1fa993cfc070a701368b3a7bfa99414d84e4119c2017dd67970`, P2F2 workload/grammar/frontier, canonical question mapping absence, and Lock2 `8e5842eb01100e0b23c3fa0fe85736fee081d759ec5458fc0f95c307024c6188`.

No source carrier, structural preimage, parentage, physical expectation, P2F2 workload, candidate grammar/frontier, or Lock2 was regenerated.

## Hostile court

GitHub Actions run 35578937508, job 106267056438, implementation SHA `1e2b64e9e520db9b9fbe7b42ab0170da6ba90725`: **35 passed**.

The court proves exact int/float physical-key distinction remains global, rejects generic coercion and nearby representations, admits only the two exact Q291 variables and nine exact native codes, keeps special states noncanonical and system missing separate, preserves the R1E ceiling and canonical-question absence, preserves non-WVS behavior, and exposes no candidate outputs.

## Stop law

R15/R16 were not run in this worker. Candidate A/B/C, I03, I05, measured P2X, and any WVS7 SAV/ZIP read were not run. The next lawful action is the R15/R16 retry against the reissued R6S projection.
