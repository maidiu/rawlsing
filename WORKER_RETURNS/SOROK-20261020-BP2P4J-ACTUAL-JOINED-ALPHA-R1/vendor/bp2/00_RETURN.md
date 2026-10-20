# SOROK BP2 — JOINED ACTOR/EVENT/RULE/PERFORMED-ACTION PRODUCER R1

## 0. Identity, launch truth, custody and scope

| Binding | Value |
|---|---|
| Repository | `maidiu/rawlsing` (PRIVATE) |
| Branch | `agent/rabochii-sorok-20261020-bp2-joined-event-rule-action-positive-r1` |
| Exact sealed startup | `e699fed59925a3d7b3f02805f85771ae2df32be8` |
| Commission blob | `32c4f08ead12a0cdaa34c912d42edccce9311087` (verified by `git hash-object` against the startup tree) |
| Write scope | only `WORKER_RETURNS/SOROK-20261020-BP2-JOINED-ACTOR-EVENT-RULE-ACTION-R1/**` |
| Model / harness | user-selected DeepSeek V4.1-Flash, reasoning MAX requested, one local DeepSeek Harness session; no model/harness switch, no sub-agent, no paid API call |
| Native authority | **NOT_GRANTED** |
| Upstream edits | none; 30 staged files verified byte-identical to their origin commits |

**Active-worker check.** At launch the remote
`agent/rabochii-sorok-20261020-bp2-joined-event-rule-action-positive-r1` ref existed and
pointed at exactly the sealed startup `e699fed59`. No prior BP2 worker commits existed, so
there was no live BP2 session, dirty BP2 tree or remote work to preserve. I created an
isolated worktree at the sealed commit and did not touch BP1, BP3, C9R, C9RI, BP4, Pyat,
PRE-MAIN or any production path. BP1 (`be9f3a9e1`/author `b4e07ef51`), BP3 (`7faaa0722`) and
C9RI (`5753d9b4f`) were treated as returned and were not restarted.

**What this return is.** The first physically joined source-free causal chain over the three
already-existing engines: BP1's two independently acting, materially situated actor
histories → BP3's keyed exclusive journal, external monotonic anchor and accepted OUT9
read-only consumer → C9R's actor/event/response/target/commit/later-action consumer. It is
an L1 physically executable technical positive with real positive / NO_CHANGE / DENY paths,
cold-process verification and ten same-assertion source severances. It is **not** L2 native
science and **not** L3 product.

---

## 1. FINDINGS

### 1.1 The joined chain actually executes as one causal chain

`bp2_joined/producer.py::JoinedProducer` runs six separable stages over one root:

| Stage | Actual mechanism | What is bound |
|---|---|---|
| `world_occurrence` | BP1 `build_two_actor_life()` + `build_world_occurrence()` | actor A snapshot, other actor B snapshot, shared objective, material receipt, both performed actions, causal parents, logical clock |
| `c8_exclusive_append` | BP3 `ExclusiveJournal.append_occurrence` | keyed capability, version CAS, external anchor row, proof sidecar |
| `out9_read` | `c9_event_ingress.receive_event` + accepted `C8ReadOnlyConsumer` | exact occurrence id, state digest, commit receipt id, writer version, canonical byte readset |
| `e1_binding` | C9R `ActorIdentityRecord`, `make_event_witness`, `ADP019EventPort` | same occurrence id/state digest/commit receipt/actor id/source owner/clock/BP1 causal parents inside the E1 content hash |
| `c9_commit` | C9R `run_candidate_path` with CAN008 `RULE_A` + separate CAN011 `RULE_T`/grant | response receipt hash → grant → sealed full target record → atomic SQLite commit |
| `later_e2` | C9R `read_target_for_later_action` + `admit_performed_action` through `E2OwnerPort` | exact committed record digest, post-commit independent actuator and occurrence |

The three engines are imported, not re-implemented: 30 files, byte-identical to
`b4e07ef51` (BP1 + minimal `lab_sgi1`), `7faaa0722` (BP3 + C8O/OUT9) and `6fa293997`
(C9R repaired candidate + its zero-positive guard). `tools/stage_sources.py` re-reads every
staged file from the origin commit and refuses on any drift.

### 1.2 Exact identities of the recorded evidence run

The evidence root is fixed at `evidence/runtime/positive` (git-ignored) so re-running
`tools/run_courts.py` on this checkout reproduces the same identities. The C8 journal identity
binds its absolute path, so these values are stable **for this checkout path**; a different
path yields a different journal id and therefore a different commit receipt id and downstream
target identity. That is an honest property of the accepted BP3 journal, not hidden
nondeterminism.

| Identity | Value |
|---|---|
| C8 occurrence | `OCC-0001` |
| C8 committed state digest | `058d006c1ce79d2783b02a3bb4e2f92d0672aec9b406b5f3312453f9c5608b4b` |
| C8 commit receipt id | `95ac61ff1bbb8af04278d2e7ce321f56189e1f526f167b079de55c0194306e93` |
| C8 canonical bytes SHA-256 | `3a0d583cd03f004936a94d72961cf8f6715f19a062cab2e1ca66bcc2f709177a` |
| BP1 actor A source hash / snapshot | `bf80ce4a…f82e2` / `6b65980d0fbb2ecc…` |
| BP1 other actor B source hash | `ba1266db1726ce17…` |
| E1 event | `TEST_ONLY_BP2_E1_OCC-0001`, hash `f043e3b3d264e93abb0a7abe…` |
| CAN008 RULE_A content hash | `aa5033ca2b5f6321203652bf32537618fefbde4836ada572404702bef1869574` |
| CAN011 RULE_T content hash | `457894cf45902c8a4db1077bb1d043feef1b9c7bba67ad1e231e19978d1da3cb` |
| RULE_T dependency (C9R contract) | `aa5033ca…` (equals RULE_A hash) |
| Grant hash | `3236a56072294efecd81b781…` |
| Response receipt hash | `757eecb20ad793d556daa08e…` |
| Durable target id | `950a4c7903cbe832c72d234a…` |
| Target record hash | `8d784d48096f4d32d0df3d7c…` |
| Consumed target state hash | `4907a662d2494d9f7949d1f8…` |
| C9 commit receipt / authorization hash | `b4d518ed47d32a01bc1d5915…` / `18c85828af145307f37430f0…` |
| E2 owner receipt hash | `19349fd6fded91f222d50ef5…` |
| E2 actuator / occurrence / times | `TEST_ONLY_ACTUATOR_BP2_INDEPENDENT`, `TEST_ONLY_OCCURRENCE_BP2_E2`, action 217 ≥ commit 202 |

The positive receipt is `evidence/joined_positive_receipt.json`; the compact custody ledger
with eight explicit verified links is `evidence/joined_custody_ledger.json`. BP4's exact
immutable input is `evidence/bp4_downstream_afterstate.json`.

### 1.3 Ten same-assertion source severances, all RED → PASS

The named downstream assertion is
`bp2_joined.producer.joined_consumer_assertion`. It asserts the whole causal identity in one
place: same occurrence id and state digest across commit/OUT9/E1, distinct actor/other source
hashes and performed acts, response offer = the other actor's own act, `RULE_A`→`RULE_T`
dependency preserved in the durable record, later read record = committed record, consumed
state = recomputed state = E2 consumed state, `CREATE` branch, independent E2, and no
native/psychology claim. Every trial below must redden that exact function and return to
passing when the edge is restored.

| # | Edge | Physical cut | RED code | Restore |
|---:|---|---|---|---|
| 1 | `C8_PROOF` | OUT9 called without the BP3 keyed journal verifier | `PROOF_VERIFIER_REQUIRED` | same root |
| 2 | `BP1_ACTOR_OTHER_HISTORY` | actor ingress carries the **other** BP1 actor's sealed snapshot and identity | `ACTOR_ROLE_NOT_FOCAL` | same root |
| 3 | `RULE_A_SOURCE` | no CAN008 `RULE_A` resource supplied to the CAN008 port | `CAN008_RULE_A_UNISSUED` | same root |
| 4 | `RULE_T_GRANT_BINDING` | no CAN011 target grant resource supplied to the CAN011 port | `CAN011_TARGET_GRANT_UNISSUED` | same root |
| 5 | `TARGET_COMMIT_READ_HASH` | the sealed record preimage in the committed `target_state` row is rewritten before the later read | `CONSUMER_READSET_MISMATCH` | same root, exact bytes restored |
| 6 | `PERFORMED_E2` | the later receipt names the focal actor as its own actuator | `E2_ACTUATOR_SELF_BOUND` | same root, lawful receipt re-admitted |
| 7 | `BP1_OTHER_SELF_OFFER` | declared other offer replaced by the focal actor's own performed act | assertion (`non-other offer`) | identical fresh root |
| 8 | `RULE_A_REGISTRY_EMPTY` | empty production response registry | `NO_PROPOSAL` (response `CAN008_RULE_ABSENT_FROM_REGISTRY`) | identical fresh root |
| 9 | `RULE_T_SELF_ISSUED` | target request marked self-issued | `PERMISSION_SELF_ISSUED` (DENY, no target row) | identical fresh root |
| 10 | `E2_ACTION_BEFORE_COMMIT` | later action time precedes the target commit | `RESOURCE_NOT_YET_EFFECTIVE` | identical fresh root |

Trials 1–6 use the same root: the identity is cut, the assertion reddens, the exact state is
restored, and the same instance passes again. Trials 7–10 commit state by construction, so
restoration uses an identical fresh root built from the same staged sources and fixtures
(`restore_basis` is recorded per trial and is not conflated). Receipt:
`evidence/severance_receipt.json` (`all_primary_proved: true`, `all_supplementary_proved: true`).
No cut is an arbitrary mock packet: each is the actual dependency at the actual call site.

### 1.4 Lawful positive, NO_CHANGE and DENY

| Branch | What actually happens | State after |
|---|---|---|
| `CREATE` | two distinct enacted BP1 acts + independent other performed offer + granted material + exact grant | full sealed target row committed, later read and independent E2 admitted |
| `NO_CHANGE` (absent rule) | response `REFUSED` `CAN008_RULE_ABSENT_FROM_REGISTRY`, no proposal | occurrence and response kept, **0 target rows** |
| `NO_CHANGE` (insufficient history) | one declared enacted ref only | 0 target rows, response `INSUFFICIENT_ENACTED_HISTORY` |
| `NO_CHANGE` (denied material) | conditioning access `denied` → `NO_ELIGIBLE_MATERIAL_SOURCE` | 0 target rows |
| `DENY` (self-issued target request) | `PERMISSION_SELF_ISSUED` | occurrence kept, **0 target rows** |

Two genuinely distinct actor/history identities (`TEST_ONLY_BP1_ACTOR_A` repair/5 units and
`TEST_ONLY_BP1_ACTOR_B` finishing/2 units) each run the whole chain and produce different
target ids, record hashes and consumed state hashes; their relation views remain
`UNKNOWN_OR_NONRECIPROCAL` with `NO_PSYCHIC_RELATION_OWNER_GRANT`. Receipt:
`evidence/alternatives_receipt.json`.

### 1.5 Cold process verification

`tools/cold_probe.py build` runs the chain; a separate `python3 tools/cold_probe.py verify`
process re-verifies the source manifest, the BP3 keyed proof and external anchor, the OUT9
readset and canonical bytes, the durable target row digest and sealed preimage, the
`target_journal` row and commit receipt, the `RULE_A`→`RULE_T` dependency in the durable
record, and re-admits the persisted E2 owner receipt. All equalities hold
(`evidence/cold_verification.json`, `status: VERIFIED`).

### 1.6 Native-ready receiving ports with empty production registries

`bp2_joined/ports.py` implements the receiving side for authority this worker may not issue:

| Port | Enforces |
|---|---|
| `ADP010EncounterPort` | only `AVAILABLE` may be declared by a world fixture; `OPPORTUNITY`/`ENCOUNTER` require an external resource and otherwise raise typed `*_UNISSUED` |
| `ADP019EventPort` | binds a proof-verified committed C8 occurrence as a **TEST_ONLY** E1 and records `ADP019_ADMISSION_RECEIPT_ABSENT`; `admit_native` can only echo an owner-supplied receipt |
| `CAN008RulePort` | resource currentness, version, effective time, declared readset, issuer namespace, subject scope and semantics/content-hash equality |
| `CAN011TargetPort` | separate target owner from the response owner, exact `RULE_T` hash, grant binding to actor/rule/response/before-target, revocation, expiry, freshness |
| `E2OwnerPort` | independent actuator and occurrence, post-commit action time, exact consumed state hash, non-self owner |

`Resource.check()` returns typed `UNISSUED / REVOKED / EXPIRED / NOT_YET_EFFECTIVE / STALE /
VERSION_MISMATCH / HASH_MISMATCH / MISSING_READSET / FOREIGN_OWNER / CURRENT`.
`production_registries()` returns the empty C9R production response and target registries and
fails closed if either is non-empty. No rule, grant, encounter, admission or performed action
is minted by these ports.

### 1.7 Security and crash honesty

Closed in the candidate process (tests, not claims): old `Journal.commit` and
`admit_and_queue` refused with `LEGACY_WRITER_ROUTE_CLOSED` and acknowledged bytes preserved;
forged `KeyedCapability` refused; unkeyed receipt forgery refused by the keyed proof;
withheld anchor, tampered watermark MAC refused; byte-valid rollback with an old proof
detected; stale writer version refused; severed expected OUT9 digest refused; key store inside
the journal directory refused; crash after journal rename before the proof sidecar refused
(`PROOF_SIDECAR_MISSING`) and **not acknowledged**; self-actuator and self-occurrence E2
refused; a consistently re-sealed forged durable row still reddens the same assertion.

Typed residuals, not security successes:

1. **D1** — a process that imports `outbox_prototype` without importing the BP3 candidate can
   still call the old writer; raw filesystem writes are not prevented. The bypass is
   *detectable* (`LEGACY_WRITER_BYPASS_DETECTED`), not prevented.
2. **D2** — the TEST_ONLY key file is the whole boundary: an attacker holding it mints a
   valid capability (demonstrated). Anchor log and watermark rolled back together defeat
   detection. No production KMS/HSM.
3. **D3** — no ADP019 admission, no native actor occurrence, no native performed E2.
4. **Crash after rename before proof** — journal bytes are visible and byte-valid to a raw
   OUT9 read but unacknowledged. The joined consumer refuses; reconciliation is a C8 owner
   decision, not invented here.
5. **Durability** — `fsync` + rename is not a power-failure guarantee on exotic filesystems.
6. **Source semantics** — C8 occurrence custody is not actor psychology or developmental
   history.

### 1.8 One finite PS0-D01 scientific decision request

`evidence/scientific_decision_request.json` is
`BP2_PS0_D01_SCIENTIFIC_DECISION_REQUEST@1`, grounded on PS0 commit
`b1f8155338e6fae9fdca0fd11a810199ed12f3ca` document
`05_PRECISE_SCIENTIFIC_DECISION_OWNER_DOCKET.md` (`PS0-D01`), P0
`4073ae2a3363d05e429e3be885486f094414b8ce` and PA0 `3b39c86b…`. It carries: the exact finite
trial; the tested `CREATE` evidence and the tested NO_CHANGE/DENY evidence; the proposed-only
TEST_ONLY `RULE_A`/`RULE_T` semantics with their content hashes and `PROPOSED_ONLY_NOT_ISSUED`
status; the proposed scope (semantic object, state kind, subject scope) with temporal
sufficiency and transfer explicitly **not decided**; nine forbidden shortcuts; the
`ADOPT / REVISE / REJECT / REQUEST_EVIDENCE` options; seven competent owners with their current
unissued state; and the explicit non-claims. It contains no trait, affect, need, practice rate
or developmental coefficient.

### 1.9 Source closure

`vendor/source_manifest.json` lists 30 files with origin commit, origin path, SHA-256, Git blob
SHA-1 and size. `tools/stage_sources.py verify` re-reads each origin object and compares bytes,
and refuses any undeclared `.py` in `vendor/`. Four BP1 hashes reproduce BP1's published
values exactly (`source.py cbecd864…`, `ledger.py e68901da…`, `composer.py 358a3c6e…`,
`c9_bridge.py c954e7d9…`), as does G18 `joint.py 755820d7…` and C9R `identity.py 595b030b…`.

---

## 2. INTERPRETATION AND ALTERNATIVES

**What is now proved at L1.** Three previously separate source-free positives become one
falsifiable causal chain: a committed journal occurrence carries two distinct actor histories
and their performed acts; the accepted OUT9 read returns that same occurrence; C9R binds the
same occurrence id, state digest and commit receipt into the E1 content hash; a separately
owned response rule and target rule produce one durable record whose preimage and response
bindings are revalidated at commit; a later read consumes the exact committed digest; and an
independently performed later action is admitted against that digest after the commit. Cutting
any one source edge reddens the same assertion; restoring it restores the positive.

**Why this is not three adjacent green tests.** The assertion is defined over identities
produced by the whole chain, and every stage re-derives its input from the previous stage's
actual committed output: the C8 occurrence payload is compared byte-for-byte with the BP1
source payload on read, the E1 content hash carries the OUT9 readset, the grant binds the
computed response hash, the target record embeds the response and rule link, and the E2
receipt binds the recomputed record digest. A local success cannot satisfy it.

**C9R target-rule contract observation.** C9R's accepted `TargetRule.rule_content_hash` and
`proposal.source_update_rule_ref` are the **CAN008 response-rule** content hash, so the
target registry lookup is keyed by the response rule. This worker did not alter that contract:
the separate `RULE_T` identity is carried as `rule_t_content_hash` and as the exact `rule_id`
inside the sealed authorization preimage, while the durable record's `creation_rule_ref`
equals the RULE_A hash and the assertion checks `creation_rule_ref == rule_t_dependency_hash`.
If HQ wants the RULE_T's own hash as the durable `creation_rule_ref`, that is a C9R contract
change owned by the C9R/CAN011 owners, not a BP2 edit.

**Why two actors are not aliases.** The two lives have distinct actor ids, source refs/hashes,
roles, seeds, material budgets, G18 histories, ledger event-id sets, performed actions and
after-states. The joined chain is run for both, and their target records and consumed digests
differ. They remain two scripted source-free histories, not two developed humans.

**Why the clock is a fixture.** The C8 envelope's `effective_clock` is an explicit
`BP2_TEST_ONLY_LOGICAL_CLOCK` (the BP1 logical event index), injected through the base class's
own `clock` hook. Without it the wall-clock OS default makes the commit receipt id vary per
run and destroys reproducibility. This is a declared fixture clock; `require_trusted_time`
would still refuse a production trusted-time claim.

**Alternatives considered and rejected.** (a) "Reuse BP1's `run_bp1_c9` directly" — rejected:
it would leave BP3 OUT9 outside the chain and produce another adjacency, not a joined chain.
(b) "Run C9R twice on one store to get a second event" — rejected: C9R correctly refuses a
repeated event time and the journal refuses a duplicate occurrence, so the second-actor
comparison uses a separate root instead of forcing a false double-commit. (c) "Mutate the
outer row body to sever the target hash" — rejected after testing: C9R's preimage check does
not cover the outer `governed_payload`, so the cut is applied to the sealed preimage and a
separate adversarial test covers a consistently re-sealed forgery.

---

## 3. THREE SEPARATE ACCEPTANCE COURTS

**ENGINEERING — `ACCEPT_SCOPED_SOURCEFREE_JOINED_PRODUCER`.**
One whole BP3→BP1→C9R source-free positive actually executes: real keyed append and anchor,
real OUT9 read, exact E1 binding, one durable target, cold reopen equality, an independently
performed later E2, lawful NO_CHANGE and DENY with zero target rows, ten same-assertion
severances with restoration, and typed D1/D2/D3 residuals. 50 tests, 5 JUnit files, 0 RED in
this return's own courts. Scope excludes native cutover, production key custody and native
event/rule/action authority.

**SCIENTIFIC — `ACCEPT_SCOPED_TEST_ONLY_JOINED_MATERIAL_PRACTICE__HOLD_NATIVE_PSYCHOLOGY`.**
At the finite source-free grain, two materially different actor histories plus an independent
other performed offer condition a bounded response and one durable practice-labelled target,
which is later consumed by an independently performed action; absent evidence, denied material
access and self-issued requests produce no target. No psychological trait, need, practice rate,
attachment, trauma, family or developmental law is inferred, and no response text is stored as
durable actor state (the durable payload is C9R's fixed practice label with declared evidence
refs). A role, seed, fixture or repeated test event does not create an acquired human
personality. Native CAN008/CAN011 semantics remain with their owners.

**AUTHORITY — `HOLD`.** ADP007 actor genesis, ADP015 independent other/family, ADP010
opportunity/encounter, ADP019 admission, concrete CAN008 `RULE_A`, separate CAN011 `RULE_T` +
grant, native E2 performer, C8 D1/D2/D3, PSEPF production registry, Pyat N11/N12, C11 weld and
C12 person are **not issued**. No self-adoption; HQ owns intake and any independent review.

---

## 4. HQ ACTION REQUESTED, COMPETENT OWNERS AND EXACT DECISIONS

| HQ action | Competent owner | Exact decision / receipt required | Current state |
|---|---|---|---|
| Intake this joined producer at declared L1 scope | Sorok HQ (scoped method adoption only) | accept/reject engineering and scientific scope; no native grade follows | candidate |
| Decide the first finite material-practice science question | CAN008 R2 concrete `RULE_A` issuer | one exact rule body/version/content hash, subject/readset scope, alternatives, valid-empty condition, effective time, revocation | `CAN008_RULE_ISSUER_UNVERIFIED__UNISSUED` |
| Decide the separate durable target | CAN011 separate target owner | one exact `RULE_T` (kind, semantic object, operation, state kind) plus CREATE/NO_CHANGE/DENY grant with before/write sets, expiry, revocation | `RULE_T_AND_GRANT_UNISSUED` |
| Admit the precipitating occurrence | ADP019 V3 external admission court | exact event id/hash/time + owner receipt | `ADP019_ADMISSION_RECEIPT_ABSENT` |
| Bind the encounter | ADP010 encounter owner | AVAILABLE→OPPORTUNITY→ENCOUNTER for this exact subject | `OPPORTUNITY_AND_ENCOUNTER_UNISSUED` |
| Issue the native actor and independent other | ADP007 / ADP015 owners | native actor genesis and source-qualified other/family relation | `TEST_ONLY_FIXTURE_ACTORS_NOT_NATIVE` |
| Admit one performed later action | native actuator/occurrence owner | performed-action receipt bound to the consumed state hash and post-commit time | `TEST_ONLY_DECLARED_ACTUATOR_NOT_NATIVE` |
| Close C8 D1 / D2 / D3 | C8 writer owner / key-anchor custodian / ADP019 owner | all-writer cutover; production KMS + independent monotonic anchor; native admission | `HOLD` |
| Populate the production registry | PSEPF registry binder | separate accepted authority change | `PRODUCTION_REGISTRY_EMPTY` |
| Ask the user build-or-reuse for each missing issuer | user + competent owner | one plain-English question per exact missing function, answer recorded, no loop or fixture substitution | not asked by this worker |

---

## 5. MATRIX, COMMANDS, ARTIFACTS, ENVIRONMENT

### 5.1 Court matrix (JUnit in `evidence/junit/`)

| Court | Files | Tests | Result |
|---|---:|---:|---|
| joined positive + cold process | `test_joined_positive.xml` | 6 | 6 PASS / 0 RED |
| lawful alternatives and refusals | `test_joined_alternatives.xml` | 13 | 13 PASS / 0 RED |
| ten same-assertion severances | `test_joined_severance.xml` | 9 | 9 PASS / 0 RED |
| security, crash and owner boundaries | `test_joined_security.xml` | 13 | 13 PASS / 0 RED |
| native-ready ports | `test_native_ports.xml` | 9 | 9 PASS / 0 RED |
| **total** | 5 | **50** | **50 PASS / 0 RED** |

### 5.2 Exact commands

```bash
# stage or re-verify the pinned source closure
python3 tools/stage_sources.py verify

# full court + every evidence artifact (JUnit, positive, alternatives, severance, cold)
python3 tools/run_courts.py

# one court directly
PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 python3 -m pytest \
  -c tests/pytest.ini tests/test_joined_positive.py

# cold two-process build/verify
python3 tools/cold_probe.py build  <root> <receipt.json>
python3 tools/cold_probe.py verify <root> <receipt.json>
```

### 5.3 Evidence artifacts

| Artifact | Contents |
|---|---|
| `evidence/joined_positive_receipt.json` | full joined receipt incl. every stage summary and the persisted identity block |
| `evidence/joined_custody_ledger.json` | 14-step event→actor→E1→RULE_A→RULE_T→target→later-read→E2 ledger + 8 verified links |
| `evidence/alternatives_receipt.json` | NO_CHANGE (three causes), DENY, two-actor distinctness |
| `evidence/severance_receipt.json` | 6 primary + 4 supplementary trials with cut descriptions, RED codes and restoration basis |
| `evidence/cold_verification.json` | separate-process proof/anchor/OUT9/SQLite/E2 equality |
| `evidence/scientific_decision_request.json` | one finite PS0-D01 CAN008/CAN011/ADP request |
| `evidence/bp4_downstream_afterstate.json` | exact immutable C9 afterstate and consumer contract for BP4 |
| `evidence/security_receipt.json`, `d1_d2_d3_residuals.json` | closed controls and typed residuals |
| `evidence/not_run_inventory.json`, `native_functional_gap.json`, `authority_hold_register.json` | every missing native function with input→decision→receipt→consumer→effect |
| `evidence/source_actor_performer_gap_table.json` | source / actor / performer / writer / event / rule / person gaps |
| `evidence/source_manifest_summary.json`, `environment_passport.json`, `privacy_and_law.json` | closure, environment and law statement |
| `evidence/court_results.json` | per-court return codes and JUnit paths |

### 5.4 Environment passport (summary)

Python 3.11.3 · pytest 9.1.1 · SQLite stdlib · Git 2.39.1 · macOS x86_64 · stdlib-only
implementation (`hashlib`, `hmac`, `json`, `sqlite3`, `fcntl`, `subprocess`); `cryptography`
absent and not needed. `PYTHONHASHSEED=0`, `PYTHONDONTWRITEBYTECODE=1`, neutral
`tests/pytest.ini`. No paid API call observed; account, quota and spend **UNKNOWN**. Full
passport: `evidence/environment_passport.json`.

---

## 6. LIMITS, NOT_RUN AND REMAINING REDs

1. **Not native.** The actor sources are declared `TEST_ONLY_BP1_*` fixtures; the C8 occurrence
   admission grade is `SOURCEFREE_LEGACY_FIXTURE_NO_OWNER_AUTHORITY`, explicitly not an ADP019
   admission; `RULE_A`, `RULE_T`, the grant, the actuator and the occurrence are TEST_ONLY.
2. **Not a person.** Two distinct scripted histories are not two developed humans; no
   psychology, genealogy, family, biology or developmental law is created.
3. **Upstream suites not re-executed by this worker.** BP1's G13–G18 preservation suites,
   BP3's C8O/OUT12–OUT14 courts and C9R's author suite were **not** rerun here. Their receipts
   remain applicable to the staged bytes because the manifest proves those bytes are
   SHA-256 identical to the origins; independent re-execution is an HQ review action, not a
   claim of this return.
4. **C9R 62/28 author divergence** is not erased. The joined positive path is the one C9RI
   independently adjudicated as surviving; no disputed author positive is promoted.
5. **Journal identity binds its path.** Identities are reproducible on this checkout by
   re-running `tools/run_courts.py`, not portable across different paths.
6. **Crash and durability residuals** in §1.7 remain typed; the C8 owner must reconcile an
   unacknowledged post-rename state.
7. **No C10/C11/C12.** This return stops at the immutable C9 afterstate and the independently
   performed E2; BP4 owns the C10 consumer read, C11 and C12.
8. **Remaining REDs in this return's own courts: none.** Remaining REDs elsewhere are the
   preserved upstream historical REDs (e.g. G17I 56+17, OUT13-outside-OUT14 inherited RED),
   which this worker neither reran nor altered.

---

## 7. PUBLICATION

| Item | Value |
|---|---|
| Branch | `agent/rabochii-sorok-20261020-bp2-joined-event-rule-action-positive-r1` |
| Exact sealed startup | `e699fed59925a3d7b3f02805f85771ae2df32be8` |
| Remote BP2 tip before work | `e699fed59925a3d7b3f02805f85771ae2df32be8` (no prior worker commits) |
| Substantive return commit | `b2734bc21d79619c4718fc8a070a3582ad2de327` |
| Remote verification of that tip | `git ls-remote origin refs/heads/agent/rabochii-sorok-20261020-bp2-joined-event-rule-action-positive-r1` returned `b2734bc21d79619c4718fc8a070a3582ad2de327` |
| Push | ordinary non-force (`e699fed59..b2734bc21`) |
| Docs delta | this file and `PUBLICATION_RECEIPT.json`; the final remote tip after that delta is the exact SHA returned by the final direct `git ls-remote` readback in the worker's final response |
| Publication receipt | `PUBLICATION_RECEIPT.json` |

Only this return subtree is committed. No upstream file, frozen test, native module, Pyat
artifact, PRE-MAIN document, production path or other worker's branch was modified. No
self-adoption, no automatic reviewer, no new worker.
