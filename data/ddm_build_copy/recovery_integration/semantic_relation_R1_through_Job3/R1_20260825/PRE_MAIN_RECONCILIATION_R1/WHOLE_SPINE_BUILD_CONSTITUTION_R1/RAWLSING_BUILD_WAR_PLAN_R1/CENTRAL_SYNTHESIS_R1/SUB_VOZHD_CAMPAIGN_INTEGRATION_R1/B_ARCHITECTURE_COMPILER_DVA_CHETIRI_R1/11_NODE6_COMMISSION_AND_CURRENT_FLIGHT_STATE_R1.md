# SUB-VOZHD B — NODE6 COMMISSION + CURRENT FLIGHT STATE R1

Status:
`NODE5B_BANKED_AND_ACCEPTED__NODE6_COMBINED_SUCCESSOR_RUNTIME_SEAL_COMMISSIONED__OBL035_SUCCESSION_CHAIN_ACTIVE`

Campaign branch:
`agent/sub-vozhd-architecture-compiler-dva-chetiri-r1`

Node5B bank merge:
`be3a4501c41f18793e59341249be64afacc10bbf`

Node5B adjudication:
`25b6dd7e3dc2d28e06a554e5db78ea19813acc67`

## Active worker

B8:
`AS3R3 NODE6 COMBINED SUCCESSOR RUNTIME SEAL R1`

Branch:
`agent/rabochii-subv-b-as3r3-node6-combined-successor-runtime-seal-r1`

Starting HEAD:
`25b6dd7e3dc2d28e06a554e5db78ea19813acc67`

Handoff:
`84522c995706d4cbbca2295a63755c95a656c203`

No competing Node6/combined-successor-runtime-seal proof branch existed at commission time.

## Owned proof

B8 seals already-committed successor runtime evidence only:
- 18 distinct successor predicates;
- 3 distinct successor queries;
- 21 distinct successor canonical runtime objects total;
- 22 historical AS3R2 -> successor succession rows;
- sole duplicate successor target only for `{A000,A1RAPP}`;
- deterministic predicate/query/combined runtime aggregate hashes;
- full semantic-terrain invariance.

B8 invokes zero constructors and remints zero runtime objects.

Historical predecessor refs come only from:
`aae978928d2416c23d6b1562e7ac559b106b2cf7`
/
`AS3R2_CHETIRI_FINAL_MANIFEST_SEAL_20260827/04_RUNTIME_CATALOG_BINDING_MANIFEST.json`
blob:
`c3e95d0705d70537e27874eaad81e9fdf76f11b7`.

## PASS trigger

Expected:
`AS3R3_NODE6_COMBINED_SUCCESSOR_RUNTIME_SEAL_COMPLETE__READY_FOR_NODE7_FRESH_COMBINED_REPLAY`

On PASS:
1. inspect exact B8 return/write envelope;
2. bank evidence into B;
3. adjudicate Node6;
4. commission exactly one Node7 fresh combined replay worker;
5. Node7 must reconstruct from frozen producer + Node4A/Node4B inputs and reproduce successor identities/aggregate hashes independently.

Do not jump directly from Node6 to DiscoveryAuthority/frontier/replay.

## Blocker trigger

Expected:
`AS3R3_NODE6_COMBINED_SUCCESSOR_RUNTIME_SEAL__EXACT_BLOCKER_PROVED`

If the blocker exposes:
- missing committed canonical bytes: fail closed, do not remint inside Node6;
- old/new row mismatch: preserve exact historical/current identities and court the smallest cardinality/provenance defect;
- B-owned deterministic packaging defect: smallest exact B repair;
- sibling-owned authority dependency: exact cross-campaign packet only;
- trajectory/authority ambiguity: smallest HQ packet.

## Remaining chain

`Node6 combined successor runtime seal`
-> `Node7 fresh combined replay`
-> `successor DiscoveryAuthority/frontier/replay seal`
-> `AS4I0 revalidation + independent hostile validation`
-> `OBL035 / C05R2B`
-> `OBL036 / C08-G1`
-> `OBL037 equal-governed-workload bakeoff`.

OBL037 remains forbidden before OBL035 and OBL036 close.

OBL037 baseline remains:
- identical source/carrier obligations across A/B/C;
- zero deletion credit;
- zero cutover credit;
- zero retirement credit.

Terminal:
`SUB_VOZHD_B_NODE6_COMMISSIONED__OBL035_CHAIN_ACTIVE__OBL037_STILL_GATED`
