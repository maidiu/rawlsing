# Cold replay and negatives

A real subprocess exits with status 73 inside the sourcefree transducer,
after the existing P4 owner has committed the user SAY and before any
actor move. A second OS process retries the exact request and receives
`P4_PENDING_OPERATION_REQUIRES_RECONCILIATION`. The pending bytes,
complete P2 event list, clock and P3 head remain unchanged. Exactly one
copy of the user SAY exists. This verifies a cold explicit hold at the
tested interruption point.

The same-world P6 test restores one exact initial state at the same
path and changes only private bench versus mug attention. The user
detail changes, while the admitted speech, transducer inputs, uptake
and actor event are identical. Moving the user to the living room
instead commits SAY without Nadia's perception receipt. No transducer
call or response follows.

The mediator test additionally refused a proposal with a mismatched
event hash and one with an extra authority field. An uncertain
hypothesis held before recruitment. These are focused proposal-boundary
observations rather than complete hostile utterance coverage.

Commands and outcomes for qualified cases are in
[the case matrix](04_CASE_MATRIX.jsonl).

A separate P6 test committed two non-edge SAY turns and retried each
in a new OS process, including the first turn after the second was
committed. The retry transducer would raise on invocation. Both
retries returned admission with the current clock, and the P4
ledger bytes, exact P2 events, clock, and P3 head stayed identical.
The test checks durable idempotence and does not assert replay of
the original P6 narration.

The combined P4 response and P6 house suite passed 8 tests in 236.21s
on runtime cut `29c1a7260dc02422f2082a2a3f4b547ca0a10d28`.
A later focused run passed the exact mediator severance/restoration
and foreign-counterpart control together. The altered counterpart
is refused before a P3 query, and the accepted scope is bound to the
existing owner formation plan hash. This control covers one part of
the broader cross-root/branch/actor case.

## Joined regression receipt

At code cut `0455726999350fd66d68ee637ee9299df825dbb8`, the
combined P4 response, P5 experience, P6 house and bounded-expression
suite passed 43 tests in 520.20s.

```text
python -B -m pytest -q -p no:cacheprovider --tb=short \
  WORKER_RETURNS/SOROK-P4-FIRST-FULL-MPC-R1/test_response.py \
  WORKER_RETURNS/SOROK-P5-CONTINUOUS-EXPERIENCE-R1/test_experience.py \
  WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/test_house.py \
  rawlsing_next/tests/test_render_bounded_expression.py
```

This is a previous exact-cut regression receipt. Later changes to
snapshot checks and focused tests retain their own receipts.

At `279202570a9a9e028fc40152b29aa24186d79c34`, the same suite plus
the received P4 speech test passed **44 tests in 473.45s**. The
following return commits only change evidence documents.

```text
python -B -m pytest -q -p no:cacheprovider --tb=short \
  WORKER_RETURNS/SOROK-P4-FIRST-FULL-MPC-R1/test_response.py \
  WORKER_RETURNS/SOROK-P4-FIRST-FULL-MPC-R1/test_speech.py \
  WORKER_RETURNS/SOROK-P5-CONTINUOUS-EXPERIENCE-R1/test_experience.py \
  WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/test_house.py \
  rawlsing_next/tests/test_render_bounded_expression.py
```
