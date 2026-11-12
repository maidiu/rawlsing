# SOROK C03/C04 AGENT A RELAY — parent action, lock composition, and Nadia's actual experience

**Role:** Pair3 Agent A relay, permanent session `ses_e31295836ffeW9bYwX9iiMMcXS`; only opponent SAME Pair3 B `ses_e31295826ffe6kteacpU7p3nQW`.
**Branch:** `codex/sorok-duel-c03-c04-a-consumer-20261112-r1`.
**Implementation SHA:** `61f2918ec947e44dd7ecff8fd3359734469e9a90`.
**Frozen start:** `01b2d2d23259969778ce996f5527037d666f46f8` (B `1510d835fcf0a35a5b352b27f4daf4b1f0bb6b34` + Pair1 `15472ca725e03be1c87faef8c30511edcdf10111`).
**B implementation:** `255fd4905990e3c0cab3e2d95ba91b851ea701a8`.
**Contract:** `08a323b490df4e2ddd0dca7f8b3cd394dfe17e0a`; protected baseline `6a5c12f04323d74001f9632063ec907f4fc4468e`.
**Grade:** `SOURCEFREE_S2_ONLY`; no native/science/rights/actor/human/protected authority.

## 1. B's return received — genuine strengths conceded

B's C02/C03/C04 construction is real and is preserved:

- **Actual incremental B02 owner.** B replaced A's manual anchor/ticks inference with `historical_period.period_progress` + `read_material_period` and proved two chronological parent periods, the B02 employment change, parent work/care/debt changes, cold reopen and source severance. A's former `PARENT_B02_FULL_PROOF_HOLD` assertions are stale; A updated them to `B02_INCREMENTAL_PERIOD_API_QUALIFIED`. B's two-period/source-severance evidence is accepted.
- **Typed B04 purchase history.** B's `P2_PARENT_PURCHASE` acceptance, before/after source chain, purchase/ownership/currency provenance and narrow schema checks are correct. A preserves and strengthens this.
- **C03 separation.** B's explicit sourcefree decision rule, C12 decision episode, separate perform/action receipt, valid-empty decline/hold, replay and stale-decision refusal are correct. Caller request remains input; no Nadia/child outcome is read.
- **C04 writer separation.** B commits an actual `SPEECH` event, parent `own_speech`, child `speech` only under bounded same-room registration, and hidden reason in a self-only C12 episode. No child co-presence inference; no hidden reason in the event. A preserves this.
- **A's live P4/P6 boundary entry.** B correctly preserved A's `run_p4.run_parent_operation`/`run_p6.parent_background_operation` entry and recorded that ordinary P6 view/say survive after parent work. B's composition start exposed the actual next gaps.

I found **no surviving false accusation** in B's C02/C03/C04 return. The genuine remaining conflict is B04's currency writer, which B itself identified and did not hide.

## 2. My own mistakes / stale claims, conceded

- My prior B02 current-period implementation manually derived the date from anchor/ticks and advertised `HELD_INCREMENTAL_CURRENT_PERIOD_API_MISSING`. B proved the actual incremental API exists. I removed the stale assertions and now consume B's `period_progress`/`read_material_period` context; B's two-period proof is accepted.
- My first C03 perform composition held `_parent_write_lock` and called B04's public locked purchase wrapper, which reacquires `_purchase_lock` then `_parent_write_lock`. A bounded 120 s subprocess probe **timed out**. I repaired the lock order.
- My first child-experience draft exposed the parent decision action in the child response input. That was a real hidden-state leak. I removed it; the child now sees only the public utterance and `decision_state=NOT_READ`.
- My first child-experience read did not independently require the parent `own_speech` receipt; I added that check and a negative test.
- My earlier C02 B02/impact documents still contain the old hold wording. They now carry a superseding note pointing to this return and B's incremental evidence.

## 3. Repairs implemented

### A. Parent/B04 lock composition — real deadlock repaired

At frozen start:

```text
perform_parent_decision
  holds parent_activity._parent_write_lock
  -> B04.purchase_drum_kit
       -> material_operations._purchase_lock
       -> parent_activity._parent_write_lock   # deadlock
```

Bounded probe: 120 s timeout. Repair:

```text
perform_parent_decision
  -> require B04 _purchase_lock + _purchase_drum_kit
  -> with _purchase_lock:
       with _parent_write_lock:
           _perform_parent_decision_locked
             -> revalidate admitted decision source
             -> b04._purchase_drum_kit (actual unlocked writer)
             -> write C12 action receipt
```

This matches B04's public lock order, keeps decision revalidation and the actual purchase in one composition, and creates no no-lock adapter, monkeypatch, second scheduler or lock framework. Missing private hook refuses `PARENT_DECISION_B04_UNLOCKED_WRITER_UNAVAILABLE`; the exact required future hook is in `A_RETURN_R3/LOCK_AND_PURCHASE_ABI.md`.

### B. Typed purchase consumption and suspended bridge

`parent_activity` now consumes the exact B04 `P2_PARENT_PURCHASE` receipt without depending on the post-purchase `P2_PARENT_MATERIAL_ANTECEDENT` bridge:

- strict schema/root/branch/parent/alias/status/before-after checks;
- purchase source recomputation, market/owned before-after, object/kind/owner/price/currency/possession/event-clock provenance;
- exact source-chain continuity;
- exact duplicate bridge is ignored as **not history**; a bridge without an exact admitted purchase refuses `PARENT_MATERIAL_BRIDGE_NOT_ADOPTED`;
- `read_parent_history` returns the typed purchase row with object/owner/currency/unit-price/market/owned/purchase provenance and `purchase_episode_count`; the bridge is not a second history row.

The bridge remains Pair1-owned and is not adopted semantically. Removing it later changes no reader result.

### C. Actual Nadia/P6 current-experience consumer

New normal P6 entry:

```text
run_p6.experience(state, command="child-experience",
                  event_id=<id> OR operation_id=<utterance op>)
run_p6.child_speech_experience(session, ...)   # public internal seam
parent_speech.read_child_experience(...)
```

It uses the existing `situated.recent_speech` P6 actor-perception path plus the actual C12 child speech receipt. It verifies:

- focal child actor/alias and utterance root/branch;
- actual SPEECH event ID/hash/author/kind/occurrence clock/text;
- recomputed utterance source identity;
- parent `own_speech` receipt;
- child `speech` receipt channel/clock via `read_child_uptake`;
- the event is actually present in Nadia's P6 actor current-experience list, matching text/speaker/clock;
- admitted parent decision episode identity and action, without exposing its basis.

It returns only public speech and a bounded `SOROK_CHILD_SPEECH_RESPONSE_INPUT@1`:

```text
access_condition = SAME_ROOM_AT_ADMISSION
access_owner = C12_SPEECH_PERCEPTION_RECEIPT
text_source = CALLER_SUPPLIED_NOT_GENERATED
language_generation_owner = NOT_IMPLEMENTED
hidden_reason = NOT_READ
decision_state = NOT_READ
custody = C12_SPEECH_RECEIPT_NOT_MEMORY
durable_acquisition = MISSING_RULE
user_view = NOT_EXPOSED
```

Remote/no-child-receipt returns `NOT_PERCEIVED` with no text. Missing parent `own_speech` or child speech receipt refuses. Severing the event removes child uptake while the prior decision remains. Same outward text with two hidden reasons yields the same public child input; parent self-reads still differ. Ordinary P6 user view/say do not expose the parent utterance.

### D. C03 truthful inputs

The decision/action receipts now explicitly disclose:

```text
request_source = CALLER_SUPPLIED_OBJECTIVE_REQUEST
decision_evidence = EXPLICIT_SOURCEFREE_RULE_NOT_NATIVE
physical_admission = NOT_YET_PERFORMED | PERFORMED | VALID_EMPTY | HELD
language_generation_owner = C04_CALLER_SUPPLIED_TEXT
native_science = false
```

The parent decision remains material/factual, not an LLM sentence; text and hidden reason remain explicit caller inputs, not a generated mother-speech capability.

## 4. Evidence

Commands used the qualified venv and bounded pytest runs; logs are under `A_RETURN_R3/evidence/`.

| Check | Result | Evidence |
|---|---|---|
| B C02/C03/C04 packet suite (two periods, decision/action/speech) | **11 passed** in 261.31 s | `b_c02_c03_c04.log` |
| A C03/C04 consumer suite (normal P6, remote/severed, currency) | **3 passed** in 70.05 s | `a_c03_c04_consumer.log` |
| A C02 parent + live/B02 tests (stale hold assertions repaired) | **9 passed** in 112.51 s | `a_c02_regression.log` |
| C01 B/A + P2 + P3 owner | **28 passed, 1 skipped** in 88.51 s | `c01_p2_p3.log` |
| B01 + B03 current cut | **15 passed** in 108.60 s | `b01_b03.log` |
| B02 current cut | **7 passed** in 54.59 s | `b02_period.log` |
| P4 response/speech + P5 gaze/experience | **7 passed** in 86.45 s | `p4_p5.log` |
| B04 + B05 current cut | **3 failed, 1 passed** at real parent-currency mismatch | `b04_b05_currency.log` |

The pre-repair lock probe timed out at 120 s; after repair the B perform test and A parent-perform live test complete.

## 5. Requirements still unfulfilled

- **B04 currency writer** (Pair1): require parent/request/market currency equality before any debit/stock/ownership; durable `CURRENCY_MISMATCH` refusal with before == after/no possession; receipt currency fields; remove equivalence declaration; `read_purchase` validation; matching fixtures. B04/B05 default tests still fail at this real boundary. C03 refuses mismatch before B04 and passes with same-unit fixtures.
- **B05 rent/household budget**: separate from parent cash; no shared budget/conversion/double count yet.
- **Full P3 `BatchEngine` 3–5 event interleave** across B02 periods and C03/C04 consumer: not proved; P3/context owner remains Pair2/shared.
- **Language-generation owner**: text/hidden reason are caller inputs. A competent parent decision/expression generator remains an explicit seam; no LLM sentence is counted as performed.
- **Durable psychological uptake/native CAN rule**: C04 provides a response input, not memory/acquisition/science.
- **E03** crash/SIGKILL composite purchase/action/utterance; forks/cold parent lineage; MI/P5/P6 exposure; full estate. Not claimed.
- P3 source closure does not pin the parent modules; no P3 edit/weakening.

## 6. Exact artifact / changed files

Changed this turn:

```text
WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1/developmental_recursion/parent_activity.py
WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1/developmental_recursion/parent_decision.py
WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1/developmental_recursion/parent_speech.py
WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/run_p6.py
WORKER_RETURNS/SOROK-DUEL-C02-C03-R2/A_RETURN_R3/*
WORKER_RETURNS/SOROK-DUEL-C02-R1/A_RETURN_R2/test_c02_live_root_b02.py (stale B02 assertions repaired)
```

No edit was made to B04/B05/material/house/P2 material functions, P3/owner/store/projection/model_cycle/context, Pair2 files, guides/current-progress/workflows/Pyat/config/server/credentials/remote/protected files.

Return artifacts: `A_RETURN_R3/00_RETURN.md`, `C03_C04_A_ABI.md`, `LOCK_AND_PURCHASE_ABI.md`, three `PROGRAMMA_DELTA_*.json` files, `impact.json`, `evidence/*.log`.

## 7. Strongest remaining attack surfaces for SAME B

1. Apply the B04 currency ABI and make B04/B05 default tests green with matching fixtures; prove a mismatched purchase refuses before debit and C02 history shows the durable refusal.
2. Run a full P3 `BatchEngine` 3–5 event cycle across B02 periods with one parent decision/action/speech and Nadia's actual response input, cold replay, one purchase/one rent/one ownership row.
3. Attack the P6 child consumer: forge event author/hash/source, parent own_speech, child channel/clock, decision binding, severed event, hidden reason, user surface.
4. Reconcile B05 rent, B01 household cash, B04 purchase, parent cash/debt and C03 decision without conversion/double count.
5. Prove E03 SIGKILL recovery across purchase→action→speech; forks/cold lineage.
6. Replace caller-supplied speech with a competent parent expression owner if one exists, without pretending an LLM sentence is an action or native psychology.

**Hardest concrete challenge for SAME B:** make the B04/B05 currency/budget path and the full P3 batch consume one actual parent decision/action/utterance across two B02 periods, with a real Nadia response input, cold/crash recovery, one debit/ownership/rent receipt and no hidden-reason or user-view leak. A reader-only or static-fixture improvement will not surpass this cut.

## 8. Measured cost and limits

Test wall times above. Controller/provider token, latency, process RSS and retry cost are `UNKNOWN`; no instrumentation was available or invented. The two full Library architecture records remain NOT_INSPECTED locally; no contents are claimed. This is sourcefree engineering, not native actor science, source/use rights, human validation, independent acceptance or protected adoption.
