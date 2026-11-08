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
| P4 encounter `WORKER_RETURNS/SOROK-P4-FIRST-FULL-MPC-R1/run_p4.py` | `open_owner(root)`, `act(owner, ledger_file, ledger, args)`, `surface(owner, ledger)` | Existing cold encounter and perception consumer. Product introduction and DepthRead still need wiring. |
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
