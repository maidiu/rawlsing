V0 retained as correctness oracle.

V1, V2, V3, V4, and V5 passed exact baseline-root/layout checks at 250K. V4 was the fastest safe temporary configuration at 250K and passed exact baseline-root/layout checks at 2M.

V6B was the fastest large-final-shard layout at 250K and passed exact logical/audit parity at 2M, but total wall time was slower than V4.

V7 passed exact logical/audit parity, density <= 36 B/cell, and projected full-WVS storage <= 2 GiB, but was slower than V6B and V4. It is not selected.

Final: `R5_SERIAL_TURBO_VALIDATED__MODEST_GAIN__HQ_DECISION_REQUIRED`.
