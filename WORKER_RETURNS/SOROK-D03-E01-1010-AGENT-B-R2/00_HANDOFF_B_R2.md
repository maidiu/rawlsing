# SOROK #1010 — Agent B optional exact-defect last counter / source-contract challenge

**Disposition:** `B_R2_EARLY_QUIESCENCE_REPAIR_COMMITTED__FULL_NATIVE_NOT_RUN__ACTUAL_ALTERNATIVE_EVENT_SELECTION_HELD__STOP_DUEL`.
**Governing:** #1010 original A→B→A finite duel, original D02/D03/E01 task packets at `227ce149fc7864c83c179a7d3ecaef2b92c5bdab`, adopted MCR-lite, original SOROK/UM R1. This is the **single optional bounded source defect turn after A's final counter**, not another review fleet or purported G5.

## 1. Immutable source reconstruction and lineage

- Frozen join ancestor PR #996 `fb061dec16c8386b9caa1b5ea75ec7645aff88a7`.
- A first PR #1016 `6248547b2ad98002245b69cec9e399277d090f12`.
- B first PR #1019 `6bfdc3b91b1c77577fdf5545e16ed866016213d4`.
- A final PR #1022 `9e8b219bb1136a2c6fbe33e4903e850d7816b62a` **exact parent of this B R2 branch**.
- This branch `agent/sorok-d03-e01-1010-b-last-counter-r2`; final immutable commit is the revision with this handoff (verify ref).
- Protected PRE-MAIN remained `6a5c12f04323d74001f9632063ec907f4fc4468e` at receipt, untouched.
- Scope change: one bounded insertion into A final `WORKER_RETURNS/SOROK-D03-E01-1010-AGENT-A-R1/d03_e01_performer.py`; one new full-fixture hostile test `WORKER_RETURNS/SOROK-D03-E01-1010-AGENT-B-R2/test_b_final_preflight.py`; this source-grounded handoff and self-attack. **No changes to** P2Owner, P3Owner, J1, B04/B05, parent C03/C04, CG-A or protected code.

### Exact governing obligations

Original D02 terminal consumer is a later actual P3 proposal/actor decision (not merely a readset). D03 requires immediate actor response on source-qualified historical organization, no forced durable memory. E01 requires Nadia's actual response and *subsequent admitted event* under the mother-material-speech-child causal join. #1010 G2 additionally requires plausible alternative activity, qualified actual event or genuinely evaluated inaction, and real later consumer. The sourcefree interface remains narrower than native psychological science; no new issuer or actor rights are invented.

## 2. A counter accepted: these were genuine fixes

- A correctly proved that `PsycheStore.pending()` can report `PREPARED` or other unresolved P3 reservations without changing `head()`. My B pre-provider head-only guard missed that state.
- A's per-event `P3CoordinatedP2Owner` uses P3 `_root_lock` then original P2 `realize`, preserving the original cooperating P3→P2 lock order, and checks pending/head/source and owner identity before/after each write. It delegates original source-owned event effects without inventing P3 psychological results.
- A preserved B's post-provider `GuardedProvider`, original negatives and explicit G2 HOLD. The isolated 12 PASS claim in A's handoff pertains only to dependency-free tests; it is not native execution. **No refutation of these actual strengths**.
- A correctly documented that per-event locks do not create a cross-owner P3/P2 transaction and cannot roll back illicit direct-writer modifications.

## 3. New B exact defect (repaired)

**B2-01: Already-disqualified P3 state was discovered only *after* an external provider call and persisted cycle reservation.** A checked P3 pending after `provider.call` (and at P2 write), but did **not** check before constructing `BatchEngine` or invoking `RecursionCycle.bootstrap`. If a P3 operation was already pending on entry, the downstream write was necessarily refused, yet the system needlessly made the provider call and left a durable `HELD` / `AMBIGUOUS_PROVIDER_CALL` cycle with zero chance of an admissible batch in that attempt. This is a real source-order and resource/custody flaw even though it does not cause a false P2 write.

**Fix:** reuse A's **existing** `precommit_custody()` immediately before creation of `P3CoordinatedP2Owner`, `BatchEngine`, `RecursionCycle` or provider invocation. This checks the exact previously required pending/head/identity/source closures without duplicating logic, and fails fast with `E01_POSTPROVIDER_P3_PENDING_OPERATION` (legacy code reused; its name is now somewhat misleading for pre-call use). This preserves all later post-provider and per-event checks as defense in depth. No new state owner or rule.

**Negative test AUTHORED_NOT_RUN:** `test_b_final_preflight.py` uses the inherited actual `open_j1_case`, monkeypatches only `owner.store.pending` to a preexisting `PREPARED` reservation, and requires: `RecursionRefusal`, zero provider calls, unchanged world event list/P3 head, no new cycle file or batch journal. This is distinct from A's post-provider pending injection and B's post-provider stale-head cases. A's six inherited positive/negative fixture tests must be rerun to prove no regression.

## 4. Deeper finding neither previous version solved

**B2-02: The chosen '3–5 prospectives' execution interface is not the original product's prospective alternative event/outcome computation.**

Exact original implementation sources in PR #1022:
- `developmental_recursion/model_cycle.py`, blob `231cab97b4bc5e2f40de3c45d179a68ba58585c5`: `RecursionCycle._parse_proposals` requires 3–5 event documents and returns ALL as `EventProposal` list; `_run_batch` forwards the whole list to engine.
- `developmental_recursion/engine.py`, blob `a777692782003e05de6c46280b5861e97516dc90`: `BatchEngine.run_batch` iterates over `range(start_index, len(proposals))` and invokes `owner.realize` for each.
- `developmental_recursion/p2_owner.py`, blob `a6b289558898d16a58056df36dd647a0a28ec547`: `P2Owner._realize` calls `session.admit_event(case=self.case, source=self.source, history_event_refs=..., event_time=...)` rather than computing Nadia's contingent activity from multiple P3 organizations.
- Original #1010 requires qualified prospective **alternatives**, source-conditioned activity or evaluated inaction; original E01 terminal positive is an actual Nadia response and subsequent admitted event. D02 terminal consumer is an actual actor proposal/decision.

Both A and B correctly defended the **existing ABI** as an ordered batch of 3–5 events, not a menu of competing motive labels. **But that is precisely why simply retaining the batch ABI does not satisfy #1010's terminal requirement.** Realizing all scripted events is not selecting/evaluating one activity under historically constituted competing possibilities; absence of an event writer is not evaluated inaction. This is a shared semantic abstraction mismatch, not a newly proven generic bug in `RecursionCycle` itself.

**No authorized repair in this source domain:** Do NOT misuse `eligible_modes` as top-1 action, secretly choose among the 3–5 existing ordered batch events, invent a psychological chooser or modify read-only CAN/V3/P2 scientific owners. Recover the actual competent original alternative/event-outcome computation and its writer from source, verify if it can consume multi-stream actor readsets and drive one admitted event/qualified no-action; otherwise precisely issue the owner/ABI HOLD. The current adapter remains useful only for its narrower P2 sourcefree world-writer demonstration.

## 5. Executed and unexecuted proof

- I independently inspected source-immutable #1022 code plus P3 `pending`, P3 `realize`, P2 `validate_proposal`/`_realize`, `RecursionCycle._parse_proposals`/`_run_batch`, `BatchEngine.run_batch`, original 27 task packet entries and #1010 requirements.
- Independently ran a POSIX `fcntl.flock` lock check on this local Linux environment using separately opened descriptors, same process/two threads: competing thread remained blocked while first lock held, acquired only after release. This verifies one OS lock property, **not** the live A P3/P2 owner integration.
- **New B R2 native/full J1 tests: NOT_RUN.** The GitHub connector supplied individual files and diffs but no locally executable full private checkout/dependencies. The one-line repair is source-published, not demonstrated by actual full native fixture. I do not inherit A's 12 unit passes as my own executed tests.
- The `test_b_final_preflight` is newly AUTHORED_NOT_RUN. Exact runner command:
```sh
python -B -m pytest -q -x -p no:cacheprovider --tb=short \
 WORKER_RETURNS/SOROK-E01-J1-995-R1/test_j1_three_head_join.py \
 WORKER_RETURNS/SOROK-D03-E01-1010-AGENT-A-R1/test_d03_e01_performer.py \
 WORKER_RETURNS/SOROK-D03-E01-1010-AGENT-B-R1/test_b_guard_unit.py \
 WORKER_RETURNS/SOROK-D03-E01-1010-AGENT-B-R1/test_b_hostile.py \
 WORKER_RETURNS/SOROK-D03-E01-1010-AGENT-A-R1/test_a_final_custody_unit.py \
 WORKER_RETURNS/SOROK-D03-E01-1010-AGENT-A-R1/test_a_final_hostile.py \
 WORKER_RETURNS/SOROK-D03-E01-1010-AGENT-B-R2/test_b_final_preflight.py
```
- If a true native checkout is unavailable, do not pretend this is G2, G4, G5 or RED→GREEN evidence.

## 6. Self-attack, authority and stop

- The inserted pre-call barrier adds one extra potentially expensive source-closure scan but saves an external provider invocation and durable hold on already-invalid pending P3. It is not atomic against a pending reservation inserted after the preflight. A's post-provider and per-event safeguards remain responsible for that case.
- The new negative injects `pending` via monkeypatch rather than a real P3 reservation; it must be followed by native reservation/recovery execution before a broad G4 claim.
- The source of **the greater G2 mismatch** is an incorrect assumption about what the existing batch orchestration proves; no alteration to `RecursionCycle` or P2 owner was warranted under current custody. Do not count this as a fixed functional G2.
- A's prior isolated tests remain code-intact; no native integration claim, D04/D05 Rule A/T, memory, NO_CHANGE, rights promotion or protected merge.
- **G1:** exact source and contract independently read; integrated NOT_RUN.
- **G2:** `HOLD` — actual multi-stream prospectives, contingent Nadia act or evaluated no-action and independent performed consumer missing.
- **G3:** new negative authored; NOT_RUN. A's claimed 12 isolated PASS is inherited testimony; not independently replayed this turn.
- **G4:** no new event storage changes; full native cold/retry NOT_RUN.
- **G5:** NOT_PERFORMED. Independent receiving only once a bounded substantive sourcefree claim is actually executed and source-exact.
- **Engineering:** one upstream fail-fast correctness/cost improvement committed; no native evidence. **Scientific/authority:** original boundaries intact. **STOP** after this optional exchange.

## 7. Fresh counterchallenge / handoff to substantive owner (not a new duel)

Prove from original source the competent *prospective possibility/outcome* mechanism distinct from `RecursionCycle`'s ordered-to-realize batch and demonstrate **one** source-qualified Nadia activity (or genuinely computed inaction), plural pressure, a source-owned admitted effect, distinct later reader, altered-history negative and cold restoration. If no existing lawfully usable owner exists at #1010's granted source cut, return the precise missing function/ABI and the minimum necessary owner authorization, not another 3–5 event scripting demonstration.

The finite A→B→A + one defect-specific B exchange is saturated. **Do not commission another review of this custody layer or self-certify G5.**
