# SOROK P6 recognition runtime — independent review

**Candidate:** `013c63d3be43d7e32d03a0a7fa72ac22228df1f1`
**Frozen draft:** `41b21babf72c4c8b0b4b012d3c8b7d7f6247791f`
**Review scope:** independent runtime review; author code not edited.
**VERDICT: REVISE** — cold view trusts persisted `p6_gaze.json` recognition entries and emits fabricated authoritative identity/event/marking without a real admitted look.
**Isolated review branch:** `codex/sorok-p6-recognition-independent-review-20261107-r1`; exact return SHA reported by push readback.

## Findings

| Area | Result | Finding |
|---|---|---|
| Plain category before evidence | **PASS** | `new` exposes `bench/mug` as plain categories; `view` before look has `recognized_identity=None`, `recognition={}`. |
| Earned exact marking | **PASS** | `look sandals` is `ADMITTED`; emitted identity `the repaired blue-thread sandals`, marking `blue-thread-left-strap`, evidence `Blue thread crosses the left strap.` |
| Cold persistence (genuine) | **PASS** | Cold `view` after earned look emits the same identity and recognition entry. |
| Unrelated/photo/unavailable controls | **PASS** | `look photo` is admitted but emits `recognized_identity=None`; `look missing-object` is `UNAVAILABLE` with no recognition. |
| Changed evidence | **PASS** | Direct `house.recognize` with alternate marking/evidence returns the alternate identity; old evidence and `photo` evidence return `None`. |
| Gaze/actor boundary | **PASS by code inspection** | `attention.py`/`gaze.py` unchanged; gaze renders only `perceived_by_user` P4 events; recognition is from the performed event summary, not actor/Nadia state. |
| Cold fabricated recognition | **REVISE** | Cold `view` emits arbitrary persisted `recognized` identity/event/marking without checking committed marking or any P4 performed event. |

## Exact defect reproduction

Real CLI path, disposable state:

1. `run_p6.py new`
2. `run_p6.py go living room`
3. `run_p6.py look sandals`
4. Tamper `p6_gaze.json` `recognized.sandals` to fabricated identity/event/marking.
5. Cold `run_p6.py view`

Observed:

```text
view_fabricated.recognized_identity = FABRICATED AUTHORITATIVE IDENTITY
view_fabricated.recognition.sandals.event_id = fake-event-id
view_fabricated.recognition.sandals.marking = fake-marking
```

Replacing only the earned event/marking with a mismatched value:

```text
view_mismatched_event.recognized_identity = the repaired blue-thread sandals
view_mismatched_event.recognition.sandals.event_id = mismatched-event-id
view_mismatched_event.recognition.sandals.marking = wrong-marking
```

Fabricated photo entry with an admitted-photo-free profile:

```text
view.recognized_identity = FABRICATED PHOTO IDENTITY
view.detail = A photograph leans against the wall on the shelf.
```

Genuine earned state for comparison:

```text
earned_profile.event_id = TEST_ONLY_BP4_WORLD_EVT_5e8807be9d3ca1d045bbe88c4e8e42f183026fe73c11e0121310de68a838672a
p4_performed.event_id    = TEST_ONLY_BP4_WORLD_EVT_5e8807be9d3ca1d045bbe88c4e8e42f183026fe73c11e0121310de68a838672a
p4_performed.summary     = Blue thread crosses the left strap. The cork at the heel is dark.
committed marking        = blue-thread-left-strap
```

The cold view never compares the persisted entry to `house.OBJECTS` marking/evidence/identity or to the actual P4 performed event. A caller who can write `p6_gaze.json` can therefore mint authoritative-looking recognized identity, including for `photo`, without admitted look evidence. Subjective glance/detail labels remain separate; the defect is specifically the authoritative `recognized_identity`/`recognition` surface.

## Minimal fix locus

`run_p6.experience` cold-view recognition projection, not a new store/signature design:

- Do not trust persisted `identity`/`marking`/`evidence` directly.
- For the selected object, require the persisted `event_id` to resolve to an actual P4 performed `INSPECT_OBJECT` event for that exact target, and require its summary to contain the committed `house.OBJECTS[target]["evidence"]`.
- Re-derive identity/marking from `house.recognize(target, performed.summary)` and compare with the committed object; drop/refuse mismatches.
- Alternatively persist only the earned `event_id` and re-derive the recognized identity at view time from the P4 event plus committed object.
- Keep plain `available`/`detail`, genuine cold persistence, unavailable/foreign refusal and gaze/actor boundaries unchanged.

## Commands / output

```sh
/tmp/rawlsing-oct28-p1r1/venv/bin/python -m pytest -q -p no:cacheprovider --tb=short \
  WORKER_RETURNS/SOROK-P6-RECOGNITION-PROOF-20261107-R1/test_recognition_surface.py
# 3 passed in 112.92s

/tmp/rawlsing-oct28-p1r1/venv/bin/python -m pytest -q -p no:cacheprovider --tb=short \
  WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/test_house.py
# 1 passed in 92.34s
```

Additional real-CLI fabricated-entry probes are the exact outputs above. No source/human/native claims, no Pyat work, no protected merge, no PR779 writer changes, no author-code edits.

## PROGRAMMA_DELTA

- **Identity:** P6 candidate `013c63d3…`; frozen `41b21bab…`.
- **Function:** sourcefree recognition surface review.
- **Verdict:** `PLAIN_CATEGORY/EARNED/COLD-GENUINE/CONTROLS = PASS`; `COLD_FABRICATED_RECOGNITION = REVISE`.
- **Minimal fix:** revalidate persisted recognition against committed marking and actual P4 performed event at cold view.
- **Limits:** no original/native/human/science/Pyat claim; no protected receiving.
