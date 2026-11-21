# Reuse / hardcoding audit

Generic and reusable in principle:

- `pre553_anvil_stream_native_i03.VerifiedAnvilStreamEstate`
- `execute_anvil_stream_i03`
- `pre553_anvil_stream_issuance.HeldStreamIssuanceDecision`
- `pre553_anvil_stream_recorded.HeldRecordedOperation`
- `RecordedUniverseUse`

Explicit SRC04/q103 hardcoding in operator artifacts (do not reuse unchanged):

- `WORKER_RETURNS/.../run_recorded_q103_private.py`: owner SHA, `SRC04`,
  q103 question, operation and output naming.
- `WORKER_RETURNS/.../q006_materialize.py`: `SRC04`, q103, owner SHA, q103
  operation and allowed-code defaults.
- `WORKER_RETURNS/.../proof_recorded_operation.py`: `SRC04`, q103 fixture.
- Test/operator paths named q103/SRC04.

No product edit was made.
