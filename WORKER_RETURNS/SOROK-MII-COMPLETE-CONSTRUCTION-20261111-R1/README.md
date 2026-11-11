# Sorok Mechanism II sourcefree encounter

This checkpoint integrates a finite factual presentation layer into the existing
P6/P5/P4/P2 encounter. World and actor owners remain authoritative. MII only
selects and renders already committed, viewer-eligible facts; it does not write
world or actor state and makes no ordinary-presentation model call.

## Run

```sh
PYTHONDONTWRITEBYTECODE=1 /private/tmp/rawlsing-oct28-p1r1/venv/bin/python -B \
  WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/run_p6.py \
  --state .mii-test-state/demo new
```

Then use `view`, `go "living room"`, `look sandals`, `look photo`, `attend`,
`wait N`, and the MII controls:

```text
mii-status
mii-export
mii-reset
mii-stop-learning
mii-enable-learning
mii-learn-label --target TARGET --label LABEL
mii-correct-label --target TARGET --label LABEL
mii-correct-attention --target TARGET --weight N
```

Use `new --scene gallery` or `new --scene symbolic` for materially different
sourcefree fixtures. Neutral mode is the default. Adaptive mode is explicit and
only updates from performed `look` actions; system-offered and independently
chosen targets receive different evidence weight. Exposure records retain the
full eligible candidate map separately from the selected/offered detail.

## Interfaces

- `mii.py` owns `SOROK_MII_GAZE@1`, `SOROK_MII_SURFACE@1` and
  `SOROK_MII_EXPOSURE@1`.
- `house.py` supplies the house/gallery sourcefree fixtures and
  viewer-specific `presentation_conditions`.
- `run_p6.py` remains the integrated first consumer.
- `test_mii.py` covers neutral exposure, cold replay, observer identity,
  occlusion/restore, earned versus forged recognition, offered versus
  independent targeting, adaptive controls, duplicate requests, corrupt profile
  recovery, gallery fixture, and control isolation from world history.
- `measure_mii.py` writes `measurements.json`.

## Limits

Sourcefree TEST_ONLY engineering. No native science, human validity, live
provider inference, production privacy approval, or protected merge is claimed.
The user derivative profile is a separate presentation artifact; it is not
Nadia's actor memory or canonical world history.
