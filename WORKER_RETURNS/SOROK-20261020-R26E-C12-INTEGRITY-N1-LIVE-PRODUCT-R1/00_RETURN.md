# SOROK R26E — C12 INTEGRITY, N1 METHOD, LIVE PERSON-PRODUCT COMPLETION R1

## Identity and custody

| Binding | Value |
|---|---|
| Repository | private `maidiu/rawlsing` |
| Branch | `agent/rabochii-sorok-20261020-r26e-c12-integrity-science-live-product-r1` |
| Sealed startup | `dba95216d5627513ea36323f459cf97413b504d1` (remote branch existed at this exact seal; no prior worker commits) |
| Model / harness | DeepSeek V4.1-Flash, reasoning MAX, one accountable agent in OpenCode; no model/harness/subagent switch |
| Write scope | `WORKER_RETURNS/SOROK-20261020-R26E-C12-INTEGRITY-N1-LIVE-PRODUCT-R1/**` only |
| Pinned inputs | BP2P4J `5b3e65774`; BP2P4JI review `3212d716c`; N1 `cd6b0fb93`; BP2 `5065e2e69`; BP4 `d868e82c7` |
| Native authority | none; TEST_ONLY sourcefree only |

Checked before starting: no local R26E branch/worktree/process existed; the remote branch held only the commission seal. BP2, BP4, BP2P4J, N1 and the BP2P4JI review branch were not edited or reset.

---

## FINDINGS

### 1. Reproduced courts and the previously NOT_RUN N1 port court

| Court | Result | JUnit |
|---|---|---|
| BP2P4J new 33 (product 10, security 12, severance 7, closure 4) | **33/33 PASS** | `junit/bp2p4j_33.xml` |
| Original BP2 50 | **50/50 PASS** | `junit/bp2_50.xml` |
| Original BP4 15 | **15/15 PASS** | `junit/bp4_15.xml` |
| N1 source-neutral methodology 21 | **21/21 PASS** | `junit/n1_21.xml` |
| **N1 actual BP2 ports (previously NOT_RUN)** | **2/2 PASS** | `junit/n1_bp2_ports.xml` |
| R26E own qualified-C12/N1/product court | **8/8 PASS** | `junit/r26e_new.xml` |

**129 tests total, 0 failures/errors/skips.** The N1 port test ran against the exact vendored BP2 `bp2_joined.ports` from BP2P4J, not a mock: it compiles only TEST_ONLY A/T resources, leaves `grant=None`, and production registries remain empty.

### 2. C12 valid-episode discrepancy physically repaired (owned derivative)

`r26e/c12_integrity.py` subclasses the pinned BP4 `C12Store` and overrides only verification. The corrected preimages are:

- **episode**: exclude `hash` **and** the post-hash `episode_id`;
- **world_event / checkpoint**: exclude `hash` only (their actual source-owned preimage);
- sequence continuity and column-vs-body hash equality are checked for every row type.

Executed on a real `say` episode (`evidence/r26e_receipts.json → c12_valid_episode`):

- qualified verify `ok=true`, counts `episode=1, world_event=2, checkpoint=2, perception=4`;
- cold reopen in a fresh store `ok=true` with identical counts;
- stored body hash `3dd791d9…` equals both the body `hash` field and the column hash;
- `digest(body minus hash)` does **not** match (the old delivered verifier preimage);
- `digest(body minus hash minus episode_id)` does match;
- the pinned upstream `C12Store.verify` remains `ok=false` (its self-hash defect), as expected and documented.

This is a **real repair on populated episodes**, not an empty-fixture green test.

### 3. Raw SQLite attack and honest external-trust boundary

`evidence/r26e_receipts.json → raw_sqlite_attack`:

- a separate OS SQLite connection drops `episode_no_delete` and deletes one real episode; deletion succeeds;
- the corrected verifier still validates the remaining rows (`ok=true`, `episode=0`);
- a TEST_ONLY keyed `ExternalCheckpointWitness` separates the C12 DB from its checkpoint file and detects the deletion (`CHAIN_DIGEST_MISMATCH`);
- an attacker able to rewrite both the DB **and** the witness/key (same user trust domain) makes the witness check pass again.

Typed residual: `TRUST_CUSTODY_HOLD`, `TEST_ONLY_SAME_USER_EXTERNAL_WITNESS_NOT_SECURITY_BOUNDARY`, `production_kms_claim=false`. No production KMS or immutable OS completeness is claimed.

### 4. N1 screen integrated through actual BP2 ports — no durable acquisition

`r26e/live_product.py` exposes `n1_screen` / `n1_compile` over the actual BP2 port module. Executed (`n1_ports` receipt):

| Case | Screen status |
|---|---|
| two distinct enacted acts + independent offer + O/E1 | `OWNER_REVIEW_CANDIDATE` |
| missing E1 | `REQUEST_EVIDENCE` |
| no enacted act | `NO_CHANGE` |
| contradictory enacted evidence | `COMPETING` |
| self-report only | `NO_CHANGE` |
| actor as its own other | `DENY` |

The positive case compiles two **separate TEST_ONLY** A/T resources through the real ports (`rule_a_test_only=true`, `rule_t_test_only=true`), **`grant=None`**, `native_registry_mutation=false`, `downstream_state_change=false`, production response/target counts `0`. The product's C12 state is byte-identical before/after the screen and compile. Removing the method screen (ineligible case) yields `REQUEST_EVIDENCE`, no rule, no target, and the committed BP2 target/practice is untouched. H0 (`role/fixture only`) remains `NOT_EXCLUDED_BY_TEST_ONLY_EVIDENCE`; `actor_self_knowledge=UNKNOWN_WITHOUT_ADP017`.

### 5. Live product retains the actual BP2 source and A0/A2 consequence

`evidence/r26e_receipts.json → product`:

- A0 `OK`, target equals the fresh BP2 joined target, C12 qualified verify `ok=true`;
- the committed BP2 practice/E2 materializes A's projects/tool;
- WAIT to world clock 40 produces the source-owned offscreen repair with **no user command**; B's public completed units rise to 4;
- after travel + ATTEND, the offscreen claim becomes `PERMIT_FIRST_PERSON_KNOWLEDGE`; before ATTEND it is `NONRENDERABLE`;
- reentry claims include `ARRIVAL, SPEECH, MOVE, OFFSCREEN_REPAIR, MOVE`;
- `native_claims` all false; grade remains TEST_ONLY sourcefree.

The original `joined_downstream_a0_a2_assertion` also passes unchanged on the pinned product (`status=PASS`, target/consumed/C8/E2 identities exact).

### 6. Seven primary + three supplementary physical source faults

`evidence/r26e_receipts.json → severance`: the author's same named assertion
`bp2p4.assertion.joined_downstream_a0_a2_assertion` was re-executed with **7/7 primary**
and **3/3 supplementary** cuts (`all_primary_proved=true`, `all_supplementary_proved=true`).
Cuts include C8 proof, BP2 actor history, RULE_A, RULE_T, target hash, E2 self-performance,
C10/M6 access, other-history aliasing, E2-not-performed and practice-not-materialized.
The R26E method-screen removal is an additional fault: it returns no rule/grant and
leaves the actual committed target and practice untouched.

---

## INTERPRETATIONS AND ALTERNATIVES

- The C12 defect was a **verifier preimage** defect, not data corruption: the repaired verifier accepts the intact episode in-process and after cold reopen. The pinned upstream verifier remains self-referential; its eventual repair belongs to the BP4 owner, not this derivative.
- Raw SQLite erasure is a real residual. The TEST_ONLY external witness detects deletion only against a separately held checkpoint; a same-user attacker who rewrites both is not stopped. This is `TRUST_CUSTODY_HOLD`, not production security.
- N1 integration does **not** create a durable human practice: the screen can only request competent owner review; the compiled resources are TEST_ONLY and `grant=None`; production registries stay empty. The positive product practice still comes from the **separate** committed BP2 TEST_ONLY target/E2, not from the screen.
- H0 remains live; H1/H2/H3 are not discriminated beyond the declared TEST_ONLY evidence. No original psychogenesis, acquired personality, role/type inference, real parent/other source or native world is claimed.
- The literal-vs-fresh distinction is unchanged from BP2P4J: the fresh join recomputes path/key-bound identities; the literal origin is a local-only cross-check, not fabricated here.

## THREE COURTS

### ENGINEERING — `ACCEPT_SCOPED_SOURCEFREE_QUALIFIED_C12_AND_N1_PORT_INTEGRATION`

The valid-populated-episode C12 verifier is physically repaired in an owned derivative and passes in-process and after cold reopen; the N1 actual BP2 port court runs (previously NOT_RUN); 98 inherited + 21 N1 + 2 port + 8 new tests pass; the BP2 source → C9/C10/C12/M6 → A0/A2 chain remains causal; 7+3 source faults pass; the raw-SQLite/external-trust limit is typed honestly. Scope excludes production KMS, native rules, and original source rights.

### SCIENTIFIC — `ACCEPT_SCOPED_TEST_ONLY_METHOD__H0_ALIVE`

Accept the finite source-neutral evidence screen and its alternatives as a TEST_ONLY method. It never issues RULE_A/RULE_T/grant, never acquires a human practice, and preserves `OWNER_REVIEW_CANDIDATE` as a request to a competent owner. H0 remains live until genuine original evidence discriminates it; no population or individual psychology is inferred.

### AUTHORITY — `HOLD`

Concrete CAN008 `RULE_A`, independent CAN011 `RULE_T`/grant, ADP007/010/015/016/017/019/020 actor/event/E2, C8 D1/D2/D3 production trust, Pyat N11/N12 (R53 STOP), C11 and native C12 remain unissued. No self-adoption or native promotion.

---

## HQ ACTIONS / OWNERS

| ACTION | OWNER | REQUIRED DECISION/WORK | EVIDENCE |
|---|---|---|---|
| Adopt the qualified C12 verifier repair into the canonical product | BP4 C12 store owner + BP2P4J owner | merge the episode/world/checkpoint preimage fix; regenerate security receipt on populated episode | repaired verifier + cold JUnit + valid-episode receipt |
| Decide the L1 sourcefree product tranche | Sorok HQ | scoped acceptance after C12 repair; no native promotion | this return + 129-test JUnit + severance |
| Replace the TEST_ONLY external witness with real custody | independent key/anchor custodian | signed out-of-band chain anchor outside the DB trust domain; raw-SQLite protection | signed anchor + deletion test |
| CAN008 concrete RULE_A | competent V3/CAN008 rule issuer | issue exact rule body/hash/registry/currentness | issuer receipt |
| CAN011 RULE_T + grant | separate CAN011 target owner | issue exact target rule and conditional grant | adoption/grant receipt |
| ADP actor/other/E1/E2 and memory/access | ADP007/010/015/016/017/019/020 owners | issue actual actor, encounter, occurrence, performed E2, memory/access receipts | owner receipts/clocks |
| Pyat world / C11 / native C12 | Pyat HQ / C11 owner | separate world receipt and weld decision; R53 STOP respected | native receipts |
| N1 finite science petition | competent original science office | decide ADOPT/REVISE/REJECT/REQUEST_EVIDENCE on the one bounded practice packet | decision packet + evidence |

---

## NOT RUN / LIMITS

- Native CAN008/CAN011/ADP/Pyat/C8-D1-D2-D3/C11/C12: **NOT_RUN / HOLD**.
- Production KMS or OS-immutable C12 completeness: **not claimed** (`TRUST_CUSTODY_HOLD`).
- Original human psychogenesis, population inference, role/type/Enneagram inference: not attempted.
- Literal BP2 origin: local-only; the fresh join is the reproducible path.
- No upstream file edited; the repair is an owned derivative. No self-adoption or new worker.

## REPRODUCTION

```text
python3 repro/stage_sources.py            # stage BP2P4J 5b3e65774 and N1 cd6b0fb93
cd runtime/target && python3 -m pytest tests                    # 33
cd runtime/target/vendor/bp2 && python3 -m pytest tests         # 50
cd runtime/target/vendor/bp4 && PYTHONPATH=<checkout> python3 -m pytest tests  # 15
cd runtime/n1/tests && PYTHONPATH=../source:. python3 -m pytest test_n1_eligibility.py  # 21
PYTHONPATH=../source:.:../../target/vendor/bp2 python3 -m pytest test_bp2_actual_ports.py  # 2
python3 -m pytest tests                                          # 8 (R26E)
python3 repro/evidence_driver.py
```

JUnit: `junit/`. Receipts: `evidence/r26e_receipts.json`. Environment: `ENVIRONMENT_PASSPORT.json`.

## EXACT PUSHED REF

Return commit: `<filled after commit>`. Remote verification: `<filled after push>` (`git ls-remote` must match). Ordinary non-force push; only this return subtree changed.
