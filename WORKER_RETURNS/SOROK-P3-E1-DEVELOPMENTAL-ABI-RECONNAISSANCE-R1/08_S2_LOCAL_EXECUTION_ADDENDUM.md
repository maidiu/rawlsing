# S2 local execution addendum — PR #735 new head

**Status:** `S2_LOCAL_EXECUTION_PASS_AT_992779441__INDEPENDENT_R02_REACCEPTANCE_REQUIRED`. This is executor evidence, not independent R02 reacceptance, not native science and not a protected merge.

**PR:** #735.
**Executed head:** `9927794414e6b5737c5e6dbd2001b7eb7474744d`.
**Previously reviewed head:** `ee1ff298fe7e57277c34a5af16df33165743d84f`.
**Protected start:** `c852d7516e23fcb6cf2215e9be7c5fa268503516`.
**Host:** macOS 13.7.8 x86_64; CPython 3.11.3; pytest 9.1.1.
**Model reported:** `opencode/deepseek-v4.1-flash`; reasoning effort not machine-observable.

The R02 repair return correctly said its own S2 tests had not been run. This addendum records the actual local execution at the new head and the corrected command path.

## Corrected S2 command

The historical `WORKER_RETURNS/SOROK-V2-HQ324-B1-COUPLED-DEVELOPMENT-R1` directory is not present in the protected tree. The probe now vendors the byte-identical B1 author test and fixture, so the court is runnable from a clean checkout:

```bash
python3 -B -m pytest -q -p no:cacheprovider WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1/tests/test_engine.py
python3 -B -m pytest -q -p no:cacheprovider WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1/tests/test_model_cycle.py

cd WORKER_RETURNS/SOROK-P3-E1-DEVELOPMENTAL-ABI-RECONNAISSANCE-R1/probe/vendor/B1
python3 -B -m pytest -q -p no:cacheprovider test_bfirst.py

cd ../..
python3 -B -m pytest -q -p no:cacheprovider test_b1_owner_adapter.py
python3 -B run_probe.py
```

The vendored files are pinned to B1 commit `c0f4588c158b40c8903b4aae2f292eae5238b8a0`:

| File | Git blob | SHA-256 |
|---|---|---|
| `vendor/B1/bfirst.py` | `94ffc52847e4c8ae760212d1bc8543594ba793fa` | `478b989730f49a5def41a367b6f53e4aae9c80961f7f466fe669c7dbd92201a3` |
| `vendor/B1/test_bfirst.py` | `e5dd007382ab9cb3df58fc6b089ecd83f94b670f` | `973c2363c18741ef820d9f38a323234140db68d4d5b6ef3758f782a493a0c407` |
| `vendor/B1/scenario.json` | `2f0c6f0d3a451cce3a3df68a417244ee243cf6b6` | `4610650d290993c464d1aa7ba7aacf34a1cfe0afa801ff0494a052122e59cd0b` |

## Executed results

| Court | Result |
|---|---|
| Vendored B1 author court | **39 passed** in 0.51 s |
| Engine core | **45 passed** in 0.86 s |
| Engine coordinator | **19 passed** in 0.25 s |
| B1 → `DevelopmentOwner` adapter | **13 passed** in 0.86 s |
| `run_probe.py` (subprocess court + scenarios + guard) | **exit 0**; 13 tests, 0 failures/errors/skips |

`probe/receipts/PROBE_RECEIPT.json` now records the 13-test run and the same causal contrast:

```text
positive statuses            REALIZED, NO_CHANGE, REALIZED
control statuses             IMMEDIATE_ONLY, IMMEDIATE_ONLY, IMMEDIATE_ONLY
positive later activity      joint_check:caretaker
control later activity       inspect_alone:caretaker
same later event hash        true
production guard             DENY_ZERO_EFFECT / ZERO_POSITIVE_REGISTRY
```

The new R02 cases specifically pass:

- per-event `new_middle_state_ids` / `new_middle_state_record_hashes` are non-empty only on the event that commits the mediator; event 2 and event 3 report zero new targets while retaining the cumulative inventory;
- journal-only events report `TEST_ONLY_JOURNAL_ONLY_NO_DURABLE_EFFECT` and no new targets;
- mode-flipped cold reopen is refused with `B1_OWNER_EXECUTION_MODE_MISMATCH`;
- same-mode cold continuation works and retains the expected later action;
- mode metadata tamper refuses, and exact restoration restores the original snapshot.

## Evidence files

- `probe/receipts/PROBE_RECEIPT.json` — regenerated 13-test receipt at head `992779441`.
- `probe/receipts/junit.xml` — regenerated JUnit.
- `probe/source_pin.json` — includes the vendored B1 author court pins.
- `probe/receipts/INHERITED_TEST_RUNS.json` — updated counts and S2 addendum metadata.

## What this does not establish

No native CAN-008/CAN-011/ADP-016/ADP-017 issuance, no O05/O07/C9/O15 acceptance, no P2 actor-root psychological store or later P2 consumer, no independent B, no original V3 archive recovery, no protected receiving and no human validation. Independent R02 re-review of the actual new head remains required; this addendum is not a self-acceptance.
