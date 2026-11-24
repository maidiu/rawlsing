# B3A schema/readset repair candidate

This is a user-directed **author repair**, following the independent review at `528e8cde0cff9e28f3c55d5d54a66e820d7401fa`. It does not revise or accept that frozen review. The user asked to fix its two new schema/readset REDs. This candidate changes only the inherited `candidate/integration.py`; B2/M2, fixture authority, target rule, old tests and frozen independent assertions retain their exact input bytes.

Read `00_RETURN.md` for actual outcomes, source identities and disposition. `original_candidate_version.json` records the reviewed original, and `candidate_version.json` identifies this repair. The F2 runner regenerates a profiling matrix; its new output is retained as `evidence/F2_CASE_MATRIX.actual.json` and the copied historical matrix is restored byte-for-byte. Old candidate README/runner metadata are retained as input provenance; this root packet describes the new candidate.

The repair captures schema definitions (tables/indexes/triggers/views), table rows and `schema_version`, `user_version`, `application_id` in one consistent read transaction. It preserves an existing caller transaction. The public `snapshot()` row-only API remains compatible. Publication checks this full logical readset under `BEGIN IMMEDIATE`; refusal receipts compare the same logical state. No schema object or independent row is deleted to simulate unchanged state.

SQLite backup may change the destination schema cookie. The scratch schema counter is compared to its own immediate post-backup baseline, while public schema version is compared to the original public readset. Schema definitions and durable application/user versions must still match across both databases. Comparing source and backup cookies directly initially caused a false refusal; a rolled-back-DDL acceptance control caught it. The development failure remains in `evidence/development_schema_repair.*`, alongside the original two REDs in `evidence/before_fix.*`.

## Reproduce

In a disposable checkout with the existing authorized Git object store, Python 3.11+, pytest, Node and POSIX subprocess/SQLite support, run from this return directory:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 run_repair.py
```

The driver reconstructs missing runtime source using pinned Git objects. It runs the frozen 20-case independent court (including both original schema assertions and ten SIGKILLs), 13 extra repair controls, four clean/seeded refusals, B3 71, atomic 63, F2 42, unchanged X3 28, blinded F2, and live/cold positive and permission-absent loops. Expected historical X3 REDs remain literal failures. No frozen expectation is changed. New outputs are under `evidence/`; copied source/fixtures are in ignored `candidate/.runtime/` and can be rebuilt.

This is a local provisional branch based on author candidate `8bd4d6b01fd402e7e6a8d07903f2c3cada837f55`, not an invented HQ seal or canonical integration. A distinct reviewer must qualify the new candidate before independent acceptance. The prior reviewer is now this repair's author.

The logical readset excludes physical file layout and connection-local settings. It does not authenticate arbitrary privileged SQL writers, provide scalable transaction infrastructure, or establish power-loss durability. Native F1 gaps, M3 source-preimage quarantine, practice-witness identity, pre-loss threshold and standalone helper limitations are unchanged. No new M2 implementation, psychological law, actor/source grant, CAN008/CAN011 issuance or production integration is included.
