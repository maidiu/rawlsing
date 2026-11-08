# SOROK P6 recognition closure — independent review

**Repaired head:** `803a4a52e84d6d90df740785b8fd077a581d0a18`
**Prior review:** `1e9da0cdc673bca2150fdfbd72e3e24c9d4f85ed` (REVISE)
**Frozen draft:** `41b21babf72c4c8b0b4b012d3c8b7d7f6247791f`
**Review scope:** independent runtime review; no author-code edits.
**VERDICT: REVISE** — the fabricated `p6_gaze.json` path is fixed, but fabricated P4 ledger receipt/observation content is still accepted as recognition authority. Turn ordinal is also not the actual P4 turn.

## Findings

| Area | Result | Finding |
|---|---|---|
| Fabricated `p6_gaze.json` identity/event/marking | **PASS** | Cold view ignores the tampered `recognized` cache and rederives genuine recognition from durable ledger turns. |
| Fabricated photo profile | **PASS** | Fabricated photo recognition is ignored; photo look remains ordinary and no sandals recognition is emitted. |
| Genuine earned control | **PASS** | Real `look sandals` emits `the repaired blue-thread sandals`, marking `blue-thread-left-strap`, and the actual P4 performed event ID. |
| Plain category/unrelated look | **PASS** | `new` exposes `bench/mug`; pre-recognition `view` has `recognized_identity=None`; `look photo` has no recognized identity. |
| Committed object binding | **PASS** | `derive_recognition` rechecks committed `house.OBJECTS` marking/evidence and derives identity from the performed summary. |
| P4 ledger authority | **REVISE** | Editing the ledger’s `performed`/`public.observation` to a fake event ID and summary still emits authoritative recognition. No lookup against the committed P4 event/observation set occurs. |
| Turn ordinal provenance | **REVISE (data)** | `turn = len(recognized) + 1` counts recognized objects, not the actual P4 turn. Earned sandals reported `turn: 1` while the ledger had `2` turns. |
| Gaze/actor boundary | **PASS by code inspection** | `attention.py`/`gaze.py` unchanged; gaze renders only `perceived_by_user` events. The remaining defect is ledger provenance, not actor-state leakage. |

## Exact cold-CLI reproduction

Genuine earned control:

```text
look admission = ADMITTED
recognized_identity = the repaired blue-thread sandals
recognition.sandals.event_id = TEST_ONLY_BP4_WORLD_EVT_5e8807be9d3ca1d045bbe88c4e8e42f183026fe73c11e0121310de68a838672a
ledger turns = 2
recognition.sandals.turn = 1
```

Fabricated gaze cache (fixed):

```text
tampered p6_gaze recognized = FABRICATED IDENTITY / fake-event / fake-marking
cold view recognized_identity = the repaired blue-thread sandals
cold view recognition = genuine event ID only; no photo entry
```

Fabricated P4 ledger (still accepted):

```text
edited ledger performed = kind INSPECT, actor_id U, target sandals,
  summary "Blue thread crosses the left strap.", event_id FAKE-LEDGER-EVENT
edited ledger public.observation = event_id FAKE-LEDGER-EVENT, perceived_by_user true
cold view recognized_identity = the repaired blue-thread sandals
cold view recognition.sandals.event_id = FAKE-LEDGER-EVENT
```

`FAKE-LEDGER-EVENT` has no corresponding committed P4 event. The existing owner
surface is computed before recognition (`view = surface(owner, ledger)`) and
contains the authoritative visible observations, but `derive_recognition` does
not use it.

## Minimal fix locus

`house.derive_recognition` / `run_p6.experience` recognition projection:

1. Use the existing `view["observations"]` (or the owner/world event store) as the
   authority set, not the ledger’s copied `receipt.performed`/`public.observation`.
2. Require the ledger event ID to resolve to an actual committed `INSPECT` event
   with `actor_visible_id == "U"`, matching target, matching summary/evidence,
   and `perceived_by_user is True`.
3. Use the actual ledger turn index (`enumerate(ledger["turns"], start=1)` or the
   matching turn’s ordinal), not `len(recognized) + 1`, for the recognition
   `turn`.
4. Keep the committed `house.OBJECTS` marking/evidence binding and the existing
   gaze/actor boundaries unchanged.

This is an existing-authority lookup/provenance repair, not a new signature
framework or broad hardened-store design.

## Commands / receipts

```sh
/tmp/rawlsing-oct28-p1r1/venv/bin/python -m pytest -q -p no:cacheprovider --tb=short \
  WORKER_RETURNS/SOROK-P6-RECOGNITION-PROOF-20261107-R1/test_recognition_surface.py
# 4 passed in 177.28s

/tmp/rawlsing-oct28-p1r1/venv/bin/python -m pytest -q -p no:cacheprovider --tb=short \
  WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/test_house.py
# 1 passed in 75.65s
```

Additional actual cold-CLI fabricated-ledger and fabricated-gaze probes are the
exact outputs above. The candidate test suite covers fabricated gaze but not
fabricated ledger receipt/observation content; that is the test gap.

## PROGRAMMA_DELTA

- **Identity:** P6 repaired head `803a4a52…`; prior review `1e9da0c…`; frozen `41b21bab…`.
- **Function:** sourcefree recognition runtime closure review.
- **Verdict:** `GAZE_CACHE_FABRICATION = FIXED`; `GENUINE/PLAIN/PHOTO/CONTROLS = PASS`; `P4_LEDGER_AUTHORITY = REVISE`; `TURN_ORDINAL = REVISE_DATA_PROVENANCE`.
- **Minimal fix:** verify ledger event IDs against existing owner observations/world events and use the actual ledger turn ordinal.
- **Limits:** no source/native/human/science/Pyat claim, no protected merge, no PR779 writer changes, no author-code edits.
