# FFP014 — R5 CURRENT RESPONDENT ADMISSION VIA Q73A WITNESS R1

Status: `PASS__CURRENT_R5_RESPONDENT_EXECUTION_BINDING_PACKAGE_ADMITTED__Q73D_EXPOSURE_REMAINS_UNRESOLVED`

## Dispositive admission

Under Global HQ commission `FFC001` at `d3e93ab491dbbdc1763c019f44992b6884456b5b`, this worker admits one bounded `CURRENT_RESPONDENT_EXECUTION_BINDING_PACKAGE` for exact Afrobarometer R5 respondent execution using Q73A. The admission is not a claim that every R5 qimpl has resolved respondent exposure.

`CURRENT_R5_RESPONDENT_EXECUTION_BINDING_PACKAGE = ADMITTED__BOUNDED_Q73A`

`Q73D / RESPONDENT_HAS_PAID_EMPLOYMENT = EXPOSURE_BINDING_UNRESOLVED`

`UNRESOLVED_Q73D != GLOBAL_CARRIER_BLOCKER_FOR_SEPARATELY_PROVED_Q73A`

The last statement is only the disposition of this exact package. It is not a generalized doctrine that unresolved qimpl exposure is harmless. Any unresolved measurement is barred from an empirical claim requiring that measurement's exposure.

## Exact current carrier

A new logical current carrier identity is issued over the already byte-validated FFP008 physical respondent member rather than re-running the 51,587-row reconstruction for ceremony:

- carrier schema/version: `FFP014_R5_CURRENT_RESPONDENT_CARRIER@1`
- respondent carrier identity: `sha256:6c2277e8832c8f070d1213f8f68adf54f115e4978f59702d150ab69fffd4a6d5`
- physical member SHA-256: `f55741a53a4caed3f74980afba2488233caa93dd4f1a2edcfde8d90e2fcce4be`
- logical uncompressed member SHA-256: `dd2f12232270d872405ffe4d8111540168b672aa1c9b88cac7c44ee3be13cfd7`
- rows: `51,587`
- stable Library ref: `libfile_23bfb6d5340881918ac372b6b8b4cf3b`
- Library file snapshot: `file_000000005d6881f6aa1501897a52c40f`
- post-upload rematerialize/byte comparison: `PASS`

The new logical identity is necessary because FFP008's provisional root mixed valid respondent/source reconstruction with the unadmitted Q73D paid-employment semantic edge. FFP014 does not promote that root. It reuses only the exact physical member and the lawful reconstruction subset, under a new current admission manifest with Q73D quarantined.

## Exact source and reconstruction ancestry

- source: `Data/Afro Barometer Round 5.sav`
- SHA-256: `c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651`
- bytes: `49,689,458`
- rows: `51,587`
- source family/wave: `Afrobarometer / R5`
- reconstruction-code SHA-256: `ca0afd16475d9cabfbcac8b09ad68612c8ced680a3bb3051f9b1ea8a828ce774`
- respondent key: `(COUNTRY, RESPNO)`
- unique source/carrier keys: `51,587`
- duplicates: `0`
- row order is identity: `NO`

The reconstruction-code reuse ceiling is explicit: source decoding, exact source-key identity, raw source projection, and deterministic serialization are reused; FFP008's Q96→`RESPONDENT_HAS_PAID_EMPLOYMENT` mapping and all Q73D exposure products are not admitted.

## Q73A exact lawful chain

`question_impl.phase0.cae005624221d7b00dd2`

`-> Afrobarometer:R5:Q73A`

`-> current carrier respondent identified by (carrier_identity, respondent_local_id) from governed (COUNTRY, RESPNO)`

`-> COUNTRY_ALPHA3 from the first three exact source characters of that same respondent's RESPNO, with complete functional validation against source COUNTRY`

`-> C04P.b651b9af6671a2fe1166`

`-> COUNTRY_ALPHA3 NOT IN {ALG,EGY,MRC,SUD,TUN}`

`-> EXPOSED__PROVED / NONEXPOSURE__PROVED under the exact native Q73A not-asked/asked administration rule`

`-> independently joined Q73A source response fact`

Q73A exact current identity SHA-256 is `cae005624221d7b00dd2e8dcc31a8c73d2d4f1446a06d428ab40f1ee2809ad14`. FFP007 selects it and C04 binds it one-to-one to R5 source variable Q73A with `POSITIVE_EXECUTABLE_ROUTING_AUTHORITY` and native-primary evidence.

## COUNTRY_ALPHA3 provenance

No country label was informally translated into the C04 token. At the exact starting HEAD, `data/ddm_build_copy/manifests/country_source_mapping_registry.csv` governs the R5 source's numeric `COUNTRY` values against the exact source SHA. FFP014 then checks the source-native respondent-key token directly: for every one of the 51,587 `(COUNTRY,RESPNO)` rows, `RESPNO[0:3]` is functional within `COUNTRY`; for raw `COUNTRY` values `31,32,33,34,35`, those exact source tokens are respectively `ALG,EGY,MRC,SUD,TUN`, exactly the five tokens named by the Q73A C04 predicate. This bounded expression is admitted only for Afrobarometer R5 Q73A routing; it is not a global country ontology or ISO conversion rule.

## Deterministic Q73A execution

FFP014 builder SHA-256: `6a80c05d452669bd3123789de12cf9ca8f9c293386d0ed669f3a5682856f1687`.

Results across the complete admitted respondent key set:

- `EXPOSED__PROVED`: `45,598`
- `NONEXPOSURE__PROVED`: `5,989`
- `EXPOSURE__UNRESOLVED`: `0`

The excluded-country count is exactly the source-native Q73A `997=Not asked` count: `5,989`. This agreement is validation only; response state was not used to compute exposure.

The independent response sidecar contains all 51,587 Q73A response facts and deliberately contains no predicate or exposure field. The exposure sidecar contains the predicate input/result/exposure and deliberately contains no Q73A response field.

- response sidecar SHA-256: `ad62093fbc98eb7453a72015cc0fccdee9578379e46d8a9f35d64d99d5efa39d`
- response semantic sorted root: `f52d81e5286b60aecad6c12c6b59c7e124f0138d513b8eafcfb692eca44c6a94`
- response Library ref: `libfile_3195f7a5f158819189b63f28b1e8c49c`
- exposure sidecar SHA-256: `2ff4e74a3fc04a49da95925b02dad7865384f896849b4309c06f92464a85a3bf`
- exposure semantic sorted root: `e8bcd698b8d93401a85bd4e39d4ba1056a2ee5871da2fab9ad256210cb6e2aac`
- exposure Library ref: `libfile_0335c485ec6081918e15b4c3f2cd3ec5`
- both post-upload byte rechecks: `PASS`
- cold deterministic replay from the materialized Library base member: `PASS__BYTE_IDENTICAL`

Bounded positive witness after deterministic serialization sort (sorting is not identity): `(COUNTRY=1, RESPNO=BEN0002)` -> `COUNTRY_ALPHA3=BEN` -> predicate `TRUE` -> `EXPOSED__PROVED`; independent Q73A source response is `1`.

Hostile missing-response witness: `(COUNTRY=1, RESPNO=BEN0001)` has Q73A state `9` but the same independent administration chain proves `EXPOSED__PROVED`. Missing/non-substantive response therefore does not become nonexposure.

## FFP008 preservation

FFP008 remains fully binding at its negative edge:

`question_impl.phase0.391123a4e7d3c8f0fd3b / C04P.f751f53c113a339f2cb8 / RESPONDENT_HAS_PAID_EMPLOYMENT = EXPOSURE_BINDING_UNRESOLVED`

No Q96 mapping is promoted. No Q73D exposure receipt is admitted. Q73D cannot enter a claim that requires respondent-level Q73D exposure until its exact governed predicate-input binding is separately closed.

## Acceptance / ceiling

All 16 FFX001-D hostile acceptance fixtures pass at this bounded package grain; exact dispositions are in `04_HOSTILE_ACCEPTANCE_RECEIPT.tsv`. The admission receipt is `sha256:1a01cf216a4c70ffe9e9663ea8dd77381b2aecf8bea2d59c5853c234955ca244`.

This act performs no PRA, CIM, CITC, or FFX002 execution. It does not close all R5 exposure bindings, FIELD FORGE globally, P3, or OBL040.

`PASS__CURRENT_R5_RESPONDENT_EXECUTION_BINDING_PACKAGE_ADMITTED__Q73D_EXPOSURE_REMAINS_UNRESOLVED`
