# SOROK I1 — sourcefree continuing-person joined integration

**Return:** `WORKER_RETURNS/SOROK-I1-CONTINUING-PERSON-R1`
**Base:** `750548ddbb9b4392a16ce93097b856f349e16182`
**Requested branch:** `agent/sorok-i1-sourcefree-continuing-person-joined-implementation-20261030-r1`
**Date:** 2026-10-30
**Host:** oldMac (macOS 13.7.8, x86_64)
**Harness/model:** OpenCode / `opencode-go/deepseek-v4.1-flash`

## Result

The first sourcefree continuing-person integration beyond BP2P4J is implemented
as `GuardedJoinedProduct`: the unchanged BP2P4J `JoinedProduct` with the BP4R
`GuardedC12Store` as its C12 reader. The same named acceptance assertion,
`bp2p4.assertion.joined_downstream_a0_a2_assertion`, now runs against the guarded
consumer, and all ten BP2P4J severance trials run against it unchanged.

The new downstream material distinction is B's source-owned offscreen market
work. B's cash moves `54 -> 56`, completed units `3 -> 4`, position
`workshop -> market`, free hours stay `13`, and material stock stays exhausted
at `0`. A's public `other()` view exposes completed units `4`, position
`market`, and the public work event, while keeping cash/material/free-hours
private. The event body records `cash_delta: +2` and `material_delta: -1`; the
world's material stock is zero before and after because the existing BP4
offscreen rule floors it at zero. This is a material/payment and position
distinction, not merely the existing `3 -> 4` completed-unit example.

A's own material repair path supplies a second material proof: material
`2 -> 0`, completed `4 -> 6`, cash `55 -> 59`, free hours `12 -> 10`, and a
third repair is refused with `MATERIAL_EXHAUSTED`.

## Verdicts

### Engineering

**PASS (local candidate).** 50 tests pass: 33 unchanged BP2P4J tests, 9
unchanged BP4R guard tests, and 8 new I1 guarded-consumer tests. Guarded episode
fork/cold branch, cold-process reopen, writer-schema refusal, all ten
claim-specific severance trials, material double-spend refusal, presence-gated
knowledge, and parent/child material invariance pass.

Residual engineering holds: BP2P4J's self-referential `c12_verify.py` is
unchanged and unused by the guard path; durable C9/C12 cold reopen is not
claimed; the external C12 anchor is absent.

### Scientific

**PARTIAL — bounded sourcefree evidence.** The guarded consumer is a real
downstream A0-A3 consumer of the committed BP2/C8/C9/E2 and BP4 C12 state, not a
dict fixture. The new B material fact is committed and survives cold reopen and
fork. It does not establish native personhood, B's original childhood or
casual life, a native B participant, or complete continuing-person identity.

### Authority

**HOLD — no adoption.** The return is TEST_ONLY sourcefree engineering. It
creates no C12 owner anchor, CAN/ADP issuer, Pyat structural position, native
A0-A5 participant, or PRE-MAIN merge. `verify_c12` reports authenticity and
completeness as `OWNER_ANCHOR_REQUIRED`. This return does not self-adopt or
self-review.

## What is new

| Surface | Change |
|---|---|
| `bp2p4/i1_product.py` | `GuardedJoinedProduct` subclasses `JoinedProduct`; only the C12 store is replaced with `GuardedC12Store`. |
| `bp2p4/assertion.py` | Additive `product_cls` parameter, default `JoinedProduct`; the acceptance checks are unchanged. |
| `bp2p4/severance.py` | Additive `product_cls` parameter threaded through trials; default behavior unchanged. |
| `run_guarded.py` | Cold-process CLI over `GuardedJoinedProduct`. |
| `tests/test_i1_guarded_consumer.py` | Eight new tests for the guarded consumer and material/recurrence evidence. |

## Executed evidence

Commands were run from `candidate/` with Python 3.11.3, pytest 9.1.1, SQLite
3.40.1.

| Command | Exit | Result |
|---|---:|---|
| `PYTHONPATH=$PWD python3 -m pytest -o addopts='' -q tests/test_joined_product.py tests/test_joined_security.py tests/test_joined_severance.py tests/test_source_closure.py` | 0 | 33 passed |
| `BP4R_C9_DIR=$PWD PYTHONPATH=$PWD python3 -m pytest -o addopts='' -q tests/test_bp4r_candidate.py` | 0 | 9 passed |
| `PYTHONPATH=$PWD python3 -m pytest -o addopts='' -q tests/test_i1_guarded_consumer.py` | 0 | 8 passed |
| `BP4R_C9_DIR=$PWD PYTHONPATH=$PWD python3 -m pytest -o addopts='' -q tests` | 0 | 50 passed |

Full commands, test names, cold replay, and negative results are in
`02_EXECUTED_POSITIVES_NEGATIVES_AND_COLD_REPLAY.md`.

## First real sourcefree consumer

`GuardedJoinedProduct` is the consumer. It runs the existing
`joined_downstream_a0_a2_assertion` with `product_cls=GuardedJoinedProduct` and
runs `run_all_severances(..., product_cls=GuardedJoinedProduct)`. The ordinary
`JoinedProduct` and the BP2P4J acceptance target remain the default.

## Limits and next owner decisions

1. **External C12 anchor absent.** The guard verifies content, fork prefix and
   writer schema, but cannot establish authenticity or completeness without an
   owner-issued anchor. `OWNER_ANCHOR_REQUIRED` remains.
2. **B cash is owner-only.** The owner material readout is explicitly
   `OWNER_TEST_ONLY`; A's public `other()` does not expose B's cash, material, or
   free hours. A public economic projection needs an owner decision.
3. **No new B behavior was invented.** The material distinction derives from
   the existing source-owned BP4 offscreen market event. B does not acquire a
   new source, childhood, casual relation, or native identity.
4. **C9 durable handoff not closed.** G17I2's bounded handoff and the BP4R C9
   writer gate pass, but durable C9/C12 cold reopen is not claimed.
5. **F1CR targetless adapter absent.** The repaired F1CR executable is not a
   committed tree source; no REFUSE/SILENCE targetless adapter is claimed.
6. **BP2P4J verifier residual.** `bp2p4/c12_verify.py` retains its
   self-referential upstream issue; the I1 consumer uses `GuardedC12Store` and
   does not treat the old verifier as an authorization source.

## Next lawful handoff

- Owner review of the B cash/public-material projection and C12 anchor policy.
- Owner decision on durable C9/C12 and the C9 R3B interface; no edge beyond the
  selected BP2P4J/C12 episode edge is asserted.
- Integration only after owner review; no automatic PRE-MAIN or PR mutation.
