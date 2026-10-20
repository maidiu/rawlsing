# SOROK BP1 — WHOLE HISTORICAL ACTOR PRODUCTION AND ACTUAL C4→C9 CONSUMED LIFE R1

## 0. Identity, launch truth, custody and scope

| Binding | Value |
|---|---|
| Repository | `maidiu/rawlsing` (PRIVATE) |
| Branch | `agent/rabochii-sorok-20261020-bp1-historical-actor-production-c4-c9-positive-r1` |
| Startup parent (HQ dispatch physical head) | `529232d9867a5bdc0889f43fb5293131ef806055` |
| BP1 commission | `25138c1207d0b86b1d66870a46dd6275d8e3e065` |
| HQ four-return disposition | `4e1a209ef5c55d3a70ab8772b95e688e121e82aa` |
| G18 source | `61713eafe0e7a5386a8f0aed4836b15f3d921ed5` |
| C9R source | `6fa2939972ce5a2c0cc4f2b033946b276f1c2934` |
| C9RI independent return used | `5753d9b4f8fad9f2175b1e285733f95bb8387888` |
| P0 / PS0 / PA0 | `4073ae2a3363d05e429e3be885486f094414b8ce` / `b1f8155338e6fae9fdca0fd11a810199ed12f3ca` / `3b39c86b376efff8c11833b8451c1791adddb9bc` |
| Model / harness | user-selected **DeepSeek V4.1-Flash, reasoning MAX**, one accountable local DSH editor; no model/harness switch, no sub-agent, no paid API call observed |
| Write scope | only `WORKER_RETURNS/SOROK-20261020-BP1-HISTORICAL-ACTOR-PRODUCTION-R1/**` |
| Frozen-test edits | **none** |
| G18 / C9R / C9RI edits | **none**; exact vendored copies only |
| Native authority | **NOT_GRANTED** |

**Launch truth.** At BP1 fetch there was no local or remote
`agent/rabochii-sorok-20261020-bp1-historical-actor-production-c4-c9-positive-r1`
ref. HQ disposition `4e1a209ef` explicitly records both BP1 and BP3 as
*commissions published but worker branches unsealed* because branch creation was
blocked by tool safety. I did **not** fabricate a sealed startup or claim a
pre-existing seal. The direct user launch is the launch authority; I created the
named branch from the physical HQ dispatch head `529232d98`, which contains the
BP1 commission, the four-return disposition and the C9RI acceptance. This return
is bound to that dispatch head.

**C9RI snapshot.** The launch text said C9RI was still ongoing with no remote
return. By the time of BP1 fetch, the remote C9RI reviewer branch had returned at
`5753d9b4f` (independent court 17/17, 28-row compatibility ledger, eight
severance witnesses), and HQ `529232d98` accepted the sourcefree independent
positive and 28 regression classification. I did not touch the C9RI branch or
its tests; I used its pinned C9R source and verdict as the lawful terminal
handoff. If HQ intended BP1 to proceed before that return, this is the exact
snapshot difference and should be reconciled by HQ, not hidden.

---

## 1. FINDINGS

### 1.1 A real sourcefree historical actor/other producer now executes

The new package `candidate/bp1/` is callable, importable and tested:

| Module | Actual function |
|---|---|
| `bp1/source.py` | explicit `TEST_ONLY_BP1_*` fixture actor sources; role, seed, birth clock, budgets, event permissions, known unknowns; `SOURCEFREE_FIXTURE_ACTOR_NOT_NATIVE`, `native_grant=NOT_GRANTED`; no psychology/future fields |
| `bp1/ledger.py` | per-actor append-only event ledger; own-state conservation; other-action record without own-state change; durable sealed snapshots; cold replay; future-child refusal |
| `bp1/composer.py` | two independent G18 histories, one shared objective fact, two genuinely performed G18 actions, relation views `UNKNOWN_OR_NONRECIPROCAL`, lawful `NO_CHANGE`/`DENY` |
| `bp1/c9_bridge.py` | historical actor snapshot → C9R `ingress_actor` → E1 → conditioning/material eligibility → TEST_ONLY RULE_A → TEST_ONLY RULE_T/target → committed SQLite target → cold later read → independently performed TEST_ONLY E2 |

The historical actor base is the exact G18 source-issued material/performed
action receipt path. The BP1 ledger records the G18 action receipt and the exact
material receipt, and re-verifies both on cold replay. The BP1 actor source is a
**declared fixture source**, not a new native or shadow native issuer.

### 1.2 Two distinct actor-owned lives, not two variants of one seed

`build_two_actor_life()` produces:

| | `TEST_ONLY_BP1_ACTOR_A` | `TEST_ONLY_BP1_ACTOR_B` |
|---|---|---|
| role | repair | finishing |
| seed | `BP1_SEED_A_REPAIR` | `BP1_SEED_B_FINISH` |
| source / history | distinct source ref/hash and G18 history | distinct source ref/hash and G18 history |
| material budget | 5 units | 2 units |
| cash after own history + joint action | **55** | **54** |
| completed units after | **4** | **3** |
| material remaining | **2** | **0** |
| free hours | **12** | **13** |
| performed joint action | +1 completed unit, +2 cash, −1 hour | +1 completed unit, +2 cash, −1 hour |
| state hash | `b5fa11db…` | `effc83bf…` |

Shared objective facts are identical in both ledgers: same
`objective_event_id`, same objective hash, same G18 material event/receipt, same
joint witness; the participant actions and own after-states are distinct. The
actor IDs, event-id sets, source hashes and G18 history hashes are disjoint.
This is a genuine two-ledger material difference, not two copies of one adult
with a budget swap. It remains **sourcefree finite variation**, not two
independently developed human lives.

The ledgers record:

`PRIOR_HISTORY → SHARED_OBJECTIVE → PERFORMED_ACTION → OTHER_ACTION → RELATION_VIEW`

The shared objective event changes neither actor's state. Each actor's own
performed action changes only its own state. The other actor's independently
performed action is recorded as `OTHER_ACTION` with `effect_on_own_state=NONE`.
The relation view is honest `UNKNOWN_OR_NONRECIPROCAL` with
`NO_PSYCHIC_RELATION_OWNER_GRANT`; no psychology is inferred from the joint act.

### 1.3 Lawful alternatives are real

| Branch | Result |
|---|---|
| `NO_CHANGE` | actor A with own material exhausted before the task: `OWN_MATERIAL_EXHAUSTED`, state byte-equal before/after, `NO_CHANGE` event, no performed action |
| `DENY` | actor A source without `PERFORMED_ACTION` permission: `ACTOR_PERMISSION_DENIED`, state byte-equal before/after, `DENY` event, no performed action |
| future firewall | nested `metadata.future_child_personality` and serialized JSON future-child values are found recursively and refused with `FUTURE_CHILD_INFORMATION_LEAK` |
| forged actor source | rehashed source ref moved to `NATIVE_ADMIN_ACTOR` refused `ACTOR_SOURCE_REF_NOT_TEST_ONLY_BP1` |
| forged material | G18 payment 100000 refused `MATERIAL_SOURCE_NOT_AUTHENTICATED` |
| forged action after-state | cash +100000 action refused `PERFORMED_ACTION_NOT_AUTHENTICATED` |

### 1.4 Real C4→C9 consumed positive at TEST_ONLY

The exact vendored C9R `run_candidate_path` is executed with a BP1 historical
actor snapshot:

* actor ingress `ADMITTED` at `TEST_ONLY_SOURCEFREE_TECHNICAL`, native source
  unresolved by design;
* event witness `ADMITTED`;
* conditioning read-only bound; material eligibility `OK`;
* TEST_ONLY `RULE_A` lookup/response `OK`;
* separate TEST_ONLY `RULE_T` target evaluation `OK`, branch `CREATE`;
* atomic commit `COMMITTED` (target `08a8d89a…`);
* later committed-state read held for a performed E2 owner;
* independently performed E2 with independent `TEST_ONLY_ACTUATOR_B` and
  `TEST_ONLY_OCCURRENCE_E2` **ADMITTED**, consuming exact state hash
  `68050846…`.

A two-process cold replay rebuilt the same two actor lives, reopened the SQLite
store, read the exact committed record, reproduced the consumed state hash and
readmitted E2. Receipt: `evidence/c9_positive.json`, `evidence/cold_replay.json`.

The C9R author suite's 28 historical divergences are **not promoted**. The C9RI
independent court adjudicated all 28 (13 historical false positives, 14
scientific adapter incompatibilities, 1 previously unissued native authority,
**0 lost lawful positives**) and HQ accepted the sourcefree independent
positive. The BP1 C9 positive uses the exact C9R code and the C9RI lawful
handoff, not a fake proxy.

### 1.5 G18 preservation is exact

The vendored G18 source at `61713eafe…` is byte-identical. Against it:

| Court | Result |
|---|---:|
| G13 historical 181 | **108 PASS / 73 RED** |
| G14 on G13 67 | **67 PASS / 0 RED** |
| G15 prospective 75 | **75 PASS / 0 RED** |
| G16I independent 24 | **21 PASS / 3 RED strict** (22/2 baseline; 2 typed M2/MP HOLDs + 1 documented legacy schedule supersession) |
| G17 material 13 | **13 PASS / 0 RED** |
| G18 authenticated 20 | **20 PASS / 0 RED** |
| G17I independent 14 | **14 PASS / 0 RED** (11/3 baseline; 3 bypasses closed) |

The 73 RED IDs are exactly the preserved G17I set: **56 compatibility + 17
original**, exact set equality. The G18 three bypass fixes and the 21/3 strict
legacy-schedule supersession are preserved; BP1 did not return to the old
untrusted schedule.

### 1.6 M2/MP remain exact typed HOLDs

No fake mother, father, child or second parent is created:

* **M2:** 23-event archive SHA-256
  `9e0efc335e2bfc1e1d9f9bc25604af6d04578e7b6acddb31e439b6ff117a3ab7`; the
  frozen G16I continuation test remains RED under G18 strict (owner identity /
  missing current `WORLD_MATERIAL` root). HOLD, not fabrication.
* **MP:** `F_EXISTING` / `REL_ADMITTED_F_EXISTING`; no source-qualified
  second-parent history; frozen G16I reuse test remains RED; no duplicate
  actor/event, no invented father. HOLD.

Exact receipts: `evidence/m2_mp_holds.json`.

---

## 2. INTERPRETATION AND ALTERNATIVES

**What now exists.** A sourcefree historical actor/other composer that actually
creates two durable actor-owned ledgers from distinct G18 histories, records two
genuinely performed actions over one shared objective fact, conserves each
actor's own state, keeps the other's action from mutating that state, preserves
honest unknown relation views, and feeds the exact C9R sourcefree consumer to a
committed later-E2 positive. The important causal difference is in the
**performed history and material budget**, not in a narrator label or a class
prior.

**What this does not prove.** It is not a native ADP007 actor, not a real parent
or family, not a biology or psychological law, not a universal “two acts means
learned practice” rule, and not a human life. The BP1 source is a declared
TEST_ONLY fixture; the C9 rule/target are TEST_ONLY; the E2 actuator/occurrence
are TEST_ONLY. The native CAN008/CAN011/ADP007/ADP019/ADP010/C8/Pyat/C11/C12
decisions remain HOLD. The two actors are scripted sourcefree histories, not
independently developed persons.

**Why the two lives are stronger than G18's 2-vs-5 material variants.** G18 had
one scripted adult with two budgets; BP1 has distinct actor IDs, source refs,
roles, seeds, material histories, event-id sets, cash/completed/material/free-hour
states and two distinct performed actions. It is still a finite sourcefree
construction, but it is not the same adult with a budget swap.

**Why the C9 positive is not a fake proxy.** The exact C9R sourcefree code is
vendored and executed: actor ingress, event witness, conditioning/material
eligibility, response rule, target rule, atomic SQLite commit, later read, and
E2 admission. The BP1 bridge supplies the historical actor source and the
shared-objective event; it does not bypass the C9R gates. A source-edge mutation
of the actor snapshot or a fixed-default consumed state fails the same named
positive assertion; the six BP1 proof claims demonstrate the exact source edges.

**Alternatives preserved.** Insufficient own material → `NO_CHANGE`; absent
permission → `DENY`; future-child payload → typed refusal; forged actor/material/
action → refusal; no native claim → TEST_ONLY grade. No effect is not reported as
a positive.

**U2/ADP010 boundary.** The recovered U2 subject identity was **not** used as
an actor. ADP010 OEE / ADP007 / ADP019 native carriers were not invoked as
positive native authorities because their installed registries/grants are
absent. The BP1 actor source is a declared TEST_ONLY fixture; native actor
genesis remains the ADP007 owner HOLD. This avoids turning a nonactor subject or
a fixture hash into a self-issued actor.

**M2/MP.** The exact archive currentness did not yield a new source-qualified
owner mapping in the accepted inspected material. The honest disposition remains
the two typed HOLDs. No fabricated mother/father/child.

---

## 3. THREE COURT VERDICTS

**ENGINEERING — `ACCEPT_SCOPED_SOURCEFREE_HISTORICAL_ACTOR_PRODUCER`.** The
producer is executable and importable; two actor-owned lives have distinct
performed histories and states; per-actor ledgers replay; `NO_CHANGE`/`DENY`/
future firewall and forged-source refusals are real; the exact C9R consumer
commits and a cold later E2 is admitted; six same-edge source faults are
PASS→RED→PASS; G18 181/67/75/24/13/20/14 preservation is exact. Scope excludes
native actor/person/rule/C8/Pyat/C11/C12 authority and production.

**SCIENTIFIC — `ACCEPT_SCOPED_TEST_ONLY_TWO_ACTOR_MATERIAL_HISTORY /
GENERAL_HOLD`.** At the finite sourcefree grain, distinct performed histories and
material opportunities produce distinct own after-states while shared objective
facts remain identical; `NO_CHANGE`, `DENY`, unknown relation and future firewall
are preserved. No native psychogenesis, personality law, calibrated rate,
genealogy, biology or independently developed human life is claimed. The first
scientific decision request is prepared as a finite `ADOPT/REVISE/REJECT/
REQUEST_EVIDENCE` dossier, not an invented rule.

**AUTHORITY — `HOLD`.** No native ADP007 actor, ADP015 parent/other, ADP019
occurrence, CAN008 concrete `RULE_A`, CAN011 `RULE_T`/grant, ADP010 encounter,
C8 D1/D2/D3, native E2, Pyat N11/N12, C11 weld, C12 person or production
authority is issued or implied. The BP1 fixture source is
`SOURCEFREE_FIXTURE_ACTOR_NOT_NATIVE`; the C9R rule/target/E2 are TEST_ONLY.
No producer self-signature, fixture hash or model permission becomes native.

---

## 4. HQ ACTION REQUESTED AND ACCOUNTABLE OWNER

| HQ ACTION | ACCOUNTABLE OWNER | EXACT DECISION / RECEIPT REQUIRED |
|---|---|---|
| Intake BP1 and decide scoped adoption of the sourcefree historical actor producer | Sorok HQ (scoped method adoption only) | Accept/reject the engineering/scientific scope; no native grade follows; no new automatic reviewer queue |
| Decide the first finite material-practice science question | CAN008 R2 concrete `RULE_A` issuer + CAN011 separate target owner | `ADOPT / REVISE / REJECT / REQUEST_EVIDENCE` for one scoped practice predicate and target grant, with exact rule id/version/hash/scope/effective/revocation |
| Issue native actor genesis | ADP007/V3 actor developmental causality owner | ADP007 activation/source/genealogy receipt; no fixture actor substitution |
| Issue independent other/parent/family | ADP015 rule owner + source-qualified parent/other owners | Source-bound independent history/relation; M2/MP only if exact source/permission, otherwise typed HOLD |
| Issue actual E1 occurrence | ADP019 owner + C8 D3 | ADP019 occurrence receipt + C8 committed event; no co-presence-only inference |
| Issue trusted writer/anchor | C8 D1 writer owner / D2 external credential-anchor custodian | Exclusive-writer and keyed monotonic anchor receipt |
| Issue native E2 performed action | ADP019/E2 performer owner | Independent actuator/occurrence receipt bound to committed state hash |
| Issue C11 weld / C12 person | Pyat/C11 authority + native person-generation authority | Separate C11 grant and C12 continuity admission; not attempted |
| Ask user build-or-reuse for each missing issuer | User + competent owner | One plain-English question per exact missing function; record answer; do not loop or substitute a fixture |

**C9RI:** its separate branch/tests were not touched; its independent verdict is
used as the lawful C9R handoff. **G18:** not restarted, edited or self-adopted;
only the exact pinned source/tests are vendored for preservation.

---

## 5. MATRIX, ARTIFACTS AND RECEIPTS

### 5.1 Full court matrix

| Court | Result | Evidence |
|---|---:|---|
| BP1 actor production author court | **15 PASS / 0 RED** | `evidence/junit/bp1_15.xml` |
| C9R direct consumer (vendored exact) | **10 PASS / 0 RED** | `evidence/junit/c9r_10.xml` |
| G13 historical 181 | **108 PASS / 73 RED**; 56+17 exact | `evidence/g18_regression/g13_181_*.xml` |
| G14 67 | 67 PASS / 0 RED | `evidence/g18_regression/g13_181_g14_science.xml` |
| G15 75 | 75 PASS / 0 RED | `evidence/g18_regression/g15_75.xml` |
| G16I 24 baseline | 22 PASS / 2 RED (M2/MP) | `evidence/g18_regression/g16i_24_baseline.xml` |
| G16I 24 strict | **21 PASS / 3 RED** (2 HOLD + 1 legacy supersession) | `evidence/g18_regression/g16i_24_strict.xml` |
| G17 13 | 13 PASS / 0 RED | `evidence/g18_regression/g17_13.xml` |
| G18 20 | 20 PASS / 0 RED | `evidence/g18_regression/g18_20.xml` |
| G17I 14 baseline | 11 PASS / 3 RED | `evidence/g18_regression/g17i_14_baseline.xml` |
| G17I 14 repaired | **14 PASS / 0 RED** | `evidence/g18_regression/g17i_14.xml` |
| BP1 source-fault witnesses | **6/6 PASS → named assertion RED → restored** | `evidence/proof_witness_bp1.json` |
| Cold C4→C9 positive | committed target + cold record equal + E2 ADMITTED | `evidence/c9_positive.json`, `evidence/cold_replay.json` |

### 5.2 BP1 source-fault claims

| Claim | Positive node | Fault | Result |
|---|---|---|---|
| `BP1_ACTOR_SOURCE_EDGE` | forged actor source refused | source-ref TEST_ONLY gate disabled | PASS → RED → restored |
| `BP1_PERFORMED_ACTION_EDGE` | forged action after-state refused | performed-action receipt gate disabled | PASS → RED → restored |
| `BP1_MATERIAL_SOURCE_EDGE` | forged 100000 G18 material refused | material receipt gate disabled | PASS → RED → restored |
| `BP1_FUTURE_CHILD_EDGE` | nested/serialized future payload refused | recursive finder returns empty | PASS → RED → restored |
| `BP1_C9_ACTOR_SOURCE_EDGE` | forged/rehashed actor snapshot refused | snapshot verification disabled | PASS → RED → restored |
| `BP1_C9_CONSUMED_STATE_EDGE` | exact committed state consumed by E2 | fixed default state hash | PASS → RED → restored |

### 5.3 Exact source/import identities

Full manifest: `evidence/source_manifest.json` — **446 files**, tree hash
`e2f3ebac9fde19d4cc3dc17e69e506913e789ba22c393867278da9c8584d4238`.

| Source | SHA-256 | Git blob SHA-1 |
|---|---|---|
| `candidate/bp1/source.py` | `cbecd8647c64dbb92626d97a234dc245355de9f6935e55bcd64e485493a26372` | `b5cb9265c80d725d6bac61805fcb1a437ce9512d` |
| `candidate/bp1/ledger.py` | `e68901da703462c8bd5b180722f0a763fe30c8e1c5abb733d878aba89f507b39` | `499b884097cf978492bff54d7d7462ca1faf434c` |
| `candidate/bp1/composer.py` | `358a3c6e2f187e21618ed56af17025e80d5153d29af003dcd9e8df9393b63c88` | `a04ea4970e218a8be94bd53df00b4690eae3f307` |
| `candidate/bp1/c9_bridge.py` | `c954e7d9ac97796dd1a44be9bd1bc6eba5181e35fbb17e4085b22c93efe18a5f` | `3112125ccb25474ff827a648970fac700fcedac5` |
| `tests/test_bp1_actor_production.py` | `2e35fef86fbd4130bead502ff9d24609036b8445ee5578188dadceb03679a6ce` | `d54a010fa0c54d062ed1e4858b411eb928c439e1` |
| vendored G18 `lab_sgi1/joint.py` | `755820d7d703cd459aec8271a784c39a69e9374aae501da1cd9f37bbccc21ee9` | `325c4eb738cd61b1803ddc8f7cb8ce97c41ba17f` |
| vendored C9R `candidate/identity.py` | `595b030b6e34f0a4bfcb2032a48d098803e0a9246344f572feb416d77214fb06` | `ac87f640b58c00e2a2cfa178f4ac0eaf40d3fc5a` |

The G18 `joint.py` hash and C9R `identity.py` blob match their origin
custody/PA0 references; the vendored trees are byte-identical, not re-authored.

### 5.4 Commands, environment and cold replay

```bash
python3 -B tools/run_bp1_courts.py
python3 -B tools/proof_integrity_gate_r1.py witness \
  tests/test_bp1_actor_production.py.proof.json --root <repo>
python3 -B tools/bp1_cold_probe.py build  runtime/cold/bp1.sqlite runtime/cold/receipt.json
python3 -B tools/bp1_cold_probe.py verify runtime/cold/bp1.sqlite runtime/cold/receipt.json
```

Environment: Python 3.11.3, pytest 9.1.1, Git 2.39.1, local shared-store
worktree; no paid API call; cash/quota **UNKNOWN**. Passport:
`evidence/environment_passport.json`, `evidence/environment_passport_delta.json`.

### 5.5 Scientific decision dossier

`evidence/scientific_decision_request.json` is a finite
`ADOPT / REVISE / REJECT / REQUEST_EVIDENCE` request, not an invented rule. It
names the exact inputs (two TEST_ONLY actor sources, one shared objective, two
performed G18 actions, material receipt, actor/history refs), the alternatives
(CREATE / NO_CHANGE / DENY), the proposed-only TEST_ONLY rules, the forbidden
shortcuts (trait/affect coefficients, P psychology without P source, future
child, narrator-as-action, fixture registry as native grant), and the exact
competent owner decisions. It preserves the PS0 S01–S10 separation.

### 5.6 Non-run / native gap / privacy

`evidence/not_run_inventory.json` and `evidence/native_functional_gap.json` name
every missing native function with
**input → authenticating decision → receipt → consumer → scientific effect** and
the competent owner. `evidence/authority_hold_register.json` records the holds.
`evidence/source_privacy_and_law.json` records: no original respondent data, no
original35, no Pyat native world, no production, no C9R/G18/C9RI edits; actor
identifiers are explicit TEST_ONLY fixtures and not real persons; no privacy or
native law claim.

---

## 6. LIMITS AND DISCLOSURE

1. **The actor source is TEST_ONLY.** `SOURCEFREE_FIXTURE_ACTOR_NOT_NATIVE`,
   `native_grant=NOT_GRANTED`. It is not ADP007, not U2 identity used as an
   actor, not a real person.
2. **The C9 rule/target/E2 are TEST_ONLY.** `RULE_A`, `RULE_T`, target grant,
   actuator and occurrence are declared test evidence; no native CAN008/CAN011,
   ADP019 or E2 authority follows.
3. **The C9R 28 historical divergences are not erased.** They are used only
   through the C9RI 28-row adjudication (0 lost lawful positives) and the exact
   C9R sourcefree consumer. The C9R author 90-suite 62/28 remains historical
   evidence, not a promoted positive.
4. **G16I 21/3 strict.** Two typed M2/MP HOLDs and one documented legacy
   caller-mutated schedule supersession remain. The source-issued variable
   schedule is the lawful replacement; do not revert to the old untrusted
   schedule.
5. **Two actor lives are sourcefree finite histories.** They have distinct
   sources, roles, material budgets, event ids, histories and performed actions,
   but they are still scripted by the fixture composer, not independently
   developed human beings.
6. **No native authority.** None of the native owners in §4 has issued a rule,
   actor, occurrence, target or person grant. This return is an implementation
   candidate for HQ intake, not self-adoption.

---

## 7. PUBLICATION

| Item | Value |
|---|---|
| Branch | `agent/rabochii-sorok-20261020-bp1-historical-actor-production-c4-c9-positive-r1` |
| Startup parent | `529232d9867a5bdc0889f43fb5293131ef806055` |
| Substantive return commit | `3e95acd5dc523507f654368520e37c884b998ce0` |
| Evidence/verification commit | `d8588d3aeb061d2b0e63ebc6c1bd4177a65fd275` |
| Remote verification of that tip | `git ls-remote origin refs/heads/agent/rabochii-sorok-20261020-bp1-historical-actor-production-c4-c9-positive-r1` returned `d8588d3aeb061d2b0e63ebc6c1bd4177a65fd275` (ordinary non-force push; parent `529232d9867a5bdc0889f43fb5293131ef806055`) |
| Final pushed tip at verification | `d8588d3aeb061d2b0e63ebc6c1bd4177a65fd275` |
| Publication receipt | `PUBLICATION_RECEIPT.json` |

Only this branch is committed and pushed (ordinary non-force push). No
self-adoption; Sorok HQ owns the post-return review decision. C9RI remains the
independent reviewer of its own sourcefree 28-row verdict; G18 remains frozen.

This publication record is the docs delta committed after the verified evidence
tip; the branch tip after that delta is the exact SHA returned by the final
direct `git ls-remote` readback in the worker's final response.
