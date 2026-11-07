# P4 sourcefree encounter

Run from the repository root with Python 3.11. The state directory is created on the first command. Keep it at the same path for later commands, as required by the received P2 owner.

```sh
cli=WORKER_RETURNS/SOROK-P4-FIRST-FULL-MPC-R1/run_p4.py
state=$(mktemp -d)
python3 "$cli" --state "$state" new
python3 "$cli" --state "$state" say 'I need a closer look at that edge.' --request-edge --request-id my-speech
python3 "$cli" --state "$state" inspect-edge '<invitation event ID printed by say>' --request-id my-inspection
python3 "$cli" --state "$state" view
```

The caller supplies the text and chooses whether to ask about the edge with `--request-edge`. Plain SAY commits the exact utterance without recruiting an inspection invitation. The explicit request remains separate from the Other's choice and from the caller's subsequent decision to inspect. `new --history imposed_plan` selects the contrasting actor antecedent. `new --history ''` selects valid-empty history. The history switch belongs to setup. It is unavailable to the actor and user during an encounter.

- `run_p4.py` initializes the received P2/P3 sourcefree scenario and commits P3 formation before it accepts a user action. It reads the P2 projection for visible footing and displays the arrival anchors and current encounter observations. Its public JSON contains the admission, whether the operation performed, the observed outward event when available, and the next choice.
- `speech.admit_speech` records exact SAY input. On admission it uses the received BP4 world event and perception writers. The internal receipt separates the attempt, admission, performed world event, and actor access.
- `response.read_response` verifies that the committed speech and actor perception match the receipt, then reads the received P3 `PsycheStore.query` and `projections.activate` using antecedent records. `response.express` commits a bounded sourcefree outward expression using P2 and requires a user perception before returning it. The expression reports an outward act without exposing the actor's mediator.
- After admitted speech the received S46 interval writer advances two clock units. In the positive witness its actual repair consumes the remaining material. Refused speech does not advance time or produce that repair. The joint response opens an inspection action tied to its event ID. Actual inspection is material no-change and returns control.
- The lock serializes P4 CLI commands. The internal ledger retains completed receipts and supports request-ID replay. An interrupted write with a pending ledger reservation requires reconciliation.

[evidence/cli-transcript.json](evidence/cli-transcript.json) contains the public surfaces and local process timings. [evidence/internal-receipts.json](evidence/internal-receipts.json) contains the sourcefree audit data, including the private side of the trace. The final public view equals the view after the second action on a cold reopen. The runtime invokes no model provider.

This is bounded sourcefree engineering. The outward responses use a test-only expression mapping for the workshop agenda. P4 does not issue a native C9 rule, create ADP memory, verify independent B ownership, operate S14 rights, or establish human Gate4 or Gate5 evidence. Scientific issuance and protected integration remain with their respective owners.
