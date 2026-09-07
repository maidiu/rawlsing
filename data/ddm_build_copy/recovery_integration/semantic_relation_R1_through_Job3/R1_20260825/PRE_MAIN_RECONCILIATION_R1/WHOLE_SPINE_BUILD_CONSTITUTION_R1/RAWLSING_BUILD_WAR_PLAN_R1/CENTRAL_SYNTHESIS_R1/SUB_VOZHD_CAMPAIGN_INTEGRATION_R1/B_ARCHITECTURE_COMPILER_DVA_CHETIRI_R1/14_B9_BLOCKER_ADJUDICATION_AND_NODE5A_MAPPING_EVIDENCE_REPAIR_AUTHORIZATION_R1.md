# SUB-VOZHD B — B9 BLOCKER ADJUDICATION + NODE5A-R2 MAPPING EVIDENCE REPAIR AUTHORIZATION R1

Status:
`B9_EXACT_BLOCKER_ACCEPTED__NODE5A_R2_MAPPING_PAYLOAD_EVIDENCE_REPAIR_AUTHORIZED__NODE7_FROZEN`

Campaign:
`SUB-VOZHD B — ARCHITECTURE / COMPILER / DVA / CHETIRI`

Campaign branch:
`agent/sub-vozhd-architecture-compiler-dva-chetiri-r1`

Binding central/PRE-MAIN ref:
`5b308c1a87e11a95cfd53cc72e660f641abfdb33`

## 1. B9 bank

Worker:
`B9 — AS3R3 NODE7 FRESH COMBINED REPLAY R1`

Worker branch:
`agent/rabochii-subv-b-as3r3-node7-fresh-combined-replay-r1`

Starting HEAD:
`08313b07afd01a1abe159a06f62f5e7b674dc683`

Handoff:
`d4f29d97204851c9f99d4f64a1abc9c883d0dec8`

Terminal tip:
`86ccd0c39a314553a805e2df5466c49ecbc1cc62`

Terminal:
`AS3R3_NODE7_FRESH_COMBINED_REPLAY__EXACT_BLOCKER_PROVED`

Campaign bank merge:
`10cf2539d58303ba3e2d42809ac5e00afbe04a0d`

Verified:
- branch = 12 ahead / 0 behind Node7 starting HEAD;
- all 12 changed paths confined to the B9 worker directory;
- return artifacts complete;
- no production/central/PRE-MAIN/main/sibling/downstream work.

## 2. SUB-VOZHD B blocker adjudication

Verdict:
`ACCEPTED__EXACT_REPLAY_PROTOCOL_BLOCKER__NO_FALSE_PASS`

Blocked target:
`NODE5A_R2_ROLE_MAPPING_PAYLOAD_SHA256`

Exact digest:
`081e3b8594be3d9348bc0565cd9085cca1e999ae58ef7881f040d11f5da89c7e`.

B9 proved:
- committed material mapping rows exist;
- exact 19-row crosswalk blob:
  `26a7c35df2e6454c5e270a03b3571599bdf152fd`;
- Node5A-R2 receipts preserve the digest;
- exact payload bytes are not committed;
- no executable hash-preimage helper is committed;
- no adopted mapping-payload serialization law is committed;
- Node7 authorization forbids target-hash fitting;
- qualifying fresh Node7 replay count must therefore remain 0.

The underlying semantic/runtime realization is NOT reopened:
- predicate mappings = 19;
- distinct predicates = 18;
- sole alias = `{A000,A1RAPP}`;
- query mappings = 3;
- distinct queries = 3;
- combined mappings = 22;
- distinct successor objects = 21;
- Node6 seal remains comparison target:
  `df0395983de34996d33c258d0705cfc178df9cfe7982899431a0002c544481da`.

## 3. Independent provenance verification by SUB-VOZHD B

The complete Node5A-R2 intermediate commit sequence was independently compared from the command-only tip through terminal.

It adds, one at a time:
- `CHANGED_FILES.txt`;
- `RESULT.md`;
- `RESULT.json`;
- `ROLE_TO_CANONICAL_REF_CROSSWALK.csv`;
- `ALIAS_CLASS_RECEIPT.json`;
- `FRESH_REPLAY_RECEIPT.json`;
- `COUNT_LAW_VALIDATION_RECEIPT.json`;
- `EXACT_REF_LEDGER.csv`;
- `CANONICAL_PREDICATE_MANIFEST.json`.

No intermediate committed helper, payload carrier, or mapping-payload serialization artifact exists.

Original Node5A-R2 command:
`AS3R3_NODE5A_R2_REPLAY_SEAL/00_WORKER_COMMAND.md`
requires exact mapping replay but does not define a serialization law for the mapping payload digest.

Original fail-closed Node5A at:
`34caf24a79a0b49eae4cd0937e7b13f56bb38c2e`
also records mapping identity reproduction but commits no mapping-payload byte carrier or serialization law.

Therefore:
`MISSING_PREIMAGE_LAW_IS_REAL__NOT_HIDDEN_IN_COMMITTED_NODE5A_HISTORY`.

## 4. Ownership / authority holding

This blocker is an evidence-completeness defect inside SUB-VOZHD B's existing AS3R3/Chetiri proof chain.

A bounded repair may recover and seal missing replay evidence without:
- changing semantic authority;
- changing producer authority;
- changing Node4A inputs;
- changing Node5A-R2 mapping rows;
- changing any successor predicate identity;
- changing Authority34 count law;
- changing Node4B/Node5B/Node6 evidence;
- changing terrain/fairness.

Therefore SUB-VOZHD B may commission the forensic evidence-repair worker.

No HQ adoption is required merely to RECOVER pre-existing exact evidence or prove an already-used deterministic serialization law, provided the repair is independently grounded and non-semantic.

SUB-VOZHD B may campaign-adjudicate a recovered evidence supplement.

SUB-VOZHD B may NOT invent and retrospectively adopt an arbitrary serialization convention selected because it matches the target digest.

If independent provenance cannot establish the exact preimage/law, the repair must fail closed and return:
`READY_FOR_VOZHD_HQ_ADJUDICATION__NODE5A_R2_MAPPING_REPLAY_PROTOCOL_IRRECOVERABLE`.

## 5. Exact repair objective

Produce ONE of:

### Outcome A — exact preimage recovery
Recover the exact bytes whose SHA-256 is:
`081e3b8594be3d9348bc0565cd9085cca1e999ae58ef7881f040d11f5da89c7e`

and commit those bytes in an auditable lossless carrier plus:
- byte length;
- media type/encoding;
- exact SHA-256 reproduction;
- provenance showing why these are the original mapping payload bytes, not a target-fit candidate;
- parser/decoder sufficient to recover the exact 19 material mapping rows.

### Outcome B — exact serialization-law recovery
Recover an exact deterministic serialization algorithm/protocol from independently grounded evidence that, when applied to the unchanged committed 19 Node5A-R2 mapping rows/material, produces the exact payload bytes and digest above.

The law must specify all identity-affecting details, including as applicable:
- input field set/projection;
- row order;
- object/list shape;
- field order or sorted-key rule;
- separators;
- Unicode handling;
- newline/trailing-newline law;
- CSV dialect if CSV;
- normalization/coercion rules;
- exact byte encoding.

The law must be proven from independent provenance, not chosen by trying encodings until SHA-256 matches.

## 6. Forbidden target fitting

The repair worker must NOT:
- enumerate arbitrary plausible serializations and select the one whose hash matches `081e3b...`;
- brute-force whitespace/newline/field-order variants against the target;
- declare a new retrospective law merely because it reproduces the target;
- alter the target digest;
- alter the 19 mapping rows;
- alter successor refs;
- alter Node5A-R2 accepted artifacts.

The target digest may be used for FINAL VERIFICATION only after an independently grounded preimage/law has been recovered.

## 7. Lawful provenance search surface

The repair worker shall inspect, in priority order:
1. immutable Node5A-R2 commit history;
2. original fail-closed Node5A artifacts/history;
3. exact producer/Node4A construction surfaces;
4. reachable committed replay/helper conventions that Node5A demonstrably invoked or copied;
5. immutable PR/commit/workflow evidence if it positively records the payload/preimage generation;
6. any exact retained artifact referenced by a committed Node5A receipt.

Mere similarity to another worker's serialization convention is not authority.

## 8. PASS consequence

If repair PASS is independently proven:
1. return to SUB-VOZHD B;
2. bank repair evidence;
3. campaign-adjudicate it as supplemental Node5A-R2 replay evidence;
4. freeze the exact recovered preimage/law for Node7;
5. recommission Node7 fresh combined replay from the repaired campaign head;
6. Node7 must still execute the actual two-process constructor replay and reproduce all Node6 targets.

Repair PASS itself does NOT close Node7.

## 9. Downstream freeze

Until repair PASS + B adjudication:
- Node7 remains BLOCKED;
- successor DiscoveryAuthority/frontier/replay seal is not launched;
- AS4I0 is not launched;
- C05R2B is not launched;
- OBL036 is not entered;
- OBL037 remains forbidden.

Terminal:
`SUB_VOZHD_B_B9_BLOCKER_ACCEPTED__NODE5A_MAPPING_EVIDENCE_REPAIR_NEXT__NODE7_FROZEN`
