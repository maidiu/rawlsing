# SR04 PRE-ACCEPTANCE HARNESS AUDIT

Status: `HARNESS_INVALIDATED__NO_CARRIER_RESULT_ACCEPTABLE`

Audited implementation HEAD: `ea508994a80b9d66bd3729f6641ef5600aa624c4`

This audit is HQ/browser authority. It does not alter C11 semantics or the carrier court. It invalidates the current mechanical implementation before any carrier result can be accepted.

## Terminal ruling

`ea508994a80b9d66bd3729f6641ef5600aa624c4` and all earlier SR04 harness commits are **PRE-ACCEPTANCE IMPLEMENTATION ONLY**. No result produced by them may close G-SR04.

The defects below are implementation defects, not evidence for or against any carrier.

## Proven defects

1. **Q04 oracle-shape violation**
   - Frozen contract: `Q04_WVS_Q152_TO_Q156_5WAY` must execute the actual Q152×Q153×Q154×Q155×Q156 joint.
   - Audited harness SQL only performs `SELECT COUNT(*) ... var_name='Q152'`.
   - Therefore the measured query is not the frozen query.

2. **Q08 oracle-shape violation**
   - Frozen contract: `Q08_BRANCH_CONDITIONED_COTRAVEL` must condition on `benchmark_branch_id=1` and return the Q152×Q153 joint.
   - Audited harness SQL only counts rows for Q152/Q153 and does not apply branch conditioning or return the joint.

3. **Candidate query results are not compared to the independent oracle**
   - The harness computes `QUERY_ORACLE.json` but candidate execution treats successful SQL execution as correctness.
   - A carrier can therefore return a wrong answer and still receive `MEASURED_CORRECT`.

4. **Stored-candidate replay is not actually read back for three candidates**
   - DuckDB-native, SQLite and PostgreSQL replay digests are computed from the original in-memory pandas fixture rather than streaming the data back from the candidate store.
   - Therefore the digest cannot prove storage round-trip equivalence.

5. **PostgreSQL connection lifetime defect**
   - The harness closes the PostgreSQL connection immediately after load/index build and then attempts to execute timed queries through that closed connection.
   - The current run is therefore expected to fail or mis-handle PostgreSQL timing even after the locale correction.

6. **Slow-debug execution shape**
   - The harness rebuilds and expands ~3,029,328 neutral events from raw source bytes before discovering small implementation defects.
   - This is not a semantic defect, but it makes mechanical debugging unnecessarily expensive and repeatedly redoes already-proven source decoding.

## Required correction discipline

Before another full raw-source run:

- implement a tiny synthetic fixture exercising all 16 named query shapes;
- require exact candidate-output equality to that synthetic oracle;
- require true candidate read-back digests for all four candidate types;
- unit-test PostgreSQL connection lifecycle with the tiny fixture;
- only after those tests pass may the harness consume WVS7/LiTS I raw bytes;
- after a real neutral fixture is built and validated once, it may be reused by exact digest under the SR04 execution-discipline addendum rather than rebuilt after every implementation-only patch.

## No architecture consequence

Nothing in this audit changes:

- the raw-source proving inputs;
- the four carrier candidates;
- the correctness > speed > lightness priority;
- the 5 GiB reserve;
- I02/I03/I05 semantics;
- the eventual all-35-source rebuild.

It only restores the rule that a carrier may be called correct **only after exact query answers and exact stored read-back agree with an independent oracle**.
