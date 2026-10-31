# SOROK B-F1CR-R2 — live independent B history and targetless C10 recurrence

**Status: `ENGINEERING_ACCEPT_SCOPED__LIVE_B_AND_TARGETLESS_C10_CONSUMER__SCIENCE_AUTHORITY_HOLD`.**

PRE-MAIN reference at launch was `750548ddbb9b4392a16ce93097b856f349e16182`. At return the remote PRE-MAIN head is `5ad805e52a4fd0dbaae3a6b91801164e74ebc6f3` (docs/CI-only #545); this worker branch remains based on the authorized `750548dd` start and was not rebased or merged. The R5 source correction is preserved: exact original F1C is recovered; the claimed F1CR patched executable remains `SOURCE_NOT_FOUND`; R5's `f1c_reconstructed_candidate.py` is used only as an explicitly labeled reconstruction. No PRE-MAIN, original branch, native source or actor authority was modified.

## FINDING

1. **R5 replay.** Exact original F1C `7e3492a2…` and R5 reconstructed candidate `12f183a3…` were replayed against the frozen `test_full_history_binding.py` `271e6aa1…`.
   - Original: 13/13 cases exit 0; three live-history mutations fail as historical evidence.
   - Reconstructed: 13/13 cases exit 0; **3/3 live-history mutations pass** with `LIVE_A_HISTORY_CHANGED`, `LIVE_B_HISTORY_CHANGED`, `LIVE_SHARED_HISTORY_CHANGED`.
   - The local reconstructed 13-case result hash is `87fa57f6…`; the original is `830b2dc9…`. R5's historical hashes differ (`4de846b2…` / `5c3b91dd…`) because this replay used the reconstructed runtime; case set and expected/observed outcomes are preserved.
2. **Targetless C10 consumer.** A new sourcefree adapter consumes R5's `freeze`/`intervene` B history/material-action record and emits an exact `TargetlessC10Ledger` with distinct states:
   - `TARGETLESS_REFUSE` — performed B refusal, targetless, durable non-action history;
   - `TARGETLESS_SILENCE` — non-event condition, `performer=None`;
   - `TARGETLESS_NO_PROPOSAL` — no proposal;
   - `HELD_MISSING_RULE` — no competent evaluation receipt;
   - `TARGETLESS_UNOBSERVED` — B action exists but A does not observe it;
   - `EVALUATED_NO_CHANGE` — actually evaluated NO_CHANGE with a competent receipt;
   - `SHARE_OBSERVED` / `SHARE_UNOBSERVED` for the access contrast.
   No state fabricates a C9 proposal, C9 target, performed E2, learned practice or utterance; targetless states advance time and retain durable history.
3. **Actual first consumer.** `TargetlessGuardedJoinedProduct` subclasses the existing I1 `GuardedJoinedProduct` and consumes the targetless ledger under the same product root/store/branch. It is not a second actor store and not a disconnected `RefusalSession`. The I1 A0–A3 public/other state and B owner material readout are read after consumption.
4. **Access contrast.** Observed SHARE gives A a readable `B_SHARED_TOOL` event and tool access; unobserved SHARE gives tool access but no readable B event. Observed REFUSE gives a readable `B_REFUSED_TOOL` event; unobserved REFUSE gives neither event nor tool. SILENCE gives neither.
5. **Material ledger.** I1's inherited offscreen market work still reports `material_delta=-1` while stock is 0. The adapter refuses the unexplained clamp:
   - no prior stock and no replenishment -> `MATERIAL_EXHAUSTED`;
   - source-visible test-only replenishment of 1 at tick 39, then one unit consumed at tick 40 -> `1 -> 0`, `clamped=False`;
   - explicit material-work refusal preserves stock and records `MATERIAL_WORK_REFUSED`;
   - non-stock tool action records zero material consumption.
   The I1 event is preserved as historical fact; the continuity ledger supplies the missing prior-stock receipt instead of silently accepting the clamp.
6. **Cold replay.** The targetless ledger and A memory replay identically in two fresh Python processes; the I1 product reopens the durable targetless history under the same root and returns the same states/hashes and `c12_ok=True`.
7. **Negatives.** All required same-consumer negatives refuse: severed B live prehistory; forged shared digest; absent B tool/time; REFUSE without a performed event; NO_CHANGE without a competent receipt; unobserved event in A memory. Restoring the original preimages reproduces the intended state.

## EXECUTED EVIDENCE

- R5 reconstructed live-history court: **3 passed**.
- R5 original live-history court: **3 failed** (preserved historical RED).
- R5 original/reconstructed 13 outcomes: **13 exit 0 each**.
- New targetless C10 court: **14 passed**.
- I1 guarded baseline: **8 passed**.
- I1 same-person targetless integration: **5 passed**.
- Two-process cold replay: equal outputs; ledger hash stable.

Exact commands, paths, hashes and the material ledger receipts are in `02_EXECUTED_POSITIVES_NEGATIVES_MATERIAL_LEDGER.md` and `04_COLD_REPLAY_AND_ROLLBACK.json`.

## INTERPRETATION

The targetless states are now causally meaningful in a continuing-person chronology: REFUSE and SILENCE are distinct, an unobserved B action is not inserted into A's memory, and no targetless state is promoted to C9/E2/practice. The material ledger is coherent by an explicit prior-stock receipt or refusal, not by negative-and-clamp.

## ACTION / OWNER

- **Original F1C/F1CR author and R31J/C8 owner:** review the reconstructed candidate; the claimed patched bytes remain `SOURCE_NOT_FOUND` and must not be relabeled.
- **I1/CP-A5 owner:** review the `TargetlessGuardedJoinedProduct` extension and the targetless C10 receipt semantics; no adoption is claimed.
- **C9/C10/C12 owners:** decide whether the targetless continuity receipt is a lawful C10 read adjunct or remains a distinct TEST_ONLY ledger. No C9 proposal or target was invented.
- **Incumbent HQ and a distinct reviewer:** intake and independently review. No self-adoption.

## THREE COURTS

- **ENGINEERING:** `ACCEPT_SCOPED` — exact R5 replay, distinct targetless states, same-I1-person consumption, material ledger, access contrast, cold replay and all required negatives pass at the sourcefree TEST_ONLY grade.
- **SCIENCE:** `HOLD` — no native B, original actor/world, Rule A/T, acquired practice, performed E2 or A0–A5 human continuity is proved. The reconstructed candidate is not the missing F1CR source.
- **AUTHORITY:** `HOLD` — no CAN/ADP/SCI05/Pyat/C11/C12 issuance, C9/C10 owner adoption, PRE-MAIN merge or self-review. M35/S35 and original grants remain separate.

## DONE / REMAINING / BLOCKERS / LARGEST MOVE / FLIGHT / DELTA

- **DONE:** R5 original/reconstructed live-history replay; 3/3 mutation repair; targetless C10 state machine; I1 same-person consumer; material ledger reconciliation; observed/unobserved access; cold replay; all seven negatives.
- **REMAINING:** owner review of F1CR reconstruction; I1/C9/C10 owner disposition of the targetless receipt; native/scientific grants; independent reviewer.
- **BLOCKERS:** F1CR patched bytes `SOURCE_NOT_FOUND`; no native B/world/C9/C10 authority; C12 anchor absent; targetless C10 remains a sourcefree adjunct, not canonical C10.
- **LARGEST MOVE:** original F1C/I1/C10 owners accept or reject the exact targetless receipt contract and the reconstructed live-history candidate.
- **FLIGHT:** sourcefree local Git/Python; no active worker, PRE-MAIN, prior branch, native source or PR #514/#516 disturbed.
- **DELTA:** live B history is replayed and guarded; targetless REFUSE/SILENCE/NO_PROPOSAL/HELD/UNOBSERVED/NO_CHANGE are distinguished; the same I1 person consumes the targetless history; material `-1`/0 is reconciled by prior stock or refusal, not clamp.

## LIMITS

- Local model is `opencode-go/deepseek-v4.1-flash`; MAX reasoning effort is not independently observable.
- The sourcefree reconstructed candidate is not the missing F1CR patched executable.
- The targetless C10 ledger is an adjunct; it does not create a C9 target, C9 proposal, E2, practice or native C10 authority.
- No original survey/respondent corpus, native source, CAN/ADP/Pyat issuance or PRE-MAIN mutation occurred.
