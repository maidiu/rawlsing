# SOROK C9RI — Independent productive-compatibility and E2-consumer court

**Reviewer branch:** `agent/reviewer-sorok-20261019-c9ri-independent-positive-compatibility-e2-consumer-r1`
**Exact sealed startup:** `85d78d928d03d33f80d59d259a6aad9c57967a98` (self-created branch; HEAD verified before work; no existing C9RI lane found).
**Exact review target:** C9R `6fa2939972ce5a2c0cc4f2b033946b276f1c2934` (final return commit; parent `be3251f2af…`, the author's post-repair verification commit for remote SHA `ddcb448b…`).
**Role/model:** single independent I2 reviewer in OpenCode, DeepSeek V4.1-Flash (user-routed), reasoning MAX requested; zero model/harness switches. Not C9R author, C9PI, HQ, CAN/ADP issuer, production integrator.
**Write scope:** only `WORKER_RETURNS/SOROK-20261019-C9RI-INDEPENDENT-PRODUCTIVE-COMPATIBILITY-R1/**`. No frozen C9P/C9PI/C9R file, test, native module, CAN/ADP/Pyat/production artifact was edited (witness mutations ran on staged copies and were restored by the shared gate).

---

## FINDINGS

### 1. Provenance and closure (independently verified)

* The C9R return vendors the C9P target and C9PI oracle. I verified every staged origin file byte-for-byte against the origin commits **with my own git-blob comparison** (not the C9R manifest):
  * C9P `38fba47614e82a86fc5a3fa3f50c27048493e808`: **42/42 files identical**.
  * C9PI `df2382b8d9478f0a904dcff06ee45bb0119a1bda`: **132/132 files identical**.
  * Receipt: `evidence/origin_closure_verification.json`.
* Target tree provenance: `6fa29399` is a child of the author's return commit `be3251f2`; the only delta is the banked remote-verification record. No divergence between the author's pushed return and the commissioned review target.
* Ambient workspace pytest config poisons the frozen `from conftest import …` court pattern; all runs used an external neutral ini. This is an environment artifact, not a return defect.

### 2. Reproduction (all counts independently re-executed)

| Court | My result | Expected | JUnit |
|---|---|---|---|
| C9P author baseline (exact target) | **90 PASS / 0 RED** | 90/90 | `evidence/c9ri-baseline-author-90.xml` |
| C9PI baseline review (hostile 26 + custody 3 + edges 6) | **17 PASS / 29 RED** (26 hostile + 3 custody RED) | 11/26 + 0/3 + 6 edges | `evidence/c9ri-baseline-review.xml` |
| C9R candidate vs frozen C9PI review | **46 PASS / 0 RED** | all repaired | `evidence/c9ri-repaired-review.xml` |
| C9R candidate vs original author suite | **62 PASS / 28 RED** | 62/28 | `evidence/c9ri-repaired-author-90.xml` |
| C9R direct consumer court | **10 PASS** | 10 | `evidence/c9ri-c9r-consumer.xml` |
| C9R six same-test fault trials | **6/6 PASS→RED→PASS** (reproduced) | 6/6 | `evidence/c9ri-reproduced-c9r-fault-trials.json` |
| C9R two-database cold replay | **logical snapshots equal; integrity ok; read HELD** | equal | `evidence/c9ri-reproduced-c9r-cold-replay.json` |
| My independent court (below) | **17 PASS** | — | `evidence/c9ri-court.xml` |
| My eight severance witnesses | **8/8 baseline PASS → assertion RED → restored** | — | `evidence/c9ri_proof_witness.json` |

### 3. The 28 author-suite divergences — adjudicated case by case

Independent classification (full machine-readable trace per row:
`evidence/c9ri_28_row_compatibility_ledger.json`):

| Classification | Count |
|---|---|
| `HISTORICAL_FALSE_POSITIVE_FIXED` | 13 |
| `SCIENTIFIC_ADAPTER_INCOMPATIBILITY` | 14 |
| `NATIVE_AUTHORITY_PREVIOUSLY_UNISSUED` | 1 |
| `LEGITIMATE_FUNCTIONAL_POSITIVE_LOST` | **0** |
| `PREIMAGE_NOT_REPRODUCIBLE` | **0** |

Systemic roots, traced to exact gates:

1. **Focal actor binding (7 pipeline tests + the differential test).** The C9P
   pipeline fixtures build events with `actor_role="ACTOR_A"` while the focal
   actor is `actor-c9p-001`; the repaired `events.ingress_event` requires the
   witness role to bind the focal actor (`events.py:214-225`), exactly the C9PI
   hostile `test_wrong_actor_event_refused` requirement. Those downstream
   positives were inadmissible; the intended outcomes are reachable with lawful
   fixtures (my independent differential and positive tests).
2. **Manual `TargetDecision` commits (7 tests).** Helpers construct a
   `TargetDecision` by hand and call `commit`; the repaired transaction requires
   a sealed full record preimage plus authorization preimage
   (`transaction.py:191-196`), exactly the C9PI fabricated-decision requirement.
   Reads that followed such fake commits were historical false positives; the
   read/consumer semantics are preserved on lawful commits (my positive).
3. **Under-bound grants (4 tests).** Grants declared arbitrary response hashes
   (`"r1"`, `"resp-sev"`) or none at all; the repaired gate enforces exact
   response binding (`target_rules.py:382-389`), the C9PI
   `test_target_grant_exact_binding[response_hash-WRONG_RESPONSE]` requirement.
   The lawful CREATE is preserved with an exact grant.
4. **Label-only evidence (4 tests).** Author fixtures passed `"h-a","h-b"`,
   `"offer-1"`, `"world-1"` without the TEST_ONLY declared-evidence namespace;
   the repaired response gate requires distinct TEST_ONLY_-namespaced enacted
   refs, an independent declared offer and material refs
   (`response_rules.py:241-270`). These were false positives under the accepted
   sourcefree adapter; the same semantics are preserved with declared evidence
   (my positive; C9PI's own positive edge).
5. **Boolean authority (3 release-gate tests).** Caller booleans no longer clear
   or reshape native holds (`release_gate.py`). The one test expecting a native
   `AUTHORIZED` from booleans could only ever have been
   `NATIVE_AUTHORITY_PREVIOUSLY_UNISSUED`; the other two relied on boolean-derived
   hold lists.
6. **Missing performed-action commit-time binding (2 tests).** Old receipts
   omitted `target_commit_time`; the repaired admission requires it
   (`action_admission.py:246-253`) per the C9PI pre-commit hostile case. The
   admitted positive is preserved with a bound receipt.
7. **Refusal-precedence changes (14 rows; `SCIENTIFIC_ADAPTER_INCOMPATIBILITY`).**
   Tests that already expected a non-positive outcome (DENY/abort/HELD/absence)
   still fail closed, but a stricter earlier check fires first or the pipeline
   aborts before the old stage. No positive branch was granted; each intended
   non-positive semantic is preserved by the repaired path, my court, or a
   passing C9PI case (e.g., `COMMIT_READSET_MISSING` vs `STALE_TARGET_PRESTATE`,
   `AS_OF_BEFORE_COMMIT`, `CONSUMER_READSET_MISMATCH`, `NO_CHANGE` with exact
   grant, `ACTION_BEFORE_TARGET_COMMIT`).

**Conclusion on the 28:** the divergences are not a denial-only collapse. The
lawful positive mechanism survives and is exercised by three independent bodies
of evidence: C9PI's own frozen positive edge (`test_permission_conditions_full_create`,
`test_committed_target_conditions_cold_later_read` — passing before and after),
C9R's ten direct consumer cases, and my own reviewer-authored positive. No
legitimate previously-authorized positive was lost; the 29 hostile/custody REDs
remain closed on unmodified frozen files.

### 4. My independent lawful positive / NO_CHANGE / DENY / adversarial court

Reviewer-authored fixtures (`TEST_ONLY_C9RI_*`), distinct from C9P/C9R:

* **Lawful positive:** actor ingress → E1 event (focal binding) → read-only
  conditioning (material access granted) → CAN008 `RULE_A` (TEST_ONLY) →
  response receipt → CAN011 `RULE_T` (TEST_ONLY) with exact response-bound grant →
  full sealed record + authorization preimage → SQLite atomic commit → cold
  reopen byte-equal → later E2 consumer read of exact committed state
  (`ACTION_ADMISSION_HELD` without an owner receipt) → independently performed
  action admitted with `target_commit_time` and exact consumed-state hash.
* **NO_CHANGE:** empty declared history → `NO_CHANGE`; occurrence preserved; no
  target row.
* **DENY:** denied material access and a revoked grant both refuse CREATE;
  occurrence preserved; no target/ghost rows.
* **Differential:** two lawful trajectories (workshop/wrench vs garden/spade)
  produce distinct event hashes, records and target identities, both committed.
* **Adversarial:** forged consumed state (`CONSUMED_STATE_MISMATCH`), pre-commit
  action (`ACTION_BEFORE_TARGET_COMMIT`), self-actuator
  (`ACTUATOR_SELF_BOUND`), unperformed occurrence
  (`OCCURRENCE_NOT_INDEPENDENT`), counterfeit consumer body
  (`CONSUMER_READSET_MISMATCH`), manual fabricated decision (aborted
  `TARGET_RECORD_PREIMAGE_MISSING`), commit readset blindness (aborted
  `COMMIT_READSET_MISSING`), injected SQLite fault (rollback, no ghost), stale
  actor clock (`STANDING_STATE_STALE`).
* **G17/C8 laundering:** a native-grade forged-material event is refused without
  an owner receipt resolver; a C8-looking owner ref with TEST_ONLY grade is
  refused by the TEST_ONLY namespace check; a `native_positive_claim` is
  `NATIVE_ADMISSIBILITY_HELD`; caller booleans cannot clear the release gate.
  No synthetic actor source can become native.
* **Eight severance witnesses** (shared gate, staged candidate mutated then
  restored): actor/clock, event source-owner readset, target record preimage,
  permission revocation, consumed state, performed-action ordering, SQLite
  commit readset, declared-response binding. All baseline PASS → named assertion
  RED → restored (`evidence/c9ri_proof_witness.json`).

---

## INTERPRETATION

The C9R mechanism creates a finite, falsifiable differential change: a
TEST_ONLY E1 event plus declared evidence conditions a response, a separately
typed target rule persists one full semantic record (with exact response,
permission, causal parents, before-state and publication grade), and a later E2
consumer is admitted only from a receipt bound to the exact committed state
hash and to a post-commit independently declared action. Alternative branches
are genuinely preserved: insufficient declared history → `NO_CHANGE`; denied
material / revoked permission → refusal with occurrence preserved; native
claims → typed HOLD. Severing the record, response binding, permission, consumed
state, action ordering, actor clock or SQLite readset reddens the same named
assertions.

**Alternative hypotheses considered.** (a) “The 28 REDs are simply a
denial-only hardening.” Rejected: C9PI's own positive edge and my independent
positive both produce a committed CREATE and later read after the repair.
(b) “C9R silently weakened the frozen oracle.” Rejected: my file-level closure
check is 42/42 and 132/132 byte-identical, and I re-ran the frozen courts
unmodified. (c) “The old 90-suite represents a lost lawful positive class.”
Rejected for every row: each failure traces to a specific now-forbidden unsafe
input (focal-binding, fabricated decision, under-bound grant, label-only
evidence, caller booleans, missing commit-time) or to a refusal-precedence
change; no row depends on a semantic capacity that is unavailable.

**Confidence.** High for the engineering findings (all counts and mutations
reproduced from exact bytes); high for “no lost lawful positive at TEST_ONLY
grain” (three independent bodies of positive evidence); the scientific reading
is bounded to declared TEST_ONLY semantics, not human practice.

---

## THREE COURT VERDICTS

* **Engineering — `ACCEPT_SCOPED`.** 29/29 frozen C9PI REDs closed on unmodified
  files; 46/46 repaired review; 10/10 author consumer cases; 6/6 author fault
  trials and two-DB cold replay reproduced; my 17-case court and 8/8 same-edge
  severance witnesses pass; every one of the 28 divergences independently traced;
  no lawful positive lost.
* **Scientific — `ACCEPT_SCOPED_TEST_ONLY_DECLARED_EVIDENCE_MECHANISM`.** A real
  finite differential mechanism with preserved alternatives (positive,
  NO_CHANGE, DENY, held native claim), not a human-population claim. Concrete
  CAN008/CAN011 semantics remain outside this court.
* **Authority — `HOLD`.** No native RULE_A/RULE_T, ADP019 occurrence, ADP010
  encounter, performed-action owner receipt or PSEPF positive-registry entry is
  issued; no test/source hash/boolean/registry label can create native
  authority. Owners named below.

---

## MISSING_FUNCTION_CHECK / FUNCTION_CARD

**Question:** Is the native actual actor/response/target/performed-E2 producer
already present, partially built, unconnected, or unavailable?

**Answer: partially built and unconnected; the missing piece is competent
issuer/admission evidence, not code capability.**

| Layer | Carrier (exact) | State |
|---|---|---|
| Zero-positive firewall (consumed) | `rawlsing_next/v3_psepf_zero_positive_guard.py` (blob `e0528d65…` per C9P owner graph), `wsc_gt0_v3_runtime.py`, `wsc_gt0_protocol.py` | present, imported, diagnostic DENY_ZERO_EFFECT preserved |
| ADP-010 encounter/opportunity machinery | `rawlsing_next/v3_adp010_oee_executor_authenticated.py`, `v3_adp010_oee_executor.py` (bounded AVAILABLE→OPPORTUNITY→ENCOUNTER; consumes an already-owned subject ref; creates no subject/contact/exposure) | reusable; not invoked as positive authority |
| ADP-010 input-authority verifier | `rawlsing_next/gt34_adp010_input_authority_acceptance.py`, `v3_adp010_oee_executor_obl055_acceptance_bound.py` | verifier exists; **installed registry zero-positive → fails closed** |
| C9 transport/commit/consumer | C9R `candidate/` (event witness, rule registries, exact target record/preimage, SQLite readset, later-action consumer, performed-action admission) | present, tested at TEST_ONLY |
| Concrete CAN008 RULE_A | adoption/canon documents exist; **concrete rule body/version/hash unissued** | missing issuer decision |
| Concrete CAN011 RULE_T + grant | canon exists; **concrete target rule, CREATE/NO_CHANGE/DENY grant, before/read/write sets, expiry/revocation unissued** | missing issuer decision |
| ADP019 occurrence admission / ADP010 encounter receipt | executor/verifier code exists; **no admitted occurrence/encounter receipt issued** | missing owner receipt |
| Independently performed E2 action | C9R admission logic exists; **no native actuator/occurrence owner receipt issued** | missing owner receipt |
| PSEPF positive-transition registry | guard exists; **production registry empty by design** | missing binder decision |

**Plain-English gap:** inputs (exact admitted event/encounter + signed concrete
rules + grant) → available transformation (ADP-010 executor + C9R transaction /
consumer) → output (full target record + later-action read) → consumer (E2
action admission / C10 world binding). The transformation and consumer exist;
what is missing is the externally issued input authority. A correct
`TYPED_REFUSAL` here is not a missing function.

---

## HQ ACTION / OWNER

| Recommended HQ action | Competent owner | Required decision | Evidence satisfying it |
|---|---|---|---|
| Adopt the scoped TEST_ONLY mechanism | Sorok HQ | Accept at `ACCEPT_SCOPED`; no native grade | this return + JUnit + witness receipts |
| Issue concrete RULE_A | CAN008 R2 concrete-rule issuer | One exact signed rule body/version/hash, subjects, predicates, effective time | issuing-office adoption record + rule preimage |
| Issue concrete RULE_T + grant | CAN011 target owner | Exact target rule + CREATE/NO_CHANGE/DENY grant with before/read/write sets, expiry, revocation | separate adoption record + grant id/scope |
| Admit occurrence | ADP019 external admission court | Exact event id/hash/time + owner receipt | admission receipt + event cursor |
| Bind encounter | ADP010 encounter owner | Exact encounter to actor identity | encounter receipt (registry acceptance) |
| Bind performed E2 action | Native later-action consumer/actuator owner | Register reader + admit one performed action after commit | consumer/actuator/occurrence receipt |
| Populate positive registry | PSEPF production registry binder | Separate accepted authority change | registry artifact + binder change |
| Native adoption | Sorok HQ + issuers + fresh I2 | New native positive only after all receipts | full native bundle |

**Not adopted by this reviewer. No self-adoption.**

---

## NOT RUN / LIMITS

No native C9 positive, no human H1/H2/H3 science, no canon/identity issuance, no
ADP/Pyat/world/N11/N12/C10/C11/C12 action, no production installation, no
power-loss or media-durability proof, no exactly-once claim, no original source
read, no re-litigation of C9PI's frozen findings. C9R's `.gitignore`d runtime
SQLite trees were not committed; cold DBs were regenerated by my runs.

## ENVIRONMENT / COMMANDS

Python 3.11.3 · pytest 9.0.2 · Git 2.43.0 · macOS x86_64 · SQLite stdlib ·
`PYTHONHASHSEED=0`, `PYTHONDONTWRITEBYTECODE=1`, external neutral pytest ini
(ambient importlib poison avoided). Passport:
`evidence/environment_passport.json`. Cost: **UNKNOWN**. Key commands:

```
python repro/stage_courts.py
pytest -q -c <neutral.ini> runtime/repro/WORKER_RETURNS/SOROK-…-C9P-…/tests   # 90 pass
pytest -q -c <neutral.ini> runtime/repro/review                                  # 17 pass/29 RED
pytest -q -c <neutral.ini> runtime/repaired/WORKER_RETURNS/SOROK-…-C9P-…/tests  # 62 pass/28 RED
pytest -q -c <neutral.ini> runtime/repaired/review                               # 46 pass
pytest -q -c <neutral.ini> tests/test_c9r_consumer.py                            # 10 pass
python run_c9r_evidence.py                                                       # 6/6 faults + cold
pytest -q -c <neutral.ini> WORKER_RETURNS/SOROK-20261019-C9RI-…/tests           # 17 pass
python severance/proof_integrity_gate_r1.py witness <my contract> --root .       # 8/8
```

## EXACT PUSHED REF

Return commit for this packet: recorded by the commit carrying this file; remote
verification of the branch tip is in `evidence/remote_verification.json` and the
final answer to HQ. Ordinary non-force push, only this reviewer subtree changed.
