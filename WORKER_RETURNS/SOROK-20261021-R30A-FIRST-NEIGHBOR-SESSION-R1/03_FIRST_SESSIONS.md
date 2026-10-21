# First and later encounter receipts

## Available first session

Source: `evidence/session_available.json`; cold CLI transcript `evidence/cli_available.txt`.

Sequence actually executed:

1. User enters already-ongoing workshop scene; A and B are present.
2. User: `"Hello. I just moved in."` → exact A utterance `"Which side of the landing?"` bound at clock 10.
3. User `DO help` → A's actual free/material/tool state admits the repair; A performs a source-owned `REPAIR` event and says exactly `"Hold the near edge. I'll check the seam."`
4. `ATTEND` → no new actor-private truth; A already responded.
5. `ASK CONTACT` → A grants `landing_line`; this is an A C12 `CONTACT` occurrence, not a UI unlock.
6. `WAIT 30` → clock 40; A ends the scene because the market/light presses. B independently moves to the market and performs `OFFSCREEN_REPAIR` (completed units 4→5). The scene closes naturally.
7. Outside portal: `OFFSCREEN 30` → clock 70; A sends the later message `"The seam held. I'm at the market until six."` because a channel exists and A is available.
8. `RETURN` → same C12 person, same target/consumed identity; A says `"The seam held. You came back."`
9. `verify` → R26E qualified C12, 21 episodes / 11 world events / 16 checkpoints / 27 perceptions, OK.

The later B state is public and changed: `completed_units=5`, `position=market`, one public work event. The user did not command that activity.

Cold reopen: `evidence/cold_reopen.json` records the same target and consumed-state hash before/after a fresh `FirstSession.open`, with both verifications OK.

## Pressed / refusal first session

Source: `evidence/session_pressed.json`; CLI `evidence/cli_pressed.txt`.

- A's actual `free_hours` is zero in this branch.
- User `"Do you need a hand?"` → A: `"I can't take that on now. I have to finish."`
- `DO help` → refused; **no REPAIR event** exists.
- `ASK CONTACT` → A: `"Not yet. I don't know you."`; no channel.
- `WAIT 30` → A ends the scene: `"I have to go. The market closes."`
- B still performs independent offscreen work at clock 40.
- `OFFSCREEN 30` → **no message**; `MESSAGES` returns `NO_CHANNEL`.
- Attempted `MESSAGE` → typed `NO_CONTACT_CHANNEL` refusal.
- `RETURN` → same person, A says `"You came back."`; no manufactured warmth or contact.
- `verify` → 19 episodes / 10 world events / 14 checkpoints / 24 perceptions, OK.

## User early exit / offscreen life

Source: `evidence/session_early_exit.json`.

- User speaks, helps, asks contact, then `LEAVE` at clock 10.
- `OFFSCREEN 30` → B independently goes to market and completes a repair at clock 40; A's later message is lawfully sent at clock 40 because the channel exists.
- `RETURN` → same person, B public state changed; no reroll.

## Actor-owned inquiry

A quiet `ATTEND` before any A speech can trigger A's own question: `"You're looking at the seam. Can you see the gap?"` (`tests/test_r30a_first_session.py::test_quiet_attend_can_trigger_actor_owned_question`). It is not a narrator prompt; it is an A world event and C12 episode.

## What is not forced

- Help is accepted only when A's actual material/free/tool state admits it.
- Contact is granted only when A's actual availability and prior interaction support it.
- A may leave, refuse, end the scene, or decline contact.
- No message appears without a channel.
- No relationship score, trust meter, romance gradient, guilt hook or omniscient stats panel exists.
- Reentry is the same C12 person/history, not a new canned actor.

## Test count

`evidence/junit/r30a.xml`: **10/10 R30A tests passed**.
`evidence/junit/r29p_subset.xml`: **4/4 selected R29P inherited integration tests passed**. The full inherited 155 suite is **NOT_RUN** and is not counted as R30A proof.
