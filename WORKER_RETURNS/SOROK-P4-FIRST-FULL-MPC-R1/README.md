# P4 sourcefree encounter

Run from the repository root with Python 3.11. The state directory is created on the first command. Keep it at the same path for later commands, as required by the received P2 owner.

```sh
cli=WORKER_RETURNS/SOROK-P4-FIRST-FULL-MPC-R1/run_p4.py
state=$(mktemp -d)
python3 "$cli" --state "$state" new
python3 "$cli" --state "$state" say 'I need a closer look at that edge.' --request-edge --request-id my-speech
python3 "$cli" --state "$state" inspect-edge '<invitation event ID printed by say>' --then-wait --request-id my-inspection
python3 "$cli" --state "$state" view
```

The caller supplies the text and chooses whether to ask about the edge with `--request-edge`. Plain SAY commits the exact utterance without recruiting an inspection invitation. The explicit request remains separate from the Other's choice and from the caller's subsequent decision to inspect. `new --history imposed_plan` selects the contrasting actor antecedent. `new --history ''` selects valid-empty history. The history switch belongs to setup. It is unavailable to the actor and user during an encounter.

- `run_p4.py` initializes the received P2/P3 sourcefree scenario and commits P3 formation before it accepts a user action. It reads the P2 projection for visible footing and displays the arrival anchors and current encounter observations. Its public JSON contains the admission, whether the operation performed, the observed outward event when available, and the next choice.
- `speech.admit_speech` records exact SAY input. On admission it uses the received BP4 world event and perception writers. The internal receipt separates the attempt, admission, performed world event, and actor access.
- `response.read_response` verifies that the committed speech and actor perception match the receipt, then reads the received P3 `PsycheStore.query` and `projections.activate` using antecedent records. `response.express` commits a bounded sourcefree outward expression using P2 and requires a user perception before returning it. The expression reports an outward act without exposing the actor's mediator.
- A perceived invitation returns control at its own clock with material intact. The caller can inspect using the invitation event ID. Plain inspection leaves material and time unchanged. The optional `--then-wait` explicitly lets two workshop clock units pass **after** inspection. In the positive witness the received S46 interval performs a repair during that wait. Invalid invitation tokens and refused speech perform no interval. The existing admitted-speech timing applies when the response offers no inspection.
- The lock serializes P4 CLI commands. The internal ledger retains completed receipts and supports request-ID replay. An interrupted write with a pending ledger reservation requires reconciliation.

[evidence/cli-transcript.json](evidence/cli-transcript.json) contains the public surfaces and local process timings. [evidence/internal-receipts.json](evidence/internal-receipts.json) contains the sourcefree audit data, including the private side of the trace. The final public view equals the view after the second action on a cold reopen. The runtime invokes no model provider.

This is bounded sourcefree engineering. The outward responses use a test-only expression mapping for the workshop agenda. P4 does not issue a native C9 rule, create ADP memory, verify independent B ownership, operate S14 rights, or establish human Gate4 or Gate5 evidence. Scientific issuance and protected integration remain with their respective owners.

## Control-return and continuing-world scope (2026-11-07 receiving clarification)

The sourcefree P4 decision law is **NOT** "every utterance freezes the world" and is **NOT** "WAIT is the only way time advances." The ordinary action surface persists while the Other acts. After an outward `private_check` ("Give me a moment to check this edge myself") or `inspect_alone` ("I'll check the edge first"), the separately received S46 objective interval may proceed without a new caller command where no unprovided user judgment is being substituted. The tests demonstrate this existing, bounded continuation: in the imposed/empty P3 histories the first spoken response is distinct, no invitation exists, and the ordinary base choices remain available even as the received S46 model changes time/material. **Do not represent this as the user choosing passivity, adopting a particular thought, or granting a blank check for arbitrary narrative time jumps.**

The `joint_check` exception is narrower: A says "Come look at this edge with me", which directly offers an immediate, material-relevant inspection **before** the repair changes the edge. That exact response creates a user-choice boundary. The invitation returns at clock 230 with material 1 and no ACTUAL interval. Plain `inspect-edge` takes place at 230 and has no material/time effect; explicitly selected `--then-wait` runs the sourcefree S46 interval only afterward. Refused or spent invitations cannot authorize that interval.

A **later continuous situated-experience implementation** should narrate only publicly perceptible, source-bound activity and salience while the autonomous world proceeds; do not counterfeit a privately chosen user interpretation or fabricate the user's remembered associations. User-authored SAY/DO/ATTEND/INSPECT/interruption must be possible within ongoing actor activity with meaningful time/perception/physical-access consequences. The simulated world must keep advancing independently where justified; an ordinary user need not request `WAIT` to permit time's existence. **This P4 CLI does not yet deliver such a general continuous narrative or attention scheduler.** Its current first-consumer scope is the bounded, cold-reopenable D002 MPC-1..7 sourcefree mechanism with a workshop fixture and two user-selected speech/inspection controls; `--then-wait` is a special proof control, not the intended everyday UX or a mandatory universal gate.

The later re-review objection to *all* non-joint observed speech yielding background interval execution is therefore rejected as **overbroad**; the genuinely actionable invitation must return early, which the independently re-reviewed runtime already does. This distinction is a D002 control-return interpretation, not new original scientific issuance, native actor authority, independent third-party GitHub approval, or evidence of actual human usability. The original science/native/B/S14/Gate4/Gate5 holds remain.
