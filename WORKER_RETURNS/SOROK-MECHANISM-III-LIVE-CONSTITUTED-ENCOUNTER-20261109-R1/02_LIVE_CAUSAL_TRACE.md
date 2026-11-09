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
