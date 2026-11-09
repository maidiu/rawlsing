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

## Joined P6 speech measurement

Code revision `0455726999350fd66d68ee637ee9299df825dbb8`.
Five actual P6 SAY calls in the same Python process, each through
`run_p6.experience` with a fresh request ID and the local fixture
transducer. The P6 entry point reopened the owner each turn. A sixth
SAY used the same state and fixture in a fresh Python subprocess.
All six committed a reply.

| Measurement | Observed |
| --- | --- |
| Same-process P6 SAY wall seconds | 8.775, 8.894, 8.683, 8.590, 8.619 |
| Median same-process P6 SAY seconds | 8.683 |
| CPU seconds for the five P6 calls | 43.283 |
| Fresh-process P6 SAY wall seconds | 8.817 |
| Parent peak RSS bytes | 52,109,312 |
| Final internal uptake bytes | 2,897 |
| Parent rusage block counters delta | 0 input / 0 output |

The block counters do not establish physical I/O bytes. This is a
fixture-backed run with six local calls and zero external model calls.
The five samples do not warrant a p95. No controlled historical-tail
or concurrent-load series was run. These P6 figures include owner
reopen and should be kept separate from the earlier open-owner P4
measurement above.
