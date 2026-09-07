# SUB-VOZHD B — NODE5B ADJUDICATION + NODE6 AUTHORIZATION R1

Status:
`NODE5B_ACCEPTED_AT_CAMPAIGN_GRAIN__NODE6_COMBINED_SUCCESSOR_RUNTIME_SEAL_AUTHORIZED_NEXT`

Campaign:
`SUB-VOZHD B — ARCHITECTURE / COMPILER / DVA / CHETIRI`

Campaign branch:
`agent/sub-vozhd-architecture-compiler-dva-chetiri-r1`

Binding central/PRE-MAIN ref:
`5b308c1a87e11a95cfd53cc72e660f641abfdb33`

## 1. Node5B bank

Worker:
`B7 — AS3R3 NODE5B QUERY MINT + REPLAY SEAL R1`

Worker branch:
`agent/rabochii-subv-b-as3r3-node5b-query-mint-replay-r1`

Handoff:
`83e002d22ee0d6136e38b5e62023a488dc36cb6e`

Terminal tip:
`b26a2b313834e0ba0a1773ebc1c25e46156dac00`

Terminal:
`AS3R3_NODE5B_QUERY_MINT_REPLAY_SEAL_COMPLETE__READY_FOR_COMBINED_SUCCESSOR_RUNTIME_SEAL`

Campaign bank merge:
`be3a4501c41f18793e59341249be64afacc10bbf`

Verified worker delta:
- 3 commits ahead / 0 behind handoff;
- exactly 10 worker-output files changed;
- all inside the authorized B7 worker directory;
- no combined successor seal;
- no successor DiscoveryAuthority/frontier/replay seal;
- no AS4I0;
- no LiTS-I/I05/C05R2B;
- no C08/G1;
- no OBL037;
- no V3;
- no production code, central state, PRE-MAIN, main, or sibling-campaign edits.

## 2. SUB-VOZHD B adjudication

Verdict:
`PASS__NODE5B_ACCEPTED_AT_CAMPAIGN_GRAIN__READY_FOR_NODE6`

Accepted exact successor queries:

- `T_Q301_2_RAW`
  -> `EmpiricalQuerySpec@1.0.0 / 8a7bf5bbb1c2d8d6328dc5507416931a9c12e2c76668e0fc47af8add254c5d44`;
- `T_Q301_7_RAW`
  -> `EmpiricalQuerySpec@1.0.0 / deb71e653592d8bdb246f8c4d53359e290708d3875e38433f518b307f520c6f7`;
- `T_Q301_2_Q301_7_RAW`
  -> `EmpiricalQuerySpec@1.0.0 / ef8b19744ec3c06e352f7accf75efbc216ffc454905da09948763a2c54fdc053`.

Exact cardinality:
`3 QUERY SEMANTIC DEFINITIONS -> 3 SOURCE MAPPINGS -> 3 DISTINCT EmpiricalQuerySpec OBJECTS`.

No query alias exception exists or was used.

Query package SHA-256:
`c185a68c3850131f701dae3b2cb20b66d947d40ef447ac69f0bcebe9d467732e`.

Canonical representation SHA-256:
- `T_Q301_2_RAW` -> `16414b17c709dca60e93c4636540febca73dd44e5d0bcd5b236c5c2a6dad3744`;
- `T_Q301_7_RAW` -> `2817fa258c30e77f4d9eff632dc570343cab63db28f5b94857b7dd9be170c89e`;
- `T_Q301_2_Q301_7_RAW` -> `0bb9a74d85091e8954206669c1b180ea05426511b644e12075a8bbd96a178bd6`.

Accepted replay:
- primary constructor invocations = 3;
- primary query mints = 3;
- two isolated constructor replays reproduce all refs, canonical representations, crosswalk, condition binding, and package identity;
- two fresh Python subprocess cross-checks reproduce the same package/query refs byte-identically;
- successor predicate remints = 0;
- predicate constructor calls = 0.

Condition provenance remains:
`A000`
through the lawful predicate alias:
`{A000,A1RAPP}`
to canonical successor predicate:
`ac3fcb4e32a41f9972004b2c31da61e9b32ba69568a795d2c1e584c9bed21be0`.

## 3. Node6 governing law

Authority30 defines:

### Node 6 — Combined successor runtime seal

Join:
- predicate canonical representations from Node5A-R2;
- query canonical representations from Node5B;
- aggregate runtime catalog hashes;
- 22-row historical AS3R2 -> successor succession crosswalk;
- semantic-terrain invariance receipts.

Node6 is a join/seal node.

It is NOT Node7 fresh combined replay.

Do not collapse Node6 and Node7.

## 4. Correct combined cardinality

Authority28 historically expected 19 predicate runtime refs + 3 query runtime refs on the old AS3R2 side.

Authority34 later corrected successor predicate canonical cardinality while preserving 19 source/role rows.

Therefore Node6 must preserve BOTH:

Historical AS3R2 succession rows:
- 19 predicate rows;
- 3 query rows;
- total crosswalk rows = 22.

Successor canonical objects:
- 18 distinct `EmpiricalPredicate@1.0.0` objects;
- 3 distinct `EmpiricalQuerySpec@1.0.0` objects;
- total distinct successor canonical runtime objects = 21.

The predicate crosswalk rows for `A000` and `A1RAPP` lawfully converge on the same successor predicate ref.

Freeze:

`22 HISTORICAL RUNTIME ROWS -> 22 SUCCESSION MAPPINGS -> 21 DISTINCT SUCCESSOR CANONICAL OBJECTS`

with sole successor predicate alias:
`{A000,A1RAPP}`.

Do not manufacture a 22nd distinct successor object.

## 5. Exact historical old-side authority

The old AS3R2 refs must be read only from the accepted historical seal:

Historical seal commit:
`aae978928d2416c23d6b1562e7ac559b106b2cf7`

Exact file:
`data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/AS3R2_CHETIRI_FINAL_MANIFEST_SEAL_20260827/04_RUNTIME_CATALOG_BINDING_MANIFEST.json`

Git blob:
`c3e95d0705d70537e27874eaad81e9fdf76f11b7`

Schema:
`AS3R2_RUNTIME_CATALOG_BINDING_MANIFEST@1.0.0`

It contains:
- all 19 historical `runtime_empirical_predicate_ref` rows keyed by AS3 atom ID;
- all 3 historical `runtime_empirical_query_spec_ref` rows keyed by AS3 query-template ID;
- historical runtime catalog binding identity:
  `88cf52def32ad8942628e90d3f954d8fc59c785c668a891290ddf74a91d19afd`.

Historical AS3R2 refs remain:
`PRESERVED__SUPERSEDED_NON_REPLAYABLE_FOR_EXECUTABLE_USE`.

Node6 may crosswalk them as historical predecessors only.

Node6 must NOT reconstruct their preimages or present them as executable runtime objects.

## 6. Node6 authorization ceiling

Node6 is authorized to:
- consume committed Node5A-R2 predicate canonical representations/manifest/crosswalk;
- consume committed Node5B query canonical representations/manifest/crosswalk;
- verify all referenced exact successor object hashes against committed canonical representation bytes;
- assemble a deterministic successor predicate catalog aggregate over the 18 distinct predicate refs;
- assemble a deterministic successor query catalog aggregate over the 3 distinct query refs;
- assemble a deterministic combined runtime catalog aggregate over the 21 distinct successor canonical objects;
- emit the exact 22-row AS3R2 historical-runtime-ref -> AS3R3 successor-runtime-ref crosswalk;
- preserve the 19-role/18-predicate alias law explicitly in the crosswalk;
- emit a complete semantic-terrain invariance receipt;
- emit provenance tying every successor row to frozen AS3 semantic source ID/content hash and exact historical AS3R2 predecessor ref;
- seal the combined successor runtime package as evidence for Node7.

Node6 may create aggregate package/catalog evidence identities.

Node6 may NOT:
- invoke predicate constructor;
- invoke query constructor;
- remint predicates or queries;
- alter any canonical successor object representation;
- reconstruct historical AS3R2 object preimages;
- create successor DiscoveryAuthority/frontier/replay identities;
- perform Node7 fresh combined replay;
- run AS4I0;
- run hostile validation;
- run LiTS-I/I05/C05R2B;
- enter C08/G1;
- launch OBL037;
- enter V3.

## 7. Node6 success condition

PASS requires:
- exact Node5A-R2 predicate manifest/canonical representations load and verify;
- exact Node5B query manifest/canonical representations load and verify;
- 18 distinct successor predicate refs exactly;
- 3 distinct successor query refs exactly;
- 21 distinct combined successor canonical refs exactly;
- 22 historical-to-successor crosswalk rows exactly;
- old predicate rows = 19;
- old query rows = 3;
- only duplicate successor target across the 22-row crosswalk is the lawful predicate alias `{A000,A1RAPP}`;
- no query aliases;
- all old-side refs match the accepted AS3R2 historical runtime manifest;
- all successor-side refs match Node5A-R2/Node5B;
- aggregate predicate/query/combined catalog hashes are deterministic and serialized;
- semantic terrain invariance passes;
- constructors invoked = 0;
- runtime objects reminted = 0.

PASS token:
`AS3R3_NODE6_COMBINED_SUCCESSOR_RUNTIME_SEAL_COMPLETE__READY_FOR_NODE7_FRESH_COMBINED_REPLAY`.

## 8. Downstream chain

`Node6 combined successor runtime seal`
-> `Node7 fresh-process combined replay`
-> `successor DiscoveryAuthority/frontier/replay seal`
-> `AS4I0 revalidation + independent hostile validation`
-> `OBL035 / C05R2B`
-> `OBL036 / C08-G1`
-> `OBL037 equal-governed-workload bakeoff`.

OBL037 remains forbidden before OBL035 and OBL036 close.

Terminal:
`SUB_VOZHD_B_NODE5B_ACCEPTED__NODE6_COMBINED_SUCCESSOR_RUNTIME_SEAL_NEXT`
