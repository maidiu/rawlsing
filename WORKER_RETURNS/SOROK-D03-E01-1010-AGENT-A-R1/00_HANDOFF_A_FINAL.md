# #1010 D03/E01 — AGENT A FINAL COUNTER (B→A) — immutable-source handoff

**Candidate verdict:** `BOUNDED_PREWRITE_AND_PER_EVENT_CUSTODY_REPAIRED__ISOLATED_12_PASS__FULL_S2_NOT_RUN__G2_HISTORICAL_PERFORMANCE_HELD__STOP`.

This is ONE A→B→A descendant. It does not assert self-acceptance, native psychological science, D04/D05, or automatic protected integration.

## 1 — Source/provenance and author lease

- Governing commission: https://github.com/maidiu/rawlsing/issues/1010 ; original PROGRAMMA/27-task D02,D03,E01 and B04/C04 dependencies; original #939 controlled fleet unchanged.
- Protected PRE-MAIN evidence cut (read-only): `6a5c12f04323d74001f9632063ec907f4fc4468e`.
- Initial J1 #996 immutable author return `fb061dec16c8386b9caa1b5ea75ec7645aff88a7`, code/test source `c724d1a89626f3e177acd004c0be20029dc7ade4`.
- Initial A #1016 `6248547b2ad98002245b69cec9e399277d090f12`.
- B #1019 immutable parent `6bfdc3b91b1c77577fdf5545e16ed866016213d4`. B's six-file repair and original tests are all preserved.
- A final branch: `agent/sorok-d03-e01-1010-a-final-counter-r1`. Exact immutable final SHA is the branch head after this handoff. Compare its tree with B head; neither read-only upstream files nor PRE-MAIN may change.

## 2 — B's genuine engineering victory (PRESERVED)

B's `post_provider_guard.GuardedProvider` calls an unchanged provider and synchronously validates P3 head, P2/P3 root/actor/branch/clock/state, and J1 source closure **before** `RecursionCycle` parses and writes its ordered 3–5 events. Its prewrite timing test reproduced A's original late-check sequence. B explicitly rejected false G2 promotion of `P2Owner`'s prebound `case/source` to Nadia's motivated choice. A agrees.

I independently reran B's **exact** committed guard blob `633435c5fa52528265401535986d1dbc3fcafb1d` and its **exact** unit-test blob `b312758563092b134eedc085f3e3a2d11c3d1395`: all four pass with A's eight dependency-free custody tests (12 total).

No source-grounded refutation of B's original correction exists. Do not revert it.

## 3 — New exact defects, root causes, repairs and first-reader impact

**A2-01 P3 pending reservation invisible to B's head check (NEW).** Exact P3 `p3/state_store.py:PsycheStore.pending` returns all `p3_operations` rows with `phase<>COMPLETE`. `PsycheStore.reserve` commits an operation reservation without committing a new P3 record/head. B's callback checks `head()`, `owner.snapshot()`, J1 code closure, but not `pending()`. Consequently, a provider can leave P3 `PREPARED` while the head and P2 snapshot are unchanged; B's validator approves a proposal that P3's own `P3Owner.realize` would refuse as pending. **Repair:** check `owner.store.pending()` both in B's post-provider callback and at every P2 event write; exact refusal codes `E01_POSTPROVIDER_P3_PENDING_OPERATION` and `E01_EVENT_WRITE_P3_PENDING_OPERATION`. No P2 write on positive pending check.

**A2-02 B's guard-to-write race (NEW).** B's proxy runs before `_parse_proposals`, `BatchEngine.run_batch`, and individual `P2Owner.realize` calls. A later legitimate P3 operation could change the head or reserve a pending operation after B approved, before a P2 write. **Repair:** `owner_custody.P3CoordinatedP2Owner` implements only original `DevelopmentOwner` forwarding methods; its `realize` enters the existing P3 `_root_lock`, rechecks pending/head/root/branch/actor/J1 source closure, verifies exact expected P2 state, calls the **original** `P2Owner.realize`, and rechecks before releasing the P3 lock. This uses the same **P3→P2** lock order as `P3Owner.realize`, whose own implementation enters `_root_lock` before `_run_base`; `P2Owner.realize` already locks `recursion_owner.lock`. This closes the race between cooperating original P3 owner writers and the actual P2 owner event commit at each event, not merely once per 3–5 batch.

**A2-03 New implementation files absent from J1 reader closure (NEW).** Original J1 source closure did not include B's guard or A's new owner lease. **Repair:** `_execution_code_closure` pins current module, `GuardedProvider` imported source and `P3CoordinatedP2Owner` imported source via exact expected sibling paths + file SHA-256. It is checked at initialization, after provider, and around each actual writer; the hash is included in the final diagnostic report. It does not imply an atomic filesystem lease against hot rewriting.

## 4 — Tested RED→GREEN / objective evidence

Locally executed exact committed blobs:
```text
B/post_provider_guard.py      633435c5fa52528265401535986d1dbc3fcafb1d
B/test_b_guard_unit.py       b312758563092b134eedc085f3e3a2d11c3d1395
A/owner_custody.py           f2ada98b684030eeb356d24851e80f1ae0008845
A/test_a_final_custody_unit.py 010c8af99e786e769618cc6d50590d7f06767987
```

```sh
python -B -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-D03-E01-1010-AGENT-B-R1/test_b_guard_unit.py \
  WORKER_RETURNS/SOROK-D03-E01-1010-AGENT-A-R1/test_a_final_custody_unit.py
```

Observed local reproduction: **12 passed, 0.14 s** (Python/pytest local environment). Exact original B test control passed again.

Differential test `test_b_provider_head_only_check_misses_the_reserved_p3_op_differential`: B-style head-only guard accepts a provider response with pending `PREPARED` operation and unchanged head/state. The A owner lease then refuses the same state before the mock original P2 writer receives any event. The real P3 code independently demonstrates the existence/semantics of this head-invisible state. Other directly executed negatives: source mutation, expected-state drift, reservation inserted between events, real-thread competition across the owner-lock boundary, and unauthorized direct writer bypass (correctly rejected only after the real write, proving *no* rollback/atomicity claim).

**No full native J1/P2/P3 runtime test was executed.** The new A fixture tests are **AUTHORED_NOT_RUN**: pending inserted inside the provider; pending inserted between B guard and first writer; real `P2Owner.realize` witness under P3 `_root_lock`. The pre-existing 10 J1 tests, 6 A full-fixture tests, and 2 B full-fixture tests are also NOT_RUN here.

To run actual first consumers from the original exact checkout and final A branch:
```sh
python -m py_compile WORKER_RETURNS/SOROK-D03-E01-1010-AGENT-A-R1/d03_e01_performer.py \
  WORKER_RETURNS/SOROK-D03-E01-1010-AGENT-A-R1/owner_custody.py \
  WORKER_RETURNS/SOROK-D03-E01-1010-AGENT-A-R1/test_a_final_hostile.py
python -B -m pytest -q -x -p no:cacheprovider --tb=short \
  WORKER_RETURNS/SOROK-E01-J1-995-R1/test_j1_three_head_join.py \
  WORKER_RETURNS/SOROK-D03-E01-1010-AGENT-A-R1/test_d03_e01_performer.py \
  WORKER_RETURNS/SOROK-D03-E01-1010-AGENT-B-R1/test_b_guard_unit.py \
  WORKER_RETURNS/SOROK-D03-E01-1010-AGENT-B-R1/test_b_hostile.py \
  WORKER_RETURNS/SOROK-D03-E01-1010-AGENT-A-R1/test_a_final_custody_unit.py \
  WORKER_RETURNS/SOROK-D03-E01-1010-AGENT-A-R1/test_a_final_hostile.py
```

GitHub Actions diagnostic #43508991500 (in original A return) failed before allocation in both attempts; zero steps, no logs. This is not a test outcome. No new full-repo CI run is misrepresented as green.

## 5 — What remains honestly held and why

- **G2 historical Nadia activity:** the `ExactActorProvider` produces fixed `EventProposal` documents before reading Nadia's organization. P2 `_realize` uses `session.admit_event(case=self.case, source=self.source, ...)`; the selected act is not established as a result of D03 plural P3 history. A qualified native or sourcefree activity-selection rule/first owner is still unavailable in this scope. NO new dominant-motive selector, grammar, hidden action table, or actor-authority issuance.
- **D04/D05:** `P3Owner` requires prebound original P3 plan/proposal hashes and test-only rules. This adapter cannot simply mint them. The original separate distinct later *performed* consumer through P3/P4/P6 is still unproved. Durable Rule A/T, memory formation, no-change and formation remain `MISSING_RULE`.
- **Inaction:** no qualified inaction evaluator is introduced; do NOT relabel an absent performer as evaluated NO_CHANGE.
- **Atomicity:** the lock blocks **cooperating P3Owner writers** while the original P2Owner commits each event. Direct PsycheStore writers bypassing the root lock, file hot patches between closure checks, and new native owner/origin coupling are not prevented atomically. A test proves a bypass can mutate head after a P2 write despite the guard; no false rollback claim.
- **Resources:** local test elapsed only; no full scenario throughput, RSS, model cost or CI statistics established.
- **No mandatory per-event P3 acquisition:** P3 record head must be preserved during this bounded P2-only route; future competent P3 owner must supply an explicit approved plan before claiming real P3 changes.

## 6 — G1–G5 and strongest successor attacks

| Court | Scoped disposition |
|---|---|
| G1 | Original source/owner chain reconstructed; full integrated S2 NOT_RUN |
| G2 | HOLD: no source-qualified historically conditioned Nadia choice/performance, although P2 owner route authored |
| G3 | 12/12 exact-file local unit PASS; full J1/actor hostile and code-hot-patch negatives NOT_RUN |
| G4 | Event-by-event P3→P2 lease, source closure and pending guard built; native world cold/retry NOT_RUN |
| G5 | Independent receiving NOT_PERFORMED; no self-acceptance |

**Engineering:** bounded owner-custody repair, observed isolated proof only, full execution remains held.  
**Scientific:** CAN/ADP/P3 Rule A/T and other-native actor science not issued, sourcefree only.  
**Authority:** no protected merge, user-only Browser relay, no Codex supervision or #939 fleet restart.

Most valuable next attack: independently run native J1/P2/P3 and inject a real P3 pending reservation rather than a mocked `pending()`, verify no effects are admitted while preserving existing P2 recovery; then find or prove absent a truly source-qualified actor-conditioned performer and distinct later ordinary consumer. Also probe direct-store bypass, multiprocess lock custody, exact code-source closure and performance cost. Accept any demonstrated stronger implementation; no separate chooser or fictional psychological machinery.

**Agent A final counter STOP. Hand back for the required independent G5 when executable native evidence exists.**
