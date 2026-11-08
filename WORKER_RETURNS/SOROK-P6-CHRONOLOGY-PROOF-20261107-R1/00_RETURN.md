# SOROK P6 chronology/provenance reject-restore proof

**FINDING:** The frozen P6 cold reopen path rejects a concrete corrupted chronology/provenance link in persisted house history, and restores to the exact prior cold trace.

**INTERPRETATION:** The proof exercises the real P6 runtime and existing product/writer. The tampered `photo-exposure.depends_on` is changed from `["strap-repair"]` to `["bench-installation"]`; the persisted world checkpoint and P4 receipt expectation are updated so the run reaches P6 rather than failing earlier on P4 state mismatch. Cold reopen returns `RecursionRefusal: P6_OBJECT_PROVENANCE_MISMATCH`. Restoring the original house resources and checkpoint restores byte/material-equivalent house state and an identical cold `view` result. This proves sourcefree chronology/provenance rejection and restore, not native/actor/science authority.

**ACTION:** Preserve this runnable test as proof. No P6 runtime or P5/P4/P3 file was edited. If a failure were found, the minimal repair belongs to the incumbent P6 runtime writer; none was needed for the tested path.

**OWNER:** P6 incumbent author/runtime writer; independent P6 review remains separate.

## Frozen target and command

- Frozen runtime commit: `41b21babf72c4c8b0b4b012d3c8b7d7f6247791f`
- Proof branch: `codex/sorok-p6-chronology-proof-20261107-r1`
- Runtime files read-only; only this return directory is new.
- Command:

```text
/private/tmp/rawlsing-oct28-p1r1/venv/bin/python -m pytest -q \
  WORKER_RETURNS/SOROK-P6-CHRONOLOGY-PROOF-20261107-R1/test_p6_chronology_proof.py
```

- Exit status: **0**
- Result: **1 passed in 111.09s**
- Log: `run.log`

## Assertions

1. Real P6 state creation, room entry, sandal inspection and photo inspection.
2. Pre-attention objective existence: after entering the living room, `bench-installation` exists in house history while the `P6_OBJECT_CLOSURE` source event is absent from the user's perceived IDs.
3. Persisted chronology: `photo-exposure` depends on `strap-repair`, has a later clock, and the bench installation is earlier.
4. Adverse tamper: `photo-exposure.depends_on` is replaced by `bench-installation`; checkpoint is appended; P4 receipt expectation is made consistent with the tampered snapshot.
5. Cold reopen rejects with `P6_OBJECT_PROVENANCE_MISMATCH` before returning a view.
6. Restore: original house resources are checkpointed back; cold `view` equals the pre-tamper baseline result.
7. Restored house history, source, root, epoch, objects and rooms equal the pre-tamper material; history equality is order-insensitive dictionary material.

## Limits

Sourcefree/test-only. No native science, actor grant, human acceptance, protected merge, shared-progress edit, or runtime repair is claimed. The test uses the received P5/P4/P3 dependencies and existing P6 cold path; no source bytes or external native data are involved.
