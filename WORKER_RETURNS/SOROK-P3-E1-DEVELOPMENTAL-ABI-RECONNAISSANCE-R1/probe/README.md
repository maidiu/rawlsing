# P3-E1 compatibility probe

This directory is a self-contained TEST_ONLY probe. It does not modify product code, original science, historical worker returns or protected PROGRAMMA.

## What it proves

- B1's existing SQLite CAN008 → CAN011 → persisted mediator → later reader chain can be driven through the received `DevelopmentOwner`/`BatchEngine` ABI.
- A byte-identical later event produces `joint_check:caretaker` after the mediator is stored and `inspect_alone:caretaker` in a journal-only control with no mediator.
- The mediator survives cold reopen; the later event reads it; removing it breaks the reader; exact restoration restores the result.
- Wrong root/actor/clock/source/rule-version/operation is refused before durable mutation.
- Operation ambiguity HOLDs instead of repeating an effect.
- The production zero-positive guard remains empty and returns `DENY_ZERO_EFFECT`.
- Each event reports a new TEST_ONLY mediator only when that operation committed a new target and matching transition; later use of an existing mediator and journal-only responses have explicit no-new-mediator grades.
- The `journal_only` operating mode is stored in `b1_owner_meta` and verified at every snapshot/operation. A mode-flipped cold reopen refuses rather than changing future transitions under unchanged owner identity.

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

Historical submitted receipt: 9 passed on the earlier candidate; the two-defect repair now contains 12 test functions (13 pytest cases including two mode variants) and **requires fresh S2 execution**. Do not treat the previous `receipts/PROBE_RECEIPT.json` / JUnit as the new-head result. Expected later action `joint_check:caretaker`; control later action `inspect_alone:caretaker`; production guard `DENY_ZERO_EFFECT`.

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
- On cold reopen, pass the original `journal_only` boolean explicitly for journal-only stores. Reopening them with the default `False` now refuses `B1_OWNER_EXECUTION_MODE_MISMATCH`. Legacy TEST_ONLY stores without this new metadata column fail closed (`B1_OWNER_MODE_BINDING_MISSING`); no silent migration.
- The `middle_state_ids` and `middle_state_record_hashes` arrays are cumulative state inventory. The new `new_middle_state_ids` / `new_middle_state_record_hashes` arrays and `durable_psychological_transition` are **per-operation**, derived from a committed row/transition/owner decision delta. `TEST_ONLY_VALID_EMPTY_NO_NEW_MEDIATOR` and `TEST_ONLY_JOURNAL_ONLY_NO_DURABLE_EFFECT` do not assert a new state effect.
- Full P2, B3A, HQ300, M01 and BP2P4J owner tests are not run here; inherited results remain historical evidence.
