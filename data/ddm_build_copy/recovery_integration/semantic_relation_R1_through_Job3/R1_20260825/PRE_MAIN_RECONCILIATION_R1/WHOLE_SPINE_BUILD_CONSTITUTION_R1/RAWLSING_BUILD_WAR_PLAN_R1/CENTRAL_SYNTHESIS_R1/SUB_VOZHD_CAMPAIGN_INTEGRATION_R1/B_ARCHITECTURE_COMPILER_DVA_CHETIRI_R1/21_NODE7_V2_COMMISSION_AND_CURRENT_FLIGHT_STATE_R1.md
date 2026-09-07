# SUB-VOZHD B — NODE7-V2 COMMISSION + CURRENT FLIGHT STATE R1

Status:
`B11_BANKED_AND_ACCEPTED__NODE7_V2_PROSPECTIVE_FRESH_REPLAY_COMMISSIONED__OBL035_CHAIN_ACTIVE`

Campaign branch:
`agent/sub-vozhd-architecture-compiler-dva-chetiri-r1`

B11 bank merge:
`622f0a99d14d3712400bdb4748b4de162a3dcf1f`

B11 adjudication / Node7-v2 authorization:
`5102733daa1dd341e06a12f998989c2fe58b397f`

## Active worker

B12:
`AS3R3 NODE7-V2 PROSPECTIVE FRESH COMBINED REPLAY R1`

Branch:
`agent/rabochii-subv-b-as3r3-node7-v2-prospective-fresh-combined-replay-r1`

Starting HEAD:
`5102733daa1dd341e06a12f998989c2fe58b397f`

Handoff:
`1d07a9c864542fea58b5a1536a017d035e968527`

No competing Node7-v2/prospective-fresh-combined-replay branch existed at commission time.

## Current prospective replay target

Protocol:
`AS3R3_NODE5A_R2_MAPPING_REPLAY_PROTOCOL@2.0.0`

Protocol spec Git blob:
`befee68ee14f6e80e88cb3142947a37a7619fc5b`

Committed B11 serializer:
- Git blob:
  `29b61fc7fef8db06e4ba95fedc788a20b8d28d5e`;
- SHA-256:
  `47307828a471cc525643f870c32ac15efa26565f063191d50ea32c48c72994b6`.

Current prospective mapping payload:
- Git blob:
  `d62847e9972362bf2fcaeac515360cd5cf99eab7`;
- SHA-256:
  `06f874df6bdd2e621886f748c8aa12397533e273649f99e654dc3779b5eb59db`;
- byte length:
  `12364`.

Historical mapping digest:
`081e3b8594be3d9348bc0565cd9085cca1e999ae58ef7881f040d11f5da89c7e`

remains:
`IMMUTABLE_HISTORICAL_PROVENANCE__NONREPLAYABLE_AT_CURRENT_EVIDENCE_SURFACE`.

Historical Node6 seal:
`df0395983de34996d33c258d0705cfc178df9cfe7982899431a0002c544481da`

remains:
`ACCEPTED_HISTORICAL_COMPARISON_EVIDENCE__NOT_PROSPECTIVE_REPLAY_TARGET`.

## B12 exact duty

At least two genuinely independent fresh processes must each:
- execute 19 predicate constructor calls;
- reconstruct 19 mapping rows from actual Node4A inputs + fresh predicate outputs;
- serialize those rows under protocol v2;
- reproduce `06f874df...`;
- obtain exactly 18 distinct predicates;
- preserve sole A000/A1RAPP alias;
- execute exactly 3 query constructor calls;
- reproduce exact 3 successor queries;
- preserve all 21 successor canonical object identities/representations;
- preserve all cardinality/order/terrain invariants.

Both fresh processes must emit byte-identical deterministic prospective replay realization payloads.

B12 then emits a NEW:

`AS3R3_NODE7_PROSPECTIVE_COMBINED_REPLAY_SEAL@2.0.0`

whose SHA-256 is discovered only after lawful fresh replay.

B12 must NOT claim exact reproduction of historical Node6 seal.

## PASS trigger

Expected:

`AS3R3_NODE7_V2_PROSPECTIVE_FRESH_COMBINED_REPLAY_COMPLETE__READY_FOR_SUCCESSOR_DISCOVERY_AUTHORITY_FRONTIER_REPLAY_SEAL`

On PASS:
1. inspect exact B12 branch/write envelope;
2. verify replay driver committed before qualifying runs;
3. verify two-process independence and exact constructor counts;
4. verify v2 payload reproduction;
5. verify all semantic/canonical/cardinality/terrain invariants;
6. verify historical/prospective separation;
7. verify the NEW versioned prospective combined replay seal;
8. bank B12;
9. campaign-adjudicate it;
10. commission exactly one successor DiscoveryAuthority/frontier/replay seal worker.

Do not jump directly to AS4I0 or C05R2B.

## Blocker trigger

Expected:

`AS3R3_NODE7_V2_PROSPECTIVE_FRESH_COMBINED_REPLAY__EXACT_BLOCKER_PROVED`

On blocker:
- deterministic B-owned execution/proof defect -> smallest exact repair;
- semantic/canonical/cardinality drift -> fail closed; do not mutate identities;
- protocol-v2 mismatch -> fail closed at exact protocol grain;
- sibling-owned dependency -> exact cross-campaign packet only;
- new authority ambiguity -> smallest HQ packet.

## Remaining chain

`Node7-v2 prospective fresh combined replay`
-> `successor DiscoveryAuthority/frontier/replay seal`
-> `AS4I0 revalidation`
-> `independent hostile validation`
-> `OBL035 / C05R2B real LiTS-I I05`
-> `OBL036 / C08-G1`
-> `OBL037 only after OBL035 + OBL036 close`.

## D9 / OBL004 law current

`N025_DOES_NOT_SUPPLY_GENERIC_PRODUCTION_POSITIVE_SOURCE_COMPOSABILITY_LOAD`

`JURISDICTION_OR_API_EXISTENCE != POSITIVE_AUTHORITY_LOAD`.

No generic-positive composability authority is inferred.

## Hard gates

- no OBL037 before OBL035 + OBL036;
- no OBL001 architecture selection by B;
- no OBL002 topology selection by B;
- no sibling-campaign work;
- no positive V3.

Terminal:
`SUB_VOZHD_B_NODE7_V2_COMMISSIONED__OBL035_CHAIN_ACTIVE__OBL037_GATED`
