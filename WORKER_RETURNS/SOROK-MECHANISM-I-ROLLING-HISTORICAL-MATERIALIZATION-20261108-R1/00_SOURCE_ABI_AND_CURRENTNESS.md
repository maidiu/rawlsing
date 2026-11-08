# Mechanism I source and ABI cut

Issue #785 governs this branch. GitHub returned protected PRE-MAIN
`7a5429ffbc48efd25e28c912da80c822e66bc182`. The proposed implementation branch
had no matching remote branch or managed worker binding at dispatch. P5 #775,
design #776 and reviewed P6 #779 remain open and unmerged. P6 head
`69987ef2741e6f90daede0e9e397aae0ac8e6b0b` is comparator evidence. The
implementation starts from protected P4, P3 and P2. Git CLI received HTTP 403
for remote ref reads. The GitHub connection verified the live protected ref.

| Authority or producer | Actual ABI at protected cut | Mechanism I connection |
|---|---|---|
| P4 encounter `WORKER_RETURNS/SOROK-P4-FIRST-FULL-MPC-R1/run_p4.py` | `open_owner(root)`, `act(owner, ledger_file, ledger, args)`, `surface(owner, ledger)` | Existing cold encounter and perception consumer. Opening binds the owner tool affordance before publication. General foreground targets and historical DepthRead remain pending. |
| P2 `developmental_recursion/p2_owner.py` and S45–S47 product fan-in | `load_p2().start(root)`, `.open(root)`, `fanin.session` | Existing branch, clock and actual event source. |
| Received S45–S47 vendor `r30a/first_session.py` | `world()`, `event(event_id)`, `read_root()`, `user_perceived_ids()`, `travel(location)` | Committed parent lookup. Inspection visibility and independent actor access remain separate. |
| Received vendor `bp4/product.py` and `bp4/store.py` | `_checkpoint(branch_id, clock, world, actors=None)`, `store.checkpoint(branch_id, clock, state)` | Same SQLite world checkpoint contains target and outbox. `BEGIN IMMEDIATE` serializes the read/modify/write against that store. |
| P3 `p3/p3_owner.py` and `p3/state_store.py` | `P3Owner.snapshot()`, `owner.store.head()` | Existing state references only. Historical actor links need an exact readset and access proof before admission. |
| Historical world/source law `865b5b01e1a27e99020cf2bb389af8cd4c874b57` | Sorok 51/60/61/70/80/87 | World truth, disclosure, root fork and historical impact remain separate. Protected PROGRAMMA front door determines receiving status. |

First checkpoint proof: `rawlsing_next/tests/test_sorok_history_owner.py` uses
actual P2 fan-in travel and its committed event. It exercises rollback after
checkpoint insertion, rejected unadmitted parents, conflicting surfaces,
idempotent enqueue and cold reopen. The test supplies a structured foreground
assertion. The live foreground and provider are pending and this test does not
establish their acceptance.

The outbox now persists a bounded running attempt in the same checkpoint.
A separate reopened owner can recover an expired attempt. A superseded lease
cannot save a result. A changed world snapshot marks the attempt stale.
A current candidate is durable in the outbox and remains separate from
admitted target material.

The existing P4 `surface(owner, ledger)` now reads committed surface facts
at the observer's current location when the source occurrence was perceived.
It omits outbox contents and the producer's referent key. The integration
test calls the real P4 surface after movement and verifies that leaving the
location removes the target from the view. Historical DepthRead and the
foreground producer still require integration.

P4 opening now calls `HistoricalWorld.capture_visible_tool_resource()`
before taking the ledger antecedent snapshot. It reads the exact current
owner resource and a perceived arrival or movement at that location within
the same transaction. The target denotes the coarse resource affordance
already reported by P4. The owner does not currently identify an individual
tool. The integration test asserts the opening output, durable deduplication
after reopen, and location-sensitive surface reads.

The bounded dependency evaluator is received from worker commit
`50e50d6b8dcfb86939c9a54f4e355c8ffe2c206c`. Its updated group logic accepts
occurrence parents only from the same group or an admitted parent group.
The world adapter independently restricts actual writes to H0 typed
physical facts and exact owner refs. Historical, external and actor effects
still require their respective admission paths.

A leased job now carries a sealed packet derived from its target, committed
event and current world readset. In the sourcefree test, a mock candidate
passes the evaluator, writes one compatible fact and refuses a contradictory
surface claim. A real cold `run_p4.py inspect-particular` call reads the fact
via a committed and perceived inspection event. P4 verifies the ordinary
foreground and actor witness on cold reopen, allowing the history checkpoint
to advance while preserving the mismatch refusal for changes outside that
resource. Actual model use and the independent actor activity reader remain
pending.

## PROGRAMMA_DELTA · Historical chronology

Issue #785 and the Mechanism I historical admission seam receive OpenCode
worker `ses_e52a51c43ffeuVe7ZZhNcga5YP`'s
`codex/sorok-mechanism-i-historical-chronology-20261108-r1` at
`586a34d2d6d619d444a8fecb2ad4682e571c0a77`. The existing Sorok world owner
remains the source of event identity and clock. This is HQ-verified sourcefree
engineering. Independent review and protected receiving are pending.

A new lease now binds the committed occurrence's exact event ref and clock
into `SOROK_HISTORY_ADMISSION_PACKET@1`. The first consumer is
`admission.evaluate` through `HistoricalWorld.commit_candidate`. Older
persisted packets keep their original digest inputs. The evaluator can reject
late parents, contradictory condition or custody and changes to closed
effects. Missing owner material is held. The live packet binds the occurrence
time and target. Condition and custody evidence in the evaluator tests is
controlled. The world commit remains scoped to H0 physical facts.

The worker's 18 admission tests include a valid H1 evaluator case and its
late-parent, contradictory custody and closed-effect negatives. These cases
qualify the validator and do not grant H1 world writes. Live provider and
independent review were not run for this cut. Independent activity consumption
and recurrent demand creation are the next executable seams.

The P4 CLI now wakes one background history invocation after a successful
opening or particular inspection, when a history endpoint and model are
explicitly configured. The child consumes the existing outbox via
`run_history_worker` and `runtime.run_once`. The same P4 foreground lock
serializes owner reads and writes. It is released during model inference.
The manual worker command can recover durable jobs after interrupted wakeup.
Tests verify the invocation follows the foreground save and lock release,
absent configuration skips the wake, and the guard is open during inference.
The launch proof uses an injected process starter. Live model execution and
independent review remain unverified.

### P4 background process and HTTP transport evidence

The P4 opening, automatic worker process, HTTP request, owner admission and
cold inspection now run together in
`test_p4_wake_completes_through_a_mock_http_endpoint`. The one-request loopback
fixture returns controlled material. The test reads the durable owner receipt
and checks that a separate inspection reads the exact admitted fact ID.
The endpoint is a transport fixture. Live model proof remains
`LIVE_PROVIDER_NOT_RUN`.

The HTTP adapter now bounds response bytes before JSON decoding. Oversized
responses receive `RESPONSE_LIMIT_EXCEEDED` and no candidate. This caps the
transport allocation even when an endpoint ignores the output-token request.
