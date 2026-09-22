# Source-Free Test Ledger and Expected Assertions

Committed test module:

`rawlsing_next/tests/test_fiabc_final_oracle_freeze_producers.py`

No tests were executed by this browser/GitHub-only worker. They are authored for the later repository test run.

## B03

1. **Determinism / source-free positive**
   - bind exact accepted successor WVS constants in the isolated test process;
   - standardize the accepted R1M JSON twice;
   - output bytes and standard oracle identities must match;
   - zero candidate process/output/root fields;
   - output schema is the live standard oracle;
   - `verify_frozen_oracle()` passes.

2. **Wrong wrapper**
   - mutate the R1M schema;
   - adapter must raise `FinalOracleProducerError`.

3. **Predecessor authority**
   - substitute predecessor Lock2 in the wrapper;
   - adapter must reject.

4. **Accepted identities**
   - assert exact R1M wrapper/truth/successor authority values.

## B05

5. **Candidate-root exclusion / 50×77 contract**
   - exact constants assert 50 candidates / 77 roles;
   - a path under `WORK_ROOT/cells/LITS_I/A` is rejected;
   - static contract confirms producer does not call `compose_p2r1_binding`;
   - producer source carries explicit zero candidate-process/output provenance.

The real LiTS producer is not invoked in these source-free tests because doing so would open the canonical DTA source. Its runtime checks fail closed on source SHA/shape, runtime identities, 50/77, accepted product, and accepted semantic replay.

## B06

6. **Two-source positive**
   - create source-free standard frozen oracle fixtures;
   - run final T3 producer;
   - require exact zero-candidate fields and exact 10→20→30 freeze order;
   - require returned byte SHA to equal emitted receipt SHA.

7. **Nonstandard oracle**
   - R1M wrapper supplied in place of standard oracle must be rejected.

8. **Candidate-owned oracle path**
   - oracle under `WORK_ROOT/cells` must be rejected.

9. **Missing oracle**
   - absent WVS oracle document must be rejected.

10. **Mutated/unverified oracle**
    - mutate a post-freeze oracle body;
    - verification must fail before T3 is emitted.

The production T3 path also self-validates with both `load_frozen_upstream_receipt()` and live T5 `load_frozen_source_oracle()`.
