# Mechanism I performance baseline

Measured on Darwin x86_64 at local implementation `2c963db4d`, exact
published tree `62431ce559b5c89f78f0287a5b7e5f705c441291`. The fixture
is the actual P4 opening, one automatic worker, one mock HTTP completion,
one committed H0 texture fact, and a separate P4 inspection. This is a
single-target baseline with no concurrent foreground load.

| Measurement | Observed |
|---|---:|
| Complete fixture call, including both foreground subprocesses and mock endpoint | 16.80 s |
| Reopen P4 owner in a separate process with imports already loaded | 2,443.91 ms |
| First `HistoricalWorld.read_inspection` after reopen | 70.20 ms |
| Same owner, next 300 reads, p50 | 69.78 ms |
| Same owner, next 300 reads, p95 (nearest rank) | 77.64 ms |
| Same owner, next 300 reads, maximum | 114.38 ms |

All reads returned the same inspected fact
`history-fact:bb52b812d27e032fdb1e958a85cf0d2b55b300d93a837021de3180f41d6d25ce`.
The measured path reopens no owner during warm reads, but still resolves
world and perception through the existing session on each call. The timings
therefore include those lookups. No derived-index speedup is established.

Reproduce the state from the repository root with the configured test Python.

```sh
python -m pytest -q rawlsing_next/tests/test_sorok_history_wake.py::test_p4_wake_completes_through_a_mock_http_endpoint --basetemp "$SOROK_BENCH_STATE" --durations=1
```

Use a fresh task-owned path for `SOROK_BENCH_STATE`. In a separate process,
import `run_p4.open_owner` from the P4 directory. Use the real non-symlink
test state under that path and time `open_owner(state / "actual-p2")`.
Take the last turn's `receipt.performed.event_id` from `p4_receipts.json`.
Time `HistoricalWorld(owner.base_owner.fanin.session).read_inspection(event_id)`
once, then 300 times without reopening. Check equality against the first
complete response on each iteration. Use a monotonic nanosecond timer.

Live provider latency, usage and cost are `LIVE_PROVIDER_NOT_RUN`. Queue
lead, index rebuild, cache behavior, stale cost and realistic mixed-load
tails remain unmeasured. The complete fixture duration combines different
phases and is unsuitable as a warm read or model SLO.

## Warm root replay optimization

Profiling eight reads attributed 2.179 of 2.247 instrumented seconds to
`generate_root`. A latest-checkpoint SQL experiment left the same fixture
near baseline at 69.57 ms p50 and was discarded. The received S44 root reader
now reuses a verified root digest only while the exact root document bytes
match. It still checks the branch binding and each language event reference
on every read. The P4 transport regression also checks refusal after the
cached root document is altered.

The same saved state and 300-read procedure produced 5.78 ms p50, 7.37 ms
p95, and 10.45 ms maximum. First read was 5.73 ms after owner reopen.
Owner reopen was 1,308.81 ms in that run. All 300 reads returned the identical
fact ID above. These are single-fixture measurements. They establish the
cost of avoiding repeat root generation in this path.
