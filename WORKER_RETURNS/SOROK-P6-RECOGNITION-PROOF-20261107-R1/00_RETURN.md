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
