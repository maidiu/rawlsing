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
