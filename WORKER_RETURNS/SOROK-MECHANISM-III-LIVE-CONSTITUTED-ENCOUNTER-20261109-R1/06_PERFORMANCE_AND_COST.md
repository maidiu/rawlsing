# Local fixture performance

Measured five ordinary non-edge SAY turns through P4 `act` using one
already-open P3/P2 owner, one recognized-plan history, and a local fixture
transducer. Each turn included speech commitment, the actual indexed P3
reader, response commitment and the normal public projection. Setup and
owner opening were outside the warm sample. Timing used Python
`time.perf_counter` and `time.process_time`.

| Measurement | Observed |
| --- | --- |
| Warm wall seconds | 3.034, 3.734, 3.128, 3.081, 3.199 |
| Warm median wall seconds | 3.128 |
| Total warm CPU seconds | 15.771 |
| Cold subprocess `run_p4.py --state <state> view` wall seconds | 3.843 |
| Parent peak RSS bytes | 48,017,408 |
| Last internal uptake receipt bytes | 2,495 |
| P3 targeted queries / full scans | 5 / 0 |
| P3 records returned / written | 5 / 0 |
| Store row reads including setup | 27 |
| P3 database / WAL bytes at warm readback | 135,168 / 4,152 |

Five fixture calls and zero external model calls were observed. Live
transport, token counts, provider cost, history-tail growth, and
load/failure latency remain NOT_RUN. Physical I/O bytes were not measured.
The cold view is a separate startup/read measurement. It does not
estimate a cold SAY. Five turns do not support a stable p95.
