# SUB-VOZHD B — B11 PROTOCOL-V2 MATERIALIZATION ADJUDICATION + NODE7-V2 AUTHORIZATION R1

Status:
`B11_PROTOCOL_V2_MATERIALIZATION_ACCEPTED__NODE7_V2_FRESH_REPLAY_AUTHORIZED_NEXT`

Campaign:
`SUB-VOZHD B — ARCHITECTURE / COMPILER / DVA / CHETIRI`

Campaign branch:
`agent/sub-vozhd-architecture-compiler-dva-chetiri-r1`

Binding HQ/PRE-MAIN ref:
`a56868186a0e3e34555251f16b7720b50cfd4a77`

HQ fan-in/adjudication ref:
`805418167a57d95e7098105306aff1321a7d9560`

## 1. B11 bank

Worker:
`B11 — AS3R3 NODE5A-R2 PROSPECTIVE MAPPING REPLAY PROTOCOL V2 MATERIALIZATION R1`

Worker branch:
`agent/rabochii-subv-b-as3r3-node5a-r2-prospective-mapping-protocol-v2-materialization-r1`

Starting HEAD:
`47241cc4f6407cc7c8c6750a04c9e405951882e9`

Handoff:
`d5e9baf18b1ea53cf76b6aa2f338bb3dd83329ac`

Terminal tip:
`15cc46e302a530f3b9fea3199bd91229b93ea63b`

Terminal:
`AS3R3_NODE5A_R2_PROSPECTIVE_MAPPING_REPLAY_PROTOCOL_V2_MATERIALIZATION_COMPLETE__READY_FOR_NODE7_V2_RECOMMISSION`

Campaign bank merge:
`622f0a99d14d3712400bdb4748b4de162a3dcf1f`

Verified worker delta:
- 10 commits ahead / 0 behind starting HEAD;
- exactly 10 changed paths;
- all changes confined to the authorized B11 worker directory;
- no production/schema/accepted Node4A/Node5A-R2/Node4B/Node5B/Node6/central/PRE-MAIN/main/sibling/downstream mutation.

## 2. Commit-order adjudication

Required immutable sequence is satisfied exactly:

1. handoff:
   `d5e9baf18b1ea53cf76b6aa2f338bb3dd83329ac`;
2. serializer committed:
   `84a80b6d0aec9525cae704093ae770415371a4aa`;
3. prospective payload committed as direct child:
   `6c03af3c4aed1ad6f305976d8cf60809167f8976`;
4. qualifying fresh-process receipts/return committed afterward.

Serializer:
- Git blob:
  `29b61fc7fef8db06e4ba95fedc788a20b8d28d5e`;
- file SHA-256:
  `47307828a471cc525643f870c32ac15efa26565f063191d50ea32c48c72994b6`.

Code-level inspection confirms the serializer directly implements the HQ v2 byte law:
- exact protocol-spec Git blob check;
- exact carrier Git blob check;
- exact header/19-row/order/alias/cardinality checks;
- Unicode NFC;
- JSON booleans;
- recursively sorted keys;
- compact separators;
- UTF-8/no BOM;
- exactly one trailing LF;
- no historical digest literal;
- no alternate serialization search;
- no predicate/query constructor path.

## 3. Prospective payload identity accepted

Project-current prospective mapping replay protocol:

`AS3R3_NODE5A_R2_MAPPING_REPLAY_PROTOCOL@2.0.0`

Protocol spec Git blob:
`befee68ee14f6e80e88cb3142947a37a7619fc5b`

Frozen material carrier Git blob:
`26a7c35df2e6454c5e270a03b3571599bdf152fd`

Accepted newly materialized prospective payload:

- Git blob:
  `d62847e9972362bf2fcaeac515360cd5cf99eab7`;
- SHA-256:
  `06f874df6bdd2e621886f748c8aa12397533e273649f99e654dc3779b5eb59db`;
- byte length:
  `12364`;
- payload commit:
  `6c03af3c4aed1ad6f305976d8cf60809167f8976`;
- UTF-8;
- no BOM;
- compact recursively sorted JSON;
- exact frozen row order;
- exactly one trailing LF.

Verdict:
`PASS__PROSPECTIVE_MAPPING_PAYLOAD_V2_IDENTITY_CURRENT_AT_B_CAMPAIGN_GRAIN`.

## 4. Fresh-process materialization accepted

Qualifying fresh processes:
`2`.

Both:
- ran as separate OS processes;
- used `/usr/bin/python3 -I -S`;
- shared no in-memory state;
- did not feed run-1 output into run-2;
- verified the committed serializer implementation;
- verified exact protocol/carrier inputs;
- independently produced 12364 bytes;
- independently produced SHA-256:
  `06f874df6bdd2e621886f748c8aa12397533e273649f99e654dc3779b5eb59db`;
- independently produced Git blob:
  `d62847e9972362bf2fcaeac515360cd5cf99eab7`;
- were byte-identical to each other;
- were byte-identical to committed `02_MAPPING_PAYLOAD_V2.json`.

## 5. Semantic/runtime invariants accepted unchanged

The prospective evidence-protocol succession changes NO semantic/runtime identity.

Preserved exactly:
- mapping rows = 19;
- row order = frozen HQ order;
- row fields = exact nine;
- source IDs/object IDs/content hashes;
- Node4A input hashes;
- successor kinds/object IDs/content hashes;
- role-key lookup = true for all 19;
- distinct successor predicates = 18;
- sole duplicate successor target = `A000/A1RAPP`;
- sole alias class = `{A000,A1RAPP}`.

No semantic or canonical identity drift.

## 6. Historical/prospective separation remains binding

Historical Node5A-R2 mapping digest:

`081e3b8594be3d9348bc0565cd9085cca1e999ae58ef7881f040d11f5da89c7e`

remains:

`IMMUTABLE_HISTORICAL_PROVENANCE__NONREPLAYABLE_AT_CURRENT_EVIDENCE_SURFACE`.

It is not:
- protocol-v2 input;
- serializer-selection target;
- prospective equality target;
- prospective replay identity.

Historical Node6 seal:

`df0395983de34996d33c258d0705cfc178df9cfe7982899431a0002c544481da`

remains accepted HISTORICAL comparison evidence.

It is NOT the exact seal Node7-v2 must reproduce.

## 7. Node7-v2 authorization

Authorize exactly ONE fresh Node7-v2 worker.

Exact grain:

`AS3R3_NODE7_PROSPECTIVE_FRESH_COMBINED_REPLAY_V2`

It must execute at least two genuinely independent fresh constructor processes.

Each process must reconstruct from frozen executable/input authority:
- exact frozen producer;
- exact Node4A predicate inputs;
- exact Node4B query inputs;
- immutable historical AS3R2 predecessor manifest where historical succession comparison is required;
- exact protocol-v2 spec and committed B11 serializer implementation.

Each process must:
1. fresh-construct 19 predicate results using exactly 19 predicate constructor calls;
2. reconstruct the exact 19 v2 mapping rows FROM those fresh results plus their frozen Node4A/source provenance;
3. serialize the reconstructed rows under protocol v2;
4. reproduce prospective mapping payload SHA-256:
   `06f874df6bdd2e621886f748c8aa12397533e273649f99e654dc3779b5eb59db`;
5. produce exactly 18 distinct successor predicate identities;
6. preserve sole `{A000,A1RAPP}` alias;
7. validate and fresh-construct exactly 3 successor query results using exactly 3 query constructor calls;
8. reproduce all 3 exact accepted successor query identities and canonical representations;
9. preserve exact cardinality/order/terrain/canonical-object invariants;
10. compare against historical Node6 evidence while explicitly separating historical evidence protocol from prospective protocol v2;
11. emit a NEW VERSIONED PROSPECTIVE COMBINED REPLAY SEAL.

Committed B11 prospective payload bytes are comparison target only, not row-construction input.

Historical `081e3b...` is provenance only, not a replay target.

## 8. Prospective seal law for Node7-v2

Node7-v2 shall emit a NEW evidence identity:

`AS3R3_NODE7_PROSPECTIVE_COMBINED_REPLAY_SEAL@2.0.0`.

The seal payload must be canonical compact sorted JSON + exactly one trailing LF:
`json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8") + b"\n"`.

The seal payload must bind at minimum:

- schema:
  `AS3R3_NODE7_PROSPECTIVE_COMBINED_REPLAY_SEAL_PAYLOAD@2.0.0`;
- status:
  `PASS__PROSPECTIVE_FRESH_COMBINED_REPLAY_V2`;
- protocol:
  `AS3R3_NODE5A_R2_MAPPING_REPLAY_PROTOCOL@2.0.0`;
- protocol spec Git blob:
  `befee68ee14f6e80e88cb3142947a37a7619fc5b`;
- committed serializer Git blob:
  `29b61fc7fef8db06e4ba95fedc788a20b8d28d5e`;
- committed serializer SHA-256:
  `47307828a471cc525643f870c32ac15efa26565f063191d50ea32c48c72994b6`;
- prospective mapping payload SHA-256:
  `06f874df6bdd2e621886f748c8aa12397533e273649f99e654dc3779b5eb59db`;
- prospective mapping payload Git blob:
  `d62847e9972362bf2fcaeac515360cd5cf99eab7`;
- fresh-process replay count;
- exact 19 predicate mapping result identities;
- exact 18 distinct predicate identities;
- exact sole alias class;
- exact 3 query mapping/result identities;
- exact 3 distinct query identities;
- canonical representation hashes for all 21 distinct successor objects;
- exact terrain/cardinality/order invariants;
- historical mapping digest with disposition only:
  `IMMUTABLE_HISTORICAL_PROVENANCE__NONREPLAYABLE_AT_CURRENT_EVIDENCE_SURFACE`;
- historical Node6 seal:
  `df0395983de34996d33c258d0705cfc178df9cfe7982899431a0002c544481da`;
- historical Node6 role:
  `ACCEPTED_HISTORICAL_COMPARISON_EVIDENCE__NOT_PROSPECTIVE_REPLAY_TARGET`;
- explicit statement that no historical mapping-preimage/law recovery is claimed.

Do NOT embed process-local paths/timestamps/randomness in the seal payload.

The prospective seal SHA-256 must be discovered only after lawful fresh replay and sealing.
It is not predetermined here.

## 9. Historical Node6 comparison ceiling

Node7-v2 must compare and preserve the underlying historical Node6 invariants:
- 22 historical-to-successor mapping rows;
- 21 distinct successor canonical objects;
- exact 18 predicate + 3 query identities;
- canonical representation identity;
- sole A000/A1RAPP alias;
- exact query cardinality;
- exact terrain invariants.

Node7-v2 must NOT require equality to any historical Node6 aggregate/seal identity that binds the retired/nonreplayable historical mapping-payload protocol.

Historical evidence hashes may be reported as comparison refs, but the new prospective seal is a distinct evidence identity.

## 10. Downstream boundary

Node7-v2 PASS does NOT itself create:
- successor DiscoveryAuthority/frontier/replay seal;
- AS4I0 revalidation;
- hostile validation;
- C05R2B;
- C08/G1;
- OBL037;
- V3.

Exact next node after B accepts a clean Node7-v2 PASS:

`SUCCESSOR_DISCOVERY_AUTHORITY_FRONTIER_REPLAY_SEAL`.

## 11. D9 / OBL004 law remains current

`N025_DOES_NOT_SUPPLY_GENERIC_PRODUCTION_POSITIVE_SOURCE_COMPOSABILITY_LOAD`.

`JURISDICTION_OR_API_EXISTENCE != POSITIVE_AUTHORITY_LOAD`.

This Node7-v2 lane is not itself a generic OBL004 positive composability grant.

## 12. Hard gates

- no OBL037 before OBL035 + OBL036;
- no OBL001 architecture selection by B;
- no OBL002 topology selection by B;
- no sibling-campaign work;
- no positive V3.

Terminal:
`SUB_VOZHD_B_B11_ACCEPTED__NODE7_V2_AUTHORIZED_NEXT__OBL037_STILL_GATED`
