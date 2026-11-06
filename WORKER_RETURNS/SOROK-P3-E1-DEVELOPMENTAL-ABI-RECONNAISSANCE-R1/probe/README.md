# P3-E1 compatibility probe

This directory is a self-contained TEST_ONLY probe. It does not modify product code, original science, historical worker returns or protected PROGRAMMA.

## What it proves

- B1's existing SQLite CAN008 → CAN011 → persisted mediator → later reader chain can be driven through the received `DevelopmentOwner`/`BatchEngine` ABI.
- A byte-identical later event produces `joint_check:caretaker` after the mediator is stored and `inspect_alone:caretaker` in a journal-only control with no mediator.
- The mediator survives cold reopen; the later event reads it; removing it breaks the reader; exact restoration restores the result.
- Wrong root/actor/clock/source/rule-version/operation is refused before durable mutation.
- Operation ambiguity HOLDs instead of repeating an effect.
- The production zero-positive guard remains empty and returns `DENY_ZERO_EFFECT`.

It does **not** prove native CAN-008/CAN-011/ADP-016/ADP-017 science, a P2 actor-root psychological writer, or a generated native person.

## Run

From this directory:

```bash
python3 -B -m pytest -q -p no:cacheprovider test_b1_owner_adapter.py
python3 -B run_probe.py
```

`run_probe.py` also runs the adapter court in a subprocess and writes:

- `receipts/PROBE_RECEIPT.json` — host, git, source pins, positive/control, scaling, guard, pytest.
- `receipts/junit.xml` — JUnit.
- `source_pin.json` — B1/engine/probe hashes.

Expected current result: 9 passed; positive later action `joint_check:caretaker`; control later action `inspect_alone:caretaker`; production guard `DENY_ZERO_EFFECT`.

## Files

| File | Role |
|---|---|
| `b1_owner_adapter.py` | `DevelopmentOwner` adapter over pinned B1 `bfirst.py` |
| `test_b1_owner_adapter.py` | 9-test compatibility/negative/severance court |
| `run_probe.py` | scenario execution, scaling, guard, pytest and receipt writer |
| `vendor/B1/bfirst.py` | byte-identical pinned B1 copy (SHA-256 `478b9897…`) |
| `source_pin.json` | exact commit/blob/hash pins |
| `receipts/` | generated evidence |

## Important limits

- B1's `situated_plan_comparison` / `scoped_plan_mediator` rules are authored `PROVISIONAL_MODEL_HYPOTHESIS`, not CAN-008/CAN-011 issuance.
- The adapter's `TEST_ONLY_B1_V3MS_MEDIATOR` consequence is test-only engineering.
- The probe does not touch `rawlsing_next/v3_psepf_zero_positive_guard.py` or any production registry.
- The adapter's default initial state is B1's default `initialize(prehistory())`. If a DB is created with a different B1 prehistory, reopen it by passing the same `initial`; otherwise the adapter refuses the source-identity mismatch.
- Full P2, B3A, HQ300, M01 and BP2P4J owner tests are not run here; inherited results remain historical evidence.
