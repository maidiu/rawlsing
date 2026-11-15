# P3 store ABI repair return

Status: **STORE ABI REPAIR PASS AT AUTHOR SCOPE / NOT FULL P3 ACCEPTANCE**.

This repairs the two observed store defects only. It does not accept the full P3 product, does not replace the HQ owner, and does not alter accepted #704/#697, sourcepack, prior evidence, production/native/source authority or protected state.

## Defects repaired

### 1. Frozen `SOURCEFREE_TEST_ONLY` provenance

The actual frozen P3 owner plans carry:

```json
{"grade": "SOURCEFREE_TEST_ONLY", "permitted_rules": [...]}
```

with no redundant `authority` field. The prior store required both an authority and a `TEST_ONLY`-prefixed grade.

The repair now:

- accepts the exact grade `SOURCEFREE_TEST_ONLY` as the existing explicit TEST_ONLY provenance when no conflicting explicit authority is present;
- still accepts the legacy mechanical shape with a `TEST_ONLY`-prefixed grade and/or explicit `TEST_ONLY` authority;
- does not add an authority field to the stored plan and does not invent a grant;
- denies missing provenance, unknown grades, conflicting authority/grade, explicit native/production authority, and production/native flags;
- keeps source, registry, complete rule descriptor, actor-root, plan, CAS and rollback bindings unchanged.

The normalized effects receipt records `authority: "TEST_ONLY"` and the exact plan `grade`; the plan itself remains byte-preserved.

### 2. Lossless V3MS record kinds and hashes

The actual source-pinned writer and later readers use `V3MS_MEDIATOR` (and its V3MS tension/practice equivalents), while the prior store rewrote these to `MEDIATOR` before validating the supplied record hash.

The repair now preserves the exact allowed kind spelling and exact content hash through:

- reservation and commit validation;
- SQLite storage;
- targeted query;
- cold reopening;
- record-chain and schema integrity checks.

Supported losslessly, without lifecycle mutation:

```text
MEDIATOR, TENSION, PRACTICE,
V3MS_MEDIATOR, V3MS_TENSION, V3MS_PRACTICE
```

The record schema is widened to those six exact spellings. A one-time transactional migration upgrades prior three-kind stores in place; it does not rewrite records or their hashes. New stores are schema version 2.

## Files changed

Only:

- `p3/state_store.py`
- `tests/test_state_store.py`
- `evidence/storage-abi-repair/` (this new evidence directory)

Prior `evidence/storage/` files remain byte-identical. No owner, compression, projection, rule, `__init__.py`, accepted #704/#697, sourcepack, PROGRAMMA or protected file was edited.

## Unit results

```text
python3 -m pytest -q tests/test_state_store.py
51 passed in 0.74s
```

The original 42 mechanical tests remain covered; 9 new checks cover the frozen owner plan shape, conflicting/unknown/production negatives, exact V3MS sealed kinds, cold replay and prior-schema migration.

The frozen positive test uses a plan with exact `grade: SOURCEFREE_TEST_ONLY`, no authority, and a sealed `V3MS_MEDIATOR` record. It passes write, query, cold reopen and `verify()`.

## Actual owner integration result

The actual P2-root owner command was executed unchanged:

```text
python3 -m pytest -q tests/test_p3_owner.py
1 failed, 6 passed, 1 skipped in 22.40s
```

This is separate from the unit result. The three previously failing owner positives now pass, including formation/store/later-response and idempotent reopened-owner replay. The remaining failure is **not** a store defect:

```text
test_real_subprocess_crash_boundary_recovers_prepared_base
ModuleNotFoundError: No module named 'developmental_recursion'
```

The crash child is in the owner lane and needs its repository-relative engine import path repaired there. This store lane did not edit that owner/test file, did not skip it, and did not substitute a fresh root. The actual P2-root reconstruction is therefore still a remaining owner dependency, not claimed green here.

## Schema

See `SCHEMA.sql` (generated from the repaired store). The logical tables and API are unchanged; `p3_records.kind` now accepts the six exact spellings and `PRAGMA user_version=2`. The migration is transactional and preserves existing record rows/hashes.

## Custody

- Startup: `8cc2914b1089cfc113ae1737941bd2a9efde622b`
- Protected start: `c852d7516e23fcb6cf2215e9be7c5fa268503516`
- Branch: `agent/sorok-p3-store-abi-repair-20261106-r1`
- Code commit: `7aa2b78424c6f48576f0a9ad37c5def5dae1a4d8`
- Model/runtime: OpenCode, `opencode-go/deepseek-v4.1-flash#max`; quota **UNKNOWN**, not observed.

## Remaining dependency / limits

- HQ owner lane must repair the subprocess engine import and then run the genuine crash/reopen boundary.
- Full P2 producer→store→later-reader vertical acceptance remains HQ-owned.
- No native science, new rule, memory/claim issuance, source issuance, production authority, protected merge or human-validity claim is made.
- This author result is not independent acceptance.
