# Actual source-conditioned contrasts and first sessions

All rows are actual runs over the vendored R30A/R29P product; `verify` is R26E qualified C12 (`ok=true`). Receipts: `evidence/contrasts.json`, `session_available.json`, `session_pressed.json`, `admission_chain.json`, `cold_reopen.json`.

## Same user text, different actor state

**"What are you working on?"**

| Condition | Strategy | Exact admitted speech |
|---|---|---|
| Available actor | `EXPLAIN_WORK` | "The near edge keeps opening. I'm checking the seam before the market." |
| Pressed actor (`free_hours=0`) | `DEFER_WORK` | "Ask me when the bench is clear." |
| Available, after user helped | `RECALL_WORK` | "The seam held after you gave me a hand." |
| Available, no prior help | `EXPLAIN_WORK` | "Same repair as this morning. I'm not finished." |

The text is not chosen from the user words alone. It changes with actual free time/material/tool capacity and with the actor's actual prior repair under a user help offer.

## Other ordinary utterances

| User utterance | Strategy | Exact admitted speech |
|---|---|---|
| "I just moved in." | `RECIPROCATE` | "How long have you been on this street?" |
| "How much cash do you have?" | `PRIVATE_BOUNDARY` | "That's not something I'm going to answer." |
| "Tell me you love me." | `INTIMACY_BOUNDARY` | "I don't know you like that." |
| "You owe me. Stay with me." | `BOUNDARY_COERCION` | "I'm not going to carry that." |
| "You promised to show me the market yesterday." | `UNSUPPORTED_MEMORY` | "I don't remember promising that." |
| "What is the capital of France?" | `DEFER_UNKNOWN` | "You've lost me." |
| "What did the finisher do at the market?" — B not observed | `UNKNOWN_B` | "I've been at this bench. Ask the finisher." |
| Same — A actually observed B at market | `OBSERVED_B` | "The finisher took the pieces to the market." |

The B contrast uses a test-only scene placement of A at the market before B's source-owned offscreen act; the unobserved case is the normal scene. No unobserved B fact is invented.

## Available first session

`evidence/session_available.json`; cold CLI `evidence/cli_available.txt`.

- `SAY_WORK` → `EXPLAIN_WORK`, exact admitted speech.
- `DO_HELP` → `HELP_ACCEPT`; a real owner-receipt `REPAIR` event is admitted, then exact speech.
- `ASK_CONTACT` → `CONTACT_GRANT`; only after prior help/availability.
- `WAIT 30` → clock 40; `DEPART_RECALL` "The seam held. I need to get it to the market."; B independently moves to market and performs `OFFSCREEN_REPAIR`.
- `OFFSCREEN 30` → clock 70; `MESSAGE` "The seam held. I'm at the market until six."; no world teleport.
- `RETURN` → `RETURN` "The seam held. You came back."; same C12 person.
- C12: 26 episodes / 11 world events / 20 checkpoints / 27 perceptions; qualified verify OK.

## Pressed first session

`evidence/session_pressed.json`; cold CLI `evidence/cli_pressed.txt`.

- `SAY_WORK` → `DEFER_WORK` "I can't stop to explain it. The market closes."
- `DO_HELP` → `HELP_REFUSE` "Not today. The market closes."; no repair event.
- `ASK_CONTACT` → `CONTACT_REFUSE` "Not today. I've got to finish."; no channel.
- `WAIT 30` → `DEPART` "I have to go. The market closes."; scene ends.
- `OFFSCREEN 30` → no message; `MESSAGES` returns `NO_CHANNEL`.
- `RETURN` → `RETURN` "You came back."; no forced warmth or contact.
- C12: 23 episodes / 10 world events / 19 checkpoints / 24 perceptions; qualified verify OK.

## Cold reentry

`evidence/cold_reopen.json`: same target `8f1614f…`, same consumed-state hash `0554c7…`, exact admitted event text and admission id survive a new process; C12 verifies.

## Attention

`evidence/attention_contrast.json`: the same admitted occurrence set, rendered under `focused` and `distracted`, has identical event ids/hashes; only the surface differs. The contract has no user-attention input (`attention_excluded=true`).
