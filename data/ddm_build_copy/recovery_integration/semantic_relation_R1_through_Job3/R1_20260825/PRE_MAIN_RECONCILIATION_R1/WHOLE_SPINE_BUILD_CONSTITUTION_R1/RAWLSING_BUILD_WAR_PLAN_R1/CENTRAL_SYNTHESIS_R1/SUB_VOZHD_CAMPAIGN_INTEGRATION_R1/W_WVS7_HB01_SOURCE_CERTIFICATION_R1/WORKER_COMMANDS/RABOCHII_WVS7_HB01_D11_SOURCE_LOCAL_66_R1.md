# RABOCHII WVS7/HB01 — D11 SOURCE-LOCAL 66-SCOPE MATERIALIZATION R1

Repository:
`maidiu/rawlsing`

Worker branch:
`agent/rabochii-subv-w-hb01-wvs7-d11-source-local-66-r1`

Commissioning campaign branch:
`agent/sub-vozhd-wvs7-hb01-source-certification-r1`

Parent campaign HEAD before this command:
`f80cd38bf433ba3d46760f5eebb52de7ddc46d95`

Authorized grain:
`WVS7_D11_SOURCE_LOCAL_EMPIRICAL_UNIVERSE_66_SCOPE_MATERIALIZATION_ONLY`

## Canonical architecture authority

Source-local universe admission was adopted in canonical PRE-MAIN at:

`0712ef462e8c442231fb2071bc9a7ec2292c4b4e`

Exact implementation blob:

`rawlsing_next/pre553_source_local_universe_admission.py`
`b968fa16c6620cd06b191ebdb5da7da86f524393`

Qualification:

- governed CI run `34407835678`
- attempt 1: 44/44 bounded tests PASS
- attempt 2: 44/44 bounded tests PASS

The worker must consume this exact contract. It may copy the exact implementation blob onto its branch if the W campaign ancestry does not contain it. No local rewrite.

## Exact D12 authority

D12 worker tip:

`e404bc097f48a09265f1aec06e3d011a892f69c4`

Source:

- WVS Wave 7.sav
- SHA-256 `2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d`
- 97,220 rows
- 613 variables

Source-scope ledger:

`COUNTRY_SOURCE_SCOPE_ROW_RANGES.csv`

Exact Git blob:

`4875b9499dee06dfaa6dd6182656c3d55c2c4ce1`

Ledger SHA-256:

`cf0dfaae7a2f0f19b34ccc536b93e6aedbf37bf047d5d864e5c812fe9602d6a9`

Exact partition:

`S025_PLUS_B_COUNTR_PLUS_A_YEAR`

Scope count:

`66`

Row coverage:

`97,220 / 97,220 exactly once`

D12 replay ref:

- kind: `SCOPED_RESPONDENT_REPLAY`
- object ID: `urn:rawlsing:pre553:gsr07:wvs7:d12-scoped-respondent-replay:sha256:9d44d5097258b96c5c49faf968b85701f80ecd75df6b214a528abb6fb15ef44b`
- content hash: `9d44d5097258b96c5c49faf968b85701f80ecd75df6b214a528abb6fb15ef44b`

Identity law:

`SOURCE_SHA256_PLUS_SOURCE_ROW_ORDINAL`

D_INTERVIEW and S007 remain noncanonical respondent keys.

## Mission

Materialize exactly **66** source-local `EmpiricalUniverse@1.0.0` objects, one for every D12 source scope.

This is the source-local base lane.

It is independent of the population-certification/documentary lane.

No scope may be withheld merely because target/frame/design documentation is incomplete.

## Exact scope identity

For each row of the frozen D12 scope ledger, bind:

- S025
- B_COUNTR
- A_YEAR
- source_row_ordinal_first
- source_row_ordinal_last
- member_count
- ordered_member_binding_digest
- exact source_scope_member_set_ref
- exact source_scope_member_set_hash
- exact common source SHA
- exact common D12 replay ref

The source-local EmpiricalUniverse must preserve these as exact dependency/provenance material.

Do not map B_COUNTR/S025 to country labels by convention.

Do not infer geopolitical hierarchy.

Source-native codes are sufficient for source-local identity.

## Source-local admission authority

Mint exactly one source-local admission AuthoritySnapshot per D12 scope under the canonical contract.

Each must:

- be `ALLOW`;
- authority kind `SOURCE_SEMANTICS_TOPOLOGY`;
- govern operation `SOURCE_LOCAL_EMPIRICAL_UNIVERSE_ADMISSION_R1`;
- govern `EmpiricalUniverse@1.0.0`;
- bind exact WVS7 source artifact ref;
- bind exact scope member-set ref;
- bind exact D12 replay ref;
- carry all four required negative limits;
- depend on the exact D12 scope/replay/source determinants.

The authority is limited to source-local scope existence.

It does not certify the population.

## Documentary fields

For R1 source-local base materialization:

- preserve population/documentary authority in its existing separate D11/documentary artifacts;
- do not require those artifacts to mint the source-local base;
- use explicit `NOT_POPULATION_CERTIFIED` source-local documentary fields unless exact preserved documentary content is deliberately imported with its exact provenance.

It is lawful for all 66 source-local objects to carry `NOT_POPULATION_CERTIFIED` at this base layer while the population overlay remains separate.

This does not withdraw or supersede the old three population-certified D11 universes.

## Exact negative limits

Every object must remain bounded by:

- `NO_POPULATION_GENERALIZATION`
- `NO_WEIGHTED_POPULATION_ESTIMAND_UNLESS_SEPARATELY_AUTHORIZED`
- `NO_CROSS_UNIVERSE_POOLING_WITHOUT_RELATION_AUTHORITY`
- `NO_NEAREST_COUNTRY_OR_WAVE_BACKFILL`

## Required output

Bank under:

`.../W_WVS7_HB01_SOURCE_CERTIFICATION_R1/WORKER_RETURNS/D11_SOURCE_LOCAL_66_R1/`

At minimum:

- exact imported D12 compact scope ledger;
- exact imported D12 compact replay manifest;
- `BUILD_D11_SOURCE_LOCAL_66.py`;
- `SOURCE_LOCAL_ADMISSION_AUTHORITIES.json`;
- `SOURCE_LOCAL_EMPIRICAL_UNIVERSES.json`;
- `SOURCE_LOCAL_66_REPLAY_PARITY_RECEIPT.json`;
- `RESULT.md`;
- `RESULT.json`;
- `CHANGED_FILES.txt`.

## Qualification

Freeze the materializer before qualifying runs.

Run it at least twice in genuinely separate Python processes.

Require exact byte parity for:

- 66 admission authorities;
- 66 EmpiricalUniverse objects;
- output object refs;
- output file SHA-256 identities;
- aggregate scope/member counts.

Required invariants:

- exactly 66 universes;
- exactly 66 source-local admission authorities;
- exactly 97,220 total scope members;
- zero duplicate D12 scope refs;
- zero missing D12 scope refs;
- zero population-generalization permissions;
- zero weighted-population permissions;
- zero source-relation/pooling permissions;
- zero backfill/harmonization permissions;
- all 66 validate under canonical source-local admission R1;
- every universe is a valid C11 public carrier object under its exact authority registry.

## Population lane hard boundary

Do not alter:

- old D11 3/66 population-certified objects;
- three-partial documentary recovery results;
- D03 routing;
- weights;
- C05;
- GSR07;
- HB05/HB06/HB07/C09;
- V3/PFF.

PASS target:

`WVS7_D11_SOURCE_LOCAL_66_COMPLETE__97220_RESPONDENTS_COVERED__POPULATION_CERTIFICATION_SEPARATE__READY_FOR_SUB_VOZHD_W_TWO_LANE_JOIN`

Blocker target:

`WVS7_D11_SOURCE_LOCAL_66__EXACT_BLOCKER_PROVED`
