# P6 recognition surface — R1 candidate

**STATUS:** `RECOGNITION_SURFACE_IMPLEMENTED_SOURCEFREE__PASS__ORIGINAL_RED_RECEIPT_PRESERVED`

**FROZEN:** `41b21babf72c4c8b0b4b012d3c8b7d7f6247791f`
**ISOLATED CANDIDATE BASE:** `ec2892c5ac41156c1de36c6ec247c3ca2105d237`
**INDEPENDENT REVIEW REPAIRED:** `1e9da0cdc673bca2150fdfbd72e3e24c9d4f85ed`

## Corrected interpretation

The earlier red probe incorrectly treated `bench`, `mug`, `coaster`, `photo` and
`sandals` as specialized names. They are plain categories/ordinary glance
material and are allowed before recognition. The actual missing behavior was a
recognition-conditioned distinction between that plain category and a stable
specific objective identity. The original red receipt below is retained; its
four assertions are corrected historical evidence, not the current acceptance
criterion.

## Candidate recognition surface

- `house.OBJECTS["sandals"]` now carries a stable marking
  `blue-thread-left-strap`, evidence text, and specialist identity
  `the repaired blue-thread sandals`.
- `house.recognize(target, evidence_text)` returns the specialist identity only
  when the exact visible evidence is present; no actor, Nadia state, gaze
  history or unrelated item can establish it.
- `run_p6.experience` derives recognition from validated committed `house`
  objects plus the owner/world event set and genuine user-visible IDs—not ledger
  `performed`/`public.observation` copies. It requires an actual committed
  `INSPECT` by `U`, exact target, authoritative event summary/committed evidence
  and the actual ledger turn ordinal (`enumerate`). Mutable `p6_gaze.json`
  `recognized` payloads are ignored and replaced.
- Fabricated cache identity/event/marking, fabricated ledger event/summary,
  reused legitimate-but-mismatched event IDs, unrelated photo identity and old
  unverified entries cannot surface; a photo look cannot stand in for a sandals
  look. Plain `available` categories and ordinary glance remain before recognition.
  Cross-room/unknown objects still return `UNAVAILABLE` without recognition.
- The existing profile/store supplies cold reopen persistence; no new actor or
  memory engine was added.

## Runnable proof

```text
PYTHONDONTWRITEBYTECODE=1 /private/tmp/rawlsing-oct28-p1r1/venv/bin/python -B   -m pytest -q -p no:cacheprovider --tb=short   WORKER_RETURNS/SOROK-P6-RECOGNITION-PROOF-20261107-R1/test_recognition_surface.py
# 5 passed in 216.18s
```

Also retained: `WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/test_house.py` — 1 passed
in 76.42s after the candidate patch.

The test covers plain-category pre-recognition, earned `look sandals` identity,
cold `run_p6.py view` reopen, unavailable/foreign refusal, gaze-history-only and
private-text negatives, fabricated cache identity/event/marking, fabricated
ledger event/summary, reused mismatched event ID, unrelated photo target, exact
turn ordinal, changed specialist-input control, and stable gross
clock/room/available cardinality. Original red `evidence.json` remains preserved; candidate proof is
in `evidence_r1.json`.

---
# Original red receipt (preserved; corrected interpretation above)

# P6 recognition/availability proof — FAILING COUNTEREXAMPLE

**FROZEN:** `41b21babf72c4c8b0b4b012d3c8b7d7f6247791f`
**COMMAND:** `PYTHONDONTWRITEBYTECODE=1 /private/tmp/rawlsing-oct28-p1r1/venv/bin/python -B WORKER_RETURNS/SOROK-P6-RECOGNITION-PROOF-20261107-R1/probe.py`
**EXIT:** `1` (expected failing proof; no runtime edit)

## Result

The actual frozen P6 user output does not implement the requested recognition
boundary. Before any admitted look:

- `new` and `view` expose specialized names `available=["bench","mug"]`;
- `detail` immediately says `"The bench stands beside the doorway."`;
- entering the living room exposes `["coaster","photo","sandals"]` before any
  look or recognition event.

These are four failed assertions out of thirteen. The proof also confirms
passing controls: `look mug` is `ADMITTED` and exposes the chip observation;
`look sandals` from the workshop and `look missing-object` are `UNAVAILABLE`;
`look sandals` after entering the living room exposes the blue-thread detail;
and the changed-input control (`mug` → `cup`) changes the output identity while
keeping clock `248`, room `workshop`, and available cardinality stable.

Evidence: `evidence.json` (actual CLI outputs, all assertions, changed-input
control). No source or shared progress was edited.

## Fix location

Minimal repair belongs in the incumbent P6 author runtime:

- `run_p6.experience`: `objects = frame.pop("objects")`, `result["available"] =
  sorted(objects)`, `result["detail"] = objects.get(selected)` expose raw object
  keys/glance and do not gate on recognition/exposure.
- `house.scene`: returns every current-room object key and glance without a
  plain-category/recognition projection.
- `attention.select`: empty history selects the first object, so `view` exposes
  detail before `attention.register` ever records an admitted look.

The repair must introduce an explicit recognition view: plain category and no
specialized detail until a legitimate admitted look/exposure, then the
specialized object name/detail; retain the existing `house.perform`
unavailable/foreign-object refusal. No P6 runtime change was made by this proof.
