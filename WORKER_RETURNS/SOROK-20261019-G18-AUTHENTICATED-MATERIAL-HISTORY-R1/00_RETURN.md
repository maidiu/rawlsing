# SOROK G18 — AUTHENTICATED MATERIAL HISTORY AND WHOLE C4→C9 REPAIR R1

## 0. Identity, custody and scope

| Binding | Value |
|---|---|
| Repository | `maidiu/rawlsing` (PRIVATE) |
| Branch | `agent/rabochii-sorok-20261019-g18-authenticated-material-history-whole-c4-c9-repair-r1` |
| Sealed startup | `19503a3ea09bdf840a5ce98a9697650c387787fa` |
| G17 author return (baseline) | `90d0eb7925de54635559a879ee76fc1b97b9ff61` |
| G17I independent RED | `156b84cc8481b65c4196b42574010eb7920d6f44` |
| C9R receiving candidate | `6fa2939972ce5a2c0cc4f2b033946b276f1c2934` |
| G16I independent review | `683aa56828cda76ea70792a2c8b39cf78624e8dc` |
| G15 parent | `fbc84ba4b5ec8befcf7954357a2ba1c576f5d7a5` |
| G13 repair | `47bca2a56d34ed37186a436e7490cbaa417bfe5c` |
| G14 independent review | `d174ec79f561660a02a254cf9b7582595b43e215` |
| Model / harness | user-selected **DeepSeek V4.1-Flash, reasoning MAX**, single accountable local DSH editor; no model or harness switch |
| Write scope | only `WORKER_RETURNS/SOROK-20261019-G18-AUTHENTICATED-MATERIAL-HISTORY-R1/**` |
| Frozen-test edits | **none** |
| G17/G17I/C9R edits | **none** |

No native CAN/ADP/Pyat/person/biology/psychology authority is claimed or issued.
G17I remains the frozen independent negative oracle; this return is one candidate
return for Sorok HQ intake, not a self-adoption and not an automatic second
review queue.

---

## 1. FINDINGS

### 1.1 The three G17I bypasses are real and reproduce exactly on the G17 tip

Using the byte-exact G17 author candidate `90d0eb79…` staged under
`stage/g17_baseline_candidate/` and the unmodified G17I oracle
`tests/reviewer_oracle/test_g17i_independent.py`
(SHA-256 `0e4535a7…`, origin blob `83f17006…`):

| Bypass | G17 baseline | G18 repaired |
|---|---|---|
| Forged material `owner=FAKE`, `permission=FAKE`, `payment=100000` through `continue_person` | **ACCEPTED, continuation cash 100058** | **REFUSED**, no continuation; material receipt rejected |
| Future-child nested in `joint_material_opportunity.metadata` | **COMMITTED** | `FUTURE_CHILD_INFORMATION_LEAK` before any proposal/selection/construction |
| Same forged material through `c9_handoff_consumer` | **ACCEPTED, cash 100055** | `C9Refusal: MATERIAL_SOURCE_NOT_AUTHENTICATED:MATERIAL_BODY_HASH_MISMATCH` |

Exact before/after probe receipt: `evidence/g17i_bypass_before_after.json`.
G17I oracle result: **11 PASS / 3 RED baseline → 14 PASS / 0 RED repaired,
test file unmodified**.

### 1.2 Root cause was a producer-boundary defect, not three isolated validators

The G17 material witness was a caller-shaped dictionary. `owner_id`,
`permission`, `payment_per_actor`, `event_id` and the after-state could all be
supplied or recomputed by the caller; `continue_person` and the C9 consumer
recomputed a *self-consistent* after-state from that same untrusted packet. The
future-child guard inspected only top-level keys. A single forged source could
therefore feed a causally consistent but non-authentic life.

G18 repairs the producer-owned source/permission/actual-action boundary once,
then carries it through continuation and the named C9 consumer:

1. **Source-issued material receipt** (`lab_sgi1.joint.material_joint_opportunity`).
   The fixture origin issues an HMAC-bound receipt over the exact canonical
   payload (owner, scope, permission, effective clock, place, units, bounded
   payment/task schedule, permit). Verification checks the receipt shape, owner,
   fixture scope, source grade, `native_grant=NOT_GRANTED`, body hash, MAC, event
   id and all schedule bounds. A rehashed/copied wrapper with an extra nested
   key is rejected by a strict allowlist even if its public hashes are rewritten.
2. **Source-issued performed-action receipt** (`perform_participation`). The
   action that actually consumed the material is bound to its actor, history
   hash, material receipt, material event, before/after state and receipt MAC.
   `continue_person` verifies both receipts and recomputes the after-state from
   the verified schedule before reading any cash/time/unit value.
3. **Recursive future-child partition scan** (`proposal.find_future_child_material`).
   Every nested dict/list key, alias matched by the declared marker grammar,
   string value and opaque serialized-JSON string is scanned. Material packets
   are then required to be exact source-issued packets. Any leak is typed denied
   before proposal, selection, construction or `COMMITTED`.
4. **C9 authenticated source consumer** (`c9_handoff_consumer`). The handoff
   builder verifies material and performed action; the receiver re-verifies both
   receipts, the exact consumed material receipt/action, severance from causal
   parents, actor/before/after identity and material conservation. Fake cash
   100055 is refused, not merely recomputed.
5. **Genuine lawful paths preserved.** Default 5-unit material still performs
   the lawful 3-unit project and a 2-unit continuation (completed 5, material 0);
   exhausted material produces lawful `NO_CHANGE`; the exact valid material
   handoff remains `ACCEPTED` with `e2_later_authority=HOLD_UNISSUED`; stock,
   free-hours and tool ledgers remain conserved.

### 1.3 One documented compatibility supersession in the G16I 24 court

Strict G18 is **21 PASS / 3 RED** on the frozen G16I 24 court, not 22/2. The two
historical typed coverage HOLDs remain exactly: M2 archive continuation and MP
`F_EXISTING` reuse. The third RED is
`test_variable_task_cost_reaches_continued_context`, a pre-G18 test that mutates
`payment_per_actor=7` and `task_hours=2` **after source issuance** and recomputes
only the public `event_id`. That is precisely the unauthenticated caller-schedule
class G18 denies; the strict candidate refuses it with
`MATERIAL_BODY_HASH_MISMATCH` (`evidence/legacy_schedule_supersession.json`).
The identical scientific effect (cash +7, free-hours −2, continued-context
cash-after +11) is proved through the source-issued
`material_joint_opportunity(payment_per_actor=7, task_hours=2)` path in
`test_source_issued_variable_schedule_reaches_continued_context`.

This is a documented necessary interface supersession, not a material
regression. The frozen test file was not edited; its exact ID is preserved and
classified. HQ may accept the strict 21/3 or direct a legacy adapter; this worker
does not manufacture 22/2 by weakening source authentication.

### 1.4 Frozen baseline and repaired matrix

| Court | Frozen baseline | G18 strict | Preservation |
|---|---:|---:|---|
| G13 historical 181 | **108 PASS / 73 RED** | **108 PASS / 73 RED** | 73 exact IDs; 56 compatibility + 17 original; exact set equality |
| G14 on G13 67 | 67 PASS / 0 RED | **67 PASS / 0 RED** | exact suite |
| G15 prospective 75 | 75 PASS / 0 RED | **75 PASS / 0 RED** | exact suite |
| G16I independent 24 | 22 PASS / 2 RED | **21 PASS / 3 RED** | 2 typed coverage HOLD + 1 documented legacy-interface supersession |
| G17 material consumer 13 | 13 PASS / 0 RED | **13 PASS / 0 RED** | exact suite |
| G17I independent 14 | 11 PASS / 3 RED | **14 PASS / 0 RED** | oracle unmodified; 3 bypasses closed |
| G18 authenticated court 20 | — | **20 PASS / 0 RED** | new author court |
| Proof witnesses 14 | — | **14/14 baseline PASS → same-node assertion RED → restored** | 7 G17 + 7 G18 |

Post-gate cold reruns: G17I 14/14, G18 20/20, G17 13/13. Cold replay: positive
`COMMITTED`, replay record equal; tampered material
`UNAUTHENTICATED_MATERIAL_SOURCE`, replay unequal. Full matrix:
`evidence/court_matrix.json`; exact 73-ID comparison:
`evidence/red_identity_comparison.json`.

---

## 2. INTERPRETATION AND CAUSAL ALTERNATIVES

**What the model now demonstrates at the tested sourcefree grain.** A material
opportunity has a source owner, scope, permission, bounded schedule and exact
after-state that are checkable independently of the caller. A performed adult
action consumes that source and is itself receipt-bound. Current stock, time,
tools and owner action are conserved. A forged 100000 source cannot produce
100058 or 100055, a rehashed wrapper cannot smuggle an unknown nested field, and
a nested future-child partition cannot reach `COMMITTED`. The C9 material
consumer reads only the authenticated causal event and performed action; its
later E2 admission remains `HOLD_UNISSUED`.

**What it does not demonstrate.** This is not a native actor, parent, biology,
psychology, calibrated rate or development law. It is not proof of two
independently developed human lives, and it is not a completed C10/C11/C12
chain.

**Bounded two-actor contrast (not two human lives).** Two finite sourcefree
histories are separately sourced and replayed:

| | `G18_REPAIR` | `G18_FINISH` |
|---|---|---|
| role | repair | finishing |
| material budget | 5 units | 4 units |
| completed-units before joint task | 3 | 3 |
| material remaining | 2 | 1 |
| cash before | 53 | 55 |
| joint performed action | +1 completed unit | +1 completed unit |
| continuation units | 2 | 1 |
| completed units after | 6 | 5 |

The joint witness is `WITNESSED`; both action receipts verify; the continuation
admits both actors with different performed units and after-states. A third
exhausted finishing history (3 units) produces lawful `NO_CHANGE` for that actor
while the repair actor continues. The relation's perceived states remain
`UNKNOWN_OR_NONRECIPROCAL` with `NO_PSYCHIC_RELATION_OWNER_GRANT`; parental and
household admission are `NOT_GRANTED`. Receipt:
`evidence/two_actor_contrast.json`. This earns **bounded finite material
variation**, not a human-life or genealogy claim.

**Causal alternatives preserved.** Out-of-schedule payment/task cost is refused;
permit-false and late-clock participation produce `REFUSED` witnesses; exhausted
material produces `NO_CHANGE`; severing the material parent produces
`SEVERED_MATERIAL_SOURCE`; an unknown nested key produces
`UNAUTHENTICATED_MATERIAL_SOURCE`; a future-child marker produces
`FUTURE_CHILD_INFORMATION_LEAK`. Ordinary lawful positive paths are not refused.

**Why the legacy G16I test is refused.** Its mutation is the exact defect class
the G17I review exposed. Accepting it would restore the caller-schedule bypass.
The source-issued 7/2 schedule proves the same science without that bypass.

---

## 3. HQ ACTION REQUESTED AND ACCOUNTABLE OWNER

| HQ ACTION | ACCOUNTABLE OWNER | EXACT DECISION / RECEIPT REQUIRED |
|---|---|---|
| Intake this G18 candidate and decide scoped adoption of the authenticated sourcefree material method | Sorok HQ (scoped method adoption only) | Accept/reject the engineering and scientific scope; no native grade follows. G17I remains the frozen oracle; this return does not create an automatic reviewer queue |
| Resolve M2 native continuation | ADP015/ADP020/CAN008/CAN011 issuers, or Sorok HQ formal coverage acceptance | Issue a source-qualified M2 grammar/owner mapping and replay receipt, **or** formally accept `TYPED_COVERAGE_HOLD_ARCHIVE_GRAMMAR_INCOMPATIBLE` |
| Resolve MP `F_EXISTING` reuse | same owners | Materialise a non-duplicated source-qualified second-parent history, **or** formally accept `TYPED_COVERAGE_HOLD_KNOWN_COUNTERPART_HISTORY_NOT_MATERIALIZED` |
| Issue C9 E1/RULE_A/RULE_T/E2 | C9P/C9PI + CAN008/CAN011 + native C9 consumer owner | Exact E1/E2 grant, readset, occurrence/actuator receipt, scope/expiry/revocation. Current material handoff stays `HOLD_UNISSUED` |
| Issue native actor/parent/biology/psychology and real person generation | Original source/ADP/CAN owners and native person-generation authority | Native grant with actual source/identity; no fixture label, hash or MAC can substitute |
| Authorize C11 physical weld | Pyat/C11 authority | Separate C11 authorization/weld receipt; not attempted here |
| Authorize production/PRE-MAIN/original survey use | Original source owners + HQ/production | Explicit permission and release; not attempted here |
| User consultation on each missing native function | User + competent owner | Ask in plain English: build or reuse the exact issuer? Record the answer. Do not loop indefinitely or substitute a fixture |

---

## 4. THREE COURT VERDICTS

**ENGINEERING — `ACCEPT_SCOPED_SOURCEFREE_AUTHENTICATED_MATERIAL` with one
documented legacy-interface supersession.** All three G17I alternate-interface
bypasses are closed unmodified; the exact G17I oracle is 14/14; G18 is 20/20;
181/67/75/13 are exact; the 73 G13 RED identities are exactly preserved; 14/14
same-node source-fault proofs restore byte-exactly; cold replay and tampered
refusal execute. The G16I 24 court is 21/3, with the third RED being the frozen
pre-G18 unauthenticated schedule interface, not a material defect. Scope
excludes native authority, production and human science.

**SCIENTIFIC — `ACCEPT_SCOPED_TEST_ONLY_AUTHENTICATED_MATERIAL_MECHANISM /
GENERAL_HOLD`.** The model exhibits materially distinct finite sourcefree
histories, authenticated performed actions, conservation, source ownership,
lawful no-effect alternatives and a bounded two-actor contrast. It does not
exhibit native actors, parents, biology, psychology, calibrated rates or two
independently developed human lives. No population, general life-formation or
genealogy claim is earned. M2/MP native sources remain typed HOLDs.

**AUTHORITY — `HOLD`.** No original survey/source, native person/actor/biology/
psychology, ADP/CAN rule, RULE_A/RULE_T, C9 E2, N11/N12, V3, C11 weld, Pyat
world or production adoption is issued. The fixture-origin HMAC receipt is
explicitly `SOURCEFREE_TRUSTED_FIXTURE_ORIGIN_ONLY`,
`native_grant=NOT_GRANTED`; it is not an external issuer signature and cannot
become native authority.

---

## 5. FALSIFIABLE PROOF AND RESTORATION

### 5.1 The seven G17 edges remain proved on the G18 candidate

| Claim | Positive node | Fault | Result |
|---|---|---|---|
| `G17_STOCK_LEDGER_EDGE` | repeated project | project uses 1,000,000 instead of current stock | PASS → assertion RED → restored |
| `G17_FREE_HOURS_CLOCK_EDGE` | repeated schooling | checks ORIGIN hours instead of current hours | PASS → assertion RED → restored |
| `G17_TOOL_STOCK_EDGE` | repeated tool return | checks peer root instead of current tools | PASS → assertion RED → restored |
| `G17_PARTICIPATION_AFTERSTATE_EDGE` | forged participation cash | participation authentication bypassed | PASS → assertion RED → restored |
| `G17_FUTURE_CHILD_PARTITION_EDGE` | top-level future child | leak gate disabled | PASS → assertion RED → restored |
| `G17_JOINED_TERMINAL_STOCK_EDGE` | 6-from-5 terminal | overspend stock guard disabled | PASS → assertion RED → restored |
| `G17_C9_MATERIAL_HANDOFF_EDGE` | severed material parent | severance check disabled | PASS → assertion RED → restored |

### 5.2 Seven new G18 source-boundary edges

| Claim | Positive node | Fault | Result |
|---|---|---|---|
| `G18_MATERIAL_SOURCE_RECEIPT_EDGE` | forged 100000 material refused | receipt gate always accepts | PASS → assertion RED → restored |
| `G18_PERFORMED_ACTION_EDGE` | forged action after-state refused | action receipt gate always accepts | PASS → assertion RED → restored |
| `G18_NESTED_FUTURE_CHILD_EDGE` | nested metadata refused | recursive finder returns empty | PASS → assertion RED → restored |
| `G18_SERIALIZED_FUTURE_CHILD_EDGE` | serialized JSON string refused | string scan disabled | PASS → assertion RED → restored |
| `G18_C9_MATERIAL_SOURCE_EDGE` | forged C9 material refused | C9 material verification bypassed | PASS → assertion RED → restored |
| `G18_ISSUER_PAYMENT_BOUND_EDGE` | out-of-schedule payment refused | payment bound disabled | PASS → assertion RED → restored |
| `G18_SOURCE_SCHEMA_ALLOWLIST_EDGE` | extra nested key wrapper refused | shape allowlist disabled | PASS → assertion RED → restored |

All 14 claims passed the shared proof-integrity gate at
`MECHANICAL_WITNESS_PASS_NOT_SEMANTIC_ADOPTION`; every mutated source was
restored to its exact SHA-256 (`evidence/proof_source_restoration.json`). The
gate is a mechanical falsifier, not a scientific certificate.

### 5.3 Cold replay and exact before/after

* Positive cold replay: `run_candidate.py` → replay → `complete_causal_record_equal=true`,
  `terminal=COMMITTED`.
* Tampered replay (payment 100000 in the frozen packet):
  `terminal=UNAUTHENTICATED_MATERIAL_SOURCE`, `complete_causal_record_equal=false`.
* G17I bypass probe: 100058/COMMITTED/100055 on the baseline; refused/refused/
  refused on G18. Receipt: `evidence/g17i_bypass_before_after.json`.
* Legacy schedule test: strict refusal reason `MATERIAL_BODY_HASH_MISMATCH`;
  source-issued 7/2 positive passes. Receipt:
  `evidence/legacy_schedule_supersession.json`.

---

## 6. SOURCE, IMPORT AND ENVIRONMENT IDENTITIES

Full 422-file manifest with SHA-256 and Git blob SHA-1:
`evidence/source_manifest.json` (tree hash
`e3ad38f1adaa889bf8f5209936dcc88c2062b147fdb51a1062d0625dbe78b44b`).
Custody ledger: `evidence/source_custody.json`.

| Source | SHA-256 | Git blob SHA-1 |
|---|---|---|
| `candidate/lab_sgi1/joint.py` | `755820d7d703cd459aec8271a784c39a69e9374aae501da1cd9f37bbccc21ee9` | `325c4eb738cd61b1803ddc8f7cb8ce97c41ba17f` |
| `candidate/lab_sgi1/continuation.py` | `a02f03791da04b55e5d2abe389685033a6296ea5997b7c55059a96a2c5e567c8` | `fa05ede477200779fcfe706b9a36b4288f3cba5b` |
| `candidate/lab_sgi1/pipeline.py` | `944bf66aa778535bcc748ed2fe88f5f6872c38853aa33b540327b115c86112d6` | `966993e64a800c999e962650eec086f669bc447f` |
| `candidate/lab_sgi1/proposal.py` | `fe97a4166d52fcd6f21b8ab0c776edbfc5a0763747954a9e2e645e597713f0f5` | `3cb3a80a6c259c20a804ddfc5b8d7e8844845bd5` |
| `candidate/lab_sgi1/core.py` | `87f8e0554d467a6395ce1dfcc5a346b12074b85a39757e153bd975e2f9c4237d` | `d748cf32698434392bfed27050d4ddc92978812d` |
| `c9_handoff_consumer.py` | `0e4f95fac63983d1336e9e4646159f04c16a6718e627641c434d903ffebb8ead` | `27e2a5cc4a0434c81b1837d519c9a7db7b7dff40` |
| `tests/test_g18_authenticated_material.py` | `dbd2605c3d0b7ce1758a52ca772ada790445869235fd20e844547c6abfe39b74` | `82316a9d78bccdd3cab4622d0cda46a914284bc9` |
| `tests/test_g17_material_history_consumer.py` | `455ab20e6d0c2f306baf0af8eb8baef05755d0d6798edc090bdca8e4b9491ea1` | `ab422636ef4a0d51f58049275b0fc4d19a609448` |
| G17I oracle `tests/reviewer_oracle/test_g17i_independent.py` | `0e4535a708d83a85d763c592f3d206f0b21dbc599846d7ffcd89cd82f145a5e6` | `83f17006b22271f17c87f4563608de08395d7a1c` |
| G17 baseline `stage/g17_baseline_candidate/candidate/lab_sgi1/joint.py` | `ba0a7e190ae4b572e55176e5683680f2eee6d49c344f44d0c887bb92e469c2ea` | `8f970ce7d97392ad8bed4289469f036d61aef91c` |

Environment passport: `evidence/environment_passport.json` and
`evidence/environment_passport_delta.json` — Python 3.11.3, pytest 9.1.1,
Git 2.39.1, local shared-store worktree, sourcefree deterministic subprocess
courts. No paid API call observed; cash/quota **UNKNOWN**; no model or harness
switch.

Exact commands:

```bash
python3 -B tools/run_g18_courts.py
python3 -B tools/proof_integrity_gate_r1.py witness \
  tests/test_g17_material_history_consumer.py.proof.json --root <repo>
python3 -B tools/proof_integrity_gate_r1.py witness \
  tests/test_g18_authenticated_material.py.proof.json --root <repo>
```

JUnit: `evidence/junit/` (G13 181 by suite, G14 67, G15 75, G16I 24 strict and
baseline, G17 13 baseline/repaired/post-gate, G17I 14 baseline/repaired/post-gate,
G18 20/post-gate). Logs: `evidence/logs/`.

---

## 7. NATIVE FUNCTIONAL GAP AND NOT-RUN INVENTORY

The exact missing native functions, with
**input → authenticating decision → receipt → consumer → scientific effect**,
are recorded in `evidence/native_functional_gap.json`:
M2 continuation grammar; MP `F_EXISTING` history; C9 E1/RULE_A/RULE_T/E2;
native person/biology/psychology; C11 weld. Each card names the competent owner
and the user's plain-English build-or-reuse question.

`evidence/not_run_inventory.json` records: native M2/MP replay, C9 E1/E2,
native actor/parent/biology/psychology, C11 physical weld, C12 genuine person,
original survey/source execution, production/PRE-MAIN, external model/API calls,
native calibration/psychological law — all **NOT_RUN/HOLD**, with reasons.

`evidence/authority_hold_register.json` records each hold, owner, required
receipt, blocked consumer and scientific effect.

---

## 8. LIMITS AND DISCLOSURE

1. The sourcefree fixture origin uses a deterministic, in-source HMAC key. It is
   a **test-only fixture anchor**, not an external issuer secret and not native
   authority. A source-level attacker who can rewrite `lab_sgi1/joint.py` could
   re-sign; the boundary against that is exact source custody, the 14-claim
   mutation gate and HQ review, not a claim of cryptographic external issuance.
2. The authenticated material boundary proves source ownership at the declared
   fixture grain. It does not prove that a real person, parent, encounter,
   biology or psyche exists.
3. The two-actor contrast is two finite sourcefree material histories, not two
   independently developed human lives. Its perceived states remain
   `UNKNOWN_OR_NONRECIPROCAL`; no psychological law follows.
4. G16I 24 is 21/3 strict, not 22/2. The one new RED is the frozen pre-G18
   unauthenticated schedule interface. This is disclosed as a necessary
   interface supersession; the same scientific effect is proved through the
   source-issued schedule API. HQ may accept it or direct a legacy adapter.
5. M2/MP native continuation/reuse remain exact typed HOLDs. No child, parent,
   biological or C12 person was fabricated.
6. C9 remains a bounded material handoff; full E1/RULE_A/RULE_T/E2 is
   `HOLD_UNISSUED`.

---

## 9. PUBLICATION

| Item | Value |
|---|---|
| Branch | `agent/rabochii-sorok-20261019-g18-authenticated-material-history-whole-c4-c9-repair-r1` |
| Sealed startup | `19503a3ea09bdf840a5ce98a9697650c387787fa` |
| Substantive return commit | `__RETURN_COMMIT__` |
| Remote verification | `__REMOTE_VERIFICATION__` |
| Final pushed tip | `__FINAL_TIP__` |
| Publication receipt | `PUBLICATION_RECEIPT.json` |

Only this branch is committed and pushed (ordinary non-force push). No
self-adoption; Sorok HQ owns the post-return review decision.
