# R31E — actor-conditioned first-neighbor CLI

**Grade:** `TEST_ONLY_SOURCEFREE_R31E_ACTOR_EXPRESSION_NOT_NATIVE`  
**Source:** immutable R30A `ce0dfc67…` over R29P `001b506f…`  
**Runtime:** Python 3.11, standard library, SQLite, pytest; no external model call.

## What is new over R30A

R30A's `say()` selected fixed sentences from a small keyword taxonomy. R31E adds:

1. `R31E_ACTOR_REALIZATION_CONTRACT@1` compiled from actual actor state, world, M6 knowledge, recalled user utterances, material/time/obligation and B observation;
2. a bounded **structured candidate grammar** (60 templates, strategy families) that proposes multiple lawful candidates;
3. semantic admission that re-renders the template, checks actor knowledge/currentness/world facts/private-token exclusions, then binds one exact speech/gesture/action/silence/message as a C12 + world occurrence;
4. `R31E_EXPRESSION_PORT@1`, versioned for future R31J intake.

The actor proposal is still deterministic TEST_ONLY. It is **not** open-ended natural-language understanding, a live LLM, or a claim of human psychological fidelity.

## Run

```bash
cd WORKER_RETURNS/SOROK-20261021-R31E-ACTOR-EXPRESSION-FIRST-NEIGHBOR-R1
export PYTHONPATH="$PWD" PYTHONDONTWRITEBYTECODE=1
python3 -m r31e.cli --state /tmp/r31e-neighbor start --scenario available
python3 -m r31e.cli --state /tmp/r31e-neighbor say "What are you working on?"
python3 -m r31e.cli --state /tmp/r31e-neighbor do help
python3 -m r31e.cli --state /tmp/r31e-neighbor say "What are you working on?"
python3 -m r31e.cli --state /tmp/r31e-neighbor ask-contact
python3 -m r31e.cli --state /tmp/r31e-neighbor wait 30
python3 -m r31e.cli --state /tmp/r31e-neighbor offscreen 30
python3 -m r31e.cli --state /tmp/r31e-neighbor messages
python3 -m r31e.cli --state /tmp/r31e-neighbor return
python3 -m r31e.cli --state /tmp/r31e-neighbor verify
```

Each command is a new process and cold-reopens the same C12 branch. `pressed` is the material-availability contrast:

```bash
python3 -m r31e.cli --state /tmp/r31e-pressed start --scenario pressed
python3 -m r31e.cli --state /tmp/r31e-pressed say "What are you working on?"
python3 -m r31e.cli --state /tmp/r31e-pressed do help
python3 -m r31e.cli --state /tmp/r31e-pressed ask-contact
```

## Tests

```bash
PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests -q
```

Actual: **15/15 R31E tests**, **10/10 R30A baseline**, **5/5 selected R29P inherited tests**. Full inherited 155 is **NOT_RUN** and not counted.

## Do not mistake

- `LIVE_ACTOR_MODEL_NOT_RUN`; no provider identity/cost/latency is claimed.
- No real human A5 study, native C11/C12, ADP/CAN, Pyat N11/N12, or production deployment.
- Actor-private fields are in the actor-side contract but never in the user surface.
- All candidate text is a bounded template with source-checked slots; it is not free-form model prose.
