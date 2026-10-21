# R30A first-neighbor session — runnable local CLI

**Grade:** `TEST_ONLY_SOURCEFREE_R30A_FIRST_NEIGHBOR_PRODUCT_NOT_NATIVE`  
**Source:** immutable R29P actor/product at `001b506fa26ae879ff5b6e57138fc2696e12b538`  
**Runtime:** Python 3.11, standard library + SQLite + pytest; no external model call.

## What this is

A local, persistent first-session product over the actual R29P A/B actor lives and C12/M6 product. The user is a visitor `U`; the neighbor is actor A (repair worker); actor B is A's independent co-worker (finisher). The product supports:

- invitation/primer and portal entry into an already ongoing workshop life;
- `SAY`, `DO help`, `DO inspect`, `TRAVEL`, `ATTEND`, `WAIT`, `LEAVE`, `RETURN`;
- a natural scene end when A's shift/market obligation presses;
- an outside-portal local message channel only when A actually grants one;
- independent B offscreen activity at clock 40;
- a later A message only when a channel exists and A is available;
- cold reopen of the same persisted C12 branch in a new process;
- branch fork for tests;
- exact event/utterance commitment before user-visible composition.

## Run

From the R30A return root:

```bash
export PYTHONPATH="$PWD"
export PYTHONDONTWRITEBYTECODE=1
python3 -m r30a.cli --state /tmp/r30a-neighbor start --scenario available
python3 -m r30a.cli --state /tmp/r30a-neighbor say "Hello. I just moved in."
python3 -m r30a.cli --state /tmp/r30a-neighbor do help
python3 -m r30a.cli --state /tmp/r30a-neighbor attend
python3 -m r30a.cli --state /tmp/r30a-neighbor ask-contact
python3 -m r30a.cli --state /tmp/r30a-neighbor wait 30
python3 -m r30a.cli --state /tmp/r30a-neighbor offscreen 30
python3 -m r30a.cli --state /tmp/r30a-neighbor messages
python3 -m r30a.cli --state /tmp/r30a-neighbor return
python3 -m r30a.cli --state /tmp/r30a-neighbor verify
```

Every command is a new process; after `start`, each command cold-reopens the same product/C12 branch.

### Refusal scenario

```bash
python3 -m r30a.cli --state /tmp/r30a-pressed start --scenario pressed
python3 -m r30a.cli --state /tmp/r30a-pressed say "Hello. Do you need a hand?"
python3 -m r30a.cli --state /tmp/r30a-pressed do help
python3 -m r30a.cli --state /tmp/r30a-pressed ask-contact
python3 -m r30a.cli --state /tmp/r30a-pressed wait 30
python3 -m r30a.cli --state /tmp/r30a-pressed offscreen 30
python3 -m r30a.cli --state /tmp/r30a-pressed messages
python3 -m r30a.cli --state /tmp/r30a-pressed return
```

`pressed` changes A's actual `free_hours` to zero in the session branch before the first encounter. It is a material availability variant, not a hidden mood or a different person.

## Tests

```bash
cd WORKER_RETURNS/SOROK-20261021-R30A-FIRST-NEIGHBOR-SESSION-R1
PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests -q
```

The executed run is **10/10 passed** (JUnit `evidence/junit/r30a.xml`). A 5-test R29P inherited integration subset is also **5/5 passed** (JUnit `evidence/junit/r29p_subset.xml`); the full 155 inherited suite is **NOT_RUN** here and is not double-counted.

## Important limits

- Actor speech/gesture realization is a **bounded deterministic local occurrence layer**, not an external language model. `LIVE_MODEL_NOT_RUN`.
- A's private material/psychological fields are never in the user surface; custody/`verify` commands are evidence tools and show source/custody internals.
- `first_session` is a product-shell branch of the actual R29P root. U is added to that branch; the original root remains A/B and is not rewritten.
- Native C12/ADP/CAN/C8/C11, production deployment, real contact IDs and A5 human evaluation are HOLD/NOT_RUN.
