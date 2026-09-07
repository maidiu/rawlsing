# SUB-VOZHD B — B10 COMMISSION + CURRENT FLIGHT STATE R1

Status:
`B9_BLOCKER_BANKED_AND_ACCEPTED__B10_MAPPING_PAYLOAD_EVIDENCE_REPAIR_COMMISSIONED__NODE7_FROZEN`

Campaign branch:
`agent/sub-vozhd-architecture-compiler-dva-chetiri-r1`

B9 bank merge:
`10cf2539d58303ba3e2d42809ac5e00afbe04a0d`

B9 blocker adjudication / repair authorization:
`b344dc20f58be182ca9657049fa07e0eae85ab7e`

## Active worker

B10:
`AS3R3 NODE5A-R2 MAPPING PAYLOAD EVIDENCE REPAIR R1`

Branch:
`agent/rabochii-subv-b-as3r3-node5a-r2-mapping-payload-evidence-repair-r1`

Starting HEAD:
`b344dc20f58be182ca9657049fa07e0eae85ab7e`

Handoff:
`7e2a969c9dc7fad3ac774fc3bfc87c4fab6f8ac9`

No competing repair branch existed at commission time.

## Exact blocker being repaired

Node7 requires fresh reproduction of accepted Node5A-R2 mapping payload digest:

`081e3b8594be3d9348bc0565cd9085cca1e999ae58ef7881f040d11f5da89c7e`.

Committed Node5A-R2 material includes:
- exact 19-row mapping crosswalk;
- digest;
- canonical predicate payload;
- alias payload;

but does not include:
- exact mapping payload bytes;
- executable helper producing those bytes;
- adopted deterministic mapping-payload serialization law.

Target-hash fitting is forbidden.

## B10 PASS trigger

Expected:
`AS3R3_NODE5A_R2_MAPPING_PAYLOAD_EVIDENCE_REPAIR_COMPLETE__READY_FOR_NODE7_RECOMMISSION`

PASS means B10 has independently recovered either:
- the exact original payload byte preimage; or
- the exact original deterministic serialization law,

and only after that recovery verified the bytes hash to `081e3b...`.

On PASS:
1. inspect B10 provenance and no-target-fitting evidence;
2. bank B10;
3. campaign-adjudicate recovered evidence as supplemental Node5A-R2 replay protocol evidence;
4. freeze recovered preimage/law for Node7 consumption;
5. recommission exactly one Node7 fresh combined replay;
6. Node7 must still execute two genuinely independent fresh constructor processes and reproduce Node5A/Node5B/Node6 targets.

B10 PASS is NOT Node7 PASS.

## B10 irrecoverable trigger

Expected:
`AS3R3_NODE5A_R2_MAPPING_PAYLOAD_EVIDENCE_REPAIR__IRRECOVERABLE_PROTOCOL_BLOCKER`

Then SUB-VOZHD B shall:
1. inspect and bank the exact irrecoverability proof;
2. freeze Node7;
3. emit only:
   `READY_FOR_VOZHD_HQ_ADJUDICATION__NODE5A_R2_MAPPING_REPLAY_PROTOCOL_IRRECOVERABLE`;
4. ask HQ for the smallest lawful disposition of the replay-evidence protocol;
5. do not alter semantic identities or Node6 seal merely to avoid evidence incompleteness.

## Current frozen downstream chain

`B10 mapping evidence repair`
-> `Node7 fresh combined replay`
-> `successor DiscoveryAuthority/frontier/replay seal`
-> `AS4I0 revalidation + independent hostile validation`
-> `OBL035 / C05R2B`
-> `OBL036 / C08-G1`
-> `OBL037 equal-governed-workload bakeoff`.

Until B10 PASS + B adjudication:
- Node7 is frozen;
- DiscoveryAuthority/frontier/replay successor seal is frozen;
- AS4I0 is frozen;
- C05R2B is frozen;
- OBL036 is frozen;
- OBL037 is forbidden.

OBL037 baseline remains:
- identical source/carrier obligations across A/B/C;
- zero deletion credit;
- zero cutover credit;
- zero retirement credit.

Terminal:
`SUB_VOZHD_B_B10_COMMISSIONED__NODE7_FROZEN_ON_MAPPING_PREIMAGE_LAW__OBL037_STILL_GATED`
