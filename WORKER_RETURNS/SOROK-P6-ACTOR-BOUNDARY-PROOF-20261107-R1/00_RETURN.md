# SOROK P6 actor input/output boundary proof

**FINDING:** The frozen P6 SAY path preserves the actual P4/Nadia actor input and attributable actor/world effect exactly when only the private P6 gaze profile changes at the runtime boundary.

**INTERPRETATION:** The proof exercises the real P6 entry point and real P4 speech admission. A baseline SAY with `request_edge=False` is admitted as `PERCEIVED_NO_INSPECTION_REQUEST`, produces no expression, and runs an independent material/time interval that performs an actual world action and consumes material. Changing only actual conduct to `request_edge=True` changes the actor result to `UPTAKE`, creates a `SPEECH` expression, returns that expression as the P6 invitation, and omits the interval. Restoring the same baseline conduct while changing only `state/p6_gaze.json` changes the user-facing detail selection but leaves the P4 speech attempt/performed event, uptake readset, expression, interval, turn before/after material, narration, clock, room, admission and invitation identical. This isolates the actor boundary from the private gaze value; it does not claim native science, actor authority, or human acceptance.

**ACTION:** Preserve this runnable proof. No P6/P5/P4/P3 runtime file was edited. If a boundary leak were found, the minimal repair belongs to the incumbent P6/P4 runtime writer; none was found for the tested path.

**OWNER:** P6 incumbent author/runtime writer; independent P6 review remains separate.

## Frozen target and command

- Frozen runtime commit: `41b21babf72c4c8b0b4b012d3c8b7d7f6247791f`
- Inherited chronology proof: `9657a7b65da56c3e0ef6ec7f0538ac2aebc023f6`
- Proof branch: `codex/sorok-p6-actor-boundary-proof-20261107-r1`
- Runtime files read-only; only this return directory is new.
- Command:

```text
/private/tmp/rawlsing-oct28-p1r1/venv/bin/python -m pytest -q \
  WORKER_RETURNS/SOROK-P6-ACTOR-BOUNDARY-PROOF-20261107-R1/test_p6_actor_boundary_proof.py
```

- Exit status: **0**
- Result: **1 passed in 31.23s**
- Log: `run.log`

## Assertions

1. Real P6 `new`, real P6 `say`, real P4 `admit_speech`, and the existing P4 receipt ledger.
2. Baseline conduct: the exact text and `request_edge=False` appear in both the P4 attempt and performed event body; uptake is `PERCEIVED_NO_INSPECTION_REQUEST`; expression is absent.
3. Independent material/time activity: the baseline interval contains a real `actual_action_event_id` and `material_remaining` decreases; the P6 clock advances beyond the no-interval edge run.
4. Changed actual conduct: `request_edge=True` appears in the P4 attempt and performed event; uptake becomes `UPTAKE`; a `SPEECH` expression exists; the P6 invitation equals that expression event; the interval is absent; and the uptake readset differs from baseline.
5. Private boundary: the tampered `p6_gaze.json` profile is active because P6 detail selection differs from baseline.
6. Boundary isolation: with identical baseline conduct, the tampered-profile run has exactly identical `speech`, `uptake`, `expression`, and `interval` material, and identical `before`/`after` turn material; P6 narration, clock, room, admission and invitation also remain identical.
7. No profile edit touches P4 actor input or the independent material/time interval.

## Limits

Sourcefree/test-only. No native science, actor grant, human acceptance, protected merge, shared-progress edit, or runtime repair is claimed. The private `p6_gaze.json` change is test input only. The test uses the received P5/P4/P3 dependencies and existing P6 SAY path; no source bytes or external native data are involved.
