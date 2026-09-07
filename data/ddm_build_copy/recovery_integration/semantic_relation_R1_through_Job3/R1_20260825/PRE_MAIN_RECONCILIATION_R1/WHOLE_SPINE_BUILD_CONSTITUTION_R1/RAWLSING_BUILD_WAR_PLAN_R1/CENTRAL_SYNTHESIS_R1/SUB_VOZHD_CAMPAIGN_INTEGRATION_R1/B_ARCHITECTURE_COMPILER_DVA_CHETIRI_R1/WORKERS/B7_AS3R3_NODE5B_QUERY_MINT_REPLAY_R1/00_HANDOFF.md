# RABOCHII B7 — AS3R3 NODE5B QUERY MINT + REPLAY SEAL R1

Repository:
`maidiu/rawlsing`

Worker branch:
`agent/rabochii-subv-b-as3r3-node5b-query-mint-replay-r1`

Exact starting HEAD:
`d3e8f6587519bd7128224258c12466230f5fa079`

Terminal:
`AS3R3_NODE5B_QUERY_MINT_REPLAY_SEAL_COMPLETE__READY_FOR_COMBINED_SUCCESSOR_RUNTIME_SEAL__OR_EXACT_BLOCKER_PROVED`

Execute Node5B only.

## 1. MUST READ

### SUB-VOZHD B current authority

Read:
`data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/SUB_VOZHD_CAMPAIGN_INTEGRATION_R1/B_ARCHITECTURE_COMPILER_DVA_CHETIRI_R1/08_NODE4B_ADJUDICATION_AND_NODE5B_AUTHORIZATION_R1.md`

Binding verdict:
`PASS__NODE4B_ACCEPTED_AT_CAMPAIGN_GRAIN__READY_FOR_NODE5B`.

### HQ / central authority

Consume prospectively from immutable ref:
`5b308c1a87e11a95cfd53cc72e660f641abfdb33`.

Read:
- `.../ALL_SUB_VOZHD_AND_VERKHOVOD_FANIN_R1/02_SUB_VOZHD_B_CONTINUATION_R1.md`;
- `.../SUB_VOZHD_B_HQ_FANIN_DISPOSITION_R1/00_VOZHD_DISPOSITION.md`.

No rebase or central/PRE-MAIN merge merely to consume authority.

### AS3R3 governing authority

Read exact:
- Authority 28 — runtime identity succession HQ adoption;
- Authority 29 — frozen producer identity;
- Authority 30 — two-phase predicate -> query sequence;
- Authority 34 — corrected predicate cardinality law.

Binding sequence:
`PREDICATE_INPUT_FREEZE -> PREDICATE_MINT -> QUERY_INPUT_FREEZE -> QUERY_MINT`.

Node4B is now campaign-accepted; Node5B is the exact next lawful node.

## 2. FROZEN PRODUCER — IMMUTABLE SIDE REF

Use exact producer commit:
`cfc240aa3a64c59509eab97450a7d3603af813cc`.

Producer:
`rawlsing_next/pre553_as3r3_runtime_producer.py`
- Git blob `d63370dbcadc043dd2f27f5383cf36f0e84d1235`;
- file SHA-256 `ad7434186e5e72886333f438ed9726cec01a2d2cf740353175da938708a5ef6d`.

Contract:
`rawlsing_next/pre553_as3r3_runtime_producer_contract.py`
- Git blob `26a7d123881513524e26f2342ab93dd1141fb5f6`.

Schema:
`rawlsing_next/pre553_as3r3_runtime_producer_input.schema.json`
- Git blob `3a15657cb99624a15fc4587b2a9e587dfafe65d3`.

Relevant constructor:
`construct_successor_query(record, successor_predicate_refs=...)`.

Do not modify producer, contract, or schema.

## 3. FROZEN INPUTS / PREDICATE SURFACE

### Node5A-R2 predicate successor surface

Campaign ancestry contains the accepted Node5A-R2 evidence.

Binding:
- 19 source/role rows;
- 19 role mappings;
- 18 distinct canonical predicates;
- sole alias exactly `{A000,A1RAPP}`;
- independent A000/A1RAPP lookup preserved.

Canonical condition ref used by all three Node4B query inputs:
`EmpiricalPredicate@1.0.0 / ac3fcb4e32a41f9972004b2c31da61e9b32ba69568a795d2c1e584c9bed21be0`.

Use the exact full 18-ref canonical successor-predicate set from:
`AS3R3_NODE5A_R2_REPLAY_SEAL/CANONICAL_PREDICATE_MANIFEST.json`
and the exact role mapping from:
`AS3R3_NODE5A_R2_REPLAY_SEAL/ROLE_TO_CANONICAL_REF_CROSSWALK.csv`.

### Node4B frozen query inputs

Consume exactly:
`data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/SUB_VOZHD_CAMPAIGN_INTEGRATION_R1/B_ARCHITECTURE_COMPILER_DVA_CHETIRI_R1/WORKERS/B6_AS3R3_NODE4B_QUERY_INPUT_FREEZE_R1/01_QUERY_INPUTS.json`

Frozen source IDs:
- `T_Q301_2_RAW`;
- `T_Q301_7_RAW`;
- `T_Q301_2_Q301_7_RAW`.

Frozen query-input hashes:
- `T_Q301_2_RAW`:
  `714dde6e80801a563897f9a5cef707c7147e7fbb649473d707b8c030caecac9e`;
- `T_Q301_7_RAW`:
  `39791ee08a60ba2e8e76724200a32b0afe95411983c5eefc72c3ac19393b9416`;
- `T_Q301_2_Q301_7_RAW`:
  `ec75b212e57736664e33738ffa8d69483c4c6f82c6b8199aabef414d4846b1f1`.

Ordered query package SHA-256:
`fa68d91d4c40ff606cf4f5b06a3b213b57e3ecfc7e0c029627d7fd29413998a6`.

Complete Node4B future-input bundle:
`data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/SUB_VOZHD_CAMPAIGN_INTEGRATION_R1/B_ARCHITECTURE_COMPILER_DVA_CHETIRI_R1/WORKERS/B6_AS3R3_NODE4B_QUERY_INPUT_FREEZE_R1/03_COMPLETE_FUTURE_INPUT_BUNDLE.json`

Exact bundle SHA-256:
`2cf15c20a4c65c2dcb29c6fd015260aa9ed8a70f0537927368c86e561a834e50`.

Before minting anything:
1. recompute and verify all three query-input hashes;
2. verify exact ordered query package hash;
3. verify exact complete 19+3 bundle hash;
4. run `validate_future_input_bundle(...)`;
5. require PASS.

If the committed Node4B package does not reproduce exactly, STOP.

## 4. EXACT NODE5B WORK

### A. Validate the three frozen inputs

Using the exact frozen producer:
`validate_successor_query_input(record, successor_predicate_refs=...)`

Require 3/3 PASS against the exact 18-ref Node5A-R2 canonical successor-predicate set.

Do not alter the records.

### B. Mint exactly three successor queries

Invoke:
`construct_successor_query(record, successor_predicate_refs=...)`

exactly once for each of the 3 frozen Node4B query input records.

Constructor invocation count must equal:
`3`.

Produce exactly three AS3 query-source -> successor-query mapping rows.

Expected semantic sources remain:
- `T_Q301_2_RAW`;
- `T_Q301_7_RAW`;
- `T_Q301_2_Q301_7_RAW`.

Each query must retain:
- typed state `QUERY_AUTHORIZED_RESOLVABLE`;
- exact frozen target refs;
- exact target arity/topology;
- exact A000 condition-role provenance bound to the lawful shared canonical predicate ref;
- exact risk/source/scope/universe refs;
- RAW measure basis;
- exact requested output grain;
- exact query authority closure;
- exact producer replay root.

### C. Query identity cardinality

Current authority expects three successor query runtime identities for three distinct frozen query semantic definitions.

Success PASS requires:
- 3 constructor invocations;
- 3 source/role mapping rows;
- 3 canonical query representations;
- 3 distinct canonical `EmpiricalQuerySpec@1.0.0` refs.

If any two frozen query semantic inputs produce the same canonical query identity:
- DO NOT inject query source ID;
- DO NOT inject role/provenance wrappers;
- DO NOT inject historical AS3R2 hash;
- DO NOT modify producer/schema;
- return `EXACT_BLOCKER_PROVED__QUERY_IDENTITY_CARDINALITY_COLLISION` with the exact collision evidence.

There is no adopted query-alias exception analogous to `{A000,A1RAPP}`.

### D. Serialize exact canonical representations

Persist each of the 3 canonical successor query representations exactly once.

Produce:
- exact query-source-ID -> successor-query-ref crosswalk;
- canonical query manifest;
- exact condition-binding receipt;
- exact query package identity/hash;
- exact old/historical provenance links where already authorized, without pretending old AS3R2 runtime identity was recovered.

Do not create the combined 18-predicate + 3-query runtime seal yet.

### E. Fresh-process replay

At least two independent fresh Python processes must:
1. load exact committed Node4B frozen query inputs;
2. load exact Node5A-R2 predicate successor refs;
3. use exact frozen producer/contract;
4. validate 3/3 inputs;
5. invoke the query constructor exactly 3 times;
6. reproduce byte-identically:
   - all 3 query refs;
   - all 3 canonical representations;
   - query-source crosswalk;
   - condition-role bindings;
   - package identity/hash.

No predicate reminting is allowed during replay.

Require:
- fresh replay count >= 2;
- byte-identical result across runs.

## 5. FROZEN TERRAIN / INVARIANTS

Preserve unchanged:
- Node4A 19 frozen predicate input records;
- Node5A-R2 19 role mappings / 18 canonical predicates;
- sole predicate alias `{A000,A1RAPP}`;
- Node4B 3 frozen query input records;
- A000 condition-role provenance;
- 3 query semantic definitions;
- K=18;
- J=2;
- recursive depth=18;
- candidate count=82;
- candidate membership/order;
- RAW-only measure basis;
- no-pruning;
- RNG=`NONE`;
- minimum_raw_denominator=0;
- common I03 law;
- typed-nonpositive learned/PRE-V3 target;
- common A/B/C terrain/fairness.

## 6. HARD STOPS

Do NOT:
- remint or modify successor predicates;
- modify Node4B query input records;
- freeze new query semantics;
- create combined successor runtime seal;
- perform the later fresh combined replay node;
- create successor DiscoveryAuthority/frontier/replay identities;
- run AS4I0;
- run independent hostile validation;
- run LiTS-I/I05/C05R2B;
- enter C08/G1;
- launch OBL037;
- enter V3;
- edit production code;
- edit central state/PRE-MAIN/main;
- perform HQ adoption;
- modify sibling campaign work.

If an exact sibling-owned dependency is discovered, freeze only that lane and return a `CROSS_CAMPAIGN_DEPENDENCY` packet.

## 7. WRITE ENVELOPE

Write only under:
`data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/SUB_VOZHD_CAMPAIGN_INTEGRATION_R1/B_ARCHITECTURE_COMPILER_DVA_CHETIRI_R1/WORKERS/B7_AS3R3_NODE5B_QUERY_MINT_REPLAY_R1/`

Required outputs:
- `00_RETURN.md`;
- `01_SUCCESSOR_QUERY_MANIFEST.json`;
- `02_QUERY_SOURCE_TO_SUCCESSOR_REF_CROSSWALK.csv`;
- `03_CANONICAL_QUERY_REPRESENTATIONS.json`;
- `04_QUERY_IDENTITY_CARDINALITY_RECEIPT.json`;
- `05_CONDITION_BINDING_RECEIPT.json`;
- `06_FRESH_PROCESS_REPLAY_RECEIPT.json`;
- `07_TERRAIN_INVARIANCE_RECEIPT.json`;
- `08_ZERO_PREDICATE_REMINT_RECEIPT.json`;
- `CHANGED_FILES.txt`.

Optional bounded helpers/tests may exist only in this worker directory.

## 8. SUCCESS CONDITION

PASS only if simultaneously:
- Node4B frozen bundle/hash reproduces exactly before mint;
- 3/3 frozen query inputs validate;
- query constructor calls = 3 exactly;
- query source mappings = 3 exactly;
- canonical query refs = 3 distinct exactly;
- all 3 canonical query representations serialized once;
- condition-role provenance remains exact A000 through lawful predicate alias;
- at least two fresh-process replays are byte-identical;
- successor predicate remints = 0;
- combined successor seal not created;
- later chain not entered.

PASS token:
`AS3R3_NODE5B_QUERY_MINT_REPLAY_SEAL_COMPLETE__READY_FOR_COMBINED_SUCCESSOR_RUNTIME_SEAL`

Otherwise:
`AS3R3_NODE5B_QUERY_MINT_REPLAY_SEAL__EXACT_BLOCKER_PROVED`

Return to:
`SUB-VOZHD B — ARCHITECTURE / COMPILER / DVA / CHETIRI`.
