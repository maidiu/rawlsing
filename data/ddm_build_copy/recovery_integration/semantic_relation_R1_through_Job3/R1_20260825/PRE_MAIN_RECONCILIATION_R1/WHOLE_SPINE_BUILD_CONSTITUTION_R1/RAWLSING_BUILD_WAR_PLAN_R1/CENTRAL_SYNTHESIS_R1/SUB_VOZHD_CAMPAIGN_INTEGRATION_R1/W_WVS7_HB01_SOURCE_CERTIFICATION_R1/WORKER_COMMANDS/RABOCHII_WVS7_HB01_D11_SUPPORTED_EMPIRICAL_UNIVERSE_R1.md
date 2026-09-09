# RABOCHII WVS7/HB01 — D11 SUPPORTED EMPIRICAL UNIVERSE MATERIALIZATION R1

Repository: `maidiu/rawlsing`

Worker branch:
`agent/rabochii-subv-w-hb01-wvs7-d11-supported-empirical-universe-r1`

Commissioning campaign:
`agent/sub-vozhd-wvs7-hb01-source-certification-r1`

Commission only after the D03/D12 PASS:
`e404bc097f48a09265f1aec06e3d011a892f69c4`

## Exact authority ceiling

Materialize `EmpiricalUniverse@1.0.0` objects for exactly these documentary-full source scopes:

1. Australia 2018 — source scope `S025=362018; B_COUNTR=36; A_YEAR=2018`
2. United Kingdom - Great Britain 2022 — `S025=8262022; B_COUNTR=826; A_YEAR=2022`
3. United Kingdom - Northern Ireland 2022 — `S025=9092022; B_COUNTR=909; A_YEAR=2022`

No EmpiricalUniverse object may be minted for any of the other 63 WVS7 source scopes.

## Immutable consumed authority

- source SAV SHA-256:
  `2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d`
- D12 replay ref hash:
  `9d44d5097258b96c5c49faf968b85701f80ecd75df6b214a528abb6fb15ef44b`
- D12 exact scope ledger SHA-256:
  `cf0dfaae7a2f0f19b34ccc536b93e6aedbf37bf047d5d864e5c812fe9602d6a9`
- accepted country documentary inventory:
  `930d89b8930c21c9a8f1180093ee15ed10c495e4`
- accepted W6 GB/NI positive documentary recovery:
  `471b64953b58cd39baf9368358ef782c6308957c`
- accepted fail-closed HQ join:
  `efca0824b87415b9a99991b989eb0c8334cdcd9d`
- W6R4 no-change preservation return:
  `72f9ec8c5a10112bb9540e92b6c5cdd305845b96`

## Exact positive documentary material

### Australia 2018

Target population:
`Adults 18+ resident in private households in Australia`

Frame:
`Address-based sampling; mail primary contact`

Actual design:
`Sequential mixed-mode; self-completion online/paper; fieldwork 2018-04-03 through 2018-08-06; N=1813; response=30.2%`

Accepted source-owner provenance includes:
- WVSA Australia analytical report release;
- WVSA Australia ACSPRI methodology presentation;
- the accepted R2C Australia documentary row and HQ full-universe disposition.

### Great Britain 2022

Target:
`Adult population age 18+ in Great Britain (England, Scotland and Wales). No groups excluded or under-represented; Scotland and Wales intentionally over-represented for analysis, with post-survey weighting for national representativeness.`

Frame:
`Royal Mail Postcode Address File (PAF), Small User version, excluding high-volume business addresses.`

Actual design:
`Two-stage address probability sample: stratified random PPS selection of postcode sectors, then 30 addresses per selected sector from PAF; one adult age 18+ randomly selected within participating household.`

Positive design detail:
`273 postcode sectors in Great Britain; 56 in Scotland and 45 in Wales. Stratifiers: country/region, population-density tertiles, percentage owner-occupied. Rare multi-household addresses randomly subsampled electronically.`

### Northern Ireland 2022

Target:
`Entire adult population age 18+ of Northern Ireland; no groups excluded, over-represented, or under-represented.`

Frame:
`Royal Mail Postcode Address File (PAF), Small User version, excluding high-volume business addresses.`

Actual design:
`Two-stage address probability sample: stratified random PPS selection of postcode sectors, then 30 addresses per selected sector from PAF; one adult age 18+ randomly selected within participating household.`

Positive design detail:
`45 postcode sectors, 30 addresses each. Stratifiers: population-density tertiles and percentage owner-occupied. Rare multi-household addresses randomly subsampled electronically.`

## Object law

Use the exact PRE553 `AuthoritySnapshot@1.0.0` and `EmpiricalUniverse@1.0.0` canonical identity law from `rawlsing_next/pre553_empirical_objects.py`.

For each supported source scope:

1. materialize one exact positive country-universe documentary `AuthoritySnapshot` whose content is limited to the accepted positive target/frame/design facts above and exact evidence refs;
2. materialize one `EmpiricalUniverse` with typed state `UNIVERSE_IDENTIFIED`;
3. bind its respondent namespace to the exact D12 source-scope member-set ref;
4. bind source lineage to exact source SHA + exact row ordinal interval + D12 replay ref;
5. preserve `canonical_wave_if_governed=null` unless an exact separate canonical-wave authority is already present;
6. set no source-relation refs unless an exact accepted relation authority exists;
7. create no weight, estimand, design-variance, routing, query, fact, or C11 objects.

The exact three row intervals and source-scope member-set refs must be consumed from the D12 ledger, not reconstructed from country labels.

## Replay court

Run the exact D11 materializer at least twice in genuinely separate processes.

PASS requires:
- exactly 3 AuthoritySnapshots;
- exactly 3 EmpiricalUniverse objects;
- exact object/ref parity across both executions;
- zero universe objects for the remaining 63 source scopes;
- exact source-scope member-set linkage;
- no canonical D_INTERVIEW/S007 use;
- no source relation default;
- no missingness/incidence/complement inference.

## Required outputs

Bank under:
`.../W_WVS7_HB01_SOURCE_CERTIFICATION_R1/WORKER_RETURNS/D11_SUPPORTED_EMPIRICAL_UNIVERSE_R1/`

At minimum:
- `RESULT.md`
- `RESULT.json`
- `COUNTRY_UNIVERSE_AUTHORITY_SNAPSHOTS.json`
- `EMPIRICAL_UNIVERSE_OBJECTS.json`
- `D11_REPLAY_PARITY_RECEIPT.json`
- `BUILD_D11_SUPPORTED_UNIVERSES.py`
- `CHANGED_FILES.txt`

## Hard stops

- do not mint a fourth universe;
- do not infer target/frame/design for any unresolved or partial country;
- do not infer person-position routing;
- no GSR07 full court;
- no C05 parity;
- no C09;
- no HB05/HB06/HB07;
- no architecture selection;
- no positive V3.

PASS terminal:
`WVS7_D11_SUPPORTED_EMPIRICAL_UNIVERSE_MATERIALIZATION_COMPLETE__3_OF_66_ACCEPTED__63_PRESERVED_FAIL_CLOSED__READY_FOR_SUB_VOZHD_W_JOIN`
