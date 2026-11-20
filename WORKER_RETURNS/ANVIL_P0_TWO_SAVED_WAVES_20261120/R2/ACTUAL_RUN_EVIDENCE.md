# P0 R2 actual saved-C11 attempt

## Decision

The new scoped user decision is recorded in `USER_DECISION_R2.json`, with exact
saved source/manifest identities, host `MainMac`, and purpose
`P0_TWO_SAVED_WAVES_ANALYTICAL_DOWNSTREAM_R2`. It is a new direct user decision,
not a retroactive change to any historical construction receipt or grant.

## Typed binding

The private run used the existing `IssuedWorkloadRecord` and
`CurrentDecisionResolver` contract to bind one exact decision ref per wave,
then attempted the first C6 real-carrier gate: construction of the typed
`ExternalI02Roots` required by `SavedC11Admission` / `DirectEstateI03Session`.

Command shape (run in the isolated worktree, with the private proof directory
supplied by the controller):

```bash
/usr/bin/time -l env PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 \
  python3 -B <PRIVATE_PROOF_DIR>/r2_actual_attempt.py
```

## Result

Both waves independently refused at the same earliest executable gate:

- class: `ExternalI02IntegrityError`
- message: `unsupported externally held certificate schema`
- stage: `TYPED_EXTERNAL_I02_ROOT_ADMISSION`
- saved schema: `ANVIL_STREAM_C11_ESTATE@1`
- source opened: false
- Parquet read: false
- respondent rows emitted/read: 0
- downstream I03/I05/Batch/S04/DHIKR/FF01/C4/C5/C6: `NOT_REACHED`

This is a carrier/schema incompatibility between the actual saved stream
carriers and the C6 direct-I02 admission contract. It is not an estimator,
query-issuer or native-provider compatibility result.

No schema bypass, projection, rebuild or manual root substitution was used.
A stream-carrier-to-direct-I02 adapter would be a broader carrier seam for
REMONT, not a P0 ordinary single-owner repair.
