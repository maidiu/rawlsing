# B12 RETURN — AS3R3 NODE7-V2 PROSPECTIVE FRESH COMBINED REPLAY R1

Status: **PASS**

Terminal:
`AS3R3_NODE7_V2_PROSPECTIVE_FRESH_COMBINED_REPLAY_COMPLETE__READY_FOR_SUCCESSOR_DISCOVERY_AUTHORITY_FRONTIER_REPLAY_SEAL`

Branch:
`agent/rabochii-subv-b-as3r3-node7-v2-prospective-fresh-combined-replay-r1`

## Qualifying replay implementation
- committed driver commit: `e5f9a14a77c2b84a86ce6eefaddb4b5c12b17e39`
- driver Git blob: `b308205e7454a896b57c24ef658ddf83d720b1d2`
- driver SHA-256: `2d9a8107d8e03c03abd5e9e5a3e45de6f0cb5c0ba988b68cc6856c1a77330004`
- frozen producer/contract/schema and Node4A/Node4B carriers were verified byte-exact before execution.

## Independent fresh processes
Two separate `/usr/bin/python3 -I -S` OS processes executed from disjoint roots. Neither consumed the other process's outputs. Each independently:
- validated and constructed exactly 19 predicates;
- reconstructed all 19 protocol-v2 mapping rows from actual Node4A inputs plus fresh predicate results;
- reproduced prospective mapping SHA-256 `06f874df6bdd2e621886f748c8aa12397533e273649f99e654dc3779b5eb59db` (Git blob `d62847e9972362bf2fcaeac515360cd5cf99eab7`, 12364 bytes);
- produced 18 distinct predicates with sole alias `{A000,A1RAPP}`;
- validated and constructed exactly 3 queries;
- reproduced all 3 accepted successor query identities and canonical representations;
- reproduced 22 mapping results -> 21 distinct successor canonical objects;
- preserved the exact frozen terrain/cardinality/order invariants;
- did not enter downstream Node7 execution.

Both processes emitted byte-identical deterministic realizations:
- realization SHA-256: `7dccb36d8b7bb5b4e7862d926b32cff3a055762b550938a347a980425f0d1979`
- realization Git blob: `9f0a93f8e34c8ef78a462028fa1e96047d1faba0`
- realization byte length: 15366

## Prospective combined replay seal v2
- kind/version: `AS3R3_NODE7_PROSPECTIVE_COMBINED_REPLAY_SEAL@2.0.0`
- seal payload SHA-256: `1a47edb125389b43e62926908b0d86129940da57983283e2d07a457c52606f4e`
- object ID: `urn:rawlsing:pre553:as3r3:node7:prospective-combined-replay-seal:v2:sha256:1a47edb125389b43e62926908b0d86129940da57983283e2d07a457c52606f4e`

The seal is prospective and new. It does **not** claim exact reproduction of historical Node6 seal `df0395983de34996d33c258d0705cfc178df9cfe7982899431a0002c544481da`. Historical mapping digest `081e3b8594be3d9348bc0565cd9085cca1e999ae58ef7881f040d11f5da89c7e` remains `IMMUTABLE_HISTORICAL_PROVENANCE__NONREPLAYABLE_AT_CURRENT_EVIDENCE_SURFACE` and was not used as a replay target or preimage target.

Historical Node6 remains comparison evidence only: `ACCEPTED_HISTORICAL_COMPARISON_EVIDENCE__NOT_PROSPECTIVE_REPLAY_TARGET`.

No DiscoveryAuthority/frontier/replay identity was created, no OBL037 work was launched, and no downstream candidate execution was entered.
