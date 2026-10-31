# S6 ORIGIN AND BEST SUCCESSOR RECONCILIATION

**Return branch:** `agent/pyat-rabochii-845-s6-successor-consumer-crosswalk-20261030-r1`  
**Role:** independent original-function, developmental-scientific and whole-machine reconciler. Not S1–S5 author, H1, PRE-MAIN integrator, original scientific issuer or own reviewer.  
**Frozen input:** 845 branch names / 838 historical tips; 3,135 original function rows from the five immutable/regrade shards.  
**Inputs:** S1 `6a658ad3…`, S2 `3042fca8…`, S3 `ebdb51a5…`, S4 `d93e8c24…`, S5 `32dac59b…`; evidence law `f50651a2…`; HQ intake PR #547.  
**Baseline PRE-MAIN:** `750548ddbb9b4392a16ce93097b856f349e16182`.  
**Actual PRE-MAIN rechecked:** `5fc1d43e3d5412194d1f1eaa30ff448f84635e99`; `rawlsing_next` tree identical at baseline and actual head: `1d88d3fbb1d18dadfda946d9cd7f309d84afa479`. No rawlsing_next source delta.

---

## 1. Reconciliation method

The 3,135 returned AST rows are not 3,135 lost capabilities. They were normalized and joined by:

- immutable original function ID, shard, path, symbol and historical blob;
- existing S1/S3/S4 family IDs;
- same path + symbol across shards;
- same function symbol + exact historical blob across different paths;
- explicit priority-family path/symbol aliases.

Result: **1,879 function groups** covering all **3,135 rows exactly once**, plus **2 external priority cases** that are not in the 3,135 row set (P41 service and R61-R09 negative). `CROSS_SHARD_FUNCTION_GROUPS.jsonl` carries every member function ID, all shards, origin candidates and inherited branches.

**1,040 groups are production/candidate or priority-external; 841 are evidence-only/test/repro/reviewer material.** Evidence-only groups are preserved as evidence, not trash. A group is not called “unique missing” merely because a current path is absent; competing current implementations and current consumers are recorded.

Origin is the earliest available tip date among branches carrying the member row; exact creation order remains **UNPROVEN** where the original branch history was not reconstructed. All current-receiver claims are static Git/AST/text-reference facts, not executed callgraphs.

---

## 2. Priority-family census

| Priority family | Groups | Original rows | Evidence-only groups | Current state | Engineering status | Rank-1 groups |
|---|---:|---:|---:|---|---|---:|
| R61-R03 recovered universe | 119 | 510 | 0 | 8 current exact; 32 production-reference; 33 test-reference; 2 different implementation; 44 unknown | `HOLD__SCOPED_R03_RECOVERED__FULL_ORIGINAL_CONTRACT_UNPROVEN`; no-action for exact | 0 |
| R61-R08 evidence binder | 22 | 164 | 0 | 20 current-unknown/no exact path; 2 production-reference only | `HOLD__PATH_ABSENT_REVIEWED_CANDIDATE__CURRENT_ABI_CONSUMER_UNPROVEN` | 20 |
| R61-R09 forged capture | 1 external | 0 | 0 | no current capture owner | `RED__CHILD_AUTHORED_CAPTURE_AND_LOADED_BYTES` | 1 |
| P41/E04L service | 5 | 4 + external service | 0 | E03 exact current; larger P41 service absent | `HOLD__PATH_ABSENT_LARGER_SERVICE__E03_EXACT_NOT_WHOLE_SERVICE` | 5 |
| C3/R5/PR526 | 33 | 67 | 0 | 4 current exact; 5 reference-only; 2 test-reference; 7 different implementation; 13 path-absent; 2 unknown | `HOLD__CURRENT_DECODER_DRIFT__PORT_C3_G01_D01_D02_WITH_PR526_CUSTODY` | 15 |
| R9 source runtime | 103 | 216 | 0 | broker/session/binding all absent | `HOLD__PATH_ABSENT_SOURCEFREE_R9__RECONCILE_WITH_PR526_CUSTODY` | 103 |
| F7/P07 | 63 | 146 | 0 | temporal absent; P07 sealed-owner invalid; current resolver present | `HOLD__F7_TCB_AND_P07_CUSTODY_OPEN` | 54 |
| Selected-world seam | 93 | 112 | 53 | E03 exact current; selected-world contract absent | `RED__SEAM_26_PASS_1_FAIL__REPAIR_REQUIRED` | 40 |
| PE/V2K | 123 | 130 | 74 | PE `_auth` defective; V2K collection error | `RED__PE_AUTH_ROLE_REVERSAL_DEFECT__V2K_COLLECTION_ERROR` | 49 |
| R157 source configuration | 73 | 73 | 0 | config factory absent; current source alternatives | `HOLD__PATH_ABSENT_CONFIG_FACTORY__CURRENT_SOURCE_PREP_ALTERNATIVES` | 54 |

The remainder (`OTHER`, 1,246 groups / 1,713 rows) is generic production or evidence material: 100 current-code/no-action, 34 current-different-implementation, 65 reference-only, 49 test-reference-only, 407 sourcefree/operation-test holds and 841 evidence-only groups.

---

## 3. Deep priority findings and best successors

### 3.1 R61-R03 recovered universe versus original full contract

Current exact/retained code:

- `rawlsing_next/pre553_universal_workload.py` — `8e7fe00a3ed008361d9f3c501e7782b2de3a636e`
- `rawlsing_next/pre553_issued_workload.py` — `31e84f49d624f5524906e9e7839d2873106f8249`
- `rawlsing_next/pre553_native_workload_binding.py` — `dac73e484f8619088f5c6701b2b6991c07540f3b`
- `rawlsing_next/pre553_source_native_preimage_adapter.py` — `a6299c1a6e8b26bd055ced1f49e5b757f20ccd8c`
- `universal_grammar/{types,native_map,enumerate}.py` — current exact/retained code.

Evidence: R61-R03V R5 independent review `d15de915ea3388894c0f8839d28db3b23bc00367` returned `ACCEPT_SCOPED_LOCAL` for the shared capture/restore validator: author suite 16/16, retained R01 32/32, reviewer probes 5/5; genuine original-pin restore, missing/wrong-pin refusals, deletion/duplication/substitution refusals, content mutation and empty-ledger/duplicate-fact refusals. It explicitly leaves R04 joined custody/durability, R05 lifecycle/grades, F5-F8 global, original35/1890 N11, N12/Sorok, protected CI/production and J52/W52 **NOT_REACHED**.

Best successor: current `pre553_universal_workload` + `pre553_issued_workload` + `pre553_native_workload_binding` + `pre553_source_native_preimage_adapter` and current `universal_grammar` tree. Do not re-add identical code. The full original all35 warranted U/E_pre universe and original use authority remain a separate source/science court.

Action rank: 2 for current exact/no-action; 3 for reference-only groups. Concrete action: prove the full original all35 contract against the scoped R03/R03V acceptance; rerun mutation witnesses and sourcefree tests on the exact current receiver; obtain original source/science owner for any full-universe claim.

### 3.2 R61-R08 independent evidence admission/binder

Candidate source: `be1133391d91b5c2bf69299188e6f011162f269b`; module blob `3ca860e409f1d063da4cd03dd1691a89c67333f6` (117,917 UTF-8 chars). Current PRE-MAIN has **no** `pre553_universal_evidence_binding.py`.

Independent evidence: R61-R08V R8 at `2937966b3fc2388c8853bce2b984fb0cbfcdfa12` returned `ACCEPT_SCOPED_LOCAL_TRUSTED_HOST_ADMISSION_AND_CONSUMER_BINDING`. Author suite 126/126 (113 R08 + 13 C1); independent successor replay 76/76; R8 targeted probes 5/5; semantic adapters 3/3; cache-hit explicit configuration refusals preserved. Limits: full live J42/E41, live P41 progressive, repaired live E04, original source/science, production/CI, N11/N12, F6/F7/F8, actor, Sorok, R03/R09 and protected capture are **NOT_REACHED**.

Best current comparison targets: `pre553_empirical_possibility_provider.py` (`23167aa25291…`), C1 composition/state/replay (`604c8d591d4c…`, `3a5e3db8a0…`, `47e65aad5e0a…`), P41 service and J42 adapters. These are alternatives/candidates, not proven replacements.

Action rank 1. Concrete action: produce an ABI/schema/descriptor diff of the 118KB binder against the current provider/C1/J42/P41 receivers; run sourcefree positive and fault-negative tests on the exact current receiver; if no exact duplicate exists, route the reviewed candidate to H1/owner review. Do not merge solely on local scoped acceptance.

### 3.3 R61-R09 forged observation/capture negative

Independent review: `agent/opencode-pyat-r61-r09v-r2-independent-review-r1` at `25510c8d84f0ae5e452b301b017bdedf46f40b5c`; return blob `c2632d2ce3e4fb7d7630d042591bcd211bc02928`. Verdict: `REVISE` scoped local + `HOLD` central independent-capture promise.

Actual positive: independent reference and sealed observation both produced `ACCEPTED_C11_LOGICAL_RELEASE`, event_count 2, m01_m18_count 18, release `REL-R09`, repository length 1; wrong expectation refused `RESULT_MISMATCH`.

Actual negatives: D1 parent seals a child-authored observation; actual return 41 can be sealed as 42 through a monkeypatched `json.dump`. D4 child-reported loaded bytes: a fabricated `loaded_sources` digest carrying the benign tree digest is accepted while loaded code returns 41. D7 malformed non-JSON expectation crashes. Self-root caller admission is disclosed.

Best successor: no current code; the required primitive is a parent-owned observation channel for actual Python return objects and actual loaded bytes, not another HMAC over a child self-report. Owner: R09/CI engineering plus host/platform administrator for an OS-level boundary. Action rank 1 RED. No production promotion.

### 3.4 P41/E04L original service versus current exact E03 adapter

Current E03 exact: `rawlsing_next/pre553_n9_n10w_progressive_candidate.py` blob `84d404147547767be8ecd4b6e1541f5fa3a8c8a2`. It is code presence only; it is not whole N9/N10W or a P41 service.

Original P41 service: `WORKER_RETURNS/PYAT-R41-P41-GENERIC-PROGRESSIVE-N10E-N10W-SERVING-R1/runtime/p41_service.py`, blob `7d428106c79bcc56973f7c0044fc273a2b354554`, in branch `agent/rabochii-pyat-r41-p41-generic-progressive-n10w-service-r1` at `f27d1101048638bba395143a48efb7ef00bfcda4`. Functions: `P41Service.progressive`, `historical`, `publish_rule_revision`, `revoke`, `consumer_read`, `current_clock_snapshot`, plus E03 chain receipt. Original return: 19/19 sourcefree tests; three severance witnesses W1 computed-empirical edge, W2 N9 structural edge, W3 selection/currentness identity edge, each exact assertion RED then restored green; multi-conditioner, reverse A|Y, minority, zero support, null, rule revision, clock, revocation, no-current and cold replay exercised.

Current E03 exact plus P41 service is the best successor path. N10W global installation requires joint N9+N10E positive read and authorization; N11/N12 not granted; original-source measured estate held. Action rank 1. Concrete action: port P41 service onto the current E03/C1/N10E/M4/M5 receivers, run the 19 tests and three witnesses on the exact current receiver, then owner/H1 review. Do not relabel E03 test-green as full P41 service acceptance.

### 3.5 C3 decoder/R5 numeric representation versus PR526 physical snapshot

Current PRE-MAIN: `pre553_physical_decoder.py` `8732e34d0ea3f4cfffd7d33ee00f258dbc2d65dd`; `pre553_r5_codec.py` `72f8f3c03ed065e86fea4e76bb17f8e06c2bf540`; `closed35_g01_sav_numeric_representation_authority.py` **absent**.

C3 accepted six blobs: G01 `31a9afd7d91ed4cb2fb1c1aab3ef86a5fdda1f85`; physical decoder `d3d828c171ea9fdd0e90563aff6ef705f5aae2cf`; R5 codec `6000a1704d713f65e07610d81e9b3fd8bdd515ca`; three tests. HQ130 `APPROVE_AT_DECLARED_GRAIN`; OPS-01 C3 `ADOPTED`; prior six-file court 55/55. Current PR526 decoder has stronger `_SourceSnapshot` read-only/stable/TOCTOU custody and source identity; C3 has D01 declared-encoding admission and D02 opaque date/time carrier that current lacks.

Correct reading: current decoder is not a proven superset; C3 is not a drop-in replacement. Best successor is a port that combines current source-snapshot custody with C3 G01/D01/D02 and the R5 carrier, then re-runs the 55-test court on the current receiver. Source-native read/decode requires the original source custodian; synthetic/sourcefree tests are allowed but were not executed by S6. Action rank 1 for 15 groups; rank 3 for current different implementations.

### 3.6 R9 source broker/session/execution binding

Current PRE-MAIN: all three paths absent (`pre553_source_access_broker.py`, `pre553_source_session.py`, `pre553_execution_binding.py`). R9 accepted final blobs: broker `090d978bbd631820938f6f76252e09674f44ff99`, session `ac1390b861f69d21b65d9af25af9fa49cd217e08`, binding `0e11af2205a01dcf32aca3e462540040a62e9a29`. HQ202 `ACCEPT_HARDENED_EXECUTION_BINDING__SOURCE_FREE_R9_RUNTIME_COMPLETE_AT_BINDING_GRAIN`; HQ203 keeps the R9 review valid/active. Prior claims: 20 broker, 15 session, 34 binding, R7 55/55.

The current decoder has PR526 source-snapshot custody; the R9 branch decoder `b406d45fae41…` routes through broker/session but lacks that custody. Best successor: add the three R9 modules as sourcefree infrastructure, reconcile the decoder route so PR526 custody is preserved, and run the broker/session/binding/R7 courts on the current receiver. Source-path access remains subject to the source custodian; no blanket source hold on the sourcefree modules. Action rank 1 for all 103 groups.

### 3.7 F7 temporal comparison versus P07 hostile native failures

Current PRE-MAIN: `pre553_temporal_comparability.py` absent; current `pre553_source_relations.py` `5b67e3f98a5faf95a6c82700af2346fef6e306a5`.

Candidate: F7 final Python `6f6b462b1cdef54d7989f15452473383c1661594`; P07 sealed-owner variants `d9fb2c48ff6f2b68b2b8b06a47402c65cf6b7737` and `8053d30d306a3654ebf563043088311ff390bb2b`. Review chain: HQ213–HQ232 hostile rereviews; HQ232 RR-04G writable lexical custody cell reproduced; HQ236 narrower coordinated attack reproduced; HQ240 writable module-global alias `_authenticated_source_relation_decide` and non-issuer-authenticated terminal receipt; HQ245–HQ248 native Stage A/B blocked (OOB, malformed `PyObject_Call`, `PyErr_Fetch`, parity, trusted callable, decide leak, Stage B quarantine).

Best successor: do **not** promote the sealed P07 owner. Preserve current `SourceRelationResolver` unless a new owner-custody design is independently proved; repair/replace the F7 dependency on the sealed entrypoint; rerun HQ232/HQ236 negatives and the F7 49 focused + 159 regression on current receivers. Temporal arithmetic helpers may be sourcefree tested; T1/TCB/issuer/receipt authority is separate. Action rank 1 for 54 groups; current exact resolver methods are no-action.

### 3.8 Selected-world seam and S3 direct 26/1 failure

S3 actual independent receipt at branch `ed34944e253b78714a28d72b8ca2a6521ce15930`: `test_r3_s02_seam_witness.py` = **26 passed / 1 failed**, exit 1. Failure: `test_s00c_change_source_owned_synthetic_numeric_values_changes_result`, `KeyError: 'exact_probabilities'`; the consumer result does not expose `exact_probabilities["1"] == {"$exact_fraction": [1,2]}` after source-owned synthetic numeric mutation. Author-reported 18/60 is not reproduced.

Current E03 exact is present (`84d40414…`); selected-world contract, seam consumer and current P41/N9/N10W service are absent. Best successor: repair the exact seam mutation path first, rerun all 27 seam tests with zero failures; then integrate selected-world contract with current P41/C1/N9 consumer. Actor/N11/N12 authority remains ungranted. Action rank 1 RED for 40 groups; 53 evidence-only test groups preserved.

### 3.9 PE strict issuer reversal and V2K dependency collection

PE: S3 actual independent strict court at branch `e61a26ce24f023a53d6b116bb9eca2fb7b6f8e65`, PE blob `58484f4c3d9aae148d4116dcf00420c432aefcbd`, returned **4 passed / 9 failed**. The decisive failure is reverse-scoped issuer forgery not refused; `_auth` is `PROVEN_DEFECTIVE_AT_DECLARED_SCOPE`. Author court 21/21 does not close the nine strict failures. Typed/schema helpers are sourcefree candidates, not condemned by the complete-contract failure.

V2K: exact branch `694fb45085cd5e4891949921a44edb77c3f603f2` collection error; `pre553_original_workload_contract_v2_candidate` missing, so reported 24 + 111 passes are not reproducible at the exact cut. `OwnerScopePlan`, `_validate_original_against_c11`, `run_sourcefree` remain science/foreign-issuer holds.

Best successor: repair PE `_auth` reverse-scoped issuer; rerun the 13 strict cases and full K9/K10; restore/bind the V2K missing dependency at the exact receiver and rerun four suites. No science adoption from the 21 author passes. Action rank 1 RED.

### 3.10 R157 source configuration versus actual U/E_pre execution

R157 accepted source-configuration preparation: candidate `1384612bfed8d801140e00ace353779338599da3`, final acceptance/evidence `1924499ef52403a0f331b8aff9b7c7eff99bf1e2`, independent review `d81bc2c67baf933461ae6cfca468f24779cc7e44`, plan seal `4c0c619eac747afee1d8e65e1418bf2d472da4c3`. Evidence: 35/35 sources; 18,276 unique implementation IDs exactly once; 18,413 ordered physical slots; 18,250 exact relation joins; 26 explicit unmatched IDs; 35/35 actual native fixture calls returned validated `C11LogicalRelease`; 34 focused tests passed; wrong-source identity refused and correct SRC26 restored. Zero raw source respondent execution.

Current PREMAIN has no `rawlsing_next/source_configuration` factory. Current alternatives: `pre553_source_equivalence.py` (`0e7f9f6d77ef6efe2c66b04f0527bb1ab99f4ef8`), `pre553_source_local_universe_admission.py` (`b968fa16c6620cd06b191ebdb5da7da86f524393`), source-backed C11 facade. These are not proven replacements for the factory.

Best successor: map the R157 35 configurations to current source-local-universe/source-equivalence owners and verify exact item/slot identities before any old-factory recovery; then run actual U/E_pre original execution only under a separate competent source/operation grant. Action rank 1 for 54 groups; reference-only groups rank 3. Do not revert mature R157 preparation to the old `source_configuration` factory.

---

## 4. Ranked selectable actions

1. **Port C3 G01/D01/D02 + R5 carrier into 8732/72f8 while preserving PR526 source custody; run 55-test C3 court on current receiver.** Highest direct decode/representation contribution.
2. **Integrate R9 broker/session/binding as sourcefree modules and reconcile the decoder route with PR526 custody; run 20/15/34/R7 tests.** Highest source-access contribution.
3. **Diff and test the R61-R08 118KB binder against current provider/C1/J42/P41; route sourcefree positive+fault-negative receipts to owner/H1.** Highest evidence-admission contribution.
4. **Port P41 service onto current E03/C1/N10E/M4/M5; run 19 tests + 3 severance witnesses; keep N10W/N9/N11 authority held.** Highest N10W service contribution.
5. **Repair P07/F7 owner custody and TCB boundary; rerun HQ232/HQ236 negatives and F7 49/159; do not adopt sealed owner.** Highest F7/T1 contribution.
6. **Repair selected-world seam 26/1 failure; rerun 27 tests with zero failures; then current P41/C1/N9 consumer.** Blocks selected-world/N10W.
7. **Repair PE `_auth` reverse-scoped issuer and V2K missing dependency; rerun 9 strict + 24/111 exact suites.** Blocks PE/V2K science claim.
8. **Map R157 35/35 preparation to current source-local-universe/source-equivalence; run actual U/E_pre only under separate grant.** Blocks original35 execution claim.
9. **Keep R61-R03 current code; prove full all35 contract vs scoped R03V acceptance.** No duplicate recovery.
10. **Repair R61-R09 parent-owned observation channel; rerun D1/D4/D7 and real C11 positive.** Blocks native capture.

---

## 5. Accounting and limits

- All 3,135 original rows are present in `CROSS_SHARD_FUNCTION_GROUPS.jsonl` member IDs exactly once; 1,879 row-derived groups + 2 external priority cases.
- All 845 branch names/838 distinct tips are preserved in the five branch-reconciliation inputs; no branch was dropped.
- No branch code, branch test, source-native read, survey response, actor operation, PRE-MAIN merge or original-return rewrite was performed by S6.
- Historical test receipts are attributed, not re-executed. S3's actual sourcefree receipts (seam 26/1, PE 4/9, V2K collection error, selected-world 24 pass, E03 18 pass) are used as evidence; S6 did not re-run them.
- Current PREMAIN may move; this reconciliation used actual `5fc1d43e…` with the same `rawlsing_next` tree as baseline. Re-run comparisons if it moves again.
- Independent H1 #534 and S7 #538 hostile review are required at the exact return SHA. No self-adoption.
