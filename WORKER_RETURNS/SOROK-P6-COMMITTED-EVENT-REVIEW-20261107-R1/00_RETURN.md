# SOROK P6 committed-event closure — independent review

**Candidate:** `4f3f465923a61e9e3d76b9c0aa7f6ffd8ecad318`
**Prior REVISE:** `9a8a01ac99d006772049689858c4cd50a3035f9f`
**Prior candidate:** `803a4a52e84d6d90df740785b8fd077a581d0a18`
**Scope:** exact prior P6 recognition provenance REVISE only; no runtime/PR779 edits, no arbitrary store hardening, no source/human/native/Pyat/protected work. The separate joined-encounter worker was not touched.
**VERDICT: PASS_SCOPED** — fabricated ledger event, cross-target event, forged gaze, and turn ordinal are closed against committed owner events.

## Findings

| Prior defect | Result | Evidence |
|---|---|---|
| Fabricated P4 ledger event accepted | **PASS** | Ledger `performed`/`public.observation` rewritten to `FAKE-LEDGER-EVENT`; cold CLI `recognition={}`, `recognized_identity=None`. |
| Cross-target actual event accepted | **PASS** | Sandals turn rewritten to the real photo event ID; cold CLI `recognition={}`, `recognized_identity=None`. |
| Genuine inspect turn ordinal | **PASS** | Genuine `look sandals` reports `turn: 2`, matching the actual P4 ledger turn ordinal; not `len(recognized)+1`. |
| Forged gaze cache | **PASS** | Tampered `p6_gaze.json` `recognized` is ignored; cold view rederives the genuine committed event/marking only. |
| Source of truth | **PASS** | `derive_recognition` uses `session.events()` and `session.user_perceived_ids()`; requires committed `INSPECT`, actor `U`, matching body target, and user-visible event ID. Ledger summary/public observation are not authority. |
| Genuine earned control | **PASS** | `look sandals` emits `the repaired blue-thread sandals`, marking `blue-thread-left-strap`, event `TEST_ONLY_BP4_WORLD_EVT_5e8807be…`, turn `2`. |
| Plain category/unrelated look | **PASS** | `new` exposes `bench/mug`; pre-recognition `view` has no identity; `look photo` has no recognized identity. |
| Actor input boundary | **PASS by code inspection** | No actor/Nadia input was added; only existing committed owner events and user-perceived IDs are consulted. |

## Actual CLI probe (disposable state)

```text
genuine look sandals:
  admission=ADMITTED
  recognized_identity=the repaired blue-thread sandals
  recognition.sandals.event_id=TEST_ONLY_BP4_WORLD_EVT_5e8807be9d3ca1d045bbe88c4e8e42f183026fe73c11e0121310de68a838672a
  recognition.sandals.turn=2

ledger after sandals + photo look: turns=3
sandals turn event=TEST_ONLY_BP4_WORLD_EVT_5e8807be…
photo turn event=TEST_ONLY_BP4_WORLD_EVT_994fe682…

forged gaze:
  cold recognition still genuine sandals event; fabricated identity absent

fake ledger event:
  cold recognition={} ; recognized_identity=None

cross-target real photo event on sandals turn:
  cold recognition={} ; recognized_identity=None
```

The genuine cold view after a sandals look re-emits the earned identity (candidate test); the probe’s later photo look selects photo, so `recognized_identity` is `None` while the genuine sandals recognition entry remains present.

## Commands / receipts

```sh
/tmp/rawlsing-oct28-p1r1/venv/bin/python -m pytest -q -p no:cacheprovider --tb=short \
  WORKER_RETURNS/SOROK-P6-RECOGNITION-PROOF-20261107-R1/test_recognition_surface.py
# 5 passed in 238.71s

/tmp/rawlsing-oct28-p1r1/venv/bin/python -m pytest -q -p no:cacheprovider --tb=short \
  WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/test_house.py
# 1 passed in 83.47s
```

## Minimal fix already present

`house.derive_recognition(objects, turns, events, user_visible)` now:

- enumerates ledger turns for the actual turn ordinal;
- resolves `performed.event_id` through `session.events()`;
- requires the ID in `session.user_perceived_ids()`;
- requires committed `INSPECT`, actor `U`, and matching body target;
- derives identity from the committed object and owner-event summary.

No further authority lookup is needed for this prior REVISE scope. This is not a claim of arbitrary store hardening.

## PROGRAMMA_DELTA

- **Identity:** P6 candidate `4f3f4659…`; prior REVISE `9a8a01ac…`.
- **Function:** committed owner-event recognition provenance and exact turn ordinal.
- **Verdict:** `PRIOR_REVISE_CLOSED = PASS_SCOPED`; `FAKE_LEDGER/CROSS_TARGET/FORGED_GAZE/TURN = PASS`; `GENUINE/PLAIN/PHOTO/CONTROLS = PASS`.
- **Evidence:** 5 candidate recognition tests + 1 house test; actual cold CLI probe outputs above.
- **Limits:** sourcefree P6 only; no native/human/science/Pyat/protected claim; no runtime or PR779 writer changes.
