# SUB-VOZHD B — NODE6 ADJUDICATION + NODE7 AUTHORIZATION R1

Status:
`NODE6_ACCEPTED_AT_CAMPAIGN_GRAIN__NODE7_FRESH_COMBINED_REPLAY_AUTHORIZED_NEXT`

Campaign:
`SUB-VOZHD B — ARCHITECTURE / COMPILER / DVA / CHETIRI`

Campaign branch:
`agent/sub-vozhd-architecture-compiler-dva-chetiri-r1`

Binding central/PRE-MAIN ref:
`5b308c1a87e11a95cfd53cc72e660f641abfdb33`

## 1. Node6 bank

Worker:
`B8 — AS3R3 NODE6 COMBINED SUCCESSOR RUNTIME SEAL R1`

Worker branch:
`agent/rabochii-subv-b-as3r3-node6-combined-successor-runtime-seal-r1`

Handoff:
`84522c995706d4cbbca2295a63755c95a656c203`

Terminal tip:
`681cfb7bd8fd9738c1ad9f61320765e861e2f44e`

Terminal:
`AS3R3_NODE6_COMBINED_SUCCESSOR_RUNTIME_SEAL_COMPLETE__READY_FOR_NODE7_FRESH_COMBINED_REPLAY`

Campaign bank merge:
`c365d11807c7761650e83e13f53f77c6fb24b320`

Verified worker delta:
- 10 commits ahead / 0 behind handoff;
- exactly 10 required worker-output files changed;
- all inside the authorized B8 worker directory;
- no production code, central state, PRE-MAIN, main, sibling campaign, Node7, DiscoveryAuthority/frontier/replay, AS4I0, LiTS-I/I05/C05R2B, C08/G1, OBL037, or V3 work.

## 2. SUB-VOZHD B adjudication

Verdict:
`PASS__NODE6_ACCEPTED_AT_CAMPAIGN_GRAIN__READY_FOR_NODE7`

Accepted exact cardinality law:
`22 HISTORICAL RUNTIME ROWS -> 22 SUCCESSION MAPPINGS -> 21 DISTINCT SUCCESSOR CANONICAL OBJECTS`.

Breakdown:
- 19 predicate succession rows;
- 18 distinct successor predicates;
- sole lawful alias `{A000,A1RAPP}`;
- 3 query succession rows;
- 3 distinct successor queries;
- 0 query aliases;
- 21 distinct successor canonical runtime objects total.

Accepted sealed hashes:
- historical->successor crosswalk:
  `6038d22864840311ebe0a1a76040befb0496009657edcbc4bfd90b89fadd53c7`;
- predicate aggregate:
  `752312e62387c4ec56dd2e2e899a14ba976183a07d2e01c29ed2d1abf45c912e`;
- query aggregate:
  `0ac6d8025afbe538620db46361fefb165d2d883f9c9e6f1f9424b08b33daba30`;
- combined runtime aggregate:
  `3fdedecb92a39494fb7fbcf11b5d36d8aff376474dd72f5203e929398f78f1e1`;
- canonical-object integrity receipt:
  `e9c6e7cdc7381cb75ca86f41947203e9e188e73b522601791fda27736aa79169`;
- semantic-terrain receipt:
  `4277d27bb0851f75110d8c5cc6449c832e239fd998bf10ea46e0e096976f4d22`;
- zero-constructor/remint receipt:
  `1496e14439a175e66d028399426705f923e54bf2277de638e136d78ec093c54d`;
- combined Node6 seal:
  `df0395983de34996d33c258d0705cfc178df9cfe7982899431a0002c544481da`.

Node6 correctly preserved:
- committed Node5A-R2 canonical predicate payload:
  `ef5cd10a5af7fcaad82b7dca39f2035ff829c59fe6f45ec681f872810276ac27`;
- committed Node5B query package:
  `c185a68c3850131f701dae3b2cb20b66d947d40ef447ac69f0bcebe9d467732e`;
- Node5B package serialization exception:
  canonical JSON without trailing newline;
- canonical object representations:
  already-frozen per-object serialization laws;
- all new Node6 payloads:
  canonical compact sorted JSON + trailing newline.

Constructors invoked by Node6:
`0`.

Successor runtime objects reminted by Node6:
`0`.

## 3. Node7 governing law

Authority30 defines Node7:

`Fresh-process combined replay`

It must independently reproduce the completed successor realization from:
- frozen producer;
- frozen Node4A predicate inputs;
- frozen Node4B query inputs;
and reproduce all successor object identities and all Node6 aggregate hashes.

Authority34 corrects the predicate identity cardinality.

Therefore the exact current replay law is:

`19 PREDICATE CONSTRUCTOR CALLS + 3 QUERY CONSTRUCTOR CALLS`
-> `22 SOURCE/ROLE/TEMPLATE MAPPING RESULTS`
-> `21 DISTINCT CANONICAL SUCCESSOR OBJECTS`.

A000 and A1RAPP are two independently preserved predicate mapping rows whose constructor results lawfully converge on the same canonical predicate ref.

Node7 success is NOT "22 distinct objects."

It is:
- 22/22 mapping-row identities reproduced;
- 21 distinct canonical successor refs reproduced;
- sole alias exactly `{A000,A1RAPP}`;
- all Node6 aggregate/seal hashes reproduced.

## 4. Node7 authorization ceiling

Node7 is authorized to perform actual fresh-process reconstruction/replay.

Each independent fresh process may:
1. load exact frozen producer/contract/schema from immutable producer commit;
2. load exact Node4A 19 predicate input records;
3. validate all 19 predicate inputs;
4. invoke `construct_successor_predicate(...)` exactly 19 times;
5. preserve 19 source/role mappings and obtain exactly 18 distinct predicate refs with sole A000/A1RAPP alias;
6. load exact Node4B 3 query input records;
7. first verify Node4B query-input/package/full-bundle hashes;
8. validate all 3 query inputs against the freshly reconstructed exact predicate-ref set;
9. invoke `construct_successor_query(...)` exactly 3 times;
10. obtain exactly 3 distinct successor query refs;
11. serialize all freshly reconstructed canonical representations under the exact already-frozen object serialization laws;
12. independently reconstruct the exact 22-row historical->successor crosswalk using the immutable AS3R2 historical manifest;
13. independently reconstruct predicate/query/combined runtime aggregate payloads under Node6 ordering/serialization laws;
14. compare every result against committed Node5A-R2, Node5B, and Node6 targets.

At least two completely independent fresh processes are required.

The two processes must not consume prior-process in-memory results.

## 5. Exact replay targets

### Producer

Commit:
`cfc240aa3a64c59509eab97450a7d3603af813cc`

Producer Git blob:
`d63370dbcadc043dd2f27f5383cf36f0e84d1235`

Producer file SHA-256:
`ad7434186e5e72886333f438ed9726cec01a2d2cf740353175da938708a5ef6d`

### Node4A predicate inputs

Accepted return:
`4d66bc34c256f6bf3f9f707dda80d963881f3510`

Carrier Git blob:
`504944f9533b7385d201076e2e834b8a9446dee8`

Carrier SHA-256:
`a5687a9ed938c4c8dd80f0bfd58ffa30c4e8ca6c84629fb19c5a360ae3761155`

Predicate input count:
`19`.

### Node4B query inputs

Current campaign ancestry:
`data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/SUB_VOZHD_CAMPAIGN_INTEGRATION_R1/B_ARCHITECTURE_COMPILER_DVA_CHETIRI_R1/WORKERS/B6_AS3R3_NODE4B_QUERY_INPUT_FREEZE_R1/`

Complete future bundle:
`2cf15c20a4c65c2dcb29c6fd015260aa9ed8a70f0537927368c86e561a834e50`

Ordered query input package:
`fa68d91d4c40ff606cf4f5b06a3b213b57e3ecfc7e0c029627d7fd29413998a6`

Per-query input hashes:
- `T_Q301_2_RAW`:
  `714dde6e80801a563897f9a5cef707c7147e7fbb649473d707b8c030caecac9e`;
- `T_Q301_7_RAW`:
  `39791ee08a60ba2e8e76724200a32b0afe95411983c5eefc72c3ac19393b9416`;
- joint:
  `ec75b212e57736664e33738ffa8d69483c4c6f82c6b8199aabef414d4846b1f1`.

### Committed successor targets

Predicate side:
- Node5A-R2 mapping rows = 19;
- distinct refs = 18;
- canonical payload = `ef5cd10a5af7fcaad82b7dca39f2035ff829c59fe6f45ec681f872810276ac27`;
- role mapping payload = `081e3b8594be3d9348bc0565cd9085cca1e999ae58ef7881f040d11f5da89c7e`;
- alias payload = `5f3763afced573d70fc72233d3c28d6f2d4d2f3ce8585d050a48a43ef8b00f5d`.

Query side:
- 3 refs exactly:
  - `8a7bf5bbb1c2d8d6328dc5507416931a9c12e2c76668e0fc47af8add254c5d44`;
  - `deb71e653592d8bdb246f8c4d53359e290708d3875e38433f518b307f520c6f7`;
  - `ef8b19744ec3c06e352f7accf75efbc216ffc454905da09948763a2c54fdc053`;
- query package = `c185a68c3850131f701dae3b2cb20b66d947d40ef447ac69f0bcebe9d467732e`.

Node6:
- crosswalk = `6038d22864840311ebe0a1a76040befb0496009657edcbc4bfd90b89fadd53c7`;
- predicate aggregate = `752312e62387c4ec56dd2e2e899a14ba976183a07d2e01c29ed2d1abf45c912e`;
- query aggregate = `0ac6d8025afbe538620db46361fefb165d2d883f9c9e6f1f9424b08b33daba30`;
- combined aggregate = `3fdedecb92a39494fb7fbcf11b5d36d8aff376474dd72f5203e929398f78f1e1`;
- combined seal = `df0395983de34996d33c258d0705cfc178df9cfe7982899431a0002c544481da`.

### Historical predecessor manifest

Commit:
`aae978928d2416c23d6b1562e7ac559b106b2cf7`

Manifest:
`AS3R2_CHETIRI_FINAL_MANIFEST_SEAL_20260827/04_RUNTIME_CATALOG_BINDING_MANIFEST.json`

Git blob:
`c3e95d0705d70537e27874eaad81e9fdf76f11b7`

Historical state:
`PRESERVED__SUPERSEDED_NON_REPLAYABLE_FOR_EXECUTABLE_USE`.

Historical preimages are not needed and must not be reconstructed.

## 6. Node7 success condition

PASS requires, independently in every fresh process:
- producer identity verified;
- Node4A carrier/input hashes verified;
- predicate input validations = 19/19;
- predicate constructor invocations = exactly 19;
- predicate mapping rows = exactly 19;
- distinct predicate refs = exactly 18;
- sole predicate alias = exactly A000/A1RAPP;
- Node4B hashes/bundle verified before query construction;
- query input validations = 3/3;
- query constructor invocations = exactly 3;
- query mapping rows = exactly 3;
- distinct query refs = exactly 3;
- query aliases = 0;
- combined mapping rows = exactly 22;
- distinct combined successor refs = exactly 21;
- every committed canonical object identity/representation hash reproduced;
- exact Node5A-R2 predicate payload/mapping/alias hashes reproduced;
- exact Node5B query package/ref identities reproduced;
- exact Node6 crosswalk/predicate aggregate/query aggregate/combined aggregate/seal hashes reproduced;
- semantic terrain remains unchanged.

Across at least two fresh processes:
- all claimed replay outputs are byte-identical at the sealed evidence grain.

## 7. Boundary after PASS

Node7 does NOT:
- create successor DiscoveryAuthority/frontier/replay identities;
- revalidate AS4I0;
- run independent hostile validation;
- run LiTS-I/I05/C05R2B;
- enter C08/G1;
- launch OBL037;
- enter V3;
- modify production code;
- modify central state/PRE-MAIN/main;
- modify sibling campaign work.

Exact next node after B adjudicates a Node7 PASS:

`SUCCESSOR_DISCOVERY_AUTHORITY_FRONTIER_REPLAY_SEAL`.

## 8. Downstream sequence

`Node7 fresh combined replay`
-> `successor DiscoveryAuthority/frontier/replay seal`
-> `AS4I0 revalidation + independent hostile validation`
-> `OBL035 / C05R2B`
-> `OBL036 / C08-G1`
-> `OBL037 equal-governed-workload bakeoff`.

OBL037 remains forbidden until OBL035 and OBL036 close.

Terminal:
`SUB_VOZHD_B_NODE6_ACCEPTED__NODE7_FRESH_COMBINED_REPLAY_NEXT`
