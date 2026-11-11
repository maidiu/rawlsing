# P5 workshop encounter

Run the sourcefree encounter from the repository root. Keep the state directory at its original path for cold reopen.

```sh
cli=WORKER_RETURNS/SOROK-P5-CONTINUOUS-EXPERIENCE-R1/run_p5.py
state=$(mktemp -d)
python3 "$cli" --state "$state" new
python3 "$cli" --state "$state" say 'Could we look at this edge?' --request-edge
python3 "$cli" --state "$state" inspect-edge '<invitation ID from the response>'
python3 "$cli" --state "$state" attend
python3 "$cli" --state "$state" attend
python3 "$cli" --state "$state" view
```

- **SAY** carries the caller’s exact words. `--request-edge` explicitly asks about the work and can prompt a different response from Nadia. An observed invitation returns at its own clock with the material untouched. Use its ID to accept it, or speak again to redirect the encounter.
- **INSPECT** examines the work independently when no invitation is pending. **ATTEND** uses the received local perception action. An admitted examination occupies three workshop ticks. Ordinary speech and attention occupy one. Pass `--thorough` to either inspection command to delegate two three-tick work periods. The received S46 interval can carry Nadia’s repair during those actions. If material is exhausted, the interval can pass quietly.
- **ORIENT** registers interest in an occurrence the user perceived. Pass an event ID from the narration. The reader needs several distinct choices before it favors a channel. It persists those choices in `p5_gaze.json` and uses them only to select public detail. A direct perceived reply stays audible. `view` reopens the world and renders the same surface without advancing time.

The P4 owner and receipt ledger remain the authority for conduct, clock, history, and state. P5 feeds action duration to the received S46 producer and records co-presence at the moment of a repair. Narration reads the resulting S45 surface, with separate inputs for eligible occurrence IDs, demonstrated attention and a decision boundary. An upstream materializer can supply occurrences to the world reader through that boundary without supplying user preferences to the actor.

The workshop uses the received integer clock. These spans distinguish a brief act from an examination within the fixture. They have no calibrated wall-clock conversion. The default P5 seed uses the received S44 sampler to establish two remaining units after prehistory. In the example Nadia repairs one unit during inspection, another while the caller attends, and has no material action on the second ATTEND. The narrator uses only perceived speech and the observable descriptions carried by the fixture.
