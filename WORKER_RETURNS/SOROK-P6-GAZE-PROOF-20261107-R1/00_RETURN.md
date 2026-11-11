# SOROK P6 — same-world gaze counterfactual proof

**RESULT: PASS.** The real frozen P6 runtime distinguishes earlier attention from
actual user conduct.

- **Frozen P6 SHA:** `41b21babf72c4c8b0b4b012d3c8b7d7f6247791f`
- **Proof branch:** `codex/sorok-p6-gaze-proof-20261107-r1`
- **Runtime:** P6 `run_p6.experience` -> P5/P4 entry points; sourcefree only.
- **Proof:** `WORKER_RETURNS/SOROK-P6-GAZE-PROOF-20261107-R1/test_gaze_proof.py`
- **Environment:** `/private/tmp/rawlsing-oct28-p1r1/venv/bin/python`

## Command and result

```sh
/private/tmp/rawlsing-oct28-p1r1/venv/bin/python -m pytest -q \
  WORKER_RETURNS/SOROK-P6-GAZE-PROOF-20261107-R1/test_gaze_proof.py
```

```text
.                                                                        [100%]
1 passed in 100.19s
exit status 0
```

## Counterfactual construction

One `P6 new` state is created. The exact initial state directory is copied to a
backup; each variant restores that same-path, byte-identical snapshot. The
objective world, initial actor, clock, and actual user conduct sequence are
therefore held fixed:

```text
new -> view (phenomenal only)
go living room -> look sandals -> go workshop   (same in both variants)
```

Only `p6_gaze.json` prior attention/exposure history is varied:

- variant A: history target `bench`;
- variant B: history target `mug`.

## Assertions observed

- Both variants remain at clock `248` for the first view and `253` after the
  identical conduct sequence.
- Same room `workshop`; same available objects `["bench", "mug"]`.
- Optional phenomenal detail differs:
  - A: `The bench stands beside the doorway.`
  - B: `A mug stands beside the bench.`
- Identical committed world: `owner.snapshot().document()` equal.
- Identical user conduct: P4 ledger equal; user-perceived event IDs equal.
- Identical Nadia conduct: `session.episodes("A")` equal.
- Identical positions and P6 house/object/history state.
- Only gaze history/exposure and selected detail differ.

This is the required distinction: attention changes an optional phenomenal
selection; it does not change the committed world, clock, user conduct, or
Nadia's conduct.

## Scope / limits

- The proof uses the frozen P6 runtime read-only; no P6/P5/P4/runtime file was
  edited. No shared progress or protected state was changed.
- P5 #775 and P6 #779 remain unreceived candidates; this proof does not accept
  or merge them. Sourcefree evidence only; no native/S3/science/human claim.
- No runtime failure was found, so no repair is requested from the incumbent P6
  writer.
