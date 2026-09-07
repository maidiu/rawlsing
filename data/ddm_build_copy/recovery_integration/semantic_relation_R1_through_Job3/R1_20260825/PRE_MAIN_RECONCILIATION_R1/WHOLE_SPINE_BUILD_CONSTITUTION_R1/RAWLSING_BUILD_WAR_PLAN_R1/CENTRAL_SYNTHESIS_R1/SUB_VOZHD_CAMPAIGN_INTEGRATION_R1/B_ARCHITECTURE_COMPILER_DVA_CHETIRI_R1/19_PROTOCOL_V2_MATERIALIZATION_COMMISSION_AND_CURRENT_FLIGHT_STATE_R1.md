# SUB-VOZHD B — PROTOCOL V2 MATERIALIZATION COMMISSION + CURRENT FLIGHT STATE R1

Status:
`HQ_CLASS_B_CURRENT__B11_PROTOCOL_V2_MATERIALIZATION_COMMISSIONED__NODE7_GATED_PENDING_PASS`

Campaign branch:
`agent/sub-vozhd-architecture-compiler-dva-chetiri-r1`

HQ consumption / materialization authorization:
`47241cc4f6407cc7c8c6750a04c9e405951882e9`

## Active worker

B11:
`AS3R3 NODE5A-R2 PROSPECTIVE MAPPING REPLAY PROTOCOL V2 MATERIALIZATION R1`

Branch:
`agent/rabochii-subv-b-as3r3-node5a-r2-prospective-mapping-protocol-v2-materialization-r1`

Starting HEAD:
`47241cc4f6407cc7c8c6750a04c9e405951882e9`

Handoff:
`d5e9baf18b1ea53cf76b6aa2f338bb3dd83329ac`

No competing prospective mapping-protocol-v2 materialization proof branch existed at commission time.

## Exact owned grain

B11 owns only:

`AS3R3_NODE5A_R2_PROSPECTIVE_MAPPING_REPLAY_PROTOCOL_V2_MATERIALIZATION`

It must:
- consume exact HQ protocol spec blob `befee68ee14f6e80e88cb3142947a37a7619fc5b`;
- consume exact frozen mapping carrier blob `26a7c35df2e6454c5e270a03b3571599bdf152fd`;
- commit exact serializer implementation;
- commit exact prospective payload bytes;
- seal the newly materialized prospective payload SHA-256;
- reproduce byte-identical payload output in at least two independent fresh processes;
- preserve all 19 rows, 18 successor predicates, and sole `{A000,A1RAPP}` alias;
- use zero serialization search / zero target fitting.

Historical digest:
`081e3b8594be3d9348bc0565cd9085cca1e999ae58ef7881f040d11f5da89c7e`

remains:
`IMMUTABLE_HISTORICAL_PROVENANCE__NONREPLAYABLE_AT_CURRENT_EVIDENCE_SURFACE`

and is not B11's target.

## PASS trigger

Expected terminal:

`AS3R3_NODE5A_R2_PROSPECTIVE_MAPPING_REPLAY_PROTOCOL_V2_MATERIALIZATION_COMPLETE__READY_FOR_NODE7_V2_RECOMMISSION`

On PASS:
1. inspect exact B11 return/write envelope;
2. verify serializer implementation was committed before qualifying fresh-process proofs;
3. verify exact prospective payload bytes/hash and process independence;
4. verify all 19 mapping rows/18 predicate identities/alias remain unchanged;
5. bank B11 into campaign;
6. campaign-adjudicate the materialized v2 payload identity and replay evidence;
7. recommission exactly ONE fresh Node7 replay under protocol v2.

B11 PASS does NOT itself close Node7.

## Blocker trigger

Expected terminal:

`AS3R3_NODE5A_R2_PROSPECTIVE_MAPPING_REPLAY_PROTOCOL_V2_MATERIALIZATION__EXACT_BLOCKER_PROVED`

If blocker:
- protocol/spec/carrier mismatch: freeze exact lane and prove mismatch;
- deterministic implementation defect inside B-owned evidence materialization: smallest exact repair only;
- semantic/canonical row drift: FAIL CLOSED; do not normalize away or mutate rows;
- new authority ambiguity: smallest HQ packet;
- sibling-owned dependency: exact cross-campaign packet only.

## Node7 prospective requirements after B11 PASS

The recommissioned Node7 must:
- execute at least two independent fresh constructor processes;
- reconstruct exact 19 predicate mappings;
- serialize those mappings under protocol v2 in each process;
- reproduce the same newly materialized v2 payload identity;
- reproduce exact 18 successor predicates;
- preserve sole `{A000,A1RAPP}` alias;
- reproduce exact 3 successor query identities;
- preserve all existing cardinality/order/terrain/canonical-object invariants;
- preserve historical digest as nonreplayable provenance;
- preserve historical Node6 seal:
  `df0395983de34996d33c258d0705cfc178df9cfe7982899431a0002c544481da`
  as historical comparison evidence only;
- emit a NEW VERSIONED PROSPECTIVE COMBINED REPLAY SEAL.

## D9 / OBL004 law current

`N025_DOES_NOT_SUPPLY_GENERIC_PRODUCTION_POSITIVE_SOURCE_COMPOSABILITY_LOAD`

`JURISDICTION_OR_API_EXISTENCE != POSITIVE_AUTHORITY_LOAD`

This does not block B11.

At any later exact B/OBL004 production structural operation + exact source-set grain, B must explicitly enumerate and positively bind each required P3 premise or fail closed.

## Current downstream chain

`B11 protocol-v2 materialization`
-> `Node7 prospective fresh combined replay`
-> `successor DiscoveryAuthority/frontier/replay seal`
-> `AS4I0 revalidation`
-> `independent hostile validation`
-> `OBL035 / C05R2B real LiTS-I I05`
-> `OBL036 / C08-G1`
-> `OBL037 only after OBL035 + OBL036 close`.

Hard gates remain:
- no OBL037 before OBL035 + OBL036;
- no OBL001 architecture selection by B;
- no OBL002 topology selection by B;
- no sibling-campaign work;
- no positive V3.

Terminal:
`SUB_VOZHD_B_B11_PROTOCOL_V2_MATERIALIZATION_COMMISSIONED__NODE7_GATED__OBL037_GATED`
