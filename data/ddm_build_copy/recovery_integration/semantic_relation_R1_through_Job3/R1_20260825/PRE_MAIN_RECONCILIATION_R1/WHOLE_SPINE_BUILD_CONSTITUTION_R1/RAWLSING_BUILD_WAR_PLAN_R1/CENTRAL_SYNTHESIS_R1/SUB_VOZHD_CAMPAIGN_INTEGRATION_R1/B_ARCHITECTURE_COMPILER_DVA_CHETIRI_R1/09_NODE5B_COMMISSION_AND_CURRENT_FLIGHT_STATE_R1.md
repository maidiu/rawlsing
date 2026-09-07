# SUB-VOZHD B — NODE5B COMMISSION + CURRENT FLIGHT STATE R1

Status:
`NODE4B_BANKED_AND_ACCEPTED__NODE5B_COMMISSIONED__OBL035_SUCCESSION_CHAIN_ACTIVE`

Campaign branch:
`agent/sub-vozhd-architecture-compiler-dva-chetiri-r1`

Node4B bank merge:
`480a19de81815ce51083bc2fe0a506516ab3516f`

Node4B adjudication:
`d3e8f6587519bd7128224258c12466230f5fa079`

## Active worker

B7:
`AS3R3 NODE5B QUERY MINT + REPLAY SEAL R1`

Branch:
`agent/rabochii-subv-b-as3r3-node5b-query-mint-replay-r1`

Starting HEAD:
`d3e8f6587519bd7128224258c12466230f5fa079`

Handoff:
`83e002d22ee0d6136e38b5e62023a488dc36cb6e`

No duplicate Node5B proof branch existed at commission time.

Owned proof:
- revalidate exact Node4B 19+3 future input bundle;
- validate exact 3 frozen query inputs;
- call frozen successor query constructor exactly 3 times;
- produce exactly 3 distinct successor query refs;
- serialize exactly 3 canonical query representations;
- preserve A000 condition-role provenance through the lawful predicate alias;
- fresh-process replay at least twice;
- remint zero predicates.

## PASS trigger

Expected terminal:
`AS3R3_NODE5B_QUERY_MINT_REPLAY_SEAL_COMPLETE__READY_FOR_COMBINED_SUCCESSOR_RUNTIME_SEAL`

On PASS:
1. inspect exact B7 return/write envelope;
2. bank lawful evidence;
3. adjudicate Node5B at campaign grain;
4. commission exactly one combined successor runtime seal worker;
5. do NOT collapse the separately required fresh combined replay node into the combined-seal worker unless a newer exact HQ act explicitly changes the sequence.

## Blocker trigger

Expected terminal:
`AS3R3_NODE5B_QUERY_MINT_REPLAY_SEAL__EXACT_BLOCKER_PROVED`

If blocker is:
- B-owned and inside current authority: launch smallest exact repair;
- identity/cardinality anomaly without adopted alias law: do not manufacture uniqueness; return exact court packet;
- sibling-owned: freeze only exact lane and emit cross-campaign dependency packet;
- new authority/trajectory need: smallest HQ adjudication packet.

## Remaining chain

`Node5B`
-> `combined successor runtime seal`
-> `fresh combined replay`
-> `successor DiscoveryAuthority/frontier/replay seal`
-> `AS4I0 revalidation + independent hostile validation`
-> `OBL035 / C05R2B`
-> `OBL036 / C08-G1`
-> `OBL037 equal-governed-workload bakeoff`.

OBL037 baseline remains:
- identical source/carrier retention across A/B/C;
- zero deletion credit;
- zero cutover credit;
- zero retirement credit.

OBL037 remains forbidden until OBL035 and OBL036 close.

Terminal:
`SUB_VOZHD_B_NODE5B_COMMISSIONED__OBL035_CHAIN_ACTIVE__OBL037_STILL_GATED`
