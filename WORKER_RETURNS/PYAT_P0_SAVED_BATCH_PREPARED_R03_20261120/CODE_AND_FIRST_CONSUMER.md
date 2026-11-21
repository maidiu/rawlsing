# P0 C11 → I03 → saved Batch / R03 v2 prepared-session reuse (candidate)

**Role:** forward PYAT engineering. This branch is a descendant of the existing #1238 Q014–Q018/Q020 source family, NOT a PRE-MAIN receiving branch. Sourcefree-only; tests COMMITTED_UNTESTED until REMONT/OpenCode actually runs.

The recognized expensive operation is not a missing empirical-query kernel: `SavedC11Admission.execute_i03` rebuilds `DirectEstateI03Session` postings per operation. The existing `PreparedSavedC11Admission` and `execute_saved_batch` prepared path already conserve the real native I03/I05 evaluator, authority and scope. This change connects an already authenticated **ordinary** saved admission to that existing prepared path without a second full-hash/open, guarded by the original exact admission type and CURRENT check.

**Code changes:** `PreparedSavedC11Admission.from_verified_admission` and optional `execute_saved_batch(..., reuse_prepared_session=True)`; default False preserves existing saved Batch behavior. No new query grammar, scientific issuer, numerical estimator, S04 organizer, person sampler, or second persistent store. First real consumer: original eligible R03 v2 issued QUERY jobs → existing saved Batch scheduler → existing I03 execution kernel with one posting-index build. The independent Q014/R03 tests must still establish governed source/question correctness; this is an engineering throughput path only.

**Required REMONT/OpenCode execution at exact candidate SHA:**
- `python -m pytest -q -o addopts='' -p no:cacheprovider rawlsing_next/tests/test_pre553_prepared_saved_i03.py rawlsing_next/tests/test_pyat997_r03_governed_query_issuer_v2.py` (omit nonexistent named file; see exact queue target)
- Run separately one actual sourcefree `R03_ASKED_ELIGIBLE` court and existing Q014–Q018/Q020 if the exact source head supports them; do NOT copy inherited PASS counts to new SHA.
- Measure one postings build for an issued Batch, unchanged output/fact/replay identities versus legacy, false predicate, changed CURRENT grant, executor failure before a partial claim, one/ten/100 reuse with repetition clearly labeled. Host high-width one/ten/100 **distinct** work and <=6GiB remain UNPROVED.

**Unresolved:** Original R03 question administration/asked/eligible source decisions and missing scientific issuer; native all-source empirical permission and survey design/weights; S04/I05 structural authority parity; Q017 calibrated inference; actual external Field Forge source consumer. That science cannot be minted by prepared-session code.
