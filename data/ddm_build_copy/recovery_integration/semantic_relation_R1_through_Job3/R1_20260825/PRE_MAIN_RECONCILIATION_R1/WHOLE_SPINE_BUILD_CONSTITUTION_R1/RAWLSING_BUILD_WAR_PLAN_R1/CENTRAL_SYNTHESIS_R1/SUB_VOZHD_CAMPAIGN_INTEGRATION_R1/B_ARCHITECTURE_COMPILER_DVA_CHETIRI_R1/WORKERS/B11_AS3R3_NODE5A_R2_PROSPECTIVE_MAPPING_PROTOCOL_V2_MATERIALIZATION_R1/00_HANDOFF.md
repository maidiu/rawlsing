# RABOCHII B11 — AS3R3 NODE5A-R2 PROSPECTIVE MAPPING REPLAY PROTOCOL V2 MATERIALIZATION R1

Repository:
`maidiu/rawlsing`

Worker branch:
`agent/rabochii-subv-b-as3r3-node5a-r2-prospective-mapping-protocol-v2-materialization-r1`

Exact starting HEAD:
`47241cc4f6407cc7c8c6750a04c9e405951882e9`

Terminal:
`AS3R3_NODE5A_R2_PROSPECTIVE_MAPPING_REPLAY_PROTOCOL_V2_MATERIALIZATION_COMPLETE__READY_FOR_NODE7_V2_RECOMMISSION__OR_EXACT_BLOCKER_PROVED`

Execute ONLY the bounded prospective protocol-v2 materialization task.

This is NOT Node7.
This is NOT historical preimage recovery.
This is NOT semantic succession.

## 1. MUST READ EXACT HQ AUTHORITY

Consume prospectively, without rebasing merely to import authority:

Current HQ/PRE-MAIN immutable ref:
`a56868186a0e3e34555251f16b7720b50cfd4a77`

HQ fan-in/adjudication ref:
`805418167a57d95e7098105306aff1321a7d9560`

Read exactly:

`data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/VOZHD_HQ_FANIN_B10_AND_SUBV_D_20260907_R1/01_NODE5A_R2_HISTORICAL_MAPPING_PROTOCOL_DISPOSITION.md`

Expected blob:
`070e2a41debb60bfcaf63862fa48fdd53816c05c`

Read exact protocol spec:

`data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/VOZHD_HQ_FANIN_B10_AND_SUBV_D_20260907_R1/02_NODE5A_R2_PROSPECTIVE_MAPPING_REPLAY_PROTOCOL_V2.json`

Required protocol-spec Git blob:
`befee68ee14f6e80e88cb3142947a37a7619fc5b`

Read B campaign HQ-consumption receipt:

`data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/SUB_VOZHD_CAMPAIGN_INTEGRATION_R1/B_ARCHITECTURE_COMPILER_DVA_CHETIRI_R1/18_HQ_B10_CLASS_B_PROTOCOL_V2_CONSUMPTION_AND_MATERIALIZATION_AUTHORIZATION_R1.md`

## 2. HISTORICAL / PROSPECTIVE SEPARATION

Historical mapping digest:

`081e3b8594be3d9348bc0565cd9085cca1e999ae58ef7881f040d11f5da89c7e`

has HQ disposition:

`IMMUTABLE_HISTORICAL_PROVENANCE__NONREPLAYABLE_AT_CURRENT_EVIDENCE_SURFACE`.

It is NOT:
- an input to the serializer;
- an input to materialization;
- a prospective target;
- a target for serializer selection;
- a target for any equality assertion in this worker;
- proof that protocol v2 was historically used.

Do NOT attempt to recover or reproduce it.

Do NOT search serialization variants.

Do NOT compare the v2 payload hash against it.

Protocol v2 is prospective and project-current because HQ adopted it independently.

## 3. EXACT FROZEN SEMANTIC INPUT

Consume exact current mapping carrier:

`data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/AS3R3_NODE5A_R2_REPLAY_SEAL/ROLE_TO_CANONICAL_REF_CROSSWALK.csv`

Required Git blob:
`26a7c35df2e6454c5e270a03b3571599bdf152fd`

Required CSV header exactly:

`as3_id,source_object_id,source_content_hash,node4a_input_sha256,successor_kind,successor_object_id,successor_content_hash,alias_class,role_key_lookup_preserved`

Required data rows:
`19`

Required row order:

1. `A000`
2. `A1V1`
3. `A1V2`
4. `A1V3`
5. `A1V4`
6. `A1V5`
7. `A1SSUB`
8. `A1SSPS`
9. `A1SMIS`
10. `A1RAPP`
11. `A2V1`
12. `A2V2`
13. `A2V3`
14. `A2V4`
15. `A2V5`
16. `A2SSUB`
17. `A2SSPS`
18. `A2SMIS`
19. `A2RAPP`

Frozen nine row fields exactly:
- `as3_id`
- `source_object_id`
- `source_content_hash`
- `node4a_input_sha256`
- `successor_kind`
- `successor_object_id`
- `successor_content_hash`
- `alias_class`
- `role_key_lookup_preserved`

No omitted keys.
No added keys.

Alias:
- A000 = `{A000,A1RAPP}`
- A1RAPP = `{A000,A1RAPP}`
- all other rows = empty string.

`role_key_lookup_preserved` must parse from the frozen carrier into JSON boolean `true` for all 19 rows.

Frozen successor semantics remain:
- mapping rows = 19;
- distinct successor predicate refs = 18;
- sole alias exactly `{A000,A1RAPP}`;
- no mapping row mutation;
- no successor ExactRef mutation.

## 4. EXACT PROTOCOL-V2 PAYLOAD OBJECT

Construct exactly:

`{"protocol": <protocol-value>, "rows": <19 row objects>}`

where protocol-value is exactly:

`AS3R3_NODE5A_R2_MAPPING_REPLAY_PROTOCOL@2.0.0`

and rows are the frozen records in the exact frozen order.

Before serialization:
- normalize every string value using Unicode NFC;
- preserve booleans as booleans;
- preserve empty alias as empty JSON string;
- do not coerce other strings;
- do not add metadata to the payload.

## 5. EXACT SERIALIZATION LAW

Implement ONCE from the immutable v2 spec:

- format: RFC8259 JSON;
- encoding: UTF-8;
- BOM: none;
- `ensure_ascii=False`;
- recursively sorted keys;
- separators exactly `(",", ":")`;
- no insignificant whitespace;
- rows remain in exact frozen row order;
- append exactly ONE LF byte `0x0A`;
- no other trailing bytes.

For Python, an implementation conforming to the frozen law may use the equivalent of:

`json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8") + b"\n"`

ONLY after the input rows have been validated and NFC-normalized exactly as specified.

Do not invent alternative encodings.
Do not test alternatives.

## 6. COMMIT ORDER / IMMUTABLE IMPLEMENTATION REQUIREMENT

The serializer implementation itself MUST be committed before the qualifying fresh-process materialization proofs.

Required sequence:

1. add exact serializer implementation under this B11 worker directory;
2. commit it;
3. record its exact commit SHA + Git blob + file SHA-256;
4. then run at least two genuinely independent fresh Python processes using THAT committed serializer implementation and the frozen mapping carrier;
5. those processes materialize the prospective payload from scratch.

The final worker branch may add receipts/payload after the serializer commit, but it must be possible to prove the qualifying runs used byte-identical code to the committed serializer.

Do not use an uncommitted scratch serializer as the authoritative implementation.

## 7. REQUIRED SERIALIZER BEHAVIOR

The committed serializer must fail closed unless all are true:
- exact protocol spec blob is the required `befee68e...` when provenance is checked by the worker;
- exact input carrier blob is `26a7c35d...`;
- exact header;
- exactly 19 data rows;
- exact row order;
- exactly nine fields per row;
- every `role_key_lookup_preserved` value is literal semantic true after parsing;
- A000/A1RAPP alias values exact;
- all other alias values empty;
- successor object IDs/content hashes remain exactly those in the carrier.

The serializer must not import, read, embed, compare, or require the historical `081e3b...` digest.

## 8. MATERIALIZE EXACT PROSPECTIVE PAYLOAD

Commit exact payload bytes under:

`data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/SUB_VOZHD_CAMPAIGN_INTEGRATION_R1/B_ARCHITECTURE_COMPILER_DVA_CHETIRI_R1/WORKERS/B11_AS3R3_NODE5A_R2_PROSPECTIVE_MAPPING_PROTOCOL_V2_MATERIALIZATION_R1/02_MAPPING_PAYLOAD_V2.json`

That file itself is the authoritative byte carrier and must end in exactly one LF.

Seal:
- file byte length;
- Git blob SHA;
- SHA-256;
- protocol ID/version;
- exact input carrier blob;
- exact serializer commit/blob/file SHA-256.

The prospective payload SHA-256 is a NEW identity discovered by lawful materialization.

It must NOT be predetermined in this handoff.

## 9. TWO GENUINELY INDEPENDENT FRESH PROCESSES

After serializer implementation is committed, run at least TWO independent fresh Python processes.

Each process must:
1. start with no shared in-memory state from the other;
2. load the frozen mapping carrier;
3. use the committed serializer implementation;
4. validate the exact frozen input constraints;
5. construct the 19 row objects;
6. serialize protocol-v2 payload from scratch;
7. emit exact payload bytes to its own independent temporary output;
8. compute SHA-256 only AFTER materialization.

Require across processes:
- payload bytes byte-identical;
- byte lengths identical;
- payload SHA-256 identical.

Require both process outputs to be byte-identical to committed:
`02_MAPPING_PAYLOAD_V2.json`.

Record process commands, exit status, output SHA-256, byte length, and an appropriate immutable proof that each process used the committed serializer implementation.

Do not feed process 1 output into process 2.

## 10. ROW PRESERVATION / IDENTITY INVARIANTS

Prove from source carrier vs materialized payload:
- rows = 19 exactly;
- exact row order preserved;
- exact nine fields preserved;
- source IDs preserved;
- source object IDs/hashes preserved;
- Node4A input hashes preserved;
- successor kind preserved;
- successor object IDs/hashes preserved;
- alias strings preserved;
- role-key lookup = true for all rows;
- distinct successor predicate content hashes = 18;
- sole duplicate successor target corresponds exactly to A000/A1RAPP;
- no other duplicate alias class introduced.

No semantic terrain changes are authorized.

## 11. D9 / OBL004 CURRENT LAW

Current negative ceiling:

`N025_DOES_NOT_SUPPLY_GENERIC_PRODUCTION_POSITIVE_SOURCE_COMPOSABILITY_LOAD`

and:

`JURISDICTION_OR_API_EXISTENCE != POSITIVE_AUTHORITY_LOAD`.

This materialization task is not an OBL004 production structural operation/source-set proof and does not require opening that lane.

Do NOT treat J01-A, C06, P3 jurisdiction, N025, or D9 as generic positive authority.

Do not perform sibling campaign work.

## 12. HARD STOPS

Do NOT:
- execute `construct_successor_predicate`;
- execute `construct_successor_query`;
- run Node7;
- remint any runtime object;
- modify Node5A-R2 accepted artifacts;
- modify Node4A/Node4B/Node5B/Node6;
- rewrite historical Node6 seal;
- claim historical `081e3b...` reproduction;
- create successor DiscoveryAuthority/frontier/replay identities;
- run AS4I0;
- run hostile validation;
- run LiTS-I/I05/C05R2B;
- enter C08/G1;
- launch OBL037;
- select OBL001 architecture;
- select OBL002 topology;
- enter positive V3;
- modify central/PRE-MAIN/main;
- modify sibling campaign work.

## 13. WRITE ENVELOPE

Write only under:

`data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/SUB_VOZHD_CAMPAIGN_INTEGRATION_R1/B_ARCHITECTURE_COMPILER_DVA_CHETIRI_R1/WORKERS/B11_AS3R3_NODE5A_R2_PROSPECTIVE_MAPPING_PROTOCOL_V2_MATERIALIZATION_R1/`

Required outputs:

- `00_RETURN.md`
- `01_PROTOCOL_V2_SERIALIZER.py`
- `02_MAPPING_PAYLOAD_V2.json`
- `03_PAYLOAD_IDENTITY_RECEIPT.json`
- `04_FRESH_PROCESS_MATERIALIZATION_RECEIPT.json`
- `05_MAPPING_ROW_PRESERVATION_RECEIPT.json`
- `06_HISTORICAL_PROSPECTIVE_SEPARATION_RECEIPT.json`
- `07_NO_SEARCH_NO_TARGET_FITTING_RECEIPT.json`
- `CHANGED_FILES.txt`

Optional bounded tests/helpers may live only in this worker directory.

No production-code path is authorized.

## 14. PASS CONDITION

PASS only if ALL are true:
- exact protocol spec blob verified;
- exact frozen carrier blob verified;
- serializer implementation committed before qualifying runs;
- serializer implements protocol v2 exactly;
- exact prospective payload bytes committed;
- payload SHA-256 sealed;
- at least two independent fresh process materializations;
- both produce byte-identical prospective payload;
- both match committed payload bytes exactly;
- 19 rows preserved exactly;
- 18 distinct successor predicates preserved exactly;
- sole A000/A1RAPP alias preserved;
- no semantic/canonical identity drift;
- historical digest used as neither input nor prospective target;
- serialization variants searched = 0;
- target fitting = false;
- Node7 not entered.

PASS token:

`AS3R3_NODE5A_R2_PROSPECTIVE_MAPPING_REPLAY_PROTOCOL_V2_MATERIALIZATION_COMPLETE__READY_FOR_NODE7_V2_RECOMMISSION`

Otherwise:

`AS3R3_NODE5A_R2_PROSPECTIVE_MAPPING_REPLAY_PROTOCOL_V2_MATERIALIZATION__EXACT_BLOCKER_PROVED`

Return to:
`SUB-VOZHD B — ARCHITECTURE / COMPILER / DVA / CHETIRI`.
