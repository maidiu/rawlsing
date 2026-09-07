# SUB-VOZHD B — HQ B10 CLASS B / PROTOCOL V2 CONSUMPTION + MATERIALIZATION AUTHORIZATION R1

Status:
`HQ_B10_CLASS_B_CONSUMED_PROSPECTIVELY__PROTOCOL_V2_CURRENT__ONE_MATERIALIZATION_WORKER_AUTHORIZED`

Campaign:
`SUB-VOZHD B — ARCHITECTURE / COMPILER / DVA / CHETIRI`

Campaign branch:
`agent/sub-vozhd-architecture-compiler-dva-chetiri-r1`

Returned campaign tip before this receipt:
`520871609ec58b8e6d7fabb7fb242ad38855973a`

No rebase was performed merely to consume HQ authority.

## 1. Exact HQ authority consumed prospectively

Current HQ/PRE-MAIN immutable ref:
`a56868186a0e3e34555251f16b7720b50cfd4a77`

HQ fan-in/adjudication ref:
`805418167a57d95e7098105306aff1321a7d9560`

HQ fan-in terminal:
`HQ_FANIN_COMPLETE__B10_CLASS_B_PROSPECTIVE_REPLAY_PROTOCOL_AUTHORIZED__OBL009_ADOPTED__OBL017_DEPENDENCY_ROUTED__OBL045_RETIRED__SUBV_D_STAND_DOWN`

Exact continuation:
`VOZHD_HQ_FANIN_B10_AND_SUBV_D_20260907_R1/03_SUB_VOZHD_B_CONTINUATION.md`

Continuation Git blob:
`09aa0e7f2404af09f94095dd15c15ca9669966d1`

Exact historical-protocol disposition:
`VOZHD_HQ_FANIN_B10_AND_SUBV_D_20260907_R1/01_NODE5A_R2_HISTORICAL_MAPPING_PROTOCOL_DISPOSITION.md`

Disposition Git blob:
`070e2a41debb60bfcaf63862fa48fdd53816c05c`

Exact prospective protocol spec:
`VOZHD_HQ_FANIN_B10_AND_SUBV_D_20260907_R1/02_NODE5A_R2_PROSPECTIVE_MAPPING_REPLAY_PROTOCOL_V2.json`

Protocol spec Git blob:
`befee68ee14f6e80e88cb3142947a37a7619fc5b`

Project-current protocol:
`AS3R3_NODE5A_R2_MAPPING_REPLAY_PROTOCOL@2.0.0`

## 2. HQ Class B holding

Historical Node5A-R2 mapping payload digest:

`081e3b8594be3d9348bc0565cd9085cca1e999ae58ef7881f040d11f5da89c7e`

is now:

`IMMUTABLE_HISTORICAL_PROVENANCE__NONREPLAYABLE_AT_CURRENT_EVIDENCE_SURFACE`.

It is NOT:
- a prospective serializer-selection target;
- an input to protocol-v2 materialization;
- a required prospective equality;
- evidence that protocol v2 was historically used.

No historical preimage/law recovery is claimed.

Freeze:

`SEMANTIC_IDENTITY_PRESERVED != HISTORICAL_EVIDENCE_PROTOCOL_PRESERVED`.

## 3. Frozen semantic/runtime spine

Unchanged:
- predicate source/role rows = 19;
- role-to-successor mappings = 19;
- distinct successor predicates = 18;
- sole alias = `{A000,A1RAPP}`;
- query mappings = 3;
- distinct successor queries = 3;
- historical-to-successor mappings = 22;
- distinct successor canonical objects = 21.

Exact material mapping carrier:
`AS3R3_NODE5A_R2_REPLAY_SEAL/ROLE_TO_CANONICAL_REF_CROSSWALK.csv`

Carrier Git blob:
`26a7c35df2e6454c5e270a03b3571599bdf152fd`

Carrier row count:
`19`.

Historical Node6 seal:
`df0395983de34996d33c258d0705cfc178df9cfe7982899431a0002c544481da`

remains accepted HISTORICAL comparison evidence.

It is NOT the exact prospective replay seal that future Node7 must emit.

## 4. Protocol-v2 exact byte law

Frozen payload object:
- top-level keys exactly `protocol`, `rows`;
- `protocol = "AS3R3_NODE5A_R2_MAPPING_REPLAY_PROTOCOL@2.0.0"`;
- `rows` contains exactly the 19 frozen mapping rows;
- each row contains exactly:
  - `as3_id`
  - `source_object_id`
  - `source_content_hash`
  - `node4a_input_sha256`
  - `successor_kind`
  - `successor_object_id`
  - `successor_content_hash`
  - `alias_class`
  - `role_key_lookup_preserved`.

Exact row order:
`A000,A1V1,A1V2,A1V3,A1V4,A1V5,A1SSUB,A1SSPS,A1SMIS,A1RAPP,A2V1,A2V2,A2V3,A2V4,A2V5,A2SSUB,A2SSPS,A2SMIS,A2RAPP`.

Exact alias law:
- A000 alias_class = `{A000,A1RAPP}`;
- A1RAPP alias_class = `{A000,A1RAPP}`;
- all other alias_class = empty string.

`role_key_lookup_preserved` is JSON boolean true for all 19 rows.

All strings are Unicode NFC before serialization.

Serialization:
- RFC8259 JSON;
- UTF-8;
- no BOM;
- recursively lexicographically sorted keys;
- separators exactly `,` and `:`;
- no insignificant whitespace;
- exact frozen row order;
- exactly one terminal LF byte `0x0A`;
- `ensure_ascii=false`.

This is a prospective law selected by HQ.
No variant search is authorized or needed.

## 5. Immediate local authorization

Authorize exactly ONE smallest bounded worker:

`AS3R3_NODE5A_R2_PROSPECTIVE_MAPPING_REPLAY_PROTOCOL_V2_MATERIALIZATION`

Its job is only to:
1. consume exact protocol blob `befee68e...`;
2. consume exact carrier blob `26a7c35d...`;
3. implement the serializer exactly;
4. materialize the exact payload bytes once under that law;
5. commit serializer source + exact payload bytes;
6. seal prospective payload SHA-256;
7. execute at least two genuinely independent fresh-process materializations from the frozen carrier + committed serializer/protocol;
8. require byte-identical output and identical SHA-256;
9. prove all 19 input/output mapping rows are exactly preserved;
10. prove no semantic/canonical identity, alias, count, ordering, or terrain drift.

It MUST NOT:
- execute Node7 constructors;
- search serialization variants;
- target-fit;
- compare the materialized prospective payload to the historical `081e3b...` digest as a success criterion;
- rewrite historical Node5A-R2/Node6 artifacts;
- alter producer/schema/Node4A/Node4B/Node5B/Node6;
- enter DiscoveryAuthority/frontier/replay, AS4I0, C05R2B, C08/G1, OBL037, or V3.

## 6. Node7 gate

Node7 remains:
`FROZEN_PENDING_PROTOCOL_V2_MATERIALIZATION_PASS_AND_B_ADJUDICATION`.

On a clean materialization PASS:
1. inspect exact return;
2. bank worker;
3. campaign-adjudicate prospective payload identity + executable serialization evidence;
4. recommission exactly one Node7 fresh combined replay under protocol v2.

Future Node7 must emit a NEW versioned prospective combined replay seal.

## 7. D9 / OBL004 negative ceiling consumed

Exact HQ disposition blob:
`f1d06a042e447747338a6fbce67e0691b674bd2a`

Current laws:
`N025_DOES_NOT_SUPPLY_GENERIC_PRODUCTION_POSITIVE_SOURCE_COMPOSABILITY_LOAD`

`JURISDICTION_OR_API_EXISTENCE != POSITIVE_AUTHORITY_LOAD`.

These do not block this protocol-materialization lane.

When B later enters an exact OBL004 production structural operation + source-set grain, B must:
1. name the exact operation;
2. name the exact source set;
3. enumerate every separately required positive P3 premise;
4. bind every premise to exact competent positive authority;
5. fail closed on any missing premise.

No J01-A/C06/P3/N025/D9 generic-positive shortcut is allowed.

## 8. Hard gates

- no OBL037 before OBL035 + OBL036 close;
- B does not select OBL001 architecture;
- B does not select OBL002 topology;
- no sibling-campaign work;
- no positive V3 execution.

Terminal:
`SUB_VOZHD_B_HQ_CLASS_B_CONSUMED__PROTOCOL_V2_MATERIALIZATION_NEXT__NODE7_STILL_GATED`
