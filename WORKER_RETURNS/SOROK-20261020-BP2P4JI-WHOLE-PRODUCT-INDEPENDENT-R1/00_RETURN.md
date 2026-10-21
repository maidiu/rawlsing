# SOROK BP2P4JI — INDEPENDENT WHOLE-PRODUCT AND C12 CUSTODY COURT R1

## Identity and custody

| Binding | Value |
|---|---|
| Repository | private `maidiu/rawlsing` |
| Branch | `agent/reviewer-sorok-20261020-bp2p4ji-whole-product-custody-independent-r1` |
| Sealed startup | `a413a3ed0cce3d364991ad3c3b48c0201375926c` (HQ R25; contains the BP2P4JI commission) |
| Review target | BP2P4J `5b3e6577400ea1d88971ae6b48e41a118b8059ae` |
| Model / harness | DeepSeek V4.1-Flash, reasoning MAX, one accountable reviewer in OpenCode; no model/harness switch |
| Write scope | `WORKER_RETURNS/SOROK-20261020-BP2P4JI-WHOLE-PRODUCT-INDEPENDENT-R1/**` only |
| Upstream edits | **none**; BP2P4J, BP2, BP4, BP1, BP3, C9R/C9RI and the author runtime were read-only staged copies |

No reviewer branch or local session existed before this court; the author BP2P4J worktree was left untouched.

---

## FINDINGS

### 1. Courts reproduced independently

| Court | Result | JUnit |
|---|---|---|
| BP2P4J new courts (product 10 + security 12 + severance 7 + source closure 4) | **33/33 PASS**, 0 failures, 0 errors, 0 skips | `junit/new_33.xml` |
| Original BP2 court (byte-exact vendored copy) | **50/50 PASS** | `junit/original_bp2_50.xml` |
| Original BP4 court (byte-exact vendored copy, pinned live `rawlsing_next`) | **15/15 PASS** | `junit/original_bp4_15.xml` |
| Source closure | **150/150 manifest files verified** against origin commits BP2 `5065e2e…`, BP4 `d868e82…` | `evidence/reproduced_courts.json` |

Commands and paths are in `evidence/reproduced_courts.json` and `logs/`. The target tree was staged read-only from `5b3e65774`; `repro/stage_target.py` rebuilds it.

### 2. Literal origin and fresh join both exist, with an honest distinction

The surviving local BP2 origin runtime is present and was independently loaded:

| Literal BP2 identity | Verified value |
|---|---|
| target | `950a4c7903cbe832c72d234a0095946720910c23c8235a28c3118afd8fc1b9f8` |
| record hash | `8d784d48096f4d32d0df3d7c659a23b501681877a948580e0c0150ac60efcd3e` |
| consumed state | `4907a662d2494d9f7949d1f809195264e001f90d39021feb73e5a75cc31c656d` |
| C8 occurrence / state digest | `OCC-0001` / `058d006c1ce79d2783b02a3bb4e2f92d0672aec9b406b5f3312453f9c5608b4b` |
| E2 receipt | `19349fd6fded91f222d50ef5774deab1203619c390fb554e2bd4970e9c7f05aa` |
| RULE_A / RULE_T / grant | `aa5033ca…` / `457894cf…` / `3236a560…` |

`evidence/literal_origin_verified.json`. The literal C8 receipt/key/path are local and not portable; the committed fresh join reproduces the path/key-independent invariants and explicitly classifies the path/key-bound fields as recomputed (author reconciliation test passed). No literal identity was fabricated on a new key.

### 3. MANDATORY C12 DISCREPANCY — RESOLVED: DELIVERED VERIFIER DEFECT, NOT C12 CORRUPTION

The security receipt's `independent_chain_verify.ok=false` with `episode:0:body_hash_mismatch` is **reproduced exactly**, and its cause is now proven:

- A fresh `JoinedProduct` **without** an episode: independent verify `ok=true` (checkpoint/world/perception rows verify); upstream BP4 verify is already `ok=false` (self-referential).
- After one valid **`say`** episode: independent verify is `ok=false` with `episode:0:body_hash_mismatch`; the same row is **intact**:
  - `digest(body minus hash)` = `19bd5075…` (delivered verifier's preimage) ≠ body hash;
  - `digest(body minus hash minus episode_id)` = `6d0342e7…` = the stored body `hash` column.
- The delivered `bp2p4/c12_verify.verify_branch_chain` excludes only `hash`, but BP4 `C12Store.append_episode` computes the hash **before** appending `episode_id`. The `episode_id` is post-hash metadata, so the verifier's preimage is wrong.
- The author's `test_upstream_bp4_store_verify_is_self_referential` passes because it has **no episode row**; it is a different fixture state, not evidence that episode rows verify.
- A minimal repaired verifier that excludes `hash` and `episode_id` for episodes returns `ok=true` on the same intact row.

These results are in `evidence/c12_discrepancy.json`. The recorded failure is therefore **not** stale evidence and **not** C12 data corruption: it is a deterministic verifier preimage defect in the candidate's own `c12_verify.py`, triggered by any valid episode. The return's claim that "this return verifies independently" is true only for episode-free stores.

**Minimal failing example:** `JoinedProduct(...); product.say("x"); verify_branch_chain(root)` → `ok:false`, `["episode:0:body_hash_mismatch"]`; the stored row's true preimage hash matches its own `hash` after excluding `episode_id`.

### 4. Seven load-bearing severances and three supplementary variations reproduced

The author's `tests/test_joined_severance.py` exercises the same named assertion
`bp2p4.assertion.joined_downstream_a0_a2_assertion` with seven primary cuts and three
supplementary cuts; all 7 tests passed in the 33-court re-execution. Primary edges:
BP2 C8 proof, BP2 actor history, BP2 RULE_A, BP2 RULE_T, BP2 target hash, BP2 E2
self-performance, BP4 C10/M6 access; supplementary: other-history aliasing,
E2-not-performed, practice-not-materialized. Each baseline passes, the physical cut
reddens the same assertion, and restoration passes. No cut is an authored mock.

### 5. Independent adversarial edges (reviewer additions)

`evidence/adversarial_edges.json`:

| Edge | Observed | Grade |
|---|---|---|
| Raw SQLite `DROP TRIGGER` + `DELETE` on a real episode | deletion succeeds; remaining rows verify `ok=true`; only a stored out-of-band `chain_digest` changes | **HOLD/RESIDUAL** — append-only is in-process, not an OS boundary |
| External chain-digest trust | `chain_digest` is an unkeyed value; an attacker with DB + digest-store access can rewrite it | **HOLD** — no signed/independently custodied anchor |
| C12 episode verifier | valid episode fails the delivered `c12_verify` | **REVISE** — minimal preimage repair required |
| Clock without post-BP2 marker | `TIME_COORDINATE_HOLD` | PASS (typed refusal) |
| Shape-valid envelope / native smuggling / self-actuator / self-occurrence / forged world owner / tampered target | refused by the author's re-executed security court | PASS at TEST_ONLY scope |
| Other-actor aliasing | supplementary severance reddens the same assertion | PASS |
| Literal vs recomputed BP2 identity | literal origin verified locally; fresh join recomputes path/key-bound fields; no mismatch | PASS with local-only literal scope |

### 6. Product behavior and authority

The joined A0/A2 chain executes: the BP2 `V3MS_PRACTICE` target and performed E2
materialize into A's projects/tools and the workshop tool; the offscreen market repair
changes `completed_units` only when the E2/performed practice is present; without E2 the
same clock produces `OFFSCREEN_NO_CHANGE`; A cannot see the offscreen event until travel
+ ATTEND; fork shares the pre-fork root and diverges lawfully. The whole chain is
`TEST_ONLY_SOURCEFREE`; no native ADP/CAN/Pyat/C11/C12 claim is made.

---

## INTERPRETATIONS / ALTERNATIVES

- **Why the C12 verdict is REVISE, not RED:** the stored episode is intact and its true preimage verifies; the failure is in the delivered verifier's preimage selection (`episode_id` was appended after hashing). This is a minimal, exact repair, not a data-loss event. However, the candidate's C12 custody claim is not independently executable on a valid episode until that repair is applied, so scoped whole-product acceptance is not granted.
- **Why the clean test passes:** it has no episode row. The mandatory contradiction is a **fixture difference plus a verifier defect**, not a stale artifact and not C12 corruption. The security receipt's `ok=false` is a truthful signal of the delivered verifier's failure, but the return's interpretation ("upstream only") is incomplete.
- **What the product actually demonstrates:** a source-verified BP2 target/E2 is materialized into real C12/BP4 state and a changed A2 consequence; the offscreen event is source-owned and independent of user text; branch alternatives are causal. This is L1 TEST_ONLY technical behavior, not native psychogenesis.
- **Residual boundaries:** raw SQLite can remove rows if it drops the trigger; the completeness check is an unkeyed digest with no trusted signer; the clock bridge is a declared process-order marker, not a signed chronological proof; the literal BP2 origin is local-only; C8 key/anchor, CAN/ADP, Pyat and C11 remain unissued.
- **Scientific:** the practice label and tool effect are declared TEST_ONLY rule artifacts; no original human developmental psychology, acquired trait, real parent/other source or native world is inferred.

---

## THREE-COURT JUDGMENT

### ENGINEERING — **REVISE**

The whole product chain and 98 reproduced tests pass, and the seven+ primary/supplementary source faults behave causally. But the delivered C12 custody verifier fails on every valid episode, so a required custody claim is not met. Required minimal repair:

1. In `bp2p4/c12_verify.py`, episode verification must recompute the actual stored preimage: exclude `hash` **and** `episode_id` (the post-hash metadata), while world events/checkpoints continue to exclude `hash` only.
2. Add a regression that creates a real episode (`say`) and asserts `verify_branch_chain(root).ok is True`; update the security receipt after the repair.
3. Upstream BP4 owner (`bp4/store.py`, return `d868e82…`) should stop the self-referential `C12Store.verify` by hashing the exact stored preimage, or store `episode_id` inside the hashed preimage. This is a BP4 repair, not an edit to the immutable original in this review.

Owner: BP2P4J C12 verifier owner + BP4 C12 store owner; both are named in the ACTION table. Re-run the 33 + 50 + 15 courts after repair. No C12 corruption was found.

### SCIENTIFIC — **ACCEPT_SCOPED_TEST_ONLY**

Accept the finite declared TEST_ONLY BP2 practice/E2 → BP4 C12/world/A0–A2 consequence and its alternatives. Reject any reading as original human psychogenesis, acquired personality, real parent/other source or native world. The scientific content remains with the competent owners.

### AUTHORITY — **HOLD**

CAN008 concrete RULE_A, CAN011 RULE_T/grant, ADP007/010/015/016/017/019/020 actor/event/E2, production C8 D1/D2/D3, Pyat N11/N12, C11 and native C12 remain unissued. No sourcefree L1 result is native authority.

---

## HQ ACTIONS / OWNERS

| ACTION | OWNER | REQUIRED DECISION/WORK | EVIDENCE |
|---|---|---|---|
| Repair C12 episode verification | BP2P4J author / C12 verifier owner | exclude `episode_id` from the episode preimage; add valid-episode regression; regenerate `security_receipt.json` | `verify_branch_chain` ok on a real `say` episode; JUnit |
| Repair upstream BP4 `C12Store.verify` | BP4 C12 store owner (`d868e82…`) | verify the exact stored preimage or include `episode_id` before hashing | upstream verify agrees with the independent verifier on all row types |
| Accept/reject the L1 whole-product tranche | Sorok HQ | scoped engineering decision after the C12 verifier repair; no native promotion | this return + repaired JUnit/cold/severance receipts |
| Secure C12 completeness/anti-rollback | independent key/anchor custodian | signed out-of-band chain digest and raw-SQLite protection | signed anchor + tamper test |
| Native rule/event/actor/E2 | CAN008/CAN011/ADP owners | issue exact rule/grant/actor/event/E2 receipts | owner receipts, registries, clocks |
| Pyat world / C11 / native C12 | Pyat HQ / C11 owner | separate original-world and weld decisions | native receipts; no Sorok mutation |
| Literal-origin portability | BP2/BP4 custodians | keep the literal cross-check local-only or publish a lawful portable origin | origin-change reconciliation, no fabricated key/path |

---

## NOT RUN / LIMITS

- Native CAN008/CAN011/ADP007/010/015/016/017/019/020 issuance, C8 D1/D2/D3 production trust, Pyat N11/N12, C11, native C12: **NOT_RUN / HOLD**.
- Upstream code repair: **not performed** in this review; the minimal repair contract is named above with exact owners.
- Literal BP2 origin: verified locally but not portable; the fresh join is the reproducible path.
- Raw-respondent/private source, production install, automatic reviewer launch: not used.

## REPRODUCTION

```text
python3 repro/stage_target.py          # rebuild runtime/target from 5b3e65774
cd runtime/target && python3 -m pytest tests          # 33
cd runtime/target/vendor/bp2 && python3 -m pytest tests  # 50
cd runtime/target/vendor/bp4 && PYTHONPATH=<checkout> python3 -m pytest tests  # 15
python3 repro/c12_discrepancy.py      # mandatory C12 court
python3 repro/adversarial_edges.py    # raw SQLite / clock / fresh join
```

JUnit: `junit/`. Evidence: `evidence/{reproduced_courts,c12_discrepancy,adversarial_edges,literal_origin_verified}.json`. Environment: `ENVIRONMENT_PASSPORT.json`.

## EXACT PUSHED REF

Return commit: `<filled after commit>`. Remote verification: `<filled after push>` (`git ls-remote` must match). Ordinary non-force push; only this review return subtree changed.
