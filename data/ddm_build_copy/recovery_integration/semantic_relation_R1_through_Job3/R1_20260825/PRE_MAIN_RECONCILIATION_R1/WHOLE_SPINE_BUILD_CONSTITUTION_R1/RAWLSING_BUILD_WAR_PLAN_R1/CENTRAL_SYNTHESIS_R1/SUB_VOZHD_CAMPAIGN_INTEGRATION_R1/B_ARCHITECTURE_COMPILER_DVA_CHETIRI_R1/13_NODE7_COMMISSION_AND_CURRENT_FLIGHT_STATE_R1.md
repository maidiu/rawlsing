# SUB-VOZHD B — NODE7 COMMISSION + CURRENT FLIGHT STATE R1

Status:
`NODE6_BANKED_AND_ACCEPTED__NODE7_FRESH_COMBINED_REPLAY_COMMISSIONED__OBL035_SUCCESSION_CHAIN_ACTIVE`

Campaign branch:
`agent/sub-vozhd-architecture-compiler-dva-chetiri-r1`

Node6 bank merge:
`c365d11807c7761650e83e13f53f77c6fb24b320`

Node6 adjudication:
`08313b07afd01a1abe159a06f62f5e7b674dc683`

## Active worker

B9:
`AS3R3 NODE7 FRESH COMBINED REPLAY R1`

Branch:
`agent/rabochii-subv-b-as3r3-node7-fresh-combined-replay-r1`

Starting HEAD:
`08313b07afd01a1abe159a06f62f5e7b674dc683`

Handoff:
`d4f29d97204851c9f99d4f64a1abc9c883d0dec8`

No competing Node7/fresh-combined-replay proof branch existed at commission time.

## Owned proof

B9 must execute at least two independent fresh-process reconstructions from:
- frozen producer;
- exact Node4A predicate inputs;
- exact Node4B query inputs;
- historical AS3R2 predecessor manifest for crosswalk construction.

Per fresh process:
- predicate constructor calls = 19;
- query constructor calls = 3;
- mapping results = 22;
- distinct canonical successor objects = 21;
- distinct predicates = 18;
- distinct queries = 3;
- sole predicate alias = `{A000,A1RAPP}`;
- query aliases = 0.

It must reproduce the committed Node5A-R2, Node5B, and Node6 identity/hash targets exactly, including Node6 combined seal:
`df0395983de34996d33c258d0705cfc178df9cfe7982899431a0002c544481da`.

## PASS trigger

Expected:
`AS3R3_NODE7_FRESH_COMBINED_REPLAY_COMPLETE__READY_FOR_SUCCESSOR_DISCOVERY_AUTHORITY_FRONTIER_REPLAY_SEAL`

On PASS:
1. inspect exact B9 return/write envelope;
2. bank lawful evidence into B;
3. adjudicate Node7;
4. commission exactly one successor DiscoveryAuthority/frontier/replay seal worker;
5. do not jump directly to AS4I0 or C05R2B.

## Blocker trigger

Expected:
`AS3R3_NODE7_FRESH_COMBINED_REPLAY__EXACT_BLOCKER_PROVED`

If blocker is:
- deterministic B-owned replay/package defect: smallest exact B repair;
- identity/cardinality anomaly: fail closed and court exact anomaly; do not force uniqueness;
- missing sibling-owned authority: exact cross-campaign dependency only;
- new trajectory/authority ambiguity: smallest HQ packet.

## Remaining chain

`Node7 fresh combined replay`
-> `successor DiscoveryAuthority/frontier/replay seal`
-> `AS4I0 revalidation + independent hostile validation`
-> `OBL035 / C05R2B`
-> `OBL036 / C08-G1`
-> `OBL037 equal-governed-workload bakeoff`.

OBL037 remains forbidden until OBL035 and OBL036 close.

OBL037 baseline remains:
- identical source/carrier obligations across A/B/C;
- zero deletion credit;
- zero cutover credit;
- zero retirement credit.

Terminal:
`SUB_VOZHD_B_NODE7_COMMISSIONED__OBL035_CHAIN_ACTIVE__OBL037_STILL_GATED`
