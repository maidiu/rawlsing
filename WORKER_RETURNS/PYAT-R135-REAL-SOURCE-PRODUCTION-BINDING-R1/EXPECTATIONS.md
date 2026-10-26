# R135 frozen narrow expectations

- Production path accepts only externally supplied `NativePreimageBundle` authorities, query authority, and an externally supplied `IssuedWorkloadRecord`.
- No production function calls `build_authority_set` or constructs ALLOW/TEST_ONLY authority defaults.
- `execute_production_workload` calls `execute_issued_workload(..., allow_test_only=False)` and does not call source_factory before `admit`.
- Synthetic harness proof must show one native empirical fact from a supplied exact query, exact output refs, no-drop/restoration, and value dependence.
- A TEST_ONLY record, wrong envelope/U/Epre/jobs/host/purpose/source/universe/risk/role must refuse.
- Existing TEST_ONLY path remains unchanged.
- Synthetic success is not source/learned/FF/V553 proof.
