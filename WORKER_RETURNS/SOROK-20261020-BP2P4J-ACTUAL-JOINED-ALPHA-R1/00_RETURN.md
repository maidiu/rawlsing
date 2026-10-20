# SOROK BP2P4J — ONE JOINED BP2→BP4 SOURCE-FREE PERSON/PRODUCT CHAIN R1

## 0. Identity, custody and scope

| Binding | Value |
|---|---|
| Repository | `maidiu/rawlsing` (PRIVATE) |
| Branch | `agent/rabochii-sorok-20261020-bp2p4j-joined-technical-alpha-r1` |
| Exact sealed startup | `267e97ff88acc4b19ea832bf8147f3ac2fa3bc81` (remote branch tip before work; no prior worker commits) |
| Commission | `WORKER_COMMISSIONS/SOROK-20261020-BP2P4J-ACTUAL-JOINED-SOURCEFREE-PERSON-ALPHA-R1/00_COMMISSION.md` at the startup |
| Pinned BP2 input | `agent/rabochii-sorok-20261020-bp2-joined-event-rule-action-positive-r1@5065e2e6934e9d5bca800cbf88c79e461bcf2393` |
| Pinned BP4 input | `agent/rabochii-sorok-20261020-bp4-c10-c12-continuing-person-alpha-r1@d868e82c7c83def2df18295244d93af9706e647f` |
| Write scope | only `WORKER_RETURNS/SOROK-20261020-BP2P4J-ACTUAL-JOINED-ALPHA-R1/**` |
| Model / harness | DeepSeek V4.1-Flash, reasoning MAX requested, one DeepSeek Harness session; no model/harness/sub-agent/paid-provider switch |
| Native authority | **NOT_GRANTED** |
| Upstream edits | **none**; 150 staged files verified byte-identical to their origin commits |

**Active-worker check.** The remote BP2P4J branch existed and pointed at exactly the sealed startup
`267e97ff8`; no prior BP2P4J worker commits existed. I created an isolated worktree at that commit and did
not write to BP2, BP4, BP1, BP3, C9R/C9RI, Pyat, PRE-MAIN, production or any other branch. BP2 and BP4
are immutable inputs; their branches were not restarted or reset.

**What this return is.** The missing producer→user-product causal edge is built: BP2's real
`JoinedProducer` C8/C9/E2 output is consumed by BP4's real `C10`/`C12`/`M6`/A0–A3 implementation, with
the committed BP2 practice materialized into real actor/world state and a real downstream consequence in
the A2 offscreen life. It is an L1 physically executed TEST_ONLY whole-chain result. It is not native
science, not a C11 weld and not a native generated person.

---

## 1. THE MANDATORY DISCREPANCY IS CLOSED, LITERALLY AND BY RECOMPUTATION

**Literal origin (present on this machine).** The surviving BP2 evidence runtime
(`…/BP2-…/evidence/runtime/positive`, the run that produced the committed
`evidence/bp4_downstream_afterstate.json`) is consumed **in place, read-only**:

| Literal BP2 identity | Value |
|---|---|
| C9 target | `950a4c7903cbe832c72d234a0095946720910c23c8235a28c3118afd8fc1b9f8` |
| Target record hash | `8d784d48096f4d32d0df3d7c659a23b501681877a948580e0c0150ac60efcd3e` |
| Consumed state hash | `4907a662d2494d9f7949d1f809195264e001f90d39021feb73e5a75cc31c656d` |
| C8 occurrence / state digest | `OCC-0001` / `058d006c1ce79d2783b02a3bb4e2f92d0672aec9b406b5f3312453f9c5608b4b` |
| E2 receipt | `19349fd6fded91f222d50ef5774deab1203619c390fb554e2bd4970e9c7f05aa` |

`bp4.c10.receive` verifies that runtime's BP3 keyed proof and external anchor, the sealed target row and
its digest, both BP1 snapshots and the OUT9 readset; `bp4.product` then runs A0–A3 normally
(`evidence/literal_origin_join.json`: assertion `PASS`, 30/30 identity rows exact, 0 recomputed). The C12
practice points at the literal target record, and the A2 offscreen repair completes (`completed_units=4`).
This is the direct answer to "BP4 must actually read the BP2 target `950a4c79…`".

**Why a literal target cannot be reproduced from the committed return.** BP2's C8 commit receipt
identity binds (a) a random TEST_ONLY HMAC key generated per run and (b) the absolute journal path
(`capability nonce = f(journal_id)`, and the C8O capability fingerprint embeds
`journal_id`). Both are deliberately excluded from the committed BP2 return. Therefore the literal
`95ac61ff…` receipt, E1 hash, response/grant hashes, target id, record hash and consumed hash cannot be
re-derived elsewhere. What *is* reproducible is reproduced **exactly**: occurrence id, C8 state/content/
identity digests, writer version, both BP1 actor source/snapshot hashes, RULE_A and RULE_T semantic
hashes, the practice label and the E2 act/actuator/occurrence.

**Fresh reproducible join (committed tests).** `reunion.build_fresh` runs BP2's actual producer in this
return's own runtime root. The evidence run yields C8 digest `058d006c…` (identical), target
`d9f25cc6…`, record `0f75841f…`, consumed `60a4734e…`, E2 `94da6f9a…`. The reconciliation receipt
(`evidence/joined_positive.json → reconciliation`) classifies every field:
**20 EXACT** (path/key independent) and **10 RECOMPUTED** (path/key bound), with the explicit origin-change
explanation. No field is silently passed through.

**The old BP4 root is not the consumer.** `tests/test_joined_security.py` builds BP4's standalone product,
shows its historical target is `08a8d89a…`, and shows the joined product's A0 reports the BP2 target and
refuses a product root bound to a different run (`JOIN_BINDING_SOURCE_MISMATCH`) or with no post-BP2 world
root marker (`TIME_COORDINATE_HOLD`).

**The shape-valid envelope is not trusted.** BP4's `bp4.bp2_compat.validate_envelope` accepts a
shape-correct envelope naming the literal target. `bp2p4.envelope.verify_producer_envelope` re-derives
every field from the physical artifacts and refuses it
(`SHAPE_VALID_ENVELOPE_NOT_BACKED_BY_ARTIFACTS`). Native-smuggling envelopes are refused the same way.

---

## 2. FINDINGS

### 2.1 The whole chain physically executes on one root

| Stage | Actual implementation | Evidence |
|---|---|---|
| BP1 two histories | `bp1.composer.build_two_actor_life()` (pinned) | two distinct actor ids/sources/snapshots, distinct G18 histories |
| BP2 C8 | `bp2_joined.producer.JoinedProducer` keyed append + external anchor | `OCC-0001`, `058d006c…`, keyed proof verified |
| BP2 E1 | `bp2_joined` E1 witness over the actual OUT9 read | content carries occurrence id, C8 state digest, commit receipt, BP1 causal parents |
| BP2 CAN008 `RULE_A` | TEST_ONLY rule resource through `bp2_joined.ports.CAN008RulePort` | `aa5033ca…`, response `9b881a3a…` (fresh) |
| BP2 CAN011 `RULE_T` + grant | separate owner resource + grant | `457894cf…` (dependency `aa5033ca…`), grant `45592390…` |
| BP2 durable target | C9R `CandidateStore` atomic full-record commit | target `d9f25cc6…`, record `0f75841f…` |
| BP2 performed E2 | independent TEST_ONLY actuator/occurrence | receipt `94da6f9a…`, act `inspect_with_tool`, action 217 ≥ commit 202 |
| BP4 C10 | `bp4.c10.receive` re-verifies C8 proof, C9 target, both snapshots | A0 `c9.target_id` == BP2 target, `c8.state_digest` == `058d006c…` |
| BP4 C12 | `bp4.store.C12Store` append-only SQLite | root branch, checkpoint, cold reentry |
| BP4 M6/V2 | current `rawlsing_next.m6_actor_safe_expression` | `ARRIVAL` READY; unperceived offscreen `NONRENDERABLE`; after ATTEND `PERMIT_FIRST_PERSON_KNOWLEDGE` |
| A0–A3 | `bp4.product.BP4Product` inherited unchanged | observe/say/do/attend/wait/travel/other/reentry/fork |

`bp2p4.product.JoinedProduct` subclasses BP4's real product and replaces only seed construction. No
shadow C8/C9/C10 engine is introduced.

### 2.2 The BP2 practice has real downstream consequences

The committed `V3MS_PRACTICE` target (`c9p:coordinated_material_inspection`) and the performed E2 act
(`inspect_with_tool`) are materialized into actor A's `projects`/`tools_remaining` and the workshop tool
resource. Consequences, all exercised through the ordinary product:

* A0 `self.state.projects` contains the practice record whose `source_target_ref` is the BP2 target
  record hash, and `tools_remaining == 1`;
* the offscreen worker can complete a market repair at world clock 40 because the tool was inspected
  (`completed_units 3→4`);
* with the same committed target but **no performed E2**, there is no practice, no tool, the offscreen
  event is a lawful `OFFSCREEN_NO_CHANGE` and `completed_units` stays 3.

That is a stored-state consequence, not a narrative difference.

### 2.3 Seven load-bearing source severances + three deeper variations

Named assertion: `bp2p4.assertion.joined_downstream_a0_a2_assertion` (the same function in every trial).

| # | Edge | Physical cut | RED message | Restore |
|---:|---|---|---|---|
| 1 | `BP2_C8_PROOF` | tamper external anchor watermark | `BP2_C8_PROOF_INVALID` | same root, exact bytes |
| 2 | `BP2_ACTOR_HISTORY` | BP1 actor source not the one inside the C8 occurrence | `BP1_ACTOR_SOURCE_NOT_MATCHING_BP2_C8` | same root, original source |
| 3 | `BP2_RULE_A` | delete the committed CAN008 response row | `BP2_RULE_A_RESPONSE_ABSENT` | same root, exact bytes |
| 4 | `BP2_RULE_T` | delete the separate CAN011 authorization row | `BP2_RULE_T_AUTHORIZATION_ABSENT` | same root, exact bytes |
| 5 | `BP2_TARGET_HASH` | rewrite the sealed target preimage | `BP2_C9_CONSUMED_HASH_MISMATCH` | same root, exact bytes |
| 6 | `BP2_E2` | E2 receipt binds the focal actor as its own actuator | `BP2_E2_SELF_PERFORMED` | same root, original source |
| 7 | `BP4_C10_M6_ACCESS` | delete actor A's durable perception of the arrival | `A0_CLAIM_SET` (empty claim set) | fresh C12 root, same BP2 artifacts |
| + | `BP2_OTHER_HISTORY_ALIASED` | other actor's snapshot replaced by the focal actor's | `BP1_OTHER_SNAPSHOT_NOT_MATCHING_BP2_C8` | same root |
| + | `BP2_E2_NOT_PERFORMED` | no E2 receipt | `A0_E2_ADMITTED` | same root |
| + | `BP2_PRACTICE_NOT_MATERIALIZED` | practice withheld from the world | `A0_PRACTICE_NOT_ESTABLISHED` | same root |

Receipt: `evidence/severance_receipt.json` (`all_primary_proved: true`,
`all_supplementary_proved: true`). No cut is an authored mock dict: cuts 1–5 mutate the real artifact
bytes or SQLite rows, cuts 6/7 remove the real source edge, and each restoration re-runs the same
assertion.

### 2.4 Positive, NO_CHANGE and DENY

| Branch | Actual result |
|---|---|
| BP2 positive | `CREATE`, sealed target, E2 admitted, consumed hash equal |
| BP2 NO_CHANGE | empty CAN008 registry: `RESPONSE REFUSED`, target branch `NO_CHANGE`, **0 target rows**, occurrence preserved |
| BP2 DENY | self-issued CAN011 request: `PERMISSION_SELF_ISSUED`, **0 target rows**, occurrence preserved |
| product NO_CHANGE | `inspect` and `attend` return `NO_CHANGE`, no state mutation |
| product DENY | `repair` → `MATERIAL_EXHAUSTED`; `repair` at market → `WRONG_LOCATION`; `travel("nowhere")` → `WORLD_LOCATION_UNKNOWN`; address absent other → `OTHER_ACTOR_NOT_PRESENT` |
| no-effect alternative | no performed E2 → no practice/tool → `OFFSCREEN_NO_CHANGE`, `completed_units=3` |

Receipt: `evidence/alternatives_receipt.json`.

### 2.5 Cold reentry, fork and independent offscreen life

* **Cold reentry**: one process builds and advances to world clock 40; a second fresh process reopens the
  same root and reads the same BP2 target/consumed hash, same C8 digest, same clock and the same claim
  set (`evidence/cold_reentry.json`, `equal: true`).
* **Fork**: `branch_leave` and `root` share the pre-fork rows hash-for-hash; leaving the tool lets B
  complete the market work (4), taking it produces a lawful no-change (3); post-fork event sets differ
  (`evidence/fork_receipt.json`).
* **Independent offscreen life**: the clock-40 event is produced by world time and a world-owner receipt,
  not by a user sentence; A cannot see it until travel + ATTEND, and M6 refuses the pre-ATTEND claim and
  permits it afterwards.

### 2.6 Clock/owner congruence (no silent ordering)

Two declared domains: `BP2_TEST_ONLY_LOGICAL_CLOCK` (event/commit 202, E2 action 217) and
`BP4_TEST_ONLY_WORLD_CLOCK` (origin 10, offscreen 40). The only declared relation is same-process
emission order (`BP2_C8_COMMIT → BP2_C9_TARGET_COMMIT → BP2_E2_ADMISSION → BP4_SEED_BIND →
BP4_WORLD_ROOT_CREATE`); `numeric_ordering_used` is `false`. A C12 root without the recorded post-BP2
marker is refused with `TIME_COORDINATE_HOLD`
(`evidence/clock_docket.json`, `tests/test_joined_product.py`).

### 2.7 Exact source closure

`vendor/source_manifest.json`: 150 files, origin commits BP2 `5065e2e` and BP4 `d868e82`, with SHA-256 and
Git blob per file. `tools/stage_sources.py verify` re-reads every origin object. After import, every
loaded upstream module is checked against a manifest hash, and the two live `rawlsing_next` modules are
checked against the blobs pinned by BP4 (`m6_actor_safe_expression` `74d9701c…`, guard `e0528d65…`).
BP2's published BP1/G18/C9R hashes reproduce exactly (`source.py cbecd864…`, `ledger.py e68901da…`,
`composer.py 358a3c6e…`, `c9_bridge.py c954e7d9…`, `joint.py 755820d7…`,
`identity.py 595b030b…`).

### 2.8 Two upstream defects/residuals found and reported (not patched)

1. **BP4 `C12Store.verify` is self-referential.** It compares `digest(body)` where `body` still contains
   its own `hash`, so every non-empty table reports a false error. The rows were written as
   `digest(body without hash)`. `bp2p4.c12_verify` verifies the real chain and the disagreement is
   recorded in `evidence/security_receipt.json`. BP4 is unmodified.
2. **Append-only is a process guard, not an external boundary.** Raw SQLite access can `DROP` the C12
   trigger and delete rows; remaining rows stay valid and completeness is only detectable against an
   out-of-band `chain_digest` recorded before the attack. Typed residual, tested honestly.

---

## 3. INTERPRETATIONS AND ALTERNATIVES

* **What is genuinely joined.** The BP2 target is not displayed as metadata: it is the source of the C10
  read, of actor A's practice state, of the workshop tool state, and therefore of the A2 offscreen
  outcome. Cutting the target, the E2, the response row, the authorization row, the C8 proof or the
  actor history changes the same A0/A2 observation.
* **Why the literal and the fresh runs both matter.** The literal run proves the *actual committed BP2
  artifacts* are consumed. The fresh run proves the chain is reproducible from committed sources and
  tests. Neither substitutes for the other; the reconciliation table states exactly which identities
  survive re-derivation and why the others cannot.
* **What is not claimed.** The actors are TEST_ONLY fixtures; the rules, grant, E2, C8 key/anchor and
  world are TEST_ONLY; no psychology, developmental law, genealogy, native actor or native person is
  created. No response text is stored as durable actor state; the durable payload is C9R's fixed
  practice label plus declared evidence refs.
* **Alternatives considered.** (a) Reusing BP4's own `build_seed` — rejected: it rebuilds the historical
  BP1-only C9 target and would leave the discrepancy open. (b) Hand-building an envelope from the BP2
  evidence JSON — rejected: shape-valid but unbacked; the emitted envelope is re-derived from the
  physical artifacts and a forged one is refused. (c) Comparing BP2 logical time numerically with BP4
  world time — rejected: declared process order only, with a typed hold.
* **The `RULE_T` dependency field.** C9R's accepted contract keys the target registry on the CAN008
  response-rule hash; the separate `RULE_T` identity is carried as its own `rule_t_content_hash` and its
  exact `rule_id` inside the sealed authorization preimage. This is a C9R contract property, not a BP2P4J
  choice; changing it would be a C9R/CAN011 owner decision.

---

## 4. THREE SEPARATE COURTS

**ENGINEERING — `ACCEPT_SCOPED_SOURCEFREE_JOINED_PRODUCT_ALPHA`.**
One same-root BP2 C8/OUT9→BP1 two histories→C9 RULE_A/RULE_T→persisted target→independently performed
E2→BP4 C10→C12→A0–A3 actually runs; the literal BP2 target `950a4c79…` is consumed when the origin
runtime is present, and the fresh reproducible run matches every path-independent identity exactly;
positive/NO_CHANGE/DENY; cold reentry and fork; seven load-bearing same-assertion severances plus three
variations; source closure and no upstream edits. Scope excludes native cutover, production trust and
native person.

**SCIENTIFIC — `ACCEPT_SCOPED_TEST_ONLY_FINITE_MATERIAL_PRACTICE__HOLD_NATIVE_PSYCHOLOGY`.**
A finite source-free material/relational situation produces a declared practice target, a changed
later world outcome and lawful alternatives (no-effect, no material, wrong place, absent other). The
independent other acts on world time with its own owner receipt. No trait, need, affect, attachment,
family or developmental coefficient is inferred; a role, seed, fixture or repeated event is not acquired
human personality. Native CAN008/CAN011 science remains with its owners.

**AUTHORITY — `HOLD`.**
Pyat N11/N12 (the R53 J52/W52 user STOP is respected and no workaround is attempted), ADP007/010/015/
016/017/019/020, CAN008 `RULE_A`, CAN011 `RULE_T`/grant, native E2, C8 D1/D2/D3, C11 weld, native C12 and
A4/A5 remain unissued. No self-adoption; HQ owns intake and any independent review.

---

## 5. HQ ACTIONS, COMPETENT OWNERS AND EXACT DECISIONS

| Action | Owner | Exact decision / receipt | Current |
|---|---|---|---|
| Intake the joined L1 product | Sorok HQ | accept/reject scoped engineering and scientific scope; no native grade follows | candidate |
| Issue the first concrete CAN008 rule | CAN008 R2 concrete issuer | exact rule body/version/hash, subject/readset scope, alternatives, valid-empty, effective/revocation | `UNISSUED` |
| Issue the separate target rule + grant | CAN011 target owner | exact `RULE_T` plus CREATE/NO_CHANGE/DENY grant with before/write sets | `UNISSUED` |
| Admit the occurrence | ADP019 court | exact event id/hash/time + owner receipt | `ADP019_ADMISSION_RECEIPT_ABSENT` |
| Bind opportunity/encounter | ADP010 owner | AVAILABLE→OPPORTUNITY→ENCOUNTER for this subject | `UNISSUED` |
| Issue actor and independent other | ADP007 / ADP015 | native actor genesis and source-qualified other | `TEST_ONLY_FIXTURE` |
| Admit a performed E2 | native actuator owner | receipt bound to consumed hash and post-commit time | `TEST_ONLY_ACTUATOR` |
| Close C8 D1/D2/D3 | C8 writer/key/anchor/ADP019 owners | all-writer cutover; production KMS+anchor; native admission | `HOLD` |
| Issue a real world | Pyat HQ | source-qualified world within rights (respecting the user STOP) | `HOLD` |
| Repair BP4 `C12Store.verify` | BP4 owner | verify `digest(body without hash)` | `UPSTREAM_DEFECT_REPORTED` |
| Weld C11 / generate C12 | C11/C12 authorities | separate grants after the above | `HOLD` |

---

## 6. COURT MATRIX, COMMANDS AND ARTIFACTS

### 6.1 Matrix

| Court | File | Tests | Result |
|---|---|---:|---|
| source closure / pinned imports | `test_source_closure.xml` | 4 | 4 PASS |
| joined product positive | `test_joined_product.xml` | 10 | 10 PASS |
| seven + three severances | `test_joined_severance.xml` | 7 | 7 PASS |
| security / forgery / residuals | `test_joined_security.xml` | 12 | 12 PASS |
| **new total** | | **33** | **33 PASS / 0 RED** |
| original BP2 suite (pinned) | `original_bp2_50.xml` | 50 | 50 PASS |
| original BP4 suite (pinned) | `original_bp4_15.xml` | 15 | 15 PASS |
| **grand total** | | **98** | **98 PASS / 0 RED** |

The original suites run from the staged byte-exact copies (`vendor/bp2`, `vendor/bp4`); BP4's suite is
run with the checkout root on `PYTHONPATH` because it imports the live pinned M6 module, exactly as in
its own return.

### 6.2 Commands

```bash
python3 tools/stage_sources.py verify         # re-read all 150 origin objects
python3 tools/run_courts.py                   # every court + every evidence artifact
python3 run_joined.py --root DIR demo         # A0–A3 CLI over a fresh joined chain
python3 run_joined.py --root DIR observe      # cold reentry in a new process
python3 run_joined.py --root DIR --origin <bp2-origin-runtime> assert
```

### 6.3 Evidence

| Artifact | Contents |
|---|---|
| `evidence/joined_positive.json` | fresh BP2 run, custody, emitted envelope, assertion receipt, reconciliation |
| `evidence/literal_origin_join.json` | literal `950a4c79…` join + PASS receipt + 30/30 exact reconciliation |
| `evidence/custody_ledger.json` | 18-step cross-domain ledger and 10 verified producer→consumer links |
| `evidence/severance_receipt.json` | 7 primary + 3 supplementary trials with cut/RED/restore |
| `evidence/alternatives_receipt.json` | BP2 and product NO_CHANGE/DENY, no-performed-E2 no-effect |
| `evidence/cold_reentry.json`, `evidence/fork_receipt.json` | two-process reentry and lawful branch divergence |
| `evidence/clock_docket.json` | both clock domains, declared process order, no numeric ordering |
| `evidence/security_receipt.json` | closed controls, typed residuals, upstream-defect receipt |
| `evidence/source_manifest_summary.json`, `environment_passport.json`, `privacy_and_law.json` | closure, environment, law |
| `evidence/not_run_inventory.json`, `native_functional_gap.json`, `authority_hold_register.json`, `source_actor_performer_clock_gap.json` | holds and exact missing native functions |
| `evidence/court_results.json`, `evidence/junit/*.xml`, `evidence/logs/*.log` | executed courts and logs |

---

## 7. DONE / REMAINING / BLOCKER / DELTA

* **DONE** — real BP2 producer→BP4 C10/C12/A0–A3 chain on one root; literal origin consumed; practice
  materialized with a downstream A2 consequence; positive/NO_CHANGE/DENY; seven + three severances;
  cold reentry; fork; M6 boundary; 150-file source closure; 98/98 tests.
* **REMAINING** — native CAN/ADP/actor/world/E2/C8 authority; C11/C12; A4/A5; BP4 `verify` defect repair;
  independent HQ acceptance.
* **BLOCKER** — none for the lawful source-free work. Native progress is blocked only by the unissued
  scientific/source authority, which this worker cannot mint.
* **DELTA** — BP4 no longer consumes its historical BP1-only C9 target; the BP2 committed target and E2
  are the actual source, and the A0/A2 product changes when they change.

---

## 8. NOT_RUN / LIMITS

1. **No native authority.** Every actor, world, rule, grant, event and performed action is TEST_ONLY.
2. **Literal origin is local-only.** The BP2 origin runtime contains a random key and a path-bound
   journal; a fresh clone will skip that cross-check (`BP2_ORIGIN_RUNTIME_ABSENT`) and still run every
   reproducible court. Set `BP2P4J_ORIGIN_RUNTIME=<dir>` to point at a preserved runtime, or
   `BP2P4J_ORIGIN_RUNTIME=none` to force the absence path.
3. **The fresh target differs from the literal target** by the documented path/key binding; all
   path-independent identities match exactly.
4. **Historical upstream REDs not re-run here**: G13's 73 RED, C9R's 62/28 author divergence and the other
   BP1/BP3 regression suites are not part of BP2's 50 or BP4's 15 and were not re-executed. They remain
   preserved historical evidence, not promotions.
5. **BP4 `C12Store.verify`** is reported as an upstream defect and worked around by an independent
   verifier; BP4 is unmodified.
6. **Raw DB access residual** for the C12 append-only guard (typed, not fixed).
7. **No production deployment, no C11 weld, no native generated person, no human-experiential claim.**

---

## 9. PUBLICATION

| Item | Value |
|---|---|
| Branch | `agent/rabochii-sorok-20261020-bp2p4j-joined-technical-alpha-r1` |
| Exact sealed startup | `267e97ff88acc4b19ea832bf8147f3ac2fa3bc81` |
| Substantive return commit | `9e7143f53271c1079bbbdc92ab49c314e606d6d6` |
| Delta commit (origin override + refreshed evidence) | `d405a065a3ca0429a4a81d325d7c7b8a5f1c6564` |
| Remote verification of that tip | `git ls-remote` returned `d405a065a3ca0429a4a81d325d7c7b8a5f1c6564`, and a detached worktree at that exact SHA re-ran the whole court green |
| Push | ordinary non-force (`267e97ff8..9e7143f53..d405a065a`) |
| Final remote SHA | `PUBLICATION_RECEIPT.json`, `evidence/remote_readback.json`, and the direct `git ls-remote` readback reported in the worker's final response |

Only this return subtree is committed. No upstream file, test, native module, Pyat artifact, PRE-MAIN
document, production path or other worker branch was modified. No self-adoption, no additional reviewer,
no new worker.
