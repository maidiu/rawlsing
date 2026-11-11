# Current R3 measured costs — sourcefree candidate

At runtime `634b75d6e`, actual DeepSeek H1 production→existing owner→institution/activity graph→P4 inspector→cold equality completed in attempt09. Provider inference48.967s;4480input/3703output tokens (2666reasoning). Reported list cost0.0028938 and Go allowance0.00173628; subscription cash charge0 does not mean no resource cost. Attempt08 H0 cost61.158s,4225input/2973output. Attempts06/07 shared requests timed out at120s; missing usage/cost is NOT_REPORTED, not zero. Attempt10 malformed links were rejected while uninspected activity remained HELD. All raw requests/results/failures are retained. Full per-call summary is in `06_COST_RECEIPTS_R3/provider-call-summary.jsonl` (a returned text is not necessarily owner acceptance).

The same three committed targets include the archive artefact, exchange measuring resource and original use-tool, plus a source-qualified institution and material activity.24 warm samples per reader, separate first-after-open sample, no provider calls:

| Measurement | Before per-read snapshot reuse | After per-read snapshot reuse |
|---|---:|---:|
| Depth batch (3 targets), p50 |437.01ms|114.94ms|
| Depth batch, p95 |513.94ms|137.00ms|
| Depth batch, max |519.47ms|244.72ms|
| Graph, p50 |88.18ms|31.44ms|
| Graph, p95 |100.70ms|37.56ms|
| Graph, max |100.71ms|55.38ms|
| Cold owner open |1.976s|1.980s|
| Process peak RSS |51,789,824bytes|51,994,624bytes|

State bytes2,723,979; graph JSON3815bytes, unchanged. Every depth and graph result hash is identical before/after. Cache lives for one synchronous reader only; a subsequent read rechecks current world/source and still refuses withheld/deleted parents. It does not memoize rights or validated truth across operations. Profiling found18 full world reconstructions for three depth reads; the implementation removes redundant reconstruction within the reader. Raw samples, exact owner blobs, environment and parity are in `06_COST_RECEIPTS_R3`.

Reproduce against a fresh command-produced state with `09_LIVE_HISTORY_RUN.py`, then run `11_MEASURE_HISTORY.py --state <state> --out <jsonl>` using the recorded Python. Provider/queue work is bounded separately by existing outbox attempts, maximum3-job drain, up-to8-target source cohort, depth2/max4 dependency activation and opt-in finite idle slots. Foreground surface does not wait for provider; unresolved physical need may legitimately hold S46.

These are local synthetic engineering measurements, not population, production load or tail guarantees. Current graph rebuild still scales with admitted episode volume. At final source0b0eb94, graph@2 additionally validates transitive historical support and exposes actual causal/support edges: the same24-sample cohort depth-batch p50/p95/max was150.76/221.39/231.04ms; graph42.50/66.95/71.46ms; cold open2.284s; peak RSS52,830,208bytes. State remained2,723,979bytes and graph JSON6192bytes. These final graph semantics include extra edges and are not presented as a pure speed comparison with graph@1. Exact current samples are `current-graph2.jsonl`. A separate controlled sourcefree component run at0b0eb94 (not live inference) measured surface+atomic outbox admission17.90/15.47ms, source-policy installation13.47ms, queue lead before lease29.06ms, lease88.38ms, candidate persistence21.36ms, owner+index commit327.88ms including nested graph rebuild130.56ms. Nested spans are inclusive and must not be summed. Raw source blobs, CPU/RSS and reproduction are in `owner-phase-final.json` and `measure-owner-phases.py`. Do not subtract model time from whole CLI time and label the remainder owner latency. Historical results below retain their exact earlier scopes.

---

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
python -m pytest -q 'rawlsing_next/tests/test_sorok_history_wake.py::test_p4_wake_completes_through_a_mock_http_endpoint[new]' --basetemp "$SOROK_BENCH_STATE" --durations=1
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
