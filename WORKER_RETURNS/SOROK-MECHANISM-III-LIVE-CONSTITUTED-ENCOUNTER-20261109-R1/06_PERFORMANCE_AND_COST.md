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

## Profile-guided snapshot reuse

A `cProfile` trace of one joined P6 fixture SAY on the previous runtime
cut recorded seven P2 snapshots and 77 root reads. Root reads consumed
22.149s cumulative within the 26.924s profiled turn. The reader now
uses the pre-transduction P3 owner snapshot for both encounter identity
and the stale-person guard. The fresh post-transduction check stays in
place. The same profile then recorded six P2 snapshots, 68 root reads,
and a 25.065s profiled turn. Both runs committed a P2 reply through P6.
Profiler overhead and host load make these times unsuitable as normal
turn latency estimates.

The targeted causal and unrelated-history tests passed (2 tests,
61.20s with concurrent local runs). Pruning an unrelated record changes
the full person identity carried for audit and leaves the scoped
recruitment and move unchanged. A stale person still refuses.

For P6 SAY, the P4 action owner now uses its existing opening snapshot
to verify the persisted ledger identity. P6 omits the redundant opening
snapshot for SAY only. The profiled path then reported five P2
snapshots and 59 root reads, down from six and 68 respectively.
The profiled turn took 21.980 seconds, a diagnostic result with
instrumentation overhead. This change neither skips P2 verification
nor reuses a snapshot across a write. The focused P6 regression passed
in 48.06s, including refusal of a tampered opening identity before
SAY or transduction, successful exact restoration, and cold retry.

## Controlled relevant-history growth

At author return `0df9b0044499dfc6a57b7d7ea35ab07e66846a09`,
a local Python probe used the received sourcefree P3 fixture to
form one or sixteen recognized-plan mediators through the real
owner. The larger fixture uses strictly antecedent resealed clocks
and parent references. Each run admitted a real non-edge SAY and
invoked `response.read_response` three times against the same open
owner and event. Formation, setup and expression were outside this
reader-only sample. The selected move was joint check in both runs.

| Relevant mediators | Wall seconds for three individual reads | Median seconds | Total CPU seconds | Final uptake bytes | Indexed queries | Records returned | Full scans |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1.743, 1.705, 1.753 | 1.743 | 5.183 | 2,897 | 3 | 3 | 0 |
| 16 | 1.795, 1.739, 1.944 | 1.795 | 5.364 | 18,257 | 3 | 48 | 0 |

The psyche head was identical before and after each series. The
receipt grows with relevant sources, and the indexed query count
stays one per read. This small controlled sample does not establish
a production latency curve. Concurrent-load and failure-latency
measurements remain unrun.
