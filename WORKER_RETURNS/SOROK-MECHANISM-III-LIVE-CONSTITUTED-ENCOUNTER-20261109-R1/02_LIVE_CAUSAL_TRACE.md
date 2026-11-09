# Mechanism III live causal trace

## Received baseline — content-bearing edge absent

Protected cut: `256d46bf425cc37e114465cddbe3c60e535766ab`.
Commission: `f65a0b3c0a4318136421af3eb69dc3e2b234355d`.
Local Codex shell, existing Python test environment, sourcefree execution.

Two independently opened P4 states used the same default recognized-plan
history and seed. For each, a separate process invoked
`run_p4.py --state <state> new`, then another invoked
`run_p4.py --state <state> say "<utterance>" --request-id baseline`.
The utterances were “Could we check the edge together?” and “I think I
will leave you to your work.” Neither supplied `--request-edge`.

Reading the committed turn from `p4_receipts.json` produced the same
tuple for both, in the order request flag, actor access, uptake status,
uptake mode, outward expression present:

```text
(False, True, 'PERCEIVED_NO_INSPECTION_REQUEST', None, False)
(False, True, 'PERCEIVED_NO_INSPECTION_REQUEST', None, False)
```

The actual producer is P4 `speech.admit_speech`, called by
`run_p4.act`. `response.read_response` checks the performed event
against the session and the actor access receipt against P2 perceptions.
The non-edge branch returns before P3 store query and
`projections.activate`. Thus both actual utterances reach the actor
but neither reaches content-bearing P3 recruitment. On the existing
edge path, `response.express` uses P2 `_actor_say` and S45 projection
conditioned on public perception. P6 `experience` routes SAY through
the same P4 `act` via P5 and reads the resulting public surface before
applying private presentation state.

This is the received-path negative, not a Mechanism III implementation
or a native semantic authority result.

## Sourcefree first consumer

The P6 `experience` and P4 `act` entry points can accept an explicit
sourcefree transducer. P4 calls it only after matching the committed SAY
and Nadia's perception receipt. The transducer gets event identity and
exact utterance, with no user gaze, private actor state, or authority
write interface. It returns bounded speech-move hypotheses, evidence
spans and a referent. A proposal is data and does not admit a claim.

For the supported current-edge request, the P4 reader uses the existing
P3 store and activation projection. It retains the activation result
internally and selects only a unique eligible received mode. Uncertain
or conflicting proposals hold. An unrelated utterance can return valid
empty. P2 performs the authorized fixture expression and S45 supplies
the public observation. No actor memory or belief is written.

A focused P6 run executed two actual SAY turns through the normal
experience entry point, with one publicly projected P2 response and a
subsequent valid-empty turn. Reopening and retrying the second request
left the persisted P4 receipt bytes unchanged and did not call the
transducer again.

```text
python -B -m pytest -q -p no:cacheprovider WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/test_house.py -k live_recruitment
1 passed, 1 deselected in 31.94s
```

The transducer in that run was a local fixture. The normal CLI has no
configured live transducer, semantic generality is unproved, and native
M6 semantic-plan authority remains held. The full court is outstanding.

## Exact mediator severance and restoration

A focused test held the committed, actor-perceived non-edge SAY and its
semantic proposal fixed. The real P3 query initially returned one
eligible joint-check mediator. A test-only SQLite savepoint removed
that exact row by record ID and hash. The same first reader then
returned no mode and no longer cited the mediator hash. Rolling back
restored the original complete uptake receipt, after which the
existing P2 writer committed the expression and S45 returned its
public observation. The speech event and P3 head were unchanged.
This is an in-process source fault, separate from cold recovery.

```text
python -B -m pytest -q -p no:cacheprovider WORKER_RETURNS/SOROK-P4-FIRST-FULL-MPC-R1/test_response.py -k loses_and_recovers
1 passed, 2 deselected in 13.80s
```

## P6 and S46 share one timeline

The focused two-turn test passed in 45.80 seconds. The joint-check
invitation returned at the opening clock without an interval. The
next nonmaterial SAY returned valid empty and advanced exactly one
tick through the existing P5/S46 pacing path. Its interval receipt
matches the one new S46 issuance by ID and hash, and matches the SAY
clock and the P4 root and branch. Replaying either request in a new
process leaves events, issuance list, clock and P3 head unchanged.

The Mechanism I historical resource was absent before and after.
A live Mechanism I outbox is unavailable on this cut, so the joined
non-dispatch case remains held.

## Joined runtime witness

At exact code revision `0455726999350fd66d68ee637ee9299df825dbb8`,
a local Python process called P6 `experience(new)` and then
`experience(say)` with request ID `witness`, `request_edge=False`
and the sourcefree proposal for “Could we check the edge together?”
It read the ordinary persisted P4 turn and asserted that P6 narration
cited the exact committed outward event.

| Boundary | Observed identity |
| --- | --- |
| P2 root | `d747d2c208fb0fe3610c9f08d728d5f358758feee6be5164e07475e4431950c6` |
| Actor, branch, clock | `TEST_ONLY_BP1_R26V_ACTOR_A`, `first_session`, 248 |
| SAY event | `TEST_ONLY_BP4_WORLD_EVT_ef3c0a4b4396e208689c3e55f6159460c2d6e46d6580a3cacceec4bdd1ad88f6` |
| SAY hash | `40d614d28896516f5ef75d7af620b99b5857d4a3a32daab3a1b2498425dbce53` |
| P2 perception | Actor `A`, channel `co_present`, clock 248, exact SAY ID |
| Semantic proposal | `01b8c178e7b7db8e6a29696b3a73d73fac1e032ecb00fd1ec88ddeeb108b82c0` |
| P3 recruitment context | `adcd7bafe0d9d669d5850299b701e256e3ec8952482168520d4d79ad0a87d776` |
| Eligible mediator | `5d5be13eec113fe97bedb56ae17fa5dd248af6b5f5903d83276a06619c06769e` |
| Mediator hash | `c59f76952cbe49354c2e8dbb0a0a9a3f7f87fec32cedb9cf252efc844396ce7d` |
| P2 outward event and S45/P6 public source | `TEST_ONLY_BP4_WORLD_EVT_af530b5bc40f026a76d95795c8016ac6a78208613d49599cf2384c1e0a9b0d64` |
| Outward hash | `a8a713c63a6188051e6a08f46acdc8e553c747281dcc30398dbf3db576443571` |

The imported call chain was P6 `experience` → P4 `act` →
`speech.admit_speech` → `response.read_response` → P3
`PsycheStore.query` and `projections.activate` → P2
`_actor_say` → S45 `project_event` → P6 narration.
